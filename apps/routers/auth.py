# from datetime import datetime
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends, status, HTTPException
# from apps.utils.utils import schemas
# from apps.utils import utils
# from apps.utils.JWTDecoder import verify_token
# from apps.utils.utils import check, dummy_check, hash, models
# from apps.utils.utils import oauth
# from apps.utils.database import get_db


# router = APIRouter(tags=['Authentication'])


# @router.post('/signin', status_code=status.HTTP_200_OK, response_model=schemas.Authenticated)
# async def sign_in(location: schemas.Token, db: Session = Depends(get_db)):
#     try:
#         decoded_token = verify_token(token=location.token)
#         if not decoded_token:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Eda eda poda")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Eda eda poda")
    
#     print(decoded_token)
#     query = db.query(models.Users).where(models.Users.sub == decoded_token["sub"])
#     if not query.first():
#         new_user = models.Users()
#         new_user.name = decoded_token["name"]
#         new_user.picture = decoded_token["picture"]
#         new_user.created_at = datetime.now()
#         new_user.last_accessed = datetime.now()
#         new_user.sub = decoded_token["sub"]
#         new_user.email = decoded_token["email"]
#         db.add(new_user)
#         db.commit()
#     else:
#         query_res = query.first()
#         query_res.last_accessed = datetime.now()
#         db.commit()

#     return {"message" : "Success"}
