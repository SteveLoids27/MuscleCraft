from __future__ import annotations

from unittest.mock import patch

import pytest

from gym_app.generated_models import GeneratedExercise, GeneratedWorkout
from gym_app.web import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["PREFER_LLM"] = False
    return app.test_client()


def test_home_shows_generator_form(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"Generate your workout" in response.data
    assert b"Muscle group" in response.data
    assert b"Difficulty" in response.data
    assert b"Generate workout" in response.data


def test_generate_workout_from_form(client) -> None:
    response = client.post(
        "/generate",
        data={
            "muscle_group": "Chest",
            "sub_area": "Upper chest",
            "difficulty": "intermediate",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Your workout plan" in response.data
    assert b"Chest" in response.data
    assert b"Sets" in response.data


def test_generate_invalid_muscle_group(client) -> None:
    response = client.post(
        "/generate",
        data={
            "muscle_group": "Invalid",
            "difficulty": "basic",
        },
    )
    assert response.status_code == 400
    assert b"Unknown muscle group" in response.data


@patch("gym_app.web.generate_workout")
def test_regenerate_button(mock_generate, client) -> None:
    mock_generate.return_value = GeneratedWorkout(
        muscle_group="Back",
        sub_area="Lats",
        difficulty="advanced",
        exercises=[GeneratedExercise(name="Pull-up", sets=4, reps="8")],
        notes="Advanced back workout",
    )
    response = client.post(
        "/generate",
        data={
            "muscle_group": "Back",
            "sub_area": "Lats",
            "difficulty": "advanced",
        },
    )
    assert response.status_code == 200
    assert b"Pull-up" in response.data
    mock_generate.assert_called_once()
