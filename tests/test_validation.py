from __future__ import annotations

import pytest

from gym_app.generated_models import GeneratedExercise, GeneratedWorkout
from gym_app.validation import validate_generate_form


def test_validate_generate_form_success() -> None:
    muscle_group, sub_area, difficulty = validate_generate_form(
        {
            "muscle_group": "Chest",
            "sub_area": "Upper chest",
            "difficulty": "intermediate",
        }
    )
    assert muscle_group == "Chest"
    assert sub_area == "Upper chest"
    assert difficulty == "intermediate"


def test_validate_generate_form_empty_sub_area_becomes_none() -> None:
    _, sub_area, _ = validate_generate_form(
        {"muscle_group": "Back", "sub_area": "", "difficulty": "basic"}
    )
    assert sub_area is None


def test_validate_missing_muscle_group() -> None:
    with pytest.raises(ValueError, match="muscle group"):
        validate_generate_form({"difficulty": "basic"})


def test_validate_missing_difficulty() -> None:
    with pytest.raises(ValueError, match="difficulty"):
        validate_generate_form({"muscle_group": "Chest"})


def test_validate_invalid_muscle_group() -> None:
    with pytest.raises(ValueError, match="Unknown muscle group"):
        validate_generate_form(
            {"muscle_group": "Invalid", "difficulty": "basic"}
        )


def test_validate_invalid_sub_area() -> None:
    with pytest.raises(ValueError, match="Invalid sub-area"):
        validate_generate_form(
            {
                "muscle_group": "Chest",
                "sub_area": "Lats",
                "difficulty": "basic",
            }
        )
