# Handoff: Ab-visibility anchor ladder + the male Gemini magnitude problem

**Date:** 2026-07-29
**Project:** Abs By AI
**Business goal this serves:** Technical excellence → profitability. The abs ARE the product; Dan's round-5 labels put every remaining complaint on that one axis, and 5 of 6 male rows produced no acceptable image at all.

## Objective

Two related changes, in one pass, validated against labels we already own before anything ships.

1. **Give ab visibility a graded anchor ladder, the way body fat already has one.** Today `SYSTEM_PROMPT` grades body fat across four tiers with precise numbers, but ab visibility has no table at all — and **male Subtle and male Ripped ask for literally the same abs.** Dan's ask, in his words, is to "dial in precisely the degree of change we want on the abs." That is a *calibration* gap, not a missing-words gap.
2. **Test the hypothesis that concrete visual ab targets get compliance where abstract body-fat percentages get hedging.** This is the genuinely unexplored route to fixing male under-change, and it is the strongest version of Dan's idea.

Then re-run `bakeoff/round5-prompt-ab/` and compare against `out/labels.json`. Full re-test is **~$1.50 and ~10 minutes**. Nothing ships on a guess.

## Current State

**Round 5 is complete and its evidence is on disk** (commits `22f2288`, `859f94d`). See `AI_COORDINATION.md` → "Condensed-vs-full prompt A/B" for the full record. What matters here:

- **Dan's 18 blind labels:** `bakeoff/round5-prompt-ab/out/labels.json`. Permanent regression set, same status as `round1/labels.json`.
- **Working harness:** `bakeoff/round5-prompt-ab/{cases.js,build-prompts.js,run.js,build-gallery.js,decode.js}`. 36 images cost $1.42. Cached cells never re-spend. `SET=1` runs Gemini only.
- **Prompt-variant question is CLOSED:** full vs condensed tied 3–3, p=1.000, and the recommendation was **ship nothing**. Do not reopen it. In particular do not reopen it on the "one prompt to maintain" premise — `condenseForKontext` is a *transform* of the full prompt, so a condensed-everywhere world still assembles and maintains the full marker-scoped prompt. Nothing would be deleted.

**The male failure, precisely:**

| Male Gemini row | Dan's verdict | What the prompt actually asked for |
|---|---|---|
| lean dramatic + max | **both rejected**, "not enough change" | `[[MUSCLE_PRIMARY]]` — the **most** ab-detailed text in the entire system |
| heavier dramatic + max | **both rejected**, "not enough change" | full 8–10% + "peak condition" + "complete physique overhaul" |
| moderate max | **both rejected**, "not enough change" | `[[MUSCLE_SECOND]]` |
| moderate dramatic | picked full — but still tagged "not enough change" + "not enough ab definition" | `[[MUSCLE_SECOND]]` |

Gemini **under-changed 19 of its 24** candidates. FLUX **over-changed 8 of its 12** (`too muscular` / `too much change`). The two male legs fail in exact opposite directions — the mirror of the known female pattern (Gemini under / Seedream over), now confirmed for men. Dan's ideal sits between them. Female Gemini was healthy by contrast: 5 of 6 rows produced a pick.

**Where ab language stands today** (`public/index.html`, `SYSTEM_PROMPT` starts line 3135):

- `BODY-FAT ANCHOR TABLE` (line ~3167): 4 graded tiers × 2 sexes, precise ranges, plus floors. **This is the mechanism that works.**
- `MUSCULARITY ANCHOR TABLE` (`[[MUSCLE_TABLE]]`, ~3171): 4 graded tiers, +2/+4/+6/+8 lb.
- **Ab visibility: no table.** Prose only, scattered across markers:
  - `[[MUSCLE_PRIMARY]]` (~3154, male fit/very_lean): maximal ab detail — "fully visible, sharply cut SIX-PACK with all six abdominal blocks separated by crisp shadow lines, a sharp vertical midline, defined obliques, visible serratus, a tight waist, and a clear V-cut." **Identical text at dramatic and max** — only the pounds number changes.
  - `[[MUSCLE_SECOND]]` (~3177, male moderate at dramatic/max): mass-focused, **almost no ab specificity**.
  - Heavier males: **no muscle marker at all.**
  - `[[FEM_RIPPED]]` (~3155): "at least twice the visible definition… clear separation between each upper-ab block."
  - `[[FEM_SUBTLE]]` (~3156): "defined feminine upper-ab outline, a clear vertical midline."
  - So **females already have a crude 2-rung ab ladder; males have exactly one rung for both tiers.**
- Marker stripping: `muscleAxisPlan()` + the `MARKERS` map at ~3282–3312. `goalSystemPrompt()` does the removal.

## Key Decisions Already Made

- **Ground truth is Dan's blind labels**, not the judge and not Claude's eyeball. `out/labels.json` is the regression set; the judge may be run as a secondary signal but does not decide.
- **The ab ladder REPLACES vague ab prose — it does not add to it.** Net prompt length must not grow. Two independent reasons below in Lessons.
- **The ladder must be `[[MARKER]]`-scoped and stripped in `muscleAxisPlan()`.** Prose-only conditionals are unreliable — see Lessons; it failed again tonight.
- **Ab language belongs in the opening TRANSFORMATION DIRECTIVE paragraph.** That is the only part of the prompt with demonstrated effect on Dan's preference (round 5: dropping 70–85% of the text changed nothing).
- **Do not undo `14b4790` (the muscle-anchor halving).** The 33 "too muscular" complaints in round 1 were about over-change, and FLUX still over-changes men 8/12. This is **not** a global magnitude increase — it is leaner and more sharply defined *without added mass*, the axis Dan keeps naming.
- **Do not lower the body-fat floors** (male 8%, female 13%). A3.1 established that a more extreme number produces *hedging*, not compliance. The whole point of the ab ladder is to specify the visual result instead of pushing the number.
- **Female Subtle stays as retuned** (`d948f93`). Female Gemini is currently healthy; do not "fix" it.
- **Model routing is settled** (female = Seedream, male = FLUX). Not in scope.

## Detailed Plan

### Step 1 — Design the ab-visibility ladder (no code yet)

Write a graded scale of ab *appearance*, not of body-fat numbers. Suggested rungs, to be refined:

| Rung | Description |
|---|---|
| 0 | Flat, soft, no visible separation |
| 1 | Tighter midsection, faint upper-ab outline, visible vertical midline |
| 2 | Top two ab blocks clearly separated, defined midline, waist visibly tapered |
| 3 | Full four-block definition with crisp separation lines, oblique lines framing the waist |
| 4 | Full six-pack, deep shadowed separation, visible serratus, clear V-cut into the waistband |

Then assign **one rung per sex × tier × starting condition**, as a table in the same style and location as `BODY-FAT ANCHOR TABLE`. Constraints from the evidence:

- Male Subtle and male Ripped **must land on different rungs** — this is the concrete defect.
- Female Subtle ≈ rung 1–2 and female Ripped ≈ rung 3 (approximately what `[[FEM_SUBTLE]]`/`[[FEM_RIPPED]]` already say in prose — the ladder should *encode* the retune Dan already approved, not change it).
- Heavier starts cap lower than lean starts at the same tier (A3.1 realism), but **must still differ between the two tiers**.

**OPEN — Dan's call, ask before shipping:** the exact rung for **male Ripped on a heavier start**. Tonight the prompt asked for peak and Gemini refused; a lower, concrete rung might get real compliance where "8–10% / peak condition" got a no-op. But it also risks formally promising less. Show Dan a side-by-side before deciding.

### Step 2 — Implement

In `public/index.html`:
1. Add `AB-DEFINITION ANCHOR TABLE` immediately after `BODY-FAT ANCHOR TABLE` (~line 3169), wrapped in a new `[[AB_TABLE_START]]`/`[[AB_TABLE_END]]` marker pair.
2. Add per-tier ab directive blocks with new markers (e.g. `[[AB_MALE_SUBTLE]]`, `[[AB_MALE_RIPPED]]`), and **delete the now-redundant ab prose** from `[[MUSCLE_PRIMARY]]` so the six-pack description exists in exactly one place. `[[MUSCLE_SECOND]]` gains an ab rung it currently lacks.
3. Register every new marker in the `MARKERS` map (~3282) and add the selection logic to `muscleAxisPlan()`.
4. Instruct the assembler to put the ab rung **in the opening directive paragraph**, next to the body-fat target.

### Step 3 — Assert before spending a cent on images

Run a marker/assembly harness over `goalSystemPrompt()` across **all** sex × condition × intensity combinations (the pattern exists — 112 assertions in `d948f93`, 662 in `14b4790`). Assert:
- **Zero `[[` marker leakage** in any combination.
- Male Subtle and male Ripped prompts contain **different** ab rungs.
- Female prompts are **byte-identical to HEAD except** for ab-ladder text (female Gemini is currently healthy — do not regress it).
- No prompt exceeds the `/api/generate-prompt` ceiling and none is truncated (the `8a7c4a4` bug — watch for `PROMPT_TRUNCATED`).
- Net `SYSTEM_PROMPT` length has **not grown materially**.

### Step 4 — Re-run the harness and compare to Dan's labels

```bash
cd bakeoff/round5-prompt-ab
rm -rf prompts out/*.jpg out/*.json          # keep out/labels.json and out/key.json!
node build-prompts.js
set -a && . ../.env && set +a && SET=1 node run.js
```
Then build a **new** blind gallery comparing **old prompt vs new prompt**, same model per row — the `round4-female-retune/build-gallery.js` shape, which is exactly this comparison. Keep the invariants: **pinned letters** for rows already in `key.json`, and an **asserted** per-set slot-A balance.

The bar to beat, from `out/labels.json`: **male Gemini rows where Dan rejected BOTH candidates must drop below 5 of 6.** That is the headline number. Secondary: fewer `not enough ab definition` tags, and no new `looks fake`.

### Step 5 — Ship only if Dan's labels improve

Usual bar: commit, push, confirm the Railway deploy, verify on absbyai.com with real generations, then check the dashboard task off. **No native retest needed** — prompt text only, touching no trigger row in the cross-platform table.

### Step 6 (cheap, optional) — the deferred judge signal

Run the shipped judge over the round-5 images and score agreement with `out/labels.json`. Near-$0 (harness + disk cache exist). Informative precisely because Dan rejected both candidates in 6 rows — it shows how the judge behaves when neither option is acceptable.

## Things to Avoid / Lessons Learned

- **"More ab language" is provably NOT the lever. This is the single most important thing in this document.** Three independent lines of evidence:
  1. `[[MUSCLE_PRIMARY]]` (male lean) already contains the most detailed ab description in the entire system — six-pack, crisp shadow lines, midline, obliques, serratus, V-cut, "no softness anywhere" — and Dan **rejected both candidates at both tiers**.
  2. Ab-word count in the effective paragraph has **zero correlation** with Dan's satisfaction: rows with no ab language were both-rejected 2/4; rows with ab language, 4/8. Identical.
  3. Round 5 showed dropping 70–85% of the prompt changed nothing. The model does not read more text as more instruction.
  The lever is **grading and placement**, not volume.
- **Regional ab prose was tried once and reverted in seven minutes** (`a255f41` → `323135e`, 2026-07-21): a lower-belly/V-cut directive made Average + Peak males *worse*. Recorded lesson: heavy regional detail crowds out whole-body change. **But that test was CONFOUNDED** — it also narrowed body fat to 8–9%, independently known to cause hedging. So the idea is not definitively refuted; it has never been tested cleanly. Test it cleanly this time: **ab ladder only, body-fat anchors untouched.**
- **Prose-only scoping is unreliable — this is now the FOURTH occurrence, and one is fresh evidence from tonight.** The `CALIBRATION RULE` (~3182) says heavier + dramatic/max should downgrade the body-fat target one step and add mid-journey language. In the round-5 `heavier-male__max` prompt the assembler **ignored it completely** — the prompt asked for the full 8–10%, "peak condition," "complete physique overhaul," with no mid-journey wording anywhere. Two consequences: (a) every new ab rule must be `[[MARKER]]`-scoped, never prose; (b) **heavier-male under-change is the A3.1 model ceiling, not a weak prompt** — the prompt asked for everything and Gemini refused. Do not "fix" heavier male by pushing the prompt harder; that lever is exhausted.
- **Retracting an instruction does not work — remove it.** From `d948f93`: a positive instruction plus a later "…but not in case X" is unreliable; the assembler obeys the earlier positive one. Delete, don't caveat.
- **Do not lower body-fat floors and do not raise muscle anchors.** Both are settled and both would recreate known failures.
- **No `deviceId` on any harness call, ever** — otherwise every generation commits `credits-data.json` and redeploys prod.
- **Seedream hard-rejects prompts >4000 chars (422).** Full prompts already run 4.0–6.5k, so the female challenger leg is condensed-only by construction. If the ab ladder grows the condensed output, re-assert the ceiling (`build-prompts.js` does this automatically).
- Gemini's female safety blocks are non-deterministic; don't over-conclude from a single blocked cell.
- Round-3/5 female photos are real private individuals and **the repo is public** — `bakeoff/round5-prompt-ab/.gitignore` keeps `photos/`, `out/*.jpg`, `out/thumbs/` and `gallery.html` out of git. Keep it that way.

## Relevant Files & Locations

- `public/index.html` — `SYSTEM_PROMPT` (~3135), `BODY-FAT ANCHOR TABLE` (~3167), `[[MUSCLE_TABLE]]` (~3171), `[[MUSCLE_PRIMARY]]` (~3154), `[[MUSCLE_SECOND]]` (~3177), `CALIBRATION RULE` (~3182), `MARKERS` map (~3282–3312), `muscleAxisPlan()`, `goalSystemPrompt()`
- `server.js` — `condenseForKontext` (~2578), Gemini safety retry preamble (~2601), `callSeedream`, `callFluxViaReplicate`
- `bakeoff/round5-prompt-ab/` — harness; **`out/labels.json` is the regression set, `out/key.json` pins gallery letters — do not delete either**
- `bakeoff/round4-female-retune/build-gallery.js` — the correct old-vs-new gallery shape to copy
- `bakeoff/prompts.js` — extracts real prompt assembly from `index.html`; `condense()` is byte-identical to production
- `bakeoff/.env` — `GEMINI_API_KEY`, `REPLICATE_API_TOKEN` (0600, gitignored). Replicate throttles to 6 req/min below a $20 balance.
- Round-5 gallery (all 18 rows labelled): https://claude.ai/code/artifact/26772cd0-d79d-4875-8b12-f24d7099da7a

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Opus, extended thinking. This is prompt-system design with four recorded scoping failures, a confounded prior experiment, and a live model ceiling to reason around — being wrong here is expensive to unwind and hard to detect. |
| **If Claude usage is high / approaching a limit** | Claude Sonnet 5, standard thinking — still Claude. Do not send this to Codex. |

Task-type override: this edits the core transformation prompt and the Anthropic-assembled prompt path — **always Claude**, regardless of usage.

## Starter Prompt for the Next Task

> Read `handoff-20260729-ab-visibility-anchor-ladder.md` in the Abs By AI project root, then `AI_COORDINATION.md` (the "Condensed-vs-full prompt A/B" entry has the evidence base). Task: add a graded AB-DEFINITION ANCHOR TABLE to `SYSTEM_PROMPT` in `public/index.html`, mirroring how `BODY-FAT ANCHOR TABLE` already grades four tiers — one ab-visibility rung per sex × tier × starting condition, `[[MARKER]]`-scoped and stripped in `muscleAxisPlan()`, placed in the opening transformation directive, and **replacing** the vague ab prose in `[[MUSCLE_PRIMARY]]` rather than adding to it (net prompt length must not grow). The concrete defect to fix first: male Subtle and male Ripped currently ask for identical abs. Do not touch the body-fat anchors, the floors, or the muscle-mass anchors — read the Lessons section before writing anything, especially the note that "more ab language" is ruled out by three independent lines of evidence. First action: write the rung scale and the per-tier assignment table, and show it to Dan for approval before editing any code — the male-Ripped-on-a-heavier-start rung is flagged OPEN and is his call.
