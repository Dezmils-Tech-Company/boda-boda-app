import os
from pathlib import Path
from dotenv import load_dotenv

print('os before set', os.environ.get('SECRET_KEY'), os.environ.get('MONGODB_URL'))
os.environ['SECRET_KEY'] = 'abc'
os.environ['MONGODB_URL'] = 'mongodb://test'
print('os after set', os.environ.get('SECRET_KEY'), os.environ.get('MONGODB_URL'))

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    MONGO_URI: str = Field(..., env='MONGODB_URL')

s = TestSettings()
print('Settings', s.SECRET_KEY, s.MONGO_URI)
