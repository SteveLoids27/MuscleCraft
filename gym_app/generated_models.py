from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class GeneratedExercise:
    name: str
    sets: int
    reps: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "sets": self.sets,
            "reps": self.reps,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GeneratedExercise:
        return cls(
            name=str(data["name"]),
            sets=int(data["sets"]),
            reps=str(data["reps"]),
            notes=str(data.get("notes", "")),
        )


@dataclass
class GeneratedWorkout:
    muscle_group: str
    difficulty: str
    exercises: list[GeneratedExercise] = field(default_factory=list)
    sub_area: str | None = None
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "muscle_group": self.muscle_group,
            "sub_area": self.sub_area,
            "difficulty": self.difficulty,
            "exercises": [exercise.to_dict() for exercise in self.exercises],
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GeneratedWorkout:
        return cls(
            id=str(data["id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            muscle_group=str(data["muscle_group"]),
            sub_area=data.get("sub_area"),
            difficulty=str(data["difficulty"]),
            exercises=[
                GeneratedExercise.from_dict(item) for item in data.get("exercises", [])
            ],
            notes=str(data.get("notes", "")),
        )
