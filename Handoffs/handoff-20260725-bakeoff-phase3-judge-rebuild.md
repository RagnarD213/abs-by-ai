# Handoff: Model bake-off v2 — Phase 3 (judge rebuild + eval against Dan's labels)

**Date:** 2026-07-25
**Project:** Abs By AI / absbyai.com
**Business goal this serves:** App adoption (transformation quality is the product's core promise) → then technical excellence. The generation ensemble already spends real money on multiple models per request; the judge is what decides which image the user sees, and right now it is provably optimizing for the look Dan rejects.

## Objective

Rebuild the generation judge so it picks the image Dan would pick. Phase 1 (harness + adapters) and Phase 2 (round-1 grid + blind labeling) are DONE. Dan has labeled all 12 cases — the ground-truth dataset now exists at `bakeoff/round1/labels.json`. Phase 3 = (1) measure how badly the CURRENT production judge agrees with Dan's labels, then (2) rebuild the judge (aesthetic rubric, position-bias control, few-shot exemplars, judge-model comparison) and prove it hits ≥80% agreement on Dan's "best" picks before any production code ships. This is the parent handoff: `handoff-20260724-model-bakeoff-v2.md` (§3 is the judge methodology; read it).

## Current State

**Phases 1 + 2 complete, committed, pushed, live-verified (no production code changed).**

- **Harness** lives in `bakeoff/` (committed). It extracts the real `SYSTEM_PROMPT`/`goalSystemPrompt()` out of `public/index.html`, drives prod `/api/generate-prompt` for the prompt text, then calls each model provider directly with **no `deviceId`** (so no credit spend, no data-file commit, no redeploy). `bakeoff/README.md` has the run recipe. Secrets live in `bakeoff/.env` (gitignored) — pull them from Railway with `railway variables --service abs-by-ai --kv | grep -E '^(GEMINI_API_KEY|REPLICATE_API_TOKEN|ANTHROPIC_API_KEY)=' > bakeoff/.env`.
- **Round-1 results:** `bakeoff/round1/results.json` (per-cell ok/blocked/error/latency/nominal-cost), `bakeoff/round1/key.json` (the blind key: `"<caseId>:<letter>" → {model, variant, latencyMs}`), `bakeoff/round1/run-log.txt`. The 76 generated images + 6 source photos are gitignored (55 MB) at `bakeoff/round1/images/` and `bakeoff/round1/photos/` on the machine that ran the batch — **Phase 3 needs these image files present locally to send to the judge.** If they're gone, re-run `node phase2.js` from `bakeoff/` (it re-spends ~$6 but is cached-idempotent) or regenerate only the specific cells the judge eval needs.
- **Ground truth:** `bakeoff/round1/labels.json` — 80 candidate labels across 12 cases: `{best, acceptable, tags[], note}` keyed by `"<caseId>:<letter>"`. Decode a letter to a model via `key.json`.
- **Blind galleries** (published artifacts, for reference): part 1 https://claude.ai/code/artifact/a7324148-3b4d-475a-ae41-15132c6b9de2 · part 2 https://claude.ai/code/artifact/75d72d4a-b557-4baa-b5fe-9504484fcbed

**What the labels say (the Phase 3 design inputs):**
- Dan's **best pick per case**: lean-male/dramatic → gemini-2.5-flash (full); lean-male/max → nano-banana-pro (condensed); moderate-male/dramatic+max → gpt-image-1.5 (condensed); heavier-male/dramatic → flux-kontext (condensed); heavier-male/max → flux-kontext (full); heavier-female/dramatic+max → gpt-image-1.5 (condensed); dan-real/dramatic → seedream-4.5 (condensed); dan-real/max → **NO best**; heavier-male-dark/dramatic → seedream-4.5 (condensed); heavier-male-dark/max → **NO best**.
- **8 of 10 best picks were the condensed prompt** (the variant that drops the tan block + muscle anchors). The full production prompt won 2.
- **Tag totals (80 labels):** too muscular **33**, too tan **23**, looks fake **20**, not enough change 17, skin tone right 14, just right 5, face drifted 4.
- **The two "no best" cases are both max/Ripped on a hard body** — every candidate was either bodybuilder-overshoot or "not enough change." No model solved max intensity on a heavier/harder body.

**The current production judge** (`server.js` ~line 2319–2410, function `judgeCandidates`): one `claude-sonnet-5` vision call, sends BEFORE + candidate A + candidate B, returns strict JSON `{a:{identity,photoreal}, b:{...}, winner, margin}`. **The winner instruction (line ~2349) literally says: pick "the MORE dramatic, more impressive body transformation ... (leaner, more muscular, more defined)."** That is optimizing for the exact 33 "too muscular" rejections. It has no skin-tone criterion, no "too muscular" demerit, binary winner + coarse clear/close margin, no position-bias control, and was never evaluated against ground truth. **Never pass `temperature`/`top_p`/`top_k` to Claude 5-family models — hard 400** (this silently killed the judge for a full day; commit `e39ac7c` removed it).

## Key Decisions Already Made

- **Dan's aesthetic = "Kino body": shredded/very-defined abs at low body fat, V-taper, NOT bodybuilder mass, NO added tan, not oiled, natural not airbrushed.** "More muscular beyond athletic" is a DEMERIT, not a win. This replaces the current judge's "more muscular = better" spec. (Confirmed by 80 labels, not assumed.)
- **Ground truth = Dan's `best` pick per case.** `acceptable` is a secondary signal (a wider "would ship this" set); tags/notes explain WHY and become the rubric language. Agreement is measured on the "best" picks.
- **Do NOT change production generation output in Phase 3.** Prompt fixes (kill tan block, shrink muscle anchors, Kino language) are Phase 4 — keep them out of the judge rebuild so the two changes don't confound each other. Phase 3 is judge-only.
- **No production code ships until the new judge beats the baseline on `labels.json`.** The labeled set becomes a permanent regression eval.
- **Provider/model facts already established** (don't re-derive): GPT Image 1.5 via Replicate needs `input_fidelity:"high"` and reads "Placed side by side with the input" as a literal diptych instruction (needs an explicit single-image clause); Seedream 4.5 hard-rejects prompts >4000 chars (422); flux-kontext refuses all female photos (E005); nano-banana-pro is stricter than gemini-2.5-flash on heavier males.
- **Production still shows ≤2 images to a user** (auto-pick or the 2-way chooser). Whether prod moves to >2 candidate models is a Phase-4 cost/latency decision. The judge rebuild should generalize to N candidates (rubric scores compose across N) but production routing stays as-is for now.

## Detailed Plan

**Step 1 — Baseline the current judge (cheap, do first).**
1. Write a scratchpad eval script in `bakeoff/` (e.g. `judge-eval.js`) that, for each case, loads the candidate images from `bakeoff/round1/images/` and their letters from `key.json`, and Dan's labels from `labels.json`.
2. Port the EXACT current production judge call from `server.js` `judgeCandidates` (~2325–2375) — same model (`claude-sonnet-5`), same prompt text, same JSON contract, **no temperature**. Keep it byte-for-byte so the baseline is honest.
3. The production judge is pairwise (A vs B). To score it against an N-way "best": for each case, run the judge on the pair {Dan's best, each other candidate}. Count it as "agrees" if the judge picks Dan's best over the alternative in a majority (or all) of those pairings. Also run it on a few full round-robins to see position bias. Record per-case agreement and the aggregate % — **this is the number everything must beat.** Expect it to be low, and expect it to systematically prefer the "too muscular" candidates (that's the whole point).
4. Save baseline results to `bakeoff/round1/judge-baseline.json` and report the number to Dan.

**Step 2 — Rewrite the judging spec around Dan's taste.** New judge prompt criteria (from `handoff-20260724` §3 Step 2, now confirmed by labels):
- **identity** (gate — keep: good/borderline/broken).
- **photoreal** (gate — keep; "looks fake" was tagged 20×, so this matters).
- **skin-tone fidelity (NEW):** matches the BEFORE photo's skin tone; penalize added tan/bronzing/warmth. (23 "too tan".)
- **aesthetic target / Kino (NEW):** very low body fat, sharply cut dramatic six-pack, V-taper, athletic — explicitly NOT bodybuilder mass. Muscularity beyond athletic proportions is a DEMERIT. (33 "too muscular".) Replace the "more dramatic/more muscular" winner line entirely.
- **transformation magnitude:** clearly changed vs BEFORE, but SUBORDINATE to aesthetic match — and note the "not enough change" failure (17×) so the judge doesn't swing to rewarding no-ops.

**Step 3 — Structural improvements to the judge call:**
1. **Per-candidate 1–5 rubric scores** per dimension instead of a bare winner — scores compose across N>2 candidates and give tie-break logic we control in code.
2. **Position-bias control:** run the comparison twice with candidate order swapped; disagreement between the two runs IS the "close margin" signal (replaces the model's self-reported margin).
3. **Few-shot exemplars:** embed 3–5 of Dan's labeled cases (BEFORE + his best pick + a rejected one + his one-line reason) as vision few-shot examples in the judge prompt. This is the "training" — iterate the exemplar set as labels accumulate. Hold out the exemplar cases from the eval so you're not scoring on the training examples.
4. **Judge-model bake-off:** evaluate `claude-sonnet-5` vs a stronger Claude (whatever is current-best — Opus 4.8 is the flagship as of this handoff; confirm the exact model string) on agreement-with-Dan. Judge cost is pennies vs image cost, so if a bigger judge buys accuracy, take it.

**Step 4 — Validate:** target ≥80% agreement with Dan on his "best" cases (exclude the 2 "no best" max cases, or treat "judge also finds nothing clearly best" as correct there). Keep `labels.json` as the permanent regression eval. Report the before/after agreement numbers to Dan with a couple of concrete example flips (cases where the old judge picked the too-muscular one and the new judge picks Dan's).

**Step 5 — Only after the judge beats baseline:** write the Phase-4 handoff (ship the new judge to `server.js` + do the prompt fixes: neutralize the SKIN TONE tan block at `public/index.html` ~3063–3066, shrink/remove the muscle anchors ~2999–3036 / `MUSCULARITY ANCHOR TABLE`, add Kino language; live-verify; watch PostHog). Do NOT ship in Phase 3.

## Things to Avoid / Lessons Learned

- **Never pass `temperature`/`top_p`/`top_k` to Claude 5-family models** — hard 400, and the judge fails open (silently serves Gemini), so a broken judge is invisible without checking Railway logs. This cost a full day once.
- **Never add a `deviceId` to a harness request** — spends real credits + commits a data file. The harness deliberately omits it.
- **Gemini/Claude self-checks pass "identical-looking" images at first glance** — trust the rubric + eyeball the actual images, don't trust a single yes/no.
- **The blind key must stay authoritative** — always decode letter→model via `key.json`; letters are reshuffled per case, so A in one case ≠ A in another.
- **Replicate has no balance API** — throttling under ~$5 silently degrades runs; check replicate.com/account/billing before any re-generation and enable auto-reload. No `402`/`429` seen during the round-1 batch, so there was balance then.
- **The 2 "no best" max cases are a real product ceiling, not a labeling gap** — don't build a judge that's forced to pick a winner there; "nothing is clearly best" is the correct verdict, and it's the signal that Phase 4's intensity/prompt work is needed.
- **Don't confound judge changes with prompt changes** — Phase 3 touches the judge only. The condensed-prompt / tan / muscle-anchor fixes are Phase 4.

## Relevant Files & Locations

- **Judge (to baseline + rebuild):** `server.js` — `judgeCandidates` ~2319–2375, routing ~2383–2410, telemetry ~2549–2555. Judge model `claude-sonnet-5`. Judge-fix history: commit `e39ac7c` (removed the fatal `temperature:0`).
- **Ground truth + harness:** `bakeoff/round1/labels.json`, `bakeoff/round1/key.json`, `bakeoff/round1/results.json`, `bakeoff/round1/images/` (gitignored, local), `bakeoff/adapters.js`, `bakeoff/runner.js`, `bakeoff/prompts.js`, `bakeoff/README.md`.
- **Prompt (Phase 4, not Phase 3):** `public/index.html` — SKIN TONE RULES ~3061–3066 (`bronze tan` line), `MUSCULARITY ANCHOR TABLE` ~3011–3013, `[[MUSCLE_*]]` blocks ~2999–3036, `muscleAxisPlan()` ~3141, `condenseForKontext` in `server.js` ~2177.
- **Parent handoff:** `handoff-20260724-model-bakeoff-v2.md` (§3 judge methodology, §4 aesthetic/prompt work).
- **Coordination:** `AI_COORDINATION.md` → active task "Extended model bake-off v2" (has the full Phase 1/2 result + label findings).
- **Env vars (names only):** `GEMINI_API_KEY`, `REPLICATE_API_TOKEN`, `ANTHROPIC_API_KEY` (Railway service `abs-by-ai`, project `invigorating-liberation` / `f44b4c7e-...`). Railway CLI at `~/.npm-global/bin/railway` (not on PATH), authenticated.
- **Memory:** `bakeoff-round1-aesthetic.md` (Dan's aesthetic + condensed-prompt finding).

## Model & Effort Recommendation

This task touches the Anthropic judge integration code AND requires vision-based image-quality judgment against a taste rubric — **always-Claude** (Codex is a poor fit for both, regardless of usage). Pick the cheapest Claude that does it well:

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Opus 4.8, extended thinking.** The judge-prompt/rubric design is the genuinely hard, expensive-to-get-wrong part of this whole project, and the work is vision-heavy — worth Opus. |
| **If Claude usage is high / approaching a limit** | **Claude Sonnet 5, standard thinking** for Step 1 (baseline) and the mechanical eval-harness plumbing (routine); escalate to Opus only for the Step 2–3 rubric/exemplar design if Sonnet's judge can't clear 80%. Fable is a reasonable middle tier if available — double-check its pricing/availability at the time (it has changed before). |

Note: the *judge model under test* (Step 3's judge-model bake-off, claude-sonnet-5 vs Opus) is a separate axis from the model you run the session on — don't conflate them.

## Starter Prompt for the Next Task

> Execute `handoff-20260725-bakeoff-phase3-judge-rebuild.md` (project root) — Phase 3 of the Abs By AI model bake-off: rebuild the generation judge to match Dan's labeled taste. Read that doc first, plus `handoff-20260724-model-bakeoff-v2.md` §3 for the judge methodology. Dan's ground-truth labels are in `bakeoff/round1/labels.json`, decoded via `bakeoff/round1/key.json`; candidate images are in `bakeoff/round1/images/` (regenerate with `node phase2.js` from `bakeoff/` if missing). Start with Step 1: baseline the CURRENT production judge (`server.js` `judgeCandidates` ~2319, `claude-sonnet-5`, no temperature — copy it exactly) against Dan's labels and report the agreement number. Then rebuild the judge around the confirmed aesthetic — shredded/defined, NOT bulky, NO tan (labels: 33 "too muscular", 23 "too tan", 20 "looks fake"), with per-candidate rubric scores, a position-bias order swap, and few-shot exemplars from Dan's best picks — and hit ≥80% agreement before changing any production code. Do NOT touch the generation prompt (tan block / muscle anchors) — that's Phase 4. No `deviceId` on any harness request.
