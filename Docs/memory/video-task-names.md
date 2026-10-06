---
name: video-task-names
description: 10-01: video tasks are named "<2-4 word video title> <LFC|SFC|AD> R<n>" for edits and "... Setup" for upload/setup tasks
metadata:
  type: feedback
---

Dan, 2026-10-01: "I want you to name all the tasks like I did the stop deadlifting shorts SFC setup. It should be at the beginning: a short 2-4 words describing the video, so I'll know what the title of the video is just from looking at those first few words. If it's long-form content, LFC. If it's short-form content, SFC. If it's an ad, then ad. Setup at the end."

**Why:** he scans a long pinned sidebar and needs to tell which video a task belongs to from its first words.

**How to apply:** rename the session at the start and state the name in every handoff starter prompt. Editing: `<2-4 word title> <LFC|SFC|AD> R<round>`. Upload and setup: `<2-4 word title> <LFC|SFC|AD> Setup`, e.g. `Stop Deadlifting SFC Setup`. Rule text: `AGENTS.md`, "Video task names in the sidebar". Related: [[handoff-starter-prompt-rule]].

**Ad format variations (Dan, 2026-10-02):** a task making other formats of an ad names the formats before `Ad`: `V` vertical, `S` square, `Sh` short cutdown, slash-joined. All three: `You're Not Too Old V/S/Sh Ad R1`; vertical only: `You're Not Too Old V Ad R1`. His words: "Going forward, use this format to name all variations where we're making the vertical square and short ... for all variations of ad tasks."
