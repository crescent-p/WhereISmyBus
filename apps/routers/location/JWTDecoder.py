import json
import base64
import logging
import requests
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from google.auth.transport.requests import Request
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from ...database import r as redis
from google.oauth2.id_token import verify_oauth2_token

GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"
CLIENT_ID = "442072746362-u6jruc44l1hj8pkntlkmcio0bs613j01.apps.googleusercontent.com"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_google_public_keys():
    cache = redis.get("keys")
    if cache:
        return json.loads(cache)

    response = requests.get(GOOGLE_CERTS_URL)
    if response.status_code != 200:
        logger.error("Failed to fetch public keys: %s", response.status_code)
        raise Exception("Failed to fetch public keys")

    cache_control = response.headers.get("cache-control", "max-age=200")
    max_age = int(
        next((x.split("=")[1] for x in cache_control.split(",") if "max-age" in x), 200))

    redis.set("keys", json.dumps(response.json()), ex=max_age)
    return response.json()


def construct_rsa_public_key(key_data):
    n = int.from_bytes(base64.urlsafe_b64decode(key_data["n"] + '=='), 'big')
    e = int.from_bytes(base64.urlsafe_b64decode(key_data["e"] + '=='), 'big')
    public_key = rsa.RSAPublicNumbers(e, n).public_key()
    return public_key


def verify_token(token):
    try:
        # Fetch the public keys
        keys = get_google_public_keys()

        # Decode the token header to get the key ID
        headers = decode(
            token, options={"verify_signature": False}, algorithms=["RS256"])
        key_data = keys["keys"][0]["kid"]

        return headers
        # Find the key with the matching key ID
        if not key_data:
            raise ValueError("Public key not found")

        # Construct the RSA public key
        public_key = construct_rsa_public_key(key_data)

        # Verify the token using the public key
        payload = decode(token, public_key, algorithms=[
                         "RS256"], audience=CLIENT_ID)

        # Return the token as it is
        return token
    except ExpiredSignatureError:
        logger.error("Token has expired")
        return None
    except InvalidTokenError:
        logger.error("Invalid token")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
