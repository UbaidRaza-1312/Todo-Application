import logging
import sys
from datetime import datetime
from typing import Any, Dict

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)

# Also add to the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def log_info(message: str, extra: Dict[str, Any] = None) -> None:
    """Log an info message"""
    logger.info(message, extra=extra)

def log_error(message: str, extra: Dict[str, Any] = None) -> None:
    """Log an error message"""
    logger.error(message, extra=extra)

def log_warning(message: str, extra: Dict[str, Any] = None) -> None:
    """Log a warning message"""
    logger.warning(message, extra=extra)

def log_debug(message: str, extra: Dict[str, Any] = None) -> None:
    """Log a debug message"""
    logger.debug(message, extra=extra)