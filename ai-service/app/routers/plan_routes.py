# app/routers/plan_routes.py

from fastapi import APIRouter, HTTPException
from app.schemas.plan_schemas import AIPlanRequest, WorkoutPlan
from app.services.llm_client import generate_plan_with_llm

router = APIRouter()

@router.post("/ai/generate",response_model = WorkoutPlan)
def generate_workout_plan(request_data:AIPlanRequest):
    """
    Endpoint to generate a personalized workout plan.

    This route receives the user's fitness profile and (optionally) their previous workout plan,
    uses the AI agent to generate a new plan, and returns it.

    Args:
        request_data (AIPlanRequest): Includes user_profile and last_plan (optional)

    Returns:
        WorkoutPlan: The AI-generated workout plan
    """

    try:
        # Call the core logic to generate a new plan
        new_plan = generate_plan_with_llm(request_data.user_profile, request_data.last_plan, request_data.allowed_exercises)
        return new_plan

    except Exception as e:
        # Catch any unexpected logic issues
        raise HTTPException(status_code=500, detail=f"Failed to generate workout plan: {str(e)}")