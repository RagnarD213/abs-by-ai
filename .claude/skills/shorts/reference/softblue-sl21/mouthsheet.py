"""Mouth crops of a lip-synced clip every K frames, labelled with the word spoken at that time.  usage: mouthsheet.py CLIP.mp4 S SLOT_START_SHORT_T OUT [K]"""
import subprocess, sys, json, numpy as np, cv2
import mediapipe as mp
from PIL import Image, ImageDraw
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
clip, S, t0, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]; K = int(sys.argv[5]) if len(sys.argv) > 5 else 2; FPSV = float(sys.argv[6]) if len(sys.argv) > 6 else 24.0
words = json.load(open(f"/Users/danielrose/Projects/_edit_work/SL-21/build/{S}/words.json"))
raw = subprocess.run([FF, "-v", "error", "-i", clip, "-vf", "scale=1080:1920:in_color_matrix=bt709,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3); cells = []
with mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.4) as FM:
    for i in range(0, len(F), K):
        r = FM.process(F[i]); t = t0 + i / FPSV
        if not r.multi_face_landmarks: continue
        lm = r.multi_face_landmarks[0].landmark; cx, cy = lm[13].x * 1080, lm[13].y * 1920; w = abs(lm[291].x - lm[61].x) * 1080
        h = int(w * 1.1); x0, y0 = int(cx - h), int(cy - h * 0.8)
        c = Image.fromarray(F[i][max(0, y0):y0 + int(h * 1.6), max(0, x0):x0 + 2 * h]).resize((200, 160))
        wd = next((x["w"] for x in words if x["t"] - 0.02 <= t <= x["e"] + 0.02), "-")
        gap = abs(lm[14].y - lm[13].y) * 1920 / max(1.0, w)
        d = ImageDraw.Draw(c); d.rectangle((0, 0, 200, 15), fill="black"); d.text((3, 2), f"f{i} {t:.2f}s {wd[:14]} gap{gap:.2f}", fill="white"); cells.append(c)
cols = 10; rows = (len(cells) + cols - 1) // cols; Sh = Image.new("RGB", (cols * 202, rows * 162), "white")
for k, c in enumerate(cells): Sh.paste(c, ((k % cols) * 202, (k // cols) * 162))
Sh.save(out, quality=88); print(out, len(cells))
