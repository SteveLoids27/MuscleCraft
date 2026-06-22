from __future__ import annotations

import json

from flask import Flask, render_template, request

from gym_app.difficulty import DIFFICULTY_LABELS, Difficulty
from gym_app.generator import generate_workout
from gym_app.muscle_groups import MUSCLE_GROUPS, get_muscle_groups


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.setdefault("PREFER_LLM", True)

    @app.get("/")
    def index():
        return render_template(
            "generate.html",
            muscle_groups=get_muscle_groups(),
            muscle_groups_json=json.dumps(MUSCLE_GROUPS),
            difficulties=list(Difficulty),
            difficulty_labels=DIFFICULTY_LABELS,
        )

    @app.post("/generate")
    def generate():
        try:
            muscle_group = request.form["muscle_group"].strip()
            sub_area = request.form.get("sub_area", "").strip() or None
            difficulty = request.form["difficulty"].strip()
            workout = generate_workout(
                muscle_group,
                sub_area,
                difficulty,
                prefer_llm=app.config["PREFER_LLM"],
            )
        except (KeyError, ValueError) as error:
            return render_template(
                "generate.html",
                muscle_groups=get_muscle_groups(),
                muscle_groups_json=json.dumps(MUSCLE_GROUPS),
                difficulties=list(Difficulty),
                difficulty_labels=DIFFICULTY_LABELS,
                error=str(error),
                selected=request.form,
            ), 400

        return render_template("workout_result.html", workout=workout)

    return app


def main() -> None:
    app = create_app()
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
