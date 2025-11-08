from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.database import get_db
from ..schemas import schemas
from ..services import user_service
from ..utils.common import create_unified_response


router = APIRouter(prefix="/auth", tags=["Authentication"])

# 注册或登录，用于用户注册或登录
@router.post("/registerorlogin", response_model=schemas.UnifiedResponse)
async def registerorlogin(form: schemas.LoginRegisterForm, db: AsyncSession = Depends(get_db)):
    token_data = await user_service.register_or_login(db=db, form=form)
    return create_unified_response(data=token_data)