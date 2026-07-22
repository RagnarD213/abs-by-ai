# Handoff: Generation Overhaul — Revert Softening, Subtle/Ripped Consolidation, Two-Model Ensemble

**Date:** 2026-07-22
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Adoption + profitability — "the after looks the same as the before" is the single failure mode that kills the product's core promise. Dan: "If people go in and their after is the same as the before, our app has no purpose."

## Objective

Three-phase overhaul of the transformation image pipeline, in this order:

1. **Phase 1 — Revert the prompt softening and put the prompt on a diet.** Transformations measurably regressed after the July 21 changes. Restore the stronger framing Dan already approved, cut the bloated hedging language, and fix the misdirected retry preambles.
2. **Phase 2 — Consolidate the UI to two options: "Subtle" and "Ripped".** Remove the Realistic 90-day toggle entirely. Subtle = today's `dramatic` prompt internals. Ripped = `max`, pushed as hard as the model allows.
3. **Phase 3 — Two-model ensemble.** Generate from Gemini AND FLUX.1 Kontext in parallel, have Claude judge (identity gate + drama comparison), auto-pick clear winners, and show a "Which future you?" chooser for borderline cases.

Every phase = its own commit(s) + push + Railway deploy + live verification on absbyai.com with the fixed proof photos + **Dan eyeball before the next phase ships**. Nothing ships on the implementer's judgment alone — that is how the regression happened.

## Current State

**The regression is real and measured.** PostHog `generation_verifier` telemetry (queried 2026-07-22):
- 2026-07-21: male `moderate/max` passed the change-verifier first try **5/5**, 0 retries.
- 2026-07-22: **every** male generation (heavier/max, moderate/dramatic, moderate/max) failed the verifier first try AND stayed `weakChange:true` after both forced retries. Dan's own re-tests of previously-used photos confirm the images are visibly worse.

**Three diagnosed causes:**

1. **Commit `ca2e5b9` (July 21, "aesthetic retarget") softened the prompt.** It cut male muscle targets ~⅓ (max +15 lb → +10 lb) and replaced the "visibly BIGGER / unmistakably different" PRIMARY-AXIS RULE with a hedged SHREDDED-AESTHETIC RULE ("modest muscle", "never thick", "supporting detail"). Dan had eyeballed the pre-`ca2e5b9` (+15 lb) version that same day and called Lean+Peak "significantly better." The retarget was chasing one hard selfie photo; it softened the ask for everyone.
2. **Prompt bloat.** `SYSTEM_PROMPT` in `public/index.html` (lines ~2884–3043) is ~5,000 chars, dominated by restraint: PRESERVE EXACTLY, FRAMING, giant AVOID list, "never bulky/blocky/veins" repeated in 6+ places. An edit model told 40 ways not to change things and 5 ways to change them returns the input photo. Our own AI_COORDINATION.md lesson (July 21): "added-region specificity competes with, rather than adds to, overall transformation magnitude."
3. **Misdirected retries.** The male intensify preambles in `server.js` (~line 2197) demand a "contest-lean shredded six-pack" for ALL males — including heavier/moderate subjects. The A3.1 investigation (July 18) proved Gemini refuses that ask on heavier bodies regardless of prompt strength, so those retries burn Gemini calls and change nothing.

**What exists and works (do not break):**
- Verifier + intensify-retry ladder in `server.js` `/api/generate-image` (~lines 2100–2223): gender/condition-aware Haiku YES/NO check, `rungBudget` (female 2, male dramatic/max 2, male moderate 1, male subtle 0), fail-open on errors, runs **before** `cacheAttempt` so retries never re-charge a credit, `weakChange` flag → client "Make it more dramatic" nudge.
- `GEN_TELEMETRY` Railway logs + PostHog `generation_verifier` events (verifierRan, verifierPassedFirstTry, retryRungsUsed, finalVerifierPassed, weakChange, sex, startCondition, intensity).
- Muscle-axis marker system: `[[MUSCLE_*]]` blocks physically stripped by `applyMuscleAxis()`/`muscleAxisPlan()` (index.html ~3070–3106) — deterministic scoping because prose scope-limits provably don't hold.
- `max_tokens: 2048` on `/api/generate-prompt` + `PROMPT_TRUNCATED` log (commit `8a7c4a4`) — a 1024 cap silently truncated guardrails once already.
- FEMALE HEAVIER REALISM RULE (Gemini model ceiling on heavier female bodies — keep; it was Dan's explicit Option A choice).
- "Fix my result" edit pass, share card, transformations gallery with before/after slider (reusable for the Phase 3 chooser).

## Key Decisions Already Made (do not relitigate)

- **Button names: "Subtle" and "Ripped".** Dan's exact choice, 2026-07-22.
- **Subtle maps to the current `dramatic` prompt tier; Ripped maps to `max` pushed as hard as possible.** The old subtle/moderate tiers die with the 4-option picker.
- **Realistic 90-day toggle is removed entirely** (UI + `REALISTIC_SYSTEM_PROMPT`). Dan: nobody wants it; dramatic is already too subtle.
- **Restore the stronger "+15 lb / visibly BIGGER / unmistakably different" energy for Ripped.** Dan verified it looked significantly better before `ca2e5b9` softened it.
- **Second model is FLUX.1 Kontext** (not gpt-image-1 first — OpenAI is stricter about editing photos of real people, which risks a new class of blocked results). gpt-image-1 is the fallback candidate if Kontext disappoints.
- **Cross-model best-of-2, not same-model best-of-2.** Telemetry proved Gemini's failures are photo-specific (same photo fails retry after retry), so two Gemini samples buy two copies of the same refusal. Approved cost: ~8–10¢/generation total (vs ~4¢ today).
- **Judge rules:** clear winner (passes identity + photoreal + clearly more dramatic) → auto-pick, single result, no chooser. Identity *clearly broken* → that image is never shown, no exceptions. Identity "slightly off / unsure" OR both good and near-equal → show the chooser; the user is the best judge of their own face.
- **Chooser presentation:** "Which future you?" screen — before photo small at top for reference, two version cards side by side, tap a card → full-screen with the existing before/after slider, "Keep this one" per card. Chosen image becomes THE result (share/save/gallery as today); the other is discarded. One credit covers the whole generation.
- **Paywalled/out-of-credits results: NO chooser.** Show the judge's best pick behind the existing locked/teaser flow, exactly as today. (The "unlock to pick your favorite" conversion hook was considered and deferred — revisit only after the simple version ships.)
- **Phase order: 1 → 2 → 3.** Revert the damage first (fastest win), then UI, then ensemble.
- **Verification method: fixed proof photos, side-by-side old vs new, Dan eyeballs before each phase ships.**

## Detailed Plan

### Phase 1 — Prompt revert + diet (client `public/index.html`, server `server.js`)

1. **Re-strengthen the muscle axis.** In `SYSTEM_PROMPT` (~2884–3043): restore the pre-`ca2e5b9` magnitude for dramatic/max — muscle anchor table back to subtle +5 / moderate +8 / dramatic +12 / max +15 lb (see commit `5943874` for the original language via `git show 5943874`), and restore the "visibly BIGGER... unmistakably different" directive framing for male fit/very_lean. KEEP the six-pack requirement `ca2e5b9` added (it's good) — the fix is adding the size/mass demand back, not removing the leanness demand.
2. **Cut the prompt hard.** Target roughly half the current length. Principles: state each guardrail ONCE (the "never bulky/veins" idea currently appears 6+ times); collapse the AVOID list to essentials; keep PRESERVE EXACTLY + FRAMING + SKIN TONE + safety rules intact but tight; the transformation directive must be the loudest, longest part of the prompt. Keep the `[[MUSCLE_*]]` marker mechanism and `muscleAxisPlan()` gating exactly as-is.
3. **Fix the male retry preambles** (`server.js` ~2197): make them condition-aware. Heavier/moderate males get a "major, whole-body fat loss + visibly more muscle" push; only fit/very_lean males get the "shredded contest-lean six-pack" language. Female preambles unchanged.
4. **Verify:** `node --check` on extracted JS; then on **prod** (local env has dummy AI keys) run the fixed proof photos (`public/img/proof/`: male-before, male-after = already-lean hard case, male2-before = heavier male, female-before) through `/api/generate-prompt` (confirm full prompt, no truncation, guardrails present, correct scoping across ≥6 gender/condition/intensity combos) and `/api/generate-image` end-to-end. Save before/after comparison images for Dan. **STOP for Dan's eyeball before Phase 2.**

### Phase 2 — Subtle/Ripped consolidation + Realistic removal (mostly `public/index.html`)

1. Delete the Result-style toggle: `#modeGrid` markup (~1547), its `selectPick` wiring (~3976), `state.mode`, `REALISTIC_SYSTEM_PROMPT` (~3057), and the `result_mode_selected` PostHog event. `goalSystemPrompt()` always uses `GOAL_SYSTEM_PROMPT`.
2. Replace the 4-card `#intensityGrid` (~1512) with 2 cards: **Subtle** (`data-value="dramatic"`) and **Ripped** (`data-value="max"`, default active). Simplest safe route: keep internal intensity values `dramatic`/`max` so the server, verifier `rungBudget`, telemetry, and body-fat anchor tables all keep working unchanged; only the UI vocabulary changes.
3. Update every ripple: `INTENSITY_LADDER` → `['dramatic','max']` (the "Make it more dramatic" / weakChange nudge becomes Subtle→Ripped; at Ripped there is no stronger step — keep the existing behavior of not showing a nudge, since Phase 3's ensemble is the real fix there); default `state.intensity`/`effectiveIntensity`; result-card copy + displayed body-fat numbers; paywall headline tier names; any copy strings naming "Peak"/"Dramatic".
4. Server back-compat: old cached clients may still send `subtle`/`moderate` — the server must keep accepting them (it already does; just don't remove those branches).
5. Verify in-browser locally (picker renders, both selections generate the right prompt tier, nudge gating, no console errors) and live on absbyai.com. **Dan eyeball.**

### Phase 3 — Two-model ensemble + judge + chooser (server + client)

1. **FLUX.1 Kontext integration** (`server.js`): new env var (e.g. `BFL_API_KEY` via api.bfl.ai, or `REPLICATE_API_TOKEN` — implementer picks the least-ops option; verify current pricing, ~4–8¢/image expected). New helper `callFluxKontext(prompt, photoBase64)` mirroring `callGemini`'s contract (returns `{ok, imageBase64, imageMime}`), with an AbortController timeout (the Supplement Audit hang lesson — never an unbounded await).
2. **Parallel generation** in `/api/generate-image`: `Promise.allSettled([callGemini(prompt), callFluxKontext(prompt)])`. If one fails/times out, proceed single-model exactly as today (reliability strictly improves, never degrades). Kontext may need a condensed prompt variant — it takes shorter instructions than Gemini; the implementer should test whether the full assembled prompt works or a trimmed version renders better.
3. **Claude judge** (one call, Sonnet-class for vision quality; Haiku if testing shows it's sufficient): inputs = BEFORE + candidate A + candidate B. Output (strict JSON): per-candidate `identity` (`good` | `borderline` | `broken`) and `photoreal` (bool), plus `winner` and `margin` (`clear` | `close`). Routing: any `broken` → that candidate is discarded, never shown. One survivor → single result. Two survivors + `clear` → winner as single result. Two survivors + (`close` OR either is `borderline`) → chooser. Fail-open: judge error → ship Gemini's image through the existing verifier ladder as today.
4. **Keep the existing verifier ladder as the safety net** for whatever single image ships (unchanged); when the chooser fires, skip the ladder (two candidates that survived the judge don't need a forced retry).
5. **Chooser UI** (`public/index.html`): "Which future you?" screen per the approved mockup — small before-photo reference at top, two cards, tap → full-screen compare reusing the gallery's before/after slider, "Keep this one" buttons. Chosen image flows into the existing result screen/state (share, save, gallery, fix-my-result all operate on the chosen image). **Locked results bypass the chooser** — judge's best goes into the existing locked/teaser flow.
6. **Telemetry:** extend `GEN_TELEMETRY` + PostHog: `models_run`, `judge_verdict`, `judge_winner`, `chooser_shown`, `chooser_choice` (which model the human picked), per sex/condition/photo. This is the standing model bake-off — after a few weeks it answers which model wins per segment.
7. **Credits:** one credit per generation regardless of candidates; both model calls happen before `cacheAttempt` (same invariant as the retry ladder).
8. Verify end-to-end on prod with all proof photos: both-models path, one-model-down path, judge JSON parsing, chooser flow at 375×812, locked-user path, no double credit charge. **Dan eyeball + final AI_COORDINATION.md reset.**

## Things to Avoid / Lessons Learned

- **Do not chase a single hard photo by softening the global prompt** — that exact move (`ca2e5b9`) caused this regression. Hard photos are Phase 3's (ensemble) and photo-guidance's problem.
- **Prose scope-limits in the system prompt do not hold** (proven twice: trainer leg-press rule, muscle-axis scoping). Any conditional prompt section must be enforced in code (`[[MUSCLE_*]]`-style markers or server-side assembly), never by "only apply this when…" instructions.
- **Gemini has a hard ceiling on heavier female bodies** (A3.1, four techniques all failed). Keep the FEMALE HEAVIER REALISM RULE. Kontext may beat this ceiling — that's a Phase 3 telemetry question, not a prompt question.
- **`max_tokens` on `/api/generate-prompt` stays at 2048** — 1024 silently truncated the guardrails mid-AVOID once. Watch for `PROMPT_TRUNCATED` in Railway logs after any prompt edit.
- **Local env has dummy Gemini/Anthropic keys** — transformation quality can only be judged on prod. Budget for real generations on the proof photos (~4–10¢ each).
- **Retries/candidates must run before `cacheAttempt`** so nothing ever double-charges a credit.
- **Adding region-specific detail (e.g. "lower belly") crowds out whole-body change magnitude** (a255f41 → reverted in 323135e). Keep the directive whole-body.
- **The verifier stays fail-open** — never block a paid generation on a checker hiccup.
- Angled/arm-obscured selfies defeat every prompt technique (telemetry-proven). If Phase 3 still leaves them weak, the fix is upfront photo guidance ("full torso, front-on, arms down"), not more prompt force — noted as a fast-follow, not in this handoff's scope.

## Relevant Files & Locations

- `public/index.html` — `SYSTEM_PROMPT` ~2884–3043; `GOAL_SYSTEM_PROMPT`/`REALISTIC_SYSTEM_PROMPT` ~3045–3063; muscle-axis markers/`muscleAxisPlan()` ~3070–3106; `#intensityGrid` ~1512; `#modeGrid` ~1547; picker wiring ~3969–3980; `INTENSITY_LADDER`/nudge ~8842–8898; generation entry ~8804.
- `server.js` — `/api/generate-image` verifier + ladder ~2100–2300 (`buildVerifierQuestion` 2103, preambles ~2193, `rungBudget` 2183, `weakChange` 2223); Gemini call ~2047 (`gemini-2.5-flash-image`); `/api/generate-prompt` max_tokens guard.
- Proof photos: `public/img/proof/` (male-before/after, male2-before/after = heavier male, female-before/after).
- Key commits: `5943874` (strong +15 lb language to restore), `ca2e5b9` (the softening — prime revert target), `18e8461` (comparative verifier — keep), `77d52fe` (lighting/sheen — keep), `323135e` (region-specificity lesson).
- Env vars (names only): `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, new `BFL_API_KEY` or `REPLICATE_API_TOKEN` (Railway).
- Telemetry: PostHog project 458833, event `generation_verifier`; Railway logs `GEN_TELEMETRY`.
- Deploy: push to `main` → Railway auto-deploy → verify on https://absbyai.com.

## Model & Effort Recommendation

This task edits the Anthropic prompt/verifier code and lives or dies on image-quality judgment — it's in the **always-Claude** category (and AI_COORDINATION.md already assigns transformation-prompt work to Claude, not Codex).

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Phases 1 & 3: Claude Opus, extended thinking (quality-critical prompt engineering + new provider integration + judge design). Phase 2: Claude Sonnet 5, standard thinking (mechanical UI consolidation). |
| **If Claude usage is high / approaching a limit** | Phases 1 & 3: Claude Sonnet 5 with extended thinking — do NOT hand these to Codex (Anthropic-integration + quality-judgment work). Phase 2 only: Codex flagship, medium effort, is acceptable — it's well-specified single-file UI work with no Anthropic-code contact; record a handoff in AI_COORDINATION.md if so. |

Fable (metered) is a reasonable middle option for Phases 1 & 3 if session limits bite — double-check current pricing/availability first.

## Starter Prompt for the Next Task

> Read `handoff-20260722-generation-overhaul.md` in the Abs By AI project root and execute it phase by phase. Also read `AI_COORDINATION.md` first per project rules and set yourself as owner with status `Implementation in progress`. Start with Phase 1: run `git show 5943874` and `git show ca2e5b9` to see the strong-vs-softened prompt language, then rebuild `SYSTEM_PROMPT` in `public/index.html` per the Phase 1 steps (restore +15 lb magnitude for Ripped-tier males, keep the six-pack requirement, cut total prompt length ~in half, keep the `[[MUSCLE_*]]` marker system) and fix the male retry preambles in `server.js` ~2197 to be condition-aware. Each phase: own commit(s), push to main, verify on absbyai.com with the proof photos in `public/img/proof/`, then STOP for Dan's eyeball before the next phase. Do not soften the prompt to chase any single difficult photo — that caused the original regression.

