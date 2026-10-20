#!/usr/bin/env python3
"""The frame gate: measure an AI clip's START/END pair against its spec, stamp the result, refuse unchecked pairs.

usage:
  gate.py START END --spec spec.json [--out DIR]     measure, write the evidence sheet and the stamp (exit 0 PASS, 1 FAIL)
  gate.py START END --review review.md               record the frame-reviewer's verdict (its last "VERDICT:" line) in the stamp
  gate.py START END --verify                         exit 0 only if the gate PASSed at this version AND a reviewer PASSed,
                                                     both for exactly these two files (sha256) and this spec
Callers (review page builders, motion generators): `from gate import require_pass; require_pass(START, END)`.

What it measures (each row PASS/FAIL with numbers; the spec says what to test, see README "The frame spec"):
  person.*   MediaPipe Pose on both frames: body line against the machine's guide, bone lengths START vs END (8 %), whether the
             END reach is what straightening those bones allows, anchored joints (hips, shoulders stay on the pad)
  rigid.*    each rigid group (a sled: plates, horns, footplate) tracked part by part: found (score), moved together, along its
             guide, by a plausible amount, and still sharp (an image model smears what it redraws)
  contact.*  parts that must ride a group (feet on the footplate) move with it, not slide on it
  still.*    parts that must not move (machine frame, seat, background) did not
  static     every pixel outside the person, the moving parts and the may_change boxes is unchanged (catches stretched frames,
             patches and pasted seams), reported as boxes
  prop.*     a held object goes where its hand goes and leaves nothing behind (RA-04 F5h2's floating half phone)
  hands      informational: hand crops at 3x on the evidence sheet for the reviewer's finger count (MediaPipe cannot count fingers)

Built 2026-10-14 on RA-04's leg press. Proven: the five rejected pairs fail, the approved F4h/F5p passes (README, "Proof").
"""
import argparse, hashlib, json, math, os, re, sys, time

GATE_VERSION = "1.0.0"   # bump on ANY change to a check or a default bound; older stamps stop verifying
STAMP_SUFFIX = ".framecheck.json"
HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULTS = dict(guide_max_deg=10.0,        # leg line vs machine guide. Approved F4h/F5p: 6.0 / 5.6; rejected F4c: 26 to 43
                bone_tol=0.08,             # torso/thigh/shin change START->END. Rejected F5h2 legs: +24 %
                reach_tol=0.08,            # END hip-ankle vs law of cosines from START bones and END knee angle
                anchor_frac=0.15,          # anchored joints may drift this fraction of the torso length
                min_score=0.85,            # free-search match score to trust a part's own move (README rule 3)
                ride_score=0.70,           # match where the group's move puts a part (F5p footplate: >= 0.77 over 9 box shifts)
                rigid_disagree_px=10.0,    # strong parts (score >= 0.9) around the group's move (F5g_d footplate vs plates: 16-24;
                                           # F5p with every box shifted 5 px: 11 at 0.87, so only strong parts count)
                rigid_disagree_frac=0.12,  # ... or this fraction of the move, whichever is larger
                guide_travel_deg=5.0,      # group travel vs its guide (F5e_b: 7, F5f_b: 7-11)
                min_sharp=0.72,            # p99 gradient END/START where the group's move puts each part. Box-shift test:
                                           # approved F5p footplate 0.79-1.04, rejected F5m (smeared) 0.31-0.66
                contact_slip_px=12.0,      # rider vs group move (F5j near shoe: 23 px; F5p near shoe: 4)
                contact_min_score=0.75,    # riders are usually the regenerated person (shoes), so a lower match bar
                still_px=3.0,              # still boxes may move this much (F5e_b top cap: 56 px)
                static_tol=24,             # grey-level change counted as "changed" (after +-1 px shift and blur)
                static_min_area=250,       # smallest changed blob (px) reported
                prop_leftover=0.6)         # share of any half of a moved prop's START box still identical in END = a leftover
                                           # (F5h2's floating half phone: top half 0.98; F5p, where the phone really left: <= 0.34)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- measuring
def ang(p, q):
    return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0]))


def joint(a, b, c):
    import numpy as np
    v1, v2 = np.subtract(a, b), np.subtract(c, b)
    return math.degrees(math.acos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9), -1, 1)))


def pose(img, side=None):
    """Landmarks of the one person (both sides), the camera-near side, the person mask. None if nobody is found."""
    import cv2, numpy as np, mediapipe as mp
    H, W = img.shape[:2]
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=True) as P:
        r = P.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not r.pose_landmarks:
        return None
    lm = r.pose_landmarks.landmark; L = mp.solutions.pose.PoseLandmark
    pts = {n.name.lower(): (lm[n].x * W, lm[n].y * H, lm[n].visibility) for n in L}
    if side in (None, "auto"):
        v = lambda s: sum(pts[f"{s}_{j}"][2] for j in ("hip", "knee", "ankle"))
        side = "left" if v("left") >= v("right") else "right"
    g = lambda j: pts[f"{side}_{j}"][:2]
    S, Hp, K, A = g("shoulder"), g("hip"), g("knee"), g("ankle")
    mask = (r.segmentation_mask > 0.3).astype(np.uint8) if r.segmentation_mask is not None else np.zeros((H, W), np.uint8)
    return dict(pts=pts, side=side, mask=mask, S=S, H=Hp, K=K, A=A,
                vis=min(pts[f"{side}_{j}"][2] for j in ("shoulder", "hip", "knee", "ankle")),
                torso=math.dist(S, Hp), thigh=math.dist(Hp, K), shin=math.dist(K, A), reach=math.dist(Hp, A),
                knee=joint(Hp, K, A), hip_angle=joint(S, Hp, K), leg_deg=ang(Hp, A))


def line_deg(l, toward=None, frm=None):
    """Angle of a guide line, pointed the same way as frm->toward (so a rail and a leg compare head to head)."""
    x1, y1, x2, y2 = l
    if toward is not None and (x2 - x1) * (toward[0] - frm[0]) + (y2 - y1) * (toward[1] - frm[1]) < 0:
        x1, y1, x2, y2 = x2, y2, x1, y1
    return ang((x1, y1), (x2, y2))


def dang(a, b):
    return (a - b + 180) % 360 - 180


def track(A, B, box, R=260, scales=(0.94, 0.97, 1.0, 1.03, 1.06)):
    """Find START's box in END within R px (rigid.py's search, plus the matched END box)."""
    import cv2, numpy as np
    x0, y0, x1, y1 = box; t = A[y0:y1, x0:x1]; best = None
    sx0, sy0 = max(0, x0 - R), max(0, y0 - R); win = B[sy0:min(B.shape[0], y1 + R), sx0:min(B.shape[1], x1 + R)]
    for s in scales:
        tt = cv2.resize(t, None, fx=s, fy=s)
        if tt.shape[0] >= win.shape[0] or tt.shape[1] >= win.shape[1]:
            continue
        r = cv2.matchTemplate(win, tt, cv2.TM_CCOEFF_NORMED); _, v, _, p = cv2.minMaxLoc(r)
        if best is None or v > best[0]:
            best = (float(v), (p[0] + sx0, p[1] + sy0), s, tt.shape)
    v, p, s, sh = best
    dx = p[0] + sh[1] / 2 - (x0 + x1) / 2; dy = p[1] + sh[0] / 2 - (y0 + y1) / 2
    return dict(score=round(v, 3), dx=round(dx, 1), dy=round(dy, 1), scale=s,
                end_box=[int(p[0]), int(p[1]), int(p[0] + sh[1]), int(p[1] + sh[0])])


def at(A, B, box, m, r=3):
    """START's box compared with END where the group's move m puts it (+-r px): does this part ride with the group?"""
    import cv2
    x0, y0, x1, y1 = box; X0, Y0 = int(round(x0 + m[0])) - r, int(round(y0 + m[1])) - r
    win = B[max(0, Y0):Y0 + (y1 - y0) + 2 * r, max(0, X0):X0 + (x1 - x0) + 2 * r]
    t = A[y0:y1, x0:x1]
    if win.shape[0] < t.shape[0] or win.shape[1] < t.shape[1]:
        return dict(score=-1.0, end_box=shift_box(box, *m))
    res = cv2.matchTemplate(win, t, cv2.TM_CCOEFF_NORMED); _, v, _, p = cv2.minMaxLoc(res)
    bx, by = max(0, X0) + p[0], max(0, Y0) + p[1]
    return dict(score=round(float(v), 3), end_box=[bx, by, bx + x1 - x0, by + y1 - y0])


def sharp(G, box):
    import cv2, numpy as np
    x0, y0, x1, y1 = [int(v) for v in box]
    c = G[max(0, y0):y1, max(0, x0):x1].astype(np.float32)
    if c.size == 0:
        return 0.0
    gx, gy = cv2.Sobel(c, cv2.CV_32F, 1, 0), cv2.Sobel(c, cv2.CV_32F, 0, 1)
    return float(np.percentile(np.hypot(gx, gy), 99))


def shift_box(b, dx, dy):
    return [int(round(b[0] + dx)), int(round(b[1] + dy)), int(round(b[2] + dx)), int(round(b[3] + dy))]


# ---------------------------------------------------------------- the gate
class Rows(list):
    def add(self, key, ok, detail, **value):
        self.append(dict(key=key, ok=ok, detail=detail, **({"value": value} if value else {})))


def run(start, end, spec, outdir):
    import cv2, numpy as np
    sp = json.load(open(spec)); D = dict(DEFAULTS, **sp.get("bounds", {}))
    S, E = cv2.imread(start), cv2.imread(end)
    if S is None or E is None or S.shape != E.shape:
        raise SystemExit(f"cannot compare: {start} {None if S is None else S.shape} vs {end} {None if E is None else E.shape}")
    GS, GE = cv2.cvtColor(S, cv2.COLOR_BGR2GRAY), cv2.cvtColor(E, cv2.COLOR_BGR2GRAY)
    Hh, Ww = GS.shape
    rows = Rows(); draw = dict(boxes=[], lines=[], flags=[], hands=[])
    per = sp.get("person")
    pS = pE = None
    allowed = np.zeros((Hh, Ww), np.uint8)

    # ---- person
    if per:
        pS, pE = pose(S, per.get("side")), None
        pE = pose(E, pS["side"] if pS else per.get("side"))
        rows.add("person:found", bool(pS and pE), f"pose found START={bool(pS)} END={bool(pE)}"
                 + (f", side {pS['side']}, min visibility {pS['vis']:.2f}/{pE['vis']:.2f}" if pS and pE else ""))
        if pS and pE:
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51))
            allowed |= cv2.dilate(np.maximum(pS["mask"], pE["mask"]), k)
            g = per.get("guide")
            if g:
                for nm, p in (("START", pS), ("END", pE)):
                    d = dang(p["leg_deg"], line_deg(g["line"], p["A"], p["H"]))
                    rows.add(f"person:guide_{nm.lower()}", abs(d) <= g.get("max_deg", D["guide_max_deg"]),
                             f"{nm} hip-to-ankle line {p['leg_deg']:.1f} deg vs guide {line_deg(g['line'], p['A'], p['H']):.1f}: "
                             f"{d:+.1f} deg (max {g.get('max_deg', D['guide_max_deg'])})", deg=round(d, 1))
                draw["lines"].append(g["line"])
            ch = {b: pE[b] / pS[b] - 1 for b in ("torso", "thigh", "shin")}
            worst = max(ch, key=lambda b: abs(ch[b]))
            rows.add("person:bones", all(abs(v) <= D["bone_tol"] for v in ch.values()),
                     "bone length change START->END " + ", ".join(f"{b} {pS[b]:.0f}->{pE[b]:.0f} ({ch[b]:+.1%})" for b in ch)
                     + f"; worst {worst} (max {D['bone_tol']:.0%})", **{b: round(v, 3) for b, v in ch.items()})
            if per.get("reach", True):
                pred = math.sqrt(pS["thigh"] ** 2 + pS["shin"] ** 2 - 2 * pS["thigh"] * pS["shin"] * math.cos(math.radians(pE["knee"])))
                full = pS["thigh"] + pS["shin"]; err = pE["reach"] / pred - 1
                rows.add("person:reach", abs(err) <= D["reach_tol"] and pE["reach"] <= full * (1 + D["reach_tol"] / 2),
                         f"END hip-to-ankle {pE['reach']:.0f} px; START bones at END knee {pE['knee']:.0f} deg allow {pred:.0f} "
                         f"({err:+.1%}, max {D['reach_tol']:.0%}); fully straight {full:.0f} (+{D['reach_tol'] / 2:.0%} slack)",
                     err=round(err, 3))
            for j in per.get("anchored", []):
                jj = j if j in pS["pts"] else f"{pS['side']}_{j}"          # "hip" means the camera-near hip
                a_, b_ = pS["pts"][jj][:2], pE["pts"][jj][:2]; d = math.dist(a_, b_); lim = D["anchor_frac"] * pS["torso"]
                rows.add(f"person:anchored_{j}", d <= lim, f"{j} moved {d:.0f} px (max {lim:.0f}, {D['anchor_frac']:.0%} of torso)",
                         px=round(d, 1))
            rows.add("person:joints", 20 <= pS["knee"] <= 181 and 20 <= pE["knee"] <= 181 and 30 <= pS["hip_angle"] <= 200
                     and 30 <= pE["hip_angle"] <= 200,
                     f"knee {pS['knee']:.0f}->{pE['knee']:.0f}, hip {pS['hip_angle']:.0f}->{pE['hip_angle']:.0f} deg")

    # ---- rigid groups and their riders
    moves, extents = {}, []
    for grp in sp.get("rigid", []):
        # 1. free search for each part; 2. the group's move = median of the parts found with confidence (2+ needed);
        # 3. every part judged where that move puts it: still matches, still sharp. A footplate an image model redrew soft
        # fails at 3 (F5m) even when its own free search is inconclusive.
        n = grp["name"]; T = {p: track(GS, GE, b) for p, b in grp["parts"].items()}
        good = {p: t for p, t in T.items() if t["score"] >= D["min_score"]}
        M = np.array([[t["dx"], t["dy"]] for t in (good or T).values()]); m = np.median(M, 0); mag = float(np.hypot(*m))
        moves[n] = (m, mag)
        scores = ", ".join("%s %.2f" % (p, t["score"]) for p, t in T.items())
        rows.add(f"rigid:{n}.found", len(good) >= 2, f"{n}: {len(good)} of {len(T)} parts found with score >= {D['min_score']} "
                 f"({scores}); the group's move is "
                 f"their median ({m[0]:+.0f},{m[1]:+.0f}) = {mag:.0f} px")
        strong = [t for t in good.values() if t["score"] >= 0.9]
        Gd = np.array([[t["dx"], t["dy"]] for t in strong]) if strong else np.zeros((0, 2))
        spread = float(np.max(np.hypot(*(Gd - m).T))) if len(strong) >= 2 else 0.0
        lim = max(D["rigid_disagree_px"], D["rigid_disagree_frac"] * mag)
        rows.add(f"rigid:{n}.together", spread <= lim, f"{n}: the {len(strong)} strongly matched parts (>= 0.9) disagree with the "
                 f"group's move by up to {spread:.0f} px (max {lim:.0f})" + ("" if len(strong) >= 2 else
                 "; fewer than 2 strong parts, so each part is judged at the group's move below"),
                 spread=round(spread, 1), move=round(mag, 1))
        for p, b in grp["parts"].items():
            pb = shift_box(b, *m)
            if pb[0] < 0 or pb[1] < 0 or pb[2] > Ww or pb[3] > Hh:
                rows.add(f"rigid:{n}.{p}", True, f"{n}.{p}: the group's move takes it past the frame edge; not judged here "
                         f"(the reviewer checks it)")
                continue
            r_ = at(GS, GE, b, m); ratio = sharp(GE, r_["end_box"]) / max(1e-6, sharp(GS, b))
            ok = r_["score"] >= D["ride_score"] and ratio >= D["min_sharp"]
            draw["boxes"].append((b, r_["end_box"], ok, f"{n}.{p}"))
            rows.add(f"rigid:{n}.{p}", ok, f"{n}.{p} where the group's move puts it: match {r_['score']:.2f} (min {D['ride_score']}), "
                     f"sharpness END/START {ratio:.2f} (min {D['min_sharp']}); own search ({T[p]['dx']:+.0f},{T[p]['dy']:+.0f}) "
                     f"score {T[p]['score']:.2f}", score=r_["score"], sharp=round(ratio, 2))
        lo, hi = grp.get("move_px", [3, 1e9])
        rows.add(f"rigid:{n}.distance", lo <= mag <= hi, f"{n} moved {mag:.0f} px (allowed {lo} to {hi:g})")
        if grp.get("guide"):
            tr = ang((0, 0), (m[0], m[1])); gd = line_deg(grp["guide"], (m[0], m[1]), (0, 0)); d = dang(tr, gd)
            rows.add(f"rigid:{n}.guide", abs(d) <= grp.get("max_deg", D["guide_travel_deg"]),
                     f"{n} travel {tr:.1f} deg vs guide {gd:.1f}: {d:+.1f} (max {grp.get('max_deg', D['guide_travel_deg'])})",
                     deg=round(d, 1))
            draw["lines"].append(grp["guide"])
        if grp.get("extent"):
            extents.append((grp["extent"], m))
    for c in sp.get("contacts", []):
        t = track(GS, GE, c["box"]); m, mag = moves.get(c["rides"], (np.zeros(2), 0.0))
        slip = math.hypot(t["dx"] - m[0], t["dy"] - m[1]); lim = c.get("max_slip_px", D["contact_slip_px"])
        ok = slip <= lim and t["score"] >= D["contact_min_score"]
        draw["boxes"].append((c["box"], t["end_box"], ok, c["name"]))
        rows.add(f"contact:{c['name']}", ok, f"{c['name']} moved ({t['dx']:+.0f},{t['dy']:+.0f}) score {t['score']:.2f} "
                 f"(min {D['contact_min_score']}); "
                 f"{c['rides']} moved ({m[0]:+.0f},{m[1]:+.0f}); slip {slip:.0f} px (max {lim:g})", slip=round(slip, 1))
        for b in (c["box"], t["end_box"]):
            allowed[max(0, b[1] - 6):b[3] + 6, max(0, b[0] - 6):b[2] + 6] = 1

    # ---- still parts
    for n, b in sp.get("still", {}).items():
        t = track(GS, GE, b, R=120); d = math.hypot(t["dx"], t["dy"])
        ok = d <= D["still_px"] and t["score"] >= D["min_score"]
        draw["boxes"].append((b, t["end_box"], ok, n))
        rows.add(f"still:{n}", ok, f"{n} moved ({t['dx']:+.0f},{t['dy']:+.0f}) = {d:.0f} px (max {D['still_px']:g}), "
                 f"score {t['score']:.2f}", px=round(d, 1))

    # ---- props held in a hand
    for pr in sp.get("props", []):
        b = pr["box"]; x0, y0, x1, y1 = b; n = pr["name"]
        for bb in (b,):
            allowed[max(0, y0 - 10):y1 + 10, max(0, x0 - 10):x1 + 10] = 1
        if not (pS and pE and pr.get("held_by")):
            continue
        w = f"{pr['held_by']}_wrist"; wS, wE = pS["pts"][w][:2], pE["pts"][w][:2]
        cS = ((x0 + x1) / 2, (y0 + y1) / 2); near = math.dist(wS, cS) <= 0.6 * pS["torso"]
        rows.add(f"prop:{n}.in_hand_start", near, f"{n} centre {math.dist(wS, cS):.0f} px from the {pr['held_by']} wrist in START "
                 f"(max {0.6 * pS['torso']:.0f})")
        hand_moved = math.dist(wS, wE)
        eq = np.abs(GS[y0:y1, x0:x1].astype(int) - GE[y0:y1, x0:x1].astype(int)) <= 6; h, w = eq.shape
        halves = {"top": eq[:h // 2], "bottom": eq[h // 2:], "left": eq[:, :w // 2], "right": eq[:, w // 2:]}
        part, same = max(((k, float(v.mean())) for k, v in halves.items()), key=lambda kv: kv[1])
        left = hand_moved > 0.2 * pS["torso"] and same >= D["prop_leftover"]
        draw["boxes"].append((b, b, not left, f"{n} (START place)"))
        rows.add(f"prop:{n}.nothing_left", not left, f"the {pr['held_by']} hand moved {hand_moved:.0f} px; the {part} half of the "
                 f"{n}'s START box is {same:.0%} unchanged in END (whole box {float(eq.mean()):.0%}; a leftover at >= "
                 f"{D['prop_leftover']:.0%})", same=round(same, 2))
        # where is the hand now: it must still be near something that looks like the prop (the reviewer checks the grip)
        allowed[max(0, int(wE[1] - 0.6 * pS["torso"])):int(wE[1] + 0.6 * pS["torso"]),
                max(0, int(wE[0] - 0.6 * pS["torso"])):int(wE[0] + 0.6 * pS["torso"])] = 1
    for b in sp.get("may_change", {}).values():
        allowed[max(0, b[1]):b[3], max(0, b[0]):b[2]] = 1

    # ---- static: everything else must be unchanged. Inside a rigid group's extent an END pixel may also be START moved by
    # the group's move (the sled itself), or background the group uncovered (START sled pixels it left).
    if sp.get("static", True):
        a, c = cv2.GaussianBlur(GS, (3, 3), 0).astype(np.int16), cv2.GaussianBlur(GE, (3, 3), 0).astype(np.int16)

        def mdiff(sh):          # |END(x) - START(x - sh)|, tolerant of +-1 px
            dx0, dy0 = int(round(sh[0])), int(round(sh[1])); out = np.full(a.shape, 255, np.int16)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    out = np.minimum(out, np.abs(c - np.roll(np.roll(a, dy0 + dy, 0), dx0 + dx, 1)))
            return out
        diff = mdiff((0, 0)); tol = D["static_tol"]
        for ext, m in extents:
            x0, y0, x1, y1 = ext; X1, Y1 = shift_box(ext, *m)[2:]
            box = np.zeros_like(allowed); box[max(0, min(y0, y0 + int(m[1]))):max(y1, Y1), max(0, min(x0, x0 + int(m[0]))):max(x1, X1)] = 1
            d1 = mdiff(m)
            # START pixels that belong to the moving piece: they reappear moved by m, and not in place
            dS = np.full(a.shape, 255, np.int16)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    dS = np.minimum(dS, np.abs(a - np.roll(np.roll(c, -int(round(m[1])) + dy, 0), -int(round(m[0])) + dx, 1)))
            piece = ((dS <= tol) & (np.abs(a - c) > tol) & (box > 0)).astype(np.uint8)
            piece = cv2.morphologyEx(piece, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
            cn, _ = cv2.findContours(piece, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            piece = cv2.drawContours(np.zeros_like(piece), cn, -1, 1, -1)
            moved = np.roll(np.roll(piece, int(round(m[1])), 0), int(round(m[0])), 1)
            uncovered = cv2.dilate(piece & (moved == 0), np.ones((5, 5), np.uint8))
            diff = np.where(box > 0, np.where((d1 <= tol) | (uncovered > 0), 0, np.minimum(diff, d1)), diff)
        ch = ((diff > tol) & (allowed == 0)).astype(np.uint8)
        ch = cv2.morphologyEx(ch, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n_, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(ch, np.ones((9, 9), np.uint8)))
        blobs = [[int(st[i, 0]), int(st[i, 1]), int(st[i, 0] + st[i, 2]), int(st[i, 1] + st[i, 3])]
                 for i in range(1, n_) if int(ch[lab == i].sum()) >= D["static_min_area"]]
        blobs.sort(key=lambda bb: -(bb[2] - bb[0]) * (bb[3] - bb[1]))
        draw["flags"] += blobs
        frac = float(ch[allowed == 0].mean()) if (allowed == 0).any() else 0.0
        rows.add("static", not blobs, f"{frac:.2%} of the {float((allowed == 0).mean()):.0%} of the picture that must stand still "
                 f"changed; {len(blobs)} region(s) of {D['static_min_area']}+ px" + (f": {blobs[:6]}" if blobs else ""),
                 regions=blobs[:12])

    # ---- hands, for the reviewer's eyes
    if pS and pE:
        for nm, img, p in (("START", S, pS), ("END", E, pE)):
            for s in ("left", "right"):
                x, y, v = p["pts"][f"{s}_wrist"]; r = int(0.3 * pS["torso"])
                if v > 0.3:
                    draw["hands"].append((f"{nm} {s} hand", img[max(0, int(y) - r):int(y) + r, max(0, int(x) - r):int(x) + r]))
    sheet = evidence(S, E, pS, pE, draw, rows, outdir, os.path.splitext(os.path.basename(end))[0])
    return rows, sheet


def evidence(S, E, pS, pE, draw, rows, outdir, stem):
    """One JPEG: START | END with skeletons, guide lines, part boxes (green found, red not), flagged static regions,
    the hand crops at 3x, and the failed rows. For the reviewer and the page."""
    import cv2, numpy as np
    os.makedirs(outdir, exist_ok=True)
    out = []
    for nm, img, p in (("START", S, pS), ("END", E, pE)):
        o = img.copy()
        for l in draw["lines"]:
            x1, y1, x2, y2 = l; dx, dy = x2 - x1, y2 - y1; k = 3 * max(o.shape) / max(1e-6, math.hypot(dx, dy))
            cv2.line(o, (int(x1 - dx * k), int(y1 - dy * k)), (int(x1 + dx * k), int(y1 + dy * k)), (255, 140, 0), 2)
        if p:
            for a, b in ((p["S"], p["H"]), (p["H"], p["K"]), (p["K"], p["A"])):
                cv2.line(o, tuple(map(int, a)), tuple(map(int, b)), (0, 255, 255), 4)
        for bS, bE, ok, _ in draw["boxes"]:
            b = bS if nm == "START" else bE
            cv2.rectangle(o, (b[0], b[1]), (b[2], b[3]), (0, 200, 0) if ok else (0, 0, 255), 2)
        if nm == "END":
            for b in draw["flags"]:
                cv2.rectangle(o, (b[0], b[1]), (b[2], b[3]), (255, 0, 255), 3)
        cv2.putText(o, nm, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        out.append(o)
    top = np.hstack(out)

    def strip(tiles, h):                       # one row of labelled tiles, wrapped to the sheet's width
        rows_, cur, w = [], [], 0
        for lab, t in tiles:
            t = cv2.resize(t, (max(1, int(t.shape[1] * h / t.shape[0])), h), interpolation=cv2.INTER_CUBIC)
            t = cv2.copyMakeBorder(t, 28, 4, 4, 4, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            cv2.putText(t, lab[:40], (4, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 200), 2)
            if cur and w + t.shape[1] > top.shape[1]:
                rows_.append(cur); cur, w = [], 0
            cur.append(t); w += t.shape[1]
        if cur:
            rows_.append(cur)
        return [np.pad(np.hstack(r)[:, :top.shape[1]], ((0, 0), (0, max(0, top.shape[1] - sum(x.shape[1] for x in r))), (0, 0)),
                       constant_values=255) for r in rows_]
    hands = [(lab, c) for lab, c in draw["hands"] if c.size]
    zooms = []
    for bS, bE, ok, lab in draw["boxes"]:
        if not ok:
            for nm, img, b in (("START", S, bS), ("END", E, bE)):
                x0, y0, x1, y1 = [int(v) for v in b]; pd = 24
                c = img[max(0, y0 - pd):y1 + pd, max(0, x0 - pd):x1 + pd].copy()
                cv2.rectangle(c, (min(pd, x0), min(pd, y0)), (min(pd, x0) + x1 - x0, min(pd, y0) + y1 - y0), (0, 0, 255), 1)
                zooms.append((f"{lab} {nm}", c))
    parts = [top] + (strip(hands, 300) if hands else []) + (strip(zooms[:12], 260) if zooms else [])
    top = np.vstack(parts)
    fails = [r for r in rows if not r["ok"]]
    pad = np.full((40 + 34 * max(1, len(fails)), top.shape[1], 3), 255, np.uint8)
    for i, r in enumerate(fails or [dict(key="ALL ROWS PASS", detail="")]):
        cv2.putText(pad, (r["key"] + "  " + r["detail"])[:150], (10, 32 + 34 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 0, 200), 2)
    path = os.path.join(outdir, f"{stem}.framecheck.jpg")
    cv2.imwrite(path, np.vstack([top, pad]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    return path


# ---------------------------------------------------------------- stamps
def stamp_path(end):
    return end + STAMP_SUFFIX


def load_stamp(start, end):
    p = stamp_path(end)
    if not os.path.exists(p):
        return None, f"no frame-gate stamp: run _shared/framecheck/gate.py {start} {end} --spec SPEC"
    return json.load(open(p)), None


def require_pass(start, end, quiet=False):
    """For callers: raise unless this exact START/END pair passed the gate at this version AND a fresh reviewer passed it."""
    d, err = load_stamp(start, end)
    if err:
        raise SystemExit(err)
    probs = []
    if d.get("gate_version") != GATE_VERSION:
        probs.append(f"stamp is gate {d.get('gate_version')}, this is {GATE_VERSION}: re-gate")
    if d.get("start_sha256") != sha256(start) or d.get("end_sha256") != sha256(end):
        probs.append("the frames changed since they were gated (sha256 differs): re-gate and re-review")
    if d.get("spec_sha256") and os.path.exists(d.get("spec", "")) and d["spec_sha256"] != sha256(d["spec"]):
        probs.append("the spec changed since the gate ran: re-gate")
    if d.get("verdict") != "PASS":
        probs.append(f"gate verdict {d.get('verdict')}: " + "; ".join(r["key"] for r in d.get("rows", []) if not r["ok"]))
    rv = d.get("review") or {}
    if rv.get("verdict") != "PASS":
        probs.append("no frame-reviewer PASS recorded (gate.py START END --review REVIEW.md)" if not rv
                     else f"frame-reviewer verdict {rv.get('verdict')} ({rv.get('file')})")
    elif rv.get("start_sha256") != d.get("start_sha256") or rv.get("end_sha256") != d.get("end_sha256"):
        probs.append("the review was of different frames")
    if probs:
        raise SystemExit(f"frame gate REFUSES {os.path.basename(start)} -> {os.path.basename(end)}:\n  - " + "\n  - ".join(probs))
    if not quiet:
        print(f"frame gate {GATE_VERSION}: PASS + reviewer PASS ({os.path.basename(start)} -> {os.path.basename(end)})")
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("start"); ap.add_argument("end")
    ap.add_argument("--spec"); ap.add_argument("--out", help="evidence folder (default: framecheck/ next to END)")
    ap.add_argument("--review", help="the frame-reviewer's review file; its last 'VERDICT:' line is recorded")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--no-stamp", action="store_true", help="measure only (proof runs)")
    ap.add_argument("--json", help="also write the result here")
    a = ap.parse_args()
    if a.verify:
        require_pass(a.start, a.end); return 0
    if a.review:
        d, err = load_stamp(a.start, a.end)
        if err:
            raise SystemExit(err)
        if d.get("start_sha256") != sha256(a.start) or d.get("end_sha256") != sha256(a.end):
            raise SystemExit("these frames are not the ones gated; re-run the gate first")
        txt = open(a.review).read()
        v = re.findall(r"VERDICT:\s*\**\s*(PASS|FAIL)", txt)
        if not v:
            raise SystemExit("no 'VERDICT: PASS' or 'VERDICT: FAIL' line in the review")
        d["review"] = dict(verdict=v[-1], file=os.path.abspath(a.review), sha256=sha256(a.review),
                           start_sha256=d["start_sha256"], end_sha256=d["end_sha256"], when=time.strftime("%Y-%m-%dT%H:%M:%S%z"))
        json.dump(d, open(stamp_path(a.end), "w"), indent=1)
        print(f"reviewer verdict {v[-1]} recorded in {os.path.basename(stamp_path(a.end))}")
        return 0 if v[-1] == "PASS" else 1
    if not a.spec:
        ap.error("--spec is required to run the gate")
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.end)), "framecheck")
    rows, sheet = run(a.start, a.end, a.spec, out)
    verdict = "PASS" if all(r["ok"] for r in rows) else "FAIL"
    for r in rows:
        print(f"  {'PASS' if r['ok'] else 'FAIL'}  {r['key']:<28} {r['detail']}")
    print(f"VERDICT {verdict}  (gate {GATE_VERSION}; evidence {sheet})")
    d = dict(gate_version=GATE_VERSION, verdict=verdict, start=os.path.abspath(a.start), end=os.path.abspath(a.end),
             start_sha256=sha256(a.start), end_sha256=sha256(a.end), spec=os.path.abspath(a.spec), spec_sha256=sha256(a.spec),
             evidence=sheet, when=time.strftime("%Y-%m-%dT%H:%M:%S%z"), rows=rows)
    if a.json:
        json.dump(d, open(a.json, "w"), indent=1)
    if not a.no_stamp:
        json.dump(d, open(stamp_path(a.end), "w"), indent=1)   # a new gate run clears any earlier review
        print(f"  stamp -> {stamp_path(a.end)}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    try:                                                     # the render queue (VIDEO-RULES, "Video builds")
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renderq"))
        from renderq import slot as _queue
    except Exception:
        from contextlib import nullcontext
        _queue = lambda *a, **k: nullcontext()               # noqa: E731
    with _queue("frame check " + os.path.basename(sys.argv[1] if len(sys.argv) > 1 else ""), pool="light"):
        sys.exit(main())
