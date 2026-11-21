#!/usr/bin/env python3
"""Where Dan's head is in the RAW roll, for the sheet's `framing[].head`: hair top, face centre x and chin, in raw
pixels. mediapipe full-range face detection for the face box; the Apple Vision person mask (shorts/reference/recentre/
personmask) for the hair top, read only inside the head band (face centre +- 0.6 face widths) so a raised hand is
never taken for hair. Used by the sheet writers when the build did not record these itself.

  measure(roll_path, [src_seconds, ...], workdir) -> {src_seconds: {hair_top, cx, chin, face_w} or None}
"""
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image

REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FF = f"{REPO}/Media/video_edit/bin/ffmpeg"
PM = f"{REPO}/.claude/skills/shorts/reference/recentre/personmask"
SW = 960


def probe(path):
    """(width, height, frame rate) AS DISPLAYED: a portrait-camera roll is stored 3840x2160 with a 90 degree rotation
    flag (the 8/28 shoot's C1654-72), and every crop in a build is in displayed pixels."""
    import json as _json
    d = _json.loads(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=width,height,r_frame_rate:stream_side_data=rotation:stream_tags=rotate", "-of", "json", path],
                                   capture_output=True, text=True).stdout)["streams"][0]
    rot = 0
    for sd in d.get("side_data_list", []):
        rot = int(sd.get("rotation", rot) or rot)
    rot = int((d.get("tags") or {}).get("rotate", rot) or rot)
    w, h = int(d["width"]), int(d["height"])
    if abs(rot) in (90, 270):
        w, h = h, w
    return w, h, d["r_frame_rate"]


def measure(roll, times, workdir):
    os.makedirs(workdir, exist_ok=True)
    W, H, _ = probe(roll)
    sh = int(round(SW * H / W / 2)) * 2
    k = W / SW

    def grab(t):
        p = os.path.join(workdir, f"h_{int(round(t * 1000)):09d}.jpg")
        if not os.path.exists(p):
            subprocess.run([FF, "-v", "error", "-y", "-ss", f"{max(0, t - 1):.4f}", "-i", roll, "-ss", f"{min(1, t):.4f}",
                            "-frames:v", "1", "-vf", f"scale={SW}:{sh}:in_color_matrix=bt709:in_range=tv", "-q:v", "3", p])
        return p

    with ThreadPoolExecutor(6) as ex:
        files = list(ex.map(grab, times))
    md = os.path.join(workdir, "masks")
    os.makedirs(md, exist_ok=True)
    todo = [f for f in files if os.path.exists(f) and not os.path.exists(os.path.join(md, os.path.basename(f)[:-4] + ".mask.png"))]
    for i in range(0, len(todo), 150):
        subprocess.run([PM, md] + todo[i:i + 150], capture_output=True)
    import mediapipe as mp
    det = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    out = {}
    for t, f in zip(times, files):
        out[t] = None
        if not os.path.exists(f):
            continue
        im = np.asarray(Image.open(f).convert("RGB"))
        r = det.process(im)
        if not r.detections:
            continue
        b = max(r.detections, key=lambda d: d.score[0]).location_data.relative_bounding_box
        cx, fw = (b.xmin + b.width / 2) * SW, b.width * SW
        chin = (b.ymin + b.height) * sh
        mp_ = os.path.join(md, os.path.basename(f)[:-4] + ".mask.png")
        hair = None
        if os.path.exists(mp_):
            m = np.asarray(Image.open(mp_).convert("L").resize((SW, sh)), np.float32) / 255.0
            x0, x1 = int(max(0, cx - 0.6 * fw)), int(min(SW, cx + 0.6 * fw))
            band = (m[:, x0:x1] > 0.5).mean(1)
            ys = np.where(band >= 0.2)[0]
            ys = ys[ys < chin]
            if len(ys):
                hair = float(ys[0])
        if hair is None:
            continue
        out[t] = dict(hair_top=round(hair * k, 1), cx=round(cx * k, 1), chin=round(chin * k, 1), face_w=round(fw * k, 1))
    return out
