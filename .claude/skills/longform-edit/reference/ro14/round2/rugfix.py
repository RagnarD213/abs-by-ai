"""A1 (the broken scale): the rug at bottom left redraws its pile texture frame to frame (A1 t1 reviewer: 14x the floor's
frame-to-frame change). The camera is locked, so the rug is held still: every frame takes the rug from one clean reference
frame inside a feathered mask, only where no person is (mediapipe selfie mask, dilated). usage: rugfix.py IN.mp4 OUT.mp4 REF_FRAME"""
import sys, subprocess, numpy as np, cv2
import mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
src, out, ref_i = sys.argv[1], sys.argv[2], int(sys.argv[3])
W, H = 1920, 1080
RUG = (180, 860, 720, 1080)                          # x0, y0, x1, y1 (1920x1080)
dec = subprocess.Popen([FF, "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
frames = []
while True:
    b = dec.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    frames.append(np.frombuffer(b, np.uint8).reshape(H, W, 3).copy())
ref = frames[ref_i]
m = np.zeros((H, W), np.float32); x0, y0, x1, y1 = RUG; m[y0:y1, x0:x1] = 1
m = cv2.GaussianBlur(m, (0, 0), 18)
seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "24", "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                        "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
worst = 0.0
for f in frames:
    p = seg.process(f).segmentation_mask > 0.3
    p = cv2.dilate(p.astype(np.uint8), np.ones((41, 41), np.uint8)).astype(np.float32)
    p = cv2.GaussianBlur(p, (0, 0), 8)
    a = (m * (1 - p))[..., None]
    worst = max(worst, float((m * p).max()))
    enc.stdin.write((f * (1 - a) + ref * a).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()
print("rugfix", out, "frames", len(frames), "max person overlap in rug mask", round(worst, 3))
