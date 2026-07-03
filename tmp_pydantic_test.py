from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

os.environ['MONGODB_URL'] = 'mongodb://test'
os.environ['SECRET_KEY'] = 'abc'

class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    MONGO_URI: str = Field(..., env=['MONGODB_URL', 'MONGO_URI'])
    JWT_SECRET_KEY: str = Field(..., env='SECRET_KEY')

s = TestSettings()
print('MONGO_URI', s.MONGO_URI)
print('JWT_SECRET_KEY', s.JWT_SECRET_KEY)
