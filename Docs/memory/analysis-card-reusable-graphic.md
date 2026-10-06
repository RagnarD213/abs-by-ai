---
name: analysis-card-reusable-graphic
description: Dan's 2026-09-18 instruction to REUSE the body-fat / fat-to-lose / muscle-to-gain analysis card from RA-01 in future videos; it lives in .claude/skills/_shared/adkit/analysis_card.py
metadata:
  type: feedback
---

Approving RA-01 "The AI Trick That Got Me Abs" (2026-09-18), Dan singled out one graphic: *"I especially like this
graphic that you made with the things to lose body fat and gain muscle. Let's make this something that we reuse in
future videos. I really, really like that. I think that illustrated it better than we did in past videos."*

**Why:** it shows the product's analysis step (scan line over his AI image → BODY FAT / FAT TO LOSE / MUSCLE TO GAIN
bars → YOUR WORKOUT PLAN) more clearly than the older stats-scan and app-screen inserts.

**How to apply:** on any line that says the app analyses the picture and builds a plan, render it with
`.claude/skills/_shared/adkit/analysis_card.py` (9:16 / 16:9, README beside it) rather than inventing a new graphic.
No printed numbers in it, one label chip placed by person mask, same person as the video's before/after. Extend the
kit (1:1, new cards) instead of forking it. Related: [[three-role-video-pipeline]], [[ad-copy-no-unbelievable-claims]].
