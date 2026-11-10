"""DS-78 R1 look options on C1882: colour F/E/B (F = Dan's pick on How To Do Pull-Ups DS-76, the same roll), crop 1/2/3, moving 12 s colour samples."""
from pathlib import Path
import subprocess, json, os, sys
from PIL import Image, ImageDraw
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = R/'Media/video_edit/bin/ffmpeg'
S = Path('/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content/C1882.MP4'); O = W/'review/media'
os.environ['PATH'] = str(F.parent)+':'+os.environ['PATH']; sys.path.insert(0, str(R/'.claude/skills/_shared/renderq')); import renderq
renderq.hold_until_exit('DS-78 R1 look options', pool='light', group='DS-78')
def ff(a): subprocess.run([str(F), '-nostdin', '-v', 'error', '-y']+list(map(str, a)), check=True)
G = {'F': dict(name='Deep And Vivid', vf='eq=contrast=1.25:gamma=1.14:brightness=0.003:saturation=1.75', note='Dan picked this on T-Bar Rows and Pull-Ups (same roll C1882) and on Hamstring Curls'),
     'E': dict(name='Vivid', vf='eq=contrast=1.22:gamma=1.16:brightness=0.000:saturation=1.58', note='a touch softer and less saturated than F'),
     'B': dict(name='Richer Contrast', vf='eq=contrast=1.13:gamma=1.20:brightness=0.015:saturation=1.18', note='Dan picked this on the V-Taper Short; he called it a little washed out on Hamstring Curls')}
C = {'1': dict(name='Original Portrait', crop=[0, 0, 2160, 3840]), '2': dict(name='Slightly Closer', crop=[60, 0, 2040, 3626]), '3': dict(name='Closer Still', crop=[120, 0, 1920, 3414])}
T = [276.0, 331.0]  # Dan on camera, early and late in the cut
for k, g in G.items():
    for t in T: ff(['-ss', t, '-i', S, '-an', '-frames:v', 1, '-vf', g['vf']+',scale=540:960:flags=lanczos:in_color_matrix=bt709:in_range=tv', O/f'colour-{k}-{t}.jpg'])
for k, c in C.items():
    x, y, cw, ch = c['crop']
    for t in T: ff(['-ss', t, '-i', S, '-an', '-frames:v', 1, '-vf', f'crop={cw}:{ch}:{x}:{y},'+G['F']['vf']+',scale=540:960:flags=lanczos:in_color_matrix=bt709:in_range=tv', O/f'crop-{k}-{t}.jpg'])
for mode, keys in [('colour', 'FEB'), ('crop', '123')]:
    im = Image.new('RGB', (900, 1640), '#0b1524'); d = ImageDraw.Draw(im)
    for i, k in enumerate(keys):
        d.text((i*300+10, 10), mode+' '+k, fill='white')
        for n, t in enumerate(T): im.paste(Image.open(O/f'{mode}-{k}-{t}.jpg').resize((300, 800)), (i*300, 40+n*800))
    im.save(W/f'evidence/{mode}-comparison.jpg')
start = 274.30  # continuous on-camera speech (If I could pick only one version... through the handles line)
for k, g in G.items():
    ff(['-ss', start, '-i', S, '-t', 12.012, '-an', '-vf', g['vf']+',scale=1080:1920:flags=lanczos:in_color_matrix=bt709:in_range=tv', '-r', '30000/1001',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', O/f'colour-{k}.mp4'])
(W/'look-options.json').write_text(json.dumps(dict(colours=G, crops=C, recommended=dict(colour='F', crop='1', voice='B'), moving_sample_source=[start, start+12.012]), indent=2))
print('LOOK_READY', flush=True)
