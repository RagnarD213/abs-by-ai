---
name: video-task-sidebar-naming
description: "10-01: every video editing session renames itself \"<short title> LFC|SFC|AD R<n>\" in the sidebar"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4bdf057f-40fb-404d-996a-767a7c74d594
  modified: 2026-10-01T14:34:08.066Z
---

Every video editing session names itself in the sidebar as `<short video title> <type> R<round>`, for example `Calories Don't Matter LFC R1`.

- Type codes: `LFC` = long-form content, `SFC` = short-form content (shorts, reels), `AD` = an ad.
- Use as much of the real title as fits the sidebar (about 3 to 5 words), then the code, then the round number.
- Rename at the start of the session with `set_session_title("self", ...)`; a new round is a new session with the next R number.

**Why:** Dan (2026-10-01) runs many video sessions at once and needs to tell them apart at a glance.

**How to apply:** any session that edits, revises or reviews a video, Claude or Codex. Starter prompts in handoffs should state the title to use. Planning chats use [[prioritize-session-naming]] style instead ("Daily Priorities MM-DD-YYYY", rule lives in the /prioritize skill). Rule text also in `AGENTS.md`.
