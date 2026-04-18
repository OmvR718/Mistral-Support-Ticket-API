from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
from app.api.auth_api import router as auth_router
from app.db.database import get_database
from app.api.ticket_api import router as ticket_router
from app.api.ticket_pred_api import router as ticket_pred_router
from app.api.document_api import router as document_router
from app.schemas.common import HealthResponse
from app.core.logging import setup_logging
from app.core.exceptions import (
    AppException, 
    app_exception_handler, 
    http_exception_handler, 
    validation_exception_handler, 
    general_exception_handler
)

# Initialize logging
logger = setup_logging()

app = FastAPI(
    title="Mistral Support Ticket API",
    description="API for managing support tickets with AI-powered classification",
    version="1.0.0"
)

# Add exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get("/health", response_model=HealthResponse)
def check_health(db: Session = Depends(get_database)):
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        database="connected"
    )

app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(ticket_pred_router)
app.include_router(document_router)