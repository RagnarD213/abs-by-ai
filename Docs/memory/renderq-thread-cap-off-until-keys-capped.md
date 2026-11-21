---
name: renderq-thread-cap-off-until-keys-capped
description: "10-21 renderq v3: ffmpeg -threads cap built but OFF; capped encodes ran 2.5-3x slower while other work was uncapped"
metadata:
  node_type: memory
  type: project
  originSessionId: fa83b8fe-06b1-4665-8456-7013414d5b4b
  modified: 2026-10-21T21:59:22.269Z
---

Render queue v3 (live 2026-10-21 16:48) admits by a core budget (heavy 4, light 2, quick 2 of 8) and a memory budget, exports RENDERQ_CORES, and has a wrapper `-threads` injection that is OFF (`THREADS_DEFAULT = False` in renderq.py; `GATE_THREADS=1` turns it on per process tree).

**Why:** bench10 on 10-21 at load 70-200: a 4-thread-capped x264 pass ran 2.5-3x slower than uncapped, because chroma-key pools (cv2/numpy threads) and work outside the queue were uncapped and took the CPU share. Floor of 1 heavy (the plan) ran the batch 2.1x slower than two at a time, so the floor is 2. Swap "in use" is not a gate (sticky for hours); swap growing is.

**How to apply:** turn the cap on only after Phase 2's chroma key sizes pools from RENDERQ_CORES and caps cv2 threads per worker, then re-run `renderq/bench10.py OLD NEW --two` and keep it only if the batch is within 15% of `two`. Results: `Handoffs/results-20261021-renderq-v3.md`. Related: [[overnight-edit-queue]], [[setup-encodes-low-priority]].
