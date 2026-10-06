---
name: vertical-centering-standard
description: 10-03 Dan's standard camera for every 9:16 vertical: crop lands on him after each cut, then holds inside a 3.3 % dead band
metadata:
  type: feedback
---

In every vertical (9:16), the crop that follows Dan lands centred on him on the first frame after each cut, then stays still until his head is 3.3 % of the crop's width off centre (20 px on the kit's 608 px crop), and only then follows, slowly. `kit_track.py --tolerance 20` is the default; the method and numbers are in `.claude/skills/_shared/framing-motion.md` ("Vertical talking head: land on him, then hold") and VIDEO-RULES.

**Why:** Dan compared two RO-10 first minutes (a third calmer vs two thirds calmer) on 2026-10-03 and said: "I like the calmest one, the two-thirds calmer. That looks the best to me... Let's make this our standard way of centering for verticals going forward. I feel like this is better than what we were doing." On 10-01 he had called the old tracking "excessive and distracting", and he also rejected a crop that never moves (he left the frame).

**How to apply:** Use it for the talking-head crop of every new vertical, Claude or Codex, without asking. Squares keep the steadier per-shot fixed centre; horizontal stays static. Do not reopen approved or published verticals. Related: [[framing-standard-hair-anchored]], [[review-page-what-i-decided]].
