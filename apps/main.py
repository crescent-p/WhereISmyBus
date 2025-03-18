
# setting up the database. Creating the table and all
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from fastapi import Depends, FastAPI, status
from requests import session
from apps import models
from apps.database import engine, get_db
from apps.routers import students, auth
from apps.routers import cphub
from apps.routers import social
from fastapi import FastAPI
import firebase_admin
from firebase_admin import messaging, credentials
from apps.routers.location.locations import remove_redundant_buses

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    # Allow requests from localhost
    allow_origins=["http://localhost", "http://127.0.0.1", "*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/', status_code=status.HTTP_200_OK)
async def test():
    return {"message": "all good boi!!"}


@app.on_event("startup")
async def startup_event():
    session = next(get_db())
    # asyncio.create_task(models.WeeklyLeaderBoard.schedule_weekly_reset(session))

app.include_router(cphub.router)
