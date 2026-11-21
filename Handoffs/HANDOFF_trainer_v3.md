# Abs By AI — AI Trainer v3 Workout Plan (July 14, 2026)

**Status: IMPLEMENTED (July 15, 2026).** Shipped in `exercises.js`, `exercise-anims.js`, `server.js`, `index.html`. §9 open items resolved: cap start at 5 ✓; drop `db-rdl` + flat `db-bench-press` from selection ✓; minimal-track chest stays **push-up-dominant (no resistance band)** — band-only swaps fall back to bodyweight. `stage` / `equipment_track` / `sex_track` are stored inside the program/intake JSONB (mirrors the existing `program.phase` pattern) rather than as new `programs` columns — no migration. Model-driven generation endpoints must be smoke-tested against a live Anthropic key on prod.
This revises the live v2 6-phase ladder (`server.js` `TRAINER_SYSTEM_PROMPT` @2902, `PHASES` @2947, `exercises.js` tiers `none/db/gym`) into a **7-stage** ladder that reflects the way Dan actually programs. All decisions below were confirmed with Dan on 2026-07-14.

---

## 1. The 7-stage ladder

Everyone trains **daily (7 days/week)**, **total-body every session** (upper + lower + abs whenever feasible), with **forgiving streaks** (metric = weeks with 5+ workouts; a missed day says "Missed yesterday? Just do today." — never guilt). Every workout ends with an **abs finisher** — it's Abs By AI.

| Stage | Total | Cardio | Lifting | Load method | Equipment floor | Functional moves |
|---|---|---|---|---|---|---|
| **1** | 5 min | — | 5 min bodyweight circuit | **Timed** (30s work / 30s rest) | **None** | No |
| **2** | 10 min | — | 10 min circuit | **Timed** (30s work / 20s rest) | **Minimal** (≤$200: kettlebell, push-up handles, ab wheel, yoga mat) | No |
| **3** | 20 min | — | 20 min | **Timed** (40s work / 20s rest, 3 rounds) | **Minimal — final home stage** (same kit as Stage 2, longer) | No |
| **4** | 20 min | 5 min | 15 min | **Sets & reps** (transition point) | **Full — first gym stage** *(or minimal track — see §4)* | No |
| **5** | 30 min | 5 min | 25 min | Sets & reps | Full *(or minimal track)* | **Yes** |
| **6** | 45 min | 10 min | 35 min | Sets & reps | Full *(or minimal track)* | Yes |
| **7** | 60 min | 15 min | 45 min | Sets & reps | Full *(or minimal track)* | Yes |

- **No exercise repeats on two consecutive days** from Stage 3 up (movements alternate within their bucket — e.g. leg press → walking lunge → leg press). Stages 1–2 circuits are short enough that some moves recur.
- **Cardio (Stages 4+ only):** zone-2 / conversational pace, **member picks the modality** (treadmill, bike, rower, incline walk). Rendered as its own timed block *before* the lifting to build the "cardio-first" habit. Not part of the whitelist exercise list. **Stages 1–3 are home stages with no cardio block** (no home cardio equipment) — the circuits themselves supply the conditioning.
- **Functional moves** (walking lunges, prowler sled, farmer carries; battle ropes for men at Stages 5–6 only) unlock at the **final three stages (5–7)**. At **Stage 7 the men's track drops non-leg functional** (no battle ropes) and alternates leg-primary functional (sled / lunge / carry) with traditional leg work.
- **Timed → reps transition:** Stages 1–3 are timed circuits; Stage 4 keeps the 20-min structure but switches to sets × reps so the body learns rep-based lifting before volume climbs.
- **Equipment jump is now at Stage 4:** Stages 1–3 are home stages (none → minimal → minimal-but-longer); **Stage 4 is the first full-equipment stage**, so the gym-upgrade prompt / track choice happens entering Stage 4 (§4).

---

## 2. Starting-stage assessment (assess-into-a-stage)

New members are placed at a starting stage from **before/after photos + experience answer + injuries + age**, taking the **more conservative** of photo vs. stated experience. Everyone still climbs to Stage 7 over time.

| Start at | When the assessment shows… |
|---|---|
| **Stage 1** | Before photo reads **obese / severely deconditioned / elderly**, OR a reported **severe injury**, OR a true never-exerciser. (Dan's explicit ultra-beginner criteria.) |
| **Stage 2** | Overweight but mobile, sedentary beginner, minor limitations; comfortable at home with minimal gear. |
| **Stage 3** | Average or lightly-deconditioned but healthy; comfortable training at home; returning beginner+. *(Still minimal-equipment — the final home stage.)* |
| **Stage 4–5** | Intermediate with a real training base / advanced returning. |

- **Cap starting stage at 5** — even an advanced, lean user gets ~2 months of ramp before the 45- and 60-min peaks. *(Proposed; confirm.)*
- Injuries and free-text medical notes ("doctor said no jumping", "high blood pressure") are **hard constraints** that can pull the start stage down and remove movements regardless of assessed level.

---

## 3. Progression between stages

- **One stage per 4-week block.**
- At each block's end (existing check-in/regeneration endpoint): if the member logged **≥50%** of that block's workouts → **advance one stage by default**. If **<50%** → offer to **repeat the current stage** one more month (their choice; not forced up).
- Keep a manual "this was too hard" hold as a safety valve.
- Cap at Stage 7 (the shared finish line).

---

## 4. Two equipment tracks (kick in at Stage 4)

Stages 1–3 are home stages (none → minimal → minimal-but-longer). **On reaching Stage 4** — the first full-equipment stage — show a **congratulations + upgrade screen** that strongly encourages a gym membership or full home gym:

- **Confirms full equipment →** run the **full-equipment plan** (primary exercises) with **minimal-equipment substitutes** shown as the one-tap swap.
- **Declines →** run an **alternate minimal-equipment plan** (a longer/heavier continuation of the Stage 3 home style as the *primary* moves) with **no-equipment substitutes** as the swap.

**Every subsequent month** (entering Stages 5, 6, 7), re-show the upgrade encouragement in progressively stronger terms — but always let them **stay on the minimal track** if they decline.

Implementation: store `equipment_track` (`'full'` | `'minimal'`) on the program row, set at Stage 4, re-prompted at each block promotion until they upgrade.

**Equipment tiers get restructured** from `none / db / gym` to **`none / min / full`**:
- `none` — bodyweight (+ a towel, which everyone has).
- `min` — none **plus** kettlebell, push-up handles, ab wheel, yoga mat. **No dumbbells, no barbells.**
- `full` — everything: dumbbells, barbells (gated by stage), machines, cables, benches. (Old `db` exercises migrate into `full`.)

---

## 4-B. Men's & women's tracks

Every member is assigned a **sex track** at intake (single tap: "I'm training as Woman / Man"; fall back to before-photo inference if skipped). Both tracks are still **total-body every day** (upper + lower + abs) — the difference is *emphasis*, i.e. how the weekly and per-session volume is weighted.

- **Women's track — emphasize lower body, SUPER-emphasize glutes.**
  - More lower-body sets than upper each session; the glutes get a dedicated hip-hinge/thrust move **plus** a glute isolation move (kickback / abduction) at Stages 5–7.
  - Glute-biasing choices throughout: sumo/wide stance on squats, hip thrust as a staple, walking lunges, single-leg glute bridge, kickbacks, hip abduction.
  - Upper body is present but lighter — enough for balance and posture, not the focus.
- **Men's track — emphasize upper body, SUPER-emphasize deltoids, biceps, triceps.**
  - More upper-body sets than lower each session; delts/arms get dedicated isolation (lateral raise, rear-delt fly, curls, triceps extensions/pushdowns) at Stages 5–7.
  - Shoulder-biasing choices: overhead press, lateral raises, rear-delt work; direct arm work.
  - Lower body is present but lighter — leg press + a hamstring/glute move, not the focus.

Emphasis only kicks in where the format allows it: Stages 1–2 (5–10 min circuits) stay near-identical across sexes apart from stance/move-slot tweaks; the divergence grows as time budgets open up (Stages 5–7). The exact per-stage prescriptions are in **§7**.

## 5. Global safety rules (hard-coded, override everything)

These are the non-negotiables Dan called out. They live in `TRAINER_SYSTEM_PROMPT` and are enforced by the whitelist + `sanitizeProgram`.

1. **No barbell or dumbbell deadlifts, ever.** The **kettlebell deadlift** (and kettlebell swing) is the *only* loaded hip-hinge from the floor. Hamstrings otherwise come from the **machine leg curl** (full track) and **glute bridges / hip thrusts** (both tracks).
   - ⚠️ **Open item:** the current library's `db-rdl` ("Dumbbell Hip Hinge") is a dumbbell deadlift variant. **Proposal: drop it from programming** in favor of `kb-deadlift` + `leg-curl` + glute work. Confirm.
2. **No flat or incline bench press, ever** (barbell). Chest is **fly-dominant**; "pushing" appears only in the later stages and only via **safer pushes** — machine chest press, dumbbell floor/neutral press, and the push-up family.
   - ⚠️ **Open item:** keep or drop the flat **`db-bench-press`**? Proposal: **drop the flat DB bench**, keep `machine-chest-press` + `db-floor-press` + push-ups as the "pushing" component so nothing mimics a flat/incline bench. Confirm.
3. **Barbell back squat only at Stages 6–7.** Leg squat hierarchy at the top:
   - **Primary: leg press.**
   - **Backup 1: safety-bar back squat.**
   - **Backup 2 (tertiary): barbell back squat.**
   Below Stage 6 the squat pattern is leg press / goblet squat / bodyweight squat only.
4. **Chest = mostly flies** (pec deck, cable fly, DB fly), with a little pushing added in the later stages only.
5. Injured areas are strictly unloaded; joint-friendly picks preferred.

---

## 6. Exercise-library changes (`exercises.js`)

### Add
| id | name | tier | cat | notes |
|---|---|---|---|---|
| `towel-row` | Towel Row (self-resisted) | none | pull | **Stage 1 flagship.** Hold a towel at max tension, arms extended in a slight squat, row to chest slowly. |
| `chair-squat` | Chair Sit-to-Stand | none | legs | Ultra-beginner squat regression (stand up from a chair). |
| `kb-deadlift` | Kettlebell Deadlift | min | legs | The **only** floor deadlift allowed. |
| `kb-swing` | Kettlebell Swing | min | conditioning | Hip-hinge power; hamstrings/glutes. |
| `kb-goblet-squat` | Kettlebell Goblet Squat | min | legs | Minimal-track squat primary. |
| `kb-row` | Kettlebell Row | min | pull | Minimal-track back primary. |
| `kb-press` | Kettlebell Overhead Press | min | push | Optional shoulder move (later minimal stages). |
| `deficit-pushup` | Deep Push-Up (on handles) | min | push | Push-up handles for extra ROM. |
| `safety-bar-squat` | Safety-Bar Back Squat | full | legs | **Stage 6–7 backup-1** loaded squat. |
| `bb-back-squat` | Barbell Back Squat | full | legs | **Re-add, Stage 6–7 tertiary only.** |
| `battle-ropes` | Battle Ropes | full | conditioning | Functional, Stage 5–7. |
| `sled-push` | Prowler Sled Push | full | conditioning | Functional, Stage 5–7. |
| `cable-glute-kickback` | Cable Glute Kickback | full | legs | **Women's track glute isolation**, Stage 5–7. |
| `hip-abduction` | Hip Abduction (machine/band) | full | legs | **Women's track glute (medius) isolation**, Stage 5–7. Band version also works on the minimal track. |

**Isolation moves already in the library** used for the Stage 5–7 emphasis work: `db-lateral-raise`, `db-rear-delt-fly` / `machine-rear-delt-fly` (delts), `db-curl` / `db-hammer-curl` / `ez-bar-curl` (biceps), `db-tricep-extension` / `db-kickback` / `cable-tricep-pushdown` (triceps), `leg-extension` / `leg-curl` / `calf-raise` (legs). These stay **excluded below Stage 5** (compound-only until then).

### Move / re-tier
- `ab-wheel-rollout`: `gym` → **`min`** (an ab wheel is on the ≤$200 list).
- All existing `db` exercises → **`full`** tier (dumbbells are full-equipment now, not minimal).

### Remove from programming (pending confirm — see §5)
- `db-rdl` (dumbbell hip hinge) and `db-bench-press` (flat DB bench). Keep the ids resolvable in `EXERCISE_BY_ID` for old stored programs, but exclude from selection.

### ⚠️ Minimal-track chest gap
With only KB / handles / ab wheel / mat, there is **no fly tool** on the minimal track — chest becomes push-up-dominant, which conflicts with "chest = mostly flies." Options: (a) accept push-up-dominant chest on the minimal track, or (b) add a **resistance band (~$15)** to the minimal kit to enable band flies. **Dan to decide.**

---

## 7. Full workouts per stage — women's & men's tracks

**The complete day-by-day programming is in [TRAINER_V3_WORKOUTS.md](TRAINER_V3_WORKOUTS.md)** — all **7 unique days × 7 stages × women/men = 98 workouts**, plus the minimal-track substitution map. That file is the single source of truth for the actual sessions; this handoff covers the system (ladder, assessment, tracks, safety, schema).

Key programming rules reflected there:
- **No exercise repeats two days in a row** from Stage 3 up (movements alternate within their bucket).
- **Chest sequencing:** Stages 3–4 use compound pushes (machine chest press / push-ups — never a barbell bench); Stages 5–7 go **fly-dominant** (cable fly / pec deck) with a little pressing.
- **Isolation only at Stages 5–7** (curls, triceps, lateral raises, rear-delt flies, glute kickbacks/abduction, calf raises). Stages 1–4 are compound-only; emphasis there comes from move *selection*.
- **Men's Stages 6–7:** one pull/day alternating vertical & horizontal; a shoulder move every day alternating compound (military/DB press) & isolation (side lateral / rear delt). **Stage 7 men** alternate leg-primary functional (sled / lunge / carry) with traditional leg work and drop non-leg functional (no battle ropes); chest trimmed to one move/day (press or fly) to make room for shoulders.
- **Women** lean lower-body/glutes throughout (hip thrust staple, kickback + abduction isolation at 5–7); **men** lean upper-body/delts+arms.

---

## 8. Server / schema / UX changes

**Server (`server.js`):**
- Replace `PHASES` (6) → `STAGES` (7): `{ minutes, cardioMin, liftMin, mode: 'timed'|'reps', equipFloor: 'none'|'min'|'full', functional: bool, label }`.
- `clampPhase` → `clampStage` (1–7); `EXPERIENCE_START_PHASE` → start-stage rubric (cap 5).
- `assessment` schema: `assigned_stage` (1–7), `starting_stage`, `equipment_track`, `sex_track`.
- Add `equipment_track` and `sex_track` to the `programs` row; `equipment_track` set at **Stage 4** (first full-equipment stage) and re-prompted on promotion.
- Progression endpoint: ≥50% logged → +1 stage; <50% → offer hold. Cap 7.
- Rewrite `TRAINER_SYSTEM_PROMPT`: new ladder table, timed-vs-reps rule, cardio-block rule, two-track rule, the §5 safety rules, the **sex-emphasis rules (§4-B)**, and the **isolation-only-at-Stages-5–7** rule (Stages 1–4 compound-only).
- Intake: re-add a **sex** question ("training as Woman / Man"), cut in v2 — it now drives the sex track. Fall back to before-photo inference if skipped.
- `exercisesForEquipment`: new `none/min/full` tiers; Stages 1–3 use `none`/`min`; on the minimal track at Stage 4+, feed the `min` pool as primary with `none` swaps.
- Enforce **no same exercise on consecutive days** in `sanitizeProgram` (or the prompt) from Stage 3 up.

**UI (`index.html`):**
- **Stage 4 upgrade screen** (congrats + strong gym encouragement → full vs. minimal track choice); monthly re-nudge for minimal-track members.
- **Timer UI** for Stages 1–3 circuits (guided work/rest intervals); sets × reps view for Stages 4–7.
- Assessment reveal ("Here's what we saw → you're starting at Stage X").
- Cardio-block card (member picks modality) rendered before the lifting at **Stages 4+** (Stages 1–3 have no cardio block).

---

## 9. Open items for Dan (confirm before build)

1. Start-stage **cap at 5** for advanced users? (§2)
2. **Drop `db-rdl`** (dumbbell hip hinge) in favor of KB deadlift + leg curl? (§5.1)
3. **Drop flat `db-bench-press`**; keep machine press + floor press + push-ups as the only "pushing"? (§5.2)
4. **Minimal-track chest:** accept push-up-dominant, or add a ~$15 **resistance band** to the minimal kit for band flies? (§6)
5. Anything wrong in the Stage table (§1) durations / cardio splits?

## Execution order (after sign-off)
1. `exercises.js`: new tiers `none/min/full`, add/move/remove per §6, fix `swap:` targets.
2. `server.js`: `STAGES`, assessment rubric, two-track logic, progression 50% rule, rewritten prompt.
3. Intake: fold equipment into the track logic; keep the 5-screen photo-first flow.
4. UI: upgrade screen, timer mode, cardio block, assessment reveal.
5. SVG animations for the new moves (last; matches existing style work).
Test UI locally with dummy keys; test Claude endpoints on prod. Commit + push per step (authorized).
