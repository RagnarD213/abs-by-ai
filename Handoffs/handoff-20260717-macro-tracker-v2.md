# Handoff: Macro Tracker v2 — Meal Prep, Multi-Photo, Uneaten Food

**Date:** 2026-07-17
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** App adoption (daily-use retention hook) + technical excellence (accuracy)

## Objective

Ship three upgrades to the existing photo-based macro tracker, as one batch since they all touch the same tracker UI and the same `/api/analyze-meal` pipeline:

1. **Meal prep meals** — user photographs a whole week's batch of identical meals (ideally the raw ingredients + packages), enters how many servings it divides into, and it's saved as a reusable card. Logging one later is a single tap: no photo, no AI call, no cost.
2. **Multiple photo angles** — a meal analysis (regular AND meal prep) can include up to 3 photos (overhead + side view, etc.) so the model can judge volume/depth better. This directly attacks the biggest error source (portion ambiguity).
3. **Uneaten food** — after logging a meal, the user can subtract what they didn't eat, two ways: (a) fast chips ("left ~¼", "left half", per-item "left the sauce") with instant client-side scaling and no AI cost, and (b) a leftover photo analyzed by a cheap Haiku call that estimates the remaining fraction of each line item. **Both options are in scope.**

A fourth item from the same planning session — the eval harness + calibration retune — is deliberately **not** in this handoff. It runs as its own task (Daniel weighs ~20 real meals first). Don't build it here, but don't do anything that blocks it either (keep the `raw` uncalibrated numbers in responses).

## Current State

The macro tracker is live on prod and works end-to-end (see `HANDOFF_macro_tracker.md` for the original build):

- **`POST /api/analyze-meal`** (server.js ~line 1605) — Sonnet 4.6 (`claude-sonnet-4-6`), raw fetch (no SDK — matches codebase style), structured outputs via `output_config.format` json_schema (`MEAL_SCHEMA` ~1492). Takes `{ photoBase64, photoMime, note, recentMeals, deviceId }`. Freemium gate: non-members get `FREE_MEAL_ANALYSES` (=3, ~line 105) tracked in `creditsStore.mealCounts`, then credits/membership required.
- **`POST /api/refine-meal`** (~line 1741) — Haiku 4.5, takes `{ analysis, answers[] }`, adjusts items after clarifying questions, free (no credit charge).
- **Pipeline guarantees:** `enforceMacroMath()` (~1555) recomputes calories from 4/4/9/7 (alcohol) macro math when the model's figure drifts >15%; `MEAL_CALIBRATION` multipliers (~1482) scale grams by context; responses carry `raw` (uncalibrated) for future calibration analysis.
- **Client (index.html, `macroSection`):** photo upload with an existing client-side downscale pipeline, note field, receipt card with per-item edit, clarify chips → refine call, Log Meal. Meal log lives in localStorage key `absbyai_logged_meals` (`[{date, loggedAt, name, items, totals}]`); daily totals recompute on load.
- **Account sync:** logged-in users sync meals via `GET/POST/DELETE /api/meals` (server.js ~2847) to a Postgres `meals` table.

Nothing from this handoff has been started. No branch, no code.

## Key Decisions Already Made

- **Meal prep photos should be of raw ingredients + packages, and the UI should say so** — labels beat guesses, and the pipeline already has a `label` source mode that trusts nutrition labels verbatim. A batch estimate built from labels ÷ 12 beats any plated-photo estimate.
- **Batch analysis costs one credit/free-use like a normal analysis; the one-tap logs afterward are free** — no AI call happens on tap.
- **Uneaten food ships both paths:** chips (client-only, instant, free) and leftover photo (Haiku, free like refine — charging twice for one meal feels bad).
- **Multi-photo applies to both regular meals and meal prep**, capped at 3 photos per analysis to bound token cost.
- **Multi-photo stays one API call, one credit** — images are the bulk of the tokens so cost rises modestly, but don't charge extra.
- **Don't touch `MEAL_CALIBRATION` values in this task** — the eval harness task will retune them from measured bias. (Daniel observes overestimation; the multipliers may be part of it, but changes should be measured, not guessed.)
- **Saved meal-prep meals live in localStorage first, with account sync for logged-in users** — same pattern as the meal log.

## Detailed Plan

### Part A — Multiple photos (do first; the other features build on it)

1. In `index.html` `macroSection`: after the first photo is chosen, show "＋ Add another angle (helps me judge portion size)" — allow up to 3 photos total, each run through the existing downscale pipeline. Show small thumbnails with remove buttons.
2. Change the client request to send `photos: [{ base64, mime }]` (order = order taken). Keep sending `photoBase64`/`photoMime` for nothing — instead, in `server.js`, accept **either** the new `photos` array **or** the legacy single `photoBase64` (backward compatibility for the iOS/Android wrappers pointing at prod).
3. In `/api/analyze-meal`, build the message content with one image block per photo, each preceded by a text label ("Photo 1", "Photo 2"…). Add to `MEAL_SYSTEM_PROMPT`: when multiple photos are provided they are the SAME meal from different angles — use overhead shots for contents and side shots for depth to estimate volume; itemize the meal once, not per photo.
4. While in the prompt, add the free accuracy wins decided in planning: (a) use the plate as a ruler (standard dinner plate ≈ 10.5 in / 27 cm, fork ≈ 7 in); (b) estimate each item's volume/weight FIRST, then convert to macros via standard densities — don't jump straight to calories.
5. Validate: reject >3 photos, enforce the same size limits per photo as today.

### Part B — Meal prep meals

6. **Server:** `/api/analyze-meal` accepts optional `{ mealPrep: true, servings: <2–20> }`. When set, append to the user text: this photo set shows an ENTIRE week's meal-prep batch (raw ingredients and/or packages); itemize and estimate nutrition for the WHOLE batch; read any visible nutrition labels verbatim. After `enforceMacroMath` + calibration, divide every item's grams/macros/calories and the totals by `servings` (round sensibly) and return both `batchTotals` and per-serving `totals`/`items`, plus `servings` echoed back. Charges the normal credit/free-use.
7. **Client — creating:** a "Meal Prep" entry point in `macroSection`. Flow: photos (multi-photo UI from Part A, with copy "Lay out everything for the week — include the packages, labels beat guesses") → "How many meals does this make?" number input → analyze → per-serving receipt card (with clarify/refine and per-item edit working as they do today) → "Save meal prep".
8. **Client — storage:** localStorage key `absbyai_saved_preps`: `[{ id, name, createdAt, servings, remaining, perServing: { items, totals }, batchTotals }]`. No photo stored (keeps localStorage small).
9. **Client — logging:** a "Your meal preps" strip/cards in the tracker: name, per-serving calories/protein, "7 of 12 left". Tap → logs one serving into `absbyai_logged_meals` exactly like a normal logged meal (so daily totals, sync, and uneaten-food all just work), decrements `remaining`. Controls: edit servings, reset remaining (new week, same recipe), delete.
10. **Account sync:** add `saved_preps` to the existing meal-sync endpoints — simplest is a new `GET/POST/DELETE /api/saved-preps` trio mirroring `/api/meals` with a `saved_preps` Postgres table (`CREATE TABLE IF NOT EXISTS` on boot, same pattern as `meals`). OPEN: if this bloats the task, ship localStorage-only and note sync as follow-up — logging still syncs because logged servings go through the normal meal log.

### Part C — Uneaten food

11. **Entry point:** on any logged meal in today's log (including logged meal-prep servings), a "Didn't finish?" affordance.
12. **Chips path (client-only):** options "Left ~¼" / "Left ~½" / "Left ~¾" scale all items' grams/macros/calories by the eaten fraction; plus a per-item mode listing the meal's line items with "left it" toggles (removes that item's contribution) — covers "ate it all but left the sauce". Update the stored meal (keep original in a `preAdjustment` field for undo), recompute daily totals, re-sync if logged in (update = delete + re-POST via existing endpoints, or add a PUT — keep it simple).
13. **Photo path (new endpoint):** `POST /api/refine-leftovers` — Haiku 4.5, free, `aiLimiter`, modeled directly on `/api/refine-meal`. Input `{ analysis: { items, mealName }, photos }` (leftover photo(s), multi-photo allowed). Structured output: per original item, `fraction_remaining` (0–1). System prompt: you are shown the itemized estimate of a meal AS SERVED and photo(s) of what was LEFT UNEATEN; estimate the fraction of each line item remaining; items not visible in the leftovers are 0. Server multiplies each item by `(1 − fraction_remaining)`, re-runs `enforceMacroMath`, returns revised items/totals. Client shows a revised receipt ("You ate: …") with the subtraction visible per item, then updates the logged meal as in step 12.
14. **Copy:** keep it judgment-free ("Leaving food is a win — log it and bank the calories").

### Part D — Ship it

15. Local UI testing with dummy keys (`PORT=3456 ANTHROPIC_API_KEY=dummy GEMINI_API_KEY=dummy node server.js`, or the `abs-by-ai` config in `.claude/launch.json`). **The local Anthropic key is invalid — Claude endpoints must be tested on prod after deploy.**
16. Commit, push to `main`, confirm Railway auto-deploy, then verify live on absbyai.com: (a) multi-photo analysis of a real meal (overhead + side), (b) create a meal prep from an ingredients photo with servings=12 and one-tap log two servings, (c) chips subtraction, (d) leftover-photo subtraction. Update `AI_COORDINATION.md` at start and finish per project rules.

## Things to Avoid / Lessons Learned

- **Never trust model calorie figures over macro math** — always route new/edited items through `enforceMacroMath` (the alcohol bug, commit `05ac0f2`, came from this).
- **Keep `raw` uncalibrated numbers flowing in responses** — the upcoming eval-harness task depends on them.
- **Don't remove the legacy single-photo request shape** — deployed native wrappers call prod.
- **No SDK** — the codebase uses raw `fetch` to the Anthropic API with an AbortController timeout pattern (see the supplement-audit fix, commit `751fe7b`); copy that pattern for any new call.
- **Charging twice for one meal was explicitly rejected** — refine, leftovers, and one-tap prep logs stay free.
- **Run-to-run variance is real** (a whiskey pour swung a meal ~10% between runs) — don't be alarmed if prod verification numbers wiggle; structure, not exact numbers, is what to verify.
- Meal photos can be large — every photo must go through the existing client downscale pipeline before upload.

## Relevant Files & Locations

- `server.js` — analyze (~1605), refine (~1741), schema (~1492), calibration (~1482), `enforceMacroMath` (~1555), freemium constant (~105), meal sync (~2847), credits store (~1991)
- `index.html` — `macroSection` (upload, receipt card, clarify chips, log, daily totals)
- `HANDOFF_macro_tracker.md` — original build handoff (architecture + marketing framing)
- localStorage keys: `absbyai_logged_meals` (existing), `absbyai_saved_preps` (new)
- Prod: https://absbyai.com (Railway auto-deploys from GitHub `main`)
- Env: `ANTHROPIC_API_KEY` (valid only on Railway)

## Model & Effort Recommendation

This task modifies the Anthropic API integration code in `server.js` (prompts, schemas, a new Claude endpoint) — that's an **always-Claude** task type regardless of usage level.

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking — the plan is fully specified; Sonnet handles multi-file implementation of a settled plan well. |
| **If Claude usage is high / approaching a limit** | Still Claude (API-integration override). Split the batch: Part A+C first (smaller), Part B in a second session. Escalate to Opus only if the prompt/schema work misbehaves on prod verification. |

## Starter Prompt for the Next Task

> Read `handoff-20260717-macro-tracker-v2.md` in the project root — it's a complete, decided plan to add three features to the Abs By AI macro tracker: multi-photo meal analysis, meal-prep saved meals (batch photo ÷ servings, one-tap logging), and uneaten-food subtraction (both quick chips and a leftover-photo Haiku endpoint). All product decisions are already made in the doc; don't re-open them. Also skim `HANDOFF_macro_tracker.md` for the original architecture. Start with Part A (multi-photo) in `server.js` + `index.html`, then Parts B, C, D in order, updating `AI_COORDINATION.md` when you start. Commit, push to main, and verify each feature live on absbyai.com per the project's delivery rules.
