from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def check(attempted_password: str, correct_password: str):
    return pwd_context.verify(attempted_password, correct_password)

def dummy_check():
    return pwd_context.dummy_verify()