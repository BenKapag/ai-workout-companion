from typing import List, Optional
from pydantic import BaseModel,Field
from datetime import datetime

class WorkoutPlanResponse(BaseModel):
    duration_weeks: Optional[int]
    goal: Optional[str]  
    experience_level: Optional[str]
    status:str
    created_at:datetime

    class Config:
        from_attributes = True  


class ExerciseInPlan(BaseModel):
    exercise_name: str
    equipment: str
    sets: Optional[int]
    reps: Optional[int]
    notes: Optional[str]

class WorkoutDayCreate(BaseModel):
    day_number: int
    day_name: Optional[str]
    focus: Optional[str]
    exercises: List[ExerciseInPlan]

class WorkoutPlanCreate(BaseModel):
    user_id: int
    duration_weeks: Optional[int]
    goal: Optional[str]
    experience_level: Optional[str]
    days: List[WorkoutDayCreate]