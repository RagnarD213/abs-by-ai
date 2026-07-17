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
