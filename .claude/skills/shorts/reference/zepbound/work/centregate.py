#!/usr/bin/env python3
"""CHECK 17 - CENTERING MEASURED ON THE DELIVERED FILE.

Not on the plan, not on the crop table: on the finished 1080x1920 frames a viewer sees. The
Ad-2 vertical shipped two rejected versions because the track, the beat sheet and the A/B all
looked right while a bad filter expression put him 300px off - nothing that inspects the build
plan can see that. So: sample every delivered short at 2 fps, run Apple Vision person
segmentation on each frame, anchor on the TORSO BLOCK (recentre/anchor.py - the hands leave
frame while he talks and would drag a centroid 100-500px), and report pixels off x=540.

Also reports CONTAINMENT: how much of the silhouette is cut by the picture's left/right edge on
each side. Arms leaving a 9:16 frame is normal; ASYMMETRIC clipping (cut on one side, empty
margin on the other) is the fault Dan flagged on v2-short3 (133px offset / 68px cut-off).
Thresholds from that calibration: <=35px invisible, >=60px re-cut, >=110px on any shot re-cut.
"""
import glob, json, os, subprocess, sys
import numpy as np, cv2
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'recentre'))
from anchor import anchors
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
L = json.load(open(os.path.join(HERE, 'layout.json')))
DROP = L['dropTop']; CW = 1080
segs = json.loads(subprocess.check_output(
    ['node', '-e', "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"],
    cwd=HERE, stderr=subprocess.DEVNULL).decode())
only = sys.argv[1:]
FPS = 2
out = {}
bad = 0
for sid, slug in segs:
    if only and sid not in only: continue
    src = os.path.join(HERE, 'out', f'{sid.lower()}_{slug}.mp4')
    if not os.path.exists(src): print(f'  {sid}: not rendered'); continue
    d = os.path.join(HERE, 'work', 'cg', sid)
    for f in glob.glob(os.path.join(d, '*')): os.remove(f)
    os.makedirs(d, exist_ok=True)
    # picture area only (below the title band), at 480 wide for Vision speed
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', src,
                    '-vf', f'fps={FPS},crop={CW}:{1920-DROP}:0:{DROP},scale=480:-2',
                    os.path.join(d, '%03d.png')], check=True)
    pngs = sorted(p for p in glob.glob(os.path.join(d, '[0-9][0-9][0-9].png')) if not os.path.basename(p).startswith('._'))
    r = subprocess.run([os.path.join(HERE, 'recentre', 'personmask'), d] + pngs, capture_output=True, text=True)
    assert 'ERR' not in r.stdout, r.stdout
    offs, clipL, clipR, n_none = [], [], [], 0
    for p in pngs:
        m = cv2.imread(p.replace('.png', '.mask.png'), cv2.IMREAD_GRAYSCALE)
        if m is None: n_none += 1; continue
        mm = m > 127
        a = anchors(mm)
        if not a: n_none += 1; continue
        w = mm.shape[1]; k = CW / w
        offs.append((a['head'] * w - w / 2) * k)   # HEAD anchor - see work/mkcrops.py
        # silhouette touching the frame edge: column coverage at the edges (as px of subject height)
        colcov = mm.sum(0) / mm.shape[0]
        clipL.append(float(colcov[:3].max()) * (1920 - DROP)); clipR.append(float(colcov[-3:].max()) * (1920 - DROP))
    o = np.array(offs)
    # PER-SHOT verdicts. Dan's calibration on v2-short3 was a STATIC crop offset (133px) on a
    # locked tripod; the frame-to-frame spread here is his own sway, which a static crop cannot
    # and should not follow (a pan on a locked tripod reads as a mistake - skill Step 5). So the
    # gate judges each shot's MEDIAN offset: re-cut at >=60px weighted or >=110px on any shot.
    man = [x for x in json.load(open(os.path.join(HERE, 'shots', 'manifest.json'))) if x['seg'] == sid]
    t0 = 0.0; shots = []
    for x in man:
        i0 = int(round(t0 * FPS)); i1 = int(round((t0 + x['dur']) * FPS))
        seg_o = o[i0:max(i1, i0 + 1)]
        shots.append((x['name'], x['dur'], float(np.median(seg_o)) if len(seg_o) else 0.0))
        t0 += x['dur']
    wsum = sum(d for _, d, _ in shots)
    weighted = sum(abs(mo) * d for _, d, mo in shots) / max(1e-6, wsum)
    worst = max(shots, key=lambda x: abs(x[2]))
    med, sd = float(np.median(o)), float(o.std())
    over70 = int((np.abs(o) > 70).sum()); over110 = int((np.abs(o) > 110).sum())
    ok = weighted < 60 and abs(worst[2]) < 110
    if not ok: bad += 1
    out[sid] = dict(median=round(med, 1), sd=round(sd, 1), n=len(o), weighted_shot_offset=round(weighted, 1),
                    worst_shot=[worst[0], round(worst[2], 1)],
                    shots={n_: round(mo, 1) for n_, _, mo in shots},
                    frames_over70=over70, frames_over110=over110, none=n_none,
                    clip_left_px=round(float(np.median(clipL)), 0), clip_right_px=round(float(np.median(clipR)), 0), ok=ok)
    print(f"  {'OK ' if ok else '✗  '} {sid}: per-shot offsets " +
          ' '.join(f"{n_.split('-',1)[1]}:{mo:+.0f}" for n_, _, mo in shots) +
          f"  | weighted {weighted:.0f}px  worst {worst[2]:+.0f}px  | sway sd {sd:.0f}px, frames >70px {over70}/{len(o)}"
          f"  | edge-touch L {np.median(clipL):.0f} R {np.median(clipR):.0f}px of height")
json.dump(out, open(os.path.join(HERE, 'work', 'centregate.json'), 'w'), indent=1)
print('\nCENTRE GATE PASS' if bad == 0 else f'\nCENTRE GATE: {bad} short(s) off')
sys.exit(0 if bad == 0 else 1)
