from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..schemas.schemas import LoginRegisterForm
from ..repository import crud
from . import auth as auth_service


async def register_or_login(db: AsyncSession, form: LoginRegisterForm):
    """
    Handles user login or registration.
    - If user exists, attempts to log them in.
    - If user does not exist, creates a new user.
    Returns token data on success.
    Raises HTTPException on failure (e.g., wrong password, suspended user).
    """
    # Check if the user already exists
    user = await crud.get_user_by_email(db, email=form.email)

    if user:
        # --- Login Logic ---
        if user.is_suspended:
            raise HTTPException(status_code=403, detail="User is suspended")

        if not auth_service.verify_password(form.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        # User is authenticated, create and return token data
        token = auth_service.create_access_token({"sub": user.email, "role": user.role})
        return {"access_token": token, "user": user.email, "role": user.role}

    # --- Registration Logic ---
    # If user does not exist, create a new one
    # If username or role not provided, don't attempt to create yet.
    # Let the frontend know the user doesn't exist so it can collect missing details.
    if not form.username or not form.role:
        # 404 signals that the user/email was not found and registration details are required
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = auth_service.get_password_hash(form.password)

    new_user = await crud.create_user(
        db,
        email=form.email,
        password=hashed_password,
        username=form.username,
        role=form.role,
    )

    # Create and return a token for the new user
    token = auth_service.create_access_token({"sub": new_user.email, "role": new_user.role})
    return {"access_token": token, "user": new_user.email, "role": new_user.role}