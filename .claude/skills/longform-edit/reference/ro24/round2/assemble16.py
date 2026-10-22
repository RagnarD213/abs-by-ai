"""RO-24 picture assembly from keyed pieces: for every film frame, the keyed presenter (key16.py FFV1, 2880x1620) graded once
on the foreground, over the chosen background, cut to the shot's framing, plus the HyperFrames graphics (composite.py), to a
1920x1080 picture. Hard cuts only. Framings (2880 space, 16:9):
   W = the whole frame (Dan about a third of the width, waist up)
   T = 0.74 of the width, top edge 4 % of the crop height above the shot's highest hair, centred on the shot's median head x
Each shot's crop is fixed for the whole shot (horizontal footage stays static, Dan 2026-09-17).

  assemble16.py <edl.json> <out.mp4> [--bg depth] [--grade warm] [--hf hf/manifest.json] [--g0 N --g1 M] [--stills g,g,...]
edl.json: {"pieces": [{"id", "f0", "f1", "key", "shots": [{"f0": <source frame>, "framing": "W"|"T"}, ...]}, ...]}
Writes <out>.build.json: every segment (film frames, piece, source frames, framing, crop) for the gates and the edit sheet.
"""
import sys, os, json, argparse, subprocess
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comp16 as C
def keymeta(path):
    """key16 writes one info file per run (<base>.mkv.json); the refined variant shares it."""
    q = path + '.json'
    return json.load(open(q if os.path.exists(q) else path.replace('_refined.mkv', '.mkv') + '.json'))
FPS = 30000 / 1001; IW, IH = 2880, 1620; SHIFT = 519;   # S framing: +346 px at 1080p, measured clear of the 3A card on the widest gesture (graphics report)
 TW = int(round(IW * 0.74)) // 2 * 2; TH = int(round(TW * 9 / 16))

def shot_crops(piece):
    meta = keymeta(piece['key']); geo = {g[0]: g for g in meta['geo']}; kf0 = meta['f0']   # key frame k = source frame kf0 + k
    assert kf0 <= piece['f0'] and piece['f1'] <= kf0 + meta['frames'], (piece['id'], 'piece outside its key range')
    out = []
    for si, sh in enumerate(piece['shots']):
        a = sh['f0'] - kf0; b = (piece['shots'][si + 1]['f0'] if si + 1 < len(piece['shots']) else piece['f1']) - kf0
        if sh['framing'] in ('W', 'S'):          # S = wide with Dan shifted right for a left-third side card (fixed, never animated)
            crop = (0, 0, IW)
        else:
            g = [geo[k] for k in range(a, b) if k in geo and geo[k][1] >= 0]
            top = min(x[1] for x in g); cx = int(np.median([x[2] for x in g]))
            y0 = max(0, int(top - 0.04 * TH)); x0 = int(np.clip(cx - TW // 2, 0, IW - TW))
            crop = (x0, y0, TW)
        out.append(dict(k0=a, k1=b, framing=sh['framing'], crop=crop))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('edl'); ap.add_argument('out')
    ap.add_argument('--bg', default='depth'); ap.add_argument('--grade', default='warm'); ap.add_argument('--hf')
    ap.add_argument('--g0', type=int, default=0); ap.add_argument('--g1', type=int, default=None); ap.add_argument('--stills', default='')
    A = ap.parse_args()
    E = json.load(open(A.edl)); stills = {int(s) for s in A.stills.split(',') if s}
    comp = None
    if A.hf:
        sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes')
        import composite as HC
        comp = HC.Compositor(json.load(open(A.hf)))
    segs = []; g = 0
    for p in E['pieces']:
        for c in shot_crops(p):
            n = c['k1'] - c['k0']
            kf0 = keymeta(p['key'])['f0']
            segs.append(dict(o0=g, o1=g + n, piece=p['id'], src0=kf0 + c['k0'], src1=kf0 + c['k1'], framing=c['framing'], crop=c['crop'],
                             key=p['key'], k0=c['k0']))
            g += n
    N = g; g1 = A.g1 if A.g1 is not None else N
    wr = C.writer(A.out)
    readers = {}
    def frame_of(seg, k):
        key = seg['key']
        st = readers.get(key)
        if st is None or st['next'] > k:
            if st: st['p'].stdout.close(); st['p'].wait()
            p = subprocess.Popen([C.FF, '-v', 'error', '-i', key, '-an', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
            st = readers[key] = dict(p=p, next=0)
        while st['next'] < k:
            st['p'].stdout.read(IW * IH * 8); st['next'] += 1
        fr = C.read_frame(st['p']); st['next'] += 1
        assert fr is not None, (key, k)
        return fr
    bgimg = C.background(A.bg)
    for seg in segs:
        for o in range(max(seg['o0'], A.g0), min(seg['o1'], g1)):
            k = seg['k0'] + (o - seg['o0'])
            F, Al = frame_of(seg, k)
            if seg['framing'] == 'S':               # green screen: slide the keyed layer, the drawn background stays put
                F2 = np.zeros_like(F); A2 = np.zeros_like(Al); F2[:, SHIFT:] = F[:, :-SHIFT]; A2[:, SHIFT:] = Al[:, :-SHIFT]; F, Al = F2, A2
            img = C.compose(F, Al, None, A.grade, bgimg)
            x, y, w = seg['crop']; h = int(round(w * 9 / 16))
            img = cv2.resize(img[y:y + h, x:x + w], (1920, 1080), interpolation=cv2.INTER_AREA)
            o8 = (img * 255 + .5).astype(np.uint8)
            if comp is not None:
                o8 = comp.apply(o8, o)
            assert o8.shape == (1080, 1920, 3)
            wr.stdin.write(o8.tobytes())
            if o in stills:
                cv2.imwrite(A.out[:-4] + f'-{o:05d}.jpg', o8[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
    wr.stdin.close(); assert wr.wait() == 0
    for st in readers.values(): st['p'].stdout.close(); st['p'].wait()
    json.dump(dict(frames=N, g0=A.g0, g1=g1, bg=A.bg, grade=A.grade, segments=segs), open(A.out + '.build.json', 'w'), indent=1)
    print('ASSEMBLE DONE', A.out, g1 - A.g0)

if __name__ == '__main__':
    main()
