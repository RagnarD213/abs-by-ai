#!/usr/bin/env python3
"""Ten editing steps started at once, through one version of the queue or another: before/after timings.

    python3 bench10.py OLD_RQ_DIR NEW_RQ_DIR [--runs 2] [--two] [--out results.json]

--two adds a third mode: the same ten steps two at a time with no queue at all (the serial baseline the v3 plan
measures against). Every run also records the kernel's share of all CPU time and swap in use (start, peak, end).
A v3 queue (one with mem_state) gets its memory clock warmed for 31 s first, as a busy live line always has it.

Each run starts the same ten real ffmpeg steps within three seconds, each through that version's ffmpeg wrapper
(ffshim.py) and its own private queue folder, so the live line is never joined or touched. CPU-idle extra slots are
off in both (GATE_IDLE=0: the Mac is never idle during the working day). Steps, in arrival order:

  long (24 s of footage, heavy in both)      picture passes from the 4K 10-bit 9/23 roll on Expansion and the ad2-sq
                                             1080p base on Extreme, x264 medium, and one ProRes 4444 intermediate
  short (an 8 s Flow clip)                   three frame dumps (PNG, JPG) and two trims to x264 crf 10

OLD: everything heavy, first come first served, frames in the job folder on Extreme/Expansion.
NEW: short steps in the quick lane, per-drive caps (drives.json), frames in scratch on the internal SSD
(renderq.scratch_dir). Outputs go to <drive>/_renderq_bench10/ and the scratch folder, all deleted afterwards."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
REAL = REPO / "Media" / "video_edit" / "bin" / "ffmpeg.real"
SRC4K = "/Volumes/Expansion/Abs By AI Raw Footage/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1696.MP4"
SRC1080 = "/Volumes/Extreme/_edit_work/ad2-sq/base.mp4"   # 1080p, 276 s (RO-14 tmp_base was deleted 10-21)
CLIP8 = "/Volumes/Extreme/_edit_work/RO-14/round2/veo/A2-flow-t1.mp4"
EXT, EXP = Path("/Volumes/Extreme/_renderq_bench10"), Path("/Volumes/Expansion/_renderq_bench10")


def jobs(mode, scratch):                                    # "two" uses the new layout (frames in scratch)
    """[(name, kind, ffmpeg args)] in arrival order."""
    ext, exp = EXT / mode, EXP / mode
    fr = (lambda k, drive: scratch / k) if mode == "new" else (lambda k, drive: drive / k)
    pic = ["-vf", "scale=1920:1080,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an"]
    return [
        ("L1 picture pass Extreme", "long", ["-ss", "20", "-i", SRC1080, "-t", "24"] + pic + [str(ext / "j01.mp4")]),
        ("F1 frame dump PNG", "short", ["-i", CLIP8, "-vsync", "0", str(fr("f1", ext) / "f1_%03d.png")]),
        ("L2 picture pass 4K Expansion", "long", ["-ss", "30", "-i", SRC4K, "-t", "24"] + pic + [str(exp / "j03.mp4")]),
        ("T1 trim AI clip", "short", ["-ss", "0.25", "-i", CLIP8, "-c:v", "libx264", "-crf", "10", "-preset", "medium",
                                      "-an", str(ext / "j04.mp4")]),
        ("P1 ProRes 4444 intermediate", "long", ["-ss", "120", "-i", SRC1080, "-t", "24", "-c:v", "prores_ks",
                                                 "-profile:v", "4444", "-an", str(ext / "j05.mov")]),
        ("F2 frame dump JPG", "short", ["-i", CLIP8, "-vsync", "0", "-q:v", "2", str(fr("f2", ext) / "f2_%03d.jpg")]),
        ("L3 picture pass 4K Expansion", "long", ["-ss", "90", "-i", SRC4K, "-t", "24"] + pic + [str(exp / "j07.mp4")]),
        ("T2 trim AI clip", "short", ["-ss", "0.5", "-i", CLIP8, "-c:v", "libx264", "-crf", "10", "-preset", "medium",
                                      "-an", str(ext / "j08.mp4")]),
        ("L4 picture pass Extreme", "long", ["-ss", "220", "-i", SRC1080, "-t", "24"] + pic + [str(ext / "j09.mp4")]),
        ("F3 frame dump PNG", "short", ["-i", CLIP8, "-vsync", "0", str(fr("f3", exp) / "f3_%03d.png")]),
    ]


def _sysload():
    """(cpu ticks [user, system, idle, nice], swap used MB) for the whole Mac."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import renderq
    try:
        sw = renderq.mem_now()["swap_used_mb"]
    except Exception:
        sw = None
    return renderq._ticks(), sw


def one_run(mode, rq_dir):
    qdir = Path(tempfile.mkdtemp(prefix="bench10-q-"))
    scratch = Path(tempfile.mkdtemp(prefix="bench10-scratch-", dir="/tmp"))
    for d in (EXT / ("new" if mode == "two" else mode), EXP / ("new" if mode == "two" else mode)):
        shutil.rmtree(str(d), ignore_errors=True)
        d.mkdir(parents=True)
    env = dict(os.environ, GATE_DIR=str(qdir), GATE_UNMANAGED="0", GATE_IDLE="0.0", GATE_GROUP="")
    for k in ("GATE_HELD", "GATE_OFF", "GATE_PRIORITY", "GATE_POOLS", "GATE_DRIVES", "GATE_DRIVE_MAP"):
        env.pop(k, None)
    js = jobs("new" if mode == "two" else mode, scratch)
    if mode != "two" and "def mem_state" in (Path(rq_dir) / "renderq.py").read_text():
        warm = ("import sys,time; sys.path.insert(0,%r); import renderq\n"
                "t=time.time()\nwhile time.time()-t<31: renderq.mem_state(); time.sleep(2)" % str(rq_dir))
        subprocess.run([sys.executable, "-c", warm], env=env)
    for _n, _k, args in js:
        for a in args:
            if "%" in a:
                Path(a).parent.mkdir(parents=True, exist_ok=True)
    procs, t0 = [], time.time()
    tk0, sw0 = _sysload()
    swaps = [sw0]
    logs = Path(tempfile.mkdtemp(prefix="bench10-logs-"))

    def launch(k, name, kind, args):
        e = dict(env, GATE_GROUP="bench-{}".format(k))       # ten different videos
        err = open(str(logs / "{}.err".format(k)), "w")
        if mode == "two":                                   # no queue: the real ffmpeg, two at a time
            cmd = [str(REAL), "-v", "error", "-y", "-nostdin"] + args
            e["GATE_OFF"] = "1"
        else:
            cmd = [sys.executable, "-E", "-s", str(Path(rq_dir) / "ffshim.py"), str(REAL), "-v", "error",
                   "-y", "-nostdin"] + args
        p = subprocess.Popen(cmd, env=e, stdout=subprocess.DEVNULL, stderr=err)
        procs.append(dict(name=name, kind=kind, p=p, args=args, launch=time.time() - t0, k=k))

    pending = list(enumerate(js))
    if mode != "two":
        for k, (name, kind, args) in pending:
            launch(k, name, kind, args)
            time.sleep(0.3)
        pending = []
    left, last_sw = list(procs), time.time()
    while left or pending:                                  # each job's own finish time
        while pending and sum(1 for j in procs if "done" not in j) < 2:
            k, (name, kind, args) = pending.pop(0)
            launch(k, name, kind, args)
            left.append(procs[-1])
        for j in list(left):
            if j["p"].poll() is not None:
                j["done"] = round(time.time() - t0, 1)
                left.remove(j)
        if time.time() - last_sw >= 2:
            swaps.append(_sysload()[1])
            last_sw = time.time()
        time.sleep(0.1)
    tk1, sw1 = _sysload()
    d = [b - a for a, b in zip(tk0, tk1)]
    sysinfo = dict(kernel_pct=round(100.0 * d[1] / max(1, sum(d)), 1), idle_pct=round(100.0 * d[2] / max(1, sum(d)), 1),
                   swap_start_mb=sw0, swap_peak_mb=max(x for x in swaps if x is not None) if any(swaps) else None,
                   swap_end_mb=sw1)
    ev = [json.loads(l) for l in (qdir / "events.log").read_text().splitlines()] if (qdir / "events.log").exists() else []
    out = []
    for j in procs:
        tag = os.path.basename(j["args"][-1])
        g = [e for e in ev if e["event"] == "granted" and e["label"].endswith(tag)]
        waited = g[0]["waited"] if g else 0.0
        start = (g[0]["t"] - t0) if g else j["launch"]
        if mode == "two":
            waited = j["launch"]
        out.append(dict(name=j["name"], kind=j["kind"], rc=j["p"].returncode, done=j["done"],
                        pool=g[0]["slot"].split(".")[0] if g else "none", waited=round(waited, 1),
                        ran=round(j["done"] - start, 1),
                        err=(logs / "{}.err".format(j["k"])).read_text()[-200:]))
    shutil.rmtree(str(logs), ignore_errors=True)
    for d in (EXT / "new" if mode == "two" else EXT / mode, EXP / "new" if mode == "two" else EXP / mode, scratch,
              qdir):
        shutil.rmtree(str(d), ignore_errors=True)
    return out, sysinfo


def summary(rows):
    done = [r["done"] for r in rows]
    short = [r["done"] for r in rows if r["kind"] == "short"]
    long_ = [r["done"] for r in rows if r["kind"] == "long"]
    return dict(all_done=max(done), avg_done=round(sum(done) / len(done), 1),
                short_avg_done=round(sum(short) / len(short), 1), long_avg_done=round(sum(long_) / len(long_), 1),
                short_avg_wait=round(sum(r["waited"] for r in rows if r["kind"] == "short") / len(short), 1),
                failed=[r["name"] for r in rows if r["rc"] != 0])


def main(argv):
    old, new = argv[0], argv[1]
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 1
    dest = argv[argv.index("--out") + 1] if "--out" in argv else None
    res = []
    modes = (("old", old), ("new", new)) + ((("two", new),) if "--two" in argv else ())
    if "--modes" in argv:                                  # e.g. --modes new,two
        want = argv[argv.index("--modes") + 1].split(",")
        modes = tuple(m for m in modes + (("two", new),) if m[0] in want)
        modes = tuple(dict(modes).items())
    for k in range(runs):
        for mode, rq in modes:
            sys.stderr.write("run {} {} ...\n".format(k + 1, mode))
            rows, sysinfo = one_run(mode, rq)
            s = summary(rows)
            s.update(sysinfo)
            res.append(dict(run=k + 1, mode=mode, summary=s, jobs=rows))
            sys.stderr.write("  {}\n".format(s))
            for r in rows:
                sys.stderr.write("    {:<30} {:<5} pool {:<6} waited {:>6} ran {:>6} done at {:>6}{}\n".format(
                    r["name"], r["kind"], r["pool"], r["waited"], r["ran"], r["done"],
                    "  FAILED " + r["err"] if r["rc"] else ""))
    if dest:
        Path(dest).write_text(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
