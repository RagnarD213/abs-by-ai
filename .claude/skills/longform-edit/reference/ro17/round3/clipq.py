#!/usr/bin/env python3
"""clipq.py TAKE_ID:A:B ... -> clipcheck on motion/takes/<TAKE_ID>.mp4 frames A..B, one at a time, each behind buildcap.wait.
The take spec is the frame pair's spec scaled from the 1672x941 stills to the 1920x1080 take, plus camera: locked."""
import sys, json, subprocess, os
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"; R3 = "/Volumes/Extreme/_edit_work/RO-17/round3"
sys.path.insert(0, REPO + "/.claude/skills/_shared"); import buildcap
CC = REPO + "/.claude/skills/_shared/framecheck/clipcheck.py"
def take_spec(i, tid):
    w = int(subprocess.run([REPO + "/Media/video_edit/bin/ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                            "-of", "csv=p=0", f"{R3}/motion/takes/{tid}.mp4"], capture_output=True, text=True).stdout.strip())
    s = json.load(open(f"{R3}/aiframes/specs/{i}.spec.json")); k = w / 1672
    sc = lambda b: [round(v * k) for v in b]
    s["may_change"] = {n: sc(b) for n, b in s.get("may_change", {}).items()}
    for key in ("still",): s[key] = {n: sc(b) for n, b in s.get(key, {}).items()} if key in s else s.get(key)
    s = {a: b for a, b in s.items() if b is not None}
    s["camera"] = "locked"; s["note"] = (s.get("note", "") + " Take spec: boxes scaled to the take width from the 1672x941 frame pair.").strip()
    p = f"{R3}/motion/specs/{tid}.take.json"; json.dump(s, open(p, "w"), indent=1); return p
if __name__ == "__main__":
    for arg in sys.argv[1:]:
        tid, a, b = arg.split(":"); i = tid.split("_")[0]
        buildcap.wait("clipcheck " + tid)
        r = subprocess.run(["python3", CC, f"{R3}/motion/takes/{tid}.mp4", "--spec", take_spec(i, tid), "--frames", f"{a}:{b}"],
                           capture_output=True, text=True)
        open(f"{R3}/motion/logs_clipcheck_{tid}.f{a}-{b}.txt", "w").write(r.stdout + r.stderr)
        last = [l for l in r.stdout.splitlines() if "VERDICT" in l or "FAIL" in l][-6:]
        print(tid, a, b, "exit", r.returncode, *last, sep="\n  ", flush=True)
