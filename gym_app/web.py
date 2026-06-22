from __future__ import annotations

import json
import os

from flask import Flask, abort, redirect, render_template, request, url_for

from gym_app.difficulty import DIFFICULTY_LABELS, Difficulty
from gym_app.formatting import format_workout_text
from gym_app.generated_models import GeneratedWorkout
from gym_app.generated_storage import GeneratedWorkoutStorage
from gym_app.generator import generate_workout_with_notice
from gym_app.muscle_groups import MUSCLE_GROUPS, get_muscle_groups
from gym_app.validation import validate_generate_form


def create_app(storage: GeneratedWorkoutStorage | None = None) -> Flask:
    app = Flask(__name__)
    app.config.setdefault("PREFER_LLM", True)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
    workout_storage = storage or GeneratedWorkoutStorage()

    def _generator_context(error: str | None = None, selected=None, notice: str | None = None):
        return {
            "muscle_groups": get_muscle_groups(),
            "muscle_groups_json": json.dumps(MUSCLE_GROUPS),
            "difficulties": list(Difficulty),
            "difficulty_labels": DIFFICULTY_LABELS,
            "error": error,
            "notice": notice,
            "selected": selected,
        }

    def _workout_context(workout: GeneratedWorkout, **extra):
        return {
            "workout": workout,
            "copy_text": format_workout_text(workout),
            **extra,
        }

    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, "description", None) or "Invalid request."
        return (
            render_template(
                "error.html",
                title="Invalid request",
                message=message,
                back_url=url_for("index"),
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            render_template(
                "error.html",
                title="Not found",
                message="That page or workout could not be found.",
                back_url=url_for("workouts"),
            ),
            404,
        )

    @app.get("/")
    def index():
        return render_template("generate.html", **_generator_context())

    @app.post("/generate")
    def generate():
        selected = request.form
        try:
            muscle_group, sub_area, difficulty = validate_generate_form(request.form)
            workout, notice = generate_workout_with_notice(
                muscle_group,
                sub_area,
                difficulty,
                prefer_llm=app.config["PREFER_LLM"],
            )
        except ValueError as error:
            return (
                render_template(
                    "generate.html",
                    **_generator_context(str(error), selected),
                ),
                400,
            )
        except Exception:
            return (
                render_template(
                    "generate.html",
                    **_generator_context(
                        "Something went wrong generating your workout. Please try again.",
                        selected,
                    ),
                ),
                500,
            )

        return render_template(
            "workout_result.html",
            **_workout_context(workout, saved=False, notice=notice),
        )

    @app.post("/workouts/save")
    def save_workout():
        try:
            payload = json.loads(request.form["workout_json"])
            workout = GeneratedWorkout.from_dict(payload)
        except (KeyError, ValueError, json.JSONDecodeError) as error:
            return (
                render_template(
                    "error.html",
                    title="Could not save workout",
                    message=f"The workout data was invalid or incomplete. ({error})",
                    back_url=url_for("index"),
                ),
                400,
            )

        try:
            workout_storage.add(workout)
        except OSError:
            return (
                render_template(
                    "error.html",
                    title="Could not save workout",
                    message="Unable to write to storage. Please try again.",
                    back_url=url_for("index"),
                ),
                500,
            )

        return redirect(url_for("workout_detail", workout_id=workout.id))

    @app.get("/workouts")
    def workouts():
        return render_template(
            "workouts.html",
            workouts=workout_storage.list_all(),
        )

    @app.get("/workouts/<workout_id>")
    def workout_detail(workout_id: str):
        workout = workout_storage.get_by_id(workout_id)
        if workout is None:
            abort(404)
        return render_template("workout_detail.html", **_workout_context(workout))

    return app


def main() -> None:
    app = create_app()
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
