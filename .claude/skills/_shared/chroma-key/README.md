# Approved green-screen key: the house standard

**Current standard (Dan, 2026-10-21): Claude's Bill Maher Fat 90-Year-Old R2 key.** Dan: *"let's lock this chroma key
as our default way to chroma key things. I want all green screen videos keyed out like this."* and *"This key looks very
clean... Let's make all our future chroma keys this clean and make this a standard."* It replaces the Codex R3 key
(locked 2026-10-20, kept below as history). Claude and Codex both key every future green-screen video this way.

**Finished reaction reference updated 2026-10-25 (editor routing since 2026-10-27: no fixed AI, VIDEO-RULES):** Dan selected
[Bill Maher Codex R5](../../shorts/reference/ds40-codex-r5-reaction-format/README.md) as the standard reaction format,
including its transitions, title above the panel, and colour on both Dan and the clip. R5 uses this Claude R2
algorithm with its own calibrated full-height pieces and Codex finishing/compositing. Keep the algorithm below;
match the approved R5 finished look. This is not permission to re-key an approved piece or replace gate results.

**The bar every key must meet** (measured on the approved sample, every frame, independent review SHIP):
edge flicker with motion removed below the camera's own picture (R2: 0.69 overall, 0.68 hair; `mcflicker.py`),
dark rim on skin edges at or below the source's (R2: 2.7%, source 8%; `measure_r2.py`), nothing see-through inside
the subject over saturated pink (watch, glasses), no floating specks, fine strands and motion blur kept. Measure every
new key against its own source with these two scripts before Dan sees it.

**The method and exact code:** `reference/ds40-claude-r2/` (hashes and Dan's words in `approval.json`; since the
2026-10-21 speed update the stage scripts there are faster code with bit-identical output, the approved originals are
in `approved-original/`, evidence in `approval.json` `speed_update_20261021`; recipe notes in
`.claude/skills/shorts/reference/ds40-greenscreen/README.md`). In order: clean plate (`plate.py`), 4K clean-plate
colour-difference key with positivity floor, local plate, hole fill and tracked watch hold-out (`keylib.py`,
`stage1_key.py`); then the finishing pass at output scale (`stage15_temporal.py`): motion-compensated temporal matte
in the edge band only, edge colour from solid pixels 3 px inside, island-only speck rule, hand-placed boxes for
reflective glass seen edge-on; then composite (`stage2_comp.py`). Recalibrate per source: plate, garbage/crop rows,
watch or glasses boxes, hair box for the measure. Reset temporal neighbours at every cut (never average across a cut).
Grade and audio stay per video.

## Run it cheaply: calibrate on excerpts, key each piece once (2026-10-21, every recipe, Claude and Codex)

The key was half of all render time on 10-21, and two thirds of that was re-keying whole clips to try a setting
(RO-24 keyed each clip three times, 40-75 minutes a run). The rule, in order:

1. **Calibrate on excerpts, never on the full clip.** Copy `reference/ds40-claude-r2/` into the job, set the plate,
   crop rows and hold-out boxes for this source, then run `calibrate.py` (quick lane, minutes): it finds the piece's
   hardest moments (the motion peaks and the tracked hold-out), keys 2-3 s excerpts there with the recipe's own
   stage 1 and 1.5, and writes a contact sheet (pale, pink, matte) plus `calibration.json`. Each excerpt is keyed with
   3 extra frames each side, so its frames are bit-for-bit what the full key gives at those frames. Adjust and re-run
   until the sheet is right. `--at SECONDS` adds a moment you know is hard; `--pick-only` just lists the picks.
2. **Key each piece exactly once, through `keyonce.py`.** It writes a `.done` stamp holding a fingerprint of the
   recipe code, plate, boxes and piece times; a matching stamp is skipped, so no round re-keys an approved piece.
   Change one piece's inputs and only that piece is keyed again. Pass the piece's cache folders with `--clear`
   (stage 1 resumes by skipping frames already on disk, so a re-key would otherwise keep old frames).
3. **Gate the one full run** with `mcflicker.py` and `measure_r2.py` (adapted to the source, as before). **Re-key only
   a failing piece** (or only its failing frames: `ONLY=f1,f2,... stage15_temporal.py ...`).

```
python3 .claude/skills/_shared/chroma-key/calibrate.py --code $JOB/recipe --src CLIP.MP4 --t0 T0 --dur D \
    --out $JOB/key/cal_A --watch $JOB/key/watch_A.json --plate $JOB/key/plate_out.npy
python3 .claude/skills/_shared/chroma-key/keyonce.py $JOB/key/A.done \
    --inputs recipe/stage1_key.py recipe/keylib.py recipe/stage15_temporal.py $JOB/key/plate_out.npy $JOB/key/watch_A.json \
    --params "T0 D" --clear $JOB/key/c1_A $JOB/key/c2_A -- zsh -c "python3 stage1_key.py T0 D c1_A && python3 srcprep.py T0 N src_A.npy && python3 stage15_temporal.py c1_A src_A.npy c2_A watch_A.json"
```

Recipes whose stage scripts take other arguments (RO-24's `stage1_16.py F0 N ... X0 X1 PLATE`) pass their own command
templates to `calibrate.py` (`--stage1 "python3 stage1_16.py {f0} {nf} {out} 752 3136 plateB"`; fields `{t0} {dur}
{f0} {nf} {n} {out} {c1} {src} {watch}`).

**Cost (measured 2026-10-21, `Handoffs/results-20261021-cheap-key.md`):** about 6.5 CPU-seconds a frame at output
scale (stage 1 at 4K about 3.5 s, stage 1.5 about 3 s), down from 9.9 s, with bit-identical output. A 30 s piece (900
frames) is about 24 minutes of a 4-core heavy slot (37 before); a calibration pass (three 2.5 s excerpts) about 10-13 minutes of a
2-core quick slot. Stage 1.5 workers hold about 0.6 GB of working memory (approved code: about 2 GB resident per
worker); `FLOW_CACHE=1` trades two more optical flows a frame for 0.1 GB less. Pools are `RENDERQ_CORES` workers with
one thread each.

---

## History: Codex R3 key (Dan, 2026-10-20, superseded 2026-10-21)

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
