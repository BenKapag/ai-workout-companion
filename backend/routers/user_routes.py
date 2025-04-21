# routers/user_routes.py

from fastapi import APIRouter, HTTPException,Depends,status
from schemas import RegisterRequest,RegisterResponse,LoginRequest,TokenLoginResponse,UserProfileCreate,UserProfileResponse
from passlib.context import CryptContext
from services.token_service import create_access_token
from services.auth_dependency import get_current_user
from services.db_service import get_user_by_username,get_user_profile_by_id,update_user_profile
import httpx

# Create the API router for user-related endpoints
router = APIRouter()

# Password hashing configuration using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database microservice URL (update if needed for Docker later)
DATABASE_SERVICE_URL = "http://localhost:8001"


@router.post("/register", response_model=RegisterResponse)
async def register_user(user: RegisterRequest):
    """
    Handles user registration:
    - Hashes the password
    - Sends the data to the DB service
    - Returns the new user's ID and username
    """
    hashed_pw = hash_password(user.password)

    data_to_send = {
        "username": user.username,
        "password": hashed_pw
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{DATABASE_SERVICE_URL}/users", json=data_to_send)

        if response.status_code != 201:
            error_message = response.json()  # Parse the actual error from the DB
            raise HTTPException(status_code=response.status_code, detail=error_message["detail"])

        # Parse the DB service response into our Pydantic response model
        response_data = response.json()
        return RegisterResponse(**response_data)

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Database service unreachable: {e}")


@router.post("/login", response_model=TokenLoginResponse)
async def login_user(login_credentials: LoginRequest):
    """
    Logs a user in by:
    - Fetching their data from the database microservice by username
    - Verifying the submitted password matches the hashed password in the DB
    - Returning a success message and jwt token on match or an error otherwise
    """

    try:
        # Make a GET request to the DB microservice to fetch user by username
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DATABASE_SERVICE_URL}/users/{login_credentials.username}")

        # If the user does not exist in the DB
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")

        # Parse the JSON response from the DB (must contain hashed password)
        user_data = response.json()

        # Verify the password using bcrypt
        if not verify_password(login_credentials.password, user_data["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid password")
        
        #Credentials are valid, generating JWT token to the user autentication
        access_token = create_access_token(data={"sub": login_credentials.username})

        # Login successful — return confirmation
        return TokenLoginResponse(message="Login successful",token=access_token)

    except httpx.RequestError as e:
        # Handle networking errors (e.g., DB service is down)
        raise HTTPException(status_code=500, detail=f"Database service unreachable: {e}")


@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    """
    Returns the username of the currently authenticated user
    based on the JWT token in the Authorization header.
    """
    return {"username": current_user}


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileCreate,
    username: str = Depends(get_current_user)
):
    """
    Creates or updates the authenticated user's profile.

    - On first-time setup, all fields must be provided.
    - On later updates, partial changes are accepted.
    """
    # Fetch user metadata from the database using the username from the token
    user = await get_user_by_username(username)
    if not user or "id" not in user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user["id"]

    # Check if the user already has a profile
    existing_profile = await get_user_profile_by_id(user_id)

    # Enforce complete profile submission on first-time setup
    if not existing_profile:
        missing_fields = [
            field for field, value in profile_data.dict().items()
            if value is None
        ]
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Missing required fields for initial setup: {missing_fields}"
            )

    # Forward the update/create operation to the database microservice
    updated_profile = await update_user_profile(user_id, profile_data)
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update or create profile"
        )

    return updated_profile




#functions that we are using

def hash_password(password: str) -> str:
    """
    Hashes the user's password securely using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against its bcrypt hash.
    """
    return pwd_context.verify(plain_password, hashed_password)