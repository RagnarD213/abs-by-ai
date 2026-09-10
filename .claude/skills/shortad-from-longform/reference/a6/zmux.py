#!/usr/bin/env python3
"""picture.mp4 (captions already burned by the compositor) + his finished mix -> the master.
The picture stream is COPIED (never re-encoded here); the audio is aud/mix_final.wav (his mix, one constant gain,
4x-oversampled limiter) encoded AAC 320k -- measured: 256k overshoots to -0.7 dBTP, 320k lands -1.2 (limit -1.0).
Asserts the VIDEO STREAM's frame count (skill A4.0aa: the container duration lies) and the audio stream's length."""
import subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
PIC = sys.argv[1] if len(sys.argv) > 1 else 'picture.mp4'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'ad1zee_vertical_9x16.mp4'
AUD = sys.argv[3] if len(sys.argv) > 3 else 'aud/mix_final.wav'
r = subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', PIC, '-i', AUD, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', OUT],
                   capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[-2000:])
def probe(sel, entries, count=False):
    c = [FP, '-v', 'error', '-select_streams', sel] + (['-count_frames'] if count else []) + \
        ['-show_entries', f'stream={entries}', '-of', 'default=nw=1', OUT]
    return dict(l.split('=') for l in subprocess.run(c, capture_output=True, text=True).stdout.strip().split('\n'))
v = probe('v', 'nb_read_frames,duration', True); a = probe('a', 'duration')
n, vd, ad = int(v['nb_read_frames']), float(v['duration']), float(a['duration'])
pic = int(probe_pic := subprocess.run([FP, '-v', 'error', '-select_streams', 'v', '-count_frames', '-show_entries',
          'stream=nb_read_frames', '-of', 'csv=p=0', PIC], capture_output=True, text=True).stdout.strip())
print(f'{OUT}: video {n} frames ({vd:.3f}s), audio {ad:.3f}s, picture had {pic}')
assert n == pic, 'video frames changed in the mux'
assert abs(ad - vd) < 0.10, f'audio {ad:.3f}s vs video {vd:.3f}s'
