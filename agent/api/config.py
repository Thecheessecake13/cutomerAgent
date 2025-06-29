# api/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, EmailStr

class Settings(BaseSettings):
    # Tell Pydantic to load .env and ignore extras
    model_config = SettingsConfigDict(
        env_file = ".env",
        extra    = "ignore",
    )

    # Database URL
    DB_URL: str = Field("sqlite:///./complaints.db", env="DB_URL")

    # (other settings…)

settings = Settings()
