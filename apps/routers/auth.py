# from datetime import datetime
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends, status, HTTPException
# from apps import schemas
# from apps import utils
# from apps.utils import check, dummy_check, hash
# from apps import models, oauth
# from apps.database import get_db
# from apps.schemas import UserCreate


# router = APIRouter(tags=['Authentication'])


# @router.post('/login', response_model=schemas.Token)
# async def login_user(user: schemas.User, db: Session = Depends(get_db)):
#     userModel = models.Users(**user)
#     userModel.last_accessed = datetime.now()

#     query_res = db.query(models.Users).where(models.Users.id == user.id)

#     if not query_res.first():
#         userModel.created_at = datetime.now()
#         db.add(userModel)
#         return {
#             "token" : oauth.create_access_token(user.id)
#         }
#     else:
#         token = oauth.create_access_token({"user_id": user.id})
#         return {"token": token}
