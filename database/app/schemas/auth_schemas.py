# auth_schemas.py

from typing import List, Optional
from pydantic import BaseModel,Field


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


# Schema for user that exist in the database and returned in responses
class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str  

    class Config:
        from_attributes = True