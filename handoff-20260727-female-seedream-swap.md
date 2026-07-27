# Handoff: Female generations — swap FLUX leg for Seedream 4.5

**Date:** 2026-07-27
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Profitability via product quality — female users currently get a measurably worse product for the same price, and heavier women (a large paying segment) hit a known quality wall with no second model to rescue them.

## Objective

Make female transformations run a real two-model race again. Today every generation runs Gemini 2.5 Flash Image + FLUX Kontext Pro in parallel with the Claude judge picking the winner — but FLUX's safety filter refuses most female photos (E005 "flagged as sensitive", ~3 of 4 female runs in testing), so women silently fall back to Gemini-only and never benefit from the ensemble. The fix: **route female generations to Gemini + Seedream 4.5, keep male generations on Gemini + FLUX Kontext, unchanged.** Ship only after a small blind-labeled female test batch confirms Seedream's female output quality to Dan's eye.

## Current State

- **Production ensemble (server.js):** two candidates generated in parallel — `callGeminiImage` (Gemini 2.5 Flash Image, ~server.js:2363) and `callFluxKontext` (~server.js:2541; Replicate path `black-forest-labs/flux-kontext-pro` at ~2497, BFL-direct fallback at ~2549). Ensemble kickoff at ~server.js:2597 uses `condenseForKontext(prompt)` for the FLUX leg. The rebuilt judge-v2 (rubric scoring, order-swap double pass, composite in our code) routes: broken identity → never shown; one survivor → serve it; agreement + clear margin → auto-pick; otherwise → 2-way chooser. All provider errors fail open to Gemini-only.
- **Sex is already known server-side.** The photo check returns the subject's apparent sex (`OK FEMALE` etc., ~server.js:1426–1444), and `/api/generate-image` already receives and uses `sex` (e.g. `rungBudget` at ~2676, female retry preambles at ~2703, telemetry at ~2803). No new detection work is needed — routing is a conditional on an existing variable.
- **FLUX female block is confirmed and un-fixable.** `safety_tolerance` maxes at 2 when an input image is attached (verified against Replicate's live OpenAPI schema); the server already runs at that ceiling. The block is probabilistic (~75% observed on female photos), not absolute.
- **Gemini's female weakness is documented (A3.1):** Gemini resists large fat-loss edits on heavier female bodies regardless of prompt strength, compounding, or forced retries. The FEMALE HEAVIER REALISM RULE (honest ~25% target at max) was the workaround. Heavier women are the segment a second model helps most.
- **Seedream 4.5 evidence (bake-off round 1, `bakeoff/round1/`):** the only model of six with **zero moderation blocks** (including all female cells); won the two skin-tone-critical cases in Dan's blind labels; 2 "best" picks overall; median 18.2s / ~$0.04 per image. Its round-1 failures were all the 4,000-char prompt limit, which the condensed prompt solves.

## Key Decisions Already Made

- **Swap, don't add.** The judge is validated as a 2-way picker only (N-way top-1 is 42.9% held-out). Never run 3 candidates — replace the FLUX leg for women.
- **Men keep Gemini + FLUX.** FLUX demonstrably wins the hard male cases (broke the Gemini heavier-male ceiling); no reason to touch it.
- **Test batch before shipping.** Seedream was only lightly exercised on female photos in round 1; Dan labels a blind female batch first (~$1–2 of spend).
- **Condensed prompt for Seedream.** It hard-rejects >4,000 chars (422), and Dan's labels favored the condensed variant anyway (8 of 10 bests).
- **Judge, identity gate, verifier ladder, fail-open, credit logic: all unchanged.** Worst case if Seedream misbehaves is today's Gemini-only behavior.
- **No purchase/UI surface changes** → baseline web verification only, no mandatory native retest (server-side routing change; confirm nothing visible changed at 375×812).

## Detailed Plan

1. **Confirm the exact Seedream Replicate slug and input schema.** The round-1 adapter lived in a session scratchpad (not committed). Check `bakeoff/round1/results.json` / `run-log.txt` for the model name used (Seedream 4.5 edit via Replicate), then pull the live OpenAPI schema from Replicate to confirm input field names (image input, prompt, any aspect/size params). Do not guess the slug.
2. **Female test batch (no production code changes).** Rebuild the light harness per the established recipe (extract `SYSTEM_PROMPT`/`goalSystemPrompt()` from `public/index.html`, drive prod `/api/generate-prompt`, call Seedream directly; **no `deviceId`** so no credits/redeploys; keys read from Railway into a 0600 scratchpad env file). Run Seedream vs Gemini on: both female proof photos (`female-before.webp`, `female-after.webp` — note both are sports-bra/shorts), the heavier female proof photo, at moderate + max, condensed prompt. ~12–16 images, ~$1–2. Publish a blind gallery artifact for Dan; record his labels.
3. **Gate:** if Dan's labels say Seedream is at least as good as Gemini on women (especially heavier builds), proceed. If not, stop and record the finding — the status quo is acceptable and nothing shipped.
4. **Implement routing in `server.js`:** at the ensemble kickoff (~2597), when `sex === 'female'`, run `callSeedream(condensedPrompt)` in place of `callFluxKontext(...)`. New `callSeedream` mirrors `callFluxKontext`'s Replicate pattern (`Prefer: wait` + polling fallback, 90s AbortController, fail to `{ok:false}`). Reuse `condenseForKontext` if its output fits Seedream's 4,000-char limit for the longest female prompts — assert this programmatically; otherwise add a trim. `sex === null`/unknown routes as male (today's pair) — least-change default.
5. **Telemetry:** `models_run` / `served_model` must carry `seedream-4.5` so PostHog `generation_verifier` events distinguish the legs. No client change (client forwards the telemetry object blindly).
6. **Verify with the stubbed-provider HTTP test pattern** (the same approach as the 57-assertion Phase 4 suite): female → seedream leg invoked, male → flux leg invoked, seedream error → fail-open Gemini-only, judge/chooser/credit paths unchanged. `node --check` on server.js.
7. **Deploy + live-verify:** commit, push to `main`, confirm Railway deploy. Run 2–3 real female generations on prod proof photos (moderate + max, incl. heavier) — confirm both models ran, judge scored both, and eyeball the served image. Run 1 male generation to confirm the FLUX path is untouched. Check Railway logs for zero judge/provider errors. Baseline browser check at 375×812 + desktop.
8. **Watch:** first week of real female traffic in PostHog — `models_run` distribution (Seedream should now appear on ~100% of female runs vs FLUX's ~25%), `judge_*` win rates, `chooser_shown` rate.
9. **OPEN (flag for Dan, do not decide unilaterally):** if Seedream genuinely delivers dramatic change on heavier female bodies, the FEMALE HEAVIER REALISM RULE's honest-but-modest targets (~25% at max) may be leaving quality on the table for the Seedream leg. Revisit only with Dan's eyes on real results — that rule was hard-won (A3.1).

## Things to Avoid / Lessons Learned

- **Do not raise FLUX `safety_tolerance`** — already at the image-input maximum (2). Dead end, verified.
- **Do not add a third candidate** — judge is 2-way validated only.
- **Do not send Seedream the full prompt** — hard 422 over 4,000 chars.
- **Do not run test batches with a `deviceId`** — spends credits and (historically) triggered redeploy churn; omitting it is the clean prod-verification path.
- **Prompt scoping is enforced in code, not prose** (`[[MUSCLE_*]]` markers, `muscleAxisPlan()`); prose-only scoping has leaked twice. Don't touch the marker system.
- **Replicate throttles below a $20 balance** (6 req/min, burst 1) — check the balance before the batch; parallel requests will 429 on a low balance.
- **Provider $0 balances break generations while `/health` stays 200** (happened with both Replicate and Anthropic). If generations fail mid-task, check balances first.
- Keep `bakeoff/round1/labels.json` as the regression ground truth; add the new female labels alongside, don't overwrite.

## Relevant Files & Locations

- `server.js` — ensemble ~2497–2600 (FLUX Replicate call, `callFluxKontext`, kickoff + `condenseForKontext`), sex plumbing ~1426–1444 / ~2676 / ~2803, judge (`JUDGE_SYSTEM`, `judgeComposite`)
- `public/index.html` — `SYSTEM_PROMPT`, `goalSystemPrompt()` (prompt source for the harness; not expected to change)
- `bakeoff/round1/` — `results.json`, `run-log.txt`, `labels.json`, `key.json`, `judge-cache/`
- `bakeoff/judge-v2.js`, `bakeoff/judge-eval.js` — judge reference + regression eval (`CACHE_ONLY=1 HELD_OUT_ONLY=1 node judge-eval.js` → 80.5% held-out, $0)
- Proof photos: `female-before.webp`, `female-after.webp`, heavier female proof asset (see round-1 grid)
- Env: `REPLICATE_API_TOKEN`, `GEMINI_API_KEY` (Railway → abs-by-ai service)
- Deploy: push to `main` → Railway auto-deploy → verify on https://absbyai.com
- Telemetry: PostHog `generation_verifier` events (`models_run`, `served_model`, `judge_*`, `chooser_*`)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Still Claude — Sonnet 5, standard thinking (see override below) |

Task-type override: this touches the AI ensemble/judge code in `server.js` (Anthropic API integration territory) and image-quality judgment calls, so it stays on Claude regardless of usage. Sonnet 5 is sufficient — the routing change is small and the hard decisions are already made; escalate to Opus only if the Seedream schema work turns out messier than expected.

## Starter Prompt for the Next Task

> Read `handoff-20260727-female-seedream-swap.md` in the Abs By AI project root and execute it. Goal: female transformations should run Gemini + Seedream 4.5 (males keep Gemini + FLUX Kontext), because FLUX refuses ~75% of female photos and women currently get a one-model product. Start with step 1–2: confirm the Seedream Replicate slug from `bakeoff/round1/`, then run the blind female test batch (no deviceId, condensed prompt, ~$1–2) and publish the gallery for Dan to label. Do NOT change production code until Dan's labels clear the gate in step 3. All settled decisions are in the handoff — don't relitigate the 2-candidate ceiling, the FLUX safety_tolerance dead end, or the FEMALE HEAVIER REALISM RULE.
