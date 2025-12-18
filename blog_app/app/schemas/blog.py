from pydantic import BaseModel
from datetime import datetime


class BlogCreate(BaseModel):
    title: str
    content: str
    author: str


class BlogRead(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime

    model_config = {"from_attributes": True}
