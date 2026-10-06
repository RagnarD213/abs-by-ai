---
name: shoot-828-slog3-format
description: "The 8/28/2026 shoot is 4K S-Log3 in THREE roll families: C1650-53 landscape + four mono tracks (lav a:1); C1654-72 (ads + dedicated shorts) PORTRAIT camera (rotation -90, decodes 2160x3840) + one dual-mono stereo stream; C1673+ landscape stereo. Always pick_lav.py per file"
metadata: 
  node_type: memory
  type: project
  originSessionId: c7f90903-a90e-4ca9-bb31-257910a8e32c
  modified: 2026-09-02T15:10:39.711Z
---

The **8/28/2026 shoot** (`/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/`, rolls **C1650–C1685**) was recorded **3840×2160, S-Log3 / S-Gamut3.Cine, 29.97p, with FOUR mono LPCM streams**. Every earlier Jeff roll (8/3, 8/14) was 1080p S-Cinetone stereo, so the old grades and the `pan=mono|c0=c1` audio rule do not transfer as written.

**Why:** the flat log image looks washed out until converted, and a fresh "fit a curve" grade on log footage lands wrong; the lav is now stream **a:1** (SNR 40 dB), a:0 is the far mic 7.2 ms late and polarity-inverted, a:2/a:3 are silent.

**How to apply:** grade with the numpy-built 33³ `.cube` (`.claude/skills/ad-edit/reference/website-video/make_lut.py`, exposure 1.45×, `eq=saturation=0.88`, `lut3d=...:interp=tetrahedral`) — validated by eye against the approved Ad 3 skin on 2026-09-01. Map audio with `-map 0:a:1` (or `[0:a:1]` in a filter graph), never `-ac 1` on the default stream. Which roll is which: `tx/probes.json` in `/Volumes/Extreme/_edit_work/website-video-828/` holds the first 100 s of every roll ≥55 s (C1650 = website video, C1652/C1653 = long-form talking, C1654–C1672 = dedicated shorts (vertical-rotated camera), C1673+ = exercise b-roll). See [[shoot-audio-two-mics]].


**Corrected 2026-09-16 (first edit of C1663, RA-01):** the four-mono layout is ONLY C1650–C1653. **C1654–C1672** (the
16 short-form ads and the dedicated shorts) were shot with the camera **physically rotated**: stored 3840×2160 with
rotation side-data −90, ffmpeg autorotates to **2160×3840 portrait** (never `-noautorotate`, never add `transpose`),
and their audio is **one stereo stream, dual-mono** (L = R = the lav; `pick_lav.py` prescribes
`-map 0:a:0 -af "pan=mono|c0=0.5*c0+0.5*c1"`). C1673–C1685 (exercise b-roll) are landscape with one stereo stream.
Dan is full-body and only ~35 % of the frame width on the portrait rolls, so hair-anchored FAR/NEAR crops upscale
~1.9×/~2.3×. Full findings: `Docs/SHOOT_828_FOOTAGE_REPORT.md`.
