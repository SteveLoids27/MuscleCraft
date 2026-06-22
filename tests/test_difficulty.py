import pytest

from gym_app.difficulty import Difficulty, get_difficulties, get_difficulty_labels, parse_difficulty


def test_three_difficulty_levels() -> None:
    assert [level.value for level in get_difficulties()] == [
        "basic",
        "intermediate",
        "advanced",
    ]


def test_difficulty_labels() -> None:
    assert get_difficulty_labels() == ["Basic", "Intermediate", "Advanced"]


def test_parse_difficulty_accepts_value_and_label() -> None:
    assert parse_difficulty("basic") == Difficulty.BASIC
    assert parse_difficulty("Intermediate") == Difficulty.INTERMEDIATE
    assert parse_difficulty("ADVANCED") == Difficulty.ADVANCED


def test_parse_difficulty_invalid() -> None:
    with pytest.raises(ValueError, match="Unknown difficulty"):
        parse_difficulty("expert")
