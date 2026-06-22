# Gym Workout App — Spec

> **Agent build guide:** See [BUILD_PROMPT.md](./BUILD_PROMPT.md) for milestones, steps, and iteration prompts.

## Product vision

This is a **workout generation application**, not a workout logging app.

The **main output** is a personalized workout plan generated from two user inputs:

1. **Muscle group** (and optional sub-area)
2. **Difficulty** (basic, intermediate, advanced)

The user selects a target muscle group and difficulty level, then the app produces a ready-to-follow workout — exercises, sets, reps, and guidance — tailored to that combination.

This is **not** a logging app. The core experience is: select inputs → generate workout → follow the plan.

---

## Status legend

| Status | Meaning |
|--------|---------|
| `done` | Shipped in the app |
| `planned` | Approved for development, not started |
| `in_progress` | Currently being built |
| `legacy` | Early prototype; will be replaced or removed |

---

## Stack

- Python 3.10+
- Flask (web UI)
- LLM API for workout generation (provider TBD)
- Standard library + `pytest` for tests

---

## Core features (primary)

These define what the application is for.

### 1. Muscle group dropdown

**Purpose:** Let the user choose which muscle group the generated workout should target.

| Muscle group | Sub-areas |
|--------------|-----------|
| **Chest** | Upper chest, middle chest, lower chest |
| **Back** | Lats, traps, rhomboids, lower back |
| **Shoulders** | Front delts, side delts, rear delts |
| **Biceps** | Front upper arm muscles |
| **Triceps** | Back upper arm muscles |
| **Forearms** | Grip and lower arm muscles |
| **Abs / Core** | Upper abs, lower abs, obliques, deep core |
| **Quads** | Front of thighs |
| **Hamstrings** | Back of thighs |
| **Glutes** | Butt muscles |
| **Calves** | Lower back of legs |

**UI behavior:**

- Primary dropdown: muscle group (Chest, Back, Shoulders, etc.)
- Secondary dropdown (optional): sub-area when the group has multiple targets
- **Required** before generating a workout

**Status:** `done`

---

### 2. Difficulty dropdown

**Purpose:** Control how hard the generated workout should be.

| Value | Description |
|-------|-------------|
| **Basic** | Beginner-friendly exercises, lower volume, simpler movements |
| **Intermediate** | Moderate volume and complexity |
| **Advanced** | Higher volume, compound/isolation mix, challenging progressions |

**UI behavior:**

- Single select: `Basic`, `Intermediate`, `Advanced`
- **Required** before generating a workout
- Drives exercise selection, volume, and intensity in the generated plan

**Status:** `done`

---

### 3. Workout generator (main output)

**Purpose:** Produce the workout plan — the primary deliverable of the app.

**Inputs:**

- Muscle group (from dropdown)
- Sub-area (optional)
- Difficulty (from dropdown)

**Output (main product):**

- A complete workout plan displayed on screen:
  - Exercise names
  - Sets and reps per exercise
  - Optional rest notes or form cues
  - Brief workout summary (focus area + difficulty)
- User can **regenerate**, **copy**, or **save** the plan

**Example flow:**

1. User opens the app
2. Selects **Back** → **Lats** and **Intermediate**
3. Clicks **Generate workout**
4. App displays a structured workout (e.g. pull-ups, barbell rows, lat pulldowns) with sets/reps
5. User follows the plan in the gym

**Generation approach:**

- **LLM integration (Groq):** Language model generates varied workouts; falls back to templates if unavailable
- API key via environment variable (not committed to the repo)

**Status:** `done`

---

## Feature roadmap (summary)

See [BUILD_PROMPT.md](./BUILD_PROMPT.md) for the full 7-milestone build plan and agent prompts.

| # | Feature | Priority | Status |
|---|---------|----------|--------|
| 1 | Data foundation (models, muscle groups, storage) | Core | done |
| 2 | Template workout generator (fallback) | Core | done |
| 3 | Generator web UI (dropdowns + results) | Core | done |
| 4 | LLM integration (Groq) | Core | done |
| 5 | Save / view generated history | Secondary | done |
| 6 | Legacy logging cleanup | — | done |
| 7 | Polish & tests | — | done |

---

## Current web routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Generator home — muscle group + difficulty dropdowns |
| `/generate` | POST | Generate workout from selections (main output) |
| `/workouts/save` | POST | Save a generated workout |
| `/workouts` | GET | List saved generated workouts |
| `/workouts/<id>` | GET | View a saved generated workout |

---

## Run the app

```bash
pip install -r requirements.txt
python -m gym_app.web
```

Open http://127.0.0.1:5000

---

## Data model

```text
GeneratedWorkout
  - id: str
  - created_at: ISO datetime
  - muscle_group: str          # e.g. "Chest"
  - sub_area: str | null       # e.g. "Upper chest"
  - difficulty: str            # basic | intermediate | advanced
  - exercises: list[GeneratedExercise]
  - notes: str (optional)

GeneratedExercise
  - name: str
  - sets: int
  - reps: str                  # e.g. "10" or "8-12"
  - notes: str (optional)      # form cues, rest, etc.
```

---

## Storage

- Generated workouts: `~/.gym_workouts/generated.json`

## Done when

- [x] User selects muscle group + difficulty and **generates a workout** as the main output
- [x] Generated plan shows exercises with sets/reps (and notes)
- [x] LLM generation works with template fallback
- [x] User can save and view generated workout history
- [x] Legacy logging code is removed
- [x] All pytest tests pass

## Future ideas (not yet scheduled)

- Exercise library / curated templates as LLM fallback
- Export workout (PDF, share link)
- Progress tracking over time
- Rest timer between sets
- User accounts and saved preferences
