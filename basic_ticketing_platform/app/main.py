from fastapi import FastAPI, Depends, HTTPException, Path
from app.database import Base
from app.db_connection import AsyncSession, get_db_session, get_engine
from pydantic import BaseModel
from app.operations import create_ticket, get_ticket, update_ticket_price, delete_ticket
from contextlib import asynccontextmanager


# Lifespan context for creating tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


# ------------------------
# Pydantic models
# ------------------------
class TicketCreate(BaseModel):
    show_name: str
    user: str | None = None
    price: float | None = None


class TicketResponse(BaseModel):
    id: int
    show: str | None
    user: str | None
    price: float | None

    class Config:
        from_attributes = True


class TicketPriceUpdate(BaseModel):
    new_price: float


# ------------------------
# Dependency
# ------------------------
async def get_db() -> AsyncSession:
    async for session in get_db_session():
        yield session


# ------------------------
# Create ticket
# ------------------------
@app.post("/tickets/", response_model=TicketResponse)
async def create_new_ticket(
    ticket_data: TicketCreate, db: AsyncSession = Depends(get_db)
):
    ticket_id = await create_ticket(
        db_session=db,
        show_name=ticket_data.show_name,
        user=ticket_data.user,
        price=ticket_data.price,
    )
    created_ticket = await get_ticket(db, ticket_id)
    if not created_ticket:
        raise HTTPException(status_code=500, detail="Failed to create ticket")
    return created_ticket


# ------------------------
# Get ticket by ID
# ------------------------
@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def read_ticket(
    ticket_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)
):
    ticket = await get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# ------------------------
# Update ticket price
# ------------------------
@app.patch("/tickets/{ticket_id}/price", response_model=dict)
async def update_ticket(
    ticket_id: int, price_update: TicketPriceUpdate, db: AsyncSession = Depends(get_db)
):
    success = await update_ticket_price(db, ticket_id, price_update.new_price)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket price updated successfully"}


# ------------------------
# Delete ticket
# ------------------------
@app.delete("/tickets/{ticket_id}", response_model=dict)
async def remove_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted successfully"}
