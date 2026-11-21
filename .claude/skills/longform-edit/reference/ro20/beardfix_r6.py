"""RO-20C round 6: keep a lip sync's mouth, put the original take's sharp beard back (the round 6 reviewer on E2-sync1: the
timing passed but sync/lipsync-2-pro smeared the beard around the mouth and chin to 0.11 to 0.28 of the take's sharpness).
Per frame: MediaPipe face mesh on the SYNCED frame gives the outer lip contour; the synced pixels are kept only inside that
contour (dilated a little, feathered), everything else is the unsynced trim the sync was made from (same frames, same size).
usage: beardfix_r6.py SYNCED.mp4 TRIM.mp4 OUT.mp4 [dilate_px=10] [feather_px=6]"""
import subprocess, sys
import cv2, numpy as np, mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
LIPS = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146]   # outer lip ring

if __name__ == "__main__":
    syn, trim, out = sys.argv[1:4]
    dil = int(sys.argv[4]) if len(sys.argv) > 4 else 10; fea = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    a, b = cv2.VideoCapture(syn), cv2.VideoCapture(trim)
    w, h = int(a.get(3)), int(a.get(4)); n = int(min(a.get(7), b.get(7)))
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "24", "-i", "-",
                            "-c:v", "libx264", "-crf", "10", "-preset", "slow", "-pix_fmt", "yuv420p",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
    fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dil + 1, 2 * dil + 1)); miss = 0
    for i in range(n):
        ok1, fs = a.read(); ok2, ft = b.read()
        if not (ok1 and ok2): break
        r = fm.process(cv2.cvtColor(fs, cv2.COLOR_BGR2RGB)); m = np.zeros((h, w), np.uint8)
        if r.multi_face_landmarks:
            L = r.multi_face_landmarks[0].landmark
            cv2.fillPoly(m, [np.array([[int(L[j].x * w), int(L[j].y * h)] for j in LIPS], np.int32)], 255)
            m = cv2.dilate(m, k)
        else: miss += 1
        al = cv2.GaussianBlur(m, (0, 0), fea).astype(np.float32)[..., None] / 255
        enc.stdin.write((fs * al + ft * (1 - al)).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    print(out, n, "frames; no face on", miss)
