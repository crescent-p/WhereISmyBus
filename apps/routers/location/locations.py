

from cmath import sqrt
from datetime import datetime, time
from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func
from sqlalchemy.orm import Session
from apps import schemas
from apps.algorithms import calculate_distance
# from apps.routers.location.location_classes import BusArrayEntry, Contributor, DistIndex
from apps.routers.location.JWTDecoder import verify_token
from apps.routers.location.location_helper import BusArrayEntry, Contributor, Coordinates, DistIndex, find_closest_location, isInParkingArea, isInside, nameResolve
from apps.schemas import Bus, BusList
from ... import models
from ...database import get_db, get_redis
import asyncio
import json
from ...database import r as redis
router = APIRouter(prefix="/locations", tags=['locations'])

# an array of objects A
# A -> has latitude longitude 
from datetime import datetime
from typing import List, Set

from apps.routers.location.location_helper import BusArrayEntry, Coordinates, DistIndex, find_closest_location, isInParkingArea, isInsideBuilding, isInsideNITC, nameResolve




allowed_time = 1500 # seconds

busArray: List[BusArrayEntry] = []


#if inside parking space add extra time delay

async def remove_redundant_buses():
    while True:
        busArrayjson = redis.get("busarray")
        if busArrayjson:
            busArray: List[BusArrayEntry] = [BusArrayEntry(**bus) for bus in json.loads(busArrayjson)]
        else:
            busArray: List[BusArrayEntry] = []
        if busArray:
            for bus in busArray:
                allowed_time = 1500
                possibleName = nameResolve(Coordinates(latitude=bus.latitude, longitude=bus.longitude))
                if possibleName != "Unknown":
                    bus.name = possibleName
                if isInParkingArea(coordinate=Coordinates(bus.latitude, bus.longitude)):
                    allowed_time = 3000
                    bus.contributors.clear()
                #Sigmoid fucntion to scale up on increased confidence, rises slowly and then very fast.
                confidence = 1/(1 + pow(25, -7*((bus.confidence/100) - 0.2)))
                elapsed_time = datetime.now() - datetime.fromisoformat(bus.last_updated)
                if elapsed_time.total_seconds() > confidence * allowed_time:
                    busArray.remove(bus)
            redis.set("busarray", json.dumps([bus.to_dict() for bus in busArray]))  
        await asyncio.sleep(15)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get('/', status_code=status.HTTP_200_OK, response_model=schemas.BusList)
async def get_bus_locations(token:str = Depends(oauth2_scheme), redis: Session = Depends(get_redis)):
    try:
        decoded_token = verify_token(token=token)
        if not decoded_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Eda eda poda")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Eda eda poda")

    #check if present in redis
    cache = redis.get("buslist")
    if cache:
        return json.loads(cache)
    busArrayjson = redis.get("busarray")
    if busArrayjson:
        busArray: List[BusArrayEntry] = [BusArrayEntry(**bus) for bus in json.loads(busArrayjson)]
    else:
        busArray: List[BusArrayEntry] = []
   
    total_contributors: Set[str] = set()
    
    for bus in busArray:
        total_contributors.update(bus.contributors)


    #add to redis 
    jsonBusList = {
        "buses": [bus.to_dict() for bus in busArray],
        "active_users": len(total_contributors)
    }
    redis.set("buslist", json.dumps(jsonBusList), ex=5)
    return jsonBusList



@router.post('/', status_code=status.HTTP_200_OK, response_model=schemas.UpdatedLocation)
async def set_bus_locations(location: schemas.LocationData, redis: Session = Depends(get_redis), db: Session = Depends(get_db)):
    try:
        decoded_token = verify_token(token=location.token)
        if not decoded_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Eda eda poda")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Eda eda poda")
    
    query = db.query(models.Users).where(models.Users.sub == decoded_token["sub"])
    if not query.first():
        new_user = models.Users()
        new_user.name = decoded_token["name"]
        new_user.picture = decoded_token["picture"]
        new_user.created_at = datetime.now()
        new_user.last_accessed = datetime.now()
        new_user.sub = decoded_token["sub"]
        new_user.email = decoded_token["email"]
        db.add(new_user)
        db.commit()
    else:
        query_res = query.first()
        query_res.last_accessed = datetime.now()
        db.commit()

    coordinate = Coordinates(latitude=location.latitude, longitude=location.longitude)

    if not isInsideNITC(coordinate= coordinate) or location.speed < 3 or isInsideBuilding(coordinate=coordinate):
        
        return {"message" : "Doesn't meet criteria to upload the location"}

    busArrayjson = redis.get("busarray")
    if busArrayjson:
        busArray: List[BusArrayEntry] = [BusArrayEntry(**bus) for bus in json.loads(busArrayjson)]
    else:
        busArray: List[BusArrayEntry] = []

    possibleLocation: List[DistIndex] = []
    for index, i in enumerate(busArray):
        dist = calculate_distance(latitude1=location.latitude, longitude1=location.longitude,
                                  latitude2=i.latitude, longitude2=i.longitude)
        previous_contributor = False
        if str(decoded_token["sub"]) in i.contributors:
            previous_contributor = True
 
        if dist < 200:
            possibleLocation.append(DistIndex(dist=dist, index=index, previous_contributor=previous_contributor))

    if not possibleLocation:
        entry = BusArrayEntry(
            latitude=location.latitude,
            longitude=location.longitude,
            speed=location.speed,
            created_at= datetime.now(),
            last_updated=datetime.now(),
            contributors={str(decoded_token["sub"])},
            no_of_contributors=1,
            location=find_closest_location(Coordinates(latitude=location.latitude, longitude=location.longitude)),
            confidence=1,
            name="Unknown"
        )
        busArray.append(entry)
    else:
        possibleLocation.sort(key=lambda x: x.dist)
        index: int = possibleLocation[0].index

        for item in possibleLocation:
            if item.previous_contributor:
                index = item.index
                break

        busArray[index].confidence += 1
        busArray[index].latitude = location.latitude
        busArray[index].longitude = location.longitude
        busArray[index].last_updated = datetime.now()
        busArray[index].speed = location.speed
        busArray[index].location = find_closest_location(Coordinates(location.latitude, location.longitude))
        busArray[index].contributors.add(str(decoded_token["sub"]))
        busArray[index].no_of_contributors = len(busArray[index].contributors) 
        

    redis.set("busarray", json.dumps([bus.to_dict() for bus in busArray]))
    return {"message": "successfully added"}










# @router.get('/{id}', status_code=status.HTTP_302_FOUND, response_model=List[schemas.StudentsOut])
# async def get_student_by_id(id: int, db: Session = Depends(get_db)):
#     query_res = db.query(models.Students).where(models.Students.id_no == id).first()
#     return query_res

# @router.get('/issues', status_code=status.HTTP_200_OK, response_model=List[schemas.StudentIssues])
# async def get_all_students_with_issues(db: Session = Depends(get_db), limit: int = 10):
#     query = db.query(models.Students, models.Issue).join(models.Issue, models.Students.id_no == models.Issue.student_id, isouter=False).all()
#     result = []
#     for student, issue in query:
#         result.append({"issue": issue, "student": student})
#     return result

# @router.get('/', status_code=status.HTTP_302_FOUND, response_model=List[schemas.StudentsOut])
# async def get_all_students(db: Session = Depends(get_db), limit: int = 10, name: str = ""):
#     query_res = db.query(models.Students).filter(models.Students.name.contains(name)).limit(limit=limit).all()
#     return query_res

# #fix studentsOut
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.StudentsOut)
# async def create_student(user: schemas.Students, db: Session = Depends(get_db)):

#     if db.query(models.Students).where(models.Students.name == user.name).first():
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This username is taken!")

#     if user.status:
#         if user.status == 1:
#             user.status = "Permanent"
#         else:
#             user.status = "Temporary"
#     new_user = models.Students(**user.model_dump())
    
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.StudentsOut)
# async def delete_student(id: int, db: Session = Depends(get_db)):
#     student = db.query(models.Students).where(models.Students.id_no == id)

#     if not student.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="That student doesn't exist!")
    
#     deleted_student = student.first()

#     student.delete() 
#     db.commit()

#     return deleted_student

