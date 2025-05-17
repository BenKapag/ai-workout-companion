# app/main.py

from fastapi import FastAPI
from app.routers import plan_routes

app = FastAPI(title="AI Workout Microservice")

app.include_router(plan_routes.router)