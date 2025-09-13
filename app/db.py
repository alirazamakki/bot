# === FILE: app/db.py ===
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database (creates app.db in project root)
DATABASE_URL = "sqlite:///app.db"

# SQLAlchemy engine & session factory
ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

# Base class for models
Base = declarative_base()

def get_session():
    """Return a new SQLAlchemy session."""
    return SessionLocal()
