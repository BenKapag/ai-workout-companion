from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db_connection import SessionLocal
from routers.user_routes import router as user_router
from routers.plan_routes import router as plan_router

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