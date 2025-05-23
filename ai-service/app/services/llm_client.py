# app/services/llm_client.py

import os
import json
import openai
import re
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv

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
    allowed_exercises: List[str]
) -> WorkoutPlan:
    """
    Generates a new WorkoutPlan using OpenRouter-hosted LLM,
    based on the user's profile, last plan (if exists), and
    a list of allowed exercise names from the Exercise Catalog.

    Args:
        user (UserProfile): The user's profile.
        last_plan (LastWorkoutPlan | None): Previous plan for context.
        allowed_exercises (List[str]): List of valid exercise names.

    Returns:
        WorkoutPlan: A new plan that adheres to the schema and only uses valid exercises.
    """

    # ✍️ System message: define format and rules
    system_prompt = (
        "You are a professional fitness AI. Your job is to generate structured, personalized workout plans.\n"
        "You MUST return ONLY a valid JSON object in this format:\n\n"
        "{\n"
        "  \"goal\": str,\n"
        "  \"experience_level\": str,\n"
        "  \"duration_weeks\": int,\n"
        "  \"created_at\": str (ISO format),\n"
        "  \"status\": str,\n"
        "  \"days\": [\n"
        "    {\n"
        "      \"day_number\": int,\n"
        "      \"day_name\": str,\n"
        "      \"focus\": str,\n"
        "      \"exercises\": [\n"
        "        {\n"
        "          \"exercise_name\": str,\n"
        "          \"equipment\": str,\n"
        "          \"sets\": int,\n"
        "          \"reps\": int,  # Always a number. If the exercise is time-based, use the 'notes' field instead.\n"
        "          \"notes\": str (optional)\n"
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "⚠️ STRICT RULES:\n"
        "- Do NOT write time values (e.g., '60 seconds') in the 'reps' field. Use the 'notes' field instead.\n"
        "- Do NOT invent exercise names. Only use exercises from the list provided.\n"
        "- Return ONLY a JSON object — no explanations, markdown, or formatting around it."
    )

    # 📋 Build user prompt
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

    # 📌 Add exercise constraint
    exercise_list_str = ", ".join(allowed_exercises[:50])  # Limit to top 50 to avoid prompt bloat
    user_prompt += (
        "⚠️ Only choose exercise names from this list:\n"
        f"{exercise_list_str}\n"
    )

    print("✅ Sending prompt to LLM...")
    print("🧠 Prompt message:\n", user_prompt)

    # 🧠 Call the LLM via OpenRouter
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=2000
    )

    # 🧪 Parse response
    response_text = response["choices"][0]["message"]["content"]

    print("⬅️ Raw LLM response:\n", response_text)

    cleaned_response = re.sub(
    r'"reps":\s*(\d+)\s*seconds',
    r'"reps": 1,\n          "notes": "Hold for \1 seconds"',
    response_text
    )

    try:
        plan_dict = json.loads(cleaned_response)
        print("✅ JSON parsed successfully.")
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON from LLM!")
        print("❌ LLM Raw output:", response_text)
        raise ValueError("❌ LLM returned invalid JSON:\n" + response_text)

    try:
        return WorkoutPlan(**plan_dict)
    except Exception as e:
        print("❌ JSON did not match WorkoutPlan schema!")
        print("❌ Parsed dict:", plan_dict)
        raise ValueError(f"❌ JSON structure mismatch with WorkoutPlan schema:\n{e}\n\nRaw output:\n{plan_dict}")
