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

**Task:** Welcome Autoresponder on Resend — 5-email welcome sequence sent over ~10 days from a dedicated marketing subdomain. Full spec: `HANDOFF_resend_autoresponder.md`.

**Owner:** Claude Code (Opus 4.8, medium effort)

**Status:** Implementation in progress — server code complete, tested locally (integration test passes), committed + pushed. Provider config (Resend subdomain + Namecheap DNS + Railway env) and live verification still pending.

**Branch:** `main`

### Goal

Every new email signup — and the 4 existing real subscribers (backfilled) — automatically receives a 5-email welcome sequence (day 0/2/4/7/10) via Resend, from `mail.absbyai.com`, with a working unsubscribe. Test `@example.com` rows are never emailed.

### Work completed (code)

- `server.js`: `WELCOME_EMAILS` (5 emails ported from `MAILERLITE_BUILD.md`), `sendWelcomeEmail` (Resend, `MARKETING_FROM`, `Reply-To: dan@absbyai.com`, `List-Unsubscribe` one-click headers), `welcomeSweep()` (clone of `trialReminderSweep` send-then-advance, hourly + first pass 45s after boot), sequence fields (`welcomeStep`/`welcomeNextAt`/`welcomeSentAt`/`unsubscribed`) initialized on `/api/subscribe` and lazily backfilled on boot + in-sweep (excludes `@example.com`), `GET|POST /api/unsubscribe` with HMAC-signed non-enumerable token + confirmation page, CAN-SPAM postal-address footer.
- **Safety gate:** the sweep is a no-op unless `WELCOME_ENABLED=true` (defaults off), so the deployed code sends nothing until the subdomain is verified and the switch is flipped. `MARKETING_FROM` falls back to the transactional identity if unset.
- Local integration test (mocked Resend): Email 1 sends to a real user, `@example.com` excluded, correct from/reply-to/headers/footer, idempotent re-sweep, one-click unsubscribe works, forged token rejected, unsubscribed user gets nothing further. All pass.

### New env vars (Railway — set before enabling)

- `MARKETING_FROM` = `Dan from Abs by AI <dan@mail.absbyai.com>`
- `MARKETING_ADDRESS` = real business mailing address (Dan to provide; placeholder in code until then)
- `WELCOME_ENABLED` = `true` (flip ON only after `mail.absbyai.com` is verified in Resend)
- Optional: `MARKETING_REPLY_TO` (defaults `dan@absbyai.com`), `UNSUBSCRIBE_SECRET` (falls back to an existing secret)
- Remove/rotate `MAILERLITE_API_KEY` (was pasted in chat; sync already no-ops without it).

### Remaining work

1. Resend: add & verify sending subdomain `mail.absbyai.com` → get DKIM/SPF/MX records.
2. Namecheap → absbyai.com → Advanced DNS: add those records (do NOT touch the root `@` SPF). Standing DNS auth covers this.
3. Railway: set the env vars above (incl. real `MARKETING_ADDRESS` from Dan), remove `MAILERLITE_API_KEY`, set `WELCOME_ENABLED=true`.
4. Verify live on absbyai.com: real signup receives Email 1 in the inbox (not spam); unsubscribe works. Optionally shorten delays to watch 1→5 (spec §6), then restore.

### Blocked on / needs from Dan

- Real physical mailing address for the CAN-SPAM footer (`MARKETING_ADDRESS`).
- Confirmed: backfill all 4 real subscribers into the sequence.

### Next action

Verify the `mail.absbyai.com` subdomain in Resend and add its DNS records at Namecheap; then set the Railway env vars (with Dan's real address) and flip `WELCOME_ENABLED=true`; then verify a real signup end-to-end on absbyai.com.

### Prior task (Supplement Audit) — status

Code complete and pushed (commit `baf25f6`, single async engine). Live-verified a small audit end-to-end. A 12-item live test then exposed a real bug: `callCounselSeat`'s fetch to Anthropic had no timeout (unlike the sibling helper at server.js:3795), so a stalled connection hangs the await forever — the job sat at `status:"running"` for 15+ minutes with no error. Fixed by adding an `AbortController` with a 4-min-per-attempt timeout (same pattern as the existing helper), pushed in a follow-up commit. Still need to re-run a 12-item live audit against the fixed code to confirm it now completes or fails cleanly within ~8 minutes (2 attempts × 4 min) instead of hanging. Not blocking the Welcome Autoresponder task above.

### Last updated

2026-07-17 by Claude Code

---

## Queued (next up after the active task)

**Task:** None currently queued. (The Welcome Autoresponder moved to the active-task section above; the Supplement Audit's remaining live verification is tracked there too.)

---

## Handoff template

Use these fields in the active-task section when transferring ownership:

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
