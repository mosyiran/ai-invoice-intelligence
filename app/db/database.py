
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database directory
DATABASE_DIR = BASE_DIR / "database"

# Create directory if it does not exist
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database file
DATABASE_PATH = DATABASE_DIR / "invoices.db"

# Database URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Database session dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
