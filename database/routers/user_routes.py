# routers/user_routes.py
# Contains all user-related API endpoints: user registration and profile creation/update

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, UserProfile
from schemas import UserCreate, UserResponse, UserProfileCreate
from sqlalchemy import func

# Create a router object to group user-related endpoints
router = APIRouter()

# Dependency to provide a DB session to each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.

    - Accepts: `username`, `password` (expected to be pre-hashed by backend)
    - Returns: the created user's `id` and `username`
    - Rejects: if the username is already taken
    """

    # Check if username is already taken
    existing_user = db.query(User).filter(func.lower(User.username) == user.username.lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create a new user object
    new_user = User(
        username=user.username,
        hashed_password=user.password  # backend should send hashed password
    )

    # Persist the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Load the generated ID

    return new_user


@router.put("/users/{user_id}/profile")
def update_profile(
    profile_data: UserProfileCreate,
    user_id: int = Path(..., description="User ID whose profile is being updated"),
    db: Session = Depends(get_db)
):
    """
    Create or update a user profile.

    - Accepts: optional fields such as `age`, `goal`, `equipment`, etc.
    - If the profile exists, updates only provided fields.
    - If not, creates a new profile linked to the user.
    - Returns: a confirmation message.
    """

    # Ensure the user exists before updating/creating a profile
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.profile:
        # Update existing profile fields that were submitted
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(user.profile, field, value)
    else:
        # Create a new profile associated with the user
        new_profile = UserProfile(**profile_data.dict(), user_id=user_id)
        db.add(new_profile)

    db.commit()
    return {"message": "Profile updated or created successfully"}
