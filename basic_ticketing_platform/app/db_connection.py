from sqlalchemy.ext.asyncio import (
    create_async_engine,  # Creates an asynchronous SQLAlchemy engine, which allows you to connect and interact with the database using async/await
    AsyncSession,  # Represents an async database session to perform queries and commit transactions asynchronously.
)
from sqlalchemy.orm import (
    sessionmaker,  # generates databse session to interact with the database
)

SQLALCHEMY_DATABASE_URL = (
    "sqlite+aiosqlite:///.database.db"  # connection string for the database
)


def get_engine():  # function that returns an async SQLAlchemy engine
    return create_async_engine(
        SQLALCHEMY_DATABASE_URL, echo=True
    )  # echo=True will log all sql queries


AsyncSessionLocal = sessionmaker(
    autocommit=False,  # changes are not committed automatically
    autoflush=False,  # won't automatically flush changes in to the database
    bind=get_engine(),  # binds the session to the async engine created
    class_=AsyncSession,  # ensures the sessions are asynchronous
)


async def get_db_session():
    async with AsyncSessionLocal() as session:  # opens a session and ensuires it's automaticcdaly closed after use
        yield session  # provides the session for use in fast api endpoints
