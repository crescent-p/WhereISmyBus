from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy import func
import uuid


class Users(Base):
    """Model representing a user."""
    __tablename__ = "users"

    email = Column(String, primary_key=True, nullable=False,
                   unique=True)  # Set unique=True for email
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    last_accessed = Column(TIMESTAMP(timezone=True),
                           server_default=text('now()'), nullable=True)
    picture = Column(String, nullable=True)
    # Set nullable=False if it must be unique
    sub = Column(String, unique=True, nullable=False)
    about_me = Column(String, nullable=True)
    picture_url = Column(
        String, nullable=True, server_default="https://cdn.vectorstock.com/i/1000v/92/16/default-profile-picture-avatar-user-icon-vector-46389216.jpg")
    notification_id = Column(String, nullable=True)

    # Corrected relationship definition
    notifications = relationship("Notification", back_populates="user")
    # Added relationship for posts
    posts = relationship("Post", back_populates="user")
    # Added relationship for comments
    comments = relationship("Comment", back_populates="user")


class Notification(Base):
    """Model representing a notification."""
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)

    user = relationship("Users", back_populates="notifications")


class Post(Base):
    """Model representing a post."""
    __tablename__ = "post"

    user_email = Column(String, ForeignKey("users.email"), nullable=False)
    type = Column(String, nullable=False)
    uuid = Column(String, primary_key=True,
                  default=lambda: str(uuid.uuid4()), nullable=False)
    high_res_image_url = Column(String, nullable=True)
    image = Column(String, nullable=True)
    description = Column(String, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    datetime = Column(TIMESTAMP(timezone=True),
                      server_default=func.now(), nullable=False)

    comments = relationship("Comment", back_populates="post")
    # Added relationship to Users
    user = relationship("Users", back_populates="posts")


class Comment(Base):
    """Model representing a comment."""
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    post_uuid = Column(String, ForeignKey("post.uuid"), nullable=False)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
    text = Column(String, nullable=False)
    datetime = Column(TIMESTAMP(timezone=True),
                      server_default=func.now(), nullable=False)

    post = relationship("Post", back_populates="comments")
    # Added relationship to Users
    user = relationship("Users", back_populates="comments")
