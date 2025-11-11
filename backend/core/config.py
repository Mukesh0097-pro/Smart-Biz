"""
Configuration management for SmartBiz AI
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # App Config
    APP_NAME: str = "SmartBiz AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://smartbiz-ai.vercel.app"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./smartbiz.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo"
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = ""
    
    # OpenMemory
    MEMORY_STORE_PATH: str = "./memory_store"
    
    # GST API (placeholder)
    GST_API_URL: str = "https://gst.gov.in/api/v1"
    GST_API_KEY: str = ""
    
    # Udyam API (placeholder)
    UDYAM_API_URL: str = ""
    UDYAM_API_KEY: str = ""
    
    # Email Configuration
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@smartbiz.ai"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    
    # File Storage
    UPLOAD_DIR: Path = Path("./uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create necessary directories
os.makedirs(settings.MEMORY_STORE_PATH, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
