from typing import Optional, TypeVar, Generic
from pydantic import BaseModel, EmailStr
import datetime
from pydantic.generics import GenericModel


T = TypeVar('T')

class UnifiedResponse(GenericModel, Generic[T]):
    code: int = 200
    detail: str = "Success"
    data: Optional[T] = None


class LoginRegisterForm(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    role: Optional[str] = None  # 'employee' or 'employer'


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    is_suspended: bool

    class Config:
        orm_mode = True


class TicketCreate(BaseModel):
    name: str
    amount: float
    link: str
    when: datetime.datetime


class TicketOut(BaseModel):
    id: int
    name: str
    when: datetime.datetime
    amount: float
    link: Optional[str] = None
    user_id: int
    status: str

    class Config:
        orm_mode = True


class TicketStatusUpdate(BaseModel):
    status: str

class EmployeeSuspensionUpdate(BaseModel):
    is_suspended: bool