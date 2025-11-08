from datetime import datetime, timezone
from typing import Any


def now_utc() -> datetime:
    """Return current UTC time with tzinfo."""
    return datetime.now(timezone.utc)


def create_unified_response(
    data: Any = None,
    code: int = 200,
    detail: str = "Success"
):
    """
    创建一个统一格式的 API 响应。
    """
    return {
        "code": code,
        "detail": detail,
        "data": data
    }