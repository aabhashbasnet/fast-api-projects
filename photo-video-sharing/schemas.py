from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class PostCreate(BaseModel):
    caption: Optional[str] = None


class PostResponse(BaseModel):
    id: int
    file_path: str
    caption: Optional[str]
    created_at: datetime
    owner_id: int

    model_config = {"from_attributes": True}
