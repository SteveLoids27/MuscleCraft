from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from gym_app.generated_models import GeneratedExercise, GeneratedWorkout
from gym_app.generated_storage import GeneratedWorkoutStorage
from gym_app.web import create_app


@pytest.fixture
def storage(tmp_path: Path) -> GeneratedWorkoutStorage:
    return GeneratedWorkoutStorage(tmp_path / "generated.json")


@pytest.fixture
def client(storage: GeneratedWorkoutStorage):
    app = create_app(storage=storage)
    app.config["TESTING"] = True
    app.config["PREFER_LLM"] = False
    return app.test_client()


def _sample_workout() -> GeneratedWorkout:
    return GeneratedWorkout(
        id="saved-workout-1",
        created_at=datetime(2026, 6, 22, 10, 0, 0),
        muscle_group="Chest",
        sub_area="Upper chest",
        difficulty="intermediate",
        notes="Test workout",
        exercises=[
            GeneratedExercise(name="Incline Press", sets=4, reps="10", notes="Control"),
        ],
    )


def test_save_workout_from_result_page(client, storage: GeneratedWorkoutStorage) -> None:
    workout = _sample_workout()
    response = client.post(
        "/workouts/save",
        data={"workout_json": json.dumps(workout.to_dict())},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Saved workout" in response.data
    assert b"Incline Press" in response.data
    assert storage.get_by_id("saved-workout-1") is not None


def test_workouts_list_page(client, storage: GeneratedWorkoutStorage) -> None:
    storage.add(_sample_workout())
    response = client.get("/workouts")
    assert response.status_code == 200
    assert b"Saved workouts" in response.data
    assert b"Chest" in response.data
    assert b"intermediate" in response.data or b"Intermediate" in response.data


def test_workout_detail_page(client, storage: GeneratedWorkoutStorage) -> None:
    storage.add(_sample_workout())
    response = client.get("/workouts/saved-workout-1")
    assert response.status_code == 200
    assert b"Incline Press" in response.data
    assert b"Upper chest" in response.data


def test_workout_detail_not_found(client) -> None:
    response = client.get("/workouts/missing-id")
    assert response.status_code == 404
    assert b"Not found" in response.data
    assert b"could not be found" in response.data


def test_save_invalid_workout_json(client) -> None:
    response = client.post("/workouts/save", data={"workout_json": "not-json"})
    assert response.status_code == 400
    assert b"Could not save workout" in response.data


def test_workout_detail_has_copy_button(client, storage: GeneratedWorkoutStorage) -> None:
    storage.add(_sample_workout())
    response = client.get("/workouts/saved-workout-1")
    assert response.status_code == 200
    assert b"Copy workout" in response.data
    assert b"Incline Press" in response.data


def test_list_all_sorted_newest_first(storage: GeneratedWorkoutStorage) -> None:
    older = GeneratedWorkout(
        id="old",
        created_at=datetime(2026, 1, 1, 9, 0, 0),
        muscle_group="Back",
        difficulty="basic",
    )
    newer = GeneratedWorkout(
        id="new",
        created_at=datetime(2026, 6, 22, 12, 0, 0),
        muscle_group="Chest",
        difficulty="advanced",
    )
    storage.add(older)
    storage.add(newer)
    assert [workout.id for workout in storage.list_all()] == ["new", "old"]
