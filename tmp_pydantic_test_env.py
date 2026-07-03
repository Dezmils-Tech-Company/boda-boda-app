import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

os.environ['SECRET_KEY'] = 'abc'
os.environ['MONGODB_URL'] = 'mongodb://localhost/test'

class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    MONGO_URI: str = Field(..., env='MONGODB_URL')
    JWT_SECRET_KEY: str = Field(..., env='SECRET_KEY')

print('ENV SECRET_KEY', os.environ.get('SECRET_KEY'))
print('ENV MONGODB_URL', os.environ.get('MONGODB_URL'))
print('Field MONGO_URI', TestSettings.model_fields['MONGO_URI'])
print('Field JWT_SECRET_KEY', TestSettings.model_fields['JWT_SECRET_KEY'])
try:
    s = TestSettings()
    print('Settings OK', s.MONGO_URI, s.JWT_SECRET_KEY)
except Exception as e:
    import traceback
    traceback.print_exc()
