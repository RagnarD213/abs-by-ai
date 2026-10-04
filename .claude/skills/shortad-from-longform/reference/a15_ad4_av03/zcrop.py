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
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut")
import landing
FPS = 30000/1001; NTOT = 7160
H_FAR, H_NEAR = 1024.0, 832.0          # 1.875x and 2.31x onto the 1920-tall phone frame
HEAD = 0.04                             # the standard's headroom: 4% of the crop height above the tallest hair
SLOPE = 170.0                           # source px/s (~300 on the phone), the audited cap
# AD 4: his six punch-ins, measured off fit.json (scale median 1.20, >= 8 samples each; the 0.4-2.8 s hook punch has 13),
# as frame ranges on his grid, clipped to the talk beats; each is NEAR, entered and left on a 6-frame ramp. Edges within 8
# frames of his picture cut start ON it (re-audit N2 on Ad 5: a cut then a push 0.2 s later reads as a naked cut + a zoom).
PUNCH_RANGES = [(0, 85), (1509, 1599), (1893, 1989), (3864, 3925), (6206, 6255), (6453, 6514)]
# watch pass on render 1 (2026-09-11):
#  * (9, 85) -> (0, 85): the hook's 9-frame FAR opening put the hair 34 px under the top edge (floor 36; the roll has no
#    headroom, y0 = 0); NEAR magnifies the source headroom (hair 22 px -> 51 phone px). The hook opens on NEAR, no ramp.
#  * (3864, 3963) -> (3864, 3925): his own cut at 3925 is VISIBLE (x2.6) and sat INSIDE his punch, so both sides were forced
#    NEAR -- a naked jump cut at 2.3x. Ending the punch on that cut makes it a zoom cut (3925-3963 becomes FAR).
#  * (6453, 6508) -> (6453, 6514): the 6-frame ramp OUT ended one frame before his cut to the supermarket card -- a zoom twitch
#    immediately followed by a hard cut. The punch now runs to the card; the cut hides the level.
RAMP = 6
# AV-03 round 1 review (2026-10-03): the picture EDL now sits on HIS picture cuts (zedl9.py), so the 09-11 forces that
# existed to hide an audio-splice cut are gone: 3543 (his cut is 3559, pose-matched), 5905 / 5912 (his cut IS 5912, where
# his window wipes off; the window beat now ends there), 6508 (he holds the outgoing take to the supermarket card).
FORCE_VISIBLE = {2937}                  # the audit of 2026-09-11 read his own cut here as a blink-jump at the phone's
                                        # magnification (head ~80 px, ratio 1.11): a level change hides it (skill A7.15)
FORCE_INVISIBLE = {1267}                # his cut on the frame the W1 window exits: the window's exit hides it
# his micro pause trims (the hook) and the start of his closing slow-down are not cuts the eye sees: no level change, no re-land
FORCE_INVISIBLE |= {s['n0'] for s in json.load(open('edl_picture.json')) if s.get('micro')}
VIS_K = 1.8                             # visible join: his change at the join > 1.8x his change around it -- at the 2.3x NEAR magnification a snap that reads small in his 16:9 reads as a jump cut (audit 2026-09-10: 11 naked cuts at 3.0)
DRIFT_PX = 60.0                         # phone px off centre that counts as drift
E = json.load(open('edl_picture.json'))
M = [m for m in json.load(open('measure.json')) if m.get('ok')]
# AV-03: "land on him" means his FACE. The person-mask head value (median column of the mask's top 18 %) sits a median 10
# source px left of his face centre on this roll (p95 20, worst 30+: hair mass, a turned head, raised hands), and the
# delivery gate, which measures the face, read one hold +6.5 % off. measure_face.json is FaceMesh on the same samples.
_FACE = json.load(open('measure_face.json'))
for m in M: m['head'] = _FACE.get(str(m['n']), m['head'] + 9.9)
mn = np.array([m['n'] for m in M]); mt = np.array([m['torso'] for m in M]); mh = np.array([m['hair'] for m in M], float)
mhead = np.array([m['head'] for m in M])
TOR = dict(zip(mn.tolist(), mt.tolist()))

# ---- torso track per picture segment, zero-phase, endpoint-anchored, slope-limited --------------------------------
def build_track(src, width):
    dn, centres, _, _ = landing.vertical_dense(mn, src, E, width, FPS)
    return dict(zip(dn.tolist(), centres.tolist()))
track = build_track(np.array([m['head'] for m in M]), H_FAR * 9/16)
track_head = build_track(mhead, H_NEAR * 9/16)
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
        vis = (punch or ratio > VIS_K or j in FORCE_VISIBLE) and j not in FORCE_INVISIBLE
        JOINS.append(dict(n=j, t=round(j/FPS, 3), ratio=round(ratio, 2), visible=bool(vis), punch=bool(punch)))
        gid.append(gid[-1] + (1 if vis else 0))
    groups = [[r[k] for k in range(len(r)) if gid[k] == g] for g in range(gid[-1] + 1)]
    gpunch = [any(holds[i]['punch'] for i in grp) for grp in groups]
    def levels(first):
        """Fixed groups first (a punch-in is NEAR; the group that leads INTO a punch is FAR, so that join is a zoom cut),
        then every free group alternates away from its fixed neighbours -- propagated BACKWARDS from each fixed group, so
        a run like [free, free, pre-punch FAR, punch NEAR] resolves to [FAR, NEAR, FAR, NEAR]. The forward-only fill left
        3271-3295 and 3295-3324 both FAR (third audit: the 3295 snap never changed)."""
        G = len(groups); lv = [None]*G
        for g in range(G):
            if gpunch[g]: lv[g] = 'NEAR'
        for g in range(G-1):
            if lv[g] is None and gpunch[g+1]: lv[g] = 'FAR'
        # free runs: alternate backwards from the fixed group on the right; a trailing run alternates forward from the left
        g = G-1
        while g >= 0:
            if lv[g] is not None: g -= 1; continue
            k = g
            while k >= 0 and lv[k] is None: k -= 1
            # free run is k+1..g; right neighbour g+1 (fixed) if it exists, else left neighbour k (fixed) if it exists
            if g+1 < G:
                nxt = lv[g+1]
                for i in range(g, k, -1):
                    lv[i] = 'FAR' if nxt == 'NEAR' else 'NEAR'; nxt = lv[i]
            elif k >= 0:
                prev = lv[k]
                for i in range(k+1, g+1):
                    lv[i] = 'FAR' if prev == 'NEAR' else 'NEAR'; prev = lv[i]
            else:
                prev = None
                for i in range(0, g+1):
                    lv[i] = first if prev is None else ('FAR' if prev == 'NEAR' else 'NEAR'); prev = lv[i]
            g = k
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
# AV-03 (2026-10-03): a hold that starts on a zoom RAMP inside continuous footage (his punch-ins at 1509/1599/1893/1989)
# is not a cut, so the crop must not re-land there: landing per hold popped the centre 15-28 source px in one frame.
# Track those chains as ONE segment (the narrowest width in the chain sets the dead band).
# Round 1 review: re-landing the crop at an INVISIBLE (pose-matched) join pops the picture sideways on a cut that is
# otherwise unseen (2189 and 4054 read as jump cuts partly for this). The crop re-lands only where the eye already sees a
# cut: a return from an insert, or a join that carries a level change (a VISIBLE join).
# ROUND 3: his two mid-film punch-ins are EASED (fit.json: 1.0 -> 1.2 over about 24 frames from 1500, back over 36 from 1578;
# again from 1890 and from 1962). Ours snapped in over 6 frames on continuous footage. The crop height now follows his
# fitted scale frame by frame through those stretches; the centre and the hair anchor are unchanged.
_F = sorted([o for o in json.load(open('fit.json')) if 's' in o and o.get('r', 0) >= 0.55], key=lambda o: o['n']); _fn = np.array([o['n'] for o in _F], float); _fs = np.array([o['s'] for o in _F], float)
for a_, b_ in ((1494, 1621), (1884, 1999)):
    yF = next(frames[n][1] for n in range(a_, b_) if n in frames and abs(frames[n][3] - H_FAR) < 1)
    yN = next(frames[n][1] for n in range(a_, b_) if n in frames and abs(frames[n][3] - H_NEAR) < 1)
    for n in range(a_, b_):
        if n not in frames: continue
        s_ = float(np.mean([np.interp(m, _fn, _fs) for m in range(n - 3, n + 4)])); k_ = float(np.clip((s_ - 1.0)/0.2, 0, 1))
        k_ = k_*k_*(3 - 2*k_); H_ = H_FAR + (H_NEAR - H_FAR)*k_; W_ = H_*9/16; cx_ = frames[n][0] + frames[n][2]/2
        frames[n] = [round(float(np.clip(cx_ - W_/2, 0, 1920 - W_)), 2), round(yF + (yN - yF)*k_, 2), round(W_, 2), round(H_, 2)]; zoom[n] = round(H_FAR/H_, 4)
sys.path.insert(0, '.'); import beats as _B
_edges = {b['n0'] for b in _B.timeline()[0]}            # a window opening or closing changes the whole layout: the eye sees a cut,
_cuts = ({s['n0'] for s in E} & {j['n'] for j in JOINS if j['visible']}) | {h['n0'] for h in holds if h['n0'] in _edges}   # so the crop lands on him there (review round 2: 6206 came back 150 px left)
track_segs = []
for h in holds:
    if track_segs and h['n0'] == track_segs[-1]['n1'] and h['n0'] not in _cuts: track_segs[-1]['n1'] = h['n1']
    else: track_segs.append(dict(n0=h['n0'], n1=h['n1']))
# ...and where a window opens or closes INSIDE one hold (6206: the audit window closes mid-take and the crop came back
# 120 px left of him, round 3). The footage is continuous there, so the landing uses the neighbouring samples of the same
# take (one frame away), which is his measured position, not an estimate across a cut.
_mn = [int(v) for v in mn]; _mh = [float(m['head']) for m in M]
_split = []
for sg in track_segs:
    cuts_ = sorted(e for e in _edges if sg['n0'] < e < sg['n1']); a_ = sg['n0']
    for e in cuts_ + [sg['n1']]:
        _split.append(dict(n0=a_, n1=e)); a_ = e
        if e < sg['n1'] and e not in _mn:
            _mn.append(e); _mh.append(float(np.interp(e, mn, [m['head'] for m in M])))
track_segs = _split
_o = np.argsort(_mn); mn = np.array(_mn)[_o]; _HEADS = np.array(_mh)[_o]
centering_report = landing.vertical_crop_frames(frames, track_segs, mn, _HEADS, FPS)
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
