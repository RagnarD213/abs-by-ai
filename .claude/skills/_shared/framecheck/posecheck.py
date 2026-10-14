#!/usr/bin/env python3
"""Measure a person's joint angles on an AI start/end frame and, for a machine exercise, check the push runs along the body.

usage: posecheck.py IMG [--rail auto|x1,y1,x2,y2] [--out overlay.jpg] [--json out.json]

Prints torso, thigh, shin and leg-line angles (degrees above horizontal, image coordinates flipped so up is positive), the hip
and knee angles, and with --rail the angle between the leg line (hip to ankle) and the machine's rail, plus how far the rail
line passes from the hip as a fraction of leg length. MediaPipe Pose (0.10.x, legacy solutions API), side nearest the camera.
Bone lengths (torso, thigh, shin) are printed so a start/end pair can be checked for limbs that grow or shrink between
frames (a 4th independent review caught a 24 % leg stretch the angles alone did not show).
Written 2026-10-14 after Dan rejected RA-04's leg press frames ("leg pressing at a 90 degree angle... No human body works like that").
"""
import argparse, json, math, sys
import cv2, numpy as np
import mediapipe as mp

def ang(p, q):                       # angle of the vector p->q above horizontal, degrees, -180..180
    return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0]))

def joint(a, b, c):                  # angle at b between b->a and b->c
    v1, v2 = np.subtract(a, b), np.subtract(c, b)
    return math.degrees(math.acos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9), -1, 1)))

def auto_rail(img, hip=None, ankle=None):
    """Longest straight edge (the chrome rails) that rises 20-80 degrees TOWARD the feet. A backrest rises toward the head,
    so with the hip and ankle known it is excluded (the first version picked the backrest on 2 of 3 frames)."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); e = cv2.Canny(g, 60, 160)
    L = cv2.HoughLinesP(e, 1, np.pi / 360, 120, minLineLength=int(0.18 * img.shape[0]), maxLineGap=12)
    best = None
    for x1, y1, x2, y2 in (L.reshape(-1, 4) if L is not None else []):
        if hip is not None and (x2 - x1) * (ankle[0] - hip[0]) < 0: x1, y1, x2, y2 = x2, y2, x1, y1
        a = ang((x1, y1), (x2, y2)) if hip is not None else abs(ang((x1, y1), (x2, y2)))
        if hip is None: a = a if a <= 90 else 180 - a
        n = math.hypot(x2 - x1, y2 - y1)
        if 20 <= a <= 80 and (best is None or n > best[0]): best = (n, (x1, y1, x2, y2))
    return best[1] if best else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("img"); ap.add_argument("--rail"); ap.add_argument("--out"); ap.add_argument("--json")
    a = ap.parse_args(); img = cv2.imread(a.img); H, W = img.shape[:2]
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=2, enable_segmentation=False) as P:
        r = P.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not r.pose_landmarks: print(json.dumps({"img": a.img, "ok": False, "why": "no person found"})); sys.exit(2)
    lm = r.pose_landmarks.landmark; L = mp.solutions.pose.PoseLandmark
    side = "LEFT" if sum(lm[getattr(L, f"LEFT_{j}")].visibility for j in ("HIP", "KNEE", "ANKLE")) >= \
                     sum(lm[getattr(L, f"RIGHT_{j}")].visibility for j in ("HIP", "KNEE", "ANKLE")) else "RIGHT"
    pt = lambda j: (lm[getattr(L, f"{side}_{j}")].x * W, lm[getattr(L, f"{side}_{j}")].y * H)
    vis = {j: round(lm[getattr(L, f"{side}_{j}")].visibility, 2) for j in ("SHOULDER", "HIP", "KNEE", "ANKLE")}
    S, Hp, K, A = pt("SHOULDER"), pt("HIP"), pt("KNEE"), pt("ANKLE")
    out = {"img": a.img, "ok": True, "side": side, "visibility": vis,
           "torso_deg": round(ang(Hp, S), 1), "thigh_deg": round(ang(Hp, K), 1), "shin_deg": round(ang(K, A), 1),
           "leg_line_deg": round(ang(Hp, A), 1), "hip_angle": round(joint(S, Hp, K), 1), "knee_angle": round(joint(Hp, K, A), 1),
           "torso_len": round(math.dist(S, Hp), 1), "thigh_len": round(math.dist(Hp, K), 1), "shin_len": round(math.dist(K, A), 1),
           "hip_to_ankle": round(math.dist(Hp, A), 1), "pts": {"shoulder": [round(v) for v in S], "hip": [round(v) for v in Hp],
           "knee": [round(v) for v in K], "ankle": [round(v) for v in A]}}
    rail = auto_rail(img, Hp, A) if a.rail == "auto" else (tuple(map(float, a.rail.split(","))) if a.rail else None)
    if rail:
        x1, y1, x2, y2 = rail
        if (x2 - x1) * (A[0] - Hp[0]) < 0: x1, y1, x2, y2 = x2, y2, x1, y1      # point the rail the same way as the legs
        ra = ang((x1, y1), (x2, y2)); d = (out["leg_line_deg"] - ra + 180) % 360 - 180
        legl = math.dist(Hp, A); n = np.array([y2 - y1, -(x2 - x1)]) / math.hypot(x2 - x1, y2 - y1)
        out.update({"rail": [round(v) for v in (x1, y1, x2, y2)], "rail_deg": round(ra, 1), "leg_vs_rail_deg": round(d, 1),
                    "rail_off_hip_legs": round(abs(np.dot(np.subtract(Hp, (x1, y1)), n)) / legl, 2)})
    if a.out:
        o = img.copy()
        for p, q in ((S, Hp), (Hp, K), (K, A)): cv2.line(o, tuple(map(int, p)), tuple(map(int, q)), (0, 255, 255), 6)
        for p in (S, Hp, K, A): cv2.circle(o, tuple(map(int, p)), 12, (0, 0, 255), -1)
        if rail:
            x1, y1, x2, y2 = rail; dx, dy = x2 - x1, y2 - y1; k = 3 * max(W, H) / math.hypot(dx, dy)
            cv2.line(o, (int(x1 - dx * k), int(y1 - dy * k)), (int(x1 + dx * k), int(y1 + dy * k)), (255, 120, 0), 3)
        cv2.putText(o, f"hip {out['hip_angle']:.0f}  knee {out['knee_angle']:.0f}  leg/rail {out.get('leg_vs_rail_deg', 'na')}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)
        cv2.imwrite(a.out, o)
    print(json.dumps(out))
    if a.json: json.dump(out, open(a.json, "w"), indent=1)

if __name__ == "__main__":
    main()
