#!/usr/bin/env python3
"""picture.mp4 (captions already burned by the compositor) + HIS AUDIO, UNTOUCHED -> the deliverable.

⚠ Dan, 2026-09-10: "Zishan's audio sounds much better... Use Zishan's audio." The first two deliveries carried his mix
+9.9 dB into a 4x-oversampled limiter, summed to mono, re-encoded -- rejected. Now:
  * AUD is his ORIGINAL export (.mov/.mp4/.m4a): its audio stream is COPIED, bit for bit (-c:a copy). The full length.
  * AUD is a .wav (cut/his_mix.wav: his mix, only CUT at the cutdown's seams with 4 ms joins): encoded AAC 320k with NO
    filter of any kind -- no gain, no limiter, no loudnorm, no channel change. The cutdown.
The picture stream is COPIED (never re-encoded here). Asserts the VIDEO STREAM's frame count (skill A4.0aa: the container
duration lies) and the audio stream's length."""
import os, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
HIS = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Zeeshan Ad Videos/this picture got me abs - ad 1/"
       "this picture got me abs | zeeshan | 16x9 | ad 1 | h264.mov")
PIC = sys.argv[1] if len(sys.argv) > 1 else 'picture.mp4'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'ad1zee_vertical_9x16.mp4'
AUD = sys.argv[3] if len(sys.argv) > 3 else HIS
copy = os.path.splitext(AUD)[1].lower() in ('.mov', '.mp4', '.m4a')
acodec = ['-c:a', 'copy'] if copy else ['-c:a', 'aac', '-b:a', '320k']      # a .wav: his cut mix, encoded, nothing else
r = subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', PIC, '-i', AUD, '-map', '0:v:0', '-map', '1:a:0',
                    '-c:v', 'copy'] + acodec + ['-movflags', '+faststart', OUT], capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[-2000:])
def probe(sel, entries, count=False, f=OUT):
    c = [FP, '-v', 'error', '-select_streams', sel] + (['-count_frames'] if count else []) + \
        ['-show_entries', f'stream={entries}', '-of', 'default=nw=1', f]
    return dict(l.split('=') for l in subprocess.run(c, capture_output=True, text=True).stdout.strip().split('\n'))
v = probe('v', 'nb_read_frames,duration', True); a = probe('a', 'duration,codec_name,channels')
n, vd, ad = int(v['nb_read_frames']), float(v['duration']), float(a['duration'])
pic = int(probe('v', 'nb_read_frames', True, PIC)['nb_read_frames'])
print(f"{OUT}: video {n} frames ({vd:.3f}s), audio {ad:.3f}s {a['codec_name']} {a['channels']}ch "
      f"({'stream-copied from ' + os.path.basename(AUD) if copy else 'AAC 320k of ' + AUD + ', no filters'}), picture had {pic}")
assert n == pic, 'video frames changed in the mux'
assert abs(ad - vd) < 0.10, f'audio {ad:.3f}s vs video {vd:.3f}s'
if copy:
    md5 = lambda f: subprocess.run([FF, '-nostdin', '-v', 'error', '-i', f, '-map', '0:a:0', '-c', 'copy', '-f', 'md5', '-'],
                                   capture_output=True, text=True).stdout.strip()
    h, o = md5(AUD), md5(OUT)
    print(f'  audio stream md5: his {h} / ours {o}')
    assert h == o, 'the audio stream is NOT his, bit for bit'
