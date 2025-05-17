# services/ai_service.py

import httpx
from app.schemas.user_profile_schemas import UserProfile
from app.schemas.plan_schemas import WorkoutPlan
from typing import Optional
from app.core.config import AI_SERVICE_URL 

async def get_generated_plan_by_ai(user_profile: UserProfile,last_plan: Optional[WorkoutPlan]) -> WorkoutPlan:
  """
  Retrieves generated workout plan from the AI microservice.
  Args:
        user_profile: include user profile
        last_plan(optional): include the last user plan

    Returns:
        WorkoutPlan: The AI-generated workout plan

  """  

  url = f"{AI_SERVICE_URL}/ai/generate"

  payload = {
        "user_profile": user_profile,
        "last_plan": last_plan
    }

  # Use async HTTP client to send the request
  async with httpx.AsyncClient() as client:
      
      response = await client.post(url, json = payload)
      # Raise an exception if the status code is 4xx or 5xx
      response.raise_for_status()
      # Parse and return the response body as JSON (dict or list)
      return response.json()
      
    


