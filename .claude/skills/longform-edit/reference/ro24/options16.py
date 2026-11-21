"""RO-24 round 1 look options on the SAME keyed frames: colour (warm = Bill Maher's approved grade, rich, natural) and background
(light = Bill Maher's flat field, depth, navy), each at the wide (W) and tight (T) framing, beside the approved Bill Maher sample
frame (same green screen, same lights) for comparison. Writes review stills + a measured table.

  options16.py <key.mkv> <frame> <outdir> [--tight x,y,w]
"""
import sys, os, json, subprocess, argparse
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comp16 as C
C.FF = C.FF + '.real'                     # a few frames, not a build
ap = argparse.ArgumentParser(); ap.add_argument('key'); ap.add_argument('frame', type=int); ap.add_argument('out'); ap.add_argument('--tight')
A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
p = subprocess.Popen([C.FF, '-v', 'error', '-i', A.key, '-frames:v', str(A.frame + 1), '-an', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
for i in range(A.frame): p.stdout.read(C.IW * C.IH * 8)
F, Al = C.read_frame(p); p.kill()
rows = np.where((Al > .35).sum(1) >= 3)[0]; top = int(rows[0]); band = Al[top:top + 260] > .5; cols = np.where(band.any(0))[0]; cx = int((cols[0] + cols[-1]) // 2)
TW = int(round(C.IW * 0.74)) // 2 * 2; TH = int(round(TW * 9 / 16))
tight = tuple(int(v) for v in A.tight.split(',')) if A.tight else (int(np.clip(cx - TW // 2, 0, C.IW - TW)), max(0, int(top - .04 * TH)), TW)
def out(img, crop, name):
    o = C.frame_out(img, crop if crop != (0, 0, C.IW) else None)
    cv2.imwrite(f'{A.out}/{name}.jpg', (np.clip(o, 0, 1)[:, :, ::-1] * 255 + .5).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 94])
    return o
def measure(o, a_full=None):
    y = .2126 * o[..., 0] + .7152 * o[..., 1] + .0722 * o[..., 2]
    mx, mn = o.max(-1), o.min(-1); sat = np.where(mx > 1e-3, (mx - mn) / np.maximum(mx, 1e-3), 0)
    return y, sat
res = {}
for mode in ['warm', 'rich', 'natural']:
    img = C.compose(F, Al, None, mode, C.background('depth'))
    for fr_name, crop in [('W', (0, 0, C.IW)), ('T', tight)]:
        o = out(img, crop, f'colour-{mode}-{fr_name}')
    # skin / face numbers on the foreground only (alpha > .99 inside the head band)
    g = C.grade(F, mode); y, sat = measure(g)
    face = (Al > .99); face[:top + 120] = False; face[top + 520:] = False
    torso = (Al > .99); torso[:top + 700] = False
    res[mode] = dict(face_luma=round(float(np.median(y[face])), 3), face_sat=round(float(np.median(sat[face])), 3),
                     arm_luma=round(float(np.median(y[torso & (sat > .2)])), 3) if (torso & (sat > .2)).any() else None)
for bg in ['light', 'depth', 'navy']:
    img = C.compose(F, Al, None, 'warm', C.background(bg))
    out(img, (0, 0, C.IW), f'bg-{bg}-W'); out(img, tight, f'bg-{bg}-T')
# the approved Bill Maher sample frame for comparison (portrait 1080x1920 -> letterboxed tile)
ref = '/Volumes/Extreme/_edit_work/DS-40-codex/round3/review/media/sample.mp4'
raw = subprocess.check_output([C.FF, '-v', 'error', '-ss', '5', '-i', ref, '-frames:v', '1', '-vf', 'scale=in_color_matrix=bt709:in_range=tv,scale=1080:1920,format=rgb24', '-f', 'rawvideo', '-'])
R = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3)
cv2.imwrite(f'{A.out}/ref-billmaher.jpg', R[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 94])
Rf = R.astype(np.float32) / 255; ry, rs = measure(Rf)
# Bill Maher face region: skin-ish pixels in the upper middle
sk = (Rf[..., 0] > Rf[..., 2] + .08) & (ry > .25); sk[:250] = False; sk[900:] = False
res['billmaher_reference'] = dict(face_luma=round(float(np.median(ry[sk])), 3), face_sat=round(float(np.median(rs[sk])), 3))
json.dump(dict(frame=A.frame, top=top, cx=cx, tight=tight, numbers=res), open(f'{A.out}/options.json', 'w'), indent=1)
print(json.dumps(res, indent=1)); print('tight', tight)
