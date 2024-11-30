# from datetime import datetime, timedelta
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# import jwt
# from sqlalchemy.orm import Session
# from .config import settings
# from apps import models, schemas
# from apps.database import get_db


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_min


# def create_access_token(data: dict):
#     to_encode = data.copy()

#     expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     print(datetime.now())
#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt
 

# def verify_access_token(token: str, credential_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         id: str = payload.get("user_id")

#         if not id:
#             raise credential_exception
#         token_data = schemas.TokenData(id=id)
#     except jwt.:
#         raise credential_exception
#     return token_data
    
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't verify token")

#     token = verify_access_token(token, credential_exception=credential_exception)

#     user = db.query(models.Admin).where(models.Admin.id == token.id).first()

#     return user