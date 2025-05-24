# services/ai_service.py

import httpx
from app.schemas.user_profile_schemas import UserProfile
from app.schemas.plan_schemas import WorkoutPlan
from typing import Optional,List,Tuple
from app.core.config import AI_SERVICE_URL 

timeout = httpx.Timeout(30.0)

async def get_generated_plan_by_ai(
user_profile: UserProfile,
last_plan: Optional[WorkoutPlan], 
allowed_exercises:List[Tuple[str, str]]) -> WorkoutPlan:
  """
  Retrieves generated workout plan from the AI microservice.
  Args:
        user_profile: include user profile
        last_plan(optional): include the last user plan
        allowed_exercises: include List of Tuples (pairs) in the form of (exercise name,equipment)

    Returns:
        WorkoutPlan: The AI-generated workout plan

  """  

  url = f"{AI_SERVICE_URL}/ai/generate"

  payload = {
        "user_profile": user_profile,
        "last_plan": last_plan,
        "allowed_exercises": allowed_exercises
    }

  # Use async HTTP client to send the request
  async with httpx.AsyncClient(timeout=timeout) as client:
      
      response = await client.post(url, json = payload)
      # Raise an exception if the status code is 4xx or 5xx
      response.raise_for_status()
      # Parse and return the response body as JSON (dict or list)
      return response.json()
      
    


