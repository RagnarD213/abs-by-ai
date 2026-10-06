---
name: revision-task-naming
description: "Every /revisions task is named \"<Editor name> revisions\" in the sidebar (Dan, 2026-10-01)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 50fa0eb6-3880-460e-9b3b-e637315900ea
  modified: 2026-10-01T22:25:15.018Z
---

Every revision task (a /revisions review of an editor's cut) renames itself at the start to the editor's first name plus "revisions": `Muhammad revisions`, `Zeeshan revisions`, `Waleed revisions`.

**Why:** Dan, 2026-10-01: "for this task and every task going forward, I want all revision tasks to be named the name of the editor, and then revisions." He finds tasks in the sidebar by the first words.

**How to apply:** call the session rename tool (`set_session_title`, session "self") as the first action of any /revisions run. This is separate from the video task names in AGENTS.md (`<title> <type> R<round>`), which are for our own editing and setup tasks. Related: [[editor-message-voice]], [[revision-docs-in-dans-voice]].
