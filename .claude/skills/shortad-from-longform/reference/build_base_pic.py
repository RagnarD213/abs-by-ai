#!/usr/bin/env python3
"""Conform the raw roll's PICTURE to the PICTURE EDL (his picture cut frames), 1920x1080 at the
grade, cumulative frame counts. Then lay the kept dissolve patches over the splices whose picture
cut did NOT move (they were built for those exact frames). Writes base.mp4."""
import json, os, subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
RAW = ("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content"
       " | jeff chagrin | dan rose/C1592.MP4")
FPS = 30000/1001
GRADE = open('grade.txt').read().strip()
P = json.load(open('edl_picture.json'))
os.makedirs('segs_pic', exist_ok=True)
parts = []
for s in P:
    nfr = s['n1'] - s['n0']
    p = f"segs_pic/{s['i']:03d}_{s['n0']}_{nfr}.mp4"
    parts.append(p)
    if os.path.exists(p) and os.path.getsize(p) > 1000: continue
    # ⚠ SNAP THE SEEK TO THE RAW'S FRAME GRID. An input -ss at an arbitrary fraction of a frame makes
    # ffmpeg's cfr output duplicate the FIRST frame whenever the phase is past half a frame (the re-audit
    # found a duplicated frame right after 9 of 29 cuts, 4 of 29 in the previous base -- a 33 ms hold, not
    # visible, but a defect class). Snapping src_in to k/FPS (+ a hair) lands the seek on a frame.
    # ⚠ AND REWRITE THE TIMESTAMPS. Snapping alone did not remove the duplicate (the roll's pts are not
    # exactly k/FPS, so the seek phase is still unknown): `setpts=N/FR/TB` puts every decoded frame on a
    # clean 0,1,2,... grid, so the constant-rate output has nothing to duplicate or drop. Verified by
    # landing_check.py's diff(n0->n0+1) at every cut.
    src = round(s['src_in']*FPS)/FPS - 0.0002
    subprocess.run([FF,'-nostdin','-v','error','-y','-ss',f"{src:.5f}",'-i',RAW,'-an',
                    '-vf', f'{GRADE},scale=1920:1080,setpts=N/({FPS:.6f})/TB','-r',f'{FPS:.6f}','-frames:v',str(nfr),
                    '-c:v','libx264','-crf','16','-preset','veryfast','-pix_fmt','yuv420p', p], check=True)
    print(f"seg {s['i']:3d}  frames {s['n0']:5d}+{nfr:4d}  src {s['src_in']:8.3f}  rel {s['rel']:+d}", flush=True)
with open('concat_pic.txt','w') as f:
    for p in parts: f.write(f"file '{p}'\n")
subprocess.run([FF,'-nostdin','-v','error','-y','-f','concat','-safe','0','-i','concat_pic.txt','-c','copy',
                '-video_track_timescale','30000','base_pic.mp4'], check=True)
n = subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-count_frames',
                    '-show_entries','stream=nb_read_frames','-of','csv=p=0','base_pic.mp4'],
                   capture_output=True, text=True).stdout.strip()
print('base_pic.mp4 frames', n, '(planned', P[-1]['n1'], ')')
assert int(n) == P[-1]['n1']
# kept dissolves only where the picture cut stayed on the audio splice
keep = json.load(open('softcuts_keep.json'))
moved = {round(s['audio_cut_in'],3) for s in P if s['rel']}
jobs = [j for j in keep if round(j['cut'],3) not in moved and round(j['t'],3) not in moved]
jobs = [j for j in jobs if not any(abs(j['t']-s['audio_cut_in'])<0.02 and s['rel'] for s in P)]
print('dissolve patches kept:', [round(j['t'],2) for j in jobs])
ins, fc, last = ['-i','base_pic.mp4'], [], '0:v'
D = 5
for k, j in enumerate(jobs):
    ins += ['-i', f"soft/p{j['i']:03d}.mp4"]
    t0 = j['n0']/FPS; t1 = (j['n0']+D)/FPS
    fc.append(f"[{k+1}:v]setpts=PTS+{t0:.6f}/TB[s{k}];[{last}][s{k}]overlay=0:0:enable='between(t,{t0:.6f},{t1:.6f})':eof_action=pass[o{k}]")
    last = f'o{k}'
if jobs:
    subprocess.run([FF,'-nostdin','-v','error','-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]',
                    '-r','30000/1001','-video_track_timescale','30000','-c:v','libx264','-crf','16','-preset','medium',
                    '-pix_fmt','yuv420p','-an','base.mp4'], check=True)
else:
    subprocess.run(['cp','base_pic.mp4','base.mp4'], check=True)
n = subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-count_frames',
                    '-show_entries','stream=nb_read_frames','-of','csv=p=0','base.mp4'], capture_output=True, text=True).stdout.strip()
print('base.mp4 frames', n)
