#!/usr/bin/env python3
"""picture.mp4 + captions.mov + THE APPROVED VERTICAL'S OWN AUDIO STREAM -> the 1:1 master.

⚠ THE AUDIO IS NOT RE-DERIVED, RE-ENCODED, RE-GAINED OR RE-LIMITED. It is the AAC stream out of
`… | claude | 9x16 | ad 2.mp4` copied bit for bit (`-c:a copy`), and this script asserts the
md5 of the copied stream equals the md5 of the source's. Dan approved that sound on 2026-09-08;
anything else -- including running the same +5.2 dB chain again from `his_mix.wav` -- would be a
different file for no reason, and the whole class of audio mistakes this project has paid for
(loudnorm's silent dynamic fallback, a lift into a limiter, a mono sum) starts with re-deriving
audio somebody had already approved.

That also means the square is 256 kbps AAC, not the 320 the square rules name: 256 is what the
approved vertical carries, and a re-encode to 320 cannot add anything the 256 stream lost.

Frame count is asserted against the beat sheet, from the VIDEO STREAM (the container's duration
is the longer of the two streams, so a truncated picture reads back as full length -- [A4].0aa).
"""
import hashlib, json, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
VERT = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/"
        "stop wasting money on nutritionists - ad 2/"
        "stop wasting money on nutritionists | claude | 9x16 | ad 2.mp4")
OUT = sys.argv[1] if len(sys.argv) > 1 else 'ad2_square_1x1.mp4'
PIC = sys.argv[2] if len(sys.argv) > 2 else 'picture.mp4'
sys.path.insert(0, '.')
import beats
PLAN = round(beats.DUR*30000/1001)

def astream_md5(path):
    r = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', path, '-map', '0:a', '-c', 'copy',
                        '-f', 'md5', '-'], capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])
    return r.stdout.strip().split('=')[1]

src_md5 = astream_md5(VERT)
r = subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', PIC, '-i', 'captions.mov', '-i', VERT,
    '-filter_complex', '[0:v][1:v]overlay=0:0:eof_action=pass:format=auto[v]',
    '-map', '[v]', '-map', '2:a', '-r', '30000/1001', '-frames:v', str(PLAN),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
    '-video_track_timescale', '30000', '-c:a', 'copy', '-movflags', '+faststart', OUT],
    capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[-2000:])

pj = json.loads(subprocess.run([FP, '-v', 'error', '-select_streams', 'v', '-count_frames',
    '-show_entries', 'stream=width,height,nb_read_frames,duration', '-of', 'json', OUT],
    capture_output=True, text=True).stdout)['streams'][0]
n = int(pj['nb_read_frames'])
out_md5 = astream_md5(OUT)
print(f'{OUT}: {pj["width"]}x{pj["height"]}  video {n} frames (planned {PLAN})  {float(pj["duration"]):.3f}s')
print(f'  audio stream md5  his vertical {src_md5}\n                    our square   {out_md5}')
if n != PLAN: raise SystemExit(f'FRAME COUNT {n} != PLAN {PLAN}')
if f'{pj["width"]}x{pj["height"]}' != '1080x1080': raise SystemExit('NOT 1080x1080')
if out_md5 != src_md5: raise SystemExit('AUDIO STREAM CHANGED -- it must be the approved vertical\'s, bit for bit')
print('  AUDIO VERBATIM: the approved vertical\'s stream, bit for bit')
