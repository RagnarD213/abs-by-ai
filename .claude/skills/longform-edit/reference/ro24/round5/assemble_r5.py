"""RO-24 round 5 picture (round 4's assembler with the round 5 EDL, plan and manifest; media paths still resolve against round 4).
Round 4's note: RO-24 round 4 picture (round 3's assembler, whole film, round 4 plan and manifest): round 2's locked cut with the six clip inserts (edl_r3.json), Dan from the round 2 plates (no
re-key) placed and composed at 1080p on the shared green-screen background template (bg_plan.json,
.claude/skills/_shared/greenscreen-bg), then every graphic (HyperFrames compositor). Frames under a full-screen item
(a clip insert, a photo scene, a card, B-roll) skip the plate decode: the compositor replaces them.

  assemble_r3.py OUT.mp4 [--g0 N --g1 M] [--stills 30,800] [--plan bg_plan.json] [--manifest film_manifest_r3.json]
Writes OUT.mp4.build.json: every run (film frames, item, source frames, framing, placement, background segment, screen
rect) for the gates and the edit sheet.
"""
import argparse, json, os, pathlib, subprocess, sys, time
import numpy as np, cv2
R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round3'); R4 = R3.parent / 'round4'; R5 = R3.parent / 'round5'
GSBG = os.environ.get('GSBG', '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg')
sys.path.insert(0, GSBG); import gsbg as G
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes'); import composite as HC
FPS = G.FPS
SET = dict(plate=str(R3 / 'mock/set_plate.png'), tv=(581, 111, 512, 285))   # Codex set plate; TV screen measured (largest near-black rect)


def keymeta(path):
    q = path + '.json'
    return json.load(open(q if os.path.exists(q) else path.replace('_refined.mkv', '.mkv') + '.json'))


def writer(path):
    return subprocess.Popen([G.FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30000/1001', '-i', '-',
                             '-an', '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p', '-c:v', 'libx264',
                             '-crf', '14', '-preset', 'medium', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                             '-movflags', '+faststart', path], stdin=subprocess.PIPE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--g0', type=int, default=0); ap.add_argument('--g1', type=int)
    ap.add_argument('--stills', default=''); ap.add_argument('--plan', default=str(R5 / 'bg_plan.json'))
    ap.add_argument('--manifest', default=str(R5 / 'film_manifest_r5.json')); ap.add_argument('--grade', default='warm')
    ap.add_argument('--reuse', help='an earlier render of the same range: frames outside --redo segments are copied from it. '
                    'TRAP (RO-24 R4, measured): each reuse generation darkens every copied frame by about 1.65 luma levels '
                    '(decode/encode round trip); use it for previews only and make the delivered file a full render')
    ap.add_argument('--redo', default='', help='background segment ids to compose again (with --reuse)')
    A = ap.parse_args()
    E = json.load(open(R5 / 'edl_r5.json'))['items']; plan = json.load(open(A.plan))['segments']
    C = HC.Compositor(json.load(open(A.manifest)))
    ctx = G.Context(R4, set_plate=SET['plate'], set_tv=SET['tv'])
    N = E[-1]['o1']; g0 = A.g0; g1 = min(N, A.g1 if A.g1 is not None else N)
    stills = {int(s) for s in A.stills.split(',') if s}
    segf = [dict(s, f0=int(round(s['t0'] * FPS)), f1=int(round(s['t1'] * FPS))) for s in plan]

    redo = {x for x in A.redo.split(',') if x}
    old = None
    if A.reuse:
        oldb = json.load(open(A.reuse + '.build.json')); assert oldb['g0'] == g0 and oldb['g1'] == g1, 'reuse needs the same range'
        old_hair = {h[0]: h for h in oldb['hair']}
        rd = subprocess.Popen([G.FF, '-v', 'error', '-i', A.reuse, '-an', '-vf', 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24',
                               '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
        old = dict(p=rd, next=g0)

    def old_frame(q):                                     # the earlier render's frame q (sequential)
        while True:
            raw = old['p'].stdout.read(1920 * 1080 * 3); assert len(raw) == 1920 * 1080 * 3, 'reuse render too short'
            n = old['next']; old['next'] += 1
            if n == q: return np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3)

    def seg_at(o):
        return next((s for s in segf if s['f0'] <= o < s['f1']), None)

    wr = writer(A.out); runs = []; bgs = {}; t_start = time.time(); done = 0; hair = []
    for it in E:
        lo, hi = max(it['o0'], g0), min(it['o1'], g1)
        if lo >= hi: continue
        if it['kind'] == 'insert':                         # the clip is an opaque manifest item: the compositor draws it
            for o in range(lo, hi):
                assert C.opaque(o), f'clip insert {it["clip"]} frame {o} has no opaque manifest item'
                f = old_frame(o) if old is not None else C.apply(None, o); wr.stdin.write(np.ascontiguousarray(f).tobytes()); done += 1
                if o in stills: cv2.imwrite(A.out[:-4] + f'-{o:05d}.jpg', f[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
            runs.append(dict(o0=lo, o1=hi, kind='insert', clip=it['clip']))
            continue
        meta = keymeta(it['key']); kf0 = meta['f0']; geo = {g[0]: g for g in meta['geo']}
        k_item0 = it['src0'] - kf0                          # plate frame of the item's first film frame
        sk0, sk1 = k_item0, k_item0 + it['n']
        top, cx = G.shot_head(geo, sk0, sk1)                # head over the WHOLE shot piece (static framing per shot)
        o = lo; anchor = None; after_cover = False         # anchor: plate frame of this item's last presenter run start
        while o < hi:
            covered = C.opaque(o); seg = None if covered else seg_at(o)
            # run: same coverage and same background segment
            e = o + 1
            while e < hi and C.opaque(e) == covered and (covered or seg_at(e) is seg): e += 1
            if covered:
                for q in range(o, e):
                    f = old_frame(q) if old is not None else C.apply(None, q); wr.stdin.write(np.ascontiguousarray(f).tobytes()); done += 1
                    if q in stills: cv2.imwrite(A.out[:-4] + f'-{q:05d}.jpg', f[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
                runs.append(dict(o0=o, o1=e, kind='covered', piece=it['piece'])); after_cover = True
                o = e; continue
            assert seg is not None, f'film frame {o} has Dan on screen but no background segment'
            if old is not None and seg['id'] not in redo:
                for q in range(o, e):
                    f = old_frame(q); wr.stdin.write(np.ascontiguousarray(f).tobytes()); done += 1
                    if q in old_hair: hair.append(old_hair[q])
                    if q in stills: cv2.imwrite(A.out[:-4] + f'-{q:05d}.jpg', f[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
                runs.append(dict(o0=o, o1=e, kind='presenter-reused', piece=it['piece'], bg=seg['id'])); o = e; continue
            bg = bgs.get(seg['id'])
            if bg is None:
                for k in [k for k in bgs if k != seg['id']]: bgs.pop(k).close()
                bg = bgs[seg['id']] = G.make_background(dict(seg, frames=seg['f1'] - seg['f0']), ctx)
                bg._next = seg['f0']
            framing = 'W' if it['framing'] in ('W', 'S') else 'T'
            mode = bg.placement
            k, ox, oy = G.affine(mode, framing, top, cx)
            cam = G.camera(mode, framing, top, cx) if seg['type'] in G.CAMERA_LOCKED else (1.0, 0.0, 0.0)
            kq = k_item0 + (o - it['o0'])
            # after an insert inside the same piece, read on from the last run's start instead of seeking to the new frame:
            # round 5's A8 split showed a fresh seek there landing one frame from round 4's continuous read (ROUND-5-REVIEW S2)
            skip = kq - anchor if (after_cover and anchor is not None) else 0
            pr = G.Presenter(it['key'], kq - skip, e - o + skip, k, ox, oy)
            for _ in range(skip): pr.read()
            if not skip: anchor = kq
            after_cover = False
            light = getattr(bg, 'light', None)
            for q in range(o, e):
                while bg._next < q:                         # keep the background's clock on film time (a render that starts mid-segment)
                    bg.frame(bg._next - seg['f0'], cam); bg._next += 1
                if old is not None: old_frame(q)          # keep the earlier render's reader in step
                img = bg.frame(q - seg['f0'], cam).copy(); bg._next = q + 1
                top_bg = img[:420].copy()
                F, Al = pr.read()
                img = G.compose(img, F, Al, pr.rect, k, A.grade, light)
                # hair clearance, measured on the rendered picture before graphics: first row from the top where at least
                # 3 pixels differ from the background drawn under him by more than 14/255 (the round 2 hairclear16 rule)
                dd = (np.abs(img[:420] - top_bg).max(-1) > 14 / 255).sum(1) >= 3
                hair.append((q, int(np.argmax(dd)) if dd.any() else None, framing, mode))
                o8 = (img * 255 + .5).astype(np.uint8)
                o8 = C.apply(o8, q)
                wr.stdin.write(np.ascontiguousarray(o8).tobytes()); done += 1
                if q in stills: cv2.imwrite(A.out[:-4] + f'-{q:05d}.jpg', o8[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
            pr.close()
            runs.append(dict(o0=o, o1=e, kind='presenter', piece=it['piece'], key=it['key'], src0=it['src0'] + (o - it['o0']),
                             framing=framing, placement=mode, bg=seg['id'], bg_type=seg['type'], affine=[k, ox, oy], rect=pr.rect,
                             crop=pr.crop, head=[top, cx]))
            if done and done % 300 < (e - o):
                print(f'  {done} frames, {done / (time.time() - t_start):.2f} fps', flush=True)
            o = e
    for b in bgs.values(): b.close()
    if old is not None: old['p'].stdout.close(); old['p'].wait()
    wr.stdin.close(); assert wr.wait() == 0
    json.dump(dict(frames=N, g0=g0, g1=g1, grade=A.grade, plan=A.plan, manifest=A.manifest, runs=runs, hair=hair), open(A.out + '.build.json', 'w'), indent=1)
    print('ASSEMBLE DONE', A.out, g1 - g0, 'frames', f'{(g1 - g0) / (time.time() - t_start):.2f} fps', flush=True)


if __name__ == '__main__':
    main()
