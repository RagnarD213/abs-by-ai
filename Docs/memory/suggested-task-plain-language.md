---
name: suggested-task-plain-language
description: spawn_task chips (suggested tasks) must have a plain-language title and tldr Dan can understand; technical detail only in the hover prompt
metadata:
  type: feedback
---

When flagging a side task with spawn_task, write the `title` and `tldr` in everyday words (what went wrong, what the new session will do, why it matters). No file names, function names, flags or code in them. The full technical detail goes only in `prompt` (shown on hover).

**Why:** Dan (2026-10-16) could not understand the card text (a label-gate sampling fix) and kept asking in chat to have it explained. He wants the card readable on its own.

**How to apply:** Two short sentences in the tldr; translate any unavoidable term in the same sentence. Test: would a smart friend who does not code get it? Also see [[explain-simply]]. Rule is also in CLAUDE.md.
