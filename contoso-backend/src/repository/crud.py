from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from ..models.models import User, Ticket


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalars().first()


async def create_user(db: AsyncSession, email: str, password: str, username: str, role: str):
    """
    Creates a new user in the database.
    Expects the password to be already hashed.
    """
    new_user = User(
        email=email,
        hashed_password=password, # Directly use the provided password (which is already a hash)
        username=username,
        role=role,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def create_ticket(db: AsyncSession, user_id: int, name: str, when: datetime.datetime, amount: float, link: Optional[str] = None):
    ticket = Ticket(user_id=user_id, name=name, when=when, amount=amount, link=link)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


async def get_tickets_by_owner(db: AsyncSession, user_id: int) -> List[Ticket]:
    res = await db.execute(select(Ticket).where(Ticket.user_id == user_id))
    return res.scalars().all()


async def get_all_visible_tickets(db: AsyncSession) -> List[Ticket]:
    # Only tickets whose owner is not suspended should be visible
    res = await db.execute(
        select(Ticket)
        .join(Ticket.owner)
        .where(User.is_suspended == False)
    )
    return res.scalars().all()


async def update_status(db: AsyncSession, current_user, ticket_id: int, new_status: str):
    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = res.scalars().first()
    if not ticket:
        return None
    ticket.status = new_status
    ticket.changer_id = current_user.id
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


async def set_employee_suspension(db: AsyncSession, employee_id: int, suspend: bool = True):
    res = await db.execute(select(User).where(User.id == employee_id))
    user = res.scalars().first()
    if not user:
        return None
    user.is_suspended = suspend
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_all_employees(db: AsyncSession) -> List[User]:
    res = await db.execute(select(User).where(User.role == 'employee'))
    return res.scalars().all()
