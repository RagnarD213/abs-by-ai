#!/usr/bin/env python3
"""Recover HIS use of every piece of media we rebuild from source: in-point + rate of each AI clip, the app recording's
time map inside both app beats (he retimes it), and the meal-plan screenshot's scroll offset. Everything is matched on
downscaled gray frames with NCC. Writes media_map.json."""
import json, subprocess, numpy as np, cv2
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
REV5 = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/00 ASSETS USED IN THE REFERENCE AD"
def frames(src, w, h, ss=None, to=None, fps=None, crop=None):
    vf = ([f'crop={crop}'] if crop else []) + ([f'fps={fps}'] if fps else []) + [f'scale={w}:{h}', 'format=gray']
    cmd = [FF, '-v', 'error'] + (['-ss', f'{ss:.4f}'] if ss is not None else []) + (['-to', f'{to:.4f}'] if to is not None else []) + \
          ['-i', src, '-vf', ','.join(vf), '-f', 'rawvideo', '-']
    b = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, h, w).astype(np.float32)
def z(a): a = a - a.mean(); return a/max(np.sqrt((a*a).sum()), 1e-6)
OUT = {}
# ---- AI clips (full frame 16:9 in his cut) --------------------------------------------------------
CLIPS = dict(pool=(2748, 2792, 'ai_women_pool.mp4'), gym=(2792, 2832, 'ai_respect_gym.mp4'),
             beach=(2832, 2970, 'ai_health_beachrun.mp4'), dad=(3478, 3618, 'ai_busydad_kitchen.mp4'))
for k, (n0, n1, f) in CLIPS.items():
    src = f'{REV5}/{f}'
    fp = json.loads(subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-show_entries',
                    'stream=r_frame_rate,duration','-of','json',src],capture_output=True,text=True).stdout)['streams'][0]
    sfps = eval(fp['r_frame_rate']); S = frames(src, 160, 90)
    H = frames('reference.mov', 160, 90, ss=n0/24-0.02, to=n1/24-0.02)[:n1-n0]
    Sz = np.stack([z(s[8:78]) for s in S])            # rows 8-78: clear of his label and CTA band
    best = []
    for i in range(0, len(H), 2):
        v = Sz.reshape(len(Sz), -1) @ z(H[i][8:78]).ravel(); j = int(np.argmax(v)); best.append((i, j, float(v[j])))
    ii = np.array([b[0] for b in best]); jj = np.array([b[1] for b in best]); rr = np.array([b[2] for b in best])
    ok = rr > 0.6
    if ok.sum() >= 3:
        A = np.vstack([ii[ok]/24, np.ones(ok.sum())]).T; (rate, inp), *_ = np.linalg.lstsq(A, jj[ok]/sfps, rcond=None)
    else: rate, inp = 1.0, 0.0
    OUT[k] = dict(src=src, n0=n0, n1=n1, src_fps=sfps, src_dur=float(fp['duration']), in_s=round(float(inp),3), rate=round(float(rate),3),
                  r_med=round(float(np.median(rr)),3), pairs=[(int(a), int(b), round(c,3)) for a, b, c in best])
    print(f'{k:6s} his {n0/24:7.3f}-{n1/24:7.3f}  src in {inp:6.3f}s  rate {rate:.3f}  r med {np.median(rr):.3f}  src dur {float(fp["duration"]):.2f}', flush=True)
# ---- app recording: his panel -> recording time ------------------------------------------------
APP = f'{LIB}/09_CLIP_app-generate-future-self.mp4'
R = frames(APP, 66, 144, fps=20)                         # 20 fps thumbnails of the 1320x2868 recording
Rz = np.stack([z(r) for r in R])
def panel_box(img):
    fld = np.array([20, 32, 22], np.float32)
    d = np.abs(img[..., :3].astype(np.float32) - fld).sum(2) > 30
    d[:, :520] = False; d[:, 1400:] = False; d[860:, :] = False     # centre column, above his CTA band
    ys, xs = np.nonzero(d)
    return (int(np.percentile(xs, 1)), int(np.percentile(ys, 1)), int(np.percentile(xs, 99)), int(np.percentile(ys, 99))) if len(xs) > 500 else None
def app_map(n0, n1, step=3):
    res = []
    for n in range(n0, n1, step):
        p = '/tmp/_zm.png'
        subprocess.run([FF,'-v','error','-y','-ss',f'{n/24-0.02:.4f}','-i','reference.mov','-frames:v','1',p], check=True)
        im = cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB); bx = panel_box(im)
        if bx is None: res.append((n, None, 0.0, None)); continue
        x0, y0, x1, y1 = bx
        # the panel's top edge is the screen's top: compare the visible part against the same fraction of the recording
        g = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY).astype(np.float32)
        ph = int(round(66 * (y1-y0)/(x1-x0)))             # visible height in thumbnail rows at the recording's width
        ph = min(ph, 144)
        t = cv2.resize(g, (66, ph), interpolation=cv2.INTER_AREA)
        v = np.array([float((z(r[:ph]) * z(t)).sum()) for r in R])
        j = int(np.argmax(v)); res.append((n, round(j/20, 3), round(float(v[j]), 3), bx))
    return res
for k, (n0, n1) in dict(app_a=(1808, 1999), app_b=(4291, 4568)).items():
    m = app_map(n0, n1)
    OUT[k] = dict(src=APP, n0=n0, n1=n1, map=m)
    print(k, ' '.join(f'{n/24:.2f}->{t}({r:.2f})' for n, t, r, _ in m if t is not None), flush=True)
# ---- meal plan scroll ----------------------------------------------------------------------------
PNG = f'{LIB}/12_APP_meal-plan.png'
pg = cv2.cvtColor(cv2.imread(PNG), cv2.COLOR_BGR2GRAY).astype(np.float32)          # 900 x 2448
sc = []
for n in range(5477, 5675, 4):
    p = '/tmp/_zm.png'
    subprocess.run([FF,'-v','error','-y','-ss',f'{n/24-0.02:.4f}','-i','reference.mov','-frames:v','1',p], check=True)
    im = cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB); bx = panel_box(im)
    if bx is None: sc.append((n, None, None)); continue
    x0, y0, x1, y1 = bx; s = 900/(x1-x0)
    g = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY).astype(np.float32)
    t = cv2.resize(g, (900, int((y1-y0)*s)), interpolation=cv2.INTER_CUBIC)
    if t.shape[0] >= pg.shape[0]: sc.append((n, 0, bx)); continue
    rr = cv2.matchTemplate(pg, t, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(rr)
    sc.append((n, int(ml[1]), bx, round(float(mv), 3)))
OUT['meal_scroll'] = dict(src=PNG, n0=5477, n1=5675, offsets=sc)
print('meal scroll', [(round(a[0]/24, 2), a[1], a[3] if len(a) > 3 else None) for a in sc])
json.dump(OUT, open('media_map.json', 'w'))
