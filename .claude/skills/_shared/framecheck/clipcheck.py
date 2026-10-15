#!/usr/bin/env python3
"""The motion-take gate: track points through an AI take with CoTracker3, flag what vanishes or appears from nowhere, check
the spec's moving and still parts on every frame, stamp the result, refuse unchecked takes.

usage:
  clipcheck.py TAKE.mp4 --spec spec.json [--frames A:B] [--out DIR]   measure, write evidence + stamp (exit 0 PASS, 1 FAIL)
  clipcheck.py TAKE.mp4 [--frames A:B] --review review.md             record the frame-reviewer's verdict in the stamp
  clipcheck.py TAKE.mp4 [--frames A:B] --verify                       exit 0 only if the gate PASSed at this version AND a
                                                                      reviewer PASSed, for exactly this file, range and spec
Callers: `from clipcheck import require_pass; require_pass(TAKE, frames=(A, B))`.

The spec is the frame pair's spec (gate.py, README "The frame spec"): every box is in the pixels of the take's first checked
frame (frame 0 is the START frame). `--frames A:B` checks only the part of a take an edit uses (both ends included).

What it measures (each row PASS/FAIL with numbers):
  vanish    a grid of points seeded on the first frame (not on people, not in may_change boxes), tracked forward. A point
            VANISHES when it is lost for good (never visible again, at least min_gone_s before the end) while it had not
            moved against its neighbours, inside the picture, no person and no moving thing covers its spot at the end,
            and the spot looks different at the end (patch correlation). Clusters of min_event_pts such points are events.
            RO-08 A5's donuts that fade out of their box.
  appear    the same, seeded on the last frame and tracked backward: something that is there at the end and came from
            nowhere (it was not carried in, it was not uncovered by something moving away).
  camera    the camera's move (similarity fitted to the background points); a FAIL only if the spec says "camera": "locked"
  rigid.*   each rigid group tracked on every sampled frame: parts together, travel along the guide, distance at the end
  contact.* riders (a shoe on a footplate) stay on their group on every frame
  still.*   still boxes do not move against the camera on any frame
  prop.*    a held prop is not lost for good outside the hand (a prop may leave with "may_leave": true, e.g. food eaten)
Evidence: TAKE.clipcheck.jpg next to the take (first|last frame with events, a strip of crops per event across its frames)
and a folder of sampled frames every 0.25 s for the frame-reviewer.

Built 2026-10-14 on RO-08's rejected donut take. Proven: README, "Motion takes".
"""
import argparse, hashlib, json, math, os, re, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gate import sha256, Rows, line_deg, dang, ang  # noqa: E402

CLIP_VERSION = "1.0.0"   # bump on ANY change to a check or a default bound; older stamps stop verifying
STAMP_SUFFIX = ".clipcheck.json"
BIN = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
FF, FP = os.path.join(BIN, "ffmpeg"), os.path.join(BIN, "ffprobe")
SMALL_W = 512             # the tracker works at 384x512; frames go in at this width
HALF_W = 960              # the vanish test compares patches and finds people at this width

DEFAULTS = dict(grid_px=40,             # grid spacing at 1080p (scaled with the take's height): 48 x 27 points
                max_frames=64,          # memory (cotracker_mps.py): longer takes are sampled, a 6 s take every 3rd frame (8 per s)
                place_frac=0.025,       # "had not moved": within this fraction of the height against its neighbours (27 px at 1080p)
                min_gone_s=0.4,         # lost for at least this long before the end
                ncc_same=0.5,           # patch correlation at or above this = the spot looks the same (the tracker lost it, nothing changed)
                flat_std=4.0,           # a patch with less grey-level spread than this is flat; two flat patches compare by mean
                flat_mean_diff=25.0,
                min_event_pts=6,        # points in one cluster to call it an event (RO-08: shipped takes at most 3, the donuts 50)
                person_pad_frac=0.03,   # person masks grown by this fraction of the height
                still_px=5.0,           # still boxes: tracker noise over a take is 1 to 3 px
                contact_slip_px=12.0,
                rigid_disagree_px=10.0, rigid_disagree_frac=0.12, guide_travel_deg=5.0, guide_min_move=15.0,
                camera_max_px=8.0,      # only with "camera": "locked"
                window_zoom=1.15, window_shift=0.08,   # a moving camera: the vanish test runs in windows across which the
                window_min_s=1.0, window_max_s=3.0,    # picture zooms at most 15 % and shifts at most 8 % of the width
                region_found=0.5,       # an event's whole region found again within 3 grid steps at this match = it moved while
                                        # covered, not vanished (RO-08 A7's bar stool, tilted under his arm: 0.69; A5's donut box: 0.10-0.18)
                prop_lost=0.7)          # share of a prop's points lost for good, away from the person, to call it vanished


# ---------------------------------------------------------------- video
def probe(clip):
    o = json.loads(subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                                   "stream=width,height,r_frame_rate,nb_read_frames", "-of", "json", clip],
                                  capture_output=True, check=True, text=True).stdout)["streams"][0]
    n, d = o["r_frame_rate"].split("/")
    return int(o["width"]), int(o["height"]), float(n) / float(d), int(o["nb_read_frames"])


def decode(clip, idx, W, H, scale_w=None):
    """RGB frames at the given indices (full size, or scale_w wide)."""
    import numpy as np
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    vf = f"select='{sel}'" + (f",scale={scale_w}:-2:flags=area" if scale_w else "")
    w, h = (scale_w, int(round(H * scale_w / W / 2)) * 2) if scale_w else (W, H)
    raw = subprocess.run([FF, "-v", "error", "-i", clip, "-vf", vf, "-vsync", "0", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    assert len(f) == len(idx), f"decoded {len(f)} of {len(idx)} frames"
    return f


def person_mask(rgb, pad):
    """Everyone in the frame (MediaPipe selfie segmentation, several people), grown by pad px. Cartoon people are often missed;
    the moving-thing test below covers them."""
    import cv2, numpy as np, mediapipe as mp
    H, W = rgb.shape[:2]; small = cv2.resize(rgb, (640, int(640 * H / W)))
    with mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1) as S:
        m = S.process(small).segmentation_mask
    m = cv2.resize((m > 0.5).astype(np.uint8), (W, H), interpolation=cv2.INTER_NEAREST)
    return cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * pad + 1, 2 * pad + 1)))


# ---------------------------------------------------------------- tracking
def grid_points(W, H, g):
    import numpy as np
    xs = np.arange(g / 2, W - g / 2 + 1e-6, g); ys = np.arange(g / 2, H - g / 2 + 1e-6, g)
    return np.array([(x, y) for y in ys for x in xs], np.float32)


def box_points(b, n=4):
    import numpy as np
    x0, y0, x1, y1 = b; ix, iy = 0.15 * (x1 - x0), 0.15 * (y1 - y0)
    return np.array([(x, y) for y in np.linspace(y0 + iy, y1 - iy, n) for x in np.linspace(x0 + ix, x1 - ix, n)], np.float32)


def run_tracker(small, seeds, W, tracker="cotracker"):
    """Seeds (N, 2) in full pixels on small[0] -> tracks (K, N, 2) in full pixels, visibility (K, N)."""
    import numpy as np
    from cotracker_mps import track
    s = (small.shape[2] - 1) / (W - 1)
    q = np.concatenate([np.zeros((len(seeds), 1), np.float32), seeds * s], 1)
    tr, vis = track(small, q)
    return tr / s, vis


def in_box(p, b):
    return b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3]


# ---------------------------------------------------------------- the vanish test (one direction)
def neighbour_motion(P, V, seeds, use, R):
    """For every point and sampled frame: the displacement its neighbours say its spot has (a local affine fit to the visible
    neighbours within R px at the seed frame, outliers dropped, so a zoom or a pan is followed), the motion its own move is
    judged against. Fewer than 6 neighbours: their median; fewer than 3: the global median."""
    import numpy as np
    K, N, _ = P.shape
    d2 = ((seeds[:, None, :] - seeds[None, :, :]) ** 2).sum(-1)
    nb = [np.nonzero((d2[n] <= R * R) & use & (np.arange(N) != n))[0] for n in range(N)]
    L = max(1, max(len(x) for x in nb)); idx = np.full((N, L), -1)
    for n, x in enumerate(nb):
        idx[n, :len(x)] = x
    ic = np.clip(idx, 0, None)
    X = np.concatenate([(seeds[ic] - seeds[:, None]) / R, np.ones((N, L, 1))], 2)          # N L 3, centred on the point
    disp = P - P[0:1]; valid = V & V[0:1]
    out = np.zeros_like(P); lam = np.diag([1e-3, 1e-3, 0.0])
    for k in range(K):
        w = ((idx >= 0) & valid[k][ic]).astype(np.float64); Y = disp[k][ic]
        cnt = w.sum(1)
        glob = np.median(disp[k][valid[k] & use], 0) if (valid[k] & use).sum() >= 3 else np.zeros(2)
        for _ in range(2):                                                                    # fit, drop outliers, refit
            A = np.einsum("nl,nli,nlj->nij", w, X, X) + lam; B = np.einsum("nl,nli,nlj->nij", w, X, Y)
            beta = np.linalg.solve(A + np.eye(3) * 1e-9, B)
            r = np.linalg.norm(Y - np.einsum("nli,nij->nlj", X, beta), axis=2)
            with np.errstate(all="ignore"):
                med = np.nanmedian(np.where(w > 0, r, np.nan), 1)
            w = w * (r <= np.maximum(3 * np.nan_to_num(med)[:, None], 4.0))
        dd = np.where(w[..., None] > 0, Y, np.nan)
        with np.errstate(all="ignore"):
            mdn = np.nanmedian(dd, 1)
        fit = beta[:, 2, :]
        out[k] = np.where((w.sum(1) >= 6)[:, None], fit, np.where((cnt >= 3)[:, None] & ~np.isnan(mdn), mdn, glob))
    return out


def ncc(A, pa, B, pb, h, hb, D):
    """Do the patch around pa in grey frame A (half size h) and the one around pb in grey frame B (half size hb, the camera's
    scale change) show the same thing? Correlation, so a lighting change does not count."""
    import cv2, numpy as np
    def crop(G, p, r):
        x, y = int(round(p[0])), int(round(p[1]))
        if x - r < 0 or y - r < 0 or x + r + 1 > G.shape[1] or y + r + 1 > G.shape[0]:
            return None
        return cv2.resize(G[y - r:y + r + 1, x - r:x + r + 1], (2 * h + 1, 2 * h + 1), interpolation=cv2.INTER_AREA).astype(np.float32)
    a, b = crop(A, pa, h), crop(B, pb, hb)
    if a is None or b is None:
        return None, "edge"
    sa, sb = a.std(), b.std()
    if sa < D["flat_std"] and sb < D["flat_std"]:
        return (1.0 if abs(a.mean() - b.mean()) < D["flat_mean_diff"] else 0.0), "flat"
    if sa < D["flat_std"] or sb < D["flat_std"]:
        return 0.0, "flat/texture"
    return float(((a - a.mean()) * (b - b.mean())).mean() / (sa * sb)), "ncc"


def lost_in_place(P, V, nmot, seeds, use, grays, mask_end, scale, other, D, H, W, fps_s, hs):
    """The points of one run that vanished in place. grays: this run's first and last frame (half size, grey); mask_end: the
    people on its last frame; scale: the camera's zoom at its last frame against its first; other = (P, V, nmot) of the
    opposite run, seeded on this run's last frame, in reverse sample order.
    A point vanished when it is never visible again (at least min_gone_s before the end), had not moved against what its
    neighbours say (local fit, so a zoom or pan is followed), its spot is inside the picture, no person and no moving thing
    covers the spot at the end (the opposite run's points there did not come in from elsewhere), and the spot looks different
    at the end than at the start (patch correlation, scaled by the zoom). Comparing the ends, not the moment of loss, is what
    keeps a person who walks in front of something and stays there from counting: their points at the end came from elsewhere.
    (A near-moment comparison was tried on 2026-10-14 and failed A6 and A7: the person mask misses people in dark scenes.)"""
    import numpy as np
    K, N, _ = P.shape
    place = D["place_frac"] * H; margin = 0.02 * W; h = max(6, int(round(0.009 * H * hs)))
    alive_after = np.flip(np.logical_or.accumulate(np.flip(V, 0), 0), 0)
    min_gone = max(2, int(math.ceil(D["min_gone_s"] * fps_s)))
    rel = np.linalg.norm((P - P[0:1]) - nmot, axis=2)
    Po, Vo, no = other; relo = np.linalg.norm((Po - Po[0:1]) - no, axis=2); r_near = D["grid_px"] * H / 1080
    inside = lambda p: margin <= p[0] <= W - margin and margin <= p[1] <= H - margin
    hb = max(2, int(round(h * scale)))
    out = []
    for n in np.nonzero(use)[0]:
        if not (V[0, n] and V[1, n]) or alive_after[-1, n]:
            continue
        t = int(np.argmin(alive_after[:, n]))                    # never visible again from sample t on
        if K - t < min_gone:
            continue
        if rel[:t][V[:t, n], n].max() > place:                   # it was moving: carried, eaten, swung; not vanished in place
            continue
        end = seeds[n] + nmot[-1, n]                             # where its spot is at the end, by its neighbours
        if not (inside(end) and inside(P[t - 1, n])):
            continue                                             # left the picture
        if mask_end[int(end[1] * hs), int(end[0] * hs)]:
            continue                                             # a person covers the spot at the end
        near = np.nonzero(np.linalg.norm(Po[0] - end, axis=1) <= r_near)[0]
        upto = K - t                                             # the opposite run's samples from the end back to the loss
        if len(near):
            mv = [relo[:upto][Vo[:upto, m], m].max() if Vo[:upto, m].any() else 0.0 for m in near]
            if float(np.median(mv)) > place:
                continue                                         # a moving thing now covers it (it came in from elsewhere)
        s, how = ncc(grays[0], seeds[n] * hs, grays[1], end * hs, h, hb, D)
        if s is None or s >= D["ncc_same"]:
            continue                                             # the spot looks the same: the tracker lost it, nothing changed
        out.append(dict(n=int(n), t=t, seed=seeds[n].tolist(), end=end.tolist(), ncc=round(s, 2), how=how))
    return out


def region_found(A, B, box, hs, R, z):
    """Best match of grey frame A's region (box, full pixels) anywhere within R px of it in grey frame B (half size, scaled by
    the zoom z): is the content still there, a little way off?"""
    import cv2, numpy as np
    x0, y0, x1, y1 = [int(round(max(0, v) * hs)) for v in box]; r = int(R * hs)
    t = A[y0:y1, x0:x1]
    if t.size == 0 or t.std() < 2:
        return 0.0
    win = B[max(0, y0 - r):y1 + r, max(0, x0 - r):x1 + r]; best = -1.0
    for s in (0.94 * z, z, 1.06 * z):
        tt = cv2.resize(t, None, fx=s, fy=s)
        if tt.shape[0] < win.shape[0] and tt.shape[1] < win.shape[1]:
            best = max(best, float(cv2.minMaxLoc(cv2.matchTemplate(win, tt, cv2.TM_CCOEFF_NORMED))[1]))
    return best


def clusters(pts, g, min_n):
    """Group lost points by seed position (neighbours within 1.6 grid steps)."""
    import numpy as np
    if not pts:
        return []
    S = np.array([p["seed"] for p in pts]); n = len(S); parent = list(range(n))
    def f(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    d = np.linalg.norm(S[:, None] - S[None], axis=2)
    for i in range(n):
        for j in range(i + 1, n):
            if d[i, j] <= 1.6 * g:
                parent[f(i)] = f(j)
    groups = {}
    for i in range(n):
        groups.setdefault(f(i), []).append(pts[i])
    return sorted([v for v in groups.values() if len(v) >= min_n], key=lambda v: -len(v))


# ---------------------------------------------------------------- the gate
def run(clip, spec, frames, outdir, cache=True, tracker="cotracker"):
    import cv2, numpy as np
    sp = json.load(open(spec)); D = dict(DEFAULTS, **sp.get("bounds", {}))
    W, H, fps, nfr = probe(clip)
    a, b = frames if frames else (0, nfr - 1)
    b = min(b, nfr - 1)
    stride = max(1, math.ceil((b - a + 1) / D["max_frames"]))
    idx = list(range(a, b + 1, stride))
    if idx[-1] != b:
        idx.append(b)
    K = len(idx); fps_s = fps / stride; g = D["grid_px"] * H / 1080
    rows = Rows(); t0 = time.time()
    small = decode(clip, idx, W, H, SMALL_W)
    first, last = decode(clip, [idx[0], idx[-1]], W, H)
    half = decode(clip, [idx[0], idx[-1]], W, H, HALF_W); hs = half.shape[2] / W
    masks = [person_mask(f, int(D["person_pad_frac"] * half.shape[1])) for f in half]
    m_last = cv2.resize(masks[-1], (W, H), interpolation=cv2.INTER_NEAREST)

    # seeds: the grid on each end frame, plus the spec's boxes on the first
    G = grid_points(W, H, g)
    spec_pts, spec_ix = [], {}
    def add(key, box):
        p = box_points(box); spec_ix[key] = list(range(sum(len(x) for x in spec_pts), sum(len(x) for x in spec_pts) + len(p)))
        spec_pts.append(p)
    for grp in sp.get("rigid", []):
        for pn, bx in grp["parts"].items():
            add(f"rigid:{grp['name']}.{pn}", bx)
    for c in sp.get("contacts", []):
        add(f"contact:{c['name']}", c["box"])
    for n, bx in sp.get("still", {}).items():
        add(f"still:{n}", bx)
    for pr in sp.get("props", []):
        add(f"prop:{pr['name']}", pr["box"])
    SP = np.concatenate(spec_pts) if spec_pts else np.zeros((0, 2), np.float32)
    fwd_seeds = np.concatenate([G, SP]).astype(np.float32)

    key = hashlib.sha256(json.dumps([sha256(clip), idx, fwd_seeds.round(1).tolist(), SMALL_W, tracker]).encode()).hexdigest()[:16]
    cpath = os.path.join(outdir, f".tracks-{key}.npz")
    os.makedirs(outdir, exist_ok=True)
    if cache and os.path.exists(cpath):
        z = np.load(cpath); Pf, Vf, Pb, Vb = z["Pf"], z["Vf"], z["Pb"], z["Vb"]
    else:
        Pf, Vf = run_tracker(small, fwd_seeds, W, tracker)
        Pb, Vb = run_tracker(np.ascontiguousarray(small[::-1]), G, W, tracker)        # backward: seeded on the last frame
        np.savez_compressed(cpath, Pf=Pf, Vf=Vf, Pb=Pb, Vb=Vb)
    nG = len(G)

    # what the grid test may use: not on a person at its seed frame, not in a may_change box (boxes are in first-frame
    # pixels; on a later frame they sit where the camera took them)
    R = 5 * g
    mc = list(sp.get("may_change", {}).values())
    def warp(bb, M):
        c = np.array([[bb[0], bb[1]], [bb[2], bb[1]], [bb[0], bb[3]], [bb[2], bb[3]]], np.float64) @ M[:, :2].T + M[:, 2]
        return [c[:, 0].min(), c[:, 1].min(), c[:, 0].max(), c[:, 1].max()]
    def usable(seeds, mask, M):
        boxes = [warp(bb, M) for bb in mc]
        return np.array([not mask[int(y * hs), int(x * hs)] and not any(in_box((x, y), bb) for bb in boxes) for x, y in seeds])
    ident = np.array([[1, 0, 0], [0, 1, 0]], np.float64)
    use_f = np.zeros(len(fwd_seeds), bool); use_f[:nG] = usable(G, masks[0], ident)

    # camera: a similarity fitted to the background grid points, first frame -> each sampled frame
    cams, cam_px = [], []
    for k in range(K):
        ok = use_f[:nG] & Vf[k, :nG] & Vf[0, :nG]
        M = None
        if ok.sum() >= 6:
            M, _ = cv2.estimateAffinePartial2D(Pf[0, :nG][ok], Pf[k, :nG][ok], method=cv2.RANSAC, ransacReprojThreshold=3.0)
        M = M if M is not None else ident.copy()
        cams.append(M)
        corners = np.array([[0, 0], [W, 0], [0, H], [W, H], [W / 2, H / 2]], np.float64)
        cam_px.append(float(np.linalg.norm(corners @ M[:, :2].T + M[:, 2] - corners, axis=1).max()))
    def own(k, ids):                       # the points' move against the camera at sample k (visible ones), median
        ok = [i for i in ids if Vf[k, i] and Vf[0, i]]
        if len(ok) < 2:
            return None
        pred = Pf[0, ok] @ cams[k][:, :2].T + cams[k][:, 2]
        return np.median(Pf[k, ok] - pred, 0)
    cam = sp.get("camera")
    locked = cam == "locked" or (isinstance(cam, dict) and cam.get("locked"))
    worst_cam = max(cam_px); kc = int(np.argmax(cam_px))
    rows.add("camera", (not locked) or worst_cam <= D["camera_max_px"],
             f"camera moved the picture by up to {worst_cam:.0f} px (frame {idx[kc]}; corners and centre, fitted to the background)"
             + (f"; spec says locked, max {D['camera_max_px']:g}" if locked else "; not declared locked, information only"),
             px=round(worst_cam, 1))
    scale = [math.sqrt(abs(np.linalg.det(M[:, :2]))) for M in cams]

    # ---- vanish (forward) and appear (backward), in windows the camera barely changes across. A first-vs-last comparison
    # needs the two ends to look alike: on RO-08 A8 (a 2x push-in) a spot 40 px wide at the end was 15 blurred px at the start.
    def cam_change(i, j):                  # zoom ratio and centre shift (px) from sample i to sample j
        A3 = lambda M: np.vstack([M, [0, 0, 1]])
        T = A3(cams[j]) @ np.linalg.inv(A3(cams[i])); c = np.array([W / 2, H / 2, 1.0])
        return scale[j] / scale[i], float(np.linalg.norm((T @ c)[:2] - c[:2]))
    def calm(i, j):
        z, sh = cam_change(i, j)
        return 1 / D["window_zoom"] <= z <= D["window_zoom"] and sh <= D["window_shift"] * W
    if all(calm(0, k) for k in range(K)):
        windows = [(0, K - 1)]
    else:
        lo, hi = max(2, int(math.ceil(D["window_min_s"] * fps_s))), max(3, int(D["window_max_s"] * fps_s))
        windows, i = [], 0
        while True:
            j = min(K - 1, i + lo)
            while j + 1 <= K - 1 and j + 1 - i <= hi and calm(i, j + 1):
                j += 1
            windows.append((i, j))
            if j >= K - 1:
                break
            i = max(i + 1, i + (j - i) // 2)                       # half-window overlap: an event at a seam is inside the next
    ends = sorted({k for w in windows for k in w})
    hf = dict(zip(ends, decode(clip, [idx[k] for k in ends], W, H, HALF_W))) if len(windows) > 1 else {0: half[0], K - 1: half[1]}
    gk = {k: cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for k, f in hf.items()}
    mk = {k: (masks[0] if k == 0 else masks[1] if k == K - 1 else person_mask(f, int(D["person_pad_frac"] * f.shape[0])))
          for k, f in hf.items()}
    lost_f, lost_b, events, biggest = [], [], [], {"vanish": 0, "appear": 0}
    moved_away = {"vanish": 0, "appear": 0}
    for (i, j) in windows:
        if len(windows) == 1:
            Pw, Vw, sw = Pf, Vf, fwd_seeds
            Qw, Uw = Pb, Vb
            uf = use_f
        else:
            sub = np.ascontiguousarray(small[i:j + 1])
            wkey = hashlib.sha256(json.dumps([key, i, j]).encode()).hexdigest()[:16]
            wpath = os.path.join(outdir, f".tracks-{wkey}.npz")
            if cache and os.path.exists(wpath):
                z = np.load(wpath); Pw, Vw, Qw, Uw = z["Pf"], z["Vf"], z["Pb"], z["Vb"]
            else:
                Pw, Vw = run_tracker(sub, G, W, tracker); Qw, Uw = run_tracker(np.ascontiguousarray(sub[::-1]), G, W, tracker)
                np.savez_compressed(wpath, Pf=Pw, Vf=Vw, Pb=Qw, Vb=Uw)
            sw = G; uf = usable(G, mk[i], cams[i])
        ub = usable(G, mk[j], cams[j])
        nfw = neighbour_motion(Pw, Vw, sw, uf, R); nbw = neighbour_motion(Qw, Uw, G, ub, R)
        z = scale[j] / scale[i]
        lf = lost_in_place(Pw, Vw, nfw, sw, uf, (gk[i], gk[j]), mk[j], z, (Qw, Uw, nbw), D, H, W, fps_s, hs)
        lb = lost_in_place(Qw, Uw, nbw, G, ub, (gk[j], gk[i]), mk[i], 1 / z, (Pw[:, :nG], Vw[:, :nG], nfw[:, :nG]), D, H, W, fps_s, hs)
        for kind, lost, backward in (("vanish", lf, False), ("appear", lb, True)):
            biggest[kind] = max(biggest[kind], max([len(c) for c in clusters(lost, g, 1)] or [0]))
            for ev in clusters(lost, g, D["min_event_pts"]):
                S = np.array([p["seed"] for p in ev])
                bx = [int(S[:, 0].min() - g / 2), int(S[:, 1].min() - g / 2), int(S[:, 0].max() + g / 2), int(S[:, 1].max() + g / 2)]
                found = region_found(gk[j] if backward else gk[i], gk[i] if backward else gk[j], bx, hs, 3 * g, 1 / z if backward else z)
                if found >= D["region_found"]:
                    moved_away[kind] += 1                                  # the same content is there, a little way off: it moved
                    continue
                fr = sorted(idx[j - p["t"] + 1] if backward else idx[i + p["t"]] for p in ev)   # last / first frame it was there
                events.append(dict(kind=kind, n=len(ev), frames=[fr[0], fr[-1]], window=[idx[i], idx[j]],
                                   box=bx, found_nearby=round(found, 2), box_frame=idx[j] if backward else idx[i],
                                   ncc=round(float(np.median([p["ncc"] for p in ev])), 2)))
        if len(windows) == 1:
            lost_f, lost_b = lf, lb
    # an event seen by two overlapping windows is one event
    def same(e, f):
        if e["kind"] != f["kind"] or e["frames"][1] < f["frames"][0] - 2 * stride or f["frames"][1] < e["frames"][0] - 2 * stride:
            return False
        ix = max(0, min(e["box"][2], f["box"][2]) - max(e["box"][0], f["box"][0])) * max(0, min(e["box"][3], f["box"][3]) - max(e["box"][1], f["box"][1]))
        return ix > 0.3 * min((e["box"][2] - e["box"][0]) * (e["box"][3] - e["box"][1]), (f["box"][2] - f["box"][0]) * (f["box"][3] - f["box"][1]))
    merged = []
    for e in sorted(events, key=lambda e: -e["n"]):
        if not any(same(e, m) for m in merged):
            merged.append(e)
    events = merged
    wtxt = "" if len(windows) == 1 else f" [{len(windows)} windows, the camera moves]"
    for kind in ("vanish", "appear"):
        evs = [e for e in events if e["kind"] == kind]
        what = ("grid points lost for good in place (no move, inside the picture, nothing moving over it, the spot looks different at the end)"
                if kind == "vanish" else "grid points there at the end, came from nowhere (traced backward: no move, nothing moved off it)")
        nl = len(lost_f if kind == "vanish" else lost_b) if len(windows) == 1 else "some"
        rows.add(kind, not evs, f"{nl} {what}{wtxt}; biggest cluster {biggest[kind]} (an event at {D['min_event_pts']})"
                 + (f"; {moved_away[kind]} cluster(s) found again nearby (moved while covered, not counted)" if moved_away[kind] else "")
                 + "".join(f"; {e['n']} pts in box {e['box']} (f{e['box_frame']} pixels) frames {e['frames'][0]}-{e['frames'][1]} "
                           f"(spot match {e['ncc']})" for e in evs[:5]), events=evs[:8])

    # ---- the spec's parts, on every sampled frame
    def ids(k_):
        return [nG + i for i in spec_ix.get(k_, [])]
    for grp in sp.get("rigid", []):
        n = grp["name"]; parts = {pn: ids(f"rigid:{n}.{pn}") for pn in grp["parts"]}
        worst_spread, worst_dev, moves = 0.0, 0.0, []
        for k in range(K):
            pm = {pn: own(k, ii) for pn, ii in parts.items()}; pm = {p: v for p, v in pm.items() if v is not None}
            if len(pm) < 2:
                moves.append(None); continue
            m = np.median(np.array(list(pm.values())), 0); moves.append(m); mag = float(np.hypot(*m))
            spread = max(float(np.hypot(*(v - m))) for v in pm.values())
            lim = max(D["rigid_disagree_px"], D["rigid_disagree_frac"] * mag)
            worst_spread = max(worst_spread, spread / lim * D["rigid_disagree_px"]) if lim else worst_spread
            if grp.get("guide") and mag >= D["guide_min_move"]:
                d = abs(dang(ang((0, 0), m), line_deg(grp["guide"], m, (0, 0))))
                worst_dev = max(worst_dev, d)
        found = [m for m in moves if m is not None]
        rows.add(f"rigid:{n}.together", worst_spread <= D["rigid_disagree_px"] and len(found) >= 0.8 * K,
                 f"{n}: parts tracked on {len(found)} of {K} samples; worst disagreement {worst_spread:.0f} "
                 f"(scaled to the {D['rigid_disagree_px']:g} px / {D['rigid_disagree_frac']:.0%} limit)")
        if grp.get("guide"):
            mx = grp.get("max_deg", D["guide_travel_deg"])
            rows.add(f"rigid:{n}.guide", worst_dev <= mx, f"{n} travel off its guide by up to {worst_dev:.1f} deg on any frame (max {mx})")
        if found:
            lo, hi = grp.get("move_px", [3, 1e9]); mag = float(np.hypot(*found[-1]))
            rows.add(f"rigid:{n}.distance", lo <= mag <= hi, f"{n} moved {mag:.0f} px by the end (allowed {lo} to {hi:g})")
        for c in [c for c in sp.get("contacts", []) if c["rides"] == n]:
            slip = 0.0; kk = 0
            for k in range(K):
                r_ = own(k, ids(f"contact:{c['name']}"))
                if r_ is not None and moves[k] is not None:
                    s_ = float(np.hypot(*(r_ - moves[k])))
                    if s_ > slip:
                        slip, kk = s_, k
            lim = c.get("max_slip_px", D["contact_slip_px"])
            rows.add(f"contact:{c['name']}", slip <= lim, f"{c['name']} slips on {n} by up to {slip:.0f} px (frame {idx[kk]}; max {lim:g})")
    for n, bx in sp.get("still", {}).items():
        worst, kk = 0.0, 0
        for k in range(K):
            m = own(k, ids(f"still:{n}"))
            if m is not None and float(np.hypot(*m)) > worst:
                worst, kk = float(np.hypot(*m)), k
        rows.add(f"still:{n}", worst <= D["still_px"], f"{n} moved up to {worst:.1f} px against the camera (frame {idx[kk]}; max {D['still_px']:g})")
    for pr in sp.get("props", []):
        if pr.get("may_leave"):
            continue
        ii = ids(f"prop:{pr['name']}")
        gone = [i for i, j in zip(range(len(ii)), ii) if not Vf[-max(1, int(D['min_gone_s'] * fps_s)):, j].any()]
        endp = [Pf[-1, ii[i]] for i in gone]
        away = [p for p in endp if not (0 <= p[0] < W and 0 <= p[1] < H and m_last[int(p[1]), int(p[0])])]
        frac = len(away) / max(1, len(ii))
        rows.add(f"prop:{pr['name']}.kept", frac < D["prop_lost"], f"{pr['name']}: {len(gone)} of {len(ii)} points not seen in the "
                 f"last {D['min_gone_s']} s, {len(away)} of them away from any person ({frac:.0%}; a vanished prop at {D['prop_lost']:.0%})")

    secs = time.time() - t0
    rows.insert(0, dict(key="tracker", ok=True, detail=f"CoTracker3: {K} frames of {a}-{b} (every {stride}), {len(fwd_seeds)} points "
                        f"forward + {nG} backward, grid {g:.0f} px, {secs:.0f} s"))
    sheet, fdir = evidence(clip, idx, first, last, events, lost_f, lost_b, W, H, outdir, rows, fps, (a, b))
    return rows, sheet, fdir, dict(frames=[a, b], stride=stride, samples=K, fps=fps)


def evidence(clip, idx, first, last, events, lost_f, lost_b, W, H, outdir, rows, fps, ab):
    """One JPEG: first | last frame with the lost points and event boxes; per event a strip of crops across its frames; the
    failed rows. Plus a folder of frames every 0.25 s for the reviewer."""
    import cv2, numpy as np
    stem = os.path.splitext(os.path.basename(clip))[0] + (f".f{ab[0]}-{ab[1]}" if ab else "")
    A, B = cv2.cvtColor(first, cv2.COLOR_RGB2BGR), cv2.cvtColor(last, cv2.COLOR_RGB2BGR)
    for p in lost_f:
        cv2.circle(A, tuple(int(v) for v in p["seed"]), 7, (255, 0, 255), -1)
    for p in lost_b:
        cv2.circle(B, tuple(int(v) for v in p["seed"]), 7, (0, 165, 255), -1)
    for e in events:
        im = A if e["kind"] == "vanish" else B
        x0, y0, x1, y1 = e["box"]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 4)
        cv2.putText(im, f"{e['kind']} f{e['frames'][0]}-{e['frames'][1]}" + ("" if e.get("box_frame") in (idx[0], idx[-1]) else f" (box in f{e.get('box_frame')})"), (x0, max(30, y0 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)
    cv2.putText(A, f"FIRST f{idx[0]} (magenta: lost in place)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)
    cv2.putText(B, f"LAST f{idx[-1]} (orange: from nowhere)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)
    top = np.hstack([A, B]); top = cv2.resize(top, (2400, int(2400 * top.shape[0] / top.shape[1])))
    parts = [top]
    for e in events[:6]:
        x0, y0, x1, y1 = e["box"]; px, py = int(0.4 * (x1 - x0)) + 20, int(0.4 * (y1 - y0)) + 20
        x0, y0, x1, y1 = max(0, x0 - px), max(0, y0 - py), min(W, x1 + px), min(H, y1 + py)
        f0, f1 = e["frames"]; span = max(f1 - f0, int(fps))
        at = sorted(set(int(v) for v in np.clip(np.linspace(f0 - span // 2, f1 + span // 2, 8), ab[0], ab[1])))
        crops = decode(clip, at, W, H)
        tiles = []
        for f, c in zip(at, crops):
            t = cv2.cvtColor(c[y0:y1, x0:x1], cv2.COLOR_RGB2BGR); t = cv2.resize(t, (int(280 * t.shape[1] / t.shape[0]), 280))
            t = cv2.copyMakeBorder(t, 30, 4, 4, 4, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            cv2.putText(t, f"{e['kind']} f{f}", (4, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 200), 2)
            tiles.append(t)
        s = np.hstack(tiles)
        s = cv2.resize(s, (2400, int(2400 * s.shape[0] / s.shape[1]))) if s.shape[1] > 2400 else \
            np.pad(s, ((0, 0), (0, 2400 - s.shape[1]), (0, 0)), constant_values=255)
        parts.append(s)
    fails = [r for r in rows if not r["ok"]]
    pad = np.full((40 + 34 * max(1, len(fails)), 2400, 3), 255, np.uint8)
    for i, r in enumerate(fails or [dict(key="ALL ROWS PASS", detail="")]):
        cv2.putText(pad, (r["key"] + "  " + r["detail"])[:180], (10, 32 + 34 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 0, 200), 2)
    parts.append(pad)
    sheet = os.path.join(outdir, f"{stem}.clipcheck.jpg")
    cv2.imwrite(sheet, np.vstack(parts), [cv2.IMWRITE_JPEG_QUALITY, 88])
    fdir = os.path.join(outdir, f"{stem}.frames"); os.makedirs(fdir, exist_ok=True)
    at = sorted(set(list(range(ab[0], ab[1] + 1, max(1, int(round(fps / 4))))) + [ab[1]]))
    for f, c in zip(at, decode(clip, at, W, H)):
        cv2.imwrite(os.path.join(fdir, f"f{f:04d}.jpg"), cv2.cvtColor(c, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    return sheet, fdir


# ---------------------------------------------------------------- stamps
def stamp_path(clip, frames=None):
    return clip + (f".f{frames[0]}-{frames[1]}" if frames else "") + STAMP_SUFFIX


def require_pass(clip, frames=None, quiet=False):
    """For callers: raise unless this exact take (and range) passed clipcheck at this version AND a fresh reviewer passed it."""
    p = stamp_path(clip, frames)
    if not os.path.exists(p):
        raise SystemExit(f"no clipcheck stamp: run _shared/framecheck/clipcheck.py {clip} --spec SPEC"
                         + (f" --frames {frames[0]}:{frames[1]}" if frames else ""))
    d = json.load(open(p)); probs = []
    if d.get("clip_version") != CLIP_VERSION:
        probs.append(f"stamp is clipcheck {d.get('clip_version')}, this is {CLIP_VERSION}: re-run")
    if d.get("clip_sha256") != sha256(clip):
        probs.append("the take changed since it was checked (sha256 differs): re-run and re-review")
    if d.get("spec_sha256") and os.path.exists(d.get("spec", "")) and d["spec_sha256"] != sha256(d["spec"]):
        probs.append("the spec changed since the check ran: re-run")
    if d.get("verdict") != "PASS":
        probs.append(f"clipcheck verdict {d.get('verdict')}: " + "; ".join(r["key"] for r in d.get("rows", []) if not r["ok"]))
    rv = d.get("review") or {}
    if rv.get("verdict") != "PASS":
        probs.append("no frame-reviewer PASS recorded (clipcheck.py TAKE --review REVIEW.md)" if not rv
                     else f"frame-reviewer verdict {rv.get('verdict')} ({rv.get('file')})")
    elif rv.get("clip_sha256") != d.get("clip_sha256"):
        probs.append("the review was of a different take")
    if probs:
        raise SystemExit(f"clipcheck REFUSES {os.path.basename(clip)}" + (f" frames {frames[0]}-{frames[1]}" if frames else "")
                         + ":\n  - " + "\n  - ".join(probs))
    if not quiet:
        print(f"clipcheck {CLIP_VERSION}: PASS + reviewer PASS ({os.path.basename(clip)})")
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip")
    ap.add_argument("--spec"); ap.add_argument("--frames", help="A:B, the frames an edit uses (both included)")
    ap.add_argument("--out", help="evidence folder (default: clipcheck/ next to the take)")
    ap.add_argument("--review"); ap.add_argument("--verify", action="store_true")
    ap.add_argument("--no-stamp", action="store_true", help="measure only (proof runs)")
    ap.add_argument("--no-cache", action="store_true", help="re-track even if this take's tracks are cached in the out folder")
    ap.add_argument("--json")
    a = ap.parse_args()
    fr = tuple(int(v) for v in a.frames.split(":")) if a.frames else None
    if a.verify:
        require_pass(a.clip, fr); return 0
    if a.review:
        p = stamp_path(a.clip, fr)
        if not os.path.exists(p):
            raise SystemExit("no clipcheck stamp; run the check first")
        d = json.load(open(p))
        if d.get("clip_sha256") != sha256(a.clip):
            raise SystemExit("this take is not the one checked; re-run the check first")
        v = re.findall(r"VERDICT:\s*\**\s*(PASS|FAIL)", open(a.review).read())
        if not v:
            raise SystemExit("no 'VERDICT: PASS' or 'VERDICT: FAIL' line in the review")
        d["review"] = dict(verdict=v[-1], file=os.path.abspath(a.review), sha256=sha256(a.review), clip_sha256=d["clip_sha256"],
                           when=time.strftime("%Y-%m-%dT%H:%M:%S%z"))
        json.dump(d, open(p, "w"), indent=1)
        print(f"reviewer verdict {v[-1]} recorded in {os.path.basename(p)}")
        return 0 if v[-1] == "PASS" else 1
    if not a.spec:
        ap.error("--spec is required to run the check")
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.clip)), "clipcheck")
    rows, sheet, fdir, info = run(a.clip, a.spec, fr, out, cache=not a.no_cache)
    verdict = "PASS" if all(r["ok"] for r in rows) else "FAIL"
    for r in rows:
        print(f"  {'PASS' if r['ok'] else 'FAIL'}  {r['key']:<26} {r['detail']}")
    print(f"VERDICT {verdict}  (clipcheck {CLIP_VERSION}; evidence {sheet}; frames for the reviewer {fdir})")
    d = dict(clip_version=CLIP_VERSION, verdict=verdict, tracker="cotracker3", clip=os.path.abspath(a.clip), clip_sha256=sha256(a.clip), **info,
             spec=os.path.abspath(a.spec), spec_sha256=sha256(a.spec), evidence=sheet, review_frames=fdir,
             when=time.strftime("%Y-%m-%dT%H:%M:%S%z"), rows=rows)
    if a.json:
        json.dump(d, open(a.json, "w"), indent=1)
    if not a.no_stamp:
        json.dump(d, open(stamp_path(a.clip, fr), "w"), indent=1)
        print(f"  stamp -> {stamp_path(a.clip, fr)}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
