# Basic Ticketing Platform

## Install fast api and the required dependencies

`pip install fastapi[all]`
`pip install -r requirements.txt`

## Source Code

### database.py

```python
from sqlalchemy import Column, Float, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):  # superclass for all the models
    pass


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(nullable=True)
    show: Mapped[str | None]
    user: Mapped[str | None]

```

The Ticket class represents the tickets table in the database. It has four fields: id, price, show, and user. The id field is an integer and serves as the primary key, uniquely identifying each ticket. The price field is a floating-point number and is optional, allowing it to be left empty if needed. The show field stores the name of the show associated with the ticket, while the user field stores the name of the user who owns the ticket. Both show and user are optional string fields.

This setup uses SQLAlchemy 2.0’s Mapped type and mapped_column function to provide type-safe ORM mapping, making the code more readable and compatible with type checkers. The Ticket model can be used to perform create, read, update, and delete (CRUD) operations on ticket records in the database
