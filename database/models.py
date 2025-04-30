# Import SQLAlchemy tools for defining the table columns and types
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime


# This tells SQLAlchemy: "any class that inherits from this becomes a database table"

# Base class for declaring ORM models (tables)
# All models should inherit from this
Base = declarative_base()

# Represents the authenticated user (login credentials only)
class User(Base):
    # This is the name of the table in PostgreSQL
    __tablename__ = "users"

    # This is the primary key column — each user will have a unique ID
    id = Column(Integer, primary_key=True, index=True)

    # This column stores the username (must be unique and not empty)
    username = Column(String, unique=True, index=True, nullable=False)

    # This column stores the password — but encrypted (hashed)
    hashed_password = Column(String, nullable=False)

     # Relationship to profile (one-to-one)
    profile = relationship("UserProfile", back_populates="user", uselist=False)


# Represents the extended profile data for each user
class UserProfile(Base):
    #name of the table in PostgreSQL
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # One-to-one foreign key relationship with users table
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Core profile fields used to personalize training plans
    age = Column(Integer)
    height_cm = Column(Integer)
    weight_kg = Column(Integer)
    experience_level = Column(String)
    fitness_goal = Column(String)
    equipment = Column(JSON)  # Stored as a list of strings (e.g., ["dumbbells", "barbell"])
    health_notes = Column(String)

    # Back-reference to the associated User
    user = relationship("User", back_populates="profile")  



class WorkoutPlan(Base):
    """
    Represents a full workout plan generated for a user.
    Each plan can contain multiple WorkoutDays (e.g., Day 1: Chest, Day 2: Back, etc.).
    """

    __tablename__ = "workout_plans"

    # Primary key: unique ID for each plan
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the user who owns this plan
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # When the plan was created (auto set when plan is generated)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Optional metadata fields copied from user profile when plan is generated
    duration_weeks = Column(Integer, nullable=True)  # Example: 4, 8, 12 weeks
    goal = Column(String, nullable=True)             # Example: "muscle_gain", "fat_loss"
    experience_level = Column(String, nullable=True) # Example: "beginner", "intermediate", "advanced"

    # Status of the plan: active (current), completed (finished), archived (old)
    status = Column(String, default="active", nullable=False)

    # Relationship: One WorkoutPlan -> Many WorkoutDays
    days = relationship(
        "WorkoutDay",
        back_populates="plan",
        cascade="all, delete-orphan"
    )




class WorkoutDay(Base):
    """
    Represents a single training day inside a user's workout plan.
    Example: "Day 1: Chest + Triceps"
    """

    __tablename__ = "workout_days"  # Table name in PostgreSQL

    # Primary key: Unique ID for each workout day
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the WorkoutPlan this day belongs to
    plan_id = Column(Integer, ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False)

    # Day number inside the plan (1, 2, 3, etc.)
    day_number = Column(Integer, nullable=False)

    # Optional name for the day ("Day 1", "Monday", etc.)
    day_name = Column(String, nullable=True)

    # Optional focus for the day ("Chest + Triceps", "Rest Day", etc.)
    focus = Column(String, nullable=True)

    # Relationship: One WorkoutDay -> Many WorkoutExercises
    exercises = relationship(
        "WorkoutExercise", 
        back_populates="day", 
        cascade="all, delete-orphan"
    )

    plan = relationship(
        "WorkoutPlan",
        back_populates="days"
    )




class WorkoutExercise(Base):
    """
    Represents a single exercise assigned to a specific WorkoutDay.
    Each WorkoutExercise links to a master ExerciseCatalog entry.
    """

    __tablename__ = "workout_exercises"  # Table name in PostgreSQL

    # Primary key: Unique ID for each workout exercise instance
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to the WorkoutDay this exercise belongs to
    day_id = Column(Integer, ForeignKey("workout_days.id", ondelete="CASCADE"), nullable=False)

    # Foreign key to the ExerciseCatalog entry (the real exercise data)
    exercise_catalog_id = Column(Integer, ForeignKey("exercise_catalog.id"), nullable=False)

    # Number of sets for this exercise
    sets = Column(Integer, nullable=True)  # Optional because some exercises could be "stretch" without sets

    # Number of reps per set
    reps = Column(Integer, nullable=True)  # Optional because some exercises could be "time-based" (e.g., plank)

    # Optional notes from the AI agent or backend
    notes = Column(String, nullable=True)  # e.g., "Focus on slow negatives", "Pause at bottom position"

    # Relationships
    day = relationship("WorkoutDay", back_populates="exercises")
    exercise = relationship("ExerciseCatalog", back_populates="workout_instances")


class ExerciseCatalog(Base):
    """
    Represents a master list of official exercises available in the app.
    Used to generate workout plans and ensure consistent exercise naming.
    """

    __tablename__ = "exercise_catalog"  # Table name in PostgreSQL

    # Primary key: Unique ID for each exercise
    id = Column(Integer, primary_key=True, index=True)

    # Name of the exercise (e.g., "Barbell Bench Press")
    name = Column(String, unique=True, nullable=False)

    # Primary muscle group targeted (e.g., "Chest")
    primary_muscle = Column(String, nullable=True)

    # Secondary muscle group (optional) (e.g., "Triceps")
    secondary_muscle = Column(String, nullable=True)

    # Equipment required (e.g., "Barbell", "Dumbbell", "Bodyweight")
    equipment = Column(String, nullable=False)

    # Difficulty level (e.g., "Beginner", "Intermediate", "Advanced")
    difficulty = Column(String, nullable=True)

    # Relationship: One ExerciseCatalog entry -> Many WorkoutExercise instances
    workout_instances = relationship(
        "WorkoutExercise",
        back_populates="exercise"
    )