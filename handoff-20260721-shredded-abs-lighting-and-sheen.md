# Handoff: Shredded abs — stop suppressing lighting contrast and skin sheen

**Date:** 2026-07-21
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Profitability. This is the core product promise at the top of the funnel — a lean/fit male user who taps "Peak" and gets a soft-looking result does not convert and is a refund risk. Dan has now judged the output four times today; the anatomy is right and the *photographic* look is not.

## Objective

Make the AFTER image read as genuinely **shredded** for male subjects who start lean/fit, matching the aesthetic Dan specified (extremely lean, razor-sharp six-pack, muscular but not bulky — the Kinobody / Greg O'Gallagher look).

The diagnosis is done and it is narrow: **our prompt currently forbids the two things that make abs read as shredded in a photograph.** We command deep ab separation while also commanding that the original photo's lighting be preserved and that the skin carry no shine at all. Under flat, diffuse lighting with matte skin, even genuinely shredded abs render soft. Definition in a photo is contrast, and we have banned contrast.

Two changes, shipped and measured together as one commit. Nothing else changes.

## Current State

Everything below is live on absbyai.com and working as designed. This is a quality-tuning task, not a bug fix.

### What already shipped today (2026-07-21) — do not redo any of it

- **Muscle axis (`5943874`, `7e3f2f4`, `3a0ebcd`)** — `SYSTEM_PROMPT` in `public/index.html` gained a `MUSCULARITY ANCHOR TABLE` and condition-gated muscle rules. Gating is enforced **in code, not by prompt instruction** — `muscleAxisPlan()` (line ~3055) returns which `[[MUSCLE_*]]` marker blocks to keep, and `applyMuscleAxis()` (line ~3039) physically deletes the rest before the prompt is sent. Three tiers: male fit/very_lean → `SHREDDED-AESTHETIC RULE`; male moderate at dramatic/max → `SECONDARY-MASS RULE`; heavier males and all females → no mass language at all.
- **Prompt truncation fix (`8a7c4a4`)** — `max_tokens` on `/api/generate-prompt` in `server.js` was raised 1024 → 2048. The longer prompts were being cut off mid-`AVOID`, silently dropping guardrails. A `PROMPT_TRUNCATED` error logs on `stop_reason=max_tokens`. **If you lengthen the prompt further in this task, re-check that a full prompt still comes back** (assert the CLOSING sentence is present).
- **Comparative verifier (`18e8461`)** — the male dramatic/max change-verifier in `server.js` (`buildVerifierQuestion`, line ~2103) was rewritten so every clause compares against the BEFORE photo.
- **Shredded-aesthetic retarget (`ca2e5b9`)** — muscle anchors cut from +15 lb to +10 lb at max and reframed as an aesthetic lean-athlete amount; the six-pack made the non-negotiable outcome for lean starters; verifier made condition-aware (lean/fit males at dramatic/max must show an actual sharply cut six-pack; heavier/moderate males keep the plain comparative question).

### The measured evidence this task is built on

PostHog `generation_verifier` telemetry, Dan's two runs one minute apart, same person and settings (very_lean/max):

| Photo | Passed first try | Retries | Final | Dan's verdict |
|---|---|---|---|---|
| Selfie (arm raised, torso angled/cropped) | No | 2 (both) | Still weak | "still looks the same" |
| Pool (full torso, front-on) | Yes | 0 | Passed | "exactly what we're looking for" |

Four earlier very_lean/max runs show the same weak + 2-rung pattern; five moderate/max runs all passed first try. Conclusion already drawn: **the verifier and retry ladder work correctly; Gemini's compliance depends heavily on photo composition.**

Latest verified prod generation (already-lean proof photo, very_lean/max, after `ca2e5b9`): HTTP 200, 9.6s, `verifierPassedFirstTry: true`, `retryRungsUsed: 0`. Dan's assessment of that image: *"real close to what we want, but I would like the abs to look more shredded."* That image is the baseline this task must beat.

### The two offending strings (both in `public/index.html`, inside `SYSTEM_PROMPT`)

**1. Line ~2955 — the PRESERVE EXACTLY verbatim block**, which the assembled prompt copies word-for-word into every generation:

```
"PRESERVE EXACTLY: the same face, facial features, jawline, hairstyle, hair color, hair length,
eye color, ethnicity, age, smile, expression, clothing, jewelry, watch, accessories, shoes, pose,
background, and lighting from the original photo. ..."
```

`and lighting` is the problem. Flat gym or snapshot lighting cannot produce the shadow in an ab groove.

**2. Line ~2973 — the AVOID list:**

```
- oily, shiny, or wet-looking skin
```

A blanket ban on shine. Real fitness photography of a shredded midsection always carries specular highlight on the muscle bellies; that highlight is half of what sells the definition. We want to keep banning *oiled and wet*, not all sheen.

Related context, do not confuse with the above: the **SKIN TONE RULES block (line ~2960)** governs tanning depth by intensity and is a separate, working mechanism. Leave its tan logic alone.

## Key Decisions Already Made

- **Fix the photographic look, not the anatomy.** The anatomy language is now correct and Dan-approved in direction; the gap is lighting and surface. Do not add more anatomical ab description — see Lessons Learned, that was tried and it backfired.
- **Ship levers 1 and 2 together, then stop and measure.** Dan explicitly asked for a controlled test on a fixed photo rather than stacking changes. Two changes in one commit, one measurement, report before touching anything else.
- **Do NOT lower the body-fat floor in this task.** Dropping the male floor from 8% toward Greg's ~6% is a real option but it is deferred. It is the same "more extreme number" move that produced worse results twice today.
- **Do NOT ship a reference image of a real person.** Feeding a target physique alongside the user photo is the strongest remaining technique (`has_reference_photo` already exists in the prompt input contract at line ~2858, hardcoded `false` at line ~8663, so the plumbing was anticipated and never built). If that route is taken later, the reference must be **one of our own generated images**, never Greg O'Gallagher's or any other real person's photos — embedding a real person's likeness in a paid product to generate customer results is a genuine legal risk independent of whether it works.
- **Identity, framing, pose, background and clothing lockdowns stay absolute.** Only the *lighting on the torso* gets latitude, and only enough to model muscle. The subject must remain obviously the same person in the same photo.
- **Female paths are not touched.** The 2026-07-18 female work is validated and live.
- **Keep enforcement in code where gating matters.** Prose scope limits have failed twice in this codebase (this task's muscle axis, and the trainer's leg-press rule). If either lever needs to apply only to a subset of users, gate it with the existing `[[MUSCLE_*]]` marker mechanism rather than by instructing the model.

## Detailed Plan

### Step 0 — Capture the baseline before changing anything

The whole value of this task is a clean before/after on a fixed input. Run this first, on **production**, and save the image:

1. Open `https://absbyai.com`.
2. In the browser console, generate with the existing prod code against a fixed lean input — `public/img/proof/male-after.webp` is the standing, front-on, already-lean-and-muscular asset used for every prior test:

```js
state.gender='male'; state.condition='very_lean'; state.intensity='max';
state.effectiveIntensity='max'; state.mode='dream';
const blob = await (await fetch('img/proof/male-after.webp')).blob();
const b64 = await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result.split(',')[1]);fr.readAsDataURL(blob);});
const prompt = await callGeminiText(goalSystemPrompt(), JSON.stringify({
  user_description:'', subject_gender:'male', subject_current_condition:'very_lean',
  intensity:'max', has_reference_photo:false }));
const res = await fetch('/api/generate-image',{method:'POST',headers:{'Content-Type':'application/json'},
  body: JSON.stringify({prompt, photoBase64:b64, photoMime:blob.type, intensity:'max',
  sex:'male', startCondition:'very_lean', distinctId:'baseline', deviceId:getDeviceId(),
  attemptId:'base-'+Date.now()})});
const d = await res.json(); // keep d.imageBase64 and d.telemetry
```

3. Record `telemetry.verifierPassedFirstTry` and `retryRungsUsed`, and keep the image for side-by-side comparison.

**Local caveat:** the local environment has dummy Gemini/Anthropic keys. Image quality can only ever be judged on production. Locally you can only assert prompt strings and syntax.

### Step 1 — Lever 1: let the torso be lit

In `public/index.html`, in the **PRESERVE EXACTLY verbatim block (~line 2955)**:

1. Remove `and lighting` from the preserve list.
2. Replace it with wording that preserves the *scene* lighting while freeing the *modelling* of the torso. Preserve the light's direction, colour temperature, time of day and overall exposure — so it still looks like the same photograph — while explicitly permitting deeper shadow inside the ab separations, the oblique lines and the V-cut, and brighter highlights across the ab blocks, chest and shoulders, so the musculature is sculpted by light rather than flattened.
3. Add a matching instruction in the **SECTION 2 / BODY TRANSFORMATION** guidance for male dramatic/max (or inside the existing lean-only `[[MUSCLE_*]]` blocks if you want it scoped to lean starters only) stating that the abdominal definition must be rendered with real light-and-shadow contrast — each ab block catching light with a distinct shadow in every groove — not as flat, low-contrast lines drawn on the skin.
4. Do **not** weaken the FRAMING block (~line 2957) or any identity/pose/background/clothing lockdown.

### Step 2 — Lever 2: allow a dry athletic sheen

In the **AVOID list (~line 2973)**:

1. Change `- oily, shiny, or wet-looking skin` to ban only the genuinely bad states — heavily oiled, greasy, wet or sweat-drenched skin — while explicitly allowing the natural, dry, matte-to-slightly-luminous skin of an athletic person under good light.
2. Add a positive instruction (SECTION 2 / BODY TRANSFORMATION, or the lean-only block) asking for taut, dry skin drawn tight over the muscle with a subtle natural sheen on the ab blocks, chest and shoulders — explicitly *not* an oiled bodybuilder-stage look.
3. Leave the SKIN TONE RULES block (~line 2960) and its tan-by-intensity logic untouched.

### Step 3 — Local verification (cheap, catches the obvious)

1. `node --check server.js` (if you touched it — you probably don't need to for this task).
2. Extract and parse the inline `<script>` blocks from `public/index.html` to confirm the client still parses.
3. Boot the local server via `preview_start` with the `abs-by-ai` config in `.claude/launch.json` and assert, for each of `male/very_lean/max`, `male/fit/dramatic`, `male/moderate/max`, `male/heavier/max`, `female/heavier/max`:
   - `goalSystemPrompt()` contains the new lighting wording and no longer contains `and lighting from the original photo`.
   - `/\[\[MUSCLE_/` does **not** appear (marker leak check — this has regressed before).
   - The female and heavier-male prompts still contain their existing rules.

### Step 4 — Ship

One commit containing both levers. Push to `main`, confirm Railway auto-deploys, and confirm the new wording is being served from `https://absbyai.com` before measuring.

Note on credentials: as of 2026-07-21 the GitHub token is stored in the **macOS keychain** (`credential.helper osxkeychain`) and the `origin` remote is the clean `https://github.com/RagnarD213/abs-by-ai.git` with no embedded token. If a push fails with HTTP 403, the token is missing `Contents: write` — an API write probe returns `x-accepted-github-permissions: contents=write`, and note that the repo's `permissions.push` field reflects Dan's *account* role, not the token's scopes, so it will misleadingly say `true`.

### Step 5 — Measure on production, same photo, same settings

1. Re-run the exact Step 0 script against the deployed code.
2. Confirm the assembled prompt still comes back **complete** — assert the CLOSING sentence (`natural, unretouched smartphone photograph`) and the male AVOID bullets (`bulging veins`, `comically oversized`, `spray-on abs`) are all present. The prompt just got longer; truncation is the known failure mode.
3. Render baseline and new result side by side and screenshot for Dan.
4. Report `verifierPassedFirstTry` and `retryRungsUsed` for both runs.

**Watch for over-firing:** if the new result now *fails* the six-pack verifier and burns retries where the baseline passed at 0 rungs, that is a cost regression and needs flagging, not silently accepting.

### Step 6 — Regression check

Run one `male/moderate/max` (Average) generation on `public/img/proof/male-before.webp`. Average users were made more dramatic earlier today via the `SECONDARY-MASS RULE` and Dan has already rejected one change for making Average worse. Confirm it has not regressed. Do not judge this by prompt text alone — generate the image.

### Step 7 — Report and stop

Show Dan the side-by-side and the telemetry. **Do not proceed to the body-fat floor drop or the reference-image work without his call** — he explicitly asked for one measured change at a time.

**OPEN:** should the lighting/sheen latitude apply to *all* subjects at dramatic/max, or only to lean/fit males? Recommendation: apply to all male dramatic/max first, since better light modelling helps an Average result too, and the guardrails against oiled skin remain. If Dan dislikes the look on Average, scope it to the lean-only `[[MUSCLE_*]]` blocks — the mechanism is already there.

## Things to Avoid / Lessons Learned

- **Do not add more anatomical ab detail.** Tried 2026-07-21 (commit `a255f41`): a directive demanding a flat lower abdomen, separated lower ab blocks, V-cut, no waistband roll. Dan's verdict: Average came back **worse and less dramatic**. Reverted in `323135e`. Read: on this pipeline, heavy prompt real estate on one region competes with, rather than adds to, overall transformation magnitude.
- **Do not chase this with a lower body-fat number.** Tightening max from 8-10% to 8-9% in that same reverted commit contributed to the worse result. Established twice: a more extreme number on a body the model is already hedging on produces more hedging, not more compliance.
- **Do not rely on prose scope limits.** Instructing the prompt-assembly model "this rule only applies to X" has failed twice in this codebase. Gate in code.
- **Do not swap image models for this.** Gemini's ceiling is real for *heavier* bodies (established 2026-07-18 across four aggressive techniques). It is not the constraint for lean subjects — Gemini complies well on a good photo, as the pool-photo run proves.
- **A near-identical output can be a correct output.** Always check what the prompt actually asked for before assuming refusal.
- **Photo composition is a real variable, not noise.** A close-up selfie with a raised arm and an angled, cropped torso defeats the retry ladder; a full front-on torso passes first try. If a test result looks weak, check which photo it was before changing code.
- **Image quality cannot be judged locally** — dummy API keys. Every quality judgment happens on absbyai.com.
- **Don't sweep unrelated files into the commit** — the repo root has many untracked handoff and asset files.

## Relevant Files & Locations

| What | Where |
|---|---|
| Prompt layer (all prompt edits for this task) | `public/index.html` |
| — `SYSTEM_PROMPT` | ~line 2848 |
| — Output contract (7 sections) | ~lines 2863–2869 |
| — **PRESERVE EXACTLY verbatim block (Lever 1)** | **~line 2955** |
| — FRAMING verbatim block (do not weaken) | ~line 2957 |
| — SKIN TONE RULES block (leave tan logic alone) | ~line 2960 |
| — **AVOID list, `oily, shiny, or wet-looking skin` (Lever 2)** | **~line 2973** |
| — `SHREDDED-AESTHETIC RULE` / `SECONDARY-MASS RULE` / `[[MUSCLE_*]]` markers | ~lines 2892–2935 |
| — `applyMuscleAxis()` / `muscleAxisPlan()` / `goalSystemPrompt()` | ~lines 3039 / 3055 / 3071 |
| — `has_reference_photo` (contract field, hardcoded false) | ~lines 2858 / 8663 |
| Verifier + retry ladder (no change expected) | `server.js` |
| — `buildVerifierQuestion()` | ~line 2103 |
| — `/api/generate-prompt` `max_tokens` + `PROMPT_TRUNCATED` log | ~line 1430 |
| Fixed test inputs | `public/img/proof/male-after.webp` (lean), `male-before.webp` (average) |
| Live site | https://absbyai.com |
| Deploy | Railway, auto-deploys from GitHub `main` |
| Telemetry | PostHog event `generation_verifier`; Railway logs `GEN_TELEMETRY {…}` |
| Prior context | `AI_COORDINATION.md`, `handoff-20260720-lean-male-muscle-axis.md` |
| Env vars (names only) | `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` |

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** The diagnosis is finished and both edits are two well-specified string changes in one file. The real work is the measurement discipline in Steps 0/5/6, which this document scripts. Don't reach for Opus by habit — there's no exploration left here. |
| **If Claude usage is high / approaching a limit** | **Still Claude Sonnet 5, standard thinking** — see the override below. This is not a Codex task, but it's also not an expensive one; Sonnet is the cheapest model that does it competently. |

**Task-type override:** this edits the Anthropic system prompt that drives image generation, which is both Anthropic-integration code and the product's core output quality — an always-Claude task type regardless of usage. Being wrong here changes the image every lean/fit male user sees, and today's session already produced two changes that had to be reverted after Dan's eyeball.

**Escalate to Claude Opus with extended thinking only if** the Step 5 measurement shows the result got *worse* or didn't move. At that point the task stops being execution and becomes diagnosis again, which is what Opus is for. Fable is a reasonable middle ground on cost if you'd rather not spend Opus budget — double-check its current pricing and availability first, as that has changed before.

## Starter Prompt for the Next Task

> Read `handoff-20260721-shredded-abs-lighting-and-sheen.md` in the project root — it has the full diagnosis, the exact strings to change, and the measurement protocol.
>
> Short version: Dan wants the AFTER images for lean/fit male users to look genuinely shredded (extremely lean, razor-sharp six-pack, muscular but not bulky). The anatomy language in `SYSTEM_PROMPT` is already correct and Dan-approved in direction. The remaining gap is photographic: our prompt tells Gemini to preserve the original photo's **lighting** (in the PRESERVE EXACTLY verbatim block, `public/index.html` ~line 2955) and bans **all shiny skin** (AVOID list, ~line 2973). Flat lighting plus matte skin renders even genuinely shredded abs as soft — definition in a photograph is contrast, and we banned contrast.
>
> Implement exactly the two levers in the handoff, as **one commit**: (1) free the torso's light modelling — keep the scene's light direction, colour temperature and exposure so it's the same photo, but explicitly allow deep shadow in each ab groove and bright highlights on the blocks; (2) narrow the skin ban to oiled/wet/sweat-drenched only, and positively ask for taut, dry skin with a subtle natural sheen. Keep every identity, framing, pose, background and clothing lockdown absolute, and leave the SKIN TONE RULES tan logic alone.
>
> **Critically: capture the Step 0 baseline generation on production BEFORE changing anything**, using the fixed proof photo `public/img/proof/male-after.webp` at very_lean/max — the whole point is a clean before/after on one input. Image quality cannot be judged locally (dummy API keys); all quality verification happens on absbyai.com. After shipping, re-run the identical generation, confirm the prompt didn't get truncated (the CLOSING sentence and the male AVOID bullets must still be present), check `verifierPassedFirstTry` / `retryRungsUsed` for a cost regression, run one Average (`male/moderate/max`) generation to confirm no regression there, then show Dan the side-by-side and **stop**.
>
> Do not add more anatomical ab description, do not lower the body-fat floor, and do not touch any female path — all three were tried or ruled out today and the reasons are in the handoff. Update `AI_COORDINATION.md` when you pick this up.
