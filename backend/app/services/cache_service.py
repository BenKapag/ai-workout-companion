# backend/app/services/cache_service.py
from fastapi import HTTPException
from app.services.db_service import db_service_get
from functools import lru_cache
import httpx
from typing import List

@lru_cache(maxsize=1)
async def get_allowed_exercise_names() -> List[str]:
    """
    Fetches and caches the list of exercise names from the database microservice.
    This runs only once per app session thanks to LRU caching.

    Returns:
        List[str]: A list of valid exercise names to be used by the AI generator.
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
