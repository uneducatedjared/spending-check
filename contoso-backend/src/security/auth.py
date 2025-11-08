from typing import Optional
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..config.database import get_db
from ..repository.crud import get_user_by_email
from ..services import auth as auth_svc
from ..models import models

# --- 认证 (Authentication) ---

async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    authorization: Optional[str] = Header(None)
) -> models.User:
    """
    依赖项：从 Authorization: Bearer <token> 请求头中解析、验证并返回当前用户。
    这是所有需要登录的接口的基础。
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization scheme")

    try:
        payload = auth_svc.decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = await get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.is_suspended:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User suspended")
    
    return user


# --- 授权 (Authorization) ---

def is_employee(current_user: models.User = Depends(get_current_user)) -> models.User:
    """
    依赖项：检查当前用户是否是 'employee'。
    """

    # 注意：这里的 current_user.role 依赖于您之前简化的 RBAC 模型。
    if not hasattr(current_user, 'role') or current_user.role != "employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Required role: employee."
        )
    return current_user


def is_employer(current_user: models.User = Depends(get_current_user)) -> models.User:
    """
    依赖项：检查当前用户是否是 'employer'。
    """

    # 注意：这里的 current_user.role 依赖于您之前简化的 RBAC 模型。
    # 如果您已经迁移到了完整的多对多 RBAC 模型，这里的逻辑需要相应调整。
    if not hasattr(current_user, 'role') or current_user.role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Required role: employer."
        )
    return current_user