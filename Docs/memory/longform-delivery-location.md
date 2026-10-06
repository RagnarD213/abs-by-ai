---
name: longform-delivery-location
description: Finished long-form videos go in the project folder "claude edited long form content/"; working files stay on the Seagate
metadata:
  type: feedback
---

Dan's instruction, 2026-08-21: **"Going forward, save your final videos in the project folder rather than on the hard drive."** He renamed the first delivery folder to `claude edited long form content/` and moved it to the project root, then asked for every earlier Claude-edited long-form video to be consolidated there too (invest-health v3 and the meal-prep split-screen demo became `04 -` and `05 -`).

The split is: **finished `FINAL_*.mp4` + `.srt` + chapters + the recipe files (`edl.json`, `ranges.py`, `chips.py`) go in the project folder**; raw rolls, extracted audio and `clips_graded/` stay on the Seagate at `_edit_work/`.

**Why:** he wants deliverables where he actually looks for them, not on an external drive he has to go find. Working files are tens of GB and the boot disk runs ~98% full, so those must not follow.

**How to apply:**
- Deliver to `claude edited long form content/<NN - Title>/`, continuing the numbering.
- **Never delete `_edit_work/clips_graded/`** — it IS video-use's segment cache, and deleting it turns a one-beat revision back into a full re-render.
- The repo is public ([[repo-is-public]]) and this folder is now inside it. `.gitignore` carries `claude edited*/` plus a global `*.mp4`/`*.mov`/… rule, because folder-name rules have failed twice after renames. Still run `git check-ignore -v` on the delivery folder after any rename.
- Related: [[bias-toward-action]].
