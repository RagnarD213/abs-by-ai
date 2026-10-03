#!/usr/bin/env python3
"""NEW VERTICAL STANDARD (2026-10-03): the shared landing.py owns horizontal tracking.
Measure head centres at every picture/hold start. Land, hold within 3.3% of crop width,
then ease toward the edge; never anchor the exit. The historical notes below describe
other preserved recipe decisions, not a replacement tracking method.

The talking-head crop, frame by frame, to Dan's LOCKED framing standard (memory framing-standard-hair-anchored):
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
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "_shared", "cut")))
import landing
FPS = 24.0; NTOT = 5980
H_FAR, H_NEAR = 1024.0, 832.0          # 1.875x and 2.31x onto the 1920-tall phone frame
HEAD = 0.04                             # the standard's headroom: 4% of the crop height above the tallest hair
SLOPE = 170.0                           # source px/s (~300 on the phone), the audited cap
RAMPS = {2615: 4, 3875: 4}              # his punch-in ramps: start frame -> frames
PUNCH = {(2615, 2748), (3875, 4048)}
VIS_K = 3.0                             # visible join: his change at the join > 3x his change around it (gap: 2.0 / 4.3)
DRIFT_PX = 60.0                         # phone px off centre that counts as drift
E = json.load(open('edl_picture.json'))
M = [m for m in json.load(open('measure.json')) if m.get('ok')]
mn = np.array([m['n'] for m in M]); mt = np.array([m['torso'] for m in M]); mh = np.array([m['hair'] for m in M], float)
TOR = dict(zip(mn.tolist(), mt.tolist()))

# ---- holds: picture segments, split where his punch-in starts ---------------------------------------------------
holds = []
for s in E:
    cuts = [s['n0']] + [r for r in RAMPS if s['n0'] < r < s['n1']] + [s['n1']]
    for a, b in zip(cuts[:-1], cuts[1:]):
        holds.append(dict(n0=a, n1=b, seg=(s['n0'], s['n1']), ramp=RAMPS.get(a, 0)))
for h in holds:
    sel = (mn >= h['n0']) & (mn < h['n1'])
    h['hmin_own'] = float(mh[sel].min()) if sel.any() else float(np.interp((h['n0']+h['n1'])/2, mn, mh))
# ---- torso track per picture segment, zero-phase, endpoint-anchored, slope-limited --------------------------------
def build_track(src, width):
    dn, centres, _, _ = landing.vertical_dense(mn, src, E, width, FPS)
    return dict(zip(dn.tolist(), centres.tolist()))
track = build_track(np.array([m['head'] for m in M]), H_FAR * 9/16)
# ---- which joins are visible: HIS render's own frame-to-frame change at the join ---------------------------------
GR = np.memmap('his256.gray', np.uint8, 'r').reshape(-1, 144, 256)      # his cut, 256x144 gray; frame n = his frame n
def hdiff(n): return float(np.abs(GR[n].astype(np.int16) - GR[n-1].astype(np.int16)).mean())
def join_ratio(j):
    loc = [hdiff(k) for k in list(range(j-6, j-1)) + list(range(j+2, j+7))]
    return hdiff(j) / max(float(np.median(loc)), 0.5)
def drift(idx, H):
    """longest run of measure samples (every ~6 frames) with the torso > DRIFT_PX phone px off the crop centre"""
    best = cur = 0; W = H*9/16
    for i in idx:
        h = holds[i]
        for n in sorted(k for k in TOR if h['n0'] <= k < h['n1']):
            cx = float(np.clip(track[n] - W/2, 0, 1920 - W)) + W/2
            cur = cur + 1 if abs(TOR[n] - cx)*1920/H > DRIFT_PX else 0
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
        punch = holds[b]['ramp'] > 0 or (holds[a]['n0'], holds[a]['n1']) in PUNCH
        vis = punch or ratio > VIS_K
        JOINS.append(dict(n=j, t=round(j/FPS, 3), ratio=round(ratio, 2), visible=bool(vis), punch=bool(punch)))
        gid.append(gid[-1] + (1 if vis else 0))
    groups = [[r[k] for k in range(len(r)) if gid[k] == g] for g in range(gid[-1] + 1)]
    best = None
    for first in ('FAR', 'NEAR'):
        other = 'NEAR' if first == 'FAR' else 'FAR'
        lv = [first if g % 2 == 0 else other for g in range(len(groups))]
        if any(lv[g] != 'NEAR' for g, grp in enumerate(groups) for i in grp if (holds[i]['n0'], holds[i]['n1']) in PUNCH):
            continue
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
    W = H*9/16; cx = track[n]
    x0 = float(np.clip(cx - W/2, 0, 1920 - W))
    frames[n] = [round(x0, 2), round(y0, 2), round(W, 2), round(H, 2)]
    zoom[n] = round(H_FAR / H, 4)
centering_report = landing.vertical_crop_frames(frames, holds, mn, np.array([m['head'] for m in M]), FPS)
json.dump(centering_report, open('vertical-centering-stats.json', 'w'), indent=2)
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
