from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db_connection import SessionLocal
from app.routers.user_routes import router as user_router
from app.routers.plan_routes import router as plan_router
from app.routers.reference_data_routes import router as data_routes

app = FastAPI(title="Database Microservice")

# Dependency for DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "Database microservice is running"}

# Register all routes from user_routes.py
app.include_router(user_router)
app.include_router(plan_router)
app.include_router(data_routes)