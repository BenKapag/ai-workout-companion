# init_db.py
# This script creates all tables defined in models.py using SQLAlchemy

from app.models import Base
from app.db_connection import engine
from app.models import User, UserProfile, WorkoutPlan, WorkoutDay, WorkoutExercise, ExerciseCatalog  # all models we create in the database


# Create all tables in the database
# This will check if they exist already, and only create if they don't
Base.metadata.create_all(bind=engine)

print("all tables created successfully!")