# Handoff: Restore male muscle magnitude on the Gemini path (the 14b4790 partial revert)

**Date:** 2026-08-08
**Project:** Abs By AI
**Business goal this serves:** Technical excellence → adoption. The transformation image IS the product, men are the marketing target, and the male Gemini leg currently under-changes so reliably that Dan rejected both candidates in 6 of 6 blind rows on 2026-08-07.

## Objective

Restore the male muscle-magnitude language that commit `14b4790` (2026-07-25) deleted from the generation prompt — the halved anchor table and the "visibly BIGGER" verbs — WITHOUT undoing the two parts of that commit that worked (the no-tan rule and the Kino/no-bodybuilder ceiling). Then blind-test the restored prompt against the already-labelled current-production baseline (6 male Gemini rows + 6 male FLUX control rows, ~$0.47), publish a blind gallery for Dan, and ship or revert based on his labels against a pre-registered bar. If this fails, the fallback is the model swap in `Handoffs/handoff-20260807-male-gemini-model-swap.md` — do NOT start that swap from this task.

## Current State

- **Production prompt** (`public/index.html`) is the post-`14b4790`, post-ladder-revert (`feb94e0`) state. Male anchors: `subtle ≈ +2 lb, moderate ≈ +4 lb, dramatic ≈ +6 lb, max ≈ +8 lb`, expressed as "slightly fuller / slightly rounder / slightly wider". Verified locations (line numbers as of 2026-08-08):
  - `public/index.html:3640` — `[[MUSCLE_PRIMARY_START]]` block (SHREDDED-ATHLETE RULE, lean/fit males)
  - `public/index.html:3658-3660` — MUSCULARITY ANCHOR TABLE + the "deliberately small / if in doubt add LESS" expression paragraph
  - `public/index.html:3665` — `[[MUSCLE_SECONDARY]]` block (moderate males: fat loss leads, modest muscle underneath)
  - `public/index.html:3682` — `[[MUSCLE_BULLET_START]]` male bullet
  - `public/index.html:3769` / `:3816` / `:3853` — marker map, `muscleAxisPlan()`, and the `goalSystemPrompt()` assembly that strips markers deterministically
- **The evidence that this restore is the right lever** is recorded in `AI_COORDINATION.md` → "WE CAUSED THE MALE GEMINI REGRESSION OURSELVES" (measured 2026-08-07): Gemini contributed ZERO of the 33 `too muscular` tags that justified the retune, and the most `not enough change` tags of any model; Dan's `not enough change` rate on male Gemini went 75% → 100% across the retune; a same-day prompt-era A/B holding the model constant showed the pre-retune prompt produces a visibly bigger, V-tapered result on the lean case.
- **The old (pre-retune) text to restore is in the diff of `14b4790`** — run `git show 14b4790 -- public/index.html` and read the `-` lines. Do not reconstruct it from memory.
- **Free baseline:** current-production-prompt male images are already generated AND Dan-labelled: `bakeoff/round5-prompt-ab/out/` + `labels.json` and `bakeoff/round6-ab-ladder/out/` + `labels.json` (round 6's "old" arm = the current production prompt). Only the NEW arm needs generating.
- **Harness to copy:** `bakeoff/round6-ab-ladder/` (`cases.js` / `build-prompts.js` / `run.js` / `build-gallery.js`, own `.gitignore` keeping jpgs + gallery out of the public repo).
- **Dashboard:** a Key task for this handoff exists on the Victory Dashboard (`money::Execute handoff: Restore male Gemini muscle magnitude + blind test`). Check it off per AI_COORDINATION Rule 9 when fully executed (a measured "ship nothing / revert" outcome counts as executed).

## Key Decisions Already Made

- **Do NOT revert `14b4790` wholesale.** It also removed the positive tan instruction, and that fix worked (round 1: 3 `too tan` on Gemini male; every round since: zero, `skin tone right` 6/6). Restore muscle magnitude ONLY; keep the no-tan rule and the "NEVER a bodybuilder: no inflated chest, no boulder shoulders, no blown-up arms, no comic-book mass" ceiling sentence.
- **Marker-scoped or nothing.** All male-magnitude text lives inside the existing `[[MUSCLE_*]]` blocks stripped by `muscleAxisPlan()`. Prose-only scoping has leaked FOUR times in this project's history. Do not add any prose conditional.
- **Do NOT restore the "Placed side by side with the input, the output must read as…" sentence** from the old MUSCLE_PRIMARY text — it was separately removed because image models read it as an instruction to render a before/after diptych.
- **Do NOT restore the old shoulder/V-taper universal bullet** ("Shoulder caps visibly rounder… WIDER"). It sat OUTSIDE the markers and pushed size onto heavier males it was never scoped to; the current tighter-waist version stays.
- **Female prompts must assemble byte-identical to HEAD.** Assert it programmatically (the round-6 build did this across all 16 female combos); a diff is a bug.
- **This is prompt-text only.** No `server.js` change, no client logic change, no judge change.
- **A third candidate model is forbidden** (judge is 2-way-validated only; N-way top-1 is 42.9%). This task never touches model routing.
- **No `deviceId` on any test call, ever** — it spends real credits and triggers a data-file commit → Railway redeploy.
- **Only two intensities are user-pickable:** Subtle = internal `dramatic`, Ripped = internal `max`. The restored anchors that actually fire in production are the dramatic/max ones (+12/+15 lb).
- **Include a FLUX control set.** The magnitude sentence lands in the directive paragraph, which survives `condenseForKontext`, so the FLUX leg (which already over-changes men 8/12) receives it too. Round 6 ran the same control for the same reason. If the restore fixes Gemini but pushes FLUX further into `too muscular`, that is a real cost the labels must capture.

## Detailed Plan

### Step 1 — The prompt edit (`public/index.html`)

Read the old text first: `git show 14b4790 -- public/index.html` (the `-` lines are what you are restoring). Then, keeping everything inside the existing markers:

1. **MUSCULARITY ANCHOR TABLE** (~line 3658): `+2/+4/+6/+8` → **`+5/+8/+12/+15 lb`**. Replace the "These numbers are deliberately small… If in doubt, add LESS" paragraph with the old expression line: "Express added mass through the structures that read instantly in a photograph: a fuller, squarer chest with a defined lower-pec line; visibly larger, rounder shoulder caps; wider lats flaring out from the armpits; a thicker upper back; noticeably thicker arms with a fuller bicep belly and a clear tricep sweep."
2. **`[[MUSCLE_PRIMARY]]`** (~line 3640): restore the old "visibly BIGGER and more muscular… fuller, squarer chest, distinctly larger and rounder shoulder caps, wider lats creating an obvious V-taper, a thicker upper back, and noticeably thicker arms" framing, KEEPING (a) the full six-pack requirement sentence, (b) the trailing "but he must still read as a lean natural athlete, NEVER a bodybuilder: no inflated chest, no boulder shoulders, no blown-up arms, no comic-book mass", and (c) the Kino closing sentence. OMIT the "Placed side by side" sentence.
3. **`[[MUSCLE_SECONDARY]]`** (~line 3665, moderate males): restore "visibly more muscular and more developed… distinctly larger and rounder shoulder caps, wider lats creating an obvious V-taper, and noticeably thicker arms", keeping the trailing no-bodybuilder clause the current text carries.
4. **`[[MUSCLE_BULLET]]`** (~line 3682): restore "Added muscle SIZE per the MUSCULARITY ANCHOR TABLE — fuller chest, larger/rounder shoulder caps, wider lats, thicker upper back, thicker arms", keeping the six-pack as co-headline.

### Step 2 — Verify the assembly before any spend

Run a combo harness over the real `goalSystemPrompt()` (round 6's build script is the template): all 32 gender/condition/intensity combos — zero `[[` marker leakage anywhere; **all 16 female combos byte-identical to HEAD**; the magnitude language present only in the intended male combos; heavier-male combos unchanged (they carry no mass markers); `node --check` clean on every inline script block.

### Step 3 — Commit, push, deploy, live-verify

Per the delivery rules: commit, push to `main`, wait ~60s for Railway, then poll on a **content marker** (e.g. the `+15 lb` anchor string in the served `index.html`), never the status code (SPA fallback serves 200 for everything). Then drive prod `/api/generate-prompt` for the male combos and assert the magnitude sentence is present in the full prompt AND survives `condenseForKontext` (check the condensed output too). No native retest trigger row is touched (prompt text only) — say so in the report.

### Step 4 — Round-7 harness

1. `cp -r bakeoff/round6-ab-ladder bakeoff/round7-magnitude-restore` (keep its `.gitignore`).
2. **Fix the caching bug first:** `run.js:36` skips any cell whose `.json` exists, including failed `{ok:false}` records. Make it treat `ok:false` as not-cached (delete/regenerate). This bit round 6 during the Gemini outage.
3. Cases: 3 male photos × 2 tiers = 6 cases (`lean-male`, `moderate-male`, `heavier-male` × dramatic/max) — already in `cases.js`.
4. Arms: **set 1 = Gemini full prompt (primary, 6 images)**, **set 2 = FLUX condensed prompt (control, 6 images)**. NEW arm only — the OLD arm reuses the round-6 "old"/round-5 labelled images at $0.
5. Build prompts via prod `/api/generate-prompt` post-deploy (so the test exercises exactly what production sends) and assert per-case that the magnitude language is present in full AND condensed variants.
6. **Estimated spend: ~$0.47** (12 images). State it before running. Zero deviceId.

### Step 5 — Blind gallery → Dan

`node build-gallery.js`, publish as an Artifact. Non-negotiable invariants the round-6 builder already enforces — keep all of them:
- Slot-A balance asserted per set (3/3 in each).
- Letters PINNED via `out/key.json`; if adding to a published gallery, verify existing pins held and diff the published HTML.
- Blinding check: zero `key.json` entries in the built HTML; no candidate block leaks "old/new" wording.
- Exercise the page in a real browser (persistence, mutual exclusion, tag chips, no console errors, no horizontal overflow) before sending Dan the link.

### Step 6 — Pre-registered bar (write this into the gallery session BEFORE any image is generated)

- **Primary (Gemini set): ship the restore only if both-rejected rows fall below 5 of 6 AND new beats old on decisive rows.** (Round 6 baseline: 6/6 both-rejected, 0 decisive.)
- **Watch tag: `too muscular`.** If Dan tags ≥3 new-arm Gemini rows `too muscular`, the restore overshot — the next dial is the anchor numbers (try the midpoint +4/+6/+9/+12), not new prose.
- **FLUX control: a regression here (new-arm FLUX `too muscular`/`too much change` clearly above the old arm's 3/3) counts against shipping** — production sends the condensed prompt to FLUX, so the restore ships to both legs or neither.
- On failure: `git revert` the prompt commit, live-verify the revert, and hand off to the model-swap doc.

### Step 7 — Close out

Decode labels against `out/key.json`, record the verdict in `AI_COORDINATION.md` (including a "do not re-litigate" summary either way), check off the dashboard Key task (`money::Execute handoff: Restore male Gemini muscle magnitude + blind test` — Rule 9; a measured "revert" is a completed outcome), and reset/update the active-task section.

## Things to Avoid / Lessons Learned

- **Prose scoping leaks — four recorded incidents.** Marker blocks stripped in `muscleAxisPlan()` are the only accepted mechanism.
- **Retracting an instruction doesn't work; remove it.** Never leave "…but not for X" contradictions in the prompt.
- **Don't chase a single region.** The 2026-07-21 lower-belly experiment showed region-specific asks crowd out whole-body change. The restore is whole-frame magnitude, not new anatomical detail.
- **Deploy polling:** poll the served HTML for a content marker; `/health` and status codes stay green through everything, including provider-balance outages.
- **Gemini's male blocks are non-deterministic** and production retries with the `SAFE FITNESS EDIT` preamble — the harness already replicates this; keep it.
- **Artifact publish gotcha:** if the Artifact tool refuses with "this session hasn't viewed the latest version," WebFetch the live artifact, verify, and publish WITHOUT `force`.
- **`/api/todos` reads are eventually consistent** — re-check after a beat before concluding a write failed.
- **The repo is public.** Test photos and generated jpgs never get committed; the round harness `.gitignore` handles it — verify with `git check-ignore` before staging.

## Relevant Files & Locations

- `public/index.html` — SYSTEM_PROMPT, `[[MUSCLE_*]]` blocks (~3640–3690), marker map ~3769, `muscleAxisPlan()` ~3816, `goalSystemPrompt()` ~3853
- `git show 14b4790 -- public/index.html` — the exact old text to restore (`-` lines)
- `bakeoff/round6-ab-ladder/` — harness template (+ the `run.js:36` caching bug)
- `bakeoff/round5-prompt-ab/out/labels.json`, `bakeoff/round6-ab-ladder/out/labels.json` — the free, already-labelled baseline
- `AI_COORDINATION.md` — "WE CAUSED THE MALE GEMINI REGRESSION OURSELVES" (evidence), Rules 8/9 (dashboard), cross-platform retest rule
- `Handoffs/handoff-20260807-male-gemini-model-swap.md` — the fallback if this fails
- Env: `REPLICATE_API_TOKEN` (FLUX control arm), `GEMINI_API_KEY`-equivalent via the harness's existing key handling (read from Railway per prior rounds)
- Dashboard: `https://absbyai.com/api/todos`, `POST /api/task-checks` (id = `money::<exact text>`)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** The plan is fully specified (exact old text in a git diff, existing harness, pre-registered bar), so flagship reasoning isn't needed — but the marker-scoping and byte-equality assertions punish sloppiness, so don't go below Sonnet. |
| **If Claude usage is high / approaching a limit** | **Codex flagship, medium effort.** Routine-shaped execution against a written spec. Do NOT use a mini-tier model — the female byte-identity and blinding invariants are exactly where a small model cuts corners. |

Override note: this touches the generation prompt (brand-critical output quality), but the creative decisions are already made and the text to restore is literal — so the usual "prompt work stays on a big Claude" rule is satisfied by the spec itself. If the executor finds itself *writing new prompt language* rather than restoring the diffed text, stop and escalate.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260808-male-gemini-magnitude-restore.md` in the Abs By AI repo (`/Users/danielrose/Documents/Claude/Projects/Abs By AI`). Read that handoff and `AI_COORDINATION.md` first — the decisions there are settled; do not relitigate them.
>
> Task: restore the male muscle-magnitude language deleted by commit `14b4790` (anchors back to +5/+8/+12/+15 lb, "visibly BIGGER" verbs — read the exact text from `git show 14b4790 -- public/index.html`), keeping the no-tan rule and the no-bodybuilder ceiling, everything `[[MARKER]]`-scoped. Assert all 16 female combos assemble byte-identical to HEAD before deploying. Commit, push, live-verify on absbyai.com (poll a content marker, not the status code). Then copy `bakeoff/round6-ab-ladder/` to `bakeoff/round7-magnitude-restore/`, fix the `run.js` ok:false caching bug, and generate the NEW arm only: 6 male Gemini rows (full prompt) + 6 male FLUX rows (condensed) ≈ $0.47, no deviceId. The OLD arm reuses the already-labelled round-5/6 images at $0. Build the blind gallery with the round-6 invariants (slot-A balance, pinned letters, blinding check, real-browser test) and send Dan the link to label. The pre-registered bar and the ship/revert rule are in the handoff's Step 6. When fully executed (either verdict), record the outcome in `AI_COORDINATION.md` and check off the dashboard task `money::Execute handoff: Restore male Gemini muscle magnitude + blind test`.
