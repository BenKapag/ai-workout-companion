# Import SQLAlchemy tools for defining the table columns and types
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

# Import the Base class we created in database.py
# This tells SQLAlchemy: "any class that inherits from this becomes a database table"
from database import Base

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
    goal = Column(String)
    equipment = Column(JSON)  # Stored as a list of strings (e.g., ["dumbbells", "barbell"])
    health_notes = Column(String)

    # Back-reference to the associated User
    user = relationship("User", back_populates="profile")  

