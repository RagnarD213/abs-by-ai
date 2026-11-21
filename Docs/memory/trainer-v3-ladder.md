---
name: trainer-v3-ladder
description: "AI Trainer v3 (shipped July 15 2026) — 7-stage ladder, sex + equipment tracks, none/min/full tiers, timed circuits"
metadata: 
  node_type: memory
  type: project
  originSessionId: 59968d1b-1706-477a-87a9-e2706f8563e8
---

AI Trainer **v3** shipped July 15 2026 (commit "AI Trainer v3: 7-stage ladder…"), replacing the v2 6-phase ladder. Spec: repo `HANDOFF_trainer_v3.md` + `TRAINER_V3_WORKOUTS.md`. Builds on [[ai-trainer-membership]].

**Ladder:** 7 stages, everyone trains daily total-body, abs finisher every day. Stages 1–3 = home (bodyweight → minimal kit → minimal kit longer), **timed circuits** (30/30, 30/20, 40/20×3). Stage 4 = first gym stage, switches to **sets×reps**; Stages 4–7 add a zone-2 cardio block the app renders before lifting. Isolation + functional moves unlock **only at Stages 5–7**. No exercise repeats on consecutive days from Stage 3 up.

**Equipment tiers** (`exercises.js`): retiered `none/db/gym` → **`none/min/full`** (dumbbells are `full` now). `min` = kettlebell + push-up handles + ab wheel + mat (NO dumbbells, **no resistance band** — minimal-track chest is push-up-dominant, band-only swaps fall back to bodyweight). `equipForStage(stage, track)`: 1→none, 2/3→min, 4-7→full (or `min` on the minimal track).

**Two tracks:** `sex_track` (woman=lower/glute emphasis, man=upper/delts+arms) chosen at intake; `equipment_track` (`full`|`minimal`) decided entering Stage 4 via an upgrade nudge → `POST /api/program/equipment-track` rebuilds the block on the chosen track.

**Safety (§5, in the system prompt + whitelist):** no barbell/DB deadlift (only `kb-deadlift`/`kb-swing`); no flat/incline bench (fly-dominant chest; pushes via machine-chest-press/db-floor-press/push-ups); squat = leg-press → safety-bar → barbell, barbell/safety-bar only at Stages 6–7. `db-rdl` + flat `db-bench-press` are excluded from selection but still resolvable for old stored programs.

**Assessment/progression:** block 1 = ASSESS mode (model picks starting stage 1–cap from photos; experience caps at beginner 3 / intermediate 4 / advanced 5, hard cap 5). Check-in progression is **workout-based**: ≥50% of the block's 28 workouts logged → +1 stage, else hold; "too hard" holds. Cap 7.

**Storage decision:** `stage` / `equipment_track` / `sex_track` live in the program (and `sex_track` in intake) **JSONB** — NOT new `programs` columns — mirroring the existing `program.phase` pattern, so no DB migration. `programStage()` reads `stage ?? phase` for back-compat with v2 rows.

**Generation-reliability rebuild (SHIPPED July 15 2026, commit "never-fail program generation").** The old single `claude-sonnet-4-6` call at `max_tokens:16000` generating all 28 days ran ~200–265s and ~half of prod test runs 502'd (socket killed crossing a proxy timeout). Now:
- `callTrainerModel` = per-attempt AbortController deadline + retry-with-backoff on transient errors (429/5xx/network reset); 4xx fails fast. Nutritionist/sleep/brief calls inherit it.
- Generation is **one short call PER WEEK** (~50s): `ASSESS_WEEK1_SCHEMA` (assessment + week 1) then `WEEK_SCHEMA` (one later week, prior weeks passed as context). `generate-program`/`checkin`/`equipment-track` return week 1 (AI) + deterministic weeks 2-4 immediately; `POST /api/program/week` upgrades each pending week. `weeksPending` (also on `GET /api/program`) drives client resume.
- **Deterministic builder** `buildDeterministicWeek` (server.js) — rule-correct weeks from the whitelist + stage/sex/equipment (role buckets in `DET_ROLES`, `detSlots`/`detRx`), powering locked-week teasers AND the never-fail fallback. Verified locally: with a broken API key `generate-program` returns a full valid 4-week plan in **0.2s** instead of hanging/502.
- Client: shows week 1 at once, "Personalizing week N of 4…" banner, per-week retry, resume-on-return via saved `weeksPending` (`upgradePendingWeeks()` in index.html). `buildTrainerUserContent` was removed (dead).

Refined so ONLY the small assessment call blocks the endpoint (commit "make program delivery instant"): `generate-program` returns after the assessment (weeks all deterministic, `weeksPending:[1,2,3,4]`, client upgrades in background). **Confirmed on prod July 15 2026:** the beginner/woman/minimal intake that failed 3/3 before now returns **HTTP 200 in ~14s** with a real AI assessment (correctly picked Stage 2 for a heavier beginner). Delivery is now fast + never-fails. Not yet live-tested with a real member token: the background `/api/program/week` upgrade producing AI weeks (structure verified locally; uses the same real-key path as the working assessment call).
