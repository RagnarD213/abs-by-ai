---
name: thumbnail-standard-codex-in-setup
description: "Dan 2026-10-02: thumbnails = 5 choices (1 pool, 1 studio, 3 AI designs of Codex's choice), made inside the Claude setup task via Codex CLI, GPT-6.1 Sol high"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9f163f86-9dae-43f9-8118-8897eb6861f8
  modified: 2026-10-02T16:34:55.571Z
---

Standard for every upload and setup task unless Dan says otherwise for a video: the Claude setup task makes five thumbnail choices itself by calling Codex in the command line on his subscription (`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`): one pool-shoot photo, one studio-shoot photo, three AI-generated images, each a unique design of Codex's choice. Show five, stop for his pick, then upload. No Gemini or other outside image model. GPT-6.1 Sol at high effort is the default for all thumbnail tasks.

**Why:** Dan set it when approving RO-16 (he dictated "GPT 6.1 Sold", meaning Sol). It replaces the 09-30 mix (pool, two studio, screenshot, designer choice) and the separate Codex thumbnail handoff.

**How to apply:** one Claude handoff per finished video covering thumbnails and setup; its starter prompt says "Use the Codex subscription to generate the images." Rule text: VIDEO-RULES.md first section and AGENTS.md. Related: [[organic-setup-codex-thumbnail-split]], [[cover-photo-selection]], [[thumbnail-design-system]].
