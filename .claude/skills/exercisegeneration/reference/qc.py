#!/usr/bin/env python3
"""THE EXERCISE-DEMO GATE, run before delivering any batch.

  qc.py <id> [<id> ...] [--dir <demos root>] [--strict-audio]
  qc.py --all                      every exercise directory under the demos root that has a unit

Per exercise it asserts: 1920x1080, the loop join is seamless (frame diff < 3.0 -- all 20 of batch 2
came in at 0.32-1.2), the range of motion is real (first-vs-middle diff > 2.0), the VO ends inside
the video, and -- new 2026-09-09 -- that the delivered narrated file carries a PASS stamp from
`_shared/audio/audio_gate.py`.

⚠ WRITTEN INTO THE SKILL 2026-09-09 (Phase 0 of the video-quality programme). SKILL.md said
"**Run `qc.py` before delivering**" and `.claude/skills/exercisegeneration/` contained SKILL.md and
nothing else -- the only qc.py on disk was in the gitignored `Media/exercise-demos/_r2/`, with batch
2's ten exercise ids compiled in, so it could not be run on any later batch. The ids are arguments now.

⚠ THE AUDIO ROW. Demos are gated `--synthetic --profile in-app-demo` (-24 +/-1.5 LUFS, the level Dan
approved for in-app playback). SKILL.md used to say to pass `--no-stamp` when the loudness row failed;
that shipped an UNSTAMPED file, which nothing downstream can check either. A row that does not fit
gets a measured bound, never a bypass.
"""
import argparse, os, subprocess, sys
from PIL import Image, ImageChops, ImageStat

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
BIN = os.path.join(REPO, "Media/video_edit/bin")
FF, FP = os.path.join(BIN, "ffmpeg"), os.path.join(BIN, "ffprobe")
SHARED = os.path.join(REPO, ".claude/skills/_shared/audio")


def probe(f, ent):
    return subprocess.check_output([FP, "-v", "error", "-show_entries", "format=" + ent,
                                    "-of", "csv=p=0", f]).decode().strip()


def stream(f):
    return subprocess.check_output([FP, "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=width,height,r_frame_rate", "-of", "csv=p=0", f]).decode().strip()


def frame(f, t, out):
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", f, "-frames:v", "1",
                    "-vf", "scale=320:-1", out], check=True)
    return Image.open(out).convert("L")


def diff(a, b): return ImageStat.Stat(ImageChops.difference(a, b)).mean[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true", help="every exercise dir under the root that has a unit")
    ap.add_argument("--dir", default=os.environ.get("DEMOS_DIR") or os.path.join(REPO, "Media/exercise-demos"))
    A = ap.parse_args()
    D = A.dir
    ids = A.ids
    if A.all or not ids:
        ids = sorted(d for d in os.listdir(D)
                     if os.path.isdir(os.path.join(D, d)) and not d.startswith(("_", "."))
                     and any(os.path.exists(os.path.join(D, d, u)) for u in ("r2-unit.mp4", "b2-unit.mp4")))
    if not ids: raise SystemExit(f"no exercises with a built unit under {D}")

    tmp = os.path.join(D, "_r2", "qctmp"); os.makedirs(tmp, exist_ok=True)
    sys.path.insert(0, SHARED)
    try: from require_stamp import require_stamp
    except Exception: require_stamp = None

    print(f"{'id':22}{'dur':>7}{'unit':>7}{'join':>7}{'range':>7}  {'vo_in':<6}{'stamp':<7}{'video'}")
    bad = []
    for eid in ids:
        f = os.path.join(D, eid, f"{eid}-AIDAN-narrated.mp4")
        unit = next((os.path.join(D, eid, u) for u in ("r2-unit.mp4", "b2-unit.mp4")
                     if os.path.exists(os.path.join(D, eid, u))), None)
        if not (os.path.exists(f) and unit):
            print(f"{eid:22}  PENDING"); bad.append(eid + " PENDING"); continue
        dur = float(probe(f, "duration")); ud = float(probe(unit, "duration"))
        vs = stream(f)
        a = frame(unit, 0, tmp + "/a.png"); b = frame(unit, max(0, ud - 0.05), tmp + "/b.png")
        m = frame(unit, ud / 2, tmp + "/m.png")
        join, rng = diff(a, b), diff(a, m)
        vof = next((os.path.join(D, eid, v) for v in ("r2-vo.mp3", "b2-vo.mp3")
                    if os.path.exists(os.path.join(D, eid, v))), None)
        vo = float(probe(vof, "duration")) if vof else 0.0
        # THE AUDIO STAMP on the delivered narrated file. --allow-synthetic: an AI voice, no camera.
        st = "n/a"
        if require_stamp:
            try: require_stamp(f, synthetic_ok=True, quiet=True); st = "PASS"
            except BaseException: st = "NONE"
        flag = ""
        if join > 3.0: flag += " JOIN!"
        if rng < 2.0: flag += " RANGE!"
        if not vof or (1.0 + vo) > dur: flag += " VO!"
        if not vs.startswith("1920,1080"): flag += " RES!"
        if st != "PASS": flag += " STAMP!"
        if flag: bad.append(eid + flag)
        print(f"{eid:22}{dur:>7.2f}{ud:>7.2f}{join:>7.2f}{rng:>7.2f}  "
              f"{str((1.0+vo) <= dur):<6}{st:<7}{vs}{flag}")
    print("\nFLAGGED:", bad if bad else "none")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
