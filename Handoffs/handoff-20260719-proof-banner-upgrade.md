# Handoff: Proof-banner upgrade (crop fix, 3rd slide, collapse-to-strip)

**Date:** 2026-07-19
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Marketing performance (ad-click conversion on the landing page) → profitability

## Objective

Upgrade the "✦ Created with Abs by AI" proof banner on the landing page: (1) stop cutting people's heads off at any screen size, (2) keep it fast on low-bandwidth cellular, (3) add a third before/after slide — a white man in his late 40s, 50–70 lbs overweight, transforming to fitness-model abs, (4) add polish (mobile swipe, off-screen pause, human captions, After-panel emphasis), and (5) after all three slides have auto-played once, collapse the banner to a slim tappable strip so the photo-upload box moves to the top of the page. Every step is its own commit, pushed to `main`, auto-deployed by Railway, and verified live on absbyai.com.

## Current State

Nothing from this plan is implemented yet — this is a fully planned, zero-code-written task. Everything lives in one file: `public/index.html`.

- **CSS** for the banner: lines ~99–155 (`.proof-strip`, `.proof-stage`, `.proof-slide`, `.proof-image-wrap`, `.proof-image`, `.proof-image-label`, dots).
- **HTML**: lines ~1362–1390 — `<section id="proofStrip">` with 2 slides (male, female), each a Before + AI-After `<img>` pair, plus 2 dot buttons.
- **JS**: `initProofStrip()` at line ~2991 — 4-second auto-rotation, dot clicks, hover/focus pause, and a `data-src` → `src` hydration loop at ~3062 (images load deferred, `loading="lazy"`, `width="375" height="500"`).
- **Images**: `public/img/proof/male-before.webp`, `male-after.webp`, `female-before.webp`, `female-after.webp` — each 375×500 WebP, only ~11–13 KB apiece.

**Root cause of the head cropping (diagnosed, not yet fixed):** `.proof-stage` has a hard-coded `height: 112px` and slides are `position: absolute; inset: 0`, so each portrait 3:4 photo is squeezed into a short wide box; `object-fit: cover; object-position: center 28%` then crops the head off, worst on wide screens.

## Key Decisions Already Made

- **Crop fix = aspect-ratio sizing, not a nudge.** Give each image box a fixed ~3:4 aspect ratio so the box grows taller with screen width and the whole person always fits. Requires restructuring the slide stack away from the fixed-height absolute positioning (e.g., grid-stacked slides in the same cell for the cross-fade). Bigger banner on desktop is a feature, not a bug.
- **Collapse-to-strip, NOT full disappearance** (Dan explicitly chose this): after one full rotation (~12s) *and* no active user interaction, the banner animates down to a slim "✦ See examples ▸" strip with a tiny thumbnail; upload box glides to the top; tapping re-expands. Rationale: no jarring layout yank mid-view, preserves social proof for hesitant visitors, and avoids CLS penalties.
- **Generate the new pair After-first, then add weight for the Before.** The A3.1 investigation (see `AI_COORDINATION.md`) proved gemini-2.5-flash-image strongly resists *removing* large amounts of fat from heavy bodies but adding weight is an easy edit — working backwards yields a matched pair with the same face. Generate 2–3 candidate pairs; **Dan picks the winner before slide 3 is wired in.**
- **Load-time verdict: the banner is cheap (~75 KB total for all 6 images), no redesign needed.** Harden anyway: eager-load slide 1 only, defer slides 2–3 to idle/post-first-paint; keep new images at 375×500 WebP ~12 KB; reserve banner space pre-load (no layout shift). The page's real weight is the monolithic index.html — explicitly out of scope.
- **Slide reordering by audience is deferred** until PostHog data shows which "Where you are now" option dominates. Not in this task.
- **Dan is non-technical** — explain work in plain language, act decisively, minimal permission-asking (per `AGENTS.md`).

## Detailed Plan

Execute in order; each numbered step = own commit + push + live verification on absbyai.com before the next.

1. **Crop fix.** In `public/index.html`: remove `height: 112px` from `.proof-stage` and `height: 112px` from `.proof-image`; give `.proof-image-wrap` (or the img) `aspect-ratio: 3 / 4` (test 4/5 too — pick what looks best while guaranteeing full heads); restructure `.proof-slide` from absolute-inset to grid-stacked (all slides in `grid-area: 1 / 1`) so the stage takes content height while the cross-fade still works; keep `object-fit: cover` but verify no head cropping at 360px, 768px, and 1280px+ widths. Keep `prefers-reduced-motion` handling.
2. **Load-time hardening.** Eager-hydrate only slide 0's two images immediately; hydrate the remaining slides on `requestIdleCallback` (with `setTimeout` fallback) or on first rotation/dot-tap, whichever comes first. Confirm reserved space (correct `width`/`height` or aspect-ratio prevents shift). Can share commit 1 if trivially small.
3. **Third slide — images first, wiring second.**
   a. Generate 2–3 candidate pairs: late-40s white man, fitness-model abs (After) → same man edited +50–70 lbs (Before). **Local `.env` has dummy Gemini/Anthropic keys** — generate via the production pipeline or any image tool with real access; match existing style (same gym-ish setting vibe, waist-up framing with full head, 375×500 WebP, ~12 KB, filenames `male2-before.webp` / `male2-after.webp` in `public/img/proof/`).
   b. **STOP — show candidates to Dan; he picks.** (OPEN: exact drama level. Dan's original ask was full fitness-model abs; Claude flagged the honesty tension with the A3.1 finding that the live product can't render heavy→shredded. Dan proceeded without explicitly choosing — include one "impressive-but-attainable" candidate among the dramatic ones so he can decide by looking.)
   c. Wire slide 3: third `data-proof-slide` block, third dot with proper `aria-label`, alt text marking it a fictional example (match existing wording). Rotation/dots/hydration must all handle N=3 (the JS already uses `slides.length` — verify).
4. **Extras.** (a) Touch swipe left/right on `.proof-stage` (pointer events, ~40 px threshold, don't hijack vertical scroll); (b) pause auto-rotation when the strip is off-screen via `IntersectionObserver`; (c) one-line human caption per slide (e.g. "Busy dad, late 40s" — keep punchy, benefits-flavored, and clearly fictional-example compliant); (d) subtle After-panel emphasis (slightly stronger border/glow on the AI-After image). PostHog event on swipe if cheap.
5. **Collapse-to-strip.** Track "full rotation completed" (all slides shown once); when true AND no hover/focus/recent pointer interaction (interaction resets a short grace timer), animate the banner to a slim strip ("✦ See examples ▸" + micro-thumbnail) and let the upload card move to top — animate heights so nothing jumps. Tap strip → re-expand + resume rotation. Session-persist collapsed state (`sessionStorage`) so returning visitors in-session start collapsed. PostHog: `proof_collapsed`, `proof_reexpanded` (plus existing pattern conventions — see `posthog.capture` calls in index.html). Respect `prefers-reduced-motion` (instant swap, no animation).

Final: update `AI_COORDINATION.md` (this task is listed under Queued) and reset/record per its working rules.

## Things to Avoid / Lessons Learned

- **Do NOT try to generate the Before→After by asking Gemini to slim a heavy body** — A3.1 proved four escalating techniques all failed; generate the fit After first and add weight.
- **Don't fully remove the banner post-rotation** — decided against (layout yank, lost social proof, CLS).
- **Don't touch the transformation prompts, verifier, or `server.js`** — this is a pure client-side/landing task; the female-dramatic work (A3) has open threads owned separately.
- Local preview has **dummy API keys** — anything model-generated must be judged via prod or external tools.
- The site serves **only `public/`**; root `*-data.json` files are the persistence layer — never untrack or move them.
- Keep new images tiny (~12 KB WebP); don't ship PNGs.
- `index.html` is one huge file — make surgical edits, run a JS syntax check (`node --check` on extracted script or load the page) before committing.

## Relevant Files & Locations

- `public/index.html` — CSS ~99–155, HTML ~1362–1390, JS `initProofStrip()` ~2991, hydration ~3062 (line numbers pre-change)
- `public/img/proof/` — existing 4 WebP images; new pair lands here
- `AI_COORDINATION.md` — task board; A3/A3.1 Gemini-ceiling context lives here
- Live site: https://absbyai.com (Railway auto-deploys from GitHub `main`)
- PostHog: existing `posthog.capture` patterns in index.html for event naming

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking — this is well-specified single-file front-end work |
| **If Claude usage is high / approaching a limit** | Codex flagship (current model), medium effort |

No always-Claude override applies (no Anthropic-API code, no long-form brand copy — the slide captions are one-liners any competent model handles). If step 5's collapse animation gets fiddly across browsers, escalate effort/model then rather than over-provisioning up front. Image generation (step 3a) is Gemini prompting, independent of which coding model runs the session.

## Starter Prompt for the Next Task

> Read `handoff-20260719-proof-banner-upgrade.md` in the Abs By AI project root and execute its Detailed Plan. It upgrades the landing-page proof banner in `public/index.html`: fix head cropping via aspect-ratio sizing, harden low-bandwidth loading, add a third before/after slide (late-40s overweight man → abs; generate the After image FIRST, then add weight for the Before — Gemini can't do the reverse), add swipe/captions/off-screen-pause/After-emphasis, then collapse-to-strip after one rotation with upload moving to top. One commit + push + live absbyai.com verification per step. STOP after generating 2–3 candidate image pairs and get Dan's pick before wiring slide 3. Start with step 1 (the crop fix). Explain each step in plain, non-technical language as you go.
