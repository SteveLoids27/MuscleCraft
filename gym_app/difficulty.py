from __future__ import annotations

from enum import Enum


class Difficulty(str, Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


DIFFICULTY_LABELS: dict[Difficulty, str] = {
    Difficulty.BASIC: "Basic",
    Difficulty.INTERMEDIATE: "Intermediate",
    Difficulty.ADVANCED: "Advanced",
}


def get_difficulties() -> list[Difficulty]:
    return list(Difficulty)


def get_difficulty_labels() -> list[str]:
    return [DIFFICULTY_LABELS[level] for level in Difficulty]


def parse_difficulty(value: str) -> Difficulty:
    normalized = value.strip().lower()
    for level in Difficulty:
        if level.value == normalized or DIFFICULTY_LABELS[level].lower() == normalized:
            return level
    raise ValueError(
        f"Unknown difficulty: {value}. Use basic, intermediate, or advanced."
    )
