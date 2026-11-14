"""SL-21 round 2, second version of the mouth merge (after the B1 review: the synced lower face was 95 % softer than the take's
stubble, lips doubled on the fades, the mouth snapped open in one frame).

Per frame, with face mesh on BOTH the synced frame and the take frame:
  * LIPS (hull of the synced lips and the take's lips, grown): the synced pixels, lightly sharpened. This is the only place the
    soft model output is shown as is.
  * LOWER FACE around them (jaw, chin, cheeks): the SHAPE of the sync (its low frequencies) with the TEXTURE of the take (its high
    frequencies), so the jaw moves with the words and the stubble and skin stay as crisp as the rest of the face.
  * Everything else: the take, untouched.
The synced mouth is switched in and out at the frame where its lips are closest to closed (searched within +-SEARCH frames of the
first and last word), over a 2-frame ramp, so the fade never shows an open and a closed mouth at once.
usage: syncfix22.py TAKE_TRIM.mp4 SYNC.mp4 OUT.mp4 --fps 25 --on-from T --on-to T [--sigma 5] [--search 5]"""
import subprocess, sys, json, numpy as np, cv2
import mediapipe as mp
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
a = sys.argv[1:]; take, sync, out = a[:3]
opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
FPSV = opt("--fps", 25.0); T_ON, T_OFF = opt("--on-from", 0.0), opt("--on-to", 1e9); SIG = opt("--sigma", 5.0); SEARCH = int(opt("--search", 5))
W, H = 1080, 1920
OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234,
        127, 162, 21, 54, 103, 67, 109]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]


def frames(p):
    raw = subprocess.run([FF, "-v", "error", "-i", p, "-vf", f"scale={W}:{H}:flags=bicubic:in_color_matrix=bt709:out_color_matrix=bt709,format=rgb24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def mesh(F):
    out = []
    with mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.4) as FM:
        for f in F:
            r = FM.process(np.ascontiguousarray(f))
            out.append(np.array([[l.x * W, l.y * H] for l in r.multi_face_landmarks[0].landmark], np.float32) if r.multi_face_landmarks else None)
    for i in range(len(out)):                     # a missed frame takes its neighbour's landmarks
        if out[i] is None: out[i] = next((out[j] for j in list(range(i - 1, -1, -1)) + list(range(i + 1, len(out))) if out[j] is not None), None)
    return out


T, S = frames(take), frames(sync); n = min(len(T), len(S)); LT, LS = mesh(T[:n]), mesh(S[:n])
gap = np.array([abs(LS[i][14, 1] - LS[i][13, 1]) / max(1.0, abs(LS[i][291, 0] - LS[i][61, 0])) for i in range(n)])
f_on = int(round(T_ON * FPSV)); f_off = min(n - 1, int(round(T_OFF * FPSV)))
# D1 review (round 2): LatentSync GAPES in the silence before the first word (a flat black mouth for a quarter second) and a
# half-blended frame at each switch shows a grey lip slab. So: the take's own closed mouth right up to the voice; the sync switches
# in on the frame, from the voice onset to SEARCH frames after it, where its lips are closest to closed (the gape has passed by
# then), and out likewise after the last word; a hard switch, never a blended frame.
c0 = range(f_on, min(n, f_on + SEARCH)); c1 = range(max(0, f_off), min(n, f_off + SEARCH + 1))
f_off = min(c1, key=lambda i: gap[i])
if "--on-exact" not in a: f_on = min(c0, key=lambda i: gap[i])      # --on-exact: switch in exactly at --on-from (one frame before the voice when the first word opens on a vowel: the open mouth ON the word is right, only the gape before it was wrong)
gate = np.zeros(n, np.float32); gate[f_on:f_off + 1] = 1.0
blur = lambda x: cv2.GaussianBlur(x, (0, 0), SIG)
EASE = [float(v) for v in a[a.index("--ease") + 1].split(",")] if "--ease" in a else []
UP = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]; LO = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]


def part_close(img, lm, k):
    """The synced frame with its mouth opened only k of the way (D2 review, round 2: on a face that fills the frame the mouth popped
    from shut to its widest in ONE frame on the first word). The inner lips move toward each other: the dark interior is squeezed to
    k of its height and the lips, chin and upper lip slide in by the rest, fading to nothing a quarter face-width away."""
    fw = abs(lm[454, 0] - lm[234, 0]); R = 0.25 * fw
    xs = np.arange(W, dtype=np.float32)
    def curve(idx):
        pts = lm[idx]; o = np.argsort(pts[:, 0]); return np.interp(xs, pts[o, 0], pts[o, 1]).astype(np.float32)
    yu, yl = curve(UP), curve(LO); x0, x1 = lm[78, 0], lm[308, 0]
    aa = np.clip((yl - yu) / 2, 0, None); aa[(xs < x0) | (xs > x1)] = 0
    edge = np.clip(np.minimum(xs - x0, x1 - xs) / max(1.0, 0.08 * (x1 - x0)), 0, 1); aa = aa * edge      # the opening tapers to the corners
    yc = (yl + yu) / 2
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32); d = Y - yc[None, :]; A = aa[None, :]; ad = np.abs(d)
    inside = ad <= k * A
    wgt = np.clip(1 - (ad - k * A) / R, 0, 1)
    src_d = np.where(inside, d / max(k, 1e-3), d + np.sign(d) * A * (1 - k) * wgt)
    return cv2.remap(img, X, (yc[None, :] + src_d).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{FPSV:g}", "-i", "-",
                        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an", out], stdin=subprocess.PIPE)
d_out = []; sharp = []
yy, xx = np.mgrid[0:H, 0:W]
for i in range(n):
    if gate[i] == 0:
        enc.stdin.write(T[i].tobytes()); continue
    if 0 <= i - f_on < len(EASE): S_i = part_close(S[i], LS[i], EASE[i - f_on])
    else: S_i = S[i]
    t, s = T[i].astype(np.float32), S_i.astype(np.float32)
    ls, lt = LS[i], LT[i]; fw = abs(ls[454, 0] - ls[234, 0])                              # face width: every size below scales with it
    # lower face (below a line under the eyes that follows the head's tilt)
    m = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(m, cv2.convexHull(ls[OVAL]).astype(np.int32), 255)
    eye_y = (ls[33, 1] + ls[263, 1]) / 2; cut = 0.45 * (ls[1, 1] - eye_y)
    line = ls[33, 1] + (ls[263, 1] - ls[33, 1]) * (xx - ls[33, 0]) / max(1e-3, ls[263, 0] - ls[33, 0]) + cut
    m[yy < line] = 0
    g = max(3, int(fw * 0.03)); m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * g + 1, 2 * g + 1)))
    m_low = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), max(4.0, fw * 0.025))[..., None] * gate[i]
    # lips: the synced lips and the take's own lips together, grown
    ml = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(ml, cv2.convexHull(np.vstack([ls[LIPS], lt[LIPS]])).astype(np.int32), 255)
    g2 = max(4, int(fw * 0.035)); ml = cv2.dilate(ml, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * g2 + 1, 2 * g2 + 1)))
    m_lip = cv2.GaussianBlur(ml.astype(np.float32) / 255, (0, 0), max(3.0, fw * 0.018))[..., None] * gate[i]
    shape = blur(s) + (t - blur(t))                                                       # the sync's shape, the take's texture
    s_sharp = np.clip(s + 0.9 * (s - cv2.GaussianBlur(s, (0, 0), 1.6)), 0, 255)           # unsharp mask on the synced lips
    o = t * (1 - m_low) + shape * m_low
    o = o * (1 - m_lip) + s_sharp * m_lip
    o = np.clip(o + 0.5, 0, 255).astype(np.uint8)
    d_out.append(float(np.abs(o.astype(np.int16) - T[i].astype(np.int16))[m_low[..., 0] < 0.004].mean()))
    x0, y0 = int(ls[152, 0] - fw * 0.18), int(ls[152, 1] - fw * 0.16); x1, y1 = int(ls[152, 0] + fw * 0.18), int(ls[152, 1] - fw * 0.02)      # a chin patch under the lips
    lap = lambda im: float(cv2.Laplacian(cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY), cv2.CV_32F).var()) if y1 > y0 and x1 > x0 else 0.0
    sharp.append((lap(o), lap(T[i]), lap(S[i])))
    enc.stdin.write(o.tobytes())
enc.stdin.close(); enc.wait()
sh = np.array(sharp)
print(json.dumps(dict(out=out, frames=n, on=[int(f_on), round(f_on / FPSV, 2)], off=[int(f_off), round(f_off / FPSV, 2)], gap_at_on=round(float(gap[f_on]), 2),
                      gap_at_off=round(float(gap[f_off]), 2), mean_abs_outside=round(float(np.mean(d_out)), 3),
                      chin_sharpness_out_take_sync=[round(float(v)) for v in sh.mean(0)])))
