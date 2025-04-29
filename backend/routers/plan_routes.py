# routers/plan_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from services.auth_dependency import get_current_user  # Dependency to extract current user from JWT token
from services.db_service import get_user_by_username, get_user_profile_by_id, get_latest_user_plan
import httpx
from core.config import DB_SERVICE_URL


# Initialize router for workout plan generation
router = APIRouter(
    prefix="/generate-plan",
    tags=["Workout Plans"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
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

    #(Temporary)!!!!!!! Mock AI Agent response
    generated_plan = {
    "duration_weeks": 8,
    "goal": user_profile.get("fitness_goal", "General Fitness"),
    "experience_level": user_profile.get("experience_level", "Beginner"),
    "days": [
        {
            "day_number": 1,
            "day_name": "Chest Day",
            "focus": "Chest + Triceps",
            "exercises": [
                {
                    "exercise_name": "Barbell Bench Press",
                    "equipment": "Barbell",
                    "sets": 4,
                    "reps": 8,
                    "notes": "Use full range of motion"
                },
                {
                    "exercise_name": "Incline Dumbbell Press",
                    "equipment": "Dumbbell",
                    "sets": 3,
                    "reps": 10,
                    "notes": "Pause at the bottom"
                },
                {
                    "exercise_name": "Triceps Pushdown",
                    "equipment": "Cable Machine",
                    "sets": 3,
                    "reps": 12,
                    "notes": None
                }
            ]
        },
        {
            "day_number": 2,
            "day_name": "Back Day",
            "focus": "Back + Biceps",
            "exercises": [
                {
                    "exercise_name": "Deadlift",
                    "equipment": "Barbell",
                    "sets": 4,
                    "reps": 5,
                    "notes": "Maintain straight back posture"
                },
                {
                    "exercise_name": "Seated Row",
                    "equipment": "Cable Machine",
                    "sets": 3,
                    "reps": 10,
                    "notes": "Squeeze shoulder blades at end"
                },
                {
                    "exercise_name": "Barbell Curl",
                    "equipment": "Barbell",
                    "sets": 3,
                    "reps": 12,
                    "notes": None
                }
            ]
        }
    ]
}

    #Save the generated plan into the database microservice
    payload = generated_plan
    payload["user_id"] = user_id  # Attach the correct user ID

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{DB_SERVICE_URL}/plans",
                json=payload
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to communicate with database service: {str(e)}"
        )

    if response.status_code != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database service error: {response.text}"
        )

    #Return a success response to the frontend
    return {"message": "Workout plan generated and saved successfully!"}
