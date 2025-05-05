from typing import Dict
from models import WorkoutPlan
from datetime import datetime

def serialize_plan(plan: WorkoutPlan) -> Dict:
    """
    Transforms a WorkoutPlan SQLAlchemy object (with eager-loaded relationships)
    into a nested dictionary matching the WorkoutPlanResponse Pydantic schema.
    """
    return {
        "id": plan.id,
        "goal": plan.goal,
        "duration_weeks": plan.duration_weeks,
        "status": plan.status,
        "experience_level": plan.experience_level,
        "created_at": plan.created_at,
        "days": [
            {
                "day_number": day.day_number,
                "day_name": day.day_name,
                "focus": day.focus,
                "exercises": [
                    {
                        "exercise_name": ex.catalogical_exercise.name,
                        "equipment": ex.catalogical_exercise.equipment,
                        "sets": ex.sets,
                        "reps": ex.reps,
                        "notes": ex.notes
                    } for ex in day.exercises
                ]
            } for day in plan.days
        ]
    }