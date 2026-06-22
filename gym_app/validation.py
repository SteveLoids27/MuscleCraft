from __future__ import annotations

from typing import Any, Mapping

from gym_app.difficulty import parse_difficulty
from gym_app.muscle_groups import is_valid_muscle_group, is_valid_sub_area


def validate_generate_form(form: Mapping[str, Any]) -> tuple[str, str | None, str]:
    muscle_group = str(form.get("muscle_group", "")).strip()
    sub_area_raw = str(form.get("sub_area", "")).strip()
    sub_area = sub_area_raw or None
    difficulty_raw = str(form.get("difficulty", "")).strip()

    if not muscle_group:
        raise ValueError("Please select a muscle group.")
    if not is_valid_muscle_group(muscle_group):
        raise ValueError(f"Unknown muscle group: {muscle_group}")
    if sub_area is not None and not is_valid_sub_area(muscle_group, sub_area):
        raise ValueError(f"Invalid sub-area '{sub_area}' for {muscle_group}.")
    if not difficulty_raw:
        raise ValueError("Please select a difficulty level.")

    difficulty = parse_difficulty(difficulty_raw).value
    return muscle_group, sub_area, difficulty
