# schemas.py
# Defines data schemas for validation and serialization using Pydantic

from typing import List, Optional
from pydantic import BaseModel


# Schema for incoming registration requests
class RegisterRequest(BaseModel):
    username: str
    password: str

# Schema for user data returned in responses
class RegisterResponse(BaseModel):
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
    
#Response for successful login include user jwt token for autentication
class TokenLoginResponse(BaseModel):
    message: str
    token: str

 # Schema used when a user sends new or updated profile data
class UserProfileCreate(BaseModel):
    age: Optional[int] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    experience_level: Optional[str] = None
    fitness_goal: Optional[str] = None
    equipment: Optional[List[str]] = None # e.g., ["dumbbells", "resistance bands"]
    health_notes: Optional[str] = None  


# Schema for user profile data returned in responses
class UserProfileResponse(BaseModel):
    age: Optional[int] 
    height_cm: Optional[int] 
    weight_kg: Optional[int] 
    experience_level: Optional[str]
    fitness_goal: Optional[str] 
    equipment: Optional[List[str]] 
    health_notes: Optional[str] 

    class Config:
        from_attributes = True  # Enables automatic conversion (to json) from SQLAlchemy models
