from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..schemas.schemas import TicketCreate
from ..repository import crud


async def create_ticket(db: AsyncSession, user, payload: TicketCreate):
    # Only employees can create tickets
    if user.role != "employee":
        raise HTTPException(status_code=403, detail="Only employees can create tickets")
    return await crud.create_ticket(
        db,
        user_id=user.id,
        name=payload.name,      
        when=payload.when,   
        amount=payload.amount,
        link=payload.link,
    )

async def get_tickets(db: AsyncSession, current_user):
    if current_user.role == "employer":
        return await crud.get_all_visible_tickets(db)
    else:
        return await crud.get_tickets_by_owner(db, user_id=current_user.id)


async def update_ticket_status(db: AsyncSession, current_user, ticket_id: int, status: str):
    if current_user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can update ticket status")
    return await crud.update_status(db, current_user, ticket_id, status)
