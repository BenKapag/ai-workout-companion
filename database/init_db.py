# init_db.py
# This script creates all tables defined in models.py using SQLAlchemy

from database import Base, engine
from models import User, UserProfile  # all models we create in the database

# Create all tables in the database
# This will check if they exist already, and only create if they don't
Base.metadata.create_all(bind=engine)
