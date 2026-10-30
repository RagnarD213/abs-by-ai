---
name: blind-google-vs-codex-images
description: 10-30: every clip start frame made by both Codex and Google, thumbnails 5 Codex + 3 Google, all unlabeled; answer "which did I choose most" only when asked
metadata:
  type: feedback
---

Dan, 2026-10-30, after upgrading to Google AI Ultra: two start frames for every clip (one Google, one Codex), never say which; thumbnails stay five Codex plus three unlabeled Google; other images get a few Google alternatives unless impractical (a background in a video). Later he will ask "Which ones did I choose the most?"

**Why:** the 10-01 Nano Banana Pro vs Codex test ended "everything is now Codex", but the Ultra plan makes Google images free of Codex allowance, and he wants fresh evidence, not a rule from one test.

**How to apply:** use `.claude/skills/_shared/blind-image/blind.py` (add, build, pick, scorecard); Google runs in Flow on the subscription (`FLOW-IMAGE-RUNBOOK.md`, not yet mapped as of 10-30); never leak source in chat, file names or pages; log every pick; answer the scorecard only on request. Shirtless refusals are logged data. Rule: `IMAGE-GENERATION.md` "Blind Google test". Related: [[veo-subscription-first]], [[codex-image-gen-from-claude]].
