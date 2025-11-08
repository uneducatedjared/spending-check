from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from ..repository import crud

async def list_employees(db: AsyncSession, current_user):
    # only employers may list employees
    if current_user.role != "employer":
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.get_all_employees(db)


async def set_suspension(db: AsyncSession, current_user, employee_id: int, suspend: bool = True):
    if current_user.role != "employer":
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.set_employee_suspension(db, employee_id, suspend=suspend)