from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_database
from app.core.security import get_current_user_id_from_token

http_bearer = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_database)
) -> int:
    """
    Dependency to get current user ID from JWT token
    """
    try:
        user_id = get_current_user_id_from_token(credentials.credentials)
        return user_id
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_id_optional(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_database)
) -> int | None:
    """
    Optional authentication - returns None if no token provided
    """
    if credentials is None:
        return None
    try:
        user_id = get_current_user_id_from_token(credentials.credentials)
        return user_id
    except ValueError:
        return None
