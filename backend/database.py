from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the database connection URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine to connect to PostgreSQL
# This engine manages the connection pool
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
# Used to create session instances for interacting with the database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for declaring ORM models (tables)
# All models should inherit from this
Base = declarative_base()
