from __future__ import annotations

from gym_app.generated_models import GeneratedExercise, GeneratedWorkout
from gym_app.formatting import format_workout_text


def test_format_workout_text_includes_exercises() -> None:
    workout = GeneratedWorkout(
        muscle_group="Chest",
        sub_area="Upper chest",
        difficulty="intermediate",
        notes="Focus on control.",
        exercises=[
            GeneratedExercise(name="Incline Press", sets=4, reps="10", notes="Slow eccentric"),
        ],
    )
    text = format_workout_text(workout)
    assert "Chest — Upper chest" in text
    assert "Intermediate" in text
    assert "Focus on control." in text
    assert "1. Incline Press — 4 x 10 (Slow eccentric)" in text
