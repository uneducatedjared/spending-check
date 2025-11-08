from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..config.database import get_db
from ..schemas import schemas
from ..security.auth import get_current_user
from ..services import ticket_service

router = APIRouter()


# 创建ticket，只有employee可以创建
@router.post("/create", response_model=schemas.TicketOut)
async def create_ticket(
    payload: schemas.TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await ticket_service.create_ticket(db=db, user=current_user, payload=payload)


# 列出ticket，employee和employer看到不同的视角
@router.get("/", response_model=List[schemas.TicketOut])
async def list_tickets(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await ticket_service.get_tickets(db=db, current_user=current_user)


# 更新ticket状态，只有employer可以更新
@router.put("/{ticket_id}", response_model=schemas.TicketOut)
async def update_ticket_status(ticket_id: int, status: schemas.TicketStatusUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    updated = await ticket_service.update_ticket_status(db=db, current_user=current_user, ticket_id=ticket_id, status=status.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated
