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

**Task:** None

**Owner:** None

**Status:** No active task

**Branch:** `main`

### Goal

No active task.

### Acceptance criteria

- Add criteria when a task begins.

### Work completed

- Shared coordination workflow created for Codex and Claude Code.

### Files changed

- `AI_COORDINATION.md`
- `AGENTS.md`
- `CLAUDE.md`

### Verification performed

- Coordination instructions reviewed for consistent ownership and handoff rules.

### Remaining work or blockers

- None.

### Decisions or context the next assistant needs

- Use this single file for the current project-wide task, even when that task touches multiple source files.
- Create separate task files under a future `tasks/` directory only if Codex and Claude Code intentionally work on different tasks in parallel branches or worktrees.

### Next action

When the next task begins, replace the placeholder active-task details, name one owner, and add task-specific acceptance criteria.

### Last updated

2026-07-16 by Codex

---

## Handoff template

Use these fields in the active-task section when transferring ownership:

- **Handing off from:** Codex or Claude Code
- **Handing off to:** Codex or Claude Code
- **Reason for handoff:** Implementation, review, investigation, or blocked work
- **Last completed step:** The most recent confirmed result
- **Exact next action:** One concrete action the receiving assistant can take immediately
- **Risks or cautions:** Uncommitted changes, sensitive areas, failed checks, or production concerns
