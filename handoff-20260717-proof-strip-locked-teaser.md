# Handoff: Screen-1 proof strip + locked-result teaser

**Date:** 2026-07-17
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Profitability (more uploads at the top of the funnel, more credit-pack/membership purchases at the paywall)

## Objective

Two small, self-contained front-end changes to the onboarding funnel in `index.html`:

1. **Proof strip on the first screen** — show new visitors 2–3 example before/after transformation pairs before we ask them to upload a shirtless photo, so they see the payoff before the high-trust ask.
2. **Locked-result teaser** — when a user is out of credits, stop hiding the after-image behind a flat lock overlay. Instead show it with the face/shoulders sharp and the torso heavily blurred, with a lock pill over the abs, and make the paywall headline reference their actual estimated body-fat number.

## Current State

- The whole site is one file: `index.html` (~8,160 lines) served by `server.js` (Express, deployed on Railway, auto-deploys from GitHub `main`).
- Screen 1 is `#formSection` (index.html:1237). Headline "Visualize Yourself With Abs" at line 1253, then the upload card `#uploadCard` at line 1264. The proof strip goes between them.
- The locked result: `showLockedResult()` (index.html:2301) shows `#resultSection` with `#afterLockOverlay` (index.html:1445) — a full-cover dark overlay with a lock icon and "Unlock to reveal". The paywall block `#paywallSection` is at index.html:1486 with headline "Your result is ready — unlock it".
- Body-fat estimates already render into `#bfBefore` / `#bfAfter` (index.html:1456-1458) — the after number is available for the paywall headline.
- Credits: every device gets 3 free generations (`FREE_CREDITS`, server.js:90). Packs: $4.99/5, $14.99/20 (server.js:96-97).
- Native-app note: purchase UI is hidden in the iOS/Android wrappers via the `app-hide-purchase` / `app-only-note` classes — the teaser change must keep using those classes exactly as the current paywall block does.

## Key Decisions Already Made

- Proof strip sits under the headline, above the upload card; auto-rotates through 2–3 pairs every few seconds; stays compact (don't push the upload card below the fold on mobile).
- Label the strip honestly as AI visualizations — e.g. "Created with Abs by AI" — never imply they are real physical transformations. This is both an honesty requirement and the product promise.
- Mixed male/female example pairs.
- Teaser blur: face/shoulders sharp, torso heavily blurred, lock pill over the abs reading "Unlock to see your abs". Do the blur client-side with CSS (e.g. a blurred copy of the image clipped with a gradient mask over the sharp one) — the full unblurred image must never be visible or trivially recoverable by removing one CSS rule while locked. Acceptable: it's already in the DOM as an <img>; the goal is visual tease, not DRM.
- Paywall headline becomes dynamic, e.g. "Your transformation is done. See yourself at 12% body fat" using the `#bfAfter` value; fall back to generic copy if no estimate is available.
- Keep all existing paywall purchase options and the `paywallGoUnlimitedBtn` membership link unchanged.

## Detailed Plan

1. **Assets (needs Dan):** pick 2–3 before/after pairs. Candidate source folders in the repo working directory: `abs by ai images/`, `abs by ai images for future videos/`, `B roll/`. The executing session should shortlist candidates, show them to Dan for approval, then export web-sized copies (roughly 400–600px tall, compressed JPEG/WebP, target <80KB each) into `img/proof/`. OPEN: Dan has not yet picked the images.
2. Add the proof strip markup to `#formSection` between the `.hero-sub` (line 1254) and `#backendStatus` (line 1257): a small card with a Before/After pair (reuse the visual language of `.before-after-grid` / `.ba-col-label` / `.transform-pill` styles already in the file), the "Created with Abs by AI" caption, and dots or a subtle crossfade rotating pairs every ~4 seconds via a tiny JS interval.
3. Lazy-load the proof images (`loading="lazy"` or set `src` after first paint) so they don't slow the first render — load time is a known concern on this app (see memory: keep-warm and downscaling work).
4. Teaser: in `showLockedResult()` / the lock path, populate `#afterImg` with the generated result, add a new overlay element that blurs only the lower ~65% of the image (blurred duplicate + `mask-image: linear-gradient(...)`, plus a semi-transparent veil so screenshots aren't clean), and replace the current full lock overlay with a small centered lock pill positioned over the abs region. Clicking anywhere on the teaser scrolls to / focuses the paywall.
5. Make the paywall headline dynamic from the body-fat estimate; keep `paywall-sub` and everything below unchanged.
6. Add PostHog events: `proof_strip_seen` (once per session on form view), `locked_teaser_shown`, and keep existing purchase events untouched (pattern: `posthog.capture('email_subscribed')` at index.html:3253).
7. Verify locally, then on production: fresh device (clear localStorage / new incognito) → strip shows and rotates; burn 3 credits → teaser shows sharp shoulders + blurred abs + dynamic headline; buy-flow buttons still work; in-app classes still hide purchases.
8. Commit, push to `main`, confirm Railway deploy, verify live at absbyai.com (required by AGENTS.md).

## Things to Avoid / Lessons Learned

- Don't touch the generation logic, credits accounting, or Stripe code — this task is presentation-only.
- Don't add heavy images to first paint; page load speed has already been optimized once (photo downscaling, keep-warm) — don't regress it.
- Don't rename or remove `#afterLockOverlay`, `#paywallSection`, `app-hide-purchase`, or `app-only-note` — other code paths and the native wrappers depend on them.
- Local preview has an invalid Anthropic key — test AI endpoints against production, but this task shouldn't need them.

## Relevant Files & Locations

- `index.html` — form screen 1237, upload card 1264, result screen 1414, lock overlay 1445, paywall 1486, `showLockedResult()` 2301, body-fat elements 1453-1459
- `server.js:90-103` — credits and pricing constants (read-only for this task)
- Image folders: `abs by ai images/`, `abs by ai images for future videos/`, `B roll/` → export to `img/proof/`
- Live site: https://absbyai.com · Deploy: Railway auto-deploy from GitHub `main`

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Codex mini-tier model, low effort (confirm current model name at run time) |

Routine, well-specified single-file UI work — no always-Claude override applies. Cheap-first; escalate only if the CSS masking fights back.

## Starter Prompt for the Next Task

> Read `handoff-20260717-proof-strip-locked-teaser.md` in the Abs By AI repo root and implement it. Start with step 1: shortlist 2–3 before/after example pairs from the folders `abs by ai images/`, `abs by ai images for future videos/`, and `B roll/`, and show them to me for approval before building the proof strip. While waiting on my approval you can implement the locked-result teaser (steps 4–6), which needs no assets. Follow the repo's AGENTS.md delivery rules: commit, push to main, verify the Railway deploy, and verify live on absbyai.com.
