from __future__ import annotations

import json
from pathlib import Path

from gym_app.generated_models import GeneratedWorkout

DEFAULT_GENERATED_PATH = Path.home() / ".gym_workouts" / "generated.json"


class GeneratedWorkoutStorage:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DEFAULT_GENERATED_PATH

    def load_all(self) -> list[GeneratedWorkout]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [GeneratedWorkout.from_dict(item) for item in raw]

    def save_all(self, workouts: list[GeneratedWorkout]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [workout.to_dict() for workout in workouts]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add(self, workout: GeneratedWorkout) -> None:
        workouts = self.load_all()
        workouts.append(workout)
        self.save_all(workouts)

    def get_by_id(self, workout_id: str) -> GeneratedWorkout | None:
        for workout in self.load_all():
            if workout.id == workout_id:
                return workout
        return None

    def list_all(self) -> list[GeneratedWorkout]:
        return sorted(self.load_all(), key=lambda workout: workout.created_at, reverse=True)
