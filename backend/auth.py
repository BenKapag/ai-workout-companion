# auth.py
# Contains the /register route logic for user sign-up

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.hash import bcrypt
from database import SessionLocal  # DB session creator
from models import User,UserProfile  # SQLAlchemy model
from schemas import UserCreate, UserResponse,LoginRequest,LoginResponse,UserProfileCreate,UserProfileResponse  # Pydantic schemas

# Create a FastAPI router to group auth-related routes
router = APIRouter()

# Dependency to create and close a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user if the username is available.
    Hashes the password before saving.
    Returns the new user's public data.
    """
    # Check if the username already exists
    existing_user = db.query(User).filter(func.lower(User.username) == user.username.lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Securely hash the plaintext password
    hashed_password = bcrypt.hash(user.password)

    # Create a new user object
    new_user = User(username=user.username, hashed_password=hashed_password)

    # Save to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get the generated ID

    return new_user


@router.post("/login", response_model=LoginResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    # Look up user by username
    db_user = db.query(User).filter(func.lower(User.username) == user.username.lower()).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Check password
    if not bcrypt.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"message": f"Welcome back, {db_user.username}!"}

# Temporary version for testing authenticated routes
def get_current_user(db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == 1).first()


@router.put("/profile")
def update_profile(
    profile_data: UserProfileCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Creates or updates the authenticated user's profile.

    - If a profile exists, only the provided fields are updated.
    - If no profile exists, a new one is created and linked to the user.
    - Required fields are enforced only during initial profile creation.
    """

    # Validate required fields for first-time profile creation
    if not user.profile:
        required_fields = ["age", "height_cm", "weight_kg", "experience_level", "goal"]
        missing = [
            field for field in required_fields
            if profile_data.dict().get(field) is None
        ]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields: {', '.join(missing)}"
            )

    # Update existing profile
    if user.profile:
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(user.profile, field, value)

    # Create new profile if none exists
    else:
        new_profile = UserProfile(**profile_data.dict(), user_id=user.id)
        db.add(new_profile)

    db.commit()
    return {"message": "Profile saved successfully."}



#Returns the authenticated user's profile data.
@router.get("/profile", response_model=UserProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    
    # raises 404 if the profile does not exist.
    if not user.profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return user.profile

