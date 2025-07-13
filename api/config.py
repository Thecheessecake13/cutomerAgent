# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import Field, EmailStr

# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file=".env", extra="ignore")
#     DB_URL: str = Field("sqlite:///./complaints.db", env="DB_URL")

# settings = Settings()

# api/config.py
# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     DB_URL: str = "sqlite:///./complaints.db"

#     class Config:
#         env_file = ".env"
#         extra    = "ignore"

# settings = Settings()


# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file=".env", extra="ignore")
#     DB_URL: str = "sqlite:///./complaints.db"

# settings = Settings()



# api/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # only needed if you keep a .env file

# simple constant or you can wrap in a class if you prefer
DB_URL = os.getenv("DB_URL", "sqlite:///./complaints.db")
