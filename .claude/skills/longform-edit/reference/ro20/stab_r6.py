"""RO-20C round 6: lock a Veo take's slow camera creep to its first frame (the round 6 reviewers suggested "a stabilize-to-f0
pass in the edit" for takes the motion gate failed only on camera drift). Per frame: ORB features on the background (people
masked out with MediaPipe selfie segmentation), a similarity transform to frame 0 (RANSAC), warp, then a small fixed zoom so no
border shows. The person is moved with the frame, exactly as the camera moved him; nothing inside the picture is redrawn.
usage: stab_r6.py IN.mp4 OUT.mp4 [first_frame=0] [count=all] [zoom=1.02]"""
import subprocess, sys
import cv2, numpy as np, mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"

if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    f0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; cnt = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
    zoom = float(sys.argv[5]) if len(sys.argv) > 5 else 1.02
    cap = cv2.VideoCapture(src); cap.set(1, f0); w, h = int(cap.get(3)), int(cap.get(4)); fps = cap.get(5)
    seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1); orb = cv2.ORB_create(4000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    Z = cv2.getRotationMatrix2D((w / 2, h / 2), 0, zoom); Z = np.vstack([Z, [0, 0, 1]])
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-",
                            "-c:v", "libx264", "-crf", "10", "-preset", "slow", "-pix_fmt", "yuv420p",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
    ref = None; n = 0; worst = 0.0
    while n < cnt:
        ok, fr = cap.read()
        if not ok: break
        m = seg.process(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).segmentation_mask
        bg = (cv2.dilate((m > 0.3).astype(np.uint8), np.ones((41, 41), np.uint8)) == 0).astype(np.uint8) * 255
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY); kp, de = orb.detectAndCompute(g, bg)
        if ref is None:
            ref = (kp, de); M = np.eye(3)
        else:
            mt = sorted(bf.match(de, ref[1]), key=lambda x: x.distance)[:800]
            a = np.float32([kp[x.queryIdx].pt for x in mt]); b = np.float32([ref[0][x.trainIdx].pt for x in mt])
            A, _ = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=2.0)
            M = np.vstack([A, [0, 0, 1]]) if A is not None else np.eye(3)
            worst = max(worst, float(np.abs(M[:2, 2]).max()), float(abs(np.hypot(M[0, 0], M[1, 0]) - 1) * w))
        fr2 = cv2.warpAffine(fr, (Z @ M)[:2], (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
        enc.stdin.write(fr2.tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    print(out, n, "frames; largest correction", round(worst, 1), "px")
