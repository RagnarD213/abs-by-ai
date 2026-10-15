#!/usr/bin/env python3
"""prep_clips.py ID=TAKE:A:B ... -> motion/final/<ID>.mp4 (take frames A..B inclusive, 24 fps, black rows cropped if Veo left
any) and motion/final/chips.json: for each clip, the AI-GENERATED chip corner (top left or top right) whose box never touches a
face or a person's head on any sampled frame. Refuses a range the motion gate + reviewer have not passed (clipcheck --verify)."""
import sys, json, subprocess, os
import numpy as np, cv2, mediapipe as mp
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"; R3 = "/Volumes/Extreme/_edit_work/RO-17/round3"
FF = REPO + "/Media/video_edit/bin/ffmpeg"
sys.path.insert(0, REPO + "/.claude/skills/_shared/framecheck")
CHIPS = {"rt": ((1866, 54), "rt", (1866 - 330, 30, 1890, 100)), "lt": ((54, 54), "lt", (30, 30, 54 + 330, 100))}

def frames(path):
    b = subprocess.run([FF, "-v", "error", "-i", path, "-vf", "scale=1920:1080:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, 1080, 1920, 3)

def black_rows(f):
    g = f.mean(axis=(0, 2, 3)); top = 0
    while top < 12 and g[top] < 6: top += 1
    bot = 0
    while bot < 12 and g[-1 - bot] < 6: bot += 1
    return top, bot

def heads(fr):
    out = []
    with mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.4) as D:
        for f in fr:
            r = D.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            for d in (r.detections or []):
                b = d.location_data.relative_bounding_box
                x0, y0, w, h = b.xmin * 1920, b.ymin * 1080, b.width * 1920, b.height * 1080
                out.append((x0 - 0.4 * w, y0 - 0.8 * h, x0 + 1.4 * w, y0 + 1.3 * h))   # face grown to the whole head and hair
    return out

def hit(a, b): return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])

if __name__ == "__main__":
    from clipcheck import require_pass
    os.makedirs(f"{R3}/motion/final", exist_ok=True)
    cj = f"{R3}/motion/final/chips.json"; chips = json.load(open(cj)) if os.path.exists(cj) else {}
    for arg in sys.argv[1:]:
        cid, spec = arg.split("="); tid, a, b = spec.split(":"); a, b = int(a), int(b)
        take = f"{R3}/motion/takes/{tid}.mp4"
        require_pass(take, frames=(a, b))
        F = frames(take)[a:b + 1]; top, bot = black_rows(F)
        vf = (f"crop=1920:{1080 - top - bot}:0:{top},scale=1920:1080:flags=lanczos," if top or bot else "") + "scale=1920:1080:flags=lanczos,format=yuv420p"
        w = int(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                                "-of", "csv=p=0", take], capture_output=True, text=True).stdout.strip())
        if w < 1920: vf = vf.replace("format=yuv420p", "unsharp=5:5:0.6:5:5:0.0,format=yuv420p")   # 720p Kling takes: a light sharpen after the upscale (A5/A7 reviewers)
        out = f"{R3}/motion/final/{cid}.mp4"
        subprocess.run([FF, "-v", "error", "-y", "-i", take, "-vf", f"select='between(n\\,{a}\\,{b})',setpts=N/24/TB," + vf, "-r", "24",
                        "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-colorspace", "bt709", "-color_primaries", "bt709",
                        "-color_trc", "bt709", "-an", out], check=True)
        H = heads(F[::4])
        free = [k for k, (_, _, box) in CHIPS.items() if not any(hit(box, h) for h in H)]
        pick = "rt" if "rt" in free else ("lt" if "lt" in free else None)
        chips[cid] = dict(take=tid, frames=[a, b], black_rows=[top, bot], n=len(F), secs=round(len(F) / 24, 3),
                          chip=[list(CHIPS[pick][0]), CHIPS[pick][1]] if pick else None, heads_seen=len(H), free=free)
        print(cid, json.dumps(chips[cid]), flush=True)
        assert pick, f"{cid}: no corner clear of every head; place the chip by hand"
    json.dump(chips, open(cj, "w"), indent=1)
