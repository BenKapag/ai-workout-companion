# Use official Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

ENV PYTHONPATH=/app

# Run the FastAPI app with uvicorn
CMD ["bash", "-c", "python app/scripts/setup_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8001"]


