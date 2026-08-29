// Paths for the supplements Shorts batch (long-form 03, 8/3 shoot).
const path = require('path');
const PROJ = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
module.exports = {
  FF: path.join(PROJ, 'Media/video_edit/bin/ffmpeg'),
  FFPROBE: path.join(PROJ, 'Media/video_edit/bin/ffprobe'),
  // ⚠ THE CLEAN MASTER, NOT THE DELIVERED ONE. The 8/27 rebuild took this video to 43%
  // insert coverage, so cutting from FINAL_supplements.mp4 would make nearly half of every
  // short a full-frame graphic the skill's rules force into a `card`. This file is the same
  // picture edit, graded, with no graphics and no stock inserts, and its audio is already
  // the fixed single-mic chain (-14.02 LUFS). Verified frame-aligned with FINAL to 0.03s.
  // NEVER use *_PRE_AUDIOFIX.mp4 - that voice is comb-filtered.
  SRC: path.join(PROJ, 'claude edited long form content/03 - The Supplements I Actually Take/CUT_v1_graded_NO-GRAPHICS.mp4'),
  FONTS: path.join(PROJ, 'ad-factory/the-upload/assembly/fonts'),
  // ⚠ THE RAW ROLL, for rev 2. Dan asked for a better take on short E's opening and the
  // discarded one is only in the raw. Proven usable, not assumed: the graded raw frame
  // correlates 0.9999 with the master frame it became (and 0.15 against its mirror, so the
  // roll is not flipped), which means raw footage cuts in seamlessly.
  RAW: '/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1514.MP4',
  RAW_WORDS: '/Volumes/Extreme/_edit_work/supplements/C1514.whisper.json',
  // the EDL's own grade, applied to raw footage so it matches the master
  GRADE: "curves=all='0/0 0.054/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'",
  // Source is 29.97, like the ab-wheel batch and unlike the 24 fps V2/V3/V6 batches.
  FPS: '30000/1001',
  FPS_N: 30000 / 1001,
};
