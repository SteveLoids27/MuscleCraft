from __future__ import annotations

import pytest

from gym_app.difficulty import Difficulty
from gym_app.generator import generate_workout_from_template, total_sets


def test_generate_chest_upper_intermediate() -> None:
    workout = generate_workout_from_template("Chest", "Upper chest", "intermediate")

    assert workout.muscle_group == "Chest"
    assert workout.sub_area == "Upper chest"
    assert workout.difficulty == "intermediate"
    assert 4 <= len(workout.exercises) <= 6
    assert all(exercise.sets >= 2 for exercise in workout.exercises)
    assert any("Incline" in exercise.name for exercise in workout.exercises)


@pytest.mark.parametrize(
    ("muscle_group", "sub_area"),
    [
        ("Chest", "Upper chest"),
        ("Back", "Lats"),
        ("Shoulders", "Side delts"),
        ("Quads", None),
        ("Hamstrings", None),
        ("Glutes", None),
    ],
)
@pytest.mark.parametrize("difficulty", ["basic", "intermediate", "advanced"])
def test_generate_across_groups_and_difficulties(
    muscle_group: str,
    sub_area: str | None,
    difficulty: str,
) -> None:
    workout = generate_workout_from_template(muscle_group, sub_area, difficulty)

    assert workout.muscle_group == muscle_group
    assert workout.difficulty == difficulty
    assert len(workout.exercises) >= 4


def test_basic_has_lower_volume_than_advanced() -> None:
    basic = generate_workout_from_template("Chest", "Middle chest", "basic")
    advanced = generate_workout_from_template("Chest", "Middle chest", "advanced")

    assert total_sets(basic) < total_sets(advanced)


def test_invalid_muscle_group_raises() -> None:
    with pytest.raises(ValueError, match="Unknown muscle group"):
        generate_workout_from_template("Invalid", None, "basic")


def test_invalid_sub_area_raises() -> None:
    with pytest.raises(ValueError, match="Invalid sub-area"):
        generate_workout_from_template("Chest", "Lats", "basic")


def test_invalid_difficulty_raises() -> None:
    with pytest.raises(ValueError, match="Unknown difficulty"):
        generate_workout_from_template("Chest", None, "expert")


def test_workout_includes_summary_note() -> None:
    workout = generate_workout_from_template("Back", "Lats", Difficulty.INTERMEDIATE.value)
    assert "Back" in workout.notes
    assert "Intermediate" in workout.notes or "intermediate" in workout.notes.lower()
