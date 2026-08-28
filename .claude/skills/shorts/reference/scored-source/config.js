// Paths for the ab-wheel Shorts batch. Source is Muhammad Arsalan's finished 16:9 organic
// cut (Drive 1lu_Im9st8XtDNXPnFOhpKyc7IA2Whf_J), 6:58.05, 1920x1080, 30000/1001 fps.
const path = require('path');
const PROJ = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
module.exports = {
  FF: path.join(PROJ, 'Media/video_edit/bin/ffmpeg'),
  FFPROBE: path.join(PROJ, 'Media/video_edit/bin/ffprobe'),
  SRC: path.join(PROJ, 'Muhammad Organic Videos', 'Daniel Organic Video -The $17 Ab Wheel Beats Every Crunch-v2 HD.mp4'),
  FONTS: path.join(PROJ, 'ad-factory/the-upload/assembly/fonts'),
  // The source is 29.97, not the 24 the earlier batches used. Resampling 29.97 -> 24 drops
  // one frame in five, and every shot in this cut carries a constant slow push, so the
  // judder would be visible on all of them. The masters ship at the source rate instead.
  FPS: '30000/1001',
  FPS_N: 30000 / 1001,
};
