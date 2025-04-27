# plan_schemas.py

from typing import List, Optional
from pydantic import BaseModel


#Exercise inside a Workout Day
class ExerciseInPlan(BaseModel):
    exercise_name: str
    sets: Optional[int]
    reps: Optional[int]
    notes: Optional[str]


# Workout Day
class WorkoutDayCreate(BaseModel):
    day_number: int  # 1, 2, 3, etc.
    day_name: Optional[str] = None  # e.g., "Chest Day"
    focus: Optional[str] = None     # e.g., "Chest + Triceps"
    exercises: List[ExerciseInPlan]

# Full Workout Plan
class WorkoutPlanCreate(BaseModel):
    duration_weeks: Optional[int] = None  # Total duration of the plan
    goal: Optional[str] = None             # e.g., "Muscle gain", "Fat loss"
    experience_level: Optional[str] = None # e.g., "Beginner", "Intermediate", "Advanced"
    days: List[WorkoutDayCreate]

# Workout Plan Response

class WorkoutPlanResponse(BaseModel):
    id: int
    duration_weeks: Optional[int]
    goal: Optional[str]
    experience_level: Optional[str]
    days: List[WorkoutDayCreate]  

    class Config:
        from_attributes = True  