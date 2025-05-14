# auth_schemas.py

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