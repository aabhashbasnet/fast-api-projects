from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from auth import get_current_user
from models import Post
from schemas import PostCreate, PostResponse
from typing import List

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    new_post = Post(
        file_path="uploads/dummy.jpg",
        caption=post.caption,
        owner_id=user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[PostResponse])
def feed(db: Session = Depends(get_db)):
    return db.query(Post).order_by(Post.created_at.desc()).all()
