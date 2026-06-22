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
  templates/          # Jinja2 HTML templates
  static/style.css
tests/                # pytest suite
```

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Web | Flask |
| AI | Groq API (Llama 3.3) |
| Storage | Local JSON |
| Tests | pytest |

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
