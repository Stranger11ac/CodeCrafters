from pydantic import BaseSettings, Field
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    secret_key: str = Field(..., env="SECRET_KEY")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
