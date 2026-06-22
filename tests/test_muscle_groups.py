import pytest

from gym_app.muscle_groups import (
    MUSCLE_GROUPS,
    get_muscle_groups,
    get_sub_areas,
    is_valid_muscle_group,
    is_valid_sub_area,
)


def test_all_eleven_muscle_groups_defined() -> None:
    assert len(MUSCLE_GROUPS) == 11
    assert get_muscle_groups() == [
        "Chest",
        "Back",
        "Shoulders",
        "Biceps",
        "Triceps",
        "Forearms",
        "Abs / Core",
        "Quads",
        "Hamstrings",
        "Glutes",
        "Calves",
    ]


def test_chest_sub_areas() -> None:
    assert get_sub_areas("Chest") == ["Upper chest", "Middle chest", "Lower chest"]


def test_back_sub_areas() -> None:
    assert get_sub_areas("Back") == ["Lats", "Traps", "Rhomboids", "Lower back"]


def test_abs_core_sub_areas() -> None:
    assert get_sub_areas("Abs / Core") == [
        "Upper abs",
        "Lower abs",
        "Obliques",
        "Deep core",
    ]


def test_unknown_muscle_group_raises() -> None:
    with pytest.raises(ValueError, match="Unknown muscle group"):
        get_sub_areas("Invalid")


def test_is_valid_muscle_group_and_sub_area() -> None:
    assert is_valid_muscle_group("Glutes") is True
    assert is_valid_muscle_group("Invalid") is False
    assert is_valid_sub_area("Glutes", "Butt muscles") is True
    assert is_valid_sub_area("Glutes", "Lats") is False
