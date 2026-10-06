---
name: shoot-923-format
description: "9/23/2026 shoot is FX30 4K S-Cinetone (not log), one dual-mono lav stream; C1716-20 are portrait-rotated shorts on a tabletop set; roll map in Docs/SHOOT_923_FOOTAGE_REPORT.md"
metadata:
  node_type: memory
  type: project
  originSessionId: 247adff9-a203-475c-8ec7-264e57559a01
  modified: 2026-09-24T00:18:18.372Z
---

The **9/23/2026 shoot** (`/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/`,
rolls **C1689 to C1720**) is Sony FX30 3840x2160 29.97p **S-Cinetone** with **one stereo stream, dual-mono**
(single lav, L = R). C1689 to C1715 are 16:9 on a green mottled backdrop set (tube light left, plant + bulb right);
**C1716 to C1720 are portrait-rotated** (rotation -90, decode 2160x3840) on a tabletop set with two cyan tubes.
C1640 and C1688 in that folder are leftovers from older cards. The camera clock is about 12 h off.

**Why:** the 8/28 rules (S-Log3 LUT, four mono tracks) do not transfer; grading this footage through the log LUT
or mapping `a:1` would be wrong.

**How to apply:** grade as Rec.709; pull audio with `pick_lav.py` (it prescribes the mid pan). Full roll map and
measurements: `Docs/SHOOT_923_FOOTAGE_REPORT.md`. Related: [[shoot-828-slog3-format]], [[shoot-audio-two-mics]],
[[framing-standard-hair-anchored]].
