from __future__ import annotations

MUSCLE_GROUPS: dict[str, list[str]] = {
    "Chest": ["Upper chest", "Middle chest", "Lower chest"],
    "Back": ["Lats", "Traps", "Rhomboids", "Lower back"],
    "Shoulders": ["Front delts", "Side delts", "Rear delts"],
    "Biceps": ["Front upper arm muscles"],
    "Triceps": ["Back upper arm muscles"],
    "Forearms": ["Grip and lower arm muscles"],
    "Abs / Core": ["Upper abs", "Lower abs", "Obliques", "Deep core"],
    "Quads": ["Front of thighs"],
    "Hamstrings": ["Back of thighs"],
    "Glutes": ["Butt muscles"],
    "Calves": ["Lower back of legs"],
}


def get_muscle_groups() -> list[str]:
    return list(MUSCLE_GROUPS.keys())


def get_sub_areas(muscle_group: str) -> list[str]:
    if muscle_group not in MUSCLE_GROUPS:
        raise ValueError(f"Unknown muscle group: {muscle_group}")
    return list(MUSCLE_GROUPS[muscle_group])


def is_valid_muscle_group(muscle_group: str) -> bool:
    return muscle_group in MUSCLE_GROUPS


def is_valid_sub_area(muscle_group: str, sub_area: str) -> bool:
    return sub_area in MUSCLE_GROUPS.get(muscle_group, [])
