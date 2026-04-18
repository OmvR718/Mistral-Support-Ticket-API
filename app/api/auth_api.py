from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_database
from app.schemas.auth import LoginRequest, SignUpRequest
from app.services.auth_service import login_user, signup_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: SignUpRequest, db: Session = Depends(get_database)):
    return signup_user(db, payload)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_database)):
    return login_user(db, payload)
