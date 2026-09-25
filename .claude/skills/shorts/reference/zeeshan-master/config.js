// SL-04: shorts from Zeeshan's "Arms & Shoulders Home Workout" (Video2 Rev 3), 11:00.1,
// 1920x1080 @ 29.97, MD5 49c7dfb3d189043dbb2bc4b326e8fd81. Read-only; never re-encoded in place.
const path = require('path');
const PROJ = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
module.exports = {
  FF: path.join(PROJ, 'Media/video_edit/bin/ffmpeg'),
  FFPROBE: path.join(PROJ, 'Media/video_edit/bin/ffprobe'),
  SRC: path.join(PROJ, 'Zeeshan Content Videos/arms and shoulders home workout - video 2/arms and shoulders home workout | zeeshan | 16x9 | video 2.mp4'),
  FONTS: path.join(PROJ, 'ad-factory/the-upload/assembly/fonts'),
  FPS: '30000/1001',
  FPS_N: 30000 / 1001,
};
