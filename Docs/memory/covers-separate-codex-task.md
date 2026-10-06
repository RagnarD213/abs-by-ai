---
name: covers-separate-codex-task
description: "Shorts editing tasks never make cover images; covers are a separate smaller task, mostly run by Codex (Dan 2026-09-25)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 920a8b4f-ee37-46a0-8a25-fecb42125c74
  modified: 2026-09-25T21:35:44.800Z
---

Do not build cover images as part of a shorts (or dedicated-short) editing task. Covers are their own, smaller task, and Dan has Codex make most of them. An editing session only lists which shorts still need covers.

**Why:** Dan, 2026-09-25, after rejecting 9 of the 10 SL-04 covers: "I want to save tokens by doing this within a smaller context task" and "I want to have Codex do most of these." He kept only short 2 cover B.

**How to apply:** never run `/coverimage` inside an editing job; the rule is written into `Handoffs/video-editing/00-RULES.md`, the DS/SL job docs, `/shorts` and `/coverimage`. Related: [[action-items-at-bottom]].
