# scripts/seed_exercises.py
# ---------------------------------------------
# Seeds the exercise_catalog table with predefined exercises.
# Ensures required exercises exist for plan generation.
# Skips duplicates based on (name + equipment).
# ---------------------------------------------

from sqlalchemy.orm import Session
from app.db_connection import SessionLocal
from app.models import ExerciseCatalog



# Static seed data: each entry must match expected AI-generated values
seed_data = [
    {
        "name": "Barbell Bench Press",
        "equipment": "Barbell",
        "primary_muscle": "Chest",
        "secondary_muscle": "Triceps",
        "difficulty": "Intermediate"
    },
    {
        "name": "Incline Dumbbell Press",
        "equipment": "Dumbbell",
        "primary_muscle": "Chest",
        "secondary_muscle": "Shoulders",
        "difficulty": "Intermediate"
    },
    {
        "name": "Triceps Pushdown",
        "equipment": "Cable Machine",
        "primary_muscle": "Triceps",
        "difficulty": "Beginner"
    },
    {
        "name": "Deadlift",
        "equipment": "Barbell",
        "primary_muscle": "Back",
        "secondary_muscle": "Hamstrings",
        "difficulty": "Advanced"
    },
    {
        "name": "Seated Row",
        "equipment": "Cable Machine",
        "primary_muscle": "Back",
        "difficulty": "Intermediate"
    },
    {
        "name": "Barbell Curl",
        "equipment": "Barbell",
        "primary_muscle": "Biceps",
        "difficulty": "Beginner"
    }
]

def seed_exercise_catalog():
    """
    Inserts predefined exercises into the exercise_catalog table.
    Existing entries (matched by name + equipment) are not duplicated.
    """
    db: Session = SessionLocal()

    try:
        for ex in seed_data:
            exists = db.query(ExerciseCatalog).filter_by(
                name=ex["name"],
                equipment=ex["equipment"]
            ).first()

            if exists:
                continue

            db.add(ExerciseCatalog(**ex))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error while seeding exercise catalog: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_exercise_catalog()
