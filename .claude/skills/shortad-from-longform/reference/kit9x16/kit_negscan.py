#!/usr/bin/env python3
"""THE NEGATIVE-EVENTS SCAN, recorded against the delivered file. The gate's compliance:negative_events row
enforces only that a person looked at frames of THIS render (>= 24) for body-shame framing (close-ups of
out-of-shape body parts framed with shame, a 'before' shot lingered on with contempt) and wrote it down.

  python3 kit_negscan.py sheet  --build DIR --video V [--n 30]     -> negscan/sheet.jpg (+ the frame times)
  python3 kit_negscan.py record --build DIR --video V --findings '<json list>' --by WHO
                                                                    -> plan.json['negative_events_scan']
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FP = FF.replace("ffmpeg", "ffprobe")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


def sheet(a):
    os.chdir(a.build)
    dur = float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                               capture_output=True, text=True).stdout.strip())
    os.makedirs("negscan", exist_ok=True)
    times = [round(dur * (i + 0.5) / a.n, 2) for i in range(a.n)]
    tiles = []
    for i, t in enumerate(times):
        p = f"negscan/f{i:02d}.png"
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", a.video, "-frames:v", "1", "-vf", "scale=270:480", p], check=True)
        tiles.append(Image.open(p))
    cols = 6
    rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (270 * cols, 480 * rows))
    for i, im in enumerate(tiles):
        sh.paste(im, (270 * (i % cols), 480 * (i // cols)))
    sh.save("negscan/sheet.jpg", quality=88)
    json.dump(dict(video=os.path.abspath(a.video), sha256=sha(a.video), times=times), open("negscan/frames.json", "w"), indent=1)
    print(f"{len(times)} frames -> negscan/sheet.jpg (times in negscan/frames.json)")


def record(a):
    os.chdir(a.build)
    fr = json.load(open("negscan/frames.json"))
    if fr["sha256"] != sha(a.video):
        raise SystemExit("negscan/sheet.jpg was made from a different render -- rebuild the sheet")
    plan = json.load(open("plan.json"))
    plan["negative_events_scan"] = dict(sha256=fr["sha256"], when=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                        frames_checked=len(fr["times"]), findings=json.loads(a.findings), by=a.by,
                                        method="negscan/sheet.jpg: evenly spaced frames judged for body-shame framing")
    json.dump(plan, open("plan.json", "w"), indent=1)
    print(f"negative_events_scan recorded: {len(fr['times'])} frames, {len(json.loads(a.findings))} finding(s), by {a.by}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet"); s.add_argument("--build", required=True); s.add_argument("--video", required=True); s.add_argument("--n", type=int, default=30)
    r = sub.add_parser("record"); r.add_argument("--build", required=True); r.add_argument("--video", required=True); r.add_argument("--findings", required=True); r.add_argument("--by", required=True)
    a = ap.parse_args()
    return dict(sheet=sheet, record=record)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
