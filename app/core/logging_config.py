import sys

from loguru import logger
from app.core.config import settings


def configure_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
        enqueue=True,
        backtrace=settings.ENVIRONMENT.lower() != "production",
        diagnose=settings.ENVIRONMENT.lower() != "production",
        serialize=settings.ENVIRONMENT.lower() == "production",
    )
