from datetime import datetime
import logging
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, logger, status, HTTPException
from apps import models, schemas
from apps.database import get_db
from apps.oauth import create_access_token
from apps.routers.location.JWTDecoder import verify_token

router = APIRouter(tags=['CPHUB'])


@router.post('/signup',
             # More appropriate status code for resource creation
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.Token)
async def sign_up(data: schemas.SignUp, db: Session = Depends(get_db)):
    try:
        # Combined query using OR to check all unique constraints in a single database call
        existing_user = db.query(models.Users).filter(
            (models.Users.user_email == data.user_email) |
            (models.Users.user_name == data.user_name) |
            (models.Users.cf_handle == data.cf_handle)
        ).first()

        if existing_user:
            # More specific error messages
            if existing_user.user_email == data.user_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )
            if existing_user.user_name == data.user_name:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already taken"
                )
            if existing_user.cf_handle == data.cf_handle:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Codeforces handle already in use"
                )

        # Hash password before storing (using passlib recommended)
        hashed_password = data.password

        # Create user with dictionary unpacking
        new_user = models.Users(
            **data.dict(exclude={'password'}),
            password_hash=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Refresh to get database-generated fields

        return schemas.Token(token=str(create_access_token(data.dict())))

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        logging.critical(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not complete registration"
        )


@router.post('/signin', status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def sign_in(data: schemas.SignIn, db: Session = Depends(get_db)):
    try:
        # add password hash check with public key
        query = db.query(models.Users).where(
            models.Users.user_email == data.user_email)
        if not query.first():
            raise HTTPException(detail="Incorrect credentials",
                                status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            query_res = query.first()
            if (query_res.password_hash == data.password):
                return schemas.Token(token=create_access_token({
                    "user_email": query_res.user_email,
                    "user_name": query_res.user_name,
                    "cf_handle": query_res.cf_handle,
                    "cf_rating": query_res.cf_rating,
                    "year": query_res.year
                }))
            else:
                raise HTTPException(
                    detail="Incorrect credentials", status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
