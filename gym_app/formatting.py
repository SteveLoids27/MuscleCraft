from __future__ import annotations

from gym_app.generated_models import GeneratedWorkout


def format_workout_text(workout: GeneratedWorkout) -> str:
    focus = workout.muscle_group
    if workout.sub_area:
        focus = f"{focus} — {workout.sub_area}"

    lines = [
        f"Workout: {focus}",
        f"Difficulty: {workout.difficulty.title()}",
        "",
    ]
    if workout.notes:
        lines.extend([workout.notes, ""])

    for index, exercise in enumerate(workout.exercises, start=1):
        line = f"{index}. {exercise.name} — {exercise.sets} x {exercise.reps}"
        if exercise.notes:
            line = f"{line} ({exercise.notes})"
        lines.append(line)

    return "\n".join(lines)
