---
name: cutout-frame-and-gap-traps
description: "RO-37 R3 (2026-10-30): why cut-outs from real footage look sloppy in spots: a one-frame decode lag, and closed gaps between arm and body; both fixed, audit per shot"
metadata:
  type: project
---
Dan on the RO-37 key: "generally looks good, but there are some spots where it's not that good." Two causes, both invisible on single test frames.

1. `ffmpeg -ss ... -f rawvideo` doubles the first frame after some seek points, so a matte and a picture decoded from different starts sit one frame apart (about 6 px on a moving arm). Add `-fps_mode passthrough` to every sequential decode.
2. BiRefNet closes the gaps between arm, hand and torso, so background stays solid there and an edge-band refiner never reaches it. A colour test inside the cut-out takes it back out (`gapfix.py`). A clean plate failed: the body covers 80% of it.

**How to apply:** on any cut-out film, audit the delivered picture per shot with a fresh reviewer on zoomed worst frames, and fix before moving Dan to the corner. Recipe: `.claude/skills/_shared/chroma-key/README.md`. Related: [[chroma-key-standard]], [[longform-greenscreen-standard]].
