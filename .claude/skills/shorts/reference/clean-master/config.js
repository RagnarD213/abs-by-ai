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
  // Source is 29.97, like the ab-wheel batch and unlike the 24 fps V2/V3/V6 batches.
  FPS: '30000/1001',
  FPS_N: 30000 / 1001,
};
