import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/dev_analytics")
    github_token: str | None = os.getenv("GITHUB_TOKEN")
    
    class Config:
        env_file = ".env"

settings = Settings()
