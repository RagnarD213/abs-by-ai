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

**Status:** `No active task`

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
- **Deviation from plan:** none in scope/architecture. One pre-existing, out-of-scope issue noticed and *not* fixed here: the main `/api/analyze-meal` fetch call still has no AbortController timeout (same bug class as the Supplement Audit hang, commit `751fe7b`) — flagged as a separate follow-up task, not touched in this commit since it predates this diff.
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

## User-authorized parallel task

**Status:** `Blocked`

**Owner:** Codex

**Task:** Screen-1 proof strip + locked-result teaser, per `handoff-20260717-proof-strip-locked-teaser.md`.

**Goal:** Improve top-of-funnel upload confidence and make the out-of-credits result/paywall more compelling without changing generation, credits, or Stripe logic.

**Acceptance criteria:** Shortlist 2–3 mixed-gender before/after pairs for Dan's approval; add an honest, compact, lazy-loaded rotating proof strip; add the torso-blurred locked teaser and dynamic body-fat paywall headline; add the three specified PostHog events; verify locally. Do not commit or push until Dan explicitly authorizes it because Claude Code is concurrently modifying the repository.

**Completed:** Implemented and locally verified the locked-result teaser, dynamic body-fat headline, accessible click/keyboard paywall focus, and `locked_teaser_shown` analytics. Mobile visual QA passed at 390×844. No generation, credits, Stripe, native-app purchase classes, or Macro Tracker code was changed.

**Remaining / next action:** Dan must approve the shortlisted example pairs (Dan, Brittany, and/or the flexing male pair). Then Codex will export approved web assets, implement and verify the rotating proof strip plus `proof_strip_seen`, and add the final `locked_teaser_shown`/proof-strip verification. Do not commit or push until Dan explicitly authorizes it.

**Coordination caution:** This parallel task was explicitly requested by Dan on 2026-07-17. Preserve Claude Code's active-task ownership and avoid its Macro Tracker code areas.

---

## Queued (next up after the active task)

**Task:** Onboarding funnel revamp — approved 2026-07-17, split into three handoffs (1 and 2 independent of each other; 3 depends on 2):

1. `handoff-20260717-proof-strip-locked-teaser.md` — screen-1 proof strip + blurred-abs locked-result teaser. Routine UI; Codex-eligible. Needs Dan's approval on example images.
2. `handoff-20260717-bridge-hub-trial-gate.md` — replace print-first screens 4–5 with a benefits bridge screen → logged-out hub preview (print upsell demoted to a top card) → trial gate reusing the existing Stripe 7-day trial. Codex-eligible.
3. `handoff-20260717-member-profile-questionnaire.md` — shared per-account member profile + 5–6 question pre-trial quiz; all features read/write it. Claude-owned (cross-feature architecture + Anthropic prompt code).

Each handoff contains all settled decisions, model/effort recommendations, and a ready-to-paste starter prompt. Implementation not started.

---

## Handoff template

Use these fields in the active-task section when transferring ownership:

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
