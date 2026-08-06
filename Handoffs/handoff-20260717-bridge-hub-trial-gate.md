# Handoff: Bridge screen + hub preview + trial gate

**Date:** 2026-07-17
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Profitability (route the free-generation funnel into 7-day membership trials instead of ending at a print upsell)

## Objective

Rework what happens after the email-capture screen. Today the funnel is: result → email capture → **print product selector → print customizer → checkout**. The new funnel is: result → email capture → **bridge screen (sells the membership benefits) → member hub in logged-out preview mode (with the print upsell demoted to a card at the top) → any feature tap opens the trial gate** (signup + 7-day free trial via the existing Stripe membership checkout). The print flow is NOT deleted — it moves behind the hub upsell card.

## Current State

- One-file front end: `index.html` (~8,160 lines); backend `server.js` on Railway, auto-deploy from GitHub `main`.
- Current flow wiring: `$('loveItBtn')` → confetti → `showEmailScreen()` (index.html:3229). Email submit posts to `/api/subscribe` then `showProductSection()` (index.html:3248-3262); "No thanks" (`emailSkipBtn`, 3263) also goes to `showProductSection()`.
- Print screens: `#productSection` (1564, canvas from $34 / poster from $18), `#customizeSection` (1611), `#confirmationSection` (1649). Printify fulfills orders (see memory: printify-print-flow).
- Member hub: `#hubSection` (1697) — currently only reachable when logged in. Tiles (`.hub-tile`, from 1750) with `data-feature` values: `macro`, `trainer`, `nutritionist`, `counsel` (Supplement Audit), `sleep`, `transformations`, `weight` (Progress), `generate`, `support`. Tile click handler at index.html:4218-4234. A "Become a member" tile (`hubBecomeMemBtn`, 1751) shows for logged-in non-members.
- Auth: `#authSection` (1673), `showAuthScreen(mode)` (2456 area / 3456), signup and login both exist; email captured on the email screen is stored in `localStorage.absbyai_email` — prefill it in signup.
- Membership screen: `#membershipSection` (2116), `showMembershipScreen(returnTo, opts)` (4740). Stripe checkout already gives first-time subscribers a **7-day free trial, card up front** (server.js ~3022-3051), one trial per user, plus an automatic "trial ends in 2 days" reminder email (server.js:2454). Pricing: $19.99/mo, $69.99/yr shown as $5.83/mo (server.js:102-103). **No trial-mechanics work is needed — reuse this.**
- Screen switching: `showScreen(name)` (2652) with the id list at 2653.
- Native apps hide digital purchases via `app-hide-purchase` / `app-only-note` classes — the trial gate and bridge-screen pricing mentions must respect the same gating.

## Key Decisions Already Made

- Screens 1–3 (form → result → email capture) stay exactly as they are.
- New screen 4 = bridge screen: user's own before/after pair on top, headline "Here's how Abs by AI helps you build your dream body", exactly three benefit bullets, single Continue button (no skip, no second CTA). The three bullets (chosen deliberately — do not expand the list):
  1. **AI Trainer** — "A personalized workout program built to get you to that photo"
  2. **Macro Tracker + AI Nutritionist** — "Snap a photo of any meal, get calories and macros instantly"
  3. **Progress Log** — "Track your body next to your goal photo and watch yourself close the gap"
- Continue → member hub in logged-out **preview mode**: all tiles visible; a "Print your future self — from $18" upsell card at the top of the tile list which opens the existing `#productSection` print flow (preserving its back-navigation).
- In preview mode, tapping any feature tile opens the **trial gate**, not the feature. Trial gate = create account (prefilled email) → existing membership checkout with 7-day trial. Wording like "Start your 7-day free trial to unlock it".
- Trial terms unchanged: 7 days, card up front, $19.99/mo / $69.99/yr after, one trial per user, existing reminder email. Decided — do not relitigate.
- Native apps: the whole trial gate is a purchase surface — hide/gate it with the existing `app-hide-purchase` pattern the same way current purchase UI is hidden.
- A follow-up task (separate handoff: `handoff-20260717-member-profile-questionnaire.md`) inserts a short "Let's build your plan" questionnaire between account creation and the trial checkout. Build this task so that insertion is easy (a single function boundary between "account created" and "open membership checkout"), but do not build the questionnaire here.

## Detailed Plan

1. Add `#bridgeSection` markup (new screen div; register its id in the `showScreen` list at index.html:2653). Reuse `.before-after-grid` for the user's own pair (images already in memory from the result screen), hero styles for the headline, and a simple 3-row benefit list (the `.hub-tile` look works well). Single `.cta-btn` Continue.
2. Rewire: email submit handler (3248) and `emailSkipBtn` (3263) → `showBridgeScreen()` instead of `showProductSection()`.
3. Hub preview mode: add a `renderHubPreview()` path so `#hubSection` can render logged-out — hide logout/membership-management rows, show all feature tiles, and insert the print upsell card (user's after-image thumbnail + "Print your future self — from $18") above the tiles. Clicking it → `showProductSection()`; the product screen's back button must return to the hub preview (there's precedent: `upsell.returnScreen` handling at index.html:3266-3268).
4. Gate tiles in preview mode: intercept the tile click handler (4218) — when not logged in (or logged in without active membership), capture PostHog `trial_gate_shown` with the feature name and show the trial gate instead of the feature.
5. Trial gate: reuse `showAuthScreen('signup')` with email prefilled from `localStorage.absbyai_email`, retitled around the trial ("Create your account to start your free trial"). On successful signup, route into `showMembershipScreen(returnTo)` where `returnTo` re-opens the feature they tapped. Keep one clean function boundary here for the future questionnaire insertion.
6. Post-trial-start: Stripe success already returns to the site (see `dest` handling around index.html:5729) — make sure the return lands in the hub with the feature unlocked.
7. Analytics funnel events: `bridge_seen`, `bridge_continue`, `hub_preview_seen`, `print_upsell_clicked`, `trial_gate_shown`, `trial_signup_started`, plus existing checkout events. This funnel is the whole point — instrument every step.
8. Edge cases: already-logged-in members finishing a new generation should skip the trial gate (bridge → hub as normal members); the old direct path `confirmationSection → Continue` should still work; `productSkipBtn` (1607) in the new context returns to hub preview.
9. Verify end-to-end on production with a fresh device: generate → lock in → email → bridge → hub preview → tile tap → signup → Stripe trial checkout (use Stripe test-clock/coupon caution: Stripe is LIVE — verify checkout page loads and cancel before paying, or use a 100% promo if one exists). Verify print card still reaches the working Printify flow.
10. Commit, push to `main`, confirm Railway deploy, verify live on absbyai.com (AGENTS.md requirement).

## Things to Avoid / Lessons Learned

- Stripe is LIVE and charging (as of 2026-07-17) — do not place real test orders without cancelling; membership webhooks are already wired and working, don't modify them.
- Don't delete the print flow or its screens — it's demoted, not removed. Printify placement has a no-crop caveat (memory: printify-print-flow); don't touch mockup rendering.
- Don't modify the trial logic in `server.js` — it's built, verified, and FTC-compliant (reminder email). This task is front-end routing plus one signup-flow retitle.
- `showScreen` hides every screen not in its id list — forgetting to register `bridgeSection` there is the classic bug.
- Local preview has an invalid Anthropic key; feature endpoints must be tested on production.
- Non-technical user: explain the funnel changes in plain language when reporting.

## Relevant Files & Locations

- `index.html` — email flow 3248-3268, product screens 1564-1670, hub 1697-1806, tile handler 4218-4234, auth 1673 + `initAccounts()` 4195, membership screen 4740, `showScreen` 2652
- `server.js` — membership plans 102-103, trial creation ~3022-3051, trial reminder 2454 (all read-only)
- Live: https://absbyai.com · Railway auto-deploy from `main` · PostHog project 458833 (us.posthog.com)
- Companion handoffs: `handoff-20260717-proof-strip-locked-teaser.md` (independent, can run first), `handoff-20260717-member-profile-questionnaire.md` (depends on this one)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Codex flagship model, medium effort (confirm current model name at run time) |

Multi-screen rewiring with several existing code paths to preserve — bigger than boilerplate but fully specified, so no always-Claude override. If the executing session finds the hub's logged-in assumptions run deeper than expected, escalate to Claude Opus (extended thinking) or Codex high rather than forcing it.

## Starter Prompt for the Next Task

> Read `handoff-20260717-bridge-hub-trial-gate.md` in the Abs By AI repo root and implement it. The funnel change: after email capture, users go to a new benefits "bridge" screen, then into the member hub in logged-out preview mode with the print upsell as a top card, and any feature tap opens a trial gate that reuses the existing signup + 7-day Stripe trial checkout. Do not modify server-side trial logic. Start by adding `#bridgeSection` and registering it in `showScreen`, then rewire the email screen's two exits. Instrument every funnel step with the PostHog events listed. Follow AGENTS.md delivery rules: commit, push to main, verify Railway deploy, verify live on absbyai.com, and explain what changed in plain language.
