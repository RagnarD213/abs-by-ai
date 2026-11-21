---
name: chroma-key-efficiency
description: Dan 2026-10-24: green-screen keys must be cheap like Codex's; never re-key whole clips to test; use calibrate.py excerpts + keyonce.py
metadata:
  type: feedback
---

Key green-screen footage the efficient way. Dan, 2026-10-24, on RO-24 round 2 (Claude's port of the house key, ~10 s a frame end to end, three full keys per clip, a full-film rewrite, many hours of shared render slots): "The chroma key looks good, but it wasn't better than what Codex did, and Codex did this in much less time. The amount of local resources and tokens you consumed during the chroma key was not acceptable. Look at what Codex did with the chroma key, and then take an efficient approach like Codex next time."

**Why:** the Mac and its render line are shared by every editor; Dan stopped other videos' work for this key twice. Quality equal to a cheaper run is not a win.

**How to apply:** before any key, read how Codex keyed the most recent green-screen job and the shared tooling in `.claude/skills/_shared/chroma-key/` (README; results doc `Handoffs/results-20261021-cheap-key.md`): calibrate settings on 2-3 s excerpts at the hardest moments (`calibrate.py`), key each piece once (`keyonce.py`, never re-key to try a setting), use the bit-identical faster stage 1 / 1.5, at most the render queue's core allowance. Key only the frames the edit uses (plus handles). Estimate the key's CPU-hours before starting and say it. Related: [[gate-the-harm-not-just-the-fix]].
