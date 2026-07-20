# Handoff: Lean/fit male transformations — add a muscle axis, fix the verifier, drop the Realistic toggle

**Date:** 2026-07-20
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Profitability first (this is the core product promise failing at the top of the funnel — a user whose "after" looks like their "before" does not convert and is a refund risk), then adoption.

## Objective

Fix the "the after looks the same as the before" failure **for lean and fit MALE subjects**. Dan tested on 2026-07-20 with his own photo at Lean + Peak (`very_lean` / `max`) and got a near-identical result. This is a *different* problem from the heavier-female failure investigated on 2026-07-18 — that one was a genuine Gemini model ceiling. **This one is our own spec: we are asking Gemini for a tiny change and it is delivering it faithfully.**

Three code-confirmed causes, to be fixed in order:
1. The transformation is specified purely as a body-fat drop, so a lean user is asked for a 2–4 point change (11–13% → 9%) — almost invisible on a real body.
2. There is **no muscle/size dimension anywhere in the prompt**, but "dream physique" for an already-lean man means *bigger*, not *skinnier*.
3. The change-verifier's safety net asks a non-comparative question, so it trivially passes on anyone who already has visible abs — the retry ladder never fires for exactly the users who need it.

Plus a product decision: **remove the Realistic 90-day toggle.**

## Current State

Everything below is live on absbyai.com and working as designed — nothing is half-built or broken. The problem is the design itself.

- **`public/index.html`** holds the prompt-engineering layer. `SYSTEM_PROMPT` (line ~2837) is the base; `GOAL_SYSTEM_PROMPT` (line ~2970, "Dream", the default) and `REALISTIC_SYSTEM_PROMPT` (line ~2982) are `.replace()` variants of it that swap only the CALIBRATION RULE block. `goalSystemPrompt()` (line ~2991) picks between them off `state.mode`.
- **BODY-FAT ANCHOR TABLE** (line ~2878) is the entire specification of intensity: `MALE: subtle 15-17%, moderate 12-14%, dramatic 9-11%, max 8-10%. FLOOR 8%.` There is no second axis.
- **`BF_BEFORE` / `BF_AFTER`** (lines 2783–2784) drive the "Estimated body fat 11–13% → 9%" card via `updateBodyFatDisplay()` (line ~3532).
- **Starting condition is user-selected**, not auto-detected — the "Where you are now" picker at line ~1476 (`heavier` / `moderate` / `fit` / `very_lean`, labelled Heavier / Average / Fit / Lean).
- **`server.js`** holds the image call and the safety net. `buildVerifierQuestion(who, intens)` at line ~2090, `looksChanged()` at ~2102, and the intensify-retry ladder at ~2162 (rung budget: female = 2 every intensity; male = 2 at dramatic/max, 1 at moderate, 0 at subtle).
- **Result style toggle** markup at line ~1543 (`#modeGrid`), wired at line ~3849 with a `result_mode_selected` PostHog event.

### The three defects, precisely

**1. Lean subjects get the smallest transformation.** Starting at Average (20–24%) and asking for Peak (8–10%) is a ~12-point drop and renders dramatically. Starting at Lean (11–13%) and asking for Peak is a 2–4 point drop. The app does *less* the fitter you are — backwards from what a user tapping "Peak" expects.

**2. No muscle axis.** The prompt is entirely fat-loss framed ("reduce", "tighten", "carve", "define") with a body-fat % target. Two bullets in the MALE section ask for wider shoulders and bicep peak, but nothing instructs Gemini to add **mass**. A lean man has no fat left to shave, so there is nothing for the model to do.

**3. The verifier passes trivially on lean subjects.** `server.js:2098` (male, dramatic/max) asks: *"is there CLEARLY VISIBLE ab muscle definition (actual separation lines on the stomach…) AND a visibly tighter/more tapered waist compared to the BEFORE photo?"* The ab clause has **no comparative anchor** — for a man who already has abs the answer is YES from the before photo alone. The verifier passes, no retry fires, and a no-op ships. The waist clause is comparative but the checker answers the question as a whole. This is why the A2 retry ladder (built 2026-07-18 and working correctly for women) did not save this case.

## Key Decisions Already Made

- **This is a spec problem, not a model ceiling.** Do NOT go down the model-swap path (FLUX / gpt-image-1 / SD inpainting) for this task — that research remains open for the *heavier-female* case only. Gemini renders what it's asked here; fix the ask.
- **Add muscularity as a second dial rather than pushing body fat lower.** Dropping the male floor below 8% is unhealthy-looking, unrealistic, and still wouldn't produce a visible change. Mass is the axis that's missing.
- **For fit/very_lean subjects, intensity should primarily drive muscle, not fat.** For heavier/moderate subjects fat loss stays the dominant axis — those already work well and must not regress.
- **The result card must stop advertising a tiny change.** "11–13% → 9%" tells a lean user the change will be small before they even look at the image. For fit/lean, show a build change instead.
- **Remove the Realistic 90-day toggle.** Two reasons: (a) Realistic tempers *every* starting condition down one step, so Lean + Peak lands on "fit" — where the user already is. It is mathematically guaranteed to be a no-op for exactly the complaining users. (b) The product hook is "meet the new you"; offering a less-impressive option immediately before the paywall works against conversion. **Hide the UI, leave the code path dormant** — a one-line revert if Dan wants it back.
- **Ship order is fixed: muscle axis → verifier → toggle.** The muscle axis changes image output for every fit/lean user and carries the real regression risk, so it gets isolated and eyeballed first.
- **Female behavior must not regress.** The 2026-07-18 work (gender-aware verifier, female anchors, FEMALE HEAVIER REALISM RULE) is live and validated. Do not touch female prompt paths or the female verifier questions in this task.

## Detailed Plan

Each step is its own commit, pushed to `main`, deployed via Railway, and live-verified on absbyai.com before the next step starts. Per `AGENTS.md`, commit/push/deploy/verify are part of completing each step, not a separate request.

**Local testing caveat:** the local environment has dummy Gemini/Anthropic keys, so **image quality can only be judged on production**. Local checks are limited to `node --check`, page-parses-clean, and prompt-string assertions (e.g. "does the generated prompt contain the mass language for this input combination").

### Step 1 — Muscle axis for fit/lean males (the main fix, highest regression risk)

In `public/index.html`, inside `SYSTEM_PROMPT`:

1. Add a **MUSCULARITY ANCHOR TABLE** next to the existing BODY-FAT ANCHOR TABLE (line ~2878), expressed in terms Gemini can render visually — added lean mass plus the specific structures that read at a glance (chest fullness, shoulder cap size, lat width, arm thickness, upper-back thickness). Scale it by intensity.
2. Add a rule that when `subject_current_condition` is `fit` or `very_lean` AND `subject_gender` is `male`, **muscularity becomes the primary axis and body fat the secondary one**. The directive must demand visible added mass, not just sharper lines. Target for Lean + Peak: 8–10% body fat **and** a fitness-cover build — visibly fuller chest, rounder/wider delts, wider lats, noticeably thicker arms, roughly 15 lb more lean mass.
3. Strengthen the existing fit/very_lean male sentence at line ~2866 — it currently asks only for *more definition* ("twice the visible definition", "sharp cuts", "serratus"). It needs the mass language too.
4. Keep the existing AVOID guardrails intact: no veins/vascularity, no comically oversized or cartoonish proportions, no spray-on abs. The target is a fitness-cover model, **not** a bodybuilder.
5. Do not change the heavier/moderate male path or any female path.

Also update the result card:

6. In `updateBodyFatDisplay()` (line ~3532), for male + `fit`/`very_lean`, show a build headline instead of a body-fat delta (e.g. "Lean → Fitness-model build"). This may need a small markup change around `bfBefore`/`bfAfter` — check the surrounding HTML. Heavier/moderate and all female cases keep the existing body-fat display, including `BF_AFTER_HEAVIER_FEMALE`.

**Verify:** on absbyai.com with Dan's real photo at Lean + Peak. Confirm the generated prompt contains the mass language, the returned image shows visibly more muscle (not just sharper abs), identity/face/pose/framing are preserved, and no vascularity or cartoonish bulk. Then regression-check one Average + Peak male generation to confirm the heavier path is unchanged. **Stop here for Dan's eyeball before Step 2.**

### Step 2 — Make the verifier comparative

In `server.js`, `buildVerifierQuestion()` (line ~2090), male branch only (lines 2097–2099):

1. Rewrite the strong (dramatic/max) question so **every clause is a comparison against the BEFORE photo** — "is the after *more* defined / *more* muscular than the before", never "is there definition". Explicitly instruct that a subject who already had visible abs in the before photo must show a clear *increase*, and that an image that could be mistaken for the before is NO.
2. Include muscle mass in the question, matching Step 1 — fuller chest, wider shoulders, thicker arms — so the check measures what we now actually ask for.
3. Leave the non-strong male question and **both female questions unchanged.**
4. Leave `rungBudget`, fail-open behavior, and the pre-`cacheAttempt` placement exactly as they are — retries must never re-charge a credit.

**Verify:** on prod, re-run Lean + Peak and read the `GEN_TELEMETRY` line in Railway logs. Confirm `verifierRan: true` and that a weak result now produces `verifierPassedFirstTry: false` with retries firing, where before it passed. A good result should still pass first try (confirm it isn't over-firing and burning Gemini calls — that costs money).

### Step 3 — Remove the Realistic 90-day toggle

In `public/index.html`:

1. Hide the `#modeGrid` pick-group (line ~1543). Prefer commenting out the markup block over deleting it.
2. Leave `state.mode = 'dream'` (line ~2818), `REALISTIC_SYSTEM_PROMPT`, and `goalSystemPrompt()` in place and untouched — dormant, so restoring is one line.
3. The `result_mode_selected` PostHog capture at line ~3852 becomes dead with the UI hidden; leaving it is harmless.

**Verify:** on absbyai.com — toggle gone, generation still works and still uses the Dream prompt, no console errors.

### OPEN questions

- **OPEN:** Should `fit` (15–17%) get the full muscle treatment or a softer version than `very_lean`? Recommendation: apply it to both, scaled — `fit` still has some fat to lose so it can use both axes, while `very_lean` is nearly all muscle. Confirm with the live result.
- **OPEN (deferred, do not action here):** starting condition is self-selected. Dan chose "Lean" for a photo that may read closer to "Fit". A wrong self-assessment shifts the whole target. Auto-detecting or sanity-checking the condition from the photo is a possible follow-up, but the muscle axis should make the app robust to it — a *lean* man and a *fit* man both get a real change. Don't bundle it.

## Things to Avoid / Lessons Learned

- **Don't chase this with a lower body-fat number.** The floor is 8% male for good reason; going lower produces a gaunt, unhealthy result and still wouldn't create a visible change on someone at 12%.
- **Don't reach for a different image model here.** Established 2026-07-18: Gemini's ceiling is real for *heavier* bodies, and four aggressive techniques (forceful BF% prompting, compound second pass, weight-loss reframing, re-leaning pass 1 alone) all failed there. None of that applies to lean subjects — Gemini complies fine, we just asked for very little.
- **A near-identical output can be a correct output.** Before assuming the model is refusing, check what the prompt actually asked for. That's the trap this whole task came out of.
- **Verifier questions must be comparative.** Presence checks ("is there X?") silently pass on subjects who already had X. This is the general lesson — apply it if any new verifier is ever added.
- **Prompt rules alone don't reliably hold.** Noted elsewhere in this codebase (the trainer's leg-press rule failed prompt-only enforcement). If the muscle axis proves unreliable across generations, consider a server-side re-check after the model responds rather than just adding more prompt text.
- **Image quality cannot be judged locally** — dummy API keys. Every quality judgment happens on absbyai.com.
- **A single proof photo proves the mechanism, not the calibration.** The A2 work passed on one synthetic photo and still needed real-photo tuning. Expect the same here; Dan's eyeball on real photos is the actual acceptance test.
- **Don't sweep unrelated files into these commits** — the repo root has many untracked handoff/asset files. Commit only the files each step touches.

## Relevant Files & Locations

| What | Where |
|---|---|
| Prompt layer, anchors, result card, toggle UI | `public/index.html` |
| — `SYSTEM_PROMPT` | ~line 2837 |
| — BODY-FAT ANCHOR TABLE | ~line 2878 |
| — fit/very_lean male directive | ~line 2866 |
| — `GOAL_SYSTEM_PROMPT` / `REALISTIC_SYSTEM_PROMPT` / `goalSystemPrompt()` | ~lines 2970 / 2982 / 2991 |
| — `BF_BEFORE` / `BF_AFTER` | ~lines 2783–2784 |
| — `updateBodyFatDisplay()` | ~line 3532 |
| — "Where you are now" picker | ~line 1476 |
| — Result style toggle markup / wiring | ~line 1543 / ~line 3849 |
| Verifier + retry ladder | `server.js` |
| — `buildVerifierQuestion()` | ~line 2090 |
| — `looksChanged()` | ~line 2102 |
| — intensify-retry ladder + `rungBudget` | ~line 2162 |
| Live site | https://absbyai.com |
| Deploy | Railway, auto-deploys from GitHub `main` |
| Telemetry | Railway logs, `GEN_TELEMETRY {…}`; PostHog event `generation_verifier` |
| Env vars (names only) | `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` |
| Prior context | `AI_COORDINATION.md` (A1–A3.1 history), `handoff-20260718-female-dramatic-and-items-3-7.md` |

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Opus, extended thinking**, for Steps 1 and 2. This is prompt engineering against a model whose behavior we've repeatedly misjudged, it directly touches the Anthropic API verifier code, and the output quality *is* the product. Step 3 is trivial — drop to Sonnet 5 or just do it inline. |
| **If Claude usage is high / approaching a limit** | **Claude Sonnet 5, standard thinking.** Steps 1–2 stay on Claude regardless (see override). The plan above is specified concretely enough that Sonnet can execute it. Step 3 (hiding one markup block) is genuinely routine and is fine on Codex mini-tier, low effort, if you want to spend nothing on it. |

**Task-type override:** Steps 1 and 2 are **always-Claude regardless of usage** — Step 2 modifies the Anthropic API integration (`looksChanged` / `buildVerifierQuestion`), and Step 1 is a brand-voice-adjacent quality decision where being wrong is expensive to unwind (it changes the image every fit/lean user sees). Only Step 3 is safe to hand to Codex.

Fable is a reasonable middle ground on cost between Sonnet and Opus if you'd rather not spend Opus budget here — double-check its current pricing and availability before relying on it, since that has changed before.

## Starter Prompt for the Next Task

> Read `handoff-20260720-lean-male-muscle-axis.md` in the project root — it has the full diagnosis and plan. Short version: lean/fit **male** transformations come back looking identical to the input because our prompt specifies the transformation purely as a body-fat drop, so a user starting at 11–13% who taps "Peak" is only asked for a ~3-point change. Gemini renders that faithfully. This is our spec, not a model ceiling — do not go down the model-swap path.
>
> Implement the three steps in the handoff **in order**, each as its own commit, pushed to `main`, deployed, and live-verified on absbyai.com before starting the next: (1) add a muscularity axis to `SYSTEM_PROMPT` in `public/index.html` so intensity drives added muscle mass — not just leanness — for fit/very_lean males, and update the result card so it stops advertising a 3-point body-fat drop to lean users; (2) rewrite the male dramatic/max verifier question in `server.js` (~line 2090) so every clause compares against the BEFORE photo, since the current presence-check ("is there visible ab definition?") trivially passes on anyone who already has abs and so the retry ladder never fires for them; (3) hide the "Result style" Realistic 90-day toggle (`#modeGrid`, `public/index.html` ~line 1543), leaving the code path dormant for easy revert.
>
> **Start with Step 1, then stop and report** — Dan needs to eyeball the live result on his real photo before Step 2, because Step 1 changes the image for every fit/lean user. Note that image quality cannot be judged locally (dummy API keys); all quality verification happens on absbyai.com. Do not touch any female prompt path or the female verifier questions — that work shipped 2026-07-18 and is validated. Also update `AI_COORDINATION.md` when you pick this up.
