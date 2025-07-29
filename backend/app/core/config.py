from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Harmoniq"
    
    # Database
    DATABASE_URL: str = "sqlite:///./harmoniq.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Tidal API (to be configured)
    TIDAL_CLIENT_ID: Optional[str] = None
    TIDAL_CLIENT_SECRET: Optional[str] = None
    TIDAL_API_BASE_URL: str = "https://api.tidal.com/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 