import datetime
from sqlalchemy import String, Integer, DateTime, Float, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ..config.database import Base

# 1. ORM 基类：User
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_suspended: Mapped[bool] = mapped_column(default=False)
    
    role: Mapped[str] = mapped_column(String(50))

    # This relationship will be populated by the Ticket's 'owner' back-reference.
    tickets: Mapped[List["Ticket"]] = relationship(
        back_populates="owner",
        primaryjoin="User.id == foreign(Ticket.user_id)"
    )

    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_identity": "user",
    }

# 2. 子类：Employee
class Employee(User):
    __mapper_args__ = { "polymorphic_identity": "employee" }

# 3. 子类：Employer
class Employer(User):
    __mapper_args__ = { "polymorphic_identity": "employer" }

# 4. Ticket 模型
class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    changer_id: Mapped[int] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    when: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now, onupdate=datetime.datetime.now)

    owner: Mapped["User"] = relationship(
        back_populates="tickets",
        # 2. Use foreign() to mark the foreign key column
        primaryjoin="foreign(Ticket.user_id) == User.id"
    )
    changer: Mapped["User"] = relationship(
        # 3. Also apply it to the changer relationship
        primaryjoin="foreign(Ticket.changer_id) == User.id"
    )