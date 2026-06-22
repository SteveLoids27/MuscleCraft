from datetime import datetime
from pathlib import Path

from gym_app.generated_models import GeneratedExercise, GeneratedWorkout
from gym_app.generated_storage import GeneratedWorkoutStorage


def test_storage_returns_empty_when_file_missing(tmp_path: Path) -> None:
    storage = GeneratedWorkoutStorage(tmp_path / "generated.json")
    assert storage.load_all() == []


def test_storage_save_load_and_get_by_id(tmp_path: Path) -> None:
    storage = GeneratedWorkoutStorage(tmp_path / "generated.json")
    workout = GeneratedWorkout(
        id="stored-1",
        created_at=datetime(2026, 6, 21, 9, 0, 0),
        muscle_group="Back",
        sub_area="Lats",
        difficulty="advanced",
        exercises=[GeneratedExercise(name="Pull-up", sets=4, reps="8")],
    )

    storage.add(workout)
    loaded = storage.load_all()

    assert len(loaded) == 1
    assert loaded[0].muscle_group == "Back"
    assert storage.get_by_id("stored-1") == workout
    assert storage.get_by_id("missing") is None
