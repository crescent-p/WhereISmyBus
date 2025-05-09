from datetime import datetime
import string
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect, status, types
from fastapi.responses import FileResponse
import shutil
import os
from apps import schemas
from requests import Session
from apps import models
from apps.database import get_db
from ..database import get_redis, r as redis

router = APIRouter(prefix="/social", tags=['social'])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# active_connections: Dict[str, List[WebSocket]] = {}


# def get_post_channel(val: str):
#     return "channel" + val + "hiyaa"


# @router.websocket("/ws/{post_id}")
# async def add_websocket_with_postid(websocket: WebSocket, post_id: str):

#     await websocket.accept()

#     post_channel = get_post_channel(post_id)

#     if post_channel not in active_connections:
#         active_connections[post_channel] = []

#     active_connections[post_channel].append(websocket)

#     try:
#         while True:
#             data = await websocket.receive_text()  # Just keeping connection alive
#     except WebSocketDisconnect:
#         active_connections[post_channel].remove(websocket)


# async def redis_listener():
#     """Listens to Redis Pub/Sub and forwards messages to WebSocket clients"""
#     pubsub = redis.pubsub()

#     # Subscribe to an admin channel that notifies when a new post is added
#     pubsub.subscribe("new_posts_channel")

#     subscribed_channels = set()

#     while True:
#         message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
#         if message:
#             channel = message["channel"]
#             data = message["data"]

#             # If a new post is added, subscribe to its channel
#             if channel == "new_posts_channel":
#                 post_id = data
#                 post_channel = get_post_channel(post_id)

#                 if post_channel not in subscribed_channels:
#                     await pubsub.subscribe(post_channel)
#                     subscribed_channels.add(post_channel)

#             # If a comment is posted, send it to WebSocket clients
#             elif channel in subscribed_channels:
#                 comment = data
#                 if channel in active_connections:
#                     for ws in active_connections[channel]:
#                         try:
#                             await ws.send_text(comment)
#                         except:
#                             active_connections[channel].remove(ws)


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "File uploaded successfully"}


@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
    return {"error": "File not found"}
# , status_code=status.HTTP_200_OK, response_model=schemas.StudentsOut
# get post by uuid


@router.get("/get_post", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def get_post_by_uuid(uuid: str, db: Session = Depends(get_db)):
    if not db.query(models.Post).where(models.Post.uuid == uuid).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Couldn't find the given post")
    query = db.query(models.Post).where(models.Post.uuid == uuid).first()
    return query


@router.post("/comment", status_code=status.HTTP_200_OK)
async def create_comment_with_post_id(comment: schemas.CreateComment, db: Session = Depends(get_db)):
    if not db.query(models.Post).where(models.Post.uuid == comment.post_uuid).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The post with said UUID is not present")
    try:
        new_comment = models.Comment(**comment.model_dump())
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/miniposts", status_code=status.HTTP_200_OK, response_model=Dict[str, List[schemas.MiniPost]])
async def get_mini_posts(limit: int, db: Session = Depends(get_db)):
    mini_posts: Dict[str, schemas.MiniPost] = {}
    post_types = db.query(models.Post.type).distinct().all()
    for post_type in post_types:
        mini_post = db.query(models.Post).order_by(models.Post.datetime.desc()).where(
            models.Post.type == post_type[0]).limit(limit).all()
        posts = []
        for post in mini_post:
            posts.append(schemas.MiniPost(  # Use dot notation to access attributes
                type=post.type,
                uuid=post.uuid,
                imageUrl=post.high_res_image_url,
                heading=post.heading,
                venue=post.venue))
        mini_posts[post_type[0]] = (posts)
    return mini_posts


@router.post("/post", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/comment", status_code=status.HTTP_200_OK, response_model=schemas.GetComment)
async def get_comments(post_id: str, cursor: Optional[datetime] = None, limit: int = 10, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).order_by(
        models.Comment.datetime.desc())
    if cursor:
        comments = comments.where(
            models.Comment.post_uuid == post_id, models.Comment.datetime > cursor)
    else:
        comments = comments.where(models.Comment.post_uuid == post_id)
    comments_list = comments.limit(limit).all()
    result = schemas.GetComment(
        body=comments_list, cursor=comments_list[-1].datetime if comments_list else None)
    return result


@router.get("/posts_by_type", status_code=status.HTTP_200_OK, response_model=schemas.GetPostByType)
async def get_posts_by_type(post_type: str, cursor: Optional[datetime] = None, limit: int = 10, db: Session = Depends(get_db)):
    print(db.query(models.Post).order_by(models.Post.datetime).where(
        models.Post.type == post_type).limit(limit))
    if cursor:
        qposts = db.query(models.Post).order_by(models.Post.datetime).where(
            models.Post.type == post_type, models.Post.datetime > cursor).limit(limit).all()
    else:
        qposts = db.query(models.Post).order_by(models.Post.datetime).where(
            models.Post.type == post_type).limit(limit).all()
    post_list: List[schemas.Post] = qposts
    res = schemas.GetPostByType(
        posts=post_list, cursor=qposts[-1].datetime if qposts else None)
    return res


def convert_to_pydantic(notification: models.Notification) -> schemas.Notification:
    return schemas.Notification(
        id=notification.id,
        message=notification.message,
        created_at=notification.created_at,
    )


@router.get("/notification", status_code=status.HTTP_200_OK, response_model=schemas.NotificationOut)
async def get_notifications(cursor: Optional[datetime] = None, limit: int = 10, db: Session = Depends(get_db)):
    notifications = db.query(models.Notification).order_by(
        models.Notification.created_at.desc())
    if cursor:
        notifications = notifications.where(
            models.Notification.created_at > cursor)
    # In your endpoint
    notifications_list = notifications.limit(limit).all()
    pydantic_notifications = [
        convert_to_pydantic(n) for n in notifications_list]

    result = schemas.NotificationOut(
        notifications=pydantic_notifications,
        cursor=notifications_list[-1].created_at if notifications_list else None,
    )
    return result


@router.post("/notification", status_code=status.HTTP_200_OK, response_model=schemas.NotificationOut)
async def create_notification(notification: schemas.CreateNotification, db: Session = Depends(get_db)):
    new_notification = models.Notification(**notification.dict())

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


# get posts based on type
# get first 10 miniposts from each type
