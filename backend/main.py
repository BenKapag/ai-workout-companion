# main.py
# Entry point for the FastAPI application

from fastapi import FastAPI
from auth import router as auth_router  # Import auth routes

# Create the FastAPI app instance
app = FastAPI()

# Register the auth router (includes /register endpoint)
app.include_router(auth_router)

# Simple health check route
@app.get("/")
def root():
    return {"message": "AI Workout Companion API is running!"}
