"""DS-31 R1 finish: Soft Blue cards (the DS-28 illustrated ribbon, shared softblue components) over base.mp4,
burned captions, approved voice, master + phone copy + SRT + graphic stills.
"""
from pathlib import Path
import subprocess, json, sys, os, re, hashlib
import numpy as np
from PIL import Image, ImageDraw
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True)
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = 'AI Homework SFC R1'
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
sys.path.insert(0, str(R/'.claude/skills/_shared')); import softblue as B
import importlib.util
spec = importlib.util.spec_from_file_location('hg', R/'scripts/video/hyperframes_graphics.py'); HG = importlib.util.module_from_spec(spec); spec.loader.exec_module(HG); C = HG.module('composite')
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
words = json.load(open(W/'words_out.json')); TOTAL = json.load(open(W/'edl.json'))['total_frames']
def at(phrase, after=0):
    toks = phrase.lower().split()
    for i in range(len(words) - len(toks) + 1):
        if words[i]['t0'] >= after and [x['w'].lower().strip('.,!?') for x in words[i:i+len(toks)]] == toks: return words[i]['t0']
    raise ValueError(phrase)
# id, card in (cut), card out (cut), labels, icons, reveal phrases, title
ITEMS = [
    ('G01', 31.94, 34.70, ['Paid Claude plan', 'Free version'], ['check', 'cross'], ['paid claude', 'not the free'], 'Do It The Right Way'),
    ('G02', 34.70, 40.65, ['AI writes it', 'Run AI checkers', 'Fix the flags'], ['doc', 'scan', 'flag'], ['run what', 'ai checkers', 'fix anything'], 'Before You Turn It In'),
    ('G03', 54.06, 58.59, ['Homework hours', 'Workouts'], ['book', 'dumbbell'], ["you'll be shocked", 'how fast'], 'Trade Homework For Training'),
]
graphics = []
for gid, a, b, labels, icons, drivers, title in ITEMS:
    rv = [max(a + .15, at(x, a - 1)) for x in drivers]
    graphics.append(dict(id=gid, t0=round(a*FPS)/FPS, t1=round(b*FPS)/FPS, labels=labels, icons=icons, reveals=rv, driven_by=list(zip(drivers, rv)), title=title, template='softblue:illustrated-ribbon (DS-28)'))
(W/'graphics-sheet.json').write_text(json.dumps(dict(graphics=graphics), indent=1))

def icon(im, name, x, y, s=90):
    d = ImageDraw.Draw(im); col = B.CYAN; lw = 5
    def line(p, c=col): d.line([(x + xx*s, y + yy*s) for xx, yy in p], fill=c, width=lw, joint='curve')
    def box(p): d.rounded_rectangle((x + p[0]*s, y + p[1]*s, x + p[2]*s, y + p[3]*s), radius=10, outline=col, width=lw)
    if name == 'check': d.ellipse((x, y, x + s, y + s), outline=col, width=lw); line([(.27, .52), (.44, .69), (.75, .33)], (64, 200, 110))
    elif name == 'cross': d.ellipse((x, y, x + s, y + s), outline=col, width=lw); line([(.32, .32), (.68, .68)], (235, 87, 87)); line([(.68, .32), (.32, .68)], (235, 87, 87))
    elif name == 'doc': box((.15, .02, .85, .98)); [line([(.3, z), (.7, z)]) for z in (.25, .42, .59, .76)]
    elif name == 'scan': d.ellipse((x + .05*s, y + .05*s, x + .68*s, y + .68*s), outline=col, width=lw); line([(.6, .6), (.95, .95)])
    elif name == 'flag': line([(.2, .05), (.2, .97)]); d.polygon([(x + .22*s, y + .08*s), (x + .85*s, y + .25*s), (x + .22*s, y + .45*s)], outline=col, width=lw)
    elif name == 'book': box((.05, .12, .95, .88)); line([(.5, .12), (.5, .88)]); [line([(.15, z), (.4, z)]) for z in (.35, .55)]; [line([(.6, z), (.85, z)]) for z in (.35, .55)]
    elif name == 'dumbbell': line([(.1, .5), (.9, .5)]); box((.05, .2, .25, .8)); box((.75, .2, .95, .8))
def draw(base, g, t):
    im = Image.fromarray(base.copy()); a, b = g['t0'], g['t1']; q = min(B.ease(t - a, .28), B.ease(b - t, .22)); y = 1070 + int((1 - q)*25)
    B.glass(im, (68, y, 1012, 1360), t, radius=18); B.text(im, (100, y + 14), g['title'], 34, B.CYAN)
    n = len(g['labels']); cw = 880/n
    for i, (label, name, r) in enumerate(zip(g['labels'], g['icons'], g['reveals'])):
        if t < r: continue
        v = B.ease(t - r, .3); x = 100 + i*cw; size = min(90, cw - 28)
        icon(im, name, x + (cw - size)/2, y + 75 + int((1 - v)*18), size)
        px = 32 if n <= 3 else 27
        for j, l in enumerate(B.wrap(label, B.font(px), cw - 12)): B.text(im, (x + (cw - B.text_w(l, B.font(px)))/2, y + 178 + j*42), l, px)
        if i < n - 1 and t >= g['reveals'][i+1]:
            if g['id'] == 'G01': B.text(im, (x + cw - 12, y + 106), 'vs', 28, B.CYAN)
            else:  # drawn chevron: the card font has no glyph for a single guillemet (it printed a comma)
                cx, cy = x + cw, y + 120; ImageDraw.Draw(im).line([(cx - 7, cy - 13), (cx + 6, cy), (cx - 7, cy + 13)], fill=B.CYAN, width=5, joint='curve')
    return np.asarray(im)

# Composite: graphics on frame-rounded intervals [t0, t1).
comp = W/'composite.mp4'
cmd = [F, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-framerate', '30000/1001', '-i', '-', '-an',
       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'fast', '-crf', '17',
       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', str(comp)]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE); still = {}
for n, f in enumerate(C.reader(str(W/'base.mp4'), wh=(1080, 1920))):
    t = n/FPS
    for g in graphics:
        if round(g['t0']*FPS) <= n < round(g['t1']*FPS):
            f = draw(f, g, t)
            if n == round(g['t1']*FPS) - 12: still[g['id']] = f.copy()
    p.stdin.write(np.ascontiguousarray(f).tobytes())
p.stdin.close(); assert p.wait() == 0; assert n + 1 == TOTAL, (n + 1, TOTAL)
for gid, f in still.items(): Image.fromarray(f).save(Q/f'{gid}.jpg', quality=92)

master = Q/f'{NAME} - complete Short.mp4'
ff(['-i', comp, '-i', W/'voice.wav', '-map', '0:v', '-map', '1:a', '-vf', f"ass='{W}/captions.ass'", '-c:v', 'libx264', '-preset', 'slow', '-crf', 17,
    '-c:a', 'aac', '-b:a', '256k', '-ar', 48000, '-frames:v', TOTAL, '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', master])
ff(['-i', master, '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 21, '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', Q/f'{NAME} - phone review.mp4'])
ff(['-ss', 3.5, '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', Q/'poster.jpg'])
def secs(x): h, m, s = x.split(':'); return int(h)*3600 + int(m)*60 + float(s)
def stamp(x): ms = round(x*1000); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
cues = []
for line in (W/'captions.ass').read_text().splitlines():
    if line.startswith('Dialogue:'): f_ = line.split(',', 9); cues.append((secs(f_[1]), secs(f_[2]), re.sub(r'\{[^}]*\}', '', f_[9])))
(Q/f'{NAME}.srt').write_text(''.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(cues)))
print('FINISHED', hashlib.sha256(master.read_bytes()).hexdigest(), flush=True)
