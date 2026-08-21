# Abs By AI — Codex and Claude Code Coordination

Shared task board for Codex and Claude Code. This file is loaded in full into every
Claude Code message in this project, so it is kept deliberately minimal — Codex is used
rarely now, and most work happens directly in Claude Code sessions without needing a
handoff file. **Full project history, past decisions, and standing operational rules are
in [`AI_COORDINATION_ARCHIVE.md`](AI_COORDINATION_ARCHIVE.md)** (not auto-loaded — read it
only when you need historical context on a specific past task or decision). Git history
and commit messages remain the permanent record of code changes.

## Working rules

1. Read this file before starting project work involving Codex handoff.
2. Only one assistant owns implementation of the active task at a time. Don't overwrite
   or continue the other assistant's unfinished work without an explicit handoff or a
   user-requested review.
3. Update this file when starting work, hitting a milestone, getting blocked, handing
   off, or finishing — keep entries short and factual (what the next assistant needs to
   continue, not a transcript).
4. When a task is fully completed, committed, pushed, deployed, and verified, clear the
   active-task section back to `No active task`.
5. When you write a handoff doc for work that hasn't been executed yet, add a Key-priority
   dashboard task for it (mechanism + gotchas are in the `/dashboard-tasks` skill).
   When that work is fully executed, check it off in the same
   session — don't wait for Dan to click it.

## Status options

`No active task` · `Planning` · `Ready for implementation` · `Implementation in progress` ·
`Ready for review` · `Blocked` · `Complete — pending reset`

---

## Active task

### AD 1 REV-2 — second revision round shipped (2026-08-21, Claude Code)

All 10 of Dan's rev-2 items applied and redelivered (`ad1_rev2_16x9.mp4`, 4:31): smooth
supersampled Ken Burns (shake fixed), three AI-generated benefit clips (frames Dan-approved, then
**Veo 3.1 Fast via Gemini API** because **Replicate credit is DRAINED — Dan to top up**; safety-filter
workaround recorded in the skill), the two iCloud dad photos with motion, clean phone-image mockup,
gen-screen-with-photo slice, oversized AI-GENERATED box hiding the email form (Dan's rule: never show
email capture in an ad), custom scan+stats animation ("Goal Muscle GAIN" — confirmed via question;
plan not revealed), "lagging" caption fix, and the end card replaced by the real sample-person
generation flow (after ALONE). Session AI spend ≈ $5. Lessons 7–13 appended to the skill's
graphics-placement learning log. Awaiting Dan's rev-2 review; 9:16 builds on approval.


No active task.

---

## Handoff template

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
