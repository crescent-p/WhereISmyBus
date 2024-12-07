import json
import base64
from jwt import encode, decode
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from ...database import r as redis


GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"
CLIENT_ID = "442072746362-s30fj5ovvkp8ags8d0s8h658t4actmo9.apps.googleusercontent.com"

def get_google_public_keys():
    # Fetch Google's public keys
    cache = redis.get("keys")
    if cache:
        response = json.loads(cache)
        return response
    else:
        response = requests.get(GOOGLE_CERTS_URL)
        if response.status_code != 200:
            raise Exception("Failed to fetch public keys")
        redis.set("keys", json.dumps(response.json()["keys"]), ex=200)
        return response.json()["keys"]

def construct_rsa_public_key(key_data):
    # Construct RSA public key from Google's keys (n, e)
    n = int.from_bytes(base64.urlsafe_b64decode(key_data["n"] + "=="), "big")
    e = int.from_bytes(base64.urlsafe_b64decode(key_data["e"] + "=="), "big")
    public_key = rsa.RSAPublicNumbers(e, n).public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

def verify_token(token):
    try:
        # Decode the token header to extract the key ID (kid)
        headers = json.loads(base64.urlsafe_b64decode(token.split(".")[0] + "=="))
        kid = headers["kid"]
        
        # Fetch Google public keys and find the matching one
        keys = get_google_public_keys()
        key_data = next(key for key in keys if key["kid"] == kid)
        public_key_pem = construct_rsa_public_key(key_data)
        
        try:
            # Decode and verify the token
            payload = decode(
                token,
                public_key_pem,
                algorithms=["RS256"],
                audience=CLIENT_ID,
                issuer="https://accounts.google.com",
                options={"verify_exp": False},
            )
            return payload  # Contains user info like email, name, etc.
        except Exception as e:
            print("Invalid token:", str(e))
            return None
    except Exception as e:
        print("Error verifying token:", str(e))
        return None
