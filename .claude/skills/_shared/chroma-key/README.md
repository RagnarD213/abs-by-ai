# Approved green-screen key

Dan locked the Bill Maher Fat 90-Year-Old R3 key on 2026-10-20 as the chroma-key style for all videos, for both Claude and Codex. Use this result for all future green-screen edits and requested key revisions. Existing approved exports stay untouched unless Dan asks to revise them. Do not ask him to select this style again.

The exact approved sample and verbatim approval are in `reference/ds40-r3/approval.json`. Public reference: https://drive.google.com/file/d/17TO-EYOAOmTu5i1Ivhu7ChOQSu-u3Q09/view . Local comparison: http://127.0.0.1:9031/ . The reference preserves fine hair, stable semitransparent gaps, clean body/arm edges and natural motion. Dan accepted the remaining enlarged gray halo and minor edge variation as good enough.

## Reuse the method, measure the footage

Use the approved R2 body/arm matte with the R3 hair refinement. R3 stabilizes the screen estimate across the shot, uses continuous local foreground color, and combines five motion-aligned alpha frames with photometric and forward/backward flow confidence. Smooth only translucent hair. Keep solid detail intact and feather the hair/body handover. The unchanged reference code is archived here with hashes; it is reproduction evidence, not a generic command to run in this folder.

The sample is native portrait 2160x3840 BT709 S-Cinetone at 30000/1001. R3's hair ROI x350:1850/y400:1300 and blend y960:1120 are specific to those 300 frames. Locate hair and screen on each new source; do not reuse those coordinates, coefficients, crop or decode transform blindly. Fit a stable screen field per continuous shot and reset temporal neighbors at source cuts. New lighting and motion require source checks against the approved moving reference, not another style audition.

R3's renderer patches an existing R2 body export for ten seconds only. For a full edit, build the approved body matte from raw frames using the archived R2 renderer, then apply R3 hair to matching original frames. Never extend or loop the sample. Apply the selected grade once to reconstructed foreground; keep background color separate. Preserve accurate BT709 RGB decoding (`accurate_rnd+full_chroma_int`) and consistent field colors to avoid a rectangular tint seam. Adapt actual source color metadata when it differs.

Compare moving hair on light and dark fields at native resolution, including internal gaps, fine loops, turns and gestures. Check glasses, arms, fingers, ghost trails, hair volume and foreground/background joins. At final resolution, run the existing exact-file gates and independent motion review. `key:hair_temporal_edges` is not implemented; the approval does not make an automated hair gate pass. Do not alter thresholds to obtain a pass.

## Audio, grade and historical checks

The global approval is for keying. Balanced audio and warmer color remain locked specifically for Bill Maher Fat 90-Year-Old. Other videos retain their own approved sound and grade. `round2-audio_refine.py` is the final Balanced recipe, not the earlier `audio_build.py`; the selected WAV and MP4 hashes are in the R3 delivery receipt. Full-length new source audio needs that same treatment, not a repeated ten-second file.

The approved sample's gate remains 37 PASS, 1 FAIL (accepted Balanced comb/tone), 1 NOT MEASURED (continuous shot has zero boundaries), 18 N/A. Preserve those historical findings. This folder promotes an unchanged, human-approved visual reference and method; it changes no executable production gate or numeric setting.

## 16:9 rolls (RO-24, 2026-10-20)

The first 16:9 adaptation (10/15 green screen, C1726) is `.claude/skills/longform-edit/reference/ro24/` (`key16.py`, README there): the same R2/R3 maths with the head-size scale, per-frame hair geometry, a clean plate of the screen and a garbage matte. It also carries a "refined" variant offered to Dan on 2026-10-20 (solid hair interior, edge colour, edge-band spill, and moving hands: the approved body key reads a skin/screen blur as solid because skin is red-heavy). Not yet approved; the approved key above stays the standard until Dan picks.
