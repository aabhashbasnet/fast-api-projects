from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.database import Ticket


# function to create a ticket


async def create_ticket(
    db_session: AsyncSession,  # as async sqlalchemy session to interact with the database
    show_name: str,  # #name of the show for the ticket
    user: str = None,  # the name or identifier of trhe user purchasing the ticket
    price: float = None,  # the price of the ticket
) -> int:
    ticket = Ticket(
        show=show_name, user=user, price=price
    )  # creates a python object of the ticket class

    async with db_session.begin():  # db_session.begin() ensures that all operations inside thuis block are part of single transaction, ife error occurs it will rollback automatically
        db_session.add(ticket)  # registers the ticket object with the session
        await db_session.flush()  # flush sends all pending changes to the db without commiting
        ticket_id = ticket.id  # retrieves the auto generated primary key oif the ticket
        await db_session.commit()  # makes the insert permanent in the database
    return ticket_id  # returns the id of the newly created ticket to the caller


# function to get a ticket


async def get_ticket(db_session: AsyncSession, ticket_id: int) -> Ticket | None:
    query = select(Ticket).where(Ticket.id == ticket_id)
    async with db_session as session:
        tickets = await session.execute(
            query
        )  # runs the query asunchronously against the database
        return (
            tickets.scalars().first()
        )  # tickets.scalrs() - extracts the actual orm objects(Ticket instance) fom the result


# function to update the price of the ticket


async def update_ticket_price(
    db_session: AsyncSession,
    ticket_id: int,
    new_price: float,
) -> bool:
    query = (
        update(Ticket).where(Ticket.id == ticket_id).values(price=new_price)
    )  # SQLAlchemy generates a single UPDATE query that directly updates the row.
    async with db_session as session:
        ticket_updated = await session.execute(query)
        await session.commit()
        if ticket_updated.rowcount == 0:
            return False
        return True


# function to delete a ticket


async def delete_ticket(db_session: AsyncSession, ticket_id: int) -> bool:
    async with db_session as session:
        tickets_removed = await session.execute(
            delete(Ticket).where(Ticket.id == ticket_id)
        )
        await session.commit()

        if tickets_removed.rowcount == 0:
            return False
        return True
