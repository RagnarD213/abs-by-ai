---
name: broll-library-first
description: Dan 2026-10-01: always scan the clip library for our real B-roll and existing AI clips; B-roll beats stock or AI; new AI clip only when nothing fits; applies to editor revisions too
metadata:
  type: feedback
---

For every video (ours or an editor's), scan the clip library line by line for places to use our real B-roll and our existing AI clips. Preference order: our real B-roll, then an existing AI clip of ours, then stock, and a new AI clip last.

**Why:** Dan, 2026-10-01, after the B-roll library was finished: "always look for ways to use B-roll in our videos. Generally, it's better to use B-roll than stock or AI clips when we have the B-roll. I also want you to look through our existing AI clips library and look for opportunities to use those clips before requesting a new one."

**How to apply:** /revisions workflow step 6 (library pass) and VIDEO-RULES "Clip library first". `clip_library.py find` is weak on multi-word queries: search one keyword at a time or filter `Media/clip-library/catalog.json` directly, and look at the contact preview. Related: [[clip-library]], [[editor-shorts-graphics-kit]].
