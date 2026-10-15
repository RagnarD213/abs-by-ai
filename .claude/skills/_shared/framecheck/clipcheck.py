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

DEFAULTS = dict(grid_px=40,             # grid spacing at 1080p (scaled with the take's height): 48 x 27 points
                max_frames=64,          # memory (cotracker_mps.py): longer takes are sampled, a 6 s take every 3rd frame (8 per s)
                place_frac=0.025,       # "had not moved": within this fraction of the height against its neighbours (27 px at 1080p)
                min_gone_s=0.4,         # lost for at least this long before the end
                ncc_same=0.5,           # patch correlation at or above this = the spot looks the same (the tracker lost it, nothing changed)
                flat_std=4.0,           # a patch with less grey-level spread than this is flat; two flat patches compare by mean
                flat_mean_diff=25.0,
                min_event_pts=4,        # points in one cluster to call it an event
                person_pad_frac=0.03,   # person masks grown by this fraction of the height
                still_px=5.0,           # still boxes: tracker noise over a take is 1 to 3 px
                contact_slip_px=12.0,
                rigid_disagree_px=10.0, rigid_disagree_frac=0.12, guide_travel_deg=5.0, guide_min_move=15.0,
                camera_max_px=8.0,      # only with "camera": "locked"
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


TRACKERS = {"tapir": "tapir_mps", "cotracker": "cotracker_mps"}


def run_tracker(small, seeds, W, tracker):
    """Seeds (N, 2) in full pixels on small[0] -> tracks (K, N, 2) in full pixels, visibility (K, N)."""
    import numpy as np, importlib
    track = importlib.import_module(TRACKERS[tracker]).track
    s = (small.shape[2] - 1) / (W - 1)
    q = np.concatenate([np.zeros((len(seeds), 1), np.float32), seeds * s], 1)
    tr, vis = track(small, q)
    return tr / s, vis


def in_box(p, b):
    return b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3]


# ---------------------------------------------------------------- the vanish test (one direction)
def neighbour_motion(P, V, seeds, use, R):
    """For every point and sampled frame: the median displacement of its visible neighbours (within R px at the seed frame,
    from the points in `use`), the local background motion its own move is judged against."""
    import numpy as np
    K, N, _ = P.shape
    d2 = ((seeds[:, None, :] - seeds[None, :, :]) ** 2).sum(-1)
    nb = [np.nonzero((d2[n] <= R * R) & use & (np.arange(N) != n))[0] for n in range(N)]
    L = max(1, max(len(x) for x in nb)); idx = np.full((N, L), -1)
    for n, x in enumerate(nb):
        idx[n, :len(x)] = x
    disp = P - P[0:1]; valid = V & V[0:1]
    out = np.zeros_like(P)
    glob = np.array([np.median(disp[k][valid[k] & use], 0) if (valid[k] & use).sum() >= 3 else np.zeros(2) for k in range(K)])
    for k in range(K):
        dd = np.where((idx >= 0)[..., None] & valid[k][np.clip(idx, 0, None)][..., None], disp[k][np.clip(idx, 0, None)], np.nan)
        cnt = (~np.isnan(dd[..., 0])).sum(1)
        with np.errstate(all="ignore"):
            med = np.nanmedian(dd, 1)
        out[k] = np.where((cnt >= 3)[:, None], med, glob[k])
    return out


def ncc(A, pa, B, pb, h, D):
    """Do the patches around pa in grey frame A and pb in grey frame B show the same thing? (correlation, gain/offset-proof)"""
    import numpy as np
    def crop(G, p):
        x, y = int(round(p[0])), int(round(p[1]))
        if x - h < 0 or y - h < 0 or x + h + 1 > G.shape[1] or y + h + 1 > G.shape[0]:
            return None
        return G[y - h:y + h + 1, x - h:x + h + 1].astype(np.float32)
    a, b = crop(A, pa), crop(B, pb)
    if a is None or b is None:
        return None, "edge"
    sa, sb = a.std(), b.std()
    if sa < D["flat_std"] and sb < D["flat_std"]:
        return (1.0 if abs(a.mean() - b.mean()) < D["flat_mean_diff"] else 0.0), "flat"
    if sa < D["flat_std"] or sb < D["flat_std"]:
        return 0.0, "flat/texture"
    return float(((a - a.mean()) * (b - b.mean())).mean() / (sa * sb)), "ncc"


def lost_in_place(P, V, nmot, seeds, use, first_g, last_g, mask_last, other, D, H, W, fps_s):
    """The points of one run that vanished in place. other = (P, V, nmot) of the opposite run, seeded on this run's last frame,
    sampled in reverse order; its points at this run's lost spots tell whether a moving thing now covers the spot."""
    import numpy as np
    K, N, _ = P.shape
    place = D["place_frac"] * H; margin = 0.02 * W; h = max(8, int(round(0.018 * H)))
    alive_after = np.flip(np.logical_or.accumulate(np.flip(V, 0), 0), 0)
    min_gone = max(2, int(math.ceil(D["min_gone_s"] * fps_s)))
    disp = P - P[0:1]; rel = np.linalg.norm(disp - nmot, axis=2)
    Po, Vo, no = other; relo = np.linalg.norm((Po - Po[0:1]) - no, axis=2)
    out = []
    for n in np.nonzero(use)[0]:
        if not (V[0, n] and V[1, n]) or alive_after[-1, n]:
            continue
        t = int(np.argmin(alive_after[:, n]))                      # first sample after which it is never visible again
        if K - t < min_gone:
            continue
        seen = V[:t, n]
        if rel[:t][seen, n].max() > place:                         # it was moving: carried, eaten, swung; not vanished in place
            continue
        end = seeds[n] + nmot[-1, n]                               # where its spot is at the end, by its neighbours' move
        last_seen = P[t - 1, n]
        if not (margin <= end[0] <= W - margin and margin <= end[1] <= H - margin and
                margin <= last_seen[0] <= W - margin and margin <= last_seen[1] <= H - margin):
            continue                                               # left the picture
        if mask_last[int(min(H - 1, end[1])), int(min(W - 1, end[0]))]:
            continue                                               # a person covers the spot at the end
        near = np.nonzero(np.linalg.norm(Po[0] - end, axis=1) <= 1.0 * D["grid_px"] * H / 1080)[0]
        upto = K - t                                               # the other run's samples from the end back to the loss
        if len(near):
            mv = [relo[:upto][Vo[:upto, m], m].max() if Vo[:upto, m].any() else 0.0 for m in near]
            if float(np.median(mv)) > place:
                continue                                           # a moving thing now covers it (it came in from elsewhere)
        s, how = ncc(first_g, seeds[n], last_g, end, h, D)
        if s is None or s >= D["ncc_same"]:
            continue                                               # the spot looks the same: the tracker lost it, nothing changed
        out.append(dict(n=int(n), t=t, seed=seeds[n].tolist(), end=end.tolist(), ncc=round(s, 2), how=how))
    return out


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
    first_g, last_g = cv2.cvtColor(first, cv2.COLOR_RGB2GRAY), cv2.cvtColor(last, cv2.COLOR_RGB2GRAY)
    pad = int(D["person_pad_frac"] * H)
    m_first, m_last = person_mask(first, pad), person_mask(last, pad)

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
    secs = time.time() - t0
    nG = len(G)

    # what the grid test may use: not on a person at its seed frame, not in a may_change box
    mc = list(sp.get("may_change", {}).values())
    def usable(seeds, mask):
        return np.array([not mask[int(y), int(x)] and not any(in_box((x, y), bb) for bb in mc) for x, y in seeds])
    use_f = np.zeros(len(fwd_seeds), bool); use_f[:nG] = usable(G, m_first)
    use_b = usable(G, m_last)
    # may_change boxes are in first-frame pixels; on the last frame they sit where the camera took them (checked below)
    R = 5 * g
    nf = neighbour_motion(Pf, Vf, fwd_seeds, use_f, R)
    nb_ = neighbour_motion(Pb, Vb, G, use_b, R)

    # camera: a similarity fitted to the background grid points, first frame -> each sampled frame
    cams, cam_px = [], []
    for k in range(K):
        ok = use_f[:nG] & Vf[k, :nG] & Vf[0, :nG]
        M = None
        if ok.sum() >= 6:
            M, _ = cv2.estimateAffinePartial2D(Pf[0, :nG][ok], Pf[k, :nG][ok], method=cv2.RANSAC, ransacReprojThreshold=3.0)
        M = M if M is not None else np.array([[1, 0, 0], [0, 1, 0]], np.float64)
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

    # may_change boxes on the last frame: where the camera took them
    Mend = cams[-1]
    mc_end = []
    for bb in mc:
        c = np.array([[bb[0], bb[1]], [bb[2], bb[3]]], np.float64) @ Mend[:, :2].T + Mend[:, 2]
        mc_end.append([c[:, 0].min(), c[:, 1].min(), c[:, 0].max(), c[:, 1].max()])
    use_b &= np.array([not any(in_box(p, bb) for bb in mc_end) for p in G])

    # ---- vanish (forward) and appear (backward)
    lost_f = lost_in_place(Pf, Vf, nf, fwd_seeds, use_f, first_g, last_g, m_last, (Pb, Vb, nb_), D, H, W, fps_s)
    lost_b = lost_in_place(Pb, Vb, nb_, G, use_b, last_g, first_g, m_first, (Pf[:, :nG], Vf[:, :nG], nf[:, :nG]), D, H, W, fps_s)
    ev_f = clusters(lost_f, g, D["min_event_pts"]); ev_b = clusters(lost_b, g, D["min_event_pts"])

    def describe(ev, backward):
        S = np.array([p["seed"] for p in ev]); ts = [p["t"] for p in ev]
        fr = sorted(idx[K - t] if backward else idx[t] for t in ts)          # the frame where it was last / first there
        box = [int(S[:, 0].min() - g / 2), int(S[:, 1].min() - g / 2), int(S[:, 0].max() + g / 2), int(S[:, 1].max() + g / 2)]
        return dict(box=box, n=len(ev), frames=[fr[0], fr[-1]], ncc=round(float(np.median([p["ncc"] for p in ev])), 2))
    events = [dict(kind="vanish", **describe(e, False)) for e in ev_f] + [dict(kind="appear", **describe(e, True)) for e in ev_b]
    for kind, evs, lost in (("vanish", [e for e in events if e["kind"] == "vanish"], lost_f),
                            ("appear", [e for e in events if e["kind"] == "appear"], lost_b)):
        what = ("lost for good in place (no move, inside the picture, nothing moving over it, the spot looks different at the end)"
                if kind == "vanish" else "there at the end, came from nowhere (traced backward: no move, nothing moved off it)")
        rows.add(kind, not evs, f"{len(lost)} grid points {what}; {len(evs)} cluster(s) of {D['min_event_pts']}+"
                 + "".join(f"; {e['n']} pts in box {e['box']} frames {e['frames'][0]}-{e['frames'][1]} (spot match {e['ncc']})"
                           for e in evs[:5]), events=evs[:8])

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

    rows.insert(0, dict(key="tracker", ok=True, detail=f"{dict(tapir='BootsTAPIR', cotracker='CoTracker3')[tracker]}: {K} frames of {a}-{b} (every {stride}), {len(fwd_seeds)} points "
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
        cv2.putText(im, f"{e['kind']} f{e['frames'][0]}-{e['frames'][1]}", (x0, max(30, y0 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)
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
    ap.add_argument("--tracker", choices=sorted(TRACKERS), default="cotracker",
                    help="cotracker = CoTracker3 (CC BY-NC); tapir = BootsTAPIR (Apache 2.0). README, Licences")
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
    rows, sheet, fdir, info = run(a.clip, a.spec, fr, out, cache=not a.no_cache, tracker=a.tracker)
    verdict = "PASS" if all(r["ok"] for r in rows) else "FAIL"
    for r in rows:
        print(f"  {'PASS' if r['ok'] else 'FAIL'}  {r['key']:<26} {r['detail']}")
    print(f"VERDICT {verdict}  (clipcheck {CLIP_VERSION}; evidence {sheet}; frames for the reviewer {fdir})")
    d = dict(clip_version=CLIP_VERSION, verdict=verdict, tracker=a.tracker, clip=os.path.abspath(a.clip), clip_sha256=sha256(a.clip), **info,
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
