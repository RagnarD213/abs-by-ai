#!/usr/bin/env python3
"""Do parts that should move as one rigid piece move together, and along the guide? (AI start/end frame physics check)

usage: rigid.py START END --part name:x0,y0,x1,y1 [--part ...] [--still name:x0,y0,x1,y1 ...] [--guide x1,y1,x2,y2]
Each --part box is cut from START and found in END by normalized cross-correlation (a search over 0.85-1.15 scale).
Prints each part's displacement, the spread between parts (rigid pieces should agree within a few percent of the move),
the angle of travel against --guide, and for --still boxes (frame, seat, background) how far they drifted (should be ~0).
Written 2026-10-14 for RA-04's leg press (Dan: the sled, platform and plates must move together; "the physics on this makes sense").
"""
import argparse, json, math
import cv2, numpy as np

def find(a, b, box, R=260):
    """Search only within R px of the part's START position (look-alike plates elsewhere in a gym fool a global search)."""
    x0, y0, x1, y1 = box; t = a[y0:y1, x0:x1]; best = None
    sx0, sy0 = max(0, x0 - R), max(0, y0 - R); win = b[sy0:min(b.shape[0], y1 + R), sx0:min(b.shape[1], x1 + R)]
    for s in np.linspace(0.94, 1.06, 7):
        tt = cv2.resize(t, None, fx=s, fy=s)
        if tt.shape[0] >= win.shape[0] or tt.shape[1] >= win.shape[1]: continue
        r = cv2.matchTemplate(win, tt, cv2.TM_CCOEFF_NORMED); _, v, _, p = cv2.minMaxLoc(r)
        if best is None or v > best[0]: best = (v, (p[0] + sx0, p[1] + sy0), s, tt.shape)
    v, p, s, sh = best
    cx0, cy0 = (x0 + x1) / 2, (y0 + y1) / 2; cx1, cy1 = p[0] + sh[1] / 2, p[1] + sh[0] / 2
    return {"score": round(float(v), 3), "dx": round(cx1 - cx0, 1), "dy": round(cy1 - cy0, 1), "scale": round(float(s), 3)}

def box(s):
    n, v = s.split(":"); return n, tuple(int(x) for x in v.split(","))

ap = argparse.ArgumentParser(); ap.add_argument("start"); ap.add_argument("end")
ap.add_argument("--part", action="append", default=[]); ap.add_argument("--still", action="append", default=[]); ap.add_argument("--guide")
a = ap.parse_args()
A = cv2.cvtColor(cv2.imread(a.start), cv2.COLOR_BGR2GRAY); B = cv2.cvtColor(cv2.imread(a.end), cv2.COLOR_BGR2GRAY)
out = {"parts": {}, "still": {}}
for s in a.part: n, b = box(s); out["parts"][n] = find(A, B, b)
for s in a.still: n, b = box(s); out["still"][n] = find(A, B, b)
if out["parts"]:
    D = np.array([[p["dx"], p["dy"]] for p in out["parts"].values()]); m = D.mean(0); mag = float(np.hypot(*m))
    out["move_px"] = round(mag, 1); out["parts_disagree_px"] = round(float(np.max(np.hypot(*(D - m).T))), 1)
    out["travel_deg"] = round(math.degrees(math.atan2(-m[1], m[0])), 1)
    if a.guide:
        x1, y1, x2, y2 = map(float, a.guide.split(",")); g = math.degrees(math.atan2(-(y2 - y1), x2 - x1))
        out["guide_deg"] = round(g, 1); out["travel_vs_guide_deg"] = round((out["travel_deg"] - g + 180) % 360 - 180, 1)
print(json.dumps(out, indent=1))
