from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    ENVIRONMENT: str = Field("production", env="ENVIRONMENT")
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    MONGO_URI: str = Field(..., env=["MONGODB_URL", "MONGO_URI"])
    MONGO_DB_NAME: str = Field("chama_db", env="DATABASE_NAME")
    JWT_SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(10080, env="REFRESH_TOKEN_EXPIRE_MINUTES")
    MPESA_ENV: str = Field("sandbox", env="MPESA_ENV")
    MPESA_CONSUMER_KEY: Optional[str] = Field(None, env="MPESA_CONSUMER_KEY")
    MPESA_CONSUMER_SECRET: Optional[str] = Field(None, env="MPESA_CONSUMER_SECRET")
    MPESA_SHORTCODE: Optional[str] = Field(None, env="MPESA_SHORTCODE")
    MPESA_PASSKEY: Optional[str] = Field(None, env="MPESA_PASSKEY")
    MPESA_CALLBACK_URL: Optional[str] = Field(None, env="MPESA_CALLBACK_URL")
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    CORS_ORIGINS: str = Field("", env="CORS_ORIGINS")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(None, env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(None, env="TWILIO_AUTH_TOKEN")
    TWILIO_FROM_PHONE: Optional[str] = Field(None, env="TWILIO_FROM_PHONE")

settings = Settings()