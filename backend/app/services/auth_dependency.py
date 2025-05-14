# services/auth_dependency.py
# Provides a reusable dependency function to extract and verify JWT from Authorization header

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.services.token_service import SECRET_KEY, ALGORITHM

# FastAPI will automatically look for an Authorization header like: "Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extracts and verifies the JWT token from the Authorization header.
    Returns the username (subject) if valid.
    Raises HTTP 401 if the token is missing, invalid, or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token using our secret and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the 'sub' (subject = username) from the payload
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        return username

    except JWTError:
        # Token is invalid, tampered with, or expired
        raise credentials_exception
