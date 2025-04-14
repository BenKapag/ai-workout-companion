# schemas.py
# Defines data schemas for validation and serialization using Pydantic

from typing import List, Optional
from pydantic import BaseModel

class UserProfileCreate(BaseModel):
    age: Optional[int] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    experience_level: Optional[str] = None
    goal: Optional[str] = None
    equipment: Optional[List[str]] = None
    health_notes: Optional[str] = None

from pydantic import BaseModel

# Schema for incoming registration requests
class UserCreate(BaseModel):
    username: str
    password: str

# Schema for user data returned in responses
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Enables automatic conversion (to json) from SQLAlchemy models


# Request body for /login
class LoginRequest(BaseModel):
    username: str
    password: str

# Response for successful login
class LoginResponse(BaseModel):
    message: str

# Schema for creating new user profile
class UserProfileCreate(BaseModel):
    age: Optional[int] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    experience_level: Optional[str] = None
    goal: Optional[str] = None
    equipment: Optional[List[str]] = None
    health_notes: Optional[str] = None

# Schema for user profile data returned in responses
class UserProfileResponse(BaseModel):
    age: Optional[int]
    height_cm: Optional[int]
    weight_kg: Optional[int]
    experience_level: Optional[str]
    goal: Optional[str]
    equipment: Optional[List[str]]
    health_notes: Optional[str]

    class Config:
        from_attributes = True  # Enables automatic conversion (to json) from SQLAlchemy models
