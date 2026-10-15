"""Self-change map (ro08/a5_cut.py's test) over windows of any clip: things that change AWAY from the man (appear, vanish, drift).
For each window, frame a against frame a+step: each pixel against the range its 7x7 neighbourhood takes on the other frame, outside
the biggest connected change (the man) grown by 40 px. usage: selfchange04.py CLIP OUTDIR a:b[:step] ...  -> OUTDIR/selfchange_a_b.jpg"""
import sys, os, json, subprocess, cv2, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
clip, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
raw = subprocess.run([FF, "-v", "error", "-i", clip, "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=bgr24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
w, h = 1080, 1920; F = [np.frombuffer(raw[i:i+w*h*3], np.uint8).reshape(h, w, 3) for i in range(0, len(raw), w*h*3)]
k7 = np.ones((7, 7), np.uint8); rep = {}
for spec in sys.argv[3:]:
    p = [int(x) for x in spec.split(":")]; a, b = p[0], p[1]; st = p[2] if len(p) > 2 else 6
    heat = np.zeros((h, w), np.float32); blobs = []
    for i in range(a, b - st + 1, st):
        A = cv2.GaussianBlur(F[i], (0, 0), 1.5).astype(np.float32); B = cv2.GaussianBlur(F[i+st], (0, 0), 1.5).astype(np.float32)
        d = np.maximum(np.maximum(A - cv2.dilate(B, k7), cv2.erode(B, k7) - A), 0).max(2)
        r = (np.abs(A - B).max(2) > 14).astype(np.uint8); n, l, s, _ = cv2.connectedComponentsWithStats(r); man = np.zeros_like(r)
        if n > 1: man = cv2.dilate((l == 1 + int(np.argmax(s[1:, 4]))).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81)))
        m = ((d > 12) & (man == 0)).astype(np.uint8); n2, l2, s2, _ = cv2.connectedComponentsWithStats(m)
        blobs += [dict(frames=[i, i+st], area=int(s2[j, 4]), box=[int(v) for v in s2[j, :4]]) for j in range(1, n2) if s2[j, 4] >= 150]
        heat = np.maximum(heat, np.where(man > 0, 0, d))
    vis = cv2.addWeighted(cv2.cvtColor(np.clip(heat*8, 0, 255).astype(np.uint8), cv2.COLOR_GRAY2BGR), 0.8, F[a], 0.3, 0)
    cv2.imwrite(f"{out}/selfchange_{a}_{b}.jpg", cv2.resize(vis, (540, 960))); rep[spec] = sorted(blobs, key=lambda x: -x["area"])[:10]
    print(spec, "blobs >=150 px away from the man:", len(blobs), "largest:", rep[spec][:4])
json.dump(rep, open(f"{out}/selfchange.json", "w"), indent=1)
