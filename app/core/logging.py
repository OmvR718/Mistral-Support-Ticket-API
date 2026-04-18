import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Setup basic logging configuration"""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    
    return logging.getLogger(__name__)

def get_logger(name: str = None):
    """Get a logger instance"""
    return logging.getLogger(name or __name__)
