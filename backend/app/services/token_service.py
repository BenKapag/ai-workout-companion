# token_service.py
# Responsible for generating and verifying JWT tokens used for user authentication

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

# Secret key to sign and verify JWTs (keep this secret in production!)
SECRET_KEY = "super-secret-dev-key"  #store in environment variable
ALGORITHM = "HS256"  # JWT signing algorithm 
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token validity period (in minutes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT access token containing the provided payload data.

    Parameters:
    - data: Dictionary with claims (e.g., {'sub': username})
    - expires_delta: Optional timedelta to customize token lifespan

    Returns:
    - A signed JWT string that expires after the given duration
    """
    # Copy the original payload so we don’t mutate it
    to_encode = data.copy()

    # Set token expiration (default to 30 minutes if not provided)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # Add the expiration claim to the payload
    to_encode.update({"exp": expire})

    # Encode the payload into a JWT using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
