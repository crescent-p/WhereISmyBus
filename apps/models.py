from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy import func, Interval



class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=True, unique=False)
    name = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone= True), server_default=text('now()'), nullable=False)
    last_accessed = Column(TIMESTAMP(timezone=True), nullable= True)



# class Admin(Base):
#     __tablename__ = "admin"

#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone= True), server_default=text('now()'), nullable=False)

# class Issue(Base):
#     __tablename__ = "issue"

#     student_id = Column(Integer, ForeignKey("students.id_no", ondelete="CASCADE"), nullable=False, primary_key=True)
#     book_id = Column(Integer, ForeignKey("books.book_code", ondelete="CASCADE"), nullable=False, primary_key=True)
#     issue_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
#     due_date = Column(TIMESTAMP(timezone=True), server_default=func.now() + text("interval '3 months'"))

# class Students(Base):
#     __tablename__ = "students"

#     id_no = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     phone_number = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     date_of_issue = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
#     date_of_expiry = Column(TIMESTAMP(timezone=True), server_default=func.now() + text("interval '1 year'"))
#     status = Column(String, default="Permanent", nullable=False)

# class Author(Base):
#     __tablename__ = "author"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     phone_number = Column(String, nullable=False)
#     email = Column(String, nullable=False)

# class Books(Base):
#     __tablename__ = "books"

#     book_name = Column(String, nullable=False)
#     book_code = Column(Integer, primary_key=True)
#     author_id = Column(Integer, ForeignKey("author.id", ondelete="CASCADE"), nullable=False)
#     date_of_arrival = Column(TIMESTAMP(timezone=True), server_default=func.now())
#     price = Column(Float, nullable=False, default=0.0)
#     rack_no = Column(Integer, default=0)
#     no_of_books = Column(Integer, default=0)


# class Request(Base):
#     __tablename__ = "request"

#     book_name = Column(String, nullable=False)
#     ISBN = Column(String, nullable=False, primary_key=True)





