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