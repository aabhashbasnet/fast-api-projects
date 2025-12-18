from contextlib import (
    asynccontextmanager,
)  # decorator to define an asynchronous context manager which can be used with asunc with , useful for setup and cleanup task
from fastapi import FastAPI
from app.database import Base
from app.db_connection import AsyncSessionLocal, get_db_session, get_engine


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):  # defines a lifespan context manager for FastAPI, to run startup and shutdown code
    engine = (
        get_engine()
    )  # calls get_engine() to create async engine connected to the db
    async with engine.begin() as conn:  # create tables if they dont exist
        await conn.run_sync(Base.metadata.create_all)
        yield  # yield statemtn pauses the lifespan func here and lets the fast api run
    await engine.dispose()  # after the app stops, this line closes the db connection pool and releases resources


app = FastAPI(
    lifespan=lifespan
)  # Passes the lifespan context manager to FastAPI., fast api will automatically run the starttup[ code before the first req(create table) and run the shutdown code adter the app stop (dispose engine)]
