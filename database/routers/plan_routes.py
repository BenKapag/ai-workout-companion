from fastapi import APIRouter, HTTPException, Depends, Path, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from db_connection import get_db
from models import WorkoutPlan,WorkoutDay, WorkoutExercise, ExerciseCatalog
from schemas.plan_schemas import LastWorkoutPlanResponse,WorkoutPlanCreate,WorkoutPlanResponse
from datetime import datetime
from typing import List, Optional
from services.serializers import serialize_plan


router = APIRouter()

@router.get("/users/{user_id}/plans/last", response_model=LastWorkoutPlanResponse)
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


@router.post("/workout-plans")
def create_workout_plan(plan_data: WorkoutPlanCreate, db: Session = Depends(get_db)):
    """
    Creates a full workout plan:
    - Archives existing active plans for the user
    - Inserts WorkoutPlan
    - Inserts associated WorkoutDays
    - For each day, inserts WorkoutExercises and links to ExerciseCatalog
    """

    #Archive existing active plans for this user
    db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == plan_data.user_id,
        WorkoutPlan.status == "active"
    ).update({WorkoutPlan.status: "archived"})

    #Insert the base WorkoutPlan
    new_plan = WorkoutPlan(
        user_id=plan_data.user_id,
        duration_weeks=plan_data.duration_weeks,
        goal=plan_data.goal,
        experience_level=plan_data.experience_level,
        created_at=datetime.utcnow(),
        status="active"
    )
    db.add(new_plan)
    db.flush()  # So new_plan.id is generated and usable for WorkoutDays

    #Insert WorkoutDays and associated exercises
    for day in plan_data.days:
        new_day = WorkoutDay(
            plan_id=new_plan.id,
            day_number=day.day_number,
            day_name=day.day_name,
            focus=day.focus
        )
        db.add(new_day)
        db.flush()  # Get new_day.id to attach exercises

        for ex in day.exercises:
            # Find matching exercise in ExerciseCatalog by name + equipment
            catalog_entry = db.query(ExerciseCatalog).filter(
                func.lower(ExerciseCatalog.name) == ex.exercise_name.lower(),
                func.lower(ExerciseCatalog.equipment) == (ex.equipment or "").lower()
            ).first()

            if not catalog_entry:
                raise HTTPException(
                    status_code=400,
                    detail=f"Exercise '{ex.exercise_name}' with equipment '{ex.equipment}' not found in catalog"
                )

            workout_ex = WorkoutExercise(
                day_id=new_day.id,
                exercise_catalog_id=catalog_entry.id,
                sets=ex.sets,
                reps=ex.reps,
                notes=ex.notes
            )
            db.add(workout_ex)

    #Commit all changes
    db.commit()

    return {"message": "Workout plan created successfully", "plan_id": new_plan.id}




@router.get("/workout-plans", response_model=List[WorkoutPlanResponse])
def get_user_workout_plans(
    user_id: int = Query(..., description="ID of the user"),
    status: Optional[str] = Query(None, description="Filter by status: active or archived"),
    db: Session = Depends(get_db)
):
    """
    Returns all workout plans for a given user.
    Supports optional filtering by status.
    Includes nested days and exercises.
    """
    # Build base query
    query = db.query(WorkoutPlan).options(
        joinedload(WorkoutPlan.days).joinedload(WorkoutDay.exercises).joinedload(WorkoutExercise.catalogical_exercise)
    ).filter(WorkoutPlan.user_id == user_id)

    # Apply status filter if provided
    if status:
        query = query.filter(WorkoutPlan.status == status)

    plans = query.order_by(WorkoutPlan.created_at.desc()).all()

    if not plans:
        raise HTTPException(status_code=404, detail="No workout plans found for this user")


    return [serialize_plan(plan) for plan in plans]


@router.get("/workout-plans/{plan_id}", response_model=WorkoutPlanResponse)
def get_workout_plan_by_id(plan_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single workout plan by its unique ID.

    - Includes nested workout days, exercises, and catalog details.
    - Returns the full structured response as defined by WorkoutPlanResponse.
    - If no plan is found with the given ID, returns 404.
    """

    # Query the database for the workout plan, eager-loading all related data:
    # - Workout days (WorkoutDay)
    # - Exercises for each day (WorkoutExercise)
    # - Catalog details for each exercise (ExerciseCatalog)
    plan = db.query(WorkoutPlan).options(
        joinedload(WorkoutPlan.days)
        .joinedload(WorkoutDay.exercises)
        .joinedload(WorkoutExercise.catalogical_exercise)
    ).filter(WorkoutPlan.id == plan_id).first()

    # Return 404 if no such plan exists
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")

    # Serialize the ORM object into a nested response dict
    return serialize_plan(plan)
