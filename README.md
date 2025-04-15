# AI Workout Companion 💪🤖

A modular, AI-powered fitness app designed to generate personalized training plans, track progress, and answer fitness-related questions.

---

## 🎯 Project Purpose

This project was created for the *Engineering of Advanced Software Solutions* course at HIT, and serves as a full-stack demonstration of microservices architecture, AI integration, and clean API design.

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **AI Agent**: FastAPI microservice (planned)
- **Frontend**: React or Streamlit (planned)
- **Containerization**: Docker, Docker Compose (upcoming)

---

## 🧩 Microservices Architecture

- `backend/`: Main API gateway, handles routing, validation, and business logic
- `database/`: Will handle all DB access (users, profiles, workouts) via FastAPI
- `ai-agent/`: Generates workout plans + answers fitness questions + Evaluate training trends, weak areas (future)
- `frontend/`: User interface for interaction with the system

---

## ✅ Current Features

- `POST /register` — Create a new user account
- `POST /login` — Authenticate user (currently mocked, JWT coming soon)
- `PUT /profile` — Create or update personal fitness profile (goal, age, experience, etc.)
- `GET /profile` — Retrieve current profile data

---

## 🔜 Coming Soon

- AI-generated weekly training plans via `/plan`
- AI chat endpoint for Q&A: `/ai/chat`
- Workout logging and progress tracking
- AI-powered analysis: Evaluate training trends, weak areas
- JWT authentication
- Full microservice separation and Docker Compose setup

---

## 🚀 Getting Started

> **Note:** Deployment instructions and Docker setup will be added in the final version of the project.

---

## 👤 Author

Ben Kapag  
HIT — Engineering of Advanced Software Solutions (2025)

---

## 📁 Status

✅ Backend core complete  
🔄 Microservices & AI in progress  
📦 Docker & Deployment coming soon
