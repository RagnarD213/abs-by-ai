# Handoff: Test replacement models for the male Gemini slot

**Date:** 2026-08-07
**Project:** Abs By AI
**Business goal this serves:** Technical excellence → adoption. The transformation image *is* the product. Men are the marketing target (every ad script is male-voiced), and the model serving them under-changes so reliably that Dan rejected **both** candidates in 6 of 6 blind rows today.

---

> ## ⚠️ READ FIRST — added hours after this doc was written, and it changes the running order
>
> Dan asked *"why did our Gemini generations get worse? They were good before."* He is right, and the cause is **ours**, not the model's.
>
> Commit **`14b4790` (2026-07-25)** halved the male muscle anchors (`+5/+8/+12/+15 lb` → `+2/+4/+6/+8`), replaced "visibly BIGGER / distinctly larger / noticeably thicker" with "**slightly** fuller / rounder / wider", added *"NEVER a bodybuilder…"*, and **dropped the pounds figure from the moderate-male path entirely.** It was justified by round 1's 33 `too muscular` tags — of which **Gemini contributed exactly ZERO**, while contributing the **most** `not enough change` complaints (11). The anchors are global, so we tuned away FLUX's failure on the model with the opposite failure.
>
> Dan's labels on the same 3 photos: `not enough change` went **75% → 100%**, and the one image he ever picked BEST and tagged `just right` (`lean-male__dramatic`) is now rejected. A same-day A/B holding the model constant and varying only the prompt era confirms the pre-retune prompt produces a visibly bigger, more V-tapered result on the lean case.
>
> **Therefore: do the cheap prompt-magnitude restoration FIRST (~$0.24, one commit to revert), and only run this model swap if that fails.** Details in `AI_COORDINATION.md` → "WE CAUSED THE MALE GEMINI REGRESSION OURSELVES".
>
> **Do NOT revert `14b4790` wholesale** — it also removed the tan instruction, and that fix worked (3 `too tan` tags on Gemini male in round 1, **zero** since; today `skin tone right` on 6 of 6). Restore muscle magnitude only; keep the no-tan rule and the no-bodybuilder ceiling.
>
> This also **retracts** the "prompt lever is exhausted" claim in Key Decisions below: all three failed attempts tried to ADD ab-definition language, and none restored the muscle magnitude that was deleted. That is a different lever and it is untested.

## Objective

Find a replacement for **Gemini 2.5 Flash Image on the MALE generation path**, using blind Dan-labelled A/B batches, and ship the swap only if it beats the current Gemini baseline. This is the male mirror of the female Seedream swap shipped 2026-07-28 (commit `8bee66c`).

This is a **model** question, not a prompt question. That is settled — see Key Decisions.

---

## Current State

**Production today (`server.js` ~2763):**

```js
const useSeedream = sex === 'female' && !!REPLICATE_API_TOKEN;
const challengerPromise = ensembleEligible
  ? (useSeedream ? callSeedream(condenseForKontext(prompt)) : callFluxKontext(condenseForKontext(prompt)))
  : Promise.resolve({ ok: false, skipped: true });
let result = await callGemini(prompt);          // <-- the ANCHOR, and the weak leg for men
```

- Every generation runs **two** models in parallel, and a Claude judge picks the winner.
- **Men:** Gemini (anchor, full prompt) + FLUX Kontext (challenger, condensed prompt).
- **Women:** Gemini + Seedream 4.5. Already swapped, already working.
- `callSeedream` **already exists and is production-tested** — it is wired for women today. Reusing it for men is a routing change, not new integration code.

**What today's round-6 test established (2026-08-07, all verified):**

| Male Gemini, 6 blind rows | result |
|---|---|
| rows where Dan rejected BOTH candidates | **6 of 6** |
| tags | `not enough change` 6/6, `not enough ab definition` 6/6 |
| FLUX, same 12 rows | **4 picks, 3 `just right` tags** |
| Gemini, same 12 rows | **0 picks, 0 `just right`** |

Dan's words: *"not enough change on the top six. A lot of them look exactly the same as the before."*

**The ab-ladder prompt fix was reverted** (`feb94e0`, reverting `4e4f4d1`) after failing its pre-registered bar. Production is back on the pre-ladder prompt, live-verified.

**Free baseline — do not regenerate it.** The current-production-prompt Gemini male images already exist and are **already Dan-labelled**:
- `bakeoff/round5-prompt-ab/out/` + `labels.json` (18 rows, incl. 6 male Gemini)
- `bakeoff/round6-ab-ladder/out/` + `labels.json` (12 male rows; the "old" arm is the current production prompt)

That makes the Gemini baseline arm **$0**.

---

## Key Decisions Already Made

- **The prompt lever on male Gemini is EXHAUSTED. Do not attempt another prompt edit.** Three independent measured attempts have now failed: (1) more/denser ab language, (2) the prose `CALIBRATION RULE` the assembler silently ignored, (3) today's `[[MARKER]]`-scoped ab ladder. Attempt 3 was built correctly and **verified on the wire** in both the full and condensed prompts — the instruction reached the model and the model did not act on it. "We wrote it badly" is no longer an available explanation.
- **The under-change is NOT limited to heavier males.** Earlier notes in `AI_COORDINATION.md` framed it that way. Today's labels show lean, moderate and heavier all failed identically. Corrected.
- **This must be a SWAP, never a third candidate.** The judge is validated **2-way only**: held-out pairwise 80.5%, but **N-way top-1 is 42.9%**. Adding a third model puts the judge in a regime where it is barely better than chance. Recorded constraint — do not relitigate.
- **Gemini is the ANCHOR, not the challenger — so this is a bigger change than the female swap.** Gemini currently (a) receives the **full** prompt while challengers get the condensed one, (b) is the fallback when the challenger fails, and (c) is rescued *by* the challenger when it is safety-blocked. Any replacement must preserve those three roles.
- **Keep Gemini for women.** Female Gemini is healthy (5 of 6 rows produced a pick in round 5). Scope this to `sex === 'male'` only.
- **Drop `flux-2-pro` from consideration** — dead last in round 1 (12/12 "too muscular", 0 skin-tone-ok).
- **No `deviceId` on any test call, ever.** It spends real credits and triggers a data-file commit → Railway redeploy.

---

## Detailed Plan

### Step 1 — Refresh the model roster before testing (do not skip)

The round-1 roster is from 2026-07-24. Check what is current on Replicate and Google before spending. Pull the **live** OpenAPI schema for any candidate and confirm the exact input fields rather than trusting the adapter:

```bash
curl -s https://api.replicate.com/v1/models/<owner>/<name> -H "Authorization: Bearer $REPLICATE_API_TOKEN" | python3 -m json.tool | head -60
```

**OPEN:** whether a newer Gemini image model (successor to 2.5 Flash Image / nano-banana-pro line) exists that fixes this natively. Worth 10 minutes — it would be the cheapest possible fix.

### Step 2 — Pick the candidates

Recommended three, with the round-1 evidence and the real production risk for each:

| Candidate | Why | Risk to check |
|---|---|---|
| **seedream-4.5** | Already integrated (`callSeedream`), $0.04, 18.2s, **0 moderation blocks in 16 female cells**, beat Gemini 9 of 12 blind female rows | **Hard 4000-char prompt limit.** Male full prompts run 4,027–6,472 chars, so it *cannot* take the full anchor prompt — it must get the condensed one. Note the asymmetry honestly. |
| **nano-banana-pro** | Round 1's "acceptable king" — reliable, 10 acceptable | **Stricter safety than Gemini** — 2 `IMAGE_SAFETY` refusals on heavier males that plain Gemini passed. A straight swap could *lose* coverage. Measure the block rate. |
| **gpt-image-1.5** | Most round-1 "best" picks (4), 0 "too tan" | **57.5s and ~$0.19/image** (~6× latency, ~5× cost of Gemini) and **no `match_input_image` aspect ratio**, so framing can never exactly match the input. Likely a production-fit failure even if it wins on looks. |

### Step 3 — Run the batch

Copy `bakeoff/round6-ab-ladder/` to `bakeoff/round7-male-model-swap/`. It already has the right shape: `cases.js` / `build-prompts.js` / `run.js` / `build-gallery.js`, its own `.gitignore` keeping `*.jpg` and `gallery.html` out of the **public** repo.

- **Cases:** the 3 male photos × 2 tiers = 6 cases (`lean-male`, `moderate-male`, `heavier-male` × Subtle/Ripped). Already defined in `cases.js`.
- **Arms:** one per candidate model. **Gemini baseline arm reuses the existing labelled images at $0** (same trick round 6 used for its "old" arm).
- **Prompts:** each candidate gets what it would actually receive **in production if it took the Gemini slot** — full prompt where the model allows it, condensed for Seedream (4000-char ceiling). Assert the char count programmatically; `build-prompts.js` already does this.
- **Estimated spend:** 6 cases × 3 models = 18 images ≈ **$2.18** (seedream $0.24 + nano-banana $0.80 + gpt-image $1.14). Under the $5 single-batch and $10 session caps — no extra approval needed, but **state the estimate before running**.

**Harness bug to fix first (bit us today):** `run.js` skips any cell whose `.json` exists — including failed `{ok:false}` records. After a provider outage a re-run silently reports `cached` and generates nothing. **Make `run.js` treat `ok:false` as "not cached."**

### Step 4 — Blind gallery → Dan

`node build-gallery.js`, then publish. Non-negotiable invariants the builder already enforces — keep them:
- **Slot-A balance asserted per set** (never let one model sit in slot A on every row).
- **Letters PINNED via `out/key.json`** so a later rebuild cannot re-point an answered row. Verify pins held after any rebuild, and diff the published HTML against the new build.
- **Blinding check:** zero `key.json` entries present in the built HTML.
- Exercise the page in a real browser before sending (persistence, mutual exclusion, no console errors).

**Publishing gotcha:** the Artifact tool refuses with "this session hasn't viewed the latest version" whenever the current session hasn't fetched the live page. The fix is `WebFetch` the URL → confirm → verify your build preserves it → publish **without** `force`. Do not reach for `force`.

### Step 5 — Decide, with a bar set BEFORE looking

Pre-register this and write it into `AI_COORDINATION.md` before generating anything:

> A candidate replaces Gemini on the male path only if it (a) **produces a pick in more than 1 of 6 rows** (Gemini's round-5 male score was 1 of 6; today's was 0 of 6), (b) shows **no increase in moderation blocks** vs Gemini's male block rate, and (c) is **under ~25s median latency**. A model that wins on looks but costs 57s fails (c) and does not ship.

### Step 6 — If a winner emerges, ship it

Mirror `8bee66c` exactly:
- Change **only** the leg selection. Judge, identity gate, verifier ladder, credit logic and fail-open stay untouched.
- Preserve Gemini's three anchor roles (full-prompt receiver, challenger-failure fallback, safety-block rescue partner) — or consciously re-architect them and say so.
- Telemetry: `models_run` and `served_model` must reflect the new pairing.
- Verify with **stubbed providers over HTTP against the real `server.js`** (note: `server.js` does `const fetch = require('node-fetch')` at line 4, so a `globalThis.fetch` patch does **not** reach it — stub via the require cache).
- Then 2–3 real prod generations (no `deviceId`) confirming `models_run`, and one female generation confirming the female path is untouched.

---

## Things to Avoid / Lessons Learned

- **Do not add a third candidate model** (judge is 2-way validated; N-way top-1 42.9%).
- **Do not "fix" this with prompt text.** Three measured failures. See Key Decisions.
- **Do not regenerate the Gemini baseline** — labelled images already exist in round-5 and round-6 output.
- **Provider balances silently degrade and `/health` stays 200.** This has now happened **four** times (Replicate, Anthropic, Google twice). The tell is `models_run` collapsing to one model in the telemetry of a real generation. Probe with one real prod call before blaming code.
- **EXIF orientation:** `sips -r` rotates pixels but does not clear the tag; Gemini ignores the tag, Seedream honours it, and the output looks upside-down. Use PIL `ImageOps.exif_transpose` and save without EXIF. (Production is unaffected — the client canvas-downscales first.)
- **The repo is PUBLIC.** Test photos and generated `.jpg`s must stay gitignored. Run `git check-ignore -v` on any new output folder before staging.
- **Replicate throttles to 6 req/min when the balance is under ~$20**, even with credit remaining. Keep it above $20 or batches will 429.
- `condenseForKontext` caps output at ~1800 chars of directive + ~250-char tail, so no challenger has ever needed a manual trim — but assert it rather than assuming.

---

## Relevant Files & Locations

| What | Where |
|---|---|
| Ensemble routing (the line to change) | `server.js` ~2763 (`useSeedream`), `callSeedream` ~2647, `callFluxViaReplicate` ~2594 |
| Model adapters | `bakeoff/adapters.js` (6 models with `nominalCost`) |
| Harness to copy | `bakeoff/round6-ab-ladder/` |
| Male test photos | `bakeoff/round5-prompt-ab/photos/{lean,moderate,heavier}-male.jpg` |
| Dan's labels (regression sets) | `bakeoff/round5-prompt-ab/out/labels.json`, `bakeoff/round6-ab-ladder/out/labels.json` |
| Judge + weights | `server.js` `JUDGE_SYSTEM`; exemplars in `assets/judge-exemplars/` |
| Coordination board | `AI_COORDINATION.md` → ab-ladder verdict section |
| Env vars (names only) | `GEMINI_API_KEY`, `REPLICATE_API_TOKEN`, `ANTHROPIC_API_KEY` |
| Prod | https://absbyai.com · PostHog project 458833 |

---

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking** for the batch run + gallery (mechanical: copy harness, run, publish). **Escalate to Opus with extended thinking for Step 6** — the swap touches the ensemble/judge/fallback logic, where being wrong is expensive to unwind. |
| **If Claude usage is high / approaching a limit** | **Codex (current flagship), medium effort** for Steps 1–4. Still bring **Step 6 back to Claude** — see the override below. |

**Task-type override, applies regardless of usage:** Step 6 touches the Anthropic API integration (the judge) and the generation ensemble's fallback behaviour — always-Claude work per the standing rule. Steps 1–5 are routine batch/harness work and are fine on the cheap tier.

**Interpretation of Dan's labels is Dan's job, not the model's.** Do not let any model overrule his picks.

---

## Starter Prompt for the Next Task

> Read `Handoffs/handoff-20260807-male-gemini-model-swap.md` and `AI_COORDINATION.md` (the ab-ladder verdict section) first.
>
> Goal: find a replacement for Gemini 2.5 Flash Image on the **male** generation path. This is a model question — the prompt lever is exhausted, with three measured failures. Do not attempt another prompt edit, and do not add a third candidate (the judge is 2-way validated only).
>
> First concrete action: refresh the model roster (Step 1) — pull live schemas for `seedream-4.5`, `nano-banana-pro` and `gpt-image-1.5`, and check whether a newer Gemini image model exists that might fix this natively. Then copy `bakeoff/round6-ab-ladder/` to `bakeoff/round7-male-model-swap/`, **fix the `run.js` bug where a failed `{ok:false}` cell is treated as cached**, and state the estimated spend (~$2.18) before running the batch.
>
> The Gemini baseline is FREE — reuse the already-labelled images in `bakeoff/round5-prompt-ab/out/` and `bakeoff/round6-ab-ladder/out/`. Generate challengers only. No `deviceId` on any call.
>
> Pre-register the ship/no-ship bar in `AI_COORDINATION.md` **before** generating anything (Step 5), then publish a blind gallery for Dan to label.
