# routers/plan_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_dependency import get_current_user  # Dependency to extract current user from JWT token
from app.services.db_service import get_user_by_username, get_user_profile_by_id, get_latest_user_plan
from app.services.db_service import save_workout_plan_to_db, db_service_get, db_service_delete
from app.services.ai_service import get_generated_plan_by_ai
from app.services.cache_service import get_allowed_exercise_names
from app.schemas.plan_schemas import WorkoutPlanResponse,GeneratedPlanResponse
import httpx
from app.core.config import DB_SERVICE_URL
import copy
from typing import Optional,List
import json


# Initialize router for workout plan generation
router = APIRouter()


@router.post("/generate-plan",response_model=GeneratedPlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_workout_plan(
    username: str = Depends(get_current_user)
):
    """
    Generates a new workout plan for the authenticated user.

    Workflow:
    1. Fetch full user record from the database using the username from the token.
    2. Fetch user's profile from the database microservice.
    3. Fetch user's latest workout plan (if exists).
    4. (For now) Mock the AI agent's response to generate a new workout plan.
    5. Save the generated plan into the database microservice.
    6. Return a success message to the frontend.

    Returns:
        JSON message confirming successful plan generation and saving.
    """

    #Fetch user full metadata
    user = await get_user_by_username(username)
    if not user or "id" not in user:
        raise HTTPException(status_code=404, detail="User not found.")

    user_id = user["id"]

    #Fetch user's profile
    user_profile = await get_user_profile_by_id(user_id)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please complete your profile before generating a plan."
        )

    #Fetch user's latest workout plan (if any)
    last_plan = await get_latest_user_plan(user_id)
    # Note: last_plan might be None if it's a new user — that's OK

    #Fetch the allowed exercises name and equipment list to the ai agent
    allowed_exercises = await get_allowed_exercise_names()

    #fetch the generated plan from the ai agent
    generated_plan = await get_generated_plan_by_ai(user_profile,last_plan,allowed_exercises)

    #Save the generated plan into the database microservice
    payload = copy.deepcopy(generated_plan)
    payload["user_id"] = user_id  # Attach the correct user ID

    created_plan_id  = await save_workout_plan_to_db(payload)

    if not created_plan_id:
        raise HTTPException(
             status_code=status.HTTP_502_BAD_GATEWAY,
             detail="Failed to save the workout plan to the database."
    )

    try:
        created_plan = await db_service_get(f"/workout-plans/{created_plan_id}")
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(
        status_code=e.response.status_code,
        detail=e.response.json().get("detail", str(e))
    )
    except Exception as e:
        raise HTTPException(
        status_code=502,
        detail=f"Failed to fetch the saved workout plan: {str(e)}"
    )


    #Return a success response to the frontend
    return {"message": "Workout plan generated and saved successfully!",
            "plan_id":created_plan_id,
            "plan": created_plan}



@router.get("/plans",response_model=List[WorkoutPlanResponse])
async def get_user_plans(
    status: Optional[str] = None,
    current_user: str = Depends(get_current_user)
):
    """
    Get workout plans for the logged-in user.
    Optionally filter by status (e.g., 'active', 'archived').
    """

    #Fetch user full metadata
    user = await get_user_by_username(current_user)
    if not user or "id" not in user:
        raise HTTPException(status_code=404, detail="User not found.")

    user_id = user["id"]

    try:
        # Build query string
        query_string = f"?user_id={user_id}"
        if status:
            query_string += f"&status={status}"

        # Send request to DB microservice
        response = await db_service_get(f"/workout-plans{query_string}")
        return response

    except httpx.HTTPStatusError as e:
        # Pass through status + message from DB microservice (e.g. 404)
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.json().get("detail", str(e))
        )

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch plans: {str(e)}")
    
    


@router.get("/plan/{plan_id}", response_model=WorkoutPlanResponse)
async def get_plan_by_id(plan_id: int):
    """
    Fetch a specific workout plan by its ID.

    - Calls the database microservice's /workout-plans/{plan_id} endpoint
    - Returns the full nested plan structure (days, exercises, etc.)
    - Raises 404 or 502 depending on error type
    """
    try:
        return await db_service_get(f"/workout-plans/{plan_id}")
    
    except httpx.HTTPStatusError as e:
        # Propagate status from the DB microservice (e.g. 404)
        error_detail = e.response.json()
        raise HTTPException(
            status_code=e.response.status_code,
            detail=error_detail.get("detail", str(e))
        )
    
    except Exception as e:
        # Fallback for any unexpected error
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch workout plan: {str(e)}"
        )


@router.delete("/plan/{plan_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan_by_id(plan_id: int,username: str = Depends(get_current_user)):

    """
    Deletes a workout plan for the authenticated user.

    - Forwards the request to the database microservice
    - Returns 204 No Content on success
    - Returns 404 if plan not found
    - Returns 502 on unexpected failure
    (we can improve it in the future and make a safety check that the plan really belongs to the specific username)
    """

    try:
        await db_service_delete(f"/workout-plans/{plan_id}")
    
    except httpx.HTTPStatusError as e:
        # Propagate status from the DB microservice (e.g. 404)
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.json().get("detail", str(e))
        )
    
    except Exception as e:
        # Fallback for any unexpected error
        raise HTTPException(
            status_code=502,
            detail=f"Failed to delete workout plan: {str(e)}"
        )

