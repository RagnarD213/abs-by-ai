# Ad 6 "You're Not Too Old", round 2: the four files after Dan locks the look

Written 2026-10-02 by the round 1 session. Recommended: **Claude Opus 5.5, High**. Sidebar name: `You're Not Too Old V/S/Sh Ad R2`.
**Dan answered the round 1 page on 2026-10-02: the look is LOCKED with three changes (below). Ready to fire.** Parent: `handoff-20261001-ad6-other-formats.md` (AV-05 + AS-04).

## Where round 1 stopped

Review page (graphic lock, nothing is a full film): `http://127.0.0.1:8816/`, served from `~/abs-review/av05-ad6/`
(internal disk, because the Extreme drive is full; restart: `python3 -m http.server 8816 --directory ~/abs-review/av05-ad6`).
It shows the first minute at 9:16, all 54 graphics and clips at 9:16, and the NEW square (1:1) graphic set with a
35 second moving square sample. Dan owes five answers (the reply box): 1 vertical graphics, 2 the hook's before and
after cards, 3 the square set, 4 the Thai shorts photo, 5 the lock-screen stretch at 2:06.

## Dan's answers (2026-10-02, verbatim in `~/abs-review/av05-ad6/decisions.json`)

Approved: the first minute, the vertical graphics and their words, the hook's before and after cards (F02, F03), the
square graphic set ("Everything else is looking good"). The two A/B questions he did not name stay at the recommended
A: keep the Thai shorts photo; keep the couch clip in the lock-screen stretch. Do not reopen any of this. Three changes:

1. **Calmer camera in the vertical.** *"The centering, I think, was a little bit too aggressive. Slightly reduce that
   and have a little bit more tolerance for going off-center to reduce the camera motion slightly."* Round 1 ran
   `kit_track.py` at its default `--tolerance 6` (crop travel 5,320 px, p90 pan 54.8 px/s, he sat 9.7 px off centre at
   the median). Rerun `kit_track.py --build <B> --tolerance 14`, report travel and pan speed before and after, and stay
   inside the gate's centring bound (a hold's median head centre within 36 source px). "Slightly": do not jump to 20+.
2. **No boxes without a reason (new standing rule, `VIDEO-RULES.md` top section).** *"For this picture of the
   overweight guy with the coffee cup, I'd like to see that full screen in the square... we should avoid cropping
   things into boxes unless there's a reason to do that."* In the SQUARE every clip and photo fills the frame unless
   filling cuts something that matters, it is a phone screen, or a label truly has no clear spot; a 1:1 window of a 16:9
   clip keeps most of it, so expect nearly all the AI clips to fill. In the VERTICAL, round 1 boxed 17 clips because
   `kit_labels.py` refused a chip on a frame-filling person; try again to fill the ones with one centred subject
   (hallway man P05, cable man P08, curl P25, beach man P33) with a smaller chip or a corner position, and keep a box
   only where the label check still refuses or the subject would be cut. List the reason beside every item that stays
   boxed in the delivery notes.
3. **The plank clip (P11, `dan_plank`) must be the colour-corrected final footage, not raw.** Round 1 used the library
   B-roll `B0001_dan-plank-kneel-mat-outdoors-vertical_9x16_12s.mp4`, which is ungraded. Find the finished export this
   shot came from (standing rule: reuse finished edited exports, never raw) and cut it from there. If no finished 9:16
   export exists, grade B0001 to match Muhammad's own graded frames of this shot (his master 113.6 to 119.4 s; the lift
   is `assets_auto/auto_03404.mp4`), prove it with a side-by-side still, and say which route was taken.

## Read first

1. `.claude/skills/shortad-from-longform/reference/kit9x16/README.md`: "An editor's master in Soft Blue Light" and
   "Ad 6 lessons (2026-10-02)".
2. `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `Handoffs/video-editing/00-RULES.md`.
3. `Handoffs/video-editing/AV-05-ad6-vertical.md`, `AS-04-ad6-square.md`, `.claude/skills/_shared/hyperframes/README.md`
   ("1:1 layouts").

## State (verified 2026-10-02)

- Build dir `/Volumes/Extreme/_edit_work/kit9x16/av05-ad6/` (the rejected Grok dir `av05-ad6-vert/` is not used).
  Master: Muhammad's finalized HD, 8,208 frames, 4:33.9. Raw roll: `C1597`.
- Done: recover, measure, content (one escalation, resolved on the page: the salad clip is stock), restyle
  (`sbl_copy.json` is the editorial copy file), setup, audio (his mix untouched), kit (design check passes), base,
  track, graphics (HyperFrames, in `hf/`), labels, words, captions.
- NOT done: the full picture, mux, prewatch gate, three fresh judges, fold, labelcheck, cutdown, deliver; the whole
  square build (only its graphic layouts and look media exist).
- Deleted to save space, regenerate if a stage asks: `segs_pic/`, `base_pic.mp4` (`base.mp4` is kept),
  `auto/ocr_frames`, `auto/r_C1597.rgb`.
- Queue: AV-05 and AS-04 are `in_progress` (Claude). Spend: under one cent. No AI clips or images were generated.

## Blocker to clear first

**The Extreme drive is full** (3.6 TB, 1 to 5 GB free during round 1; it stopped the build twice). The four builds
need about 30 GB free. Ask Dan what can go, or build on the internal disk (52 GB free). On exFAT every small file costs
2 MB, so `hf/proj` and watch strips are expensive there.

## Work

1. Dan's answers are already recorded. Apply the three changes (pictures in `sbl_copy.json`; the track by rerunning
   `kit_track.py --tolerance 14` after `base`), then:
   `kit_run.py --master "<master>" --build <B> --name "you're not too old to get abs i'm proof | claude | 9x16 | ad 6" --sbl <B>/sbl_copy.json --from restyle --deliver "<Ad 6 folder>"`
   (labels take about 15 minutes; it stops for the judged watch pass; three fresh `ra-reviewer` judges; resume
   `--from fold`; then the cutdown chain).
2. Not yet proven on a Soft Blue Light master build: `kit_plan.py`, the gate pre-check, `kit_cutdown.py` (same note as
   Ad 13). Fix the kit, never a bound. Run `gate.py` detached. At most two builds at once.
3. Square (AS-04): layouts exist (`_shared/hyperframes/square.py`), the square RENDERER for a Soft Blue Light build
   does not. `kit9x16/sq_look.py` is the starting point (it already composites base crop + plates + overlays +
   captions at 1080x1080 for the sample). Build 1:1 full + 59s from the locked vertical per `a11_sq_ad1/` and the
   shared square rules: same timeline, his audio stream copied, labels re-measured for 1:1, captions at y 880.
4. Independent `ra-reviewer` on all four delivered files before Dan sees them. Review copies + numbered action list.
5. Queue rows to `delivered`, mirror to the artifact, close the board line, delete this handoff's README row.

## Traps

- Do not upload anything. This is an ad (ends "Tap the button below"): Unlisted via `/ad-setup` only after approval.
- 402 of 865 words are under graphics that pause captions; if the gate's caption rows object, shorten graphic times
  in the copy file, never the bound.
- His master has 8 white flashes; the kit plans its own count inside his measured range. Do not add more.
- Seven clip cards keep Muhammad's burned AI chip or get ours, never both (see `sbl_copy.json` `pictures`).
- The talking head on this roll is tight: check the gate's hair rows on the delivered file.

## Starter prompt

> Read `Handoffs/handoff-20261002-ad6-round2-full-builds-after-lock.md` and the files it lists. Name this session
> "You're Not Too Old V/S/Sh Ad R2". Dan locked the look with three changes (calmer camera, no boxes without a reason, graded plank clip): apply
> them, build the full 9:16 and its 59 second cut through the gate, three fresh judges and an independent
> review, then the square full and its 59 second cut the same way, and send me the review copies with a numbered
> action list. Do not upload anything. No em dashes.

Model and effort: Claude Opus 5.5, High.
