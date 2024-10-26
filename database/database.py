from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import models  # Import the database models from models.py

# Define the database URL from the environment variable
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/database"

# Create the database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base model for database tables
Base = declarative_base()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Function to get a database session
def get_db():
    """
    Provides a database session for interacting with the database.

    This function creates a new database session, yields it to the calling
    function, and then closes the session after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()