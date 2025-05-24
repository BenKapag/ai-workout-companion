from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db_connection import get_db
from typing import List,Tuple
from app.models import ExerciseCatalog

router = APIRouter()

@router.get("/catalog-exercises/names", response_model=List[Tuple[str, str]])
def get_catalog_exercises_names(db: Session = Depends(get_db)):
    """
    Returns a tuple list of pairs that each one include exercise name and equipment from the ExerciseCatalog table.
    Used to constrain exercise selection in AI-generated workout plans.
    """

    # Query the 'name' and 'equipment' columns from the ExerciseCatalog
    results = db.query(ExerciseCatalog.name,ExerciseCatalog.equipment).all()  # returns List[Tuple[str, str]]

    return results

