from __future__ import annotations

import json
import os
import re
from pathlib import Path

from groq import Groq

from gym_app.difficulty import Difficulty, parse_difficulty
from gym_app.generated_models import GeneratedExercise, GeneratedWorkout
from gym_app.muscle_groups import is_valid_muscle_group, is_valid_sub_area

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "workout_generator.md"
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
MIN_EXERCISES = 4
MAX_EXERCISES = 6


class LLMGenerationError(Exception):
    """Raised when Groq workout generation fails."""


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass


def get_groq_api_key() -> str | None:
    _load_env()
    key = os.getenv("GROQ_API_KEY", "").strip()
    return key or None


def get_groq_model() -> str:
    _load_env()
    return os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL


def _load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _build_user_prompt(
    muscle_group: str,
    sub_area: str | None,
    difficulty: Difficulty,
) -> str:
    focus = f"{muscle_group} — {sub_area}" if sub_area else muscle_group
    return (
        f"Muscle group: {muscle_group}\n"
        f"Sub-area: {sub_area or 'any'}\n"
        f"Difficulty: {difficulty.value}\n"
        f"Generate a {difficulty.value} workout targeting {focus}."
    )


def _extract_json(content: str) -> dict:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _parse_exercises(payload: dict) -> list[GeneratedExercise]:
    raw_exercises = payload.get("exercises", [])
    if not isinstance(raw_exercises, list) or len(raw_exercises) < MIN_EXERCISES:
        raise LLMGenerationError("LLM returned too few exercises.")

    exercises: list[GeneratedExercise] = []
    for item in raw_exercises[:MAX_EXERCISES]:
        exercises.append(
            GeneratedExercise(
                name=str(item["name"]),
                sets=int(item["sets"]),
                reps=str(item["reps"]),
                notes=str(item.get("notes", "")),
            )
        )
    return exercises


def generate_workout_with_groq(
    muscle_group: str,
    sub_area: str | None,
    difficulty: str,
    *,
    client: Groq | None = None,
) -> GeneratedWorkout:
    if not is_valid_muscle_group(muscle_group):
        raise ValueError(f"Unknown muscle group: {muscle_group}")

    if sub_area is not None and not is_valid_sub_area(muscle_group, sub_area):
        raise ValueError(f"Invalid sub-area '{sub_area}' for muscle group '{muscle_group}'.")

    level = parse_difficulty(difficulty)
    api_key = get_groq_api_key()
    if not api_key:
        raise LLMGenerationError("GROQ_API_KEY is not set.")

    groq_client = client or Groq(api_key=api_key)
    response = groq_client.chat.completions.create(
        model=get_groq_model(),
        messages=[
            {"role": "system", "content": _load_system_prompt()},
            {"role": "user", "content": _build_user_prompt(muscle_group, sub_area, level)},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise LLMGenerationError("Groq returned an empty response.")

    try:
        payload = _extract_json(content)
        exercises = _parse_exercises(payload)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise LLMGenerationError(f"Failed to parse Groq response: {error}") from error

    notes = str(payload.get("notes", "")).strip()
    if not notes:
        focus = f"{muscle_group} ({sub_area})" if sub_area else muscle_group
        notes = f"{level.value.title()} workout focused on {focus}."

    return GeneratedWorkout(
        muscle_group=muscle_group,
        sub_area=sub_area,
        difficulty=level.value,
        exercises=exercises,
        notes=notes,
    )
