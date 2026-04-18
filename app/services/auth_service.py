from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.crud.user_crud import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.schemas import LoginRequest, SignUpRequest


def signup_user(db: Session, payload: SignUpRequest):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    password_hash = hash_password(payload.password)
    user = create_user(
        db=db,
        username=payload.username,
        password=password_hash,
        email=payload.email,
    )
    return {"id": user.id, "email": user.email, "username": user.username}


def login_user(db: Session, payload: LoginRequest):
    user = get_user_by_email(db, payload.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
