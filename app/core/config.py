from pathlib import Path
from typing import Optional
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

class Settings(BaseModel):
    ENVIRONMENT: str = Field(default="production")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    MONGO_URI: str = Field(...)
    MONGO_DB_NAME: str = Field(default="chama_db")
    JWT_SECRET_KEY: str = Field(...)
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=10080)
    MPESA_ENV: str = Field(default="sandbox")
    MPESA_CONSUMER_KEY: Optional[str] = Field(default=None)
    MPESA_CONSUMER_SECRET: Optional[str] = Field(default=None)
    MPESA_SHORTCODE: Optional[str] = Field(default=None)
    MPESA_PASSKEY: Optional[str] = Field(default=None)
    MPESA_CALLBACK_URL: Optional[str] = Field(default=None)
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    CORS_ORIGINS: str = Field(default="")
    LOG_LEVEL: str = Field(default="INFO")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None)
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None)
    TWILIO_FROM_PHONE: Optional[str] = Field(default=None)

    @classmethod
    def from_env(cls):
        return cls(
            ENVIRONMENT=os.getenv("ENVIRONMENT", "production"),
            HOST=os.getenv("HOST", "0.0.0.0"),
            PORT=int(os.getenv("PORT", "8000")),
            MONGO_URI=os.getenv("MONGODB_URL") or os.getenv("MONGO_URI"),
            MONGO_DB_NAME=os.getenv("DATABASE_NAME", "chama_db"),
            JWT_SECRET_KEY=os.getenv("SECRET_KEY"),
            JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256"),
            ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
            REFRESH_TOKEN_EXPIRE_MINUTES=int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080")),
            MPESA_ENV=os.getenv("MPESA_ENV", "sandbox"),
            MPESA_CONSUMER_KEY=os.getenv("MPESA_CONSUMER_KEY"),
            MPESA_CONSUMER_SECRET=os.getenv("MPESA_CONSUMER_SECRET"),
            MPESA_SHORTCODE=os.getenv("MPESA_SHORTCODE"),
            MPESA_PASSKEY=os.getenv("MPESA_PASSKEY"),
            MPESA_CALLBACK_URL=os.getenv("MPESA_CALLBACK_URL"),
            REDIS_URL=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            CORS_ORIGINS=os.getenv("CORS_ORIGINS", ""),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
            TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID"),
            TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN"),
            TWILIO_FROM_PHONE=os.getenv("TWILIO_FROM_PHONE"),
        )

settings = Settings.from_env()