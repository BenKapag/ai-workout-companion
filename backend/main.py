# main.py
# Entry point for the FastAPI application

from fastapi import FastAPI
from routers import user_routes,plan_routes  # Import user routes

# Create the FastAPI app instance
app = FastAPI()

# Register the auth router (includes /register endpoint)
app.include_router(user_routes.router)
app.include_router(plan_routes.router)

# Simple health check route
@app.get("/")
def root():
    return {"message": "AI Workout Companion API is running!"}
