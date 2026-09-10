#!/usr/bin/env python3
"""Conform the raw roll's PICTURE to Zeeshan's picture EDL on HIS 24 fps timeline, graded to his tone curve, 1920x1080.
Insert gaps are black (nothing reads the base there). Every seek is snapped to the raw's frame grid and the timestamps
rewritten (setpts=N/FR/TB) before the 29.97->24 fps pick, so no segment opens on a duplicated frame (skill A5.17/20).
Frame counts are cumulative on his grid. Writes base.mp4 (5980 frames) and asserts the count."""
import json, os, subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
HF, RF = 24.0, 30000/1001
NTOT = 5980
GRADE = ("scale=in_color_matrix=bt709:in_range=tv,format=rgb48le,lut3d=file=his.cube:interp=tetrahedral,"
         "scale=out_color_matrix=bt709:out_range=tv")
import hashlib; GH = hashlib.md5((GRADE + open("his.cube").read()).encode()).hexdigest()[:6]
E = json.load(open('edl_picture.json'))
os.makedirs('segs', exist_ok=True)
parts, cur = [], 0
def black(n, i):
    p = f'segs/black_{i:03d}_{n}.mp4'
    if not os.path.exists(p):
        subprocess.run([FF,'-nostdin','-v','error','-y','-f','lavfi','-i','color=black:s=1920x1080:r=24','-frames:v',str(n),
                        '-vf','format=yuv420p','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',p], check=True)
    return p
for i, s in enumerate(E):
    if s['n0'] > cur: parts.append(black(s['n0']-cur, i))
    n = s['n1'] - s['n0']
    src = round((s['n0']/HF + s['off'])*RF)/RF - 0.0002
    p = f"segs/{i:03d}_{s['n0']}_{n}_{src:.4f}_{GH}.mp4"
    if not (os.path.exists(p) and os.path.getsize(p) > 1000):
        subprocess.run([FF,'-nostdin','-v','error','-y','-ss',f'{src:.5f}','-i','raw.mp4','-an',
                        '-vf', f'{GRADE},setpts=N/({RF:.6f})/TB,fps=24,format=yuv420p','-frames:v',str(n),
                        '-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv', p], check=True)
    parts.append(p); cur = s['n1']
    print(f'seg {i:2d} his {s["t0"]:8.3f}-{s["t1"]:8.3f} src {src:8.3f} {n} fr', flush=True)
if cur < NTOT: parts.append(black(NTOT-cur, 999))
open('concat_base.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run([FF,'-nostdin','-v','error','-y','-f','concat','-safe','0','-i','concat_base.txt','-c','copy',
                '-video_track_timescale','24000','base.mp4'], check=True)
n = int(subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-count_frames','-show_entries',
                        'stream=nb_read_frames','-of','csv=p=0','base.mp4'], capture_output=True, text=True).stdout.strip())
print('base.mp4 frames', n, 'planned', NTOT); assert n == NTOT
