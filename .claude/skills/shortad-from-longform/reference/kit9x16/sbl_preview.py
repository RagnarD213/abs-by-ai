#!/usr/bin/env python3
"""A REVIEW CLIP OF A SHEET BUILD BEFORE THE FULL FILM EXISTS: render_sbl.py --range A B (whole beats), the captions
burned from captions.mov, the 16:9's delivered mix for the same span. For the first-minute and in-context clips on the
graphic-lock review page (PRE-RENDER-APPROVAL.md).

  python3 sbl_preview.py --build B --range A B --out NAME.mp4 [--size 540]
"""
import argparse, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
ap = argparse.ArgumentParser(); ap.add_argument("--build", required=True); ap.add_argument("--range", nargs=2, type=float, required=True)
ap.add_argument("--out", required=True); ap.add_argument("--size", type=int, default=0)
ap.add_argument("--exact", action="store_true", help="exactly the asked seconds (default: the whole beats they touch)")
a = ap.parse_args()
B = os.path.abspath(a.build); os.chdir(B)
pic = os.path.join(B, "out", f"_pv_{int(a.range[0] * 100)}_{int(a.range[1] * 100)}.mp4")
subprocess.run([sys.executable, os.path.join(HERE, "render_sbl.py"), "--range", str(a.range[0]), str(a.range[1]), "--out", pic]
               + (["--exact"] if a.exact else []), check=True)
r = json.load(open(pic + ".range.json"))
sc = f",scale={a.size}:-2" if a.size else ""
subprocess.run([FF, "-v", "error", "-y", "-i", pic, "-ss", f"{r['t0']:.5f}", "-i", "captions.mov", "-ss", f"{r['t0']:.5f}", "-t", f"{r['t1'] - r['t0']:.5f}",
                "-i", "his_mix.wav", "-filter_complex", f"[1:v]setpts=PTS-STARTPTS[c];[0:v][c]overlay=0:0:eof_action=pass:format=auto{sc}[v]",
                "-map", "[v]", "-map", "2:a", "-frames:v", str(r["frames"]), "-c:v", "libx264", "-crf", "18" if not a.size else "22", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", a.out], check=True)
print(a.out, f"{r['t0']:.2f}-{r['t1']:.2f} s")
