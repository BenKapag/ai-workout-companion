# app/services/llm_client.py

import os
import json
import openai
from datetime import datetime
from typing import Optional, List, Tuple
from dotenv import load_dotenv
from app.services.prompt_templates import system_prompt_generate_plan

from app.schemas.plan_schemas import (
    UserProfile,
    LastWorkoutPlan,
    WorkoutPlan
)

# Load environment variables from .env file
load_dotenv()

# OpenRouter API setup
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"



def generate_plan_with_llm(
    user: UserProfile,
    last_plan: Optional[LastWorkoutPlan],
    allowed_exercises: List[Tuple[str, str]]
) -> WorkoutPlan:
    """
    Generates a new WorkoutPlan using OpenRouter-hosted LLM,
    based on the user's profile, last plan (if exists), and
    a list of allowed exercise (name, equipment) pairs.

    Args:
        user (UserProfile): The user's profile.
        last_plan (LastWorkoutPlan | None): Previous plan for context.
        allowed_exercises (List[Tuple[str, str]]): Valid exercises.

    Returns:
        WorkoutPlan: A new plan that adheres to the schema and uses only valid exercises.
    """

    system_prompt = (
    "You are a professional fitness AI. Your job is to generate structured, personalized workout plans.\n"
    "You MUST return ONLY a valid JSON object in the exact format below. Do NOT include any explanation, markdown, or comments.\n\n"
    "Rules:\n"
    "- The plan must include exactly 7 days.\n"
    "- On rest days, the 'exercises' field must be an empty list [].\n"
    "- On training days, include 2 to 4 exercises.\n"
    "- Each exercise must include: 'exercise_name', 'equipment', 'sets', 'reps', and 'notes'.\n"
    "- The 'reps' field must always be an integer (e.g., 10). For time-based exercises like plank, set 'reps' to 1 and describe the duration in 'notes'.\n"
    "- The 'notes' field must include rest time, form tips, or tempo guidance.\n"
    "- Only use exercises from the provided list. Do NOT invent new exercise names.\n"
    "- Do NOT include any introductory text, markdown (like ```json), or explanations. Only return pure JSON.\n\n"
    "Return JSON object in this exact format:\n"
    "{\n"
    "  \"goal\": \"string\",\n"
    "  \"experience_level\": \"string\",\n"
    "  \"duration_weeks\": integer,\n"
    "  \"created_at\": \"ISO 8601 datetime string\",\n"
    "  \"status\": \"string\",\n"
    "  \"days\": [\n"
    "    {\n"
    "      \"day_number\": integer,\n"
    "      \"day_name\": \"string\",\n"
    "      \"focus\": \"string\",\n"
    "      \"exercises\": [\n"
    "        {\n"
    "          \"exercise_name\": \"string\",\n"
    "          \"equipment\": \"string\",\n"
    "          \"sets\": integer,\n"
    "          \"reps\": integer,\n"
    "          \"notes\": \"string\"\n"
    "        }\n"
    "      ]\n"
    "    }\n"
    "  ]\n"
    "}"
)



    # 📋 User profile
    user_prompt = (
        f"User profile:\n"
        f"- Age: {user.age}\n"
        f"- Height: {user.height_cm} cm\n"
        f"- Weight: {user.weight_kg} kg\n"
        f"- Experience level: {user.experience_level}\n"
        f"- Fitness goal: {user.fitness_goal}\n"
        f"- Equipment: {', '.join(user.equipment) if user.equipment else 'None'}\n"
        f"- Health notes: {user.health_notes or 'None'}\n\n"
    )

    # 📚 Previous plan (if any)
    if last_plan:
        user_prompt += (
            "Previous plan details:\n"
            f"- Goal: {last_plan.goal}\n"
            f"- Experience level: {last_plan.experience_level}\n"
            f"- Duration: {last_plan.duration_weeks} weeks\n"
            f"- Status: {last_plan.status}\n"
            f"- Created at: {last_plan.created_at.isoformat()}\n\n"
            "Please vary or improve the new plan based on the last one.\n"
        )
    else:
        user_prompt += "This is the user's first plan.\n\n"

    # ✅ Format allowed exercises
    formatted_exercises = "\n".join(
        [f"- {name} (Equipment: {equipment})" for name, equipment in allowed_exercises[:50]]
    )

    user_prompt += (
        "⚠️ Only choose exercises from this list:\n"
        f"{formatted_exercises}\n"
    )

    # 🧠 Call the LLM
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=2000
    )

    response_text = response["choices"][0]["message"]["content"]

    print("⬅️ Raw LLM response:\n", response_text)

    try:
        plan_dict = json.loads(response_text)
        print("✅ JSON parsed successfully.")
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON from LLM!")
        raise ValueError("❌ LLM returned invalid JSON:\n" + response_text)

    try:
        return WorkoutPlan(**plan_dict)
    except Exception as e:
        print("❌ JSON did not match WorkoutPlan schema!")
        raise ValueError(f"❌ JSON structure mismatch with WorkoutPlan schema:\n{e}\n\nRaw output:\n{plan_dict}")

