# Abs By AI — AI Trainer v2 Handoff (July 8, 2026)

## Executive summary
The AI trainer (shipped commit `618ded1`) gets a major revision, fully decided with Dan — a fresh session can start coding from the "Execution order" section. Four themes:

1. **Safety:** remove barbell bench press, barbell deadlift, and barbell back squat from the exercise library; no Olympic/powerlifting moves ever. Add flies + machine/dumbbell back replacements.
2. **Photos over questions:** cut the intake from 9 screens to ~5 by having Claude vision-read BOTH photos (before = starting point, AI-generated after = the goal). Add one new "goals beyond aesthetics" question.
3. **Daily total-body workouts:** everyone trains 7 days/week, every workout is total-body (NO push/pull/leg splits), with a phased duration ladder (10 min home → 45 min gym + zone-2 cardio).
4. **Inline SVG stick-figure animations** on every exercise card (style sample approved by Dan), keeping the YouTube button (video curation in progress separately).

## Key files
- `exercises.js` — the authoritative exercise whitelist (loaded by server + browser).
- `server.js:2205–2560` — trainer endpoints: `PROGRAM_SCHEMA`, `TRAINER_SYSTEM_PROMPT`, `buildTrainerUserContent`, `sanitizeProgram`, `stripProgramForPreview`, `VALID_INTAKE`/`validateIntake`, `/api/generate-program`, check-in/regeneration.
- `index.html:3176+` — `INTAKE_STEPS` wizard, program rendering, workout view. Photo keys: `LAST_BEFORE_KEY` / `LAST_AFTER_KEY` in localStorage.
- Deploy: push to `main` → Railway auto-deploys absbyai.com (auto commit+push authorized). Local Anthropic key is invalid — test Claude endpoints on prod. Local UI: `PORT=3456 ANTHROPIC_API_KEY=dummy GEMINI_API_KEY=dummy node server.js`.

---

## 1. Exercise library changes (`exercises.js`)

**Remove** (and fix any `swap:` fields that point at them):
- `bb-bench-press`, `bb-deadlift`, `bb-back-squat`

**Add** (full entries: setup / execution / mistake / swap / video:null):
- `db-fly` — Dumbbell Fly (equip: db, cat: push). Swap: db-floor-press.
- `cable-fly` — Cable Fly / Crossover (gym, push). Swap: db-fly.
- `pec-deck` — Pec Deck Machine Fly (gym, push). Swap: cable-fly.
- `chest-supported-db-row` — Chest-Supported Dumbbell Row (db, pull). Swap: db-row.
- `machine-row` — Machine Row (gym, pull). Swap: seated-cable-row.
- `back-extension` — 45° Back Extension (gym, pull/lower back). Swap: superman.
- `straight-arm-pulldown` — Straight-Arm Cable Pulldown (gym, pull). Swap: lat-pulldown.
- `machine-rear-delt-fly` — Reverse Pec Deck / Rear Delt Machine Fly (gym, pull). Swap: db-rear-delt-fly.
- `db-rear-delt-fly` — Bent-Over Dumbbell Rear Delt Fly (db, pull). Swap: superman.

**Rename:** `db-rdl` → display name "Dumbbell Hip Hinge" (keep the id for stored-program compatibility).

**Selection rules → add to `TRAINER_SYSTEM_PROMPT`:**
- NEVER program barbell bench press, deadlifts, back squats, cleans, snatches, jerks, or any powerlifting/Olympic lift — not even in cues or notes.
- Squat pattern: gym users → leg press (advanced) or goblet squat; beginners → goblet/bodyweight squat.
- Hamstrings: `leg-curl` (machine) is the DEFAULT for gym users. `db-rdl` (Dumbbell Hip Hinge) only when there is no machine access (home/db users), and NEVER in workouts under 15 min/day.
- Rear delts: `machine-rear-delt-fly` default for gym; `db-rear-delt-fly` when no machine.
- Chest: dumbbell/machine presses + flies (db-fly, cable-fly, pec-deck, machine-chest-press, db-bench-press, db-floor-press, push-up family).

`sanitizeProgram` already replaces unknown ids — removed ids resolve via their old library entry only if still in `EXERCISE_BY_ID`, so after deletion make sure the fallback path (same-category pick) covers old stored programs gracefully.

## 2. New intake (9 screens → 5)

New `INTAKE_STEPS` order:
1. **Photo consent** (moved to FIRST screen — it's now the headline: "Let AI read your before + after photos and build the plan to get you there"). If no photos on file, show two fallback screens instead: goal (old question 1) + a simple body-type picker.
2. **Equipment** (unchanged: home none / home dumbbells / full gym).
3. **Experience**: one tap — Beginner / Intermediate / Advanced ("I train consistently and know my way around a gym").
4. **Injuries** (unchanged chips + free text) + **optional age range** chips folded into this screen. Free-text placeholder should invite medical notes ("e.g. bad knee, doctor said no jumping, high blood pressure").
5. **NEW — "What do you want beyond the look?"** multi-select chips (the after photo shows the aesthetic goal; this captures what a photo can't): 
   - Lower my risk of heart disease / family history of heart disease
   - More energy day to day
   - Better mental health / less stress
   - Better sleep
   - Live longer / age well
   - Confidence
   - "Just the look is fine" (exclusive, like the injuries "None" chip)
   - Optional free text: "Anything else?"
   These feed `why_this_works` and exercise emphasis (e.g. heart-health goals → the zone-2 cardio phase gets framed around it).

**Cut entirely:** goal (derived from photos), days/week (everything is daily now), session length (derived from level), quit-reason, height/weight/sex (derived from photos; age stays as optional chips on screen 4).

**Server:** update `VALID_INTAKE`/`validateIntake` — remove `days_per_week`, `session_minutes`, `quit_reason`, most of `body`; add `health_goals: []` + `health_notes`, `experience: ['beginner','intermediate','advanced']`. Keep backward compat when reading OLD stored programs (render only; regeneration uses new shape — prompt the user through the new short intake if fields are missing).

**Additional questions Dan may add later (suggested, NOT building now unless he confirms):**
- "How active is your normal day?" (desk job / on my feet / physical work) — calibrates starting volume beyond what a photo shows.
- "What time will you work out?" (morning / lunch / evening) — powers workout-time push notifications (push infra exists at `/api/push/*`).

## 3. Photo vision analysis (both photos)

`buildTrainerUserContent` currently sends only the before photo. Change to send BOTH (localStorage `LAST_BEFORE_KEY` + `LAST_AFTER_KEY`, posted with the intake):
- Before photo → estimate starting point: rough body-fat range, muscle base, apparent fitness level.
- After photo (AI-generated future self) → the target: how much muscle to gain, fat to lose.
- The model derives the training goal from the GAP between them. Keep the existing "never judgmental" instruction.
- Assigned level = photo assessment COMBINED with the experience answer; the more conservative of the two wins (e.g. photo looks fit but user says beginner → beginner programming).
- Add a required `assessment` field to `PROGRAM_SCHEMA`: `{ starting_point, goal_summary, assigned_level, starting_phase }` so the UI can show "Here's what we saw" and the server can pin the ladder phase.

## 4. Daily total-body programming + phase ladder

Every plan is **7 days/week** and **every workout is total-body** — no push/pull/leg splits, ever. Under ~30 min that means compound moves only (squat, push-up, row, hinge, carry, core); isolation exercises (curls, lateral raises, flies, kickbacks, leg extension) are allowed ONLY at 30+ min/day. Daily is sustainable because volume per muscle per day is modest — the prompt must say "spread weekly volume across 7 light-moderate days; no muscle is trained to failure two days in a row."

**The phase ladder (everyone ends at Phase 6):**
| Phase | Duration/day | Where | Who starts here |
|---|---|---|---|
| 1 | 10 min | Home, bodyweight | Complete beginner (month 1) |
| 2 | 20 min | Home (db if available) | Beginner month 2 |
| 3 | 30 min | Gym | Beginner month 3 · **Intermediate month 1** |
| 4 | 35–40 min | Gym | Intermediate month 2 |
| 5 | 45 min | Gym | Intermediate month 3 · **Advanced month 1** |
| 6 | 45 min + 15 min zone-2 cardio warm-up | Gym | Advanced after 1 comfortable month — final phase for everyone |

- Home-only users (no gym) run the equivalent phases with their equipment tier; "gym" phases become full home versions.
- Program blocks stay ~4 weeks = one phase per block; the monthly check-in (existing regeneration endpoint) promotes to the next phase (or holds/demotes based on "too easy / too hard" + completion data). Store `phase` on the program row.
- Schema: replace "days per week" logic — each week has 7 days. Update `TRAINER_SYSTEM_PROMPT` session-length table for 10/20/30/40/45-min budgets (10 min ≈ 2-3 compound moves + ab finisher; 45 min ≈ 6-7 moves).
- Phase 6 renders a "Zone 2 cardio — 15 min" warm-up block (bike/incline walk/row at conversational pace) before the lifting.

## 5. Streaks, paywall, UX improvements
- **Forgiving streaks:** with daily workouts a missed day must not feel like failure. Streak metric = "weeks with 5+ workouts", and a missed day shows "Missed yesterday? Just do today." — never guilt.
- **Paywall:** free preview unlocks the **first 3 days** (was Day 1 only) — update `stripProgramForPreview` (`server.js:2336`).
- Keep the YouTube button on detail sheets; video URL curation is in progress separately (all `video: null` today).

## 6. SVG stick-figure animations (style APPROVED by Dan)
- Inline SVG + SMIL/CSS looping stick figures (~2s loop, line figures, round caps, `stroke: var(--acc)` or currentColor), one per exercise (~85), rendered directly on the exercise card at ~120px alongside the YouTube button.
- Approved sample: push-up (body pivots at feet, arms bend) and squat (hips back + down, arms reach forward) — head circle + polyline limbs, `<animate>` on coordinates, `calcMode="spline"` easing.
- Implement as an `anim` field or an `EXERCISE_ANIMS` map keyed by exercise id in `exercises.js` (or a separate `exercise-anims.js` loaded by both). Build after all functional work.

## Execution order
1. Exercise library: removals, additions, rename, prompt guardrails + selection rules. Verify `sanitizeProgram` handles removed ids in old stored programs.
2. Intake rebuild: 5 screens (+ no-photo fallbacks), new health-goals question, server `validateIntake` update.
3. Dual-photo vision + `assessment` schema field + level assignment.
4. Daily/phase-ladder programming: 7-day weeks, total-body rule, phase stored per block, check-in promotion, zone-2 block for Phase 6.
5. Paywall (first 3 days free) + forgiving streaks.
6. SVG animations for all exercises (pure content work, last).

Test each step locally with dummy keys for UI, on prod for Claude endpoints. Commit + push per step (authorized).
