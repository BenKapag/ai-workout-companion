from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db_connection import get_db
from typing import List
from app.models import ExerciseCatalog

router = APIRouter()

@router.get("/catalog-exercises/names", response_model=List[str])
def get_catalog_exercises_names(db: Session = Depends(get_db)):
    """
    Returns a list of exercise names from the ExerciseCatalog table.
    Used to constrain exercise selection in AI-generated workout plans.
    """

    # Query only the 'name' column from the ExerciseCatalog
    results = db.query(ExerciseCatalog.name).all()  # returns List[Tuple[str]]

    # Extract the names from the list of tuples
    exercise_names = [name[0] for name in results]

    return exercise_names

