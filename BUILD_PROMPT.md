# Gym Workout App — Agent Build Prompt

This file is the **iteration guide for Cursor agents** building the workout generation application.

**Read first:** [APP_SPEC.md](./APP_SPEC.md) (product vision, data model, routes).

**Rule:** Build **one milestone per session**. Do not skip ahead. Update the milestone status table below when you finish.

---

## How agents should use this file

| Agent | Role | When to run |
|-------|------|-------------|
| `app-planner` | Confirm next milestone, acceptance criteria, files | Start of session or when blocked |
| `app-builder` | Implement **one** `in_progress` milestone | Main build work |
| `safe-code-improver` | Safe refactor after code changes | After `app-builder` |
| `app-tester` | Run `pytest`, verify acceptance criteria | After `safe-code-improver` |

### Session workflow

1. Read `APP_SPEC.md` and this file.
2. Find the **first milestone** with status `pending` — mark it `in_progress`.
3. `app-builder` implements only that milestone.
4. `safe-code-improver` reviews changed files.
5. `app-tester` runs tests and checks acceptance criteria.
6. Mark milestone `done` in this file (and sync `APP_SPEC.md` roadmap if needed).
7. End with `MILESTONE_COMPLETE` or `MILESTONE_BLOCKED: <reason>`.

### Constraints (all milestones)

- This is a **workout generator**, not a logging app.
- Home page = muscle group + difficulty → **Generate workout**.
- Remove or ignore legacy logging UX when a milestone says to replace it.
- Use `pytest` — all tests must pass before marking `done`.
- API keys via environment variables only (never commit secrets).
- Prefer small diffs; match existing `gym_app/` structure.

---

## Milestone status

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Data foundation (models, muscle groups, difficulty, storage) | `done` |
| 2 | Template workout generator (no LLM — fallback engine) | `done` |
| 3 | Generator web UI (dropdowns + results page) | `done` |
| 4 | LLM workout generator integration | `done` |
| 5 | Save & view generated workout history | `pending` |
| 6 | Legacy cleanup (remove logging prototype) | `done` |
| 7 | Polish, error handling & full test coverage | `pending` |

---

## Milestone 1 — Data foundation

**Goal:** Define the data layer for generated workouts — models, muscle group catalog, difficulty levels, and JSON storage.

**Status:** `done`

### Steps

1. Create `gym_app/muscle_groups.py` with all muscle groups and sub-areas from `APP_SPEC.md`.
2. Create `gym_app/difficulty.py` with `Basic`, `Intermediate`, `Advanced` constants/enums.
3. Create `gym_app/generated_models.py` with `GeneratedWorkout` and `GeneratedExercise` dataclasses (match `APP_SPEC.md`).
4. Create `gym_app/generated_storage.py` to save/load generated workouts to `~/.gym_workouts/generated.json`.
5. Add `tests/test_muscle_groups.py`, `tests/test_generated_models.py`, `tests/test_generated_storage.py`.
6. Do **not** remove legacy logging code yet — only add new modules.

### Files

| Action | Path |
|--------|------|
| Create | `gym_app/muscle_groups.py` |
| Create | `gym_app/difficulty.py` |
| Create | `gym_app/generated_models.py` |
| Create | `gym_app/generated_storage.py` |
| Create | `tests/test_muscle_groups.py` |
| Create | `tests/test_generated_models.py` |
| Create | `tests/test_generated_storage.py` |

### Acceptance criteria

- [x] All 11 muscle groups and sub-areas are defined and queryable.
- [x] Three difficulty levels exist: `basic`, `intermediate`, `advanced`.
- [x] `GeneratedWorkout` / `GeneratedExercise` serialize to/from JSON.
- [x] Storage can save, load, and retrieve generated workouts by id.
- [x] All pytest tests pass.

### Agent prompt

```
Build Milestone 1 from BUILD_PROMPT.md: data foundation for the workout generator.
Read APP_SPEC.md for the data model and muscle groups. Implement only Milestone 1.
```

---

## Milestone 2 — Template workout generator

**Goal:** A deterministic workout generator (no LLM) so the app can produce workouts before API integration. This becomes the **fallback** when the LLM is unavailable.

**Status:** `done`

### Steps

1. Create `gym_app/generator.py` with a `generate_workout(muscle_group, sub_area, difficulty) -> GeneratedWorkout` function.
2. Use curated exercise templates per muscle group + difficulty (hardcoded dict or JSON in `gym_app/data/exercises.json`).
3. Each generated workout has 4–6 exercises with sets, reps, and short notes.
4. Difficulty affects volume: Basic = fewer sets/simpler exercises; Advanced = more sets/compound movements.
5. Add `tests/test_generator.py` covering at least 3 muscle groups × 3 difficulty levels.

### Files

| Action | Path |
|--------|------|
| Create | `gym_app/generator.py` |
| Create | `gym_app/data/exercises.json` (optional curated templates) |
| Create | `tests/test_generator.py` |

### Acceptance criteria

- [x] `generate_workout("Chest", "Upper chest", "intermediate")` returns a valid `GeneratedWorkout`.
- [x] Basic workouts use simpler exercises and lower volume than Advanced.
- [x] Invalid muscle group or difficulty raises a clear error.
- [x] All pytest tests pass.

### Agent prompt

```
Build Milestone 2 from BUILD_PROMPT.md: template-based workout generator (no LLM).
Use Milestone 1 models. Implement generate_workout() with curated exercises per muscle group and difficulty.
```

---

## Milestone 3 — Generator web UI

**Goal:** Replace the logging-first home page with the **generator UI** — muscle group dropdown, sub-area dropdown, difficulty dropdown, and workout results display.

**Status:** `done`

### Steps

1. Refactor `gym_app/web.py`:
   - `GET /` → generator form (muscle group, sub-area, difficulty dropdowns).
   - `POST /generate` → call `generate_workout()`, render results.
2. Create `gym_app/templates/generate.html` (form) and `gym_app/templates/workout_result.html` (generated plan).
3. Update `gym_app/static/style.css` for generator-first layout.
4. Sub-area dropdown updates dynamically based on muscle group (server-side or simple JS).
5. Results page shows: summary, exercise table (name, sets, reps, notes), **Regenerate** button.
6. Add `tests/test_web_generator.py` for form + generate flow.
7. Legacy logging routes may remain temporarily but must not be the home page.

### Files

| Action | Path |
|--------|------|
| Edit | `gym_app/web.py` |
| Create | `gym_app/templates/generate.html` |
| Create | `gym_app/templates/workout_result.html` |
| Edit | `gym_app/static/style.css` |
| Create | `tests/test_web_generator.py` |

### Acceptance criteria

- [x] Home page shows muscle group and difficulty dropdowns (sub-area when applicable).
- [x] Submitting the form displays a generated workout with exercises, sets, and reps.
- [x] Regenerate produces a new workout (may vary if templates allow).
- [x] All pytest tests pass.

### Agent prompt

```
Build Milestone 3 from BUILD_PROMPT.md: generator web UI with dropdowns and workout results page.
Wire to the template generator from Milestone 2. Home page must be generation-first, not logging.
```

---

## Milestone 4 — LLM workout generator

**Goal:** Integrate an LLM to generate workouts from muscle group + difficulty. Fall back to the template generator (Milestone 2) if the API fails or no key is set.

**Status:** `done`

### Steps

1. Create `gym_app/llm_generator.py` with:
   - Prompt template including muscle group, sub-area, difficulty.
   - API client (Groq — use env var `GROQ_API_KEY`).
   - JSON response parsing into `GeneratedWorkout`.
2. Create `gym_app/prompts/workout_generator.md` — the system/user prompt template.
3. Update `gym_app/generator.py` to try LLM first, fall back to templates.
4. Add `.env.example` with `GROQ_API_KEY=` (do not commit real keys).
5. Add `tests/test_llm_generator.py` with **mocked** API responses (no real API calls in CI).
6. Update `requirements.txt` if an HTTP client SDK is needed.

### Files

| Action | Path |
|--------|------|
| Create | `gym_app/llm_generator.py` |
| Create | `gym_app/prompts/workout_generator.md` |
| Edit | `gym_app/generator.py` |
| Create | `.env.example` |
| Create | `tests/test_llm_generator.py` |
| Edit | `requirements.txt` |

### Acceptance criteria

- [x] With a valid API key, LLM generates a structured workout.
- [x] Without API key or on API error, template fallback still works.
- [x] LLM prompt includes muscle group, sub-area, and difficulty.
- [x] Tests use mocks only — no live API in pytest.
- [x] All pytest tests pass.

### Agent prompt

```
Build Milestone 4 from BUILD_PROMPT.md: LLM workout generator with template fallback.
Create prompt template, API client, and mocked tests. Read APP_SPEC.md for output format.
```

---

## Milestone 5 — Save & view generated history

**Goal:** Let users save generated workouts and browse past generations.

**Status:** `pending`

**Depends on:** Milestones 3, 4

### Steps

1. After generation, add **Save workout** button on results page.
2. `POST /workouts/save` — persist current `GeneratedWorkout` via `generated_storage.py`.
3. `GET /workouts` — list saved generated workouts (date, muscle group, difficulty).
4. `GET /workouts/<id>` — detail view for a saved generated workout.
5. Reuse or replace legacy `workouts.html` / `workout_detail.html` for generated workouts.
6. Add tests for save, list, and detail routes.

### Files

| Action | Path |
|--------|------|
| Edit | `gym_app/web.py` |
| Edit | `gym_app/templates/workout_result.html` |
| Edit | `gym_app/templates/workouts.html` |
| Edit | `gym_app/templates/workout_detail.html` |
| Create | `tests/test_web_history.py` |

### Acceptance criteria

- [ ] User can save a generated workout from the results page.
- [ ] `/workouts` lists saved workouts with muscle group, difficulty, and date.
- [ ] `/workouts/<id>` shows full exercise detail.
- [ ] All pytest tests pass.

### Agent prompt

```
Build Milestone 5 from BUILD_PROMPT.md: save and view generated workout history.
Use generated_storage from Milestone 1.
```

---

## Milestone 6 — Legacy cleanup

**Goal:** Remove the logging prototype so the codebase matches the product — a workout generator only.

**Status:** `done`

### Steps

1. Remove legacy routes: `/start`, `/log`.
2. Remove or archive: `gym_app/cli.py`, `gym_app/active.py`, logging parts of `gym_app/service.py`.
3. Remove logging templates (`index.html` log form) if replaced by `generate.html`.
4. Remove legacy tests for CLI logging and active workout tracker (or mark skipped with reason).
5. Update `gym_app/__main__.py` to run the web app, not CLI.
6. Update `APP_SPEC.md` — mark legacy items removed.

### Files

| Action | Path |
|--------|------|
| Delete/Edit | `gym_app/cli.py`, `gym_app/active.py`, `gym_app/service.py` |
| Edit | `gym_app/web.py`, `gym_app/__main__.py` |
| Delete | `tests/test_cli.py`, logging-related tests |
| Edit | `APP_SPEC.md` |

### Acceptance criteria

- [x] No logging-first UI or routes remain.
- [x] App entry point is the generator web UI only.
- [x] All remaining pytest tests pass.
- [x] `APP_SPEC.md` reflects generator-only product.

### Agent prompt

```
Build Milestone 6 from BUILD_PROMPT.md: remove legacy logging prototype.
Keep generator features intact. All tests must pass.
```

---

## Milestone 7 — Polish, errors & test coverage

**Goal:** Production-ready polish — validation, error messages, UI tweaks, and full test coverage.

**Status:** `pending`

**Depends on:** All previous milestones

### Steps

1. Validate all form inputs (required muscle group, difficulty).
2. User-friendly error pages and flash messages (invalid selection, save failure, LLM error).
3. UI polish: mobile layout, clear labels, loading state on Generate.
4. Add **Copy workout** button on results page (clipboard text).
5. Review test coverage — aim for all core paths tested.
6. Update `APP_SPEC.md` roadmap — mark core features `done`.
7. Final run: `python3 -m pytest -v` and manual smoke test of full flow.

### Files

| Action | Path |
|--------|------|
| Edit | `gym_app/web.py`, templates, `style.css` |
| Edit | `tests/` (fill gaps) |
| Edit | `APP_SPEC.md`, this file (mark all milestones `done`) |

### Acceptance criteria

- [ ] Full flow works: select muscle group + difficulty → generate → view → save → history.
- [ ] Errors are handled gracefully with clear messages.
- [ ] Copy workout works on results page.
- [ ] All pytest tests pass.
- [ ] `APP_SPEC.md` "Done when" criteria are met.

### Agent prompt

```
Build Milestone 7 from BUILD_PROMPT.md: polish, error handling, and full test coverage.
Verify APP_SPEC.md "Done when" criteria. Mark all milestones done in BUILD_PROMPT.md.
```

---

## End-to-end build order (summary)

```text
M1 Data foundation
  └─► M2 Template generator
        └─► M3 Generator UI
              └─► M4 LLM integration
                    └─► M5 Save & history
                          └─► M6 Legacy cleanup
                                └─► M7 Polish & tests
```

---

## Quick start (for the user)

To kick off the full build, say in Agent mode:

```
Read BUILD_PROMPT.md and APP_SPEC.md. Build the next pending milestone.
Follow the app-builder pipeline: plan → build → safe-code-improver → app-tester.
```

To build a specific milestone:

```
Build Milestone 3 from BUILD_PROMPT.md
```

---

## Definition of done (entire application)

From `APP_SPEC.md` — the app is complete when:

- [ ] User selects muscle group + difficulty and **generates a workout** as the main output.
- [ ] Generated plan shows exercises with sets/reps (and notes).
- [ ] LLM generation works with template fallback.
- [ ] User can save and view generated workout history.
- [ ] Legacy logging code is removed.
- [ ] All pytest tests pass.
