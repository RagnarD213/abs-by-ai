"""Grab a dense set of moving-hand frames from the delivered film so the reviewer sees fingers, not just the worst edge of each shot."""
import json, subprocess, sys, numpy as np, cv2
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
runs = []
for i in range(6): runs += json.load(open(f"r3/full/c{i}.build.json"))["runs"]
P = [r for r in runs if r["kind"] == "presenter" and r["rect"][2] > 500]
OW, OH = 480, 270; rd = subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", "r3/full/film_silent.mp4", "-map", "0:v", "-vf", "scale=480:270", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
by = {}
for ri, r in enumerate(P):
    for f in range(r["f0"], r["f1"]): by[f] = ri
prev = None; best = {}; f = 0
while True:
    b = rd.stdout.read(OW * OH)
    if len(b) < OW * OH: break
    g = np.frombuffer(b, np.uint8).astype(np.float32)
    if prev is not None and f in by:
        r = P[by[f]]; g2 = g.reshape(OH, OW); p2 = prev.reshape(OH, OW); x, y, w, h = r["rect"]; X0 = max(0, x) // 4; X1 = min(1920, x + w) // 4
        m = float(np.abs(g2 - p2)[135:, X0:X1].mean())
        if m > best.get(by[f], (0, 0))[0] and r["f0"] + 2 < f < r["f1"] - 2: best[by[f]] = (m, f)
    prev = g; f += 1
pick = sorted(best.values(), reverse=True)[:60]; fr = sorted(x[1] for x in pick); json.dump(fr, open("r3/audit3/hand_frames.json", "w"))
tiles = []
for f in fr:
    raw = subprocess.run([FF, "-nostdin", "-v", "error", "-ss", f"{f * 1001 / 30000:.4f}", "-i", "r3/full/film_silent.mp4", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    img = np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3).copy(); r = next(q for q in P if q["f0"] <= f < q["f1"]); x, y, w, h = r["rect"]
    c = img[430:1080, max(0, x):min(1920, x + w)]; s = min(620 / c.shape[1], 440 / c.shape[0]); c = cv2.resize(c, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); t = np.full((440, 620, 3), 30, np.uint8); t[:c.shape[0], :c.shape[1]] = c
    tm = f * 1001 / 30000; cv2.putText(t, f"{int(tm // 60)}:{tm % 60:04.1f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 255, 255), 2); tiles.append(t)
for i in range(0, len(tiles), 9):
    T = tiles[i:i + 9] + [np.zeros((440, 620, 3), np.uint8)] * (9 - len(tiles[i:i + 9]))
    cv2.imwrite(f"r3/audit3/hands{i // 9:02d}.jpg", np.vstack([np.hstack(T[j:j + 3]) for j in (0, 3, 6)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print(len(fr))
