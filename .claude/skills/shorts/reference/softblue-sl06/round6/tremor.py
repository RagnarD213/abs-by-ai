"""Tremor-only measure (SL-06 R6, 2026-10-21). Smooth motion (a sway, a head turn, talking) is not tremor; shaking is
fast back-and-forth. For each tracked point, hf = RMS of x[t] - (x[t-1] + x[t+1]) / 2 (the frame-to-frame wobble that a
smooth path does not have), in px at 1080x1920, over the clip's first N frames.
Tracks: nose (MediaPipe face mesh) and the median optical flow inside each --box (a fist, a vial hand).
  python3 tremor.py CLIP N [--box name:x,y,w,h ...]"""
import sys, argparse, cv2, numpy as np, mediapipe as mp


def hf(P):
    P = np.asarray(P, float); d = P[1:-1] - (P[:-2] + P[2:]) / 2
    return float(np.sqrt((np.linalg.norm(d, axis=1) ** 2).mean()))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("clip"); ap.add_argument("n", type=int); ap.add_argument("--box", action="append", default=[])
    a = ap.parse_args(); cap = cv2.VideoCapture(a.clip); F = []
    while len(F) < a.n:
        ok, f = cap.read()
        if not ok: break
        F.append(cv2.resize(f, (1080, 1920), interpolation=cv2.INTER_AREA))
    out = {}
    N = []
    with mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) as fm:
        for f in F:
            r = fm.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            if r.multi_face_landmarks:
                L = r.multi_face_landmarks[0].landmark; N.append((L[1].x * 1080, L[1].y * 1920))
    if len(N) > 5: out["nose"] = hf(N)
    with mp.solutions.face_mesh.FaceMesh(static_image_mode=True) as fm:      # head box from the first frame, tracked by flow
        r = fm.process(cv2.cvtColor(F[0], cv2.COLOR_BGR2RGB))
        if r.multi_face_landmarks:
            xs = [p.x * 1080 for p in r.multi_face_landmarks[0].landmark]; ys = [p.y * 1920 for p in r.multi_face_landmarks[0].landmark]
            a.box.insert(0, f"head:{int(min(xs))},{int(min(ys))},{int(max(xs) - min(xs))},{int(max(ys) - min(ys))}")
    G = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in F]
    for b in a.box:
        name, xywh = b.split(":"); x, y, w, h = map(int, xywh.split(",")); pos = [np.zeros(2)]; cx, cy = float(x), float(y)
        for p, q in zip(G, G[1:]):
            X, Y = int(round(cx)), int(round(cy)); X = min(max(X, 0), 1080 - w); Y = min(max(Y, 0), 1920 - h)
            fl = cv2.calcOpticalFlowFarneback(p[Y:Y + h, X:X + w], q[Y:Y + h, X:X + w], None, 0.5, 3, 21, 3, 5, 1.1, 0)
            v = np.median(fl.reshape(-1, 2), 0); pos.append(pos[-1] + v); cx += v[0]; cy += v[1]
        out[name] = hf(pos)
    print(a.clip.split("/")[-1], "  ".join(f"{k} {v:.2f}" for k, v in out.items()))
    return out


if __name__ == "__main__":
    main()
