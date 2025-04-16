# routers/user_routes.py

from fastapi import APIRouter, HTTPException
from schemas import RegisterRequest,RegisterResponse,LoginRequest,LoginResponse
from passlib.context import CryptContext
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


@router.post("/login", response_model=LoginResponse)
async def login_user(login_credentials: LoginRequest):
    """
    Logs a user in by:
    - Fetching their data from the database microservice by username
    - Verifying the submitted password matches the hashed password in the DB
    - Returning a success message on match or an error otherwise
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
        if not verify_password(login_credentials.password, user_data["password"]):
            raise HTTPException(status_code=401, detail="Invalid password")

        # Login successful — return confirmation
        return LoginResponse(message="Login successful")

    except httpx.RequestError as e:
        # Handle networking errors (e.g., DB service is down)
        raise HTTPException(status_code=500, detail=f"Database service unreachable: {e}")



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