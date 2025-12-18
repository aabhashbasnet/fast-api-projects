from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogRead
from typing import List

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/", response_model=BlogRead, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogCreate, db: AsyncSession = Depends(get_db)):
    new_blog = Blog(**blog.model_dump())
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog


@router.get("/{blog_id}", response_model=BlogRead)
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=BlogRead)
async def update_blog(
    blog_id: int, blog_data: BlogCreate, db: AsyncSession = Depends(get_db)
):
    # Correct: db is the session
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Update fields
    blog.title = blog_data.title
    blog.content = blog_data.content
    blog.author = blog_data.author

    db.add(blog)
    await db.commit()
    await db.refresh(blog)
    return blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    await db.delete(blog)
    await db.commit()
    return None


@router.get("/", response_model=List[BlogRead])
async def get_all_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Blog).offset(skip).limit(limit))
    blogs = result.scalars().all()
    return blogs
