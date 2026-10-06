---
name: untagged-video-bt601-trap
description: Editor masters have no colour tags; ffmpeg decodes them as BT.601 but VLC/browsers show BT.709 — fit grades and lift clips with in_color_matrix=bt709
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 51ffdd92-ff06-4ef0-9211-2a7dfd518088
  modified: 2026-09-14T00:57:21.051Z
---

Muhammad's HD masters (Ad 3 v6, Ad 4 V4, Ad 5 V3 — checked 2026-09-13) carry **no colour tags**. ffmpeg's scaler reads an
untagged file with the **BT.601** matrix; VLC and browsers read untagged HD as **BT.709**. Any grade fitted, or clip lifted,
from the ffmpeg default decode is therefore shifted against his ad as Dan actually sees it — darker, muddier, less vivid skin —
while every ffmpeg-based comparison reads it as a match (both sides share the wrong decode).

Dan rejected the Ad 3 vertical's colour on exactly this (2026-09-13, VLC side by side): *"Muhammad's look brighter, like the
colors are more vivid. I look more tan. It's just better color correction overall."*

**Why:** the in-house check compared our file to his through the same default decode, so the error cancelled out of every number.

**How to apply:** whenever a script decodes an editor's master to RGB — grade fitting (`zlut.py`), clip lifts (`lift3.py`),
colour comparisons, thumbnails pulled from his frames — force `scale=in_color_matrix=bt709:in_range=tv` (or check the file is
tagged first with ffprobe `color_space`). Verify colour against his file decoded as BT.709. A single global LUT also could not
follow his grade, which varies by section (his Ad 3 opening is warmer) — see [[muhammad-trial-edit-analysis]] and the
shortad-from-longform skill's Ad 3 section. Related: [[editor-audio-untouched]].

**Second trap, same decode (2026-09-14, Ad 3 16:9 patch):** even with `in_color_matrix=bt709`, ffmpeg's default yuv→rgb24
path reads ~1.7 levels dark (round trip yuv→rgb→yuv biased −1.72 Y). Add `flags=accurate_rnd+full_chroma_int` to the
scale filter on decode AND encode — then the round trip is exact. A fit hides it (both sides share the bias); a patch
spliced into the editor's own frames shows it as a 2-level brightness step.
