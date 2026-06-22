from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from gym_app.generator import generate_workout
from gym_app.llm_generator import (
    LLMGenerationError,
    _build_user_prompt,
    _extract_json,
    _parse_exercises,
    generate_workout_with_groq,
)


GROQ_RESPONSE = {
    "notes": "Intermediate chest workout",
    "exercises": [
        {"name": "Incline Press", "sets": 4, "reps": "10", "notes": "Control the weight"},
        {"name": "Flat Bench", "sets": 3, "reps": "8", "notes": ""},
        {"name": "Cable Fly", "sets": 3, "reps": "12", "notes": "Squeeze"},
        {"name": "Push-up", "sets": 3, "reps": "15", "notes": "Finisher"},
    ],
}


def test_build_user_prompt_includes_inputs() -> None:
    from gym_app.difficulty import Difficulty

    prompt = _build_user_prompt("Chest", "Upper chest", Difficulty.INTERMEDIATE)
    assert "Chest" in prompt
    assert "Upper chest" in prompt
    assert "intermediate" in prompt


def test_extract_json_from_markdown_fence() -> None:
    content = "```json\n" + json.dumps(GROQ_RESPONSE) + "\n```"
    assert _extract_json(content)["notes"] == "Intermediate chest workout"


def test_parse_exercises_validates_minimum() -> None:
    with pytest.raises(LLMGenerationError, match="too few"):
        _parse_exercises({"exercises": [{"name": "A", "sets": 3, "reps": "10"}]})


@patch("gym_app.llm_generator.get_groq_api_key", return_value="test-key")
def test_generate_workout_with_groq_parses_response(mock_key) -> None:
    mock_message = MagicMock()
    mock_message.content = json.dumps(GROQ_RESPONSE)
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    workout = generate_workout_with_groq(
        "Chest",
        "Upper chest",
        "intermediate",
        client=mock_client,
    )

    assert workout.muscle_group == "Chest"
    assert len(workout.exercises) == 4
    assert workout.exercises[0].name == "Incline Press"
    mock_client.chat.completions.create.assert_called_once()


@patch("gym_app.llm_generator.get_groq_api_key", return_value=None)
def test_generate_workout_falls_back_without_api_key(mock_key) -> None:
    workout = generate_workout("Chest", "Upper chest", "intermediate", prefer_llm=True)
    assert workout.muscle_group == "Chest"
    assert len(workout.exercises) >= 4


@patch("gym_app.llm_generator.generate_workout_with_groq")
@patch("gym_app.llm_generator.get_groq_api_key", return_value="test-key")
def test_generate_workout_uses_groq_when_available(mock_key, mock_groq) -> None:
    from gym_app.generated_models import GeneratedExercise, GeneratedWorkout

    mock_groq.return_value = GeneratedWorkout(
        muscle_group="Chest",
        sub_area="Upper chest",
        difficulty="intermediate",
        exercises=[GeneratedExercise(name="LLM Press", sets=3, reps="10")],
        notes="From Groq",
    )

    workout = generate_workout("Chest", "Upper chest", "intermediate")
    assert workout.exercises[0].name == "LLM Press"
    mock_groq.assert_called_once()


@patch("gym_app.llm_generator.generate_workout_with_groq", side_effect=LLMGenerationError("fail"))
@patch("gym_app.llm_generator.get_groq_api_key", return_value="test-key")
def test_generate_workout_falls_back_on_llm_error(mock_key, mock_groq) -> None:
    workout = generate_workout("Chest", "Upper chest", "intermediate")
    assert len(workout.exercises) >= 4
