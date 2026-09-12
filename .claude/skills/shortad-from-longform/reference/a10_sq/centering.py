#!/usr/bin/env python3
"""Measure the presenter's horizontal placement ON THE DELIVERED FILE.

⚠ THIS IS THE CHECK THAT WAS MISSING, AND ITS ABSENCE COST TWO REJECTED VERSIONS.
Everything upstream was verified -- the track was measured with Apple Vision, the A/B
against the old crop looked right, the beat sheet was correct -- and the delivered picture
was still wrong, because the ffmpeg crop EXPRESSION built its nested ifs in the wrong
order and evaluated the last 2 s interval, extrapolated, for the whole beat. Nothing that
inspects the plan can see that. Only measuring the finished frames can.
"""
import glob, json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, '.'); sys.path.insert(0, 'rc')
from anchor import anchors
import beats as BT

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
V = sys.argv[1] if len(sys.argv) > 1 else 'ad2_square_1x1.mp4'
D = 'centering'
FPS_S = 2

def measure(rebuild=True):
    if rebuild or not os.path.isdir(f'{D}/m'):
        subprocess.run(['rm','-rf',D], check=False)
        os.makedirs(f'{D}/fr', exist_ok=True)
        subprocess.run([FF,'-nostdin','-v','error','-y','-i',V,'-vf',
                        f'fps={FPS_S},scale=270:270', f'{D}/fr/%05d.png'], check=True)
        fs = sorted(glob.glob(f'{D}/fr/*.png'))
        for i in range(0, len(fs), 60):
            subprocess.run(['./rc/personmask', f'{D}/m'] + fs[i:i+60],
                           check=True, capture_output=True)
    tl, _ = BT.timeline()
    def kind_at(t):
        for b in tl:
            if b['t0'] <= t < b['t1']: return b['kind']
        return 'talk'
    rows = []
    for f in sorted(glob.glob(f'{D}/m/*.mask.png')):
        i = int(os.path.basename(f).split('.')[0]) - 1
        t = i / FPS_S
        m = np.asarray(Image.open(f).convert('L'), dtype=np.float32)/255.0 > 0.5
        if m.mean() < 0.20: continue          # not a talking-head frame
        a = anchors(m)
        if a is None: continue
        rows.append((t, kind_at(t), (a['torso']-0.5)*1080, (a['head']-0.5)*1080))
    return rows

if __name__ == '__main__':
    rows = measure(rebuild='--reuse' not in sys.argv)
    talk = np.array([[r[0], r[2], r[3]] for r in rows if r[1] == 'talk'])
    v = talk[:, 1]
    stats = dict(n=len(talk), median=float(np.median(v)), mean=float(v.mean()),
                 sd=float(v.std()), p90=float(np.percentile(np.abs(v), 90)),
                 over40=int((np.abs(v) > 40).sum()), over70=int((np.abs(v) > 70).sum()),
                 over100=int((np.abs(v) > 100).sum()), over150=int((np.abs(v) > 150).sum()))
    # contiguous runs beyond 60 px for >= 1 s
    runs, cur = [], []
    for t, x, _ in talk:
        if abs(x) > 60: cur.append((t, x))
        else:
            if len(cur) >= 2*FPS_S: runs.append((cur[0][0], cur[-1][0], float(np.mean([c[1] for c in cur]))))
            cur = []
    if len(cur) >= 2*FPS_S: runs.append((cur[0][0], cur[-1][0], float(np.mean([c[1] for c in cur]))))
    stats['runs'] = [dict(t0=round(a,1), t1=round(b,1), mean=round(m)) for a, b, m in runs]
    json.dump(stats, open('logs/centering.json','w'), indent=1)
    print(f"talk frames {stats['n']}   median {stats['median']:+.0f}   mean {stats['mean']:+.0f}   sd {stats['sd']:.0f}")
    print(f"  >40px {stats['over40']}  >70px {stats['over70']}  >100px {stats['over100']}  "
          f">150px {stats['over150']}   p90 |x| {stats['p90']:.0f}")
    print(f"  runs beyond 60px for >=1s: {len(runs)}")
    for r in stats['runs']: print(f"     {r['t0']:7.1f}-{r['t1']:7.1f}  mean {r['mean']:+.0f}")
