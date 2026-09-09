#!/usr/bin/env python3
"""THE DOUBLE-PUMP GATE. Dense monotonic rep cutter + unit QC, frame-accurate (1/24 s).

  mono.py analyze <id> <leg> [x w y h]            print the dense motion signal
  mono.py cut     <id> <leg> <t0> <t1> [--slow F] cut a strictly-monotonic palindrome unit
  mono.py qcunit  <id> [x w y h]                  the unit must be ONE smooth unimodal pulse

  --dir <demos root>   default: $DEMOS_DIR, else <repo>/Media/exercise-demos

⚠ PROMOTED INTO THE SKILL 2026-09-09 (Phase 0 of the video-quality programme). This lived only in
`Media/exercise-demos/_r2/`, which is **gitignored** -- so SKILL.md named it as a MANDATORY rule on
every rep while the file existed on exactly one machine, in a working folder, one `rm -rf` from gone.
A rule enforced by a script that is not in the repo is not enforced. `--dir` replaced the hardcoded
`__file__/..`; nothing about the measurement changed.

⚠ `analyze` caches frames per EXERCISE, not per leg -- `rm -rf <dir>/_r2/dense/<id>-c` between legs.
⚠ A whole-frame signal reads a large-translation move as a flat plateau. Always re-run `analyze`
with a region crop scoped to the moving limb (SKILL.md, THE DOUBLE-PUMP RULE).
"""
import sys, os, subprocess, json
from PIL import Image, ImageChops, ImageStat

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
D = os.environ.get("DEMOS_DIR") or os.path.join(REPO, "Media/exercise-demos")
if "--dir" in sys.argv:
    i = sys.argv.index("--dir"); D = sys.argv[i + 1]; del sys.argv[i:i + 2]


def extract_frames(src, tmp, fps=12, crop=None):
    os.makedirs(tmp, exist_ok=True)
    if not os.listdir(tmp):
        vf = f"fps={fps}"
        if crop: vf = f"crop=iw*{crop[1]}:ih*{crop[3]}:iw*{crop[0]}:ih*{crop[2]}," + vf
        vf += ",scale=200:-1"
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src, '-vf', vf,
                        os.path.join(tmp, 'f%04d.png')], check=True)
    fs = sorted(os.listdir(tmp))
    return [(round(i / fps, 3), Image.open(os.path.join(tmp, f)).convert('L')) for i, f in enumerate(fs)]


def signal(frames):
    base = frames[0][1]
    return [(t, ImageStat.Stat(ImageChops.difference(base, im)).mean[0]) for t, im in frames]


def cmd_analyze(eid, leg, crop):
    tag = 'c' if crop else 'f'
    fr = extract_frames(os.path.join(D, eid, leg), os.path.join(D, '_r2', 'dense', f"{eid}-{tag}"), crop=crop)
    print(' '.join(f"{t}:{v:.1f}" for t, v in signal(fr)))


def cmd_cut(eid, leg, t0, t1, slow):
    src = os.path.join(D, eid, leg)
    fr = extract_frames(src, os.path.join(D, '_r2', 'dense', f"{eid}-f"))
    sig = [(t, v) for t, v in signal(fr) if t0 - 0.001 <= t <= t1 + 0.001]
    base = sig[0][1]; vals = [v for _, v in sig]
    rng = max(vals) - base
    worst = 0; run = vals[0]                       # strict monotonic check, 8% tolerance
    for v in vals:
        if v > run: run = v
        else: worst = max(worst, run - v)
    ok = worst <= 0.08 * rng
    seg = os.path.join(D, eid, 'r3-seg.mp4'); rev = os.path.join(D, eid, 'r3-rev.mp4')
    unit = os.path.join(D, eid, 'r2-unit.mp4')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src, '-ss', str(t0), '-to', str(t1), '-an',
                    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '24', seg], check=True)
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', seg, '-vf',
                    'reverse,trim=start_frame=1,setpts=PTS-STARTPTS', '-an', '-c:v', 'libx264', '-crf', '18',
                    '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '24', rev], check=True)
    cat = os.path.join(D, eid, 'r3-cat.txt'); open(cat, 'w').write(f"file '{seg}'\nfile '{rev}'\n")
    raw = os.path.join(D, eid, 'r3-rawunit.mp4')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', cat, '-c', 'copy', raw], check=True)
    if slow and abs(slow - 1.0) > 0.01:
        vf = f'setpts={slow}*PTS'
        if slow > 1.05: vf += ',minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1'
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', raw, '-vf', vf, '-an', '-c:v', 'libx264',
                        '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '24', unit], check=True)
    else:
        subprocess.run(['cp', raw, unit], check=True)
    print(json.dumps({"id": eid, "seg": [t0, t1], "monotonic_ok": ok,
                      "worst_dip_pct": round(100 * worst / max(rng, 0.01), 1), "range": round(rng, 1)}))


def cmd_qcunit(eid):
    unit = os.path.join(D, eid, 'r2-unit.mp4')
    tmp = os.path.join(D, '_r2', 'dense', f"{eid}-unit")
    subprocess.run(['rm', '-rf', tmp])
    sig = signal(extract_frames(unit, tmp, fps=12)); vals = [v for _, v in sig]
    rng = max(vals) - min(vals); peak = vals.index(max(vals))
    worst_up = 0; run = vals[0]
    for v in vals[:peak + 1]:
        if v > run: run = v
        else: worst_up = max(worst_up, run - v)
    worst_dn = 0; run = vals[peak]
    for v in vals[peak:]:
        if v < run: run = v
        else: worst_dn = max(worst_dn, v - run)
    ok = worst_up <= 0.10 * rng and worst_dn <= 0.10 * rng
    print(json.dumps({"id": eid, "unimodal_ok": ok, "bump_up_pct": round(100 * worst_up / rng, 1),
                      "bump_dn_pct": round(100 * worst_dn / rng, 1),
                      "sig": ' '.join(f"{t}:{v:.0f}" for t, v in sig)}))


a = sys.argv
if len(a) < 2: raise SystemExit(__doc__)
if a[1] == 'analyze': cmd_analyze(a[2], a[3], [float(x) for x in a[4:8]] if len(a) > 4 else None)
elif a[1] == 'cut':
    slow = 1.0
    if '--slow' in a: slow = float(a[a.index('--slow') + 1])
    cmd_cut(a[2], a[3], float(a[4]), float(a[5]), slow)
elif a[1] == 'qcunit': cmd_qcunit(a[2])
else: raise SystemExit(__doc__)
