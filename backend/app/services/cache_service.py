# backend/app/services/cache_service.py
from fastapi import HTTPException
from app.services.db_service import db_service_get
import httpx
from typing import List,Tuple


async def get_allowed_exercise_names() -> List[Tuple[str, str]]:
    """
    Fetches and caches the list of exercise names from the database microservice.

    Returns:
        List[Tuple[str, str]]: A list of valid exercise names to be used by the AI generator.
    """
    try:
        return await db_service_get("/catalog-exercises/names")

    except httpx.HTTPStatusError as e:
        # Pass through status + message from DB microservice (e.g. 404)
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.json().get("detail", str(e))
        )

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch catalog-exercises: {str(e)}")
