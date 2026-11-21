// SL-05: shorts from Zeeshan's "Stop Deadlifting" (Video 3 Rev 5), 9:16.5,
// 1920x1080 @ 29.97, MD5 e98bbb9bace1085df31950e9e51fd326. Read-only; never re-encoded in place.
const path = require('path');
const PROJ = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
module.exports = {
  FF: path.join(PROJ, 'Media/video_edit/bin/ffmpeg'),
  FFPROBE: path.join(PROJ, 'Media/video_edit/bin/ffprobe'),
  SRC: path.join(PROJ, 'Zeeshan Content Videos/stop deadlifting - video 3/stop deadlifting | zeeshan | 16x9 | video 3.mp4'),
  FONTS: path.join(PROJ, 'ad-factory/the-upload/assembly/fonts'),
  FPS: '30000/1001',
  FPS_N: 30000 / 1001,
};
