from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 500, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class DatabaseException(AppException):
    """Database related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="DATABASE_ERROR")

class AuthenticationException(AppException):
    """Authentication related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=401, error_code="AUTH_ERROR")

class ValidationException(AppException):
    """Validation related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400, error_code="VALIDATION_ERROR")

class AIServiceException(AppException):
    """AI service related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="AI_SERVICE_ERROR")

async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions"""
    logger.error(f"App exception: {exc.error_code} - {exc.message}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code or "APP_ERROR",
                "message": exc.message,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url)
            }
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url)
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions"""
    logger.warning(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": exc.errors(),
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url)
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {type(exc).__name__} - {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url)
            }
        }
    )
