from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, conint


class UpdatedLocation(BaseModel):
    message: str

class FetchedLocation(BaseModel):
    message : str
    # locations: List[str]

class Authenticated(BaseModel):
    secret: str





class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: Optional[datetime]
    user_id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)


class Students(BaseModel):
    name: str
    address: str
    email: str
    phone_number: str
    address: str
    status: Optional[conint(ge=0, le=1)] #0 means temporary 1 means Permanent

class StudentsOut(BaseModel):
    id_no: int
    name: str
    address: str
    email: str
    phone_number: str
    status: str
    date_of_issue: datetime
    date_of_expiry: datetime

    class Config:
        from_attributes = True
        
class Books(BaseModel):
    book_name: str
    author_id: int
    price: float
    rack_no: int
    no_of_books: Optional[int] = 1

class BooksOut(Books):
    author_name: str
    book_code: int
    date_of_arrival: datetime

class Issues(BaseModel):
    student_id : int
    book_id: int

class IssuesOut(Issues):
    student: StudentsOut 
    book: BooksOut
    issue_date: datetime
    due_date: datetime

class Author(BaseModel):
    name: str
    email: str
    phone_number: str


class AuthorOut(Author):
    id: int

class StudentIssues(BaseModel):
    student: StudentsOut
    issue: Issues

    class Config:
        from_attributes = True

class Request(BaseModel):
    book_name: str
    ISBN: str

class RequestOut(Request):
    class Config:
        from_attributes = True