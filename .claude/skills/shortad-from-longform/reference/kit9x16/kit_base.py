#!/usr/bin/env python3
"""CONFORM THE PICTURE to edl_picture.json (the pose-matched cut frames), 1920x1080 at the grade,
cumulative frame counts, seeks snapped to the raw's frame grid and timestamps rewritten -- the method of
`build_base_pic.py`, parameterised (any roll, any grade, any build dir). Then the 5-frame dissolve
patches for the splices the cut rule marked `cover: "dissolve"` (its last resort). Writes base.mp4.

  python3 kit_base.py --build DIR --raw ROLL [--rolls rolls.json] --grade grade.py|grade.txt|"<filter>"
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FP = FF.replace("ffmpeg", "ffprobe")
FPS = 30000 / 1001


def grade_filter(path):
    if path is None:
        return None
    if os.path.exists(path) and path.endswith(".py"):
        spec = importlib.util.spec_from_file_location("grade_mod", path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m.CURVES
    if os.path.exists(path):
        return open(path).read().strip()
    return path


def nframes(p):
    o = subprocess.run([FP, "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    return int(o.split(",")[0]) if o else -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--rolls")
    ap.add_argument("--grade")
    ap.add_argument("--crf", default="16")
    a = ap.parse_args()
    os.chdir(a.build)
    grade = grade_filter(a.grade)
    rolls = json.load(open(a.rolls)) if a.rolls else {}
    P = json.load(open("edl_picture.json"))
    pc = {round(r["cut"], 3): r for r in json.load(open("piccuts.json"))} if os.path.exists("piccuts.json") else {}
    os.makedirs("segs_pic", exist_ok=True)
    parts = []
    for s in P:
        nfr = s["n1"] - s["n0"]
        src_path = rolls.get(s.get("roll"), a.raw) if s.get("roll") else a.raw
        p = f"segs_pic/{s['i']:03d}_{s['n0']}_{nfr}.mp4"
        parts.append(p)
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            continue
        # ⚠ snap the seek to the raw's frame grid AND rewrite the timestamps (build_base_pic.py): an
        # unsnapped seek duplicates the first frame after 9 of 29 cuts; setpts=N/FR/TB puts every decoded
        # frame on a clean grid so the constant-rate output has nothing to duplicate or drop.
        src = round(s["src_in"] * FPS) / FPS - 0.0002
        vf = f"{grade + ',' if grade else ''}scale=1920:1080,setpts=N/({FPS:.6f})/TB"
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{max(0.0, src):.5f}", "-i", src_path, "-an",
                        "-vf", vf, "-r", f"{FPS:.6f}", "-frames:v", str(nfr),
                        "-c:v", "libx264", "-crf", a.crf, "-preset", "veryfast", "-pix_fmt", "yuv420p", p], check=True)
        print(f"seg {s['i']:3d}  frames {s['n0']:5d}+{nfr:4d}  src {s['src_in']:8.3f}  rel {s.get('rel', 0):+d}", flush=True)
    with open("concat_pic.txt", "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "concat_pic.txt", "-c", "copy",
                    "-video_track_timescale", "30000", "base_pic.mp4"], check=True)
    n = nframes("base_pic.mp4")
    print("base_pic.mp4 frames", n, "(planned", P[-1]["n1"], ")")
    assert n == P[-1]["n1"], f"base_pic frames {n} != planned {P[-1]['n1']}"
    # ---- dissolve patches: only where the rule marked `cover: dissolve` (never on a matched cut)
    D = 5
    jobs = []
    for s in P[1:]:
        r = pc.get(round(s["audio_cut_in"], 3))
        if r and r.get("cover") == "dissolve":
            jobs.append(s)
    if jobs:
        os.makedirs("soft", exist_ok=True)
        ins, fc, last = ["-i", "base_pic.mp4"], [], "0:v"
        for k, s in enumerate(jobs):
            # the outgoing take continued D frames past the cut, faded into the incoming segment's first D frames
            prev = P[s["i"] - 1]
            src_path = rolls.get(prev.get("roll"), a.raw) if prev.get("roll") else a.raw
            pa = f"soft/a{s['i']:03d}.mp4"
            t_out = round((prev["src_in"] + (prev["n1"] - prev["n0"]) / FPS) * FPS) / FPS - 0.0002
            vf = f"{grade + ',' if grade else ''}scale=1920:1080,setpts=N/({FPS:.6f})/TB"
            subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t_out:.5f}", "-i", src_path, "-an", "-vf", vf,
                            "-r", f"{FPS:.6f}", "-frames:v", str(D), "-c:v", "libx264", "-crf", a.crf, "-preset", "veryfast",
                            "-pix_fmt", "yuv420p", pa], check=True)
            t0 = s["n0"] / FPS
            ins += ["-i", pa]
            fc.append(f"[{k + 1}:v]setpts=PTS+{t0:.6f}/TB,fade=t=out:st={t0:.6f}:d={D / FPS:.6f}:alpha=1,format=yuva420p[s{k}];"
                      f"[{last}][s{k}]overlay=0:0:enable='between(t,{t0:.6f},{(s['n0'] + D) / FPS:.6f})':eof_action=pass[o{k}]")
            last = f"o{k}"
        subprocess.run([FF, "-nostdin", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fc), "-map", f"[{last}]",
                        "-r", "30000/1001", "-video_track_timescale", "30000", "-c:v", "libx264", "-crf", a.crf, "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-an", "base.mp4"], check=True)
        print("dissolve patches:", [round(s["n0"] / FPS, 2) for s in jobs])
    else:
        subprocess.run(["cp", "base_pic.mp4", "base.mp4"], check=True)
    print("base.mp4 frames", nframes("base.mp4"))


if __name__ == "__main__":
    sys.exit(main())
