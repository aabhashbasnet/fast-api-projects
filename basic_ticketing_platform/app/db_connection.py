from sqlalchemy.ext.asyncio import (
    create_async_engine,
)  # creates async sqlalchgemy engine to interact with db using async/await syntax
from sqlalchemy.orm import (
    sessionmaker,
)  # generates databse session to interact with the database

SQLALCHEMY_DATABASE_URL = (
    "sqlite+aiosqlite:///.database.db"  # connection string for the database
)


def get_engine():  # function that returns an async SQLAlchemy engine
    return create_async_engine(
        SQLALCHEMY_DATABASE_URL, echo=True
    )  # echo=True will log all sql queries
