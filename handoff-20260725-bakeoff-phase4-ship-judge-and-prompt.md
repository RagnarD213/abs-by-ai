# Handoff: Model bake-off Phase 4 — ship the rebuilt judge + fix the generation prompt

**Date:** 2026-07-25
**Project:** Abs By AI / absbyai.com
**Business goal this serves:** App adoption first (transformation quality *is* the product's core promise), then technical excellence. Two things decide what a user sees: the prompt that generates the images, and the judge that picks which one to show. Phase 3 proved both are currently mis-aimed. This phase fixes both.

## Objective

Ship the rebuilt judge (`bakeoff/judge-v2.js`) into `server.js` `judgeCandidates`, and make the three `SYSTEM_PROMPT` changes that Dan's 80 labels justify — neutralize the tan block, shrink the muscle anchors, add Kino-body language. Then live-verify on real photos and watch PostHog. These are two independent changes to the same user-visible outcome: **ship and verify them separately**, judge first, so a quality regression is attributable.

## Current State

**Phases 1–3 are complete, committed, and pushed. No production generation code has been changed yet.**

- **Phase 1/2 (done):** 6-model bake-off harness in `bakeoff/`; 76 candidate images across 12 cases in `bakeoff/round1/images/` (gitignored, ~55 MB, present on Dan's machine — regenerate with `node phase2.js` if lost).
- **Ground truth (done):** `bakeoff/round1/labels.json` — Dan's 80 labels, decoded to models via `key.json`. This is now the permanent regression eval.
- **Phase 3 (done, commit `f4a6de5`):** the production judge was baselined and a replacement was built and validated.

| | production judge | rebuilt `judge-v2` |
|---|---|---|
| **held-out pairwise (7 cases, 41 pairings)** | 61.0% | **80.5%** ✅ |
| all-cases pairwise (10 cases, 58 pairings) | 64.7% | **84.5%** |
| case-level agreement | 60% (6/10) | **100% (10/10)** |
| order-flip rate | 17.2% | 13.8% |

- **A separate production bug was found and already shipped** (commit `c08c345`, live-verified): `server.js` was forwarding upstream provider errors verbatim, so when the Anthropic balance hit $0 every visitor saw *"Your credit balance is too low… go to Plans & Billing."* Now sanitized via `friendlyAIError()`. Nothing left to do there.

## Key Decisions Already Made

Do not re-open these — each is backed by data in this repo.

- **Dan's aesthetic is the spec: shredded/very-defined abs at low body fat, V-taper, natural athletic muscle — NOT bodybuilder mass, NO added tan, not oiled, not airbrushed.** Confirmed by 80 labels (tag totals: too muscular 33, too tan 23, looks fake 20, not enough change 17), not assumed.
- **"More muscular" is a demerit above athletic, not a win.** This is the exact instruction the current judge gives and it is why it disagrees with Dan.
- **Keep `claude-sonnet-5` as the judge model.** `claude-opus-5` was tested on the identical held-out set and scored *worse* on every measure (73.2% pairwise / 4-of-7 case-level / 28.6% N-way). Production already runs Sonnet — **no model change needed.** Don't retest this.
- **Keep the few-shot exemplars.** Ablation: without them, held-out pairwise 78.0% and case-level 5/7, vs 80.5% and 7/7 with.
- **Keep the a-priori composite weights** (`DEFAULT_WEIGHTS` in `judge-v2.js`). A 4,320-setting offline sweep (`judge-tune.js`, free to re-run) puts them at the **median**, with 62% of settings ≥80%. The best setting reaches 87.8% but only by zeroing the bulk and under-change penalties — i.e. deleting the demerits that encode the taste — and its N-way top-1 collapses to 28.6%. That is overfitting to 41 pairings. **Rejected deliberately.**
- **Production keeps showing ≤2 images** (auto-pick or the 2-way chooser). The judge generalises to N candidates, but see the N-way caveat below before adding models.
- **Ship judge and prompt as separate commits, each live-verified.** Phase 3 deliberately kept them apart so the two changes don't confound each other; don't merge them now.

## Detailed Plan

### Step 1 — Ship the judge into `server.js` (own commit, live-verify before Step 2)

The target is `judgeCandidates` at **`server.js:2357`**, plus the routing block at **`server.js:2416–2440`**.

1. Replace the prompt text (currently `server.js:~2385`, the line instructing "the MORE dramatic, more impressive body transformation … (leaner, more muscular, more defined)") with the rubric spec from `bakeoff/judge-v2.js` → `SYSTEM_PROMPT`. Send it as the API `system` field, as the harness does.
2. Change the response contract from `{a,b,winner,margin}` to the per-candidate rubric: `{"candidates":[{id,identity,photoreal,skin_tone,definition,bulk,change,note}]}`. Port `scoreOnce`'s clamping/normalisation verbatim — it defends against out-of-range and missing values.
3. Port the **position-bias swap**: call twice (A,B then B,A), average each candidate's six dimension scores. Port `composite()` and `DEFAULT_WEIGHTS` unchanged.
4. **Rewire routing to use `orderDisagreement` instead of the model's self-reported `margin`.** The old `margin` was never validated and flipped 17.2% of the time on order alone. New rule, preserving today's shape:
   - any candidate `identity === 'broken'` → never shown (unchanged behaviour, and the gate is doing real work — it correctly rejected 3 candidates in the eval)
   - one survivor → serve it
   - two survivors, **no order disagreement**, both `identity === 'good'` → auto-pick the higher composite
   - otherwise (order disagreement, or a borderline identity) → the 2-way chooser
5. Keep the few-shot exemplar block and its `cache_control: {type:'ephemeral'}` — it is a stable prefix, so it prompt-caches and keeps cost down. **The three exemplar images must be reachable from the server**; they currently live in the gitignored `bakeoff/round1/images/`. **OPEN: decide how to ship them** — recommended is to commit the three "chosen" + three "rejected" + three BEFORE images (9 small JPEGs, downscaled to 768px as the harness does) into something like `assets/judge-exemplars/` and read them at boot. Do not point the server at `bakeoff/`.
6. Keep **fail-open** exactly as today: any judge error → `null` → serve the Gemini image through the existing verifier ladder. This is what makes the judge safe to ship.
7. Extend telemetry: keep `judge_*`, add the six rubric scores for the served candidate so real-traffic behaviour can be compared against `labels.json` later.
8. **Verify:** run the existing stubbed-provider HTTP tests for all routing paths, then a real prod generation on the proof photos. Confirm `models_run`, `judge_*`, `served_model` in the response and no latency regression (the judge now makes 2 calls instead of 1 — they run in parallel; confirm that in the logs).

### Step 2 — The three prompt fixes (own commit, live-verify separately)

All in `public/index.html` `SYSTEM_PROMPT`.

1. **Tan block — `public/index.html:3063–3067`.** This is the single clearest win: **23 "too tan" labels, and every one of Dan's 10 best picks was tan-free.** The block currently *instructs* a tan and scales it by intensity ("max/peak: add a warm sun-kissed bronze tan — approximately 2 shades deeper"). Replace all three intensity lines with a single rule: preserve the BEFORE photo's exact skin tone, a healthy glow at most, **no added tan/bronzing at any intensity**. Keep the existing final sentence protecting deep/dark complexions verbatim — it is doing real work.
2. **Muscle anchors — `public/index.html:3011–3016` (`MUSCULARITY ANCHOR TABLE`) and the `[[MUSCLE_*]]` blocks at 2999–3037.** 33 "too muscular" labels. The table currently asks for **+5/+8/+12/+15 lb** and the `[[MUSCLE_PRIMARY]]` block demands the subject "look visibly BIGGER". Shrink the numbers hard for the male fit/very_lean path and re-frame added size as *supporting* the abs rather than being the headline. Do **not** delete the marker structure — `muscleAxisPlan()` (`~3141`) strips these blocks deterministically by gender/condition, and that scoping mechanism is load-bearing (prose-only scoping failed twice before; see Lessons).
3. **Add Kino language** to the male paths: shredded-athletic, sharply separated abs, visible obliques/serratus, V-taper, natural athletic muscle volume, explicitly forbid bodybuilder-scale mass.
4. **Consider promoting the condensed prompt.** **8 of Dan's 10 best picks came from the condensed variant** — the one that already drops the tan block and the muscle anchors. That is independent evidence for fixes 1 and 2. `condenseForKontext` (`server.js:2209`) already produces something close to it. **OPEN for Dan:** whether the condensed prompt should simply become the main prompt for all models, rather than hand-editing the full one. Cheapest test: run the harness prompt-variant A/B again after fixes 1–3 and see whether full and condensed have converged.
5. **Verify** on prod with real photos across the male fit/very_lean, male moderate, male heavier, and female heavier paths. Confirm no truncation (`PROMPT_TRUNCATED` log), guardrails and CLOSING block intact, markers never leaking into a sent prompt.

### Step 3 — Re-run the regression eval

`labels.json` is now a permanent regression test. After the prompt changes, re-run `node judge-eval.js` from `bakeoff/`; everything is disk-cached so only genuinely new calls cost anything. Held-out pairwise must stay ≥80%.

## Things to Avoid / Lessons Learned

- **Never pass `temperature`/`top_p`/`top_k` to Claude 5-family models** — hard 400. The judge fails open, so a broken judge is *invisible* without checking Railway logs. This cost a full day once (commit `e39ac7c`).
- **Prose-only scoping of prompt rules does not hold.** Twice now a rule scoped by wording alone leaked into the wrong gender/condition path. The `[[MUSCLE_*]]` markers + `muscleAxisPlan()` exist because of that. Keep the deterministic mechanism.
- **Adding region-specific prompt detail crowds out overall transformation magnitude.** The lower-belly directive (reverted, `323135e`) made results *worse*. Prefer removing bad instructions over adding more good ones.
- **Asking for an achievable result beats asking for a peak one.** On heavier bodies Gemini hedges when asked for a contest-lean physique; the A3.1 realism rule got a *better* image by asking for less.
- **Don't chase the pairwise number with weight tuning.** The sweep shows you can reach 87.8% by deleting the demerits — and N-way collapses. The a-priori weights are the honest setting.
- **Never add a `deviceId` to a harness request** — it spends real credits, commits a data file, and triggers a Railway redeploy that kills in-flight generations.
- **Watch the Anthropic balance.** It drained to $0 mid-Phase-3 and took the live site's generations down while `/health` stayed 200. Auto-reload is the fix; `AI_PROVIDER_ACCOUNT_ERROR` in the Railway logs is now the greppable signal.

## Known Weakness to Carry Forward

**N-way top-1 is only 42.9% held-out (3/7).** Shown every candidate at once, the judge ranks Dan's pick first about half the time. This does **not** block Step 1 — production compares exactly two images, which is the 80.5% pairwise number — but it means **the judge is not yet trustworthy as an N-way chooser, so do not expand production to >2 candidate models on the strength of this eval.**

The remaining errors are **perceptual, not arithmetic**: 5 of the 9 remaining pairwise misses are the single case `heavier-male__max`, where the judge scores Dan's own pick as *more* tan (3.5–4), *bulkier* (4–4.5) and *less* photoreal (3) than the alternatives — while Dan tagged that image "skin tone right". No weighting flips that. The fix is a heavier-male exemplar or more labels on that body type. **OPEN for Dan:** ~10 more labels on heavier-male candidates would likely close this; worth ~20 minutes of his time.

## Relevant Files & Locations

- **Judge to replace:** `server.js` — `judgeCandidates` at `2357`, routing `2416–2440`, telemetry `~2549`. Judge model `claude-sonnet-5` (keep).
- **New judge to port:** `bakeoff/judge-v2.js` (`SYSTEM_PROMPT`, `scoreOnce`, `scoreCandidates`, `composite`, `DEFAULT_WEIGHTS`, `EXEMPLARS`).
- **Eval + tuning:** `bakeoff/judge-eval.js` (`HELD_OUT_ONLY=1`, `JUDGE_MODEL=`, `NO_FEWSHOT=1`, `CACHE_ONLY=1`), `bakeoff/judge-tune.js` (offline, free), `bakeoff/judge-lib.js`.
- **Results:** `bakeoff/round1/judge-baseline.json`, `judge-v2-claude-sonnet-5.json`, `judge-v2-claude-opus-5.json`, `judge-v2-claude-sonnet-5-nofewshot.json`. Cache: `bakeoff/round1/judge-cache/` (committed — re-runs cost $0).
- **Ground truth:** `bakeoff/round1/labels.json` + `key.json`.
- **Prompt to fix:** `public/index.html` — SKIN TONE `3063–3067`, `MUSCULARITY ANCHOR TABLE` `3011–3016`, `[[MUSCLE_*]]` blocks `2999–3037`, `muscleAxisPlan()` `~3141`. `condenseForKontext` in `server.js:2209`.
- **Env vars (names only):** `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `REPLICATE_API_TOKEN` (Railway service `abs-by-ai`, project `invigorating-liberation`). Railway CLI at `~/.npm-global/bin/railway` (not on PATH, authenticated).
- **Coordination:** `AI_COORDINATION.md` → active task has the full Phase 1–3 record.

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Opus 5, extended thinking.** Step 1 edits the Anthropic integration in the live generation path, and Step 2 is image-quality judgment against a taste rubric — both are expensive to get wrong. |
| **If Claude usage is high / approaching a limit** | **Claude Sonnet 5, standard thinking** for Step 1 (it is a well-specified port — the target code and the replacement both already exist). Escalate to Opus for Step 2, where the prompt edits are judgment calls needing real-photo evaluation. |

**Task-type override:** this is always-Claude regardless of usage — it touches the Anthropic API integration code *and* requires vision-based quality judgment. Codex is a poor fit for both. Note the *judge model under test* (`claude-sonnet-5`, already settled) is a separate axis from the model you run the session on.

## Starter Prompt for the Next Task

> Execute `handoff-20260725-bakeoff-phase4-ship-judge-and-prompt.md` (project root) — Phase 4 of the Abs By AI model bake-off. Phase 3 is complete at commit `f4a6de5`: the rebuilt judge in `bakeoff/judge-v2.js` scores 80.5% held-out pairwise agreement with Dan's labels vs the production judge's 61.0%, and 100% case-level vs 60%. Read that handoff first, plus `AI_COORDINATION.md` for the full Phase 1–3 record.
>
> Step 1: port `judge-v2` into `server.js` `judgeCandidates` (~line 2357) — rubric prompt as `system`, per-candidate JSON contract, the position-bias order swap, `composite()` + `DEFAULT_WEIGHTS` unchanged, and rewire routing at ~2416 to use `orderDisagreement` instead of the model's `margin`. Keep the identity gate and the fail-open behaviour exactly as they are. Decide how to ship the three few-shot exemplar image pairs to the server (they currently live in gitignored `bakeoff/round1/images/`). Commit and live-verify on absbyai.com before touching the prompt.
>
> Step 2, as a SEPARATE commit: the `SYSTEM_PROMPT` fixes in `public/index.html` — neutralize the tan block (3063–3067; 23 "too tan" labels and every one of Dan's best picks was tan-free), shrink the muscle anchors (3011–3016 and the `[[MUSCLE_*]]` blocks; 33 "too muscular"), and add Kino-body language. Keep the `[[MUSCLE_*]]` marker mechanism — prose-only scoping has failed twice.
>
> Do NOT change the judge model (Opus 5 was tested and is worse), do NOT re-tune the composite weights (a 4,320-setting sweep says the current ones are at the median; the higher settings overfit), and do NOT expand production beyond 2 candidate models — N-way top-1 is only 42.9%. Never pass `temperature` to Claude 5 models, and never add a `deviceId` to a harness request.
