from fastapi import  FastAPI, status
from apps import models
from apps.database import engine
from apps.routers import students, auth
from apps.routers.location import locations


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

app.include_router(locations.router)
# app.include_router(students.router)
app.include_router(auth.router)




