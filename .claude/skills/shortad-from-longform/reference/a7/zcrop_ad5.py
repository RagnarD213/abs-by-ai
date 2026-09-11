#!/usr/bin/env python3
"""The talking-head crop, frame by frame, to Dan's LOCKED framing standard (memory framing-standard-hair-anchored):
  * two levels only, FAR and NEAR, both anchored to the MEASURED TOP OF HIS HAIR:  y0 = min hair top - 4% of h
    (clamped to the frame -- this 8/14 roll has only ~35-45 px above his hair, so FAR cannot gain headroom);
  * the level changes ONLY at a VISIBLE talk join -- the standard's own words are "alternating across visible joins".
    Zeeshan pose-matched five of his splices (43.46 / 92.38 / 124.75 / 170.08 / 198.17 s): his render's own
    frame-to-frame change there is 1.0-2.0x the change around it, against >= 4.3x at every real cut. A zoom at such a
    join turns his invisible splice into a visible one (independent audit, 2026-09-10), so the level -- and the
    hair-anchored y0 -- carry straight across it;
  * his own two big punch-ins (108.96 s, 161.46 s) are NEAR, entered on his own 4-frame ramp;
  * the level a talk run OPENS on is chosen, not assumed: the parity that keeps Dan's longest sustained off-centre
    stretch (> 60 px on the phone, measured torso vs the crop centre) shortest, FAR on a tie. The crop deliberately does
    not chase a lean, and a lean magnified at NEAR is what walked the first cutdown to -132 px for 1.0 s;
  * x follows the Apple Vision torso anchor, smoothed INSIDE each picture segment (zero-phase, endpoint-anchored,
    slope-limited -- skill lessons A4.0ac/A5.14/A5.18), so a cut lands on him and the crop never whips across a join.
Writes crop.json: per talk frame (x0, y0, w, h) in 1920x1080 base pixels, zoom_per_frame for qc check 12, the joins."""
import json, numpy as np
FPS = 30000/1001; NTOT = 7036
H_FAR, H_NEAR = 1024.0, 832.0          # 1.875x and 2.31x onto the 1920-tall phone frame
HEAD = 0.04                             # the standard's headroom: 4% of the crop height above the tallest hair
SLOPE = 170.0                           # source px/s (~300 on the phone), the audited cap
# his punch-ins, measured off fit.json (scale 1.14-1.24, >= 8 samples), as frame ranges on his grid; each is NEAR,
# entered and left on a 6-frame ramp (his own ramps read 4-8 frames). Windows (Dan in a full-height window) carry none.
PUNCH_RANGES = [(1902, 1999), (2536, 2605), (2772, 2832), (3324, 3438), (3918, 3991), (4116, 4194), (4660, 4739),
                (4939, 5023), (5263, 5323), (6961, 7036)]   # a punch that starts within 8 frames of his picture cut starts ON it: a cut and then a push 0.2 s later reads as a naked cut plus a zoom (re-audit N2)   # edges snapped to his picture cuts where the 6-frame fit smeared them (audit: 2832 is his zoom-OUT)
RAMP = 6
FORCE_VISIBLE = {1729, 2056, 3295, 5744, 6340}   # joins the independent re-audit read as pose snaps at their ratio (1.1-1.5): a level change hides them
VIS_K = 1.8                             # visible join: his change at the join > 1.8x his change around it -- at the 2.3x NEAR magnification a snap that reads small in his 16:9 reads as a jump cut (audit 2026-09-10: 11 naked cuts at 3.0)
DRIFT_PX = 60.0                         # phone px off centre that counts as drift
E = json.load(open('edl_picture.json'))
M = [m for m in json.load(open('measure.json')) if m.get('ok')]
mn = np.array([m['n'] for m in M]); mt = np.array([m['torso'] for m in M]); mh = np.array([m['hair'] for m in M], float)
mhead = np.array([m['head'] for m in M])
TOR = dict(zip(mn.tolist(), mt.tolist()))

# ---- torso track per picture segment, zero-phase, endpoint-anchored, slope-limited --------------------------------
def limit(x, t, lim):
    o = [x[0]]
    for i in range(1, len(x)):
        dt = (t[i]-t[i-1])/FPS; o.append(o[-1] + float(np.clip(x[i]-o[-1], -lim*dt, lim*dt)))
    return np.array(o)
def build_track(src):
    tr = {}
    for s in E:
        sel = (mn >= s['n0']) & (mn < s['n1']); t = mn[sel]; x = src[sel]
        if len(t) == 0: continue
        L = len(x); k = 3
        med = np.array([np.median(x[j-min(k, j, L-1-j):j+min(k, j, L-1-j)+1]) for j in range(L)])
        if L >= 3:
            f = limit(med, t, SLOPE); b = limit(med[::-1], (-t)[::-1], SLOPE)[::-1]
            w = (t - t[0]) / max(1, t[-1] - t[0]); med = (1-w)*f + w*b
        for n in range(s['n0'], s['n1']):
            tr[n] = float(np.interp(n, t, med))
    return tr
track = build_track(mt)                    # torso: the FAR crop's anchor (hands cannot drag it)
track_head = build_track(0.4*mt + 0.6*mhead)   # NEAR shows head and shoulders: the head leads (audit: a 53 px head lean read as 122 px off)
# ---- a punch-in whose lean cannot be followed at NEAR is demoted to FAR (skill A6.21: the crop does not chase a lean;
# re-audit 2026-09-10: at 5263-5323 the head ran 96 px off for 1.0 s while the crop chased at the slope cap) --------------
HEADX = dict(zip(mn.tolist(), (0.4*mt + 0.6*mhead).tolist()))
HEADP = dict(zip(mn.tolist(), mhead.tolist()))          # the viewer sees the HEAD; the lean check measures it, not the blend
def _lean_run(p0, p1, H):
    best = cur = 0; W = H*9/16
    for n in sorted(k for k in HEADX if p0 <= k < p1):
        cx = float(np.clip(track_head[n] - W/2, 0, 1920 - W)) + W/2
        cur = cur + 1 if abs(HEADP[n] - cx)*1920/H > DRIFT_PX else 0; best = max(best, cur)
    return best
_keep = []
for p0, p1 in PUNCH_RANGES:
    r = _lean_run(p0, p1, H_NEAR)
    if r >= 4: print(f'punch {p0}-{p1} DEMOTED to FAR: head > {DRIFT_PX:.0f} px off for {r} samples (~{r*6/FPS:.1f} s) at NEAR')
    else: _keep.append((p0, p1))
PUNCH_RANGES = _keep
# ---- holds: picture segments, split where his punch-in starts ---------------------------------------------------
holds = []
for s in E:
    edges = sorted({s['n0'], s['n1']} | {e for p in PUNCH_RANGES for e in p if s['n0'] < e < s['n1']})
    for a, b in zip(edges[:-1], edges[1:]):
        inpunch = any(p0 <= a < p1 for p0, p1 in PUNCH_RANGES)
        # a ramp when this hold begins at a punch edge inside the segment (in or out), never at a picture cut
        ramp = RAMP if (a != s['n0'] and any(a in p for p in PUNCH_RANGES)) else 0
        holds.append(dict(n0=a, n1=b, seg=(s['n0'], s['n1']), ramp=ramp, punch=inpunch))
for h in holds:
    sel = (mn >= h['n0']) & (mn < h['n1'])
    h['hmin_own'] = float(mh[sel].min()) if sel.any() else float(np.interp((h['n0']+h['n1'])/2, mn, mh))
# ---- which joins are visible: HIS render's own frame-to-frame change at the join ---------------------------------
GR = np.memmap('his256.gray', np.uint8, 'r').reshape(-1, 144, 256)      # his cut, 256x144 gray; frame n = his frame n
def hdiff(n): return float(np.abs(GR[n].astype(np.int16) - GR[n-1].astype(np.int16)).mean())
def join_ratio(j):
    loc = [hdiff(k) for k in list(range(j-6, j-1)) + list(range(j+2, j+7))]
    return hdiff(j) / max(float(np.median(loc)), 0.5)
def drift(idx, H):
    """longest run of measure samples (every ~6 frames) with the level's anchor > DRIFT_PX phone px off the crop centre"""
    best = cur = 0; W = H*9/16; near = H < 900
    for i in idx:
        h = holds[i]
        for n in sorted(k for k in TOR if h['n0'] <= k < h['n1']):
            tr = track_head if near else track; an = HEADX if near else TOR
            cx = float(np.clip(tr[n] - W/2, 0, 1920 - W)) + W/2
            cur = cur + 1 if abs(an[n] - cx)*1920/H > DRIFT_PX else 0
            best = max(best, cur)
    return best
# ---- continuous talk runs -> groups (a new group at every VISIBLE join) -> levels ---------------------------------
runs = []
for i, h in enumerate(holds):
    if runs and holds[runs[-1][-1]]['n1'] == h['n0']: runs[-1].append(i)
    else: runs.append([i])
JOINS = []
for r in runs:
    gid = [0]
    for a, b in zip(r[:-1], r[1:]):
        j = holds[b]['n0']; ratio = join_ratio(j)
        punch = holds[b]['ramp'] > 0 or holds[a]['punch'] or holds[b]['punch']
        vis = punch or ratio > VIS_K or j in FORCE_VISIBLE
        JOINS.append(dict(n=j, t=round(j/FPS, 3), ratio=round(ratio, 2), visible=bool(vis), punch=bool(punch)))
        gid.append(gid[-1] + (1 if vis else 0))
    groups = [[r[k] for k in range(len(r)) if gid[k] == g] for g in range(gid[-1] + 1)]
    gpunch = [any(holds[i]['punch'] for i in grp) for grp in groups]
    def levels(first):
        lv, prev = [], None
        for g, grp in enumerate(groups):
            nxt_punch = g + 1 < len(groups) and gpunch[g + 1]
            if gpunch[g]: lvl = 'NEAR'
            elif nxt_punch: lvl = 'FAR'                       # the join into a punch-in must be a zoom cut
            elif prev is None: lvl = first
            else: lvl = 'FAR' if prev == 'NEAR' else 'NEAR'
            lv.append(lvl); prev = lvl
        return lv
    best = None
    for first in ('FAR', 'NEAR'):
        lv = levels(first)
        score = max(drift(grp, H_FAR if lv[g] == 'FAR' else H_NEAR) for g, grp in enumerate(groups))
        if best is None or score < best[0]: best = (score, lv)
    for g, grp in enumerate(groups):
        lvl = best[1][g]; H = H_FAR if lvl == 'FAR' else H_NEAR
        hm = min(holds[i]['hmin_own'] for i in grp)
        for i in grp:
            holds[i].update(level=lvl, group=holds[grp[0]]['n0'], hmin=hm, h=H,
                            y0=float(np.clip(hm - HEAD*H, 0, 1080 - H)), run_drift_samples=best[0])
            holds[i]['headroom_phone_px'] = round((holds[i]['hmin_own'] - holds[i]['y0']) / H * 1920, 1)
# ---- per frame -----------------------------------------------------------------------------------------------------
frames = {}
zoom = [1.0]*NTOT
by_n = {}
for i, h in enumerate(holds):
    for n in range(h['n0'], h['n1']): by_n[n] = i
for n, i in sorted(by_n.items()):
    h = holds[i]; H, y0 = h['h'], h['y0']
    if h['ramp'] and n < h['n0'] + h['ramp']:              # his 4-frame push-in from the previous (FAR) hold
        p = holds[i-1]; k = (n - h['n0'] + 1) / (h['ramp'] + 1); k = 1 - (1-k)**3
        H = p['h'] + (h['h'] - p['h'])*k; y0 = p['y0'] + (h['y0'] - p['y0'])*k
    W = H*9/16; cx = (track_head if h['level'] == 'NEAR' else track)[n]
    x0 = float(np.clip(cx - W/2, 0, 1920 - W))
    frames[n] = [round(x0, 2), round(y0, 2), round(W, 2), round(H, 2)]
    zoom[n] = round(H_FAR / H, 4)
json.dump(dict(frames={str(k): v for k, v in frames.items()}, holds=holds, zoom_per_frame=zoom,
               H_FAR=H_FAR, H_NEAR=H_NEAR, joins=JOINS), open('crop.json', 'w'))
print('talk joins (his change at the join / around it):')
for j in JOINS:
    print(f"  {j['n']:5d} {j['t']:7.2f}s  x{j['ratio']:5.1f}  {'VISIBLE' if j['visible'] else 'invisible -- level carries'}{'  (punch-in)' if j['punch'] else ''}")
talk = len(frames); near = sum(1 for z in zoom if z > 1.05)
print(f'{len(holds)} holds, {talk} talk frames, NEAR {100*near/talk:.0f}% of talk')
hr = np.array([h['headroom_phone_px'] for h in holds])
print(f'hair headroom on the phone per hold (px of 1920): min {hr.min()} median {np.median(hr)} max {hr.max()}')
for h in holds:
    print(f"  {h['n0']:5d}-{h['n1']:5d} {h['level']:4s} group {h['group']:5d} hmin {h['hmin_own']:4.0f} y0 {h['y0']:5.1f} "
          f"headroom {h['headroom_phone_px']:5.1f}px  run drift {h['run_drift_samples']} samples{'  ramp' if h['ramp'] else ''}")
v = []
for s in E:
    xs = [frames[n][0] for n in range(s['n0'], s['n1']) if n in frames]
    v += list(np.abs(np.diff(xs))*FPS)
print(f'crop pan inside segments: p90 {np.percentile(v,90):.0f} p99 {np.percentile(v,99):.0f} max {max(v):.0f} source px/s')
