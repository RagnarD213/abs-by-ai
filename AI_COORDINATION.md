# Abs By AI — Codex and Claude Code Coordination

This is the shared, project-level task board for Codex and Claude Code. It describes the one active task and the latest handoff between the assistants. It is not tied to one source file, and it does not replace Git history or permanent project documentation.

## Working rules

1. Read this file before beginning project work.
2. Only one assistant owns implementation of the active task at a time.
3. Do not overwrite or continue the other assistant's unfinished work without an explicit handoff or a user-requested review.
4. Update this file when starting work, reaching a meaningful milestone, becoming blocked, handing off, or completing the task.
5. Keep entries short and factual. Record what another assistant needs to continue, not a transcript of the conversation.
6. Preserve durable product and architecture decisions in the appropriate permanent documentation. Git remains the permanent record of code changes.
7. When a task is fully completed, committed, pushed, deployed, and verified, clear the active-task details and set the status to `No active task`.

## Status options

Use one of: `No active task`, `Planning`, `Ready for implementation`, `Implementation in progress`, `Ready for review`, `Blocked`, or `Complete — pending reset`.

---

## Active task

**Owner:** Claude Code
**Status:** `Implementation in progress`

### Security hardening + prompt/product improvements (started 2026-07-18)

Executing `handoff-20260717-security-and-prompt-improvements.md` (7 items, separate commit + live-verify each). User-directed; takes precedence over the member-profile task (moved to Queued).

**Item 1 — stop serving project folder publicly: COMPLETE, live-verified 2026-07-18, commit `1a63e6c`.** This also fixed a **live production outage**: the prior deploy (`1e7f9b5`, the N1 fix) had moved the browser assets into the tracked `public/` folder but left `server.js` pointing at the project root — so production was crashing on boot with `Cannot find module './exercises'` (502 on absbyai.com) AND `express.static('.')` was exposing the whole root over HTTP (real subscriber emails in `subscribers-data.json`, `credits-data.json`, `server.js`/`db.js` source, internal `*.md`). Fix: require exercises from `./public/exercises`, serve only `path.join(__dirname,'public')`, add `/privacy` route + SPA fallback to `public/index.html`. Live-verified: homepage/assets/`/dashboard`/`/admin` all 200; `/server.js`, `/subscribers-data.json`, `/credits-data.json`, `/db.js`, `/package.json`, `/AI_COORDINATION.md` all return the SPA HTML with zero real-data markers (content-type text/html).
  - **Deviation from handoff (intentional):** did NOT `.gitignore`/untrack the `*-data.json` files. They are the persistence layer — the server reads/writes them via the GitHub contents API, so untracking would 404 the load and wipe all credit balances + the subscriber list on next boot. The HTTP leak is fully closed by not *serving* them; removing them is unnecessary and destructive. `analytics.html` (dead — calls a nonexistent `/api/posthog-query`) and other root HTML are now unreachable over HTTP, which is fine.

**Item 2 — per-IP free-generation cap: COMPLETE, deployed + verified 2026-07-18, commit `4bdd203`.** Fresh-deviceId farming (each new browser id implicitly gets `FREE_CREDITS=3`) is now bounded by a per-IP daily ceiling (`FREE_IP_DAILY_CAP=6`, ~2 devices' worth) on FREE-allowance spends only. Over the cap → image returns `locked:true` (paywall path), not an error. **Payer-safe:** members and purchasers are never capped — added a persisted `creditsStore.purchasers[deviceId]` flag (set on credit fulfillment) plus a `balance>FREE_CREDITS` heuristic for legacy pre-flag payers. Client IP read from `X-Forwarded-For` (leftmost) scoped to this cap; global `trust proxy` intentionally left unset so existing rate limiters are unchanged (that's the separate N2 finding). In-memory `freeIpCounts` Map, single-replica caveat (same as `fixCounts`/`attemptCache`).
  - **Verified:** (1) deterministic logic sim — 6 free then lock per IP, other IPs unaffected, purchasers/members/legacy-payers never locked, out-of-credits paywall doesn't consume cap budget; (2) **live on Railway** via a temporary `/api/_ipcheck` (since removed, commit `002376b`) — `X-Forwarded-For` is populated and resolves to the real per-client public IP, while `req.socket.remoteAddress` is Railway's internal `100.64.0.2`. This was the one prod-specific risk (without XFF the cap would collapse into one global bucket locking out all users) — confirmed safe. Did not run 7 real paid generations from prod (real money; a single test IP can't exercise the "other IP unaffected" case anyway) — the two things that could actually break in prod (cap math + per-client IP resolution) are both verified.
  - **Note (accepted):** leftmost XFF is client-spoofable, so a sophisticated farmer could rotate the header to bypass. That's more effort than the deviceId rotation this closes, and the failure mode is "some bypass possible," never "lock everyone" — the safe direction.

**Next action:** Items 3–7 (quality/product improvements) remain. In order: 3) change-verifier on all intensities + logging; 4) realistic-vs-dream toggle; 5) auto before/after share card; 6) trim redundant prompt language; 7) specific failure copy from Gemini block reason. Items 3/4/6 edit the transformation prompt/verifier (regression risk — keep on Claude, verify each with real photos before shipping). The two CRITICAL security items (1, 2) are done.

---

### Member profile + pre-trial questionnaire (PAUSED — moved to Queued, resume after security handoff)

**Goal:** One shared server-side member profile per account feeding all six AI features (Trainer, Nutritionist, Macro Tracker, Sleep Coach, Supplement Audit, Daily Brief), plus a 5–6 question "Let's build your plan" quiz inserted between account creation and the membership checkout screen (the boundary the bridge/hub/trial-gate task left). Full spec: `handoff-20260717-member-profile-questionnaire.md`.

**Prerequisite check:** confirmed — bridge/hub/trial-gate shipped and live-verified 2026-07-17, commit `f6edbee` (see entry below and git log).

**Acceptance criteria:** profiles table/column + GET/PATCH `/api/profile`; quiz UI at the post-signup/pre-checkout boundary with PostHog events; funnel data seeds the profile at account creation; each of the 6 features reads profile context additively (no prompt rewording, no model/safety/output-contract changes) with graceful degradation when profile data is missing; write-back hooks for factual updates only; backfill for existing users on next login; each feature verified live on absbyai.com before moving to the next; one full new-user run verified (generate → trial gate → quiz → checkout → feature pre-filled).

**Next action:** implement per Detailed Plan in the handoff doc, starting with schema + API.

### Completed — Fresh money & security audit (read-only, 2026-07-17)

Full post-revenue audit of `server.js`/`db.js`/client payment paths in `AUDIT_money_security_20260717.md`. No code changed. Top findings, ranked: **N1 CRITICAL** — `/api/stripe/create-checkout` (printed products) trusts client-supplied `priceInCents` and `fulfillProductOrder` never checks the paid amount, so a 50¢ payment ships a ~$54-cost canvas (fix: server-side price lookup + amount check); **N2** — no `trust proxy`, so all rate limits are one sitewide bucket (10 AI calls/min total, 20 auth attempts/15min total); **N3** — webhook 200s on fulfillment errors so Stripe never retries (charged-but-inactive risk). July 10's F1 credit double-spend is confirmed FIXED; F2–F5/F7 remain open (low). New endpoints (Macro Tracker v2, Supplement Audit, autoresponder) verified clean on auth/ownership/idempotency. **Next action:** N1 is now FIXED (see below); N2/N3 and F2–F5/F7 remain open (low) pending Dan's go-ahead.

### Completed — N1 FIXED: print-checkout pricing hole (2026-07-17, commit `1e7f9b5`)

The critical cash-loss hole from the audit is closed. `/api/stripe/create-checkout` now prices the Stripe session from `PRODUCT_CONFIG` server-side via a new shared `productVariant()` helper and **ignores** the client's `priceInCents`; it also requires `imageId` and 400s on unknown product/size (incl. the nonexistent 8×10-framed combo). `fulfillProductOrder` gained a belt-and-braces gate that refuses to submit to Printify when `amount_total < variant.price` or `currency !== 'usd'`, and the printed artwork is now rebuilt from `imageId` (`images-api.printify.com/<id>`) instead of the client-supplied `imagePreviewUrl` (dropped from session metadata; still read as a fallback only for pre-fix in-flight sessions).

- **Local:** stubbed-Stripe harness confirmed the $0.50 attack on a 16×20-framed canvas prices at 8700, unknown/8×10-framed → 400, missing `imageId` → 400, poster 11×14 → 2700; a session-status harness confirmed the $0.50 session is blocked before Printify (loud log), a non-USD session is blocked, and a full-price session reaches the Printify orders endpoint.
- **Live on absbyai.com:** 8×10-framed → 400 "Unknown product or size", missing `imageId` → 400 "Missing imageId", and the replayed $0.50 attack returned a session that renders **$87.00** in the live embedded Stripe checkout — server-side price wins. No payment was completed.
- **OPEN (unchanged from handoff):** the id-URL artwork form (`images-api.printify.com/<id>`) has not been confirmed against a real paid Printify order — the live path historically sent `preview_url` first and used the id-URL only as a fallback. One real end-to-end print order should confirm Printify accepts it; if not, take the trusted `preview_url` server-side. Also note N3 (webhook 200s on fulfillment error) is still open, so a rejected/failed order is not retried by Stripe — check Railway logs after the first real order.

### Recently shipped — Bridge + hub preview + trial gate (COMPLETE, live-verified 2026-07-17)

The post-generation funnel now routes email submit/skip → benefits bridge → logged-out/inactive-member hub preview. The preview shows the user's transformation, the full feature list, and the existing print flow as the first card. Feature taps route through a feature-specific signup gate and the existing 7-day Stripe membership screen; successful checkout resumes the selected feature. Active members keep their normal hub. Native apps show the existing purchase-unavailable treatment. `server.js` and Stripe trial mechanics were unchanged. All six requested PostHog events are present. Shipped in commit `f6edbee`.

- **Local verification:** JavaScript syntax, unique new ids, and `git diff --check` passed. Browser QA at 390×844 passed bridge layout, bridge → preview, print selector round-trip, logged-out prefilled trial signup/back, and inactive-member membership plans/back with no console errors.
- **Production verification:** Railway direct URL and `https://absbyai.com` served the new markers. A fresh live flow using the fictional male proof asset passed generation → email "No Thanks" → bridge → hub preview → trial signup gate; print card → existing selector → hub preview also passed. No console errors, email send, account creation, Stripe checkout, or charge occurred.

### Recently shipped — Macro Tracker v2 (COMPLETE, live-verified 2026-07-17)

Three upgrades to the photo-based macro tracker, shipped as one batch per `handoff-20260717-macro-tracker-v2.md` (project root): multi-photo meal analysis, meal-prep saved meals, and uneaten-food subtraction. Commit `a64a98d` (rebased on top of unrelated subscriber-update commits from a concurrent session).

- **Part A — multi-photo:** `/api/analyze-meal` now accepts up to 3 photos (`photos: [{base64, mime}]`), still accepts the legacy single-photo `photoBase64`/`photoMime` shape for the deployed native wrappers. Prompt instructs the model to itemize once across angles (overhead for contents, side for depth) and use the plate/fork as a visual ruler. Client has add/remove-angle UI capped at 3.
- **Part B — meal prep:** `mealPrep: true` + `servings` (2–20) on the same endpoint estimates the whole batch, then divides items/totals down to a single serving (order: `enforceMacroMath` → calibration → divide, so `MEAL_CALIBRATION` stays untouched). New `saved_preps` Postgres table + `GET/POST/PUT/DELETE /api/saved-preps` mirror the existing `/api/meals` sync pattern. Client: "Meal prep (batch)" mode toggle, servings input, saved-prep cards with one-tap logging (no photo, no AI call, free), reset/delete controls.
- **Part C — uneaten food:** client-only chips (¼/½/¾ fractions + per-item "left it" toggles) scale a logged meal instantly with no AI cost; new free `POST /api/refine-leftovers` (Haiku 4.5, 60s AbortController timeout) estimates `fraction_remaining` per line item from a leftover photo, server multiplies by `(1 − fraction)` and re-runs `enforceMacroMath`. Both paths keep the pre-adjustment snapshot for undo.
- **Live-verified on absbyai.com** (synthetic test images generated locally, not real food — model still correctly interpreted shapes/colors as food and gave sensible itemization):
  - Multi-photo: 2-angle request → one itemization referencing both "overhead footprint" and "side view" language, confirming the model actually used both angles rather than duplicating items.
  - Meal-prep math: batch totals 2631 cal ÷ 4 servings = 658 cal/serving (exact match); 735g chicken ÷ 4 = 184g/serving (exact match).
  - One-tap logging: saved a prep, logged 1 serving on the live page — remaining went 4→3, "Today's total" widget updated to the correct 658 cal.
  - Chips subtraction: applied "left half" to the same logged meal — 658 → 329 cal (exact 50%), daily total widget recalculated correctly, undo restored 658.
  - Leftover-photo endpoint: two live calls to `/api/refine-leftovers` both returned well-formed per-item fractions; verified the `(1 − fraction) × original` math against the returned numbers in both cases (e.g. fraction 0.3 on a 205-cal item → 144 cal, exact).
- **Deviation from plan:** none in scope/architecture. One pre-existing issue was flagged as a follow-up (main `/api/analyze-meal` fetch had no AbortController timeout, same bug class as the Supplement Audit hang) — **fixed** as a separate follow-up commit `50c51b4`: 4-min AbortController + 504 on timeout, live-verified on absbyai.com (endpoint responds correctly).
- **Pending / not done:** account-sync live-verification for `/api/saved-preps` (requires a logged-in test account; the localStorage-only path was fully verified, sync code follows the exact pattern of the already-working `/api/meals` sync). Eval harness + calibration retune remains a separate future task per the handoff (waiting on Dan weighing ~20 real meals).

### Recently shipped — Welcome Autoresponder on Resend (COMPLETE, live-verified 2026-07-17)

5-email welcome sequence (day 0/2/4/7/10) now sending live via Resend. Full spec: `HANDOFF_resend_autoresponder.md`.

- **Live-verified:** flipped on 2026-07-17; the first sweep delivered Email 1 ("Your future self is ready") to all 4 backfilled real subscribers — dan@socialresponsemarketing.com, danroseconsulting@gmail.com, edobediting@gmail.com, maceylinden@gmail.com — all "Delivered" in the Resend log. The 2 `@example.com` rows were correctly excluded. Confirmed the live send's From (`Dan from Abs by AI <dan@absbyai.com>`), Reply-To (`dan@absbyai.com`), body copy, working `absbyai.com` link, and unsubscribe footer. Emails 2–5 auto-send on cadence via the hourly sweep.
- **Sending identity:** sends from the already-verified root domain `absbyai.com`, NOT a `mail.absbyai.com` subdomain. Resend's free plan allows only 1 domain; a 2nd needs Pro ($20/mo), so Dan chose the free route. No Namecheap DNS changes were needed.
- **Code (commits `b9ff12e`, `c216c44`):** `WELCOME_EMAILS`, `sendWelcomeEmail` (Resend + RFC 8058 `List-Unsubscribe`), `welcomeSweep()` (send-then-advance, idempotent; hourly + 45s after boot, no-op unless `WELCOME_ENABLED=true`), sequence fields on `/api/subscribe` + boot backfill (excludes `@example.com`), `GET|POST /api/unsubscribe` (HMAC token + page), CAN-SPAM footer (Abs By AI, 3520 Cavu Rd., Georgetown, TX 78628).
- **Railway env set live:** `WELCOME_ENABLED=true`, `MARKETING_FROM=Dan from Abs by AI <dan@absbyai.com>`; `MAILERLITE_API_KEY` deleted (GROUP_ID left, harmless). To pause: set `WELCOME_ENABLED=false`.
- **Open security follow-up (non-blocking):** the old MailerLite API key was pasted in chat and only removed from Railway — it still exists in the unused MailerLite account. Rotate/delete it in MailerLite when convenient.


### Prior task (Supplement Audit) — COMPLETE (2026-07-17)

Done: single-call engine + async job/polling + counsel-language rebrand shipped (commit `baf25f6`), then a live 12-item test exposed a real hang bug — `callCounselSeat`'s fetch to Anthropic had no timeout (unlike the sibling helper at server.js:3795), so a stalled connection could hang the await forever (observed: one job sat at `status:"running"` for 15+ minutes with no error). Fixed with an `AbortController` 4-min-per-attempt timeout, same pattern as the existing helper (commit `751fe7b`).

**Live-verified after the fix:** re-ran the same 12-item stack (meds, budget, 12 supplements incl. a proprietary blend and a stimulant) end-to-end against production. Completed in 445s (first attempt hit the new 4-min timeout as the connection stalled again, retry succeeded) — confirms the fix converts an infinite hang into a bounded ~8-minute-worst-case retry instead. Result was well-formed: correct free-preview locking, safety officer flagged a RED interaction and named it in the verdict, savings math and next steps present. No JSON truncation across the 12-item stack.

Known follow-up (not a blocker, noted for awareness): the client gives up polling and shows "taking longer than expected" after 5 minutes, which is shorter than the ~8-minute worst case if both attempts stall. In that rare case the server-side job still finishes, but the client has already cleared the job id from localStorage, so the user would need to re-run rather than see the already-finished result. Low probability (requires both attempts to hit the connection stall) — only worth revisiting if it shows up in real usage.

### Last updated

2026-07-17 by Claude Code

---

## Queued (next up after the active task)

**Task:** `handoff-20260717-member-profile-questionnaire.md` — shared per-account member profile + 5–6 question pre-trial quiz; all features read/write it. Claude-owned (cross-feature architecture + Anthropic prompt code). This follows the currently active bridge/hub/trial-gate task.

---

## Handoff template

Use these fields in the active-task section when transferring ownership:

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
