"""DS-31 R2 picture (R1 recipe + Dan's R2 notes: colour reopened, A1 homework tower opener approved): camera holds (approved Pair B crops + Color A, land-then-hold tracking) and B-roll, to base.mp4.
Run after prep.py. --measure-only stops after framing measurement. Parts cache by file presence: delete build/ to redo.
"""
from pathlib import Path
import subprocess, sys, os, json
import numpy as np, cv2
from PIL import Image
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
B = W/'build'; B.mkdir(exist_ok=True); F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
sys.path.insert(0, str(R/'.claude/skills/_shared/cut')); import landing
EDL = json.load(open(W/'edl.json')); S = EDL['source']; TOTAL = EDL['total_frames']
COLOR_A = json.load(open('/Volumes/Extreme/_edit_work/ds28/round5/approved-color.json'))['filter']   # R1 grade, kept for the options page
# R2: the camera grade is the round's colour pick (col/pick.json, written from col/options.json by col_options.py pick X).
PICK = json.load(open(W/'col/pick.json')) if (W/'col/pick.json').exists() else dict(option='A', filter=COLOR_A)
CAM_GRADE = PICK['filter']
STOCK = W/'stock'
ENC = ['-r', '30000/1001', '-c:v', 'libx264', '-preset', 'fast', '-crf', 18, '-pix_fmt', 'yuv420p',
       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
def fr(t): return int(round(t*FPS))
def source_t(n):
    for p in EDL['pieces']:
        n0 = round(p['film0']*FPS)
        if n0 <= n < n0 + p['frames']: return p['start'] + (n - n0)/FPS
    raise ValueError(n)
def piece_of(n):
    for i, p in enumerate(EDL['pieces']):
        n0 = round(p['film0']*FPS)
        if n0 <= n < n0 + p['frames']: return i
JOINS = [round(p['film0']*FPS) for p in EDL['pieces'][1:]]

# Shot list (film seconds, cut in the measured gap before the first word of the next line).
# cam: wide/tight Pair B. broll: file, clip in-point, grade, crop (x0 fraction of source width for 16:9 Dan clips).
WARM = 'eq=saturation=0.88:gamma=0.98,colorbalance=rm=-0.03:bm=0.03'
NEUT = 'eq=saturation=0.92'
PLAN = [
    (0.00, 'broll', dict(f='A1.mp4', at=0.0, g='null', ai=True, line='If you are in college and you have no time to work out')),  # R2: Dan approved A1 (homework tower) for the opener; recipe/a1_cut.py makes stock/A1.mp4 from the gated Flow take
    (2.80, 'tight', None),
    (5.20, 'broll', dict(f='px29582652.mp4', at=0.3, g=WARM + ',eq=brightness=-0.02', line='wasting hours every week on schoolwork')),
    (8.30, 'broll', dict(f='aichat.mp4', at=0.0, g='null', line='Use AI to do it instead')),  # R1 audit: stock showed a spreadsheet, no AI; recipe/aichat.py
    (10.10, 'broll', dict(f='B0448_dan-jump-rope-high-knees-poolside_16x9_8s.mp4', at=1.2, g=NEUT, cx=0.5, line='hours per week freed up to work out')),
    (12.75, 'broll', dict(f='px7092237.mp4', at=1.0, g=NEUT, line='Your teachers are going to hate me for this')),
    (14.60, 'broll', dict(f='px6214854.mp4', at=5.0, g=NEUT, line='but you will get better grades')),
    (16.15, 'wide', None),
    (18.30, 'tight', None),
    (19.25, 'broll', dict(f='cand2/6324555.mp4', at=0.5, g=NEUT, line='almost everything you are learning in school is useless')),  # R1 judge: the bored-girl clip read as an elementary classroom
    (22.10, 'broll', dict(f='cand2/6083402.mp4', at=0.5, g=NEUT + ',colorbalance=rm=0.04:bm=-0.05,eq=gamma=1.03', line='never going to use it, forget most of it within a year')),  # R1 audit: the yawning kid read middle-school age
    (25.65, 'wide', None),
    (28.80, 'tight', None),
    (None, 'wide', None),               # starts on the false-start join (piece 2), framing change hides it
    (34.70, 'tight', None),
    (40.65, 'broll', dict(f='cand2/6145947.mp4', at=1.0, g=NEUT, line='The other students are already doing this')),  # audit 2: open laptops facing camera  # R1 audit: old clip showed a book and a phone
    (None, 'wide', None),               # starts on the retake join (piece 3), entered from B-roll
    (45.85, 'broll', dict(f='cand2/9198195.mp4', at=0.5, g=NEUT, line='writing essays and doing homework by hand')),  # R1 audit: old clip was an adult in a cafe who stopped writing
    (50.70, 'broll', dict(f='B0431_dan-kettlebell-swings-poolside_16x9_9s.mp4', at=5.21, g='eq=gamma=1.12:saturation=0.95', cx=0.5, line='Take the hours you get back and work out every single day')),  # audits 1-3: starts sharp and upright (source frame 156), ends in the upright hold (8.58 s), face lifted
    (54.05, 'tight', None),
    (58.60, 'wide', None),
]
starts = []; ji = iter(JOINS)
for t, k, d in PLAN: starts.append(next(ji) if t is None else fr(t))
assert starts == sorted(starts) and starts[0] == 0
shots = []
for i, ((t, kind, d), n0) in enumerate(zip(PLAN, starts)):
    n1 = starts[i+1] if i + 1 < len(starts) else TOTAL
    s = dict(id=f'S{n0:04d}', n0=n0, n1=n1, a=n0/FPS, b=n1/FPS, kind='talk' if kind in ('wide', 'tight') else 'broll')
    if s['kind'] == 'talk':
        s['size'] = kind; s['crop'] = [2040, 3626, 214] if kind == 'wide' else [1120, 1990, 780]
        assert piece_of(n0) == piece_of(n1 - 1), (s['id'], 'camera hold spans a join')
    else: s.update(d)
    shots.append(s)
# every join is either a framing change between camera holds or entered from B-roll
for j in JOINS:
    k = [s for s in shots if s['n0'] == j]; assert k, ('join not on a shot boundary', j)
    prev = [s for s in shots if s['n1'] == j][0]
    assert prev['kind'] == 'broll' or k[0]['kind'] == 'broll' or prev['size'] != k[0]['size'], ('naked join', j)
for a, b in zip(shots, shots[1:]):
    if a['kind'] == b['kind'] == 'talk': assert a['size'] != b['size'], ('same framing back to back', a['id'], b['id'])

# Framing measurement: every 7 frames and every cut frame of every camera hold, from the raw roll.
anchors = B/'anchors'; anchors.mkdir(exist_ok=True); measure = W/'source-measurements.json'
talk = [s for s in shots if s['kind'] == 'talk']
ns = sorted({n for s in talk for n in list(range(s['n0'], s['n1'], 7)) + [s['n0'], s['n1'] - 1]})
old = {r['n']: r for r in json.load(open(measure)) if abs(r['source_t'] - source_t(r['n'])) < 1e-3} if measure.exists() else {}  # drop rows from an older cut list
todo = [n for n in ns if n not in old]
for n in todo:
    p = anchors/f'{n}.jpg'
    if not p.exists(): ff(['-ss', f'{source_t(n):.4f}', '-i', S, '-frames:v', 1, '-vf', 'scale=540:960', p])
if todo:
    face = subprocess.check_output([str(Path.home()/'.cache/absbyai/facebox'), *[str(anchors/f'{n}.jpg') for n in todo]], text=True)
    fd = {Path(l.split('\t')[0]).stem: l.split('\t')[1] for l in face.splitlines()}
    for n in todo:
        im = np.array(Image.open(anchors/f'{n}.jpg')); x0, y0, x1, y1 = map(int, fd[str(n)].split())
        lum = im @ np.array([.2126, .7152, .0722]); ll = max(0, x0 - 20); rr = min(540, x1 + 20)
        dark = np.where((lum[max(0, y0 - 140):y0, ll:rr] < 30).sum(axis=1) > 15)[0]; assert len(dark), (n, 'hair detection')
        hair = max(0, y0 - 140) + int(dark[0]); _, xx = np.where(lum[hair + 10:hair + 50, ll:rr] < 40); head = (ll + (xx.min() + xx.max())/2)*4
        mask = (im[:, :, 2] > im[:, :, 0]*1.35) & (im[:, :, 1] > im[:, :, 0]*1.25) & (im[:, :, 1] > 75); lx = np.where(mask[240:725].sum(0) > 180)[0]
        old[n] = dict(n=n, source_t=source_t(n), head_x=head, hair_y=hair*4, face=[x0*4, y0*4, x1*4, y1*4], lights=[int(lx.min())*4, int(lx.max() + 1)*4] if len(lx) else None)
    measure.write_text(json.dumps([old[k] for k in sorted(old)], indent=1))
rows = {r['n']: r for r in json.load(open(measure))}; reports = []
for s in talk:
    rr_ = [rows[n] for n in sorted(rows) if s['n0'] <= n < s['n1']]; cw, ch, y = s['crop']
    dn, centres, h, info = landing.vertical_dense([r['n'] for r in rr_], [r['head_x'] for r in rr_], [s], cw, FPS)
    left = np.clip(centres - cw/2, 0, 2160 - cw)
    hair_room = min(r['hair_y'] for r in rr_) - y; assert hair_room >= 40, (s['id'], 'hair', hair_room)
    for r in rr_:
        x = left[r['n'] - s['n0']]; ls = r['lights']; assert ls is not None, (s['id'], r['n'], 'no fixtures found')
        if s['size'] == 'wide': assert x <= ls[0] and x + cw >= ls[1], (s['id'], 'wide fixtures', r['n'], x, ls)
        else: assert x > ls[0] + 130 and x + cw < ls[1] - 130, (s['id'], 'tight fixture', r['n'], x, ls)
    s['tracking'] = [[int(n), round(float(x), 3)] for n, x in zip(dn, left)]
    reports.append(dict(id=s['id'], size=s['size'], samples=len(rr_), hair_min_source_px=hair_room,
                        stats=landing.motion_stats(dn, h, left + cw/2, [s], cw, FPS), clamp_px=float(np.max(np.abs(centres - (left + cw/2))))))
(W/'shots.json').write_text(json.dumps(shots, indent=1)); (W/'framing-report.json').write_text(json.dumps(reports, indent=1))
print('FRAMING OK', len(talk), 'holds', len(ns), 'samples', flush=True)
if '--measure-only' in sys.argv: sys.exit()

def probe(f):
    o = subprocess.check_output([F.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', str(f)], text=True)
    return tuple(map(int, o.strip().split(',')[:2]))
outs = []
for s in shots:
    out = B/f"{s['id']}.mp4"; outs.append(out); nfr = s['n1'] - s['n0']
    if out.exists(): continue
    if s['kind'] == 'talk':
        cw, ch, y = s['crop']
        pts = cv2.approxPolyDP(np.array([[(n - s['n0'])/FPS, x] for n, x in s['tracking']], np.float32), .1, False).reshape(-1, 2).tolist()
        expr = str(pts[0][1]) + ''.join(f'+({bb[1]-aa[1]:.4f})*clip((t-{aa[0]:.5f})/{bb[0]-aa[0]:.5f},0,1)' for aa, bb in zip(pts, pts[1:]) if bb[0] > aa[0])
        vf = f"setpts=PTS-STARTPTS,crop={cw}:{ch}:'{expr}':{y},scale=1080:1920:flags=lanczos,{CAM_GRADE},setsar=1,format=yuv420p"
        ff(['-ss', f"{source_t(s['n0']):.5f}", '-i', S, '-an', '-vf', vf, '-frames:v', nfr] + ENC + [out])
    else:
        src = STOCK/s['f']; w, h = probe(src)
        if w > h:   # 16:9 real Dan clip: fill the frame with a steady 9:16 window on him
            cw = int(round(h*9/16/2)*2); x0 = int(np.clip(s['cx']*w - cw/2, 0, w - cw)); crop = f'crop={cw}:{h}:{x0}:0,'
        else:
            ch = int(round(w*16/9/2)*2); crop = f'crop={w}:{min(h, ch)}:0:{max(0, (h - ch)//2)},' if abs(h/w - 16/9) > .01 else ''
        vf = f"setpts=PTS-STARTPTS,fps=30000/1001,{crop}scale=1080:1920:flags=lanczos,{s['g']},setsar=1,format=yuv420p"
        ff(['-ss', s['at'], '-i', src, '-an', '-vf', vf, '-frames:v', nfr] + ENC + [out])
    got = int(subprocess.check_output([F.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', str(out)], text=True).strip())
    assert got == nfr, (s['id'], 'frames', got, nfr)
    print('PART', s['id'], s['kind'], s.get('size', s.get('f')), nfr, flush=True)
cat = B/'concat.txt'; cat.write_text(''.join(f"file '{p}'\n" for p in outs))
ff(['-f', 'concat', '-safe', 0, '-i', cat, '-c', 'copy', W/'base.mp4'])
print('BASE READY', flush=True)
