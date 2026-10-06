---
name: no-swipe-sound-effect
description: Dan 2026-09-23: never use the swiping/whoosh sound effect in any video, for anything; transitions copy Muhammad's (silent flashes)
metadata:
  type: feedback
---

Never put a swipe / whoosh / swish / riser sound effect in any video, on any transition or graphic, from any source. Dan (2026-09-23, RO-05): "I really hate that swiping sound effect. We need to remember this going forward: never, ever use that swiping sound effect for anything."

**Why:** it reads as cheap and it is the first thing he noticed on a cut he rejected; Muhammad's own flash transitions are silent.

**How to apply:** `_shared/sfxlib.py` `whoosh()` / `riser()` now raise; don't work around them. Build transitions like Muhammad's ab-wheel video (silent white/blue bloom flashes, in-card whip-pans). Rule text lives in `_shared/VIDEO-RULES.md` "RO-05 rejection". Related: [[ro05-salad-cut-rejected]], [[video-editing-cost-quality-feedback]].
