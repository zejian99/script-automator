from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY:str
    FILE_PATH: str
    SAVE_PATH: str
    GMAIL_USER: str
    GMAIL_PASSWORD: str
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()