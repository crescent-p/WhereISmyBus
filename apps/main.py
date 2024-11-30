import asyncio
from fastapi import  FastAPI, status
from apps import models
from apps.database import engine
from apps.routers import students, auth
from apps.routers.location import locations

from apps.routers.location.locations import remove_redundant_buses

##setting up the database. Creating the table and all
models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "*"],  # Allow requests from localhost
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/', status_code=status.HTTP_200_OK)
async def test():
    return {"message": "all good boi!!"}


@app.on_event("startup")
async def startup_event():
    # Schedule the coroutine on startup
    asyncio.create_task(remove_redundant_buses())

app.include_router(locations.router)
# app.include_router(students.router)
# app.include_router(auth.router)




