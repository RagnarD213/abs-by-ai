---
name: video-task-sidebar-naming
description: "All video naming: edits <title> LFC|SFC|AD R<n>, setup <title> ... Setup, ad formats V/S/Sh, /revisions tasks <Editor> revisions; always say the title to Dan, code only alongside"
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

## Upload and setup tasks, and ad format variations (merged 2026-11-01)

Dan, 2026-10-01: "I want you to name all the tasks like I did the stop deadlifting shorts SFC setup. It should be at the beginning: a short 2-4 words describing the video, so I'll know what the title of the video is just from looking at those first few words. If it's long-form content, LFC. If it's short-form content, SFC. If it's an ad, then ad. Setup at the end."

**Why:** he scans a long pinned sidebar and needs to tell which video a task belongs to from its first words.

**How to apply:** rename the session at the start and state the name in every handoff starter prompt. Editing: `<2-4 word title> <LFC|SFC|AD> R<round>`. Upload and setup: `<2-4 word title> <LFC|SFC|AD> Setup`, e.g. `Stop Deadlifting SFC Setup`. Rule text: `AGENTS.md`, "Video task names in the sidebar". Related: [[handoff-starter-prompt-rule]].

**Ad format variations (Dan, 2026-10-02):** a task making other formats of an ad names the formats before `Ad`: `V` vertical, `S` square, `Sh` short cutdown, slash-joined. All three: `You're Not Too Old V/S/Sh Ad R1`; vertical only: `You're Not Too Old V Ad R1`. His words: "Going forward, use this format to name all variations where we're making the vertical square and short ... for all variations of ad tasks."

## Revision tasks (merged 2026-11-01)

Every revision task (a /revisions review of an editor's cut) renames itself at the start to the editor's first name plus "revisions": `Muhammad revisions`, `Zeeshan revisions`, `Waleed revisions`.

**Why:** Dan, 2026-10-01: "for this task and every task going forward, I want all revision tasks to be named the name of the editor, and then revisions." He finds tasks in the sidebar by the first words.

**How to apply:** call the session rename tool (`set_session_title`, session "self") as the first action of any /revisions run. This is separate from the video task names in AGENTS.md (`<title> <type> R<round>`), which are for our own editing and setup tasks. Related: [[editor-message-voice]], [[revision-docs-in-dans-voice]].

## Say the title, not the code (merged 2026-11-01)

Name every video by its recognizable title when talking to Dan; a code (RO-10, SL-15, RA-07) may follow in parentheses, never alone.
**Why:** Dan can't tell which video a code means (2026-10-17).
**How to apply:** chat, wrap-up boxes, recommendations, handoff summaries, review pages. Rule also in AGENTS.md.
