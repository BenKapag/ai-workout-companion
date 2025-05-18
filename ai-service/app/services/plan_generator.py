# app/services/plan_generator.py

from typing import Optional
from app.schemas.plan_schemas import UserProfile, WorkoutPlan, WorkoutDay, WorkoutExercise,LastWorkoutPlan
from datetime import datetime

def generate_plan(user: UserProfile, last_plan: Optional[LastWorkoutPlan]) -> WorkoutPlan:
    """
    Generates a new workout plan based on user profile and (optionally) last plan.

    Args:
        user (UserProfile): The user's fitness profile.
        last_plan (WorkoutPlan or None): The user's previous plan, if exists.

    Returns:
        WorkoutPlan: A new personalized plan.
    """

    # Define a simple exercise pool (static for now)
    exercise_pool = [
        WorkoutExercise(exercise_name="Push Ups", equipment="Bodyweight", sets=3, reps=15),
        WorkoutExercise(exercise_name="Dumbbell Squats", equipment="Dumbbell", sets=3, reps=12),
        WorkoutExercise(exercise_name="Plank", equipment="Bodyweight", sets=3, reps=60, notes="Hold in seconds"),
    ]

    # Create a list of workout days using the same exercises
    days = []
    for i in range(3):
        day = WorkoutDay(
            day_number=i + 1,
            day_name=f"Day {i + 1}",
            focus="Full Body",
            exercises=exercise_pool
        )
        days.append(day)

    # Build and return the final WorkoutPlan object
    plan = WorkoutPlan(
        goal=user.fitness_goal,
        experience_level=user.experience_level,
        duration_weeks=4,
        created_at=datetime.utcnow(),
        status="active",
        days=days
    )

    return plan
