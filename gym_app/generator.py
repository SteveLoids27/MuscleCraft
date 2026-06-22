from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gym_app.difficulty import Difficulty, parse_difficulty
from gym_app.generated_models import GeneratedExercise, GeneratedWorkout
from gym_app.muscle_groups import is_valid_muscle_group, is_valid_sub_area

EXERCISES_PATH = Path(__file__).resolve().parent / "data" / "exercises.json"
MIN_EXERCISES = 4
MAX_EXERCISES = 6

SET_ADJUSTMENT: dict[Difficulty, int] = {
    Difficulty.BASIC: -1,
    Difficulty.INTERMEDIATE: 0,
    Difficulty.ADVANCED: 1,
}


def _load_templates() -> dict[str, dict[str, list[dict[str, Any]]]]:
    raw = json.loads(EXERCISES_PATH.read_text(encoding="utf-8"))
    return raw


def _matches_sub_area(template: dict[str, Any], sub_area: str | None) -> bool:
    targets = template.get("targets", [])
    if not targets or sub_area is None:
        return True
    return sub_area in targets


def _select_templates(
    pool: list[dict[str, Any]],
    sub_area: str | None,
) -> list[dict[str, Any]]:
    matched = [item for item in pool if _matches_sub_area(item, sub_area)]
    if len(matched) < MIN_EXERCISES:
        general = [item for item in pool if not item.get("targets")]
        seen = {item["name"] for item in matched}
        for item in general:
            if item["name"] not in seen:
                matched.append(item)
                seen.add(item["name"])
    if len(matched) < MIN_EXERCISES:
        matched = list(pool)

    matched.sort(key=lambda item: item["name"])
    return matched[:MAX_EXERCISES]


def _build_exercise(
    template: dict[str, Any],
    difficulty: Difficulty,
) -> GeneratedExercise:
    base_sets = int(template["sets"])
    adjusted_sets = max(2, base_sets + SET_ADJUSTMENT[difficulty])
    return GeneratedExercise(
        name=str(template["name"]),
        sets=adjusted_sets,
        reps=str(template["reps"]),
        notes=str(template.get("notes", "")),
    )


def _summary_note(
    muscle_group: str,
    sub_area: str | None,
    difficulty: Difficulty,
) -> str:
    focus = f"{muscle_group} ({sub_area})" if sub_area else muscle_group
    return f"{difficulty.value.title()} workout focused on {focus}."


def total_sets(workout: GeneratedWorkout) -> int:
    return sum(exercise.sets for exercise in workout.exercises)


def generate_workout_from_template(
    muscle_group: str,
    sub_area: str | None,
    difficulty: str,
) -> GeneratedWorkout:
    if not is_valid_muscle_group(muscle_group):
        raise ValueError(f"Unknown muscle group: {muscle_group}")

    if sub_area is not None and not is_valid_sub_area(muscle_group, sub_area):
        raise ValueError(f"Invalid sub-area '{sub_area}' for muscle group '{muscle_group}'.")

    level = parse_difficulty(difficulty)
    templates_by_group = _load_templates()

    if muscle_group not in templates_by_group:
        raise ValueError(f"No exercise templates for muscle group: {muscle_group}")

    difficulty_pool = templates_by_group[muscle_group]
    if level.value not in difficulty_pool:
        raise ValueError(f"No templates for difficulty: {level.value}")

    pool = difficulty_pool[level.value]
    selected = _select_templates(pool, sub_area)

    if len(selected) < MIN_EXERCISES:
        raise ValueError(
            f"Not enough exercises for {muscle_group} at {level.value} difficulty."
        )

    exercises = [_build_exercise(template, level) for template in selected]
    return GeneratedWorkout(
        muscle_group=muscle_group,
        sub_area=sub_area,
        difficulty=level.value,
        exercises=exercises,
        notes=_summary_note(muscle_group, sub_area, level),
    )


def generate_workout(
    muscle_group: str,
    sub_area: str | None,
    difficulty: str,
    *,
    prefer_llm: bool = True,
) -> GeneratedWorkout:
    """Generate a workout via Groq when configured, else use templates."""
    if prefer_llm:
        from gym_app.llm_generator import (
            LLMGenerationError,
            generate_workout_with_groq,
            get_groq_api_key,
        )

        if get_groq_api_key():
            try:
                return generate_workout_with_groq(muscle_group, sub_area, difficulty)
            except LLMGenerationError:
                pass

    return generate_workout_from_template(muscle_group, sub_area, difficulty)
