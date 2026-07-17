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

**Task:** Supplement Audit — replace five-call counsel engine with a single Sonnet 5 call, fix large-stack failure ("Load failed") via async job + polling, and remove all remaining Decision Counsel language

**Owner:** Claude Code (Sonnet 5, medium effort) — full implementation spec in `HANDOFF_supplement_audit_async_fix.md` (updated 2026-07-17 to include the single-call redesign; audit runs on claude-sonnet-5 at effort high, cap raised 10→25)

**Status:** Implementation in progress — code complete and tested locally, not yet pushed/deployed/verified live

**Branch:** `main`

### Goal

1. A 12-supplement audit completes reliably on mobile Safari. 2. All user-facing copy says "Supplement Audit" — no "counsel", "counselors", "deliberating", or "President's verdict" visible to users.

### Root cause (diagnosed 2026-07-17 by Claude Code)

`POST /api/counsel` (server.js:4874) runs all 5 Claude calls (4 seats @ 8000 max_tokens with one retry each, then the President @ 10000) inside ONE HTTP request with no client timeout handling (index.html:6666, `conveneAudit`). A 12-item stack makes each seat's output much longer; Sonnet 5 adaptive thinking counts toward max_tokens, so long runs can truncate → JSON.parse fails → retry doubles seat time. Dan's test ran ~5 minutes before mobile Safari showed "Load failed" — the connection was killed (proxy/browser timeout) before the server finished. The server work may even have completed after the client gave up; the result was just never delivered.

### Acceptance criteria

- Audit runs as an async job: POST starts it and returns a job id immediately; the client polls (~every 3–5 s) a status endpoint until done, then renders the report. No HTTP request lasts longer than a few seconds.
- If the phone locks or the tab backgrounds mid-run, reopening the page resumes polling (job id kept in localStorage) instead of failing.
- Seat max_tokens raised (suggest 12000 seats / 16000 President) so a 12-item stack doesn't truncate.
- All user-facing counsel language replaced ("The counsel is deliberating…" → "Your Supplement Audit is in progress…", "Meet your counsel" → e.g. "Meet your audit team", "Ask the counsel", "The counsel has ruled", counselor/President card labels reworded, membership blurb at index.html:2133). Internal variable/endpoint names (COUNSEL_*, /api/counsel, counsel_sessions) may stay.
- Verified live at absbyai.com with a 12-item stack.

### Work completed

- Single-call engine: `MASTER_SCHEMA` + `buildMasterSystemPrompt` (server.js) merge the four seat schemas/prompts + `PRESIDENT_SCHEMA`/`PRESIDENT_PROMPT` into one call (`claude-sonnet-5`, `effort: 'high'`, `max_tokens: 24000`). Old Phase 1 (parallel seats) + Phase 2 (President) orchestration deleted. `COUNSEL_MONTHLY_CAP` raised 10→25.
- Async job: new `audit_jobs` Postgres table (db.js) + in-memory `Map` fallback for local dev without `DATABASE_URL`. `POST /api/counsel` now validates/checks the cap, creates a job row, responds `{ jobId }` immediately, then runs `runSupplementAuditJob` detached. New `GET /api/counsel/job/:id` polls status (`running` / `done` + result / `error` + message), scoped to the owning user or anonymous-by-unguessable-id.
- Client (`index.html`): `conveneAudit` now POSTs, stores the job id in `localStorage` (`absbyai_audit_job`), and polls via new `pollAuditJobLoop` every 4s (drops ignored, gives up after ~5 min). `resumeAuditJobIfPending()` runs on every page load and reopens the loader if a job was left running; `restoreSession()`'s `showHub()` is now guarded so it doesn't clobber a resumed loader. `unlockCounselAfterSubscribe` (re-run after a free user subscribes) updated to the same job/poll pattern.
- Copy rebrand: loader text, "Meet your audit team", seat labels ("Lead Auditor" / "Head Auditor"), locked/unlocked report copy, follow-up card + button + answer label, membership blurb (index.html:2133) and landing footnote both now say 25/month. Server-side follow-up error strings reworded too. Grepped both files for residual counsel/President/deliberat strings — only internal identifiers, code comments, and console.warn text remain (explicitly allowed to stay per the handoff).
- Followup endpoint moved to `effort: 'high'`; `buildPresidentContent` simplified (dropped the now-dead `missingSeats` branch, kept as the case-file builder for follow-ups only).

### Files changed

- `server.js` — single-call engine, async job table/endpoints, followup tweaks
- `db.js` — `audit_jobs` table
- `index.html` — job-polling client, resume-on-reload, copy rebrand
- `AI_COORDINATION.md` (this plan)

### Verification performed

- `node -c` on server.js/db.js and a full inline-JS syntax check on index.html — clean.
- Local run with dummy Anthropic key (`.claude/launch.json` preview): confirmed `POST /api/counsel` returns `{jobId}` immediately, the job retries once then fails gracefully with a friendly error, `GET /api/counsel/job/:id` returns 404 for unknown ids, and the browser flow (loader copy, polling, error surfaced, form restored, localStorage cleared) all work end to end. Also confirmed the resume-on-reload path: a job id left in localStorage reopens the loader screen (not the hub) and silently returns to the landing screen on a 404.
- NOT yet verified: a real multi-item audit against the live Anthropic API (needs the real key — only available on Railway/production per prior notes on this repo).

### Remaining work or blockers

- Push to `main`, confirm Railway auto-deploy, then run a real multi-item (ideally 12-item) Supplement Audit live at absbyai.com to confirm the single Claude call succeeds and the full report renders for a member.

### Decisions or context the next assistant needs

- The async-job design and single-call redesign are both implemented as specified in `HANDOFF_supplement_audit_async_fix.md` — no open design questions remain, only live verification.

### Next action

Push to main, confirm Railway deploy, and verify a multi-item Supplement Audit end-to-end on absbyai.com (as a logged-in member, to see the full unlocked report). Once verified, reset this section to `No active task`.

### Last updated

2026-07-17 by Claude Code

---

## Handoff template

Use these fields in the active-task section when transferring ownership:

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
