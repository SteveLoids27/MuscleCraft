from datetime import datetime

from gym_app.generated_models import GeneratedExercise, GeneratedWorkout


def test_generated_exercise_round_trip() -> None:
    original = GeneratedExercise(
        name="Bench Press",
        sets=3,
        reps="8-10",
        notes="Control the descent",
    )
    restored = GeneratedExercise.from_dict(original.to_dict())
    assert restored == original


def test_generated_workout_round_trip() -> None:
    original = GeneratedWorkout(
        id="gen-1",
        created_at=datetime(2026, 6, 21, 10, 30, 0),
        muscle_group="Chest",
        sub_area="Upper chest",
        difficulty="intermediate",
        notes="Push day focus",
        exercises=[
            GeneratedExercise(name="Incline Press", sets=4, reps="10", notes=""),
            GeneratedExercise(name="Cable Fly", sets=3, reps="12", notes="Squeeze at top"),
        ],
    )
    restored = GeneratedWorkout.from_dict(original.to_dict())
    assert restored == original


def test_generated_workout_optional_sub_area() -> None:
    workout = GeneratedWorkout(
        id="gen-2",
        created_at=datetime(2026, 6, 21, 11, 0, 0),
        muscle_group="Biceps",
        sub_area=None,
        difficulty="basic",
    )
    restored = GeneratedWorkout.from_dict(workout.to_dict())
    assert restored.sub_area is None
