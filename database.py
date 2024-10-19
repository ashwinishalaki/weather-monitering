
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL (SQLite)
DATABASE_URL = "sqlite:///database/weather_data.db"

# Create database directory if it doesn't exist
os.makedirs('database', exist_ok=True)

# Create an engine that manages the SQLite connection
engine = create_engine('sqlite:///database/weather_data.db', echo=False)

# Create tables based on the models
from models import Base
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session manager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
