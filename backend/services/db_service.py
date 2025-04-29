import httpx
from core.config import DB_SERVICE_URL
from schemas.user_profile_schemas import UserProfileCreate

async def get_user_by_username(username: str) -> dict | None:
    """
    Retrieves user data from the database microservice by username.

    Args:
        username (str): Unique username identifier.

    Returns:
        dict | None: User metadata (must include 'id') or None on failure.
    """
    url = f"{DB_SERVICE_URL}/users/{username}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"[DB] GET /users/{{username}} failed: {e}")
            return None


async def get_user_profile_by_id(user_id: int) -> dict | None:
    """
    Retrieves a user's profile from the database microservice by ID.

    Args:
        user_id (int): Unique user ID.

    Returns:
        dict | None: Existing profile data or None if not found.
    """
    url = f"{DB_SERVICE_URL}/users/{user_id}/profile"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None


async def update_user_profile(user_id: int, profile_data: UserProfileCreate) -> dict | None:
    """
    Sends updated profile data to the database microservice.

    Args:
        user_id (int): Unique user ID.
        profile_data (UserProfileCreate): Fields to update or create.

    Returns:
        dict | None: Updated profile on success, None on failure.
    """
    url = f"{DB_SERVICE_URL}/users/{user_id}/profile"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=profile_data.dict(exclude_unset=True))
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"[DB] PUT /users/{{id}}/profile failed: {e}")
            return None


async def get_latest_user_plan(user_id: int) -> dict | None:
    """
    Retrieves the latest workout plan for a given user from the database microservice.

    Args:
        user_id (int): Unique user ID.

    Returns:
        dict | None: Latest workout plan data, or None if not found.
    """
    url = f"{DB_SERVICE_URL}/users/{user_id}/plans/last"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()  # Returns the plan data as a Python dictionary
        except httpx.HTTPError as e:
            print(f"[DB] GET /users/{user_id}/plans/last failed: {e}")
            return None