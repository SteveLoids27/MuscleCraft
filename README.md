# MuscleCraft

**AI-powered workout generator** — pick a muscle group and difficulty, get a complete gym plan in seconds.

MuscleCraft is a Flask web app that generates personalized workouts from your target muscles and skill level. It uses **Groq** (Llama) when configured, with a curated **template fallback** so you always get a usable plan.

> This is a **workout generator**, not a logging app. The main flow is: select → generate → train.

---

## Features

- **11 muscle groups** with optional sub-areas (e.g. Chest → Upper chest)
- **3 difficulty levels** — Basic, Intermediate, Advanced
- **AI generation** via Groq with automatic template fallback
- **Save & history** — store generated workouts locally
- **Copy workout** — one-click clipboard export
- **Form validation** and clear error messages
- **70+ pytest tests**

---

## Quick start

### Prerequisites

- Python 3.10+
- (Optional) [Groq API key](https://console.groq.com/) for AI-generated workouts

### Install

```bash
git clone git@github.com:SteveLoids27/MuscleCraft.git
cd MuscleCraft
pip install -r requirements.txt
```

### Configure (optional)

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Without `GROQ_API_KEY`, the app uses built-in exercise templates.

### Run

```bash
python -m gym_app.web
```

Open **http://127.0.0.1:5000**

### Test

```bash
python -m pytest -v
```

---

## How it works

1. Choose **muscle group**, optional **sub-area**, and **difficulty**
2. Click **Generate workout**
3. Review exercises with sets, reps, and notes
4. **Copy**, **regenerate**, or **save** to history

Saved workouts are stored at `~/.gym_workouts/generated.json`.

---

## Project structure

```text
gym_app/
  web.py              # Flask routes & app factory
  generator.py        # Orchestrates LLM + template generation
  llm_generator.py    # Groq integration
  muscle_groups.py    # Muscle group catalog
  difficulty.py       # Difficulty levels
  validation.py       # Form validation
  generated_models.py # Workout data models
  generated_storage.py
  formatting.py       # Copy-to-clipboard text
  data/exercises.json # Template exercise library
  prompts/            # LLM system prompt
  templates/          # Jinja2 HTML templates
  static/style.css
.cursor/
  agents/             # Cursor subagents (planner, builder, tester, improver)
  rules/              # Pipeline, git workflow, auto-review rules
tests/                # pytest suite
BUILD_PROMPT.md       # Milestone build guide for agents
APP_SPEC.md           # Product specification
```

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Web | Flask |
| AI (runtime) | Groq API — Llama 3.3 70B Versatile |
| AI (development) | Cursor Agent + custom subagents |
| Storage | Local JSON |
| Tests | pytest |

---

## AI in the application

MuscleCraft uses AI at **runtime** to generate workouts and was built with AI **development agents** in Cursor.

### Runtime AI — workout generation

| Function | File | Description |
|----------|------|-------------|
| `generate_workout()` | `gym_app/generator.py` | Main entry — tries Groq first, falls back to templates |
| `generate_workout_with_notice()` | `gym_app/generator.py` | Same as above; returns a user-facing notice when LLM fails |
| `generate_workout_with_groq()` | `gym_app/llm_generator.py` | Calls Groq chat completions API |
| `generate_workout_from_template()` | `gym_app/generator.py` | Curated JSON exercise library (no API key required) |
| System prompt | `gym_app/prompts/workout_generator.md` | Coach persona + JSON output schema for the LLM |

**Flow:**

```text
User selects muscle group + difficulty
        │
        ▼
  GROQ_API_KEY set?
    │         │
   yes        no
    │         └──► Template generator (exercises.json)
    ▼
 Groq API (Llama 3.3)
    │
    ├─ success ──► Structured workout JSON → GeneratedWorkout
    └─ failure ──► Template fallback + notice in UI
```

**Environment variables:**

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `GROQ_API_KEY` | No | — | Enables AI workout generation |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Groq model name |
| `FLASK_SECRET_KEY` | No | dev default | Flask session signing |

**LLM output:** 4–6 exercises with sets, reps, and form notes, validated and parsed into `GeneratedWorkout` models.

---

## AI agents used to build MuscleCraft

This app was built **milestone-by-milestone** using [Cursor](https://cursor.com) Agent mode with custom subagents, rules, and build guides in `.cursor/`.

### Build pipeline

Each feature followed this pipeline (defined in `.cursor/rules/app-builder-pipeline.mdc`):

```text
app-planner  →  app-builder  →  safe-code-improver  →  app-tester
   plan            implement         review               verify
```

After every code change, `safe-code-improver` runs automatically (`.cursor/rules/auto-safe-code-review.mdc`).

### Cursor subagents

| Agent | Model | Role |
|-------|-------|------|
| **app-planner** | Claude Sonnet 4.6 | Breaks `APP_SPEC.md` into small milestones with acceptance criteria |
| **app-builder** | Claude Fable 5 | Implements **one milestone** per session — minimal working code + tests |
| **safe-code-improver** | Claude Fable 5 | Behavior-preserving refactors — naming, clarity, dead code removal |
| **app-tester** | GPT-5.3 Codex | Runs `pytest`, smoke tests, and checks acceptance criteria |

Agent definitions live in `.cursor/agents/`.

### Cursor rules & automation

| File | Purpose |
|------|---------|
| `.cursor/rules/app-builder-pipeline.mdc` | Milestone pipeline — plan → build → review → test |
| `.cursor/rules/auto-safe-code-review.mdc` | Auto-invoke `safe-code-improver` after code edits |
| `.cursor/rules/git-pr-workflow.mdc` | Branch workflow — `dev-Steve` → PR → `main` |
| `BUILD_PROMPT.md` | 7-milestone build guide with agent prompts |
| `APP_SPEC.md` | Product vision, data model, routes |
| `.cursor/automation/README.md` | One-milestone-at-a-time automation guide |

### Milestones completed (agent-built)

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Data foundation (models, muscle groups, difficulty, storage) | done |
| 2 | Template workout generator (fallback engine) | done |
| 3 | Generator web UI (dropdowns + results) | done |
| 4 | LLM integration (Groq) | done |
| 5 | Save & view workout history | done |
| 6 | Legacy logging cleanup | done |
| 7 | Polish, errors & full test coverage | done |

### How to build the next feature with agents

In **Cursor Agent mode** on branch `dev-Steve`:

```
Build <feature name> on dev-Steve. Follow the app-builder pipeline:
app-planner → app-builder → safe-code-improver → app-tester
```

Or reference a new milestone in `BUILD_PROMPT.md`:

```
Build Milestone N from BUILD_PROMPT.md
```

---

## Development

| Branch | Purpose |
|--------|---------|
| `main` | Stable, reviewed code |
| `dev-Steve` | Active feature development |

New work goes on `dev-Steve`, then merges into `main` via pull request.

See [BUILD_PROMPT.md](./BUILD_PROMPT.md) and [APP_SPEC.md](./APP_SPEC.md) for the full product spec and build milestones.

---

## License

MIT (or specify your license here)

---

Built with MuscleCraft — forge your next session.
