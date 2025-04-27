# routers/plan_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.plan_schemas import WorkoutPlanCreate
from schemas.auth_schemas import TokenLoginResponse  # Schema representing the authenticated user
from services.auth_dependency import get_current_user  # Dependency to extract current user from JWT token
import httpx
from core.config import DB_SERVICE_URL

