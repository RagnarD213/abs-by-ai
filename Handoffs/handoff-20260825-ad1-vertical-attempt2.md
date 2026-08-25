# Handoff: Ad 1 vertical (9:16) — ATTEMPT 2, exact copy of Muhammad's final

- **Handing off from:** Claude Code (2026-08-25 session — attempt 1, REJECTED)
- **Handing off to:** Claude Code (fresh session)
- **Reason for handoff:** Re-execution after Dan rejected attempt 1 ("truly awful"). Fresh
  context on purpose; the failure analysis is fully encoded in the skill.
- **Last completed step:** Attempt 1 delivered and rejected; all five complaints
  root-caused with measurements; `/shortad-from-longform` rewritten with [R1] hard rules
  (commit `5052977`); dashboard check-off reverted.
- **Exact next action:** Invoke **`/shortad-from-longform`** and follow it. This document
  adds the Dan-decisions and the two-phase sequencing below — the skill carries the method.

## What Dan decided (this supersedes anything else)

1. **Phase A — the FULL-LENGTH 9:16 first (3:52.8), copying Muhammad's ad as EXACTLY as
   possible.** Not "his style, my choices" — a real close copy. Beat-for-beat: his cut,
   his inserts in his order, his graphic content, his pacing, his music energy, his SFX
   placement, re-laid-out for vertical. The ONLY permitted deviations are standing rules
   (each logged in notes.md with its reason):
   - the 0:03 side-by-side before/after card → cut SEQUENTIAL (200-lb photo with
     "200 POUNDS" kicker, then the goal phone) — banned pattern in paid ads;
   - the app screen recording only to 25.0s (at 26s his source hits the in-app
     BEFORE/AFTER, at 29s the email-capture form — both banned on screen);
   - no email-capture UI anywhere; AI-GENERATED labels stay.
2. **Phase B — Dan cuts the script himself.** After Phase A is delivered, show Dan the
   TRANSCRIPT of the ad as a script (clean prose, one paragraph per beat, with rough
   timecodes). Dan makes the 60-second cutdown edits in that script himself. **Do NOT
   design a cutdown.** Build the ≤0:59 vertical only from Dan's edited script, mapping
   his kept sentences back to the EDL.
3. Framing: **hybrid** (full-bleed talk ~1.25–1.4x, windowed on the olive field for
   graphic beats). Captions: **full word-timed captions, no emphasis bars** (Dan's call
   from attempt 1 — unchanged).

## Why attempt 1 failed — read before starting (full detail in the skill's [R1] rules)

The QC gate passed 11/11 on a video Dan rejected: every check measured format, none
watched the video. The five confirmed mechanisms:
sleepy 99 BPM bed reused from an older reference (his is driving ~120+ BPM); 23 of 72
splices shipped as naked jump cuts because all talk ran at ONE fixed crop (he hides every
trim under an insert or a wide 1.00 ↔ punch ~1.20 alternation); 83 programmatic whooshes
(one per 2.8s — his SFX are only on graphic entrances); cutdown selected by topic and
never read as prose; beat sheet sampled at 4s with free substitution. The skill now
mandates: 1s-interval beat audit, splice-concealment pass, tempo-matched bed chosen by
ear, SFX at his counted density, and the WATCH PASS as the delivery gate (2s moving clips
at every boundary + one full listen).

## What survives from attempt 1 — verified, reuse it, do not redo it

Build dir: `/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/`

- **`edl_final.json` — his 73-segment cut recovered from the raw roll** (word-level DP
  alignment 99.6%, mel-matched, conform verified against his render at 14 pose
  checkpoints). His hook is **TAKE 1 (src 3.66–29.1)**. Trust it.
- **Reference:** `Daniel HQ Fitness AD Video v3 HD.mp4`, Drive
  `12wDmd7-ziEKux8ioVi9gkJYCo7LZP3iv` (3:52.8). Local copy + full whisper JSON in
  attempt 1's scratchpad may be gone — re-download with gdown if needed.
- **Raw roll:** `C1591.MP4` on `/Volumes/Extreme/abs by ai 8:14 shoot …/` (1080p29.97,
  voice = RIGHT channel only).
- **Measured style:** tone curve + vignette (1.00→0.26) + palette in `grade.py` — his
  palette IS motionlib `J2AD`. Two framings measured: wide 1.00 / punch ~1.20 recentred up.
- **Voice chain:** right-channel mono, EQ fitted to his mix, band error 1.2 dB
  (`fitvoice output`). Keep.
- **Vertical layout library `vlib.py`** (adaptive window heights, card holes matched to
  media aspect, caption suppression under worded graphics). Keep.
- **Asset library** incl. `clip_109_replacement.mp4` — the native-vertical 1320x2868
  recording of the real app generating (usable full-bleed). Stock already re-cast to the
  white/Asian-men-30-50 rule.
- **What to REBUILD:** the base render (needs the punch-in alternation pass), the SFX
  bed, the music bed, and the beat sheet (re-derive at 1s intervals from HIS cut).

## Deliverables

1. `ad1_vertical_9x16.mp4` (+ 540p review copy, sent in chat) — after the watch pass.
2. The script/transcript for Dan (chat + a doc he can edit — his call in-session).
3. Phase B ≤0:59 build only AFTER Dan returns his edited script (likely a later session).

## Risks / cautions

- $0.00 expected AI spend (local Whisper, ffmpeg, PIL). No production code, no deploy,
  no native-retest trigger.
- Boot disk is low on space — work on `/Volumes/Extreme/`, deliver to
  `EDITED ADS 8-20-26/ad1-how-ai-got-me-abs/` on the same drive.
- Muhammad's graphics are burned in — nothing in his render is reusable as an asset;
  everything is re-made vertically. Do not credit "Muhammad" vs "sharkimagery" to
  editors in any doc without checking `AI_COORDINATION.md`'s attribution notes.
- Update `AI_COORDINATION.md` (re-read from disk first) and check off the dashboard task
  only when Phase A is delivered AND Dan hasn't rejected it in-session; Phase B keeps its
  own row until the 0:59 ships.
