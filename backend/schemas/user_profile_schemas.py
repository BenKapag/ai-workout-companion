# user_profile_schemas.py

from typing import List, Optional
from pydantic import BaseModel

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