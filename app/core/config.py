from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    MONGO_URI: str = Field(..., env="MONGODB_URL")
    MONGO_DB_NAME: str = Field("chama_db", env="DATABASE_NAME")
    JWT_SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(1440, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    MPESA_CONSUMER_KEY: str = Field(..., env="MPESA_CONSUMER_KEY")
    MPESA_CONSUMER_SECRET: str = Field(..., env="MPESA_CONSUMER_SECRET")
    MPESA_SHORTCODE: str = Field(..., env="MPESA_SHORTCODE")
    MPESA_PASSKEY: str = Field(..., env="MPESA_PASSKEY")
    MPESA_CALLBACK_URL: str = Field(..., env="MPESA_CALLBACK_URL")
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()