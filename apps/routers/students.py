# from typing import List, Optional
# from fastapi import APIRouter, Depends, Response, status, HTTPException
# from sqlalchemy import func
# from sqlalchemy.orm import Session
# from apps import schemas
# from apps.schemas import PostBase
# from .. import models
# from ..database import get_db

# router = APIRouter(prefix="/students", tags=['students'])



# # @router.get('/{id}', status_code=status.HTTP_302_FOUND, response_model=List[schemas.StudentsOut])
# # async def get_student_by_id(id: int, db: Session = Depends(get_db)):
# #     query_res = db.query(models.Students).where(models.Students.id_no == id).first()
# #     return query_res

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

