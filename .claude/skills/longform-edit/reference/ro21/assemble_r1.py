"""RO-21 round 1 picture (from RO-24 round 4's assemble_r4.py, the locked green-screen background template): Dan from the
house-key plates (key/K*.mkv) placed and composed at 1080p on the background plan (round1/bg_plan.json), then every graphic,
picture scene and B-roll insert (HyperFrames compositor manifest, round1/film_manifest.json). Frames under a full-screen
item skip the plate decode. Behind-Dan backgrounds that show an AI picture get the AI-GENERATED chip (bottom left).

  assemble_r1.py OUT.mp4 [--g0 N --g1 M] [--stills 30,800] [--grade warm|rich|natural]
Writes OUT.mp4.build.json (runs, hair clearance per presenter frame)."""
import argparse, json, os, pathlib, subprocess, sys, time
import numpy as np, cv2
from PIL import Image
B = pathlib.Path('/Volumes/Expansion/_edit_work/RO-21'); R1 = B / 'round1'; KEY = B / 'key'
GSBG = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg'
sys.path.insert(0, GSBG); import gsbg as G
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes'); import composite as HC
FPS = G.FPS
SET = dict(plate='/Volumes/Expansion/_edit_work/RO-24/round3/mock/set_plate.png', tv=(581, 111, 512, 285))   # RO-24's Codex set plate, reused
AI_BG = {'cards', 'wall', 'soft', 'panel'}                 # these show an AI picture of Dan behind him (set draws its own chip)
fr = lambda t: int(round(t * FPS))


def items():
    """Film-frame items: one per shot. Covered shots are 'insert' (the manifest draws them); presenter shots point at the key
    range holding their source frames."""
    E = json.load(open(R1 / 'edl_r1.json')); S = json.load(open(R1 / 'shots.json')); K = json.load(open(R1 / 'key_ranges.json'))
    out = []
    for s in S:
        o0, o1 = fr(s['t0']), fr(s['t1'])
        if o1 <= o0: continue
        if s['covered']: out.append(dict(kind='insert', clip='covered', o0=o0, o1=o1)); continue
        e = next(e for e in E if fr(e['film_in']) <= o0 < fr(e['film_out']))
        assert o1 <= fr(e['film_out']) + 1, ('shot crosses an EDL join', s)
        src0 = e['f_in'] + (o0 - fr(e['film_in'])); n = o1 - o0
        k = next((k for k in K if k['f0'] <= src0 and src0 + n <= k['f0'] + k['n']), None)
        assert k, ('no key range holds', s, src0, n)
        out.append(dict(kind='shot', piece=f"E{e['k']:02d}", key=str(KEY / f"{k['name']}.mkv"), src0=src0, n=n, framing=s['framing'], o0=o0, o1=o1))
    return out


def chip_layer(xy):
    """top left like the set's own chip (clear of the lower-third band, where a bottom chip crowded the captions in the R1
    first-minute check); on a panel, inside the first photo's plain backdrop above the head"""
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); G.SB.disclosure(im, 'AI-GENERATED', xy=xy)
    a = np.asarray(im, np.float32) * (1 / 255); return a[..., :3], a[..., 3:4]


def writer(path):
    return subprocess.Popen([G.FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30000/1001', '-i', '-',
                             '-an', '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p', '-c:v', 'libx264',
                             '-crf', '14', '-preset', 'medium', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                             '-movflags', '+faststart', path], stdin=subprocess.PIPE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--g0', type=int, default=0); ap.add_argument('--g1', type=int)
    ap.add_argument('--stills', default=''); ap.add_argument('--plan', default=str(R1 / 'bg_plan.json'))
    ap.add_argument('--manifest', default=str(R1 / 'film_manifest.json')); ap.add_argument('--grade', default='warm')
    A = ap.parse_args()
    E = items(); plan = json.load(open(A.plan))['segments']
    C = HC.Compositor(json.load(open(A.manifest)))
    ctx = G.Context(R1, set_plate=SET['plate'], set_tv=SET['tv'])
    N = E[-1]['o1']; g0 = A.g0; g1 = min(N, A.g1 if A.g1 is not None else N)
    stills = {int(s) for s in A.stills.split(',') if s}
    segf = [dict(s, f0=fr(s['t0']), f1=fr(s['t1'])) for s in plan]
    chips = {'panel': chip_layer((96, 84)), 'other': chip_layer((56, 48))}
    seg_at = lambda o: next((s for s in segf if s['f0'] <= o < s['f1']), None)
    wr = writer(A.out); runs = []; bgs = {}; t_start = time.time(); done = 0; hair = []
    def emit(f, q):
        nonlocal done
        wr.stdin.write(np.ascontiguousarray(f).tobytes()); done += 1
        if q in stills: cv2.imwrite(A.out[:-4] + f'-{q:05d}.jpg', f[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
    for it in E:
        lo, hi = max(it['o0'], g0), min(it['o1'], g1)
        if lo >= hi: continue
        if it['kind'] == 'insert':
            for o in range(lo, hi):
                assert C.opaque(o), f'covered frame {o} has no opaque manifest item'
                emit(C.apply(None, o), o)
            runs.append(dict(o0=lo, o1=hi, kind='insert')); continue
        meta = json.load(open(it['key'] + '.json')); kf0 = meta['f0']; geo = {g[0]: g for g in meta['geo']}
        k_item0 = it['src0'] - kf0 + (lo - it['o0'])
        top, cx = G.shot_head(geo, it['src0'] - kf0, it['src0'] - kf0 + it['n'])
        o = lo
        while o < hi:
            covered = C.opaque(o); seg = None if covered else seg_at(o)
            e = o + 1
            while e < hi and C.opaque(e) == covered and (covered or seg_at(e) is seg): e += 1
            if covered:
                for q in range(o, e): emit(C.apply(None, q), q)
                runs.append(dict(o0=o, o1=e, kind='covered', piece=it['piece'])); o = e; continue
            assert seg is not None, f'film frame {o} has Dan on screen but no background segment'
            bg = bgs.get(seg['id'])
            if bg is None:
                for k in [k for k in bgs if k != seg['id']]: bgs.pop(k).close()
                bg = bgs[seg['id']] = G.make_background(dict(seg, frames=seg['f1'] - seg['f0']), ctx); bg._next = seg['f0']
            framing = 'W' if it['framing'] in ('W', 'S') else 'T'
            mode = bg.placement
            k, ox, oy = G.affine(mode, framing, top, cx)
            cam = G.camera(mode, framing, top, cx) if seg['type'] in G.CAMERA_LOCKED else (1.0, 0.0, 0.0)
            pr = G.Presenter(it['key'], it['src0'] - kf0 + (o - it['o0']), e - o, k, ox, oy)
            light = getattr(bg, 'light', None)
            ai = seg['type'] in AI_BG and seg.get('ai_label', True) and (seg['type'] != 'soft' or any('ai_images' in x for x in seg.get('photos', [])))
            for q in range(o, e):
                while bg._next < q: bg.frame(bg._next - seg['f0'], cam); bg._next += 1
                img = bg.frame(q - seg['f0'], cam).copy(); bg._next = q + 1
                if ai:
                    chip = chips['panel' if seg['type'] == 'panel' else 'other']; img = img * (1 - chip[1]) + chip[0] * chip[1]
                top_bg = img[:420].copy()
                F, Al = pr.read()
                img = G.compose(img, F, Al, pr.rect, k, A.grade, light)
                dd = (np.abs(img[:420] - top_bg).max(-1) > 14 / 255).sum(1) >= 3
                hair.append((q, int(np.argmax(dd)) if dd.any() else None, framing, mode))
                o8 = C.apply((img * 255 + .5).astype(np.uint8), q)
                emit(o8, q)
            pr.close()
            runs.append(dict(o0=o, o1=e, kind='presenter', piece=it['piece'], key=it['key'], src0=it['src0'] + (o - it['o0']),
                             framing=framing, placement=mode, bg=seg['id'], bg_type=seg['type'], ai_chip=bool(ai), affine=[k, ox, oy],
                             rect=pr.rect, head=[top, cx]))
            if done % 300 < (e - o): print(f'  {done} frames, {done / (time.time() - t_start):.2f} fps', flush=True)
            o = e
    for b_ in bgs.values(): b_.close()
    wr.stdin.close(); assert wr.wait() == 0
    json.dump(dict(frames=N, g0=g0, g1=g1, grade=A.grade, runs=runs, hair=hair), open(A.out + '.build.json', 'w'), indent=1)
    print('ASSEMBLE DONE', A.out, g1 - g0, 'frames', f'{(g1 - g0) / (time.time() - t_start):.2f} fps', flush=True)


if __name__ == '__main__':
    main()
