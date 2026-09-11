#!/usr/bin/env python3
"""framing.py — how much empty frame surrounds Dan, shot by shot, on an editor's cut.

    python3 framing.py CUT.mp4 [--fps 2] [--sheet framing_sheet.jpg]

Works on any footage (no plan, no door panel — the website-video hairgate needs both). MediaPipe Pose
(legacy solutions API, bundled model, offline) on 2 frames a second. Per frame the subject box is the
visible pose landmarks plus the top of the head (eye line pushed out by 2x the eye-to-mouth distance, in
whatever direction his head points, so it works on a rollout as well as upright). Shots are split where
the background jumps (a punch-in or a cut changes the top half of the frame at once). Per shot, the box
is the union of the whole shot (5th/95th percentiles, so the whole rep fits) and the margins are the
empty frame outside it, as % of the frame.

Dan's standard (2026-09-11, Zeeshan's ab wheel follow-along: "Crop in closer by 20-30%... avoid
excessive space above my head and towards the side... get it almost as tight as possible"; and the
locked hair-anchored standard of 2026-09-08: NEAR = hair to belly button, FAR = hair to shorts line,
never wide):
  upright shot (talking, standing, kneeling):  LOOSE if the top margin is over --top-upright % (8) or
                                                his knees are in frame (a full-body talking shot is the
                                                banned wide level)
  horizontal shot (a rollout, a plank, a lift): LOOSE if the shot could be cropped in --crop-move % (15)
                                                or more without cutting any of the rep off (re-centred,
                                                same aspect, 3% margin). A 16:9 frame filled edge to edge
                                                by a prone body still has sky above it; that is not loose.
A proof sheet with one frame per shot and the box drawn is written — LOOK at it; a pose miss reads as a
shot with no subject and is reported, never passed.
"""
import argparse, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[4]
FF = ROOT / "Media/video_edit/bin/ffmpeg"
FF = str(FF) if FF.exists() else "ffmpeg"
W, H = 960, 540


def frames(path, fps):
    p = subprocess.Popen([FF, "-v", "error", "-i", path, "-vf", f"fps={fps},scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


def subject_box(pose, img):
    r = pose.process(img)
    if not r.pose_landmarks:
        return None
    L = r.pose_landmarks.landmark
    pts = [(l.x, l.y) for l in L if l.visibility >= 0.5]
    if len(pts) < 6:
        return None
    eye = np.mean([(L[i].x, L[i].y) for i in (2, 5)], axis=0)
    mouth = np.mean([(L[i].x, L[i].y) for i in (9, 10)], axis=0)
    top = eye + 2.0 * (eye - mouth)
    pts.append(tuple(top))
    xs, ys = np.clip([p[0] for p in pts], 0, 1), np.clip([p[1] for p in pts], 0, 1)
    knees = any(L[i].visibility >= 0.5 and L[i].y < 0.98 for i in (25, 26))
    return xs.min(), ys.min(), xs.max(), ys.max(), knees


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cut")
    ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--sheet", default="framing_sheet.jpg")
    ap.add_argument("--top-upright", type=float, default=8.0)
    ap.add_argument("--crop-move", type=float, default=15.0)
    ap.add_argument("--min-shot", type=float, default=2.0)
    a = ap.parse_args()
    import mediapipe as mp
    pose = mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1)

    recs, thumbs, prev = [], [], None
    for k, img in enumerate(frames(a.cut, a.fps)):
        top = img[: H // 2: 8, ::8].mean(axis=2)
        jump = prev is not None and np.abs(top - prev).mean() > 10
        prev = top
        recs.append((k / a.fps, jump, subject_box(pose, img)))
        thumbs.append(img)
    shots, cur = [], []
    for i, rec in enumerate(recs):
        if rec[1] and cur:
            shots.append(cur)
            cur = []
        cur.append(i)
    shots.append(cur)

    fmt = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
    sheet_items, loose = [], 0
    print(f"{len(shots)} shots; margins are empty frame outside his box over the whole shot, % of frame")
    for sh in shots:
        t0, t1 = recs[sh[0]][0], recs[sh[-1]][0] + 1 / a.fps
        if t1 - t0 < a.min_shot:
            continue
        boxes = [recs[i][2] for i in sh if recs[i][2]]
        if len(boxes) < max(2, len(sh) // 3):
            print(f"{fmt(t0)}-{fmt(t1)}  NO SUBJECT FOUND in {len(sh) - len(boxes)} of {len(sh)} frames — insert, graphic or a pose miss; LOOK at it")
            continue
        B = np.array([b[:4] for b in boxes])
        x0, y0 = np.percentile(B[:, 0], 5), np.percentile(B[:, 1], 5)
        x1, y1 = np.percentile(B[:, 2], 95), np.percentile(B[:, 3], 95)
        knees = np.mean([b[4] for b in boxes]) > 0.5
        topm, left, right = 100 * y0, 100 * x0, 100 * (1 - x1)
        # how far the shot could be cropped in (same 16:9 aspect, re-centred, 3% margin kept) without cutting
        # any of the rep off: the box must fit a window 1/z of the frame on both axes
        zmax = (1 - 2 * 0.03) / max(x1 - x0, y1 - y0, 1e-6)
        crop_in = max(0.0, 100 * (1 - 1 / zmax))
        upright = (y1 - y0) * H >= (x1 - x0) * W
        if upright:
            bad = topm > a.top_upright or knees
            why = (f"top {topm:.0f}%{' + knees in frame (full-body wide)' if knees else ''}, "
                   f"could crop in {crop_in:.0f}%")
            kind = "upright"
        else:
            bad = crop_in >= a.crop_move
            why = f"top {topm:.0f}%, left {left:.0f}%, right {right:.0f}%, could crop in {crop_in:.0f}%"
            kind = "horizontal"
        loose += bad
        print(f"{fmt(t0)}-{fmt(t1)}  {kind:10s} {why:48s} -> {'LOOSE' if bad else 'OK'}")
        mid = sh[len(sh) // 2]
        im = Image.fromarray(thumbs[mid]).copy()
        d = ImageDraw.Draw(im)
        d.rectangle([x0 * W, y0 * H, x1 * W, y1 * H], outline=(255, 60, 60) if bad else (60, 255, 60), width=4)
        d.text((8, 8), f"{fmt(t0)} {'LOOSE' if bad else 'OK'} {why}", fill=(255, 255, 0))
        sheet_items.append(im.resize((480, 270)))
    if sheet_items:
        cols = 4
        rows = (len(sheet_items) + cols - 1) // cols
        s = Image.new("RGB", (480 * cols, 270 * rows))
        for i, im in enumerate(sheet_items):
            s.paste(im, ((i % cols) * 480, (i // cols) * 270))
        s.save(a.sheet, quality=85)
        print(f"proof sheet: {a.sheet}")
    print(f"verdict: {'LOOSE' if loose else 'OK'} — {loose} loose shot(s)"
          + (". Crop in (Dan: 20-30%): a small margin above his hair and at the sides, the whole rep in frame."
             if loose else ""))


if __name__ == "__main__":
    main()
