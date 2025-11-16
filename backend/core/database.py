"""
Database configuration and session management
"""

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from .config import settings

# Use SQLite if PostgreSQL is not available
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgresql"):
    # Try PostgreSQL, but fallback to SQLite
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            echo=False
        )
        # Test connection
        with engine.connect() as conn:
            pass
    except Exception:
        # Fallback to SQLite
        DATABASE_URL = "sqlite:///./smartbiz.db"
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=False
        )
else:
    # Create database engine
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
        pool_pre_ping=True,
        echo=False
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database tables
    """
    # Drop and recreate users table to match new schema
    try:
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    except Exception:
        pass
    
    Base.metadata.create_all(bind=engine)
    
    # Ensure DB constraints align with frontend registration (email, password, full_name required)
    try:
        with engine.begin() as conn:
            # Make full_name NOT NULL
            try:
                conn.execute(text("ALTER TABLE users ALTER COLUMN full_name SET NOT NULL"))
            except Exception:
                pass
            # Make hashed_password NOT NULL
            try:
                conn.execute(text("ALTER TABLE users ALTER COLUMN hashed_password SET NOT NULL"))
            except Exception:
                pass
    except Exception:
        # Best-effort; if ALTER fails (e.g., SQLite or already applied), continue
        pass
