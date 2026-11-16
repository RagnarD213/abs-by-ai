"""DS-30 R1 picture: camera holds and B-roll to base.mp4 (DS-31 R2 picture.py adapted).
Camera: WIDE = the camera's original portrait frame (VIDEO-RULES 2026-11-15: original portrait framing on talking shots),
TIGHT = the approved Pair B punch-in from DS-28/DS-31 on this set ([1120, 1990, 780]); land-then-hold tracking (shared
cut/landing.py) only moves the tight window. Camera grade = col/pick.json (Color C, Dan's pick on DS-31, same roll).
Every join between pieces is a framing change or sits under B-roll. Run after prep.py; --measure-only stops after framing.
Parts cache by file presence: delete build/ to redo.
"""
from pathlib import Path
import subprocess, sys, os, json
import numpy as np, cv2
from PIL import Image
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
B = W/'build'; B.mkdir(exist_ok=True); F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
sys.path.insert(0, str(R/'.claude/skills/_shared/cut')); import landing
EDL = json.load(open(W/'edl.json')); S = EDL['source']; TOTAL = EDL['total_frames']
PICK = json.load(open(W/'col/pick.json')); CAM_GRADE = PICK['filter']
STOCK = W/'stock'
OURA = '/Volumes/Extreme/Zeeshan Content Videos/my honest oura ring review - video 4/my honest oura ring review | zeeshan | 16x9 | video 4.mp4'
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
G = json.load(open(W/'broll-grade.json')) if (W/'broll-grade.json').exists() else {}
def g(k, default): return G.get(k, default)

# Shot list (film seconds; cuts in the measured gaps between lines). None = starts on a piece join.
# broll: f = file in stock/ or 'OURA' (Zeeshan's finished Oura master, BT.709), at = in-point, cx = window centre as a
# fraction of a 16:9 source's width, line = the words it covers.
PLAN = [
    (0.00, 'broll', dict(f='px33016018.mp4', at=2.4, cx=0.43, k='tesla1', line="If you're too busy to work out, I've got the solution.")),  # Tesla on self-driving, wheel turning by itself (Pexels 33016018; the audit found the Oura film's 'Tesla footage' is this same stock clip, so it is cut from the 2560x1440 original and used once)
    (3.10, 'tight', None),                                                            # "You need to trade in your car for a cheaper one that drives itself."
    (7.05, 'broll', dict(f='px37051769.mp4', at=1.0, k='traffic', line='The average American spends about an hour a day in the car.')),
    (10.25, 'wide', None),                                                            # "That's seven hours a week ... stare at the road."
    (14.20, 'broll', dict(f='px32024439.mp4', at=18.0, cx=0.40, k='tesla2', line='Once your car drives for you, that time is yours again.')),  # a different Tesla and drive, driver's hands off the wheel (Pexels 32024439)
    (17.45, 'broll', dict(f='px5636178.mp4', at=2.5, k='phone', line='Take your work calls, make your reservations,')),
    (20.05, 'tight', None),                                                           # "and talk to AI so it's already working before you get to the office."
    (None, 'wide', None),                                                             # P2 join: "The Tesla does check you're watching the road,"
    (25.85, 'broll', dict(f='px39343985.mp4', at=7.0, k='laptop', line='but you can look away ... go on your phone or look at another screen.')),
    (None, 'tight', None),                                                            # P3 join (entered from B-roll): "And a Tesla isn't a rich guy's car."
    (None, 'card', dict(k='kbb', line='Kelley Blue Book ... $47,000 all in. A base Camry is about $48,000.')),   # P4 join under the compare card (graphics.py)
    (42.93, 'wide', None),                                                            # "So you're actually saving money and"
    (47.15, 'broll', dict(f='px32000333.mp4', at=4.2, cx=0.49, pan=[[0, 0.49], [0.4, 0.48], [0.9, 0.445], [1.4, 0.39], [1.9, 0.345], [2.4, 0.335], [3.2, 0.335]], k='robotaxi', line='And if you live somewhere with robotaxis,')),
    (49.56, 'broll', dict(f='px27811282.mp4', at=1.0, cx=0.62, k='austin', line='like here in Austin, you might not need to own a car at all.')),  # R1 audit: the Zoox (Las Vegas) shot no longer sits under 'here in Austin'
    (52.85, 'wide', None),                                                            # "You'll be shocked ... driving."
    (58.93, 'tight', None),                                                           # "Subscribe for more ways to use AI to get in shape."
]
starts = []; ji = iter(JOINS)
for t, k, d in PLAN: starts.append(next(ji) if t is None else fr(t))
assert starts == sorted(starts) and starts[0] == 0, starts
shots = []
for i, ((t, kind, d), n0) in enumerate(zip(PLAN, starts)):
    n1 = starts[i+1] if i + 1 < len(starts) else TOTAL
    s = dict(id=f'S{n0:04d}', n0=n0, n1=n1, a=n0/FPS, b=n1/FPS, kind='talk' if kind in ('wide', 'tight') else kind)
    if s['kind'] == 'talk':
        s['size'] = kind; s['crop'] = [2160, 3840, 0] if kind == 'wide' else [1056, 1878, 780]   # R1 audit: the 1120x1990 window clipped the lamp bulb (bulb top at source row ~2670); same top edge (headroom unchanged), bottom now 2658
        assert piece_of(n0) == piece_of(n1 - 1), (s['id'], 'camera hold spans a join')
    else: s.update(d)
    shots.append(s)
for j in JOINS:
    k = [s for s in shots if s['n0'] == j]; assert k, ('join not on a shot boundary', j)
    prev = [s for s in shots if s['n1'] == j][0]
    assert prev['kind'] != 'talk' or k[0]['kind'] != 'talk' or prev['size'] != k[0]['size'], ('naked join', j)
for a, b in zip(shots, shots[1:]):
    if a['kind'] == b['kind'] == 'talk': assert a['size'] != b['size'], ('same framing back to back', a['id'], b['id'])

# Framing measurement: every 7 frames and every cut frame of every camera hold, from the raw roll.
anchors = B/'anchors'; anchors.mkdir(exist_ok=True); measure = W/'source-measurements.json'
talk = [s for s in shots if s['kind'] == 'talk']
ns = sorted({n for s in talk for n in list(range(s['n0'], s['n1'], 7)) + [s['n0'], s['n1'] - 1]})
def _same(r):
    try: return abs(r['source_t'] - source_t(r['n'])) < 1e-3
    except ValueError: return False   # a row past the end of a shorter cut list
old = {r['n']: r for r in json.load(open(measure)) if _same(r)} if measure.exists() else {}
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
    if s['size'] == 'wide':
        left = np.zeros(s['n1'] - s['n0']); dn = np.arange(s['n0'], s['n1']); centres = left + cw/2; h = None
    else:
        dn, centres, h, info = landing.vertical_dense([r['n'] for r in rr_], [r['head_x'] for r in rr_], [s], cw, FPS)
        left = np.clip(centres - cw/2, 0, 2160 - cw)
    hair_room = min(r['hair_y'] for r in rr_) - y; assert hair_room >= 40, (s['id'], 'hair', hair_room)
    for r in rr_:
        x = left[r['n'] - s['n0']]; ls = r['lights']; assert ls is not None, (s['id'], r['n'], 'no fixtures found')
        if s['size'] == 'tight': assert x > ls[0] + 130 and x + cw < ls[1] - 130, (s['id'], 'tight fixture', r['n'], x, ls)
    s['tracking'] = [[int(n), round(float(x), 3)] for n, x in zip(dn, left)]
    rep = dict(id=s['id'], size=s['size'], samples=len(rr_), hair_min_source_px=int(hair_room), hair_min_out_px=round(hair_room*1920/ch, 1))
    if h is not None: rep.update(stats=landing.motion_stats(dn, h, left + cw/2, [s], cw, FPS), clamp_px=float(np.max(np.abs(centres - (left + cw/2)))))
    reports.append(rep)
(W/'shots.json').write_text(json.dumps(shots, indent=1)); (W/'framing-report.json').write_text(json.dumps(reports, indent=1))
print('FRAMING OK', len(talk), 'holds', len(ns), 'samples', [(r['id'], r['size'], r['hair_min_out_px']) for r in reports], flush=True)
if '--measure-only' in sys.argv: sys.exit()

def probe(f):
    o = subprocess.check_output([F.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', str(f)], text=True)
    return tuple(map(int, o.strip().split(',')[:2]))
outs = []
for s in shots:
    out = B/f"{s['id']}.mp4"; outs.append(out); nfr = s['n1'] - s['n0']
    if out.exists(): continue
    if s['kind'] == 'card':   # placeholder under the opaque compare card (graphics replace these frames)
        ff(['-f', 'lavfi', '-i', 'color=c=0x0a2648:s=1080x1920:r=30000/1001', '-frames:v', nfr] + ENC + [out])
    elif s['kind'] == 'talk':
        cw, ch, y = s['crop']
        if s['size'] == 'wide': crop = ''
        else:
            pts = cv2.approxPolyDP(np.array([[(n - s['n0'])/FPS, x] for n, x in s['tracking']], np.float32), .1, False).reshape(-1, 2).tolist()
            expr = str(pts[0][1]) + ''.join(f'+({bb[1]-aa[1]:.4f})*clip((t-{aa[0]:.5f})/{bb[0]-aa[0]:.5f},0,1)' for aa, bb in zip(pts, pts[1:]) if bb[0] > aa[0])
            crop = f"crop={cw}:{ch}:'{expr}':{y},"
        vf = f"setpts=PTS-STARTPTS,{crop}scale=1080:1920:flags=lanczos,{CAM_GRADE},setsar=1,format=yuv420p"
        ff(['-ss', f"{source_t(s['n0']):.5f}", '-i', S, '-an', '-vf', vf, '-frames:v', nfr] + ENC + [out])
    else:
        src = OURA if s['f'] == 'OURA' else STOCK/s['f']; w, h = probe(src)
        dec = 'scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,' if s['f'] == 'OURA' else ''
        if w > h:
            cw = int(round(h*9/16/2)*2); x0 = int(np.clip(s['cx']*w - cw/2, 0, w - cw)); crop = f'crop={cw}:{h}:{x0}:0,'
            if s.get('pan'):   # the window follows a subject that crosses the frame (robotaxi pod), piecewise linear in clip time
                px = [[t_, float(np.clip(c*w - cw/2, 0, w - cw))] for t_, c in s['pan']]
                expr = f"{px[0][1]:.1f}" + ''.join(f'+({bb[1]-aa[1]:.2f})*clip((t-{aa[0]})/{bb[0]-aa[0]},0,1)' for aa, bb in zip(px, px[1:]))
                crop = f"crop={cw}:{h}:'{expr}':0,"
        else:
            ch = int(round(w*16/9/2)*2); crop = f'crop={w}:{min(h, ch)}:0:{max(0, (h - ch)//2)},' if abs(h/w - 16/9) > .01 else ''
        sfps = subprocess.check_output([F.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', str(src)], text=True).strip()
        n_, d_ = map(int, sfps.split('/')); sfps = n_/d_
        # watch judge: a 24p source brought to 29.97 by repeated frames judders (every 5th frame a hold). Play each source
        # frame once at 29.97 instead (a 1.25x speed-up, frames never blended or held; the method Dan approved on DS-107's opener).
        rt = 'setpts=N/(30000/1001)/TB' if sfps < 29 else 'setpts=PTS-STARTPTS,fps=30000/1001'
        s['speed'] = round(29.97/sfps, 3) if sfps < 29 else 1.0
        vf = f"{rt},{dec}{crop}scale=1080:1920:flags=lanczos,{g(s['k'], 'null')},setsar=1,format=yuv420p"
        ff(['-ss', s['at'], '-i', src, '-an', '-vf', vf, '-frames:v', nfr] + ENC + [out])
    got = int(subprocess.check_output([F.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', str(out)], text=True).strip())
    assert got == nfr, (s['id'], 'frames', got, nfr)
    print('PART', s['id'], s['kind'], s.get('size', s.get('f')), nfr, flush=True)
cat = B/'concat.txt'; cat.write_text(''.join(f"file '{p}'\n" for p in outs))
ff(['-f', 'concat', '-safe', 0, '-i', cat, '-c', 'copy', W/'base.mp4'])
print('BASE READY', flush=True)
