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
        

async def save_workout_plan_to_db(plan_data: dict) -> int | None:
    """
    Sends a generated workout plan to the database microservice for saving.

    Args:
        plan_data (dict): Structured plan including user_id, days, exercises

    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{DB_SERVICE_URL}/workout-plans", json=plan_data)
            response.raise_for_status()
            return response.json().get("plan_id")
    except httpx.HTTPError as e:
        print(f"[ERROR] Failed to save workout plan: {e}")
        return None
    
    

async def db_service_get(endpoint: str):
    """
    Sends a GET request to the database microservice.

    Parameters:
    - endpoint: the relative URL path, e.g., "workout-plans?user_id=5"

    Returns:
    - The response JSON (parsed as dict or list)
    - Raises HTTPError if the response fails (caught in your route)
    """
    # Build the full URL safely to avoid double slashes
    url = f"{DB_SERVICE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    # Use async HTTP client to send the request
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        # Raise an exception if the status code is 4xx or 5xx
        response.raise_for_status()

        # Parse and return the response body as JSON (dict or list)
        return response.json()