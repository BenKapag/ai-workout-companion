import os

# Base URL of the database microservice
DB_SERVICE_URL = os.getenv("DB_SERVICE_URL", "http://localhost:8001")

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://host.docker.internal:8002")

# JWT secret and algorithm settings
SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
