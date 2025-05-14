import os

# Base URL of the database microservice
DB_SERVICE_URL = os.getenv("DB_SERVICE_URL", "http://localhost:8001")

# JWT secret and algorithm settings
SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
