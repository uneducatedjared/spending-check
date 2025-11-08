from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..config.database import get_db
from ..schemas import schemas
from ..security.auth import is_employer  # 导入 is_employer 权限检查
from ..services import employee_service
from ..models import models

# 这个 router 专门给 employer 使用
router = APIRouter()

@router.get("/", response_model=List[schemas.UserOut])
async def list_employees(
    db: AsyncSession = Depends(get_db), 
    current_employer: models.User = Depends(is_employer) # 注入权限检查
):
    """
    列出所有员工。只有 employer 可以访问。
    """
    return await employee_service.list_employees(db=db, current_user=current_employer)


@router.patch("/{employee_id}/status", response_model=schemas.UserOut)
async def update_employee_status(
    employee_id: int,
    payload: schemas.EmployeeSuspensionUpdate,
    db: AsyncSession = Depends(get_db),
    current_employer: models.User = Depends(is_employer),
):
    """
    更新员工的禁用状态 (禁用或重新激活)。
    只有 employer 可以访问。
    """
    updated_employee = await employee_service.set_suspension(
        db=db,
        current_user=current_employer,
        employee_id=employee_id,
        suspend=payload.is_suspended,
    )
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee