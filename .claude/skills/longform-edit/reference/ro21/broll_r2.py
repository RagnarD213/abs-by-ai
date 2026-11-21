"""RO-21 round 2 B-roll changes (on broll_r1.py's builder): B01 = library AI clip A0207 (Dan 2026-10-29: "our AI clips of
someone weighing themselves are better than stock now"), source 1.0 s on (steps on, looks down, then the clip's own cut to
him tapping the scale), graded toward the film, AI-GENERATED chip top left for its whole time (inserts are opaque, so the
chip is burned in here). Output round2/broll/B01.mp4. python3 broll_r2.py [--stills]"""
import sys, json, subprocess, numpy as np
sys.path.insert(0, '/Volumes/Expansion/_edit_work/RO-21/recipe'); import broll_r1 as R
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg'); import gsbg as G
from PIL import Image
W = R.W; OUT = f'{W}/round2/broll'
A0207 = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/people/A0207_man-checks-broken-bathroom-scale-two-shot_16x9_5s.mp4'
R.GRADES['AI_A0207'] = R.grade(lo=0.03, curve='0/0 0.25/0.22 0.75/0.77 1/1', sat=0.08)
R.ITEMS['B01'] = [('A0207 man taps his scale', None, 0, A0207, 1.00, None, 'AI_A0207')]
chip = f'{OUT}/_chip.png'
im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); G.SB.disclosure(im, 'AI-GENERATED', xy=(56, 48)); im.save(chip)
a, b, N, pieces = R.layout('B01'); (p, s, n), = pieces
src_len = 5.375 - p[4]; assert n / R.FPS <= src_len, ('A0207 too short for B01', n / R.FPS, src_len)
vf = f"[0:v]{R.chain(p, p[6])},fps=30000/1001,trim=end_frame={n},setpts=PTS-STARTPTS[v];[1:v]format=gbrap[c];[v][c]overlay=0:0:format=gbrp," \
     f"scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1,tpad=stop_mode=clone:stop=2[out]"
subprocess.run([R.FF, '-y', '-v', 'error', '-ss', f'{p[4]:.3f}', '-i', A0207, '-loop', '1', '-i', chip, '-filter_complex', vf, '-map', '[out]',
                '-an', '-r', '30000/1001', '-frames:v', str(N + 2), '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-profile:v', 'high',
                '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv',
                '-movflags', '+faststart', f'{OUT}/B01.mp4'], check=True)
print('B01', N, 'frames (+2 padded) from A0207 @', p[4])
