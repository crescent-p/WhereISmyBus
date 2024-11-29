from cmath import sqrt
from datetime import datetime, time
from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from apps import schemas
from apps.algorithms import calculate_distance
# from apps.routers.location.location_classes import BusArrayEntry, Contributor, DistIndex
from apps.routers.location.location_classes import BusArrayEntry, Contributor, DistIndex
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
from typing import Set




allowed_time = 1500 # seconds

busArray: List[BusArrayEntry] = []



async def remove_redundant_buses():
    while True:
        busArrayjson = redis.get("busarray")
        if busArrayjson:
            busArray = json.loads(busArrayjson)
            for bus in busArray:
                confidence = bus['confidence']
                elapsed_time = datetime.now() - datetime.fromisoformat(bus['last_updated'])
                if elapsed_time.total_seconds() > confidence * allowed_time:
                    busArray.remove(bus)
            redis.set("busarray", json.dumps([bus.to_dict() for bus in busArray]))
        await asyncio.sleep(15)

# Start the background task
# asyncio.create_task(remove_redundant_buses())



@router.get('/', status_code=status.HTTP_200_OK, response_model=schemas.BusList)
async def get_bus_locations(secret: str, redis: Session = Depends(get_redis)):

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
async def set_bus_locations(secret: str, location: schemas.LocationData, redis: Session = Depends(get_redis)):

    busArrayjson = redis.get("busarray")
    if busArrayjson:
        busArray: List[BusArrayEntry] = [BusArrayEntry(**bus) for bus in json.loads(busArrayjson)]
    else:
        busArray: List[BusArrayEntry] = []

    possibleLocation: List[DistIndex] = []
    for index, i in enumerate(busArray):
        dist = calculate_distance(latitude1=location.latitude, longitude1=location.longitude,
                                  latitude2=i.latitude, longitude2=i.longitude)
        if dist < 200:
            possibleLocation.append(DistIndex(dist=dist, index=index))

    if not possibleLocation:
        entry = BusArrayEntry(
            latitude=location.latitude,
            longitude=location.longitude,
            speed=location.speed,
            last_updated=datetime.now(),
            contributors={str(location.uuid)},
            no_of_contributors=1,
            confidence=1,
            name="Unknown"
        )
        busArray.append(entry)
    else:
        possibleLocation.sort(key=lambda x: x.dist)
        index: int = possibleLocation[0].index
        busArray[index].confidence += 1
        busArray[index].latitude = location.latitude
        busArray[index].longitude = location.longitude
        busArray[index].last_updated = datetime.now()
        busArray[index].speed = location.speed
        busArray[index].contributors.add(str(location.uuid))
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

