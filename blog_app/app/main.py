from fastapi import FastAPI
from app.routers import blog
from app.database import engine, Base
from app.models.blog import Blog  # import all models here

app = FastAPI(title="Blog App")

app.include_router(blog.router)


@app.on_event("startup")
async def on_startup():
    """
    Automatically create tables when the app starts.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")
