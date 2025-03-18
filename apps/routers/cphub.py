from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from apps import models, schemas
from apps.database import get_db
from apps.oauth import create_access_token
from apps.routers.location.JWTDecoder import verify_token

router = APIRouter(tags=['CPHUB'])


@router.post('/signup', status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def sign_up(data: schemas.SignUp, db: Session = Depends(get_db)):
    # add password hash check with public key
    try:
        query = db.query(models.Users).where(
            models.Users.user_email == data.user_email)
        if not query.first():
            new_user = models.Users()
            new_user.cf_handle = data.cf_handle
            new_user.password_hash = data.password
            new_user.user_name = data.user_name
            new_user.year = data.year
            new_user.user_email = data.user_email
            db.add(new_user)
            db.commit()
        else:
            return HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="User already exists")
        return schemas.Token(token=str(create_access_token(data.dict())))
    except Exception:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, status=str(Exception))


@router.get('/signin', status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def sign_in(data: schemas.SignIn, db: Session = Depends(get_db)):
    try:
        # add password hash check with public key
        query = db.query(models.Users).where(
            models.Users.user_email == data.user_email)
        if not query.first():
            return HTTPException(detail="Incorrect credentials", status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            query_res = query.first()
            if (query_res.password_hash == data.password):
                return create_access_token(**query_res.model_dump())
            else:
                return HTTPException(detail="Incorrect credentials", status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(Exception))
