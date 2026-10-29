"""Per-clip midtone lift so each insert's window sits inside the approved DS-84 gym-cutaway range
(median luma 46-72, black share <16 at 7-22%), measured the same way the reviewer did (360-wide BT.709 decode of the window).
Curve keeps the black point (no gamma-only lift, no crushed blacks)."""
from pathlib import Path
import subprocess, json, numpy as np
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = str(R/'Media/video_edit/bin/ffmpeg')
V = json.load(open(W/'records/visual-plan.json')); L = json.load(open(W/'records/library.json'))
def curve(k): return f"curves=all='0/0 0.12/{0.12+0.55*k:.3f} 0.35/{0.35+0.45*k:.3f} 0.7/{0.7+0.18*k:.3f} 1/1',eq=saturation={1+0.25*k:.3f}"
def stats(u, vf):
    x, y, cw, ch = u['crop']; d = u['b']-u['a']; out = []
    for t in np.linspace(u['start']+0.2, u['start']+min(d, 6)-0.2, 6):
        raw = subprocess.check_output([F, '-v', 'error', '-ss', f'{t:.3f}', '-i', L[u['lib']]['path'], '-frames:v', '1', '-vf',
              f'crop={cw}:{ch}:{x}:{y},{vf+"," if vf else ""}scale=360:-2:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,format=gray', '-f', 'rawvideo', '-'])
        out.append(np.frombuffer(raw, np.uint8))
    a = np.concatenate(out).astype(float)*255/219-16*255/219  # tv->full approx
    return float(np.median(a)), float((a < 16).mean())
res = {}
for u in V['assets']:
    m0, b0 = stats(u, ''); pick = (0, m0, b0)
    for k in np.arange(0, 1.01, 0.1):
        m, b = stats(u, curve(k) if k else '')
        pick = (round(float(k), 2), m, b)
        if m >= 52 and b <= 0.20: break
    res[u['id']] = dict(before=dict(median=round(m0, 1), black=round(b0, 3)), k=pick[0], after=dict(median=round(pick[1], 1), black=round(pick[2], 3)), vf=curve(pick[0]) if pick[0] else '')
    print(u['id'], u['lib'], res[u['id']], flush=True)
(W/'records/broll-grade.json').write_text(json.dumps(dict(target='DS-84 R3 approved gym cutaways: median 46-72, black share 7-22%', clips=res), indent=2))
