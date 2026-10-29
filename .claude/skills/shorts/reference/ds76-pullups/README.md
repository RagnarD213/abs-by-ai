# DS-76 How To Do Pull-Ups (SFC, Oct 23 pool set): approved R2 recipe and lessons

Dan approved R2 on 2026-10-29. Work, evidence and full recipe: `/Volumes/Extreme/_edit_work/DS-76/round2/`.
Same series layout as DS-84 Hamstring Curls (F Deep And Vivid, Natural Warmth A, Original Portrait, large title over gym windows).
The scripts here are copies for reference (paths point at the work folder); rebuild from the work folder.

What Dan asked for and approved, reusable for the other Oct 23 gym how-tos:
- **Intro: the full-body clip FULL SCREEN** (9:16 crop of the 4K library master, full height), with the title in the
  translucent blue glass lower third at the bottom (`lt_scenes`, topic eyebrow + "How to Do <Exercise>"), captions at
  y 1605 above it. `build.py`: asset `fullscreen: true`, glass graphic composited over the clip.
- Later exercise clips: windowed under the large two-line title; **hold the title steady across back-to-back
  windowed clips** (`title_off` continues the H01 track); two independent judges flagged the per-clip retype as a blink.

Traps found by five independent reviews (fix before Dan sees it):
- Whisper merged a false start into one 2 s word ("stay"); a disfluency-prompted pass on suspicious long words found it.
- Gym library masters (colour C) measured darker than DS-84's approved cutaways: lift midtones per clip to median
  luma 46-72 and black share 7-22 % (`broll_tune.py` curve, blacks kept). Rear assisted-machine angles B0612-B0614
  are too dark to rescue; B0641 has an internal camera jump; B0643 drifts into a close-up after about 7.2 s that crops an arm.
- No true slow-negative pull-up exists in the library (on `Docs/NEXT_SHOOT_LIST.md`); a full-body normal rep that reaches
  the bar then lowers, cut before the next rep, was accepted.
- Narrowing a window so captions sit inside the picture cropped elbows: keep arms whole first; a caption below a
  window is fine, a caption straddling a window edge is not.
- When one library clip is used several times, frame-match the uses against each other (5 repeated frames slipped in once).
- Audio joins: crossfade 40 ms from source either side (fade-to-silence dipped the room tone); end pieces in room tone
  before a breath.
- `crop_check.py`'s tile sheet shows frames past the clip end (`-frames:v 1` overrides the frame limit); count tiles.
