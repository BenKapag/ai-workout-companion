# scripts/setup_db.py
"""
Initializes the database schema and seeds required tables.
Safe to run multiple times.
"""

from app.models import Base
from app.db_connection import engine
from app.scripts.seed_exercises import seed_exercise_catalog

def setup_database():
    print("Creating tables (if not exist)...")
    Base.metadata.create_all(bind=engine)

    print("Seeding exercise catalog...")
    seed_exercise_catalog()

    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
