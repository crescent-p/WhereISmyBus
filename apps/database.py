from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import redis 

r = redis.Redis(host='localhost', port=6379)

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    yield r


# Redis



# #connecting to the database.
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database='fastapi',user='crescent', 
#                                 password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected Succesfully")
#         break
#     except Exception as error:
#         print(str(error))
#         time.sleep(2)
