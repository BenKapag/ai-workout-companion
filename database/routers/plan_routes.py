from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import WorkoutPlan
from schemas.plan_schemas import WorkoutPlanResponse  

router = APIRouter()

@router.get("/users/{user_id}/plans/last", response_model=WorkoutPlanResponse)
def get_latest_workout_plan_for_user(
    user_id: int = Path(..., description="ID of the user to fetch the latest workout plan for"),
    db: Session = Depends(get_db)
):
    """
    Retrieve the latest workout plan created for a given user.

    - Returns the most recent plan based on creation timestamp.
    - Raises 404 if the user has no workout plans.

    Args:
        user_id (int): Unique ID of the user.

    Returns:
        WorkoutPlanResponse: Details of the latest workout plan.
    """

    # Query the most recent workout plan for the given user
    latest_plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user_id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    # Handle case where user has no plans
    if not latest_plan:
        raise HTTPException(status_code=404, detail="No workout plans found for this user")

    return latest_plan
