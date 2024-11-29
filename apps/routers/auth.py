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
# async def login_user(user_detail: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     query_res= db.query(models.Admin).where(models.Admin.email == user_detail.username).first()
    
#     if not query_res:
#         dummy_check()
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

#     if check(user_detail.password, query_res.password):
#         token = oauth.create_access_token({"user_id": query_res.id})
#         return {"token": token, "token_type": "bearer"}
#     else:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Password")
