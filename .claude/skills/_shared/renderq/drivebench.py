#!/usr/bin/env python3
"""Measure how much parallel work each drive takes, and set the render queue's per-drive caps from it.

    python3 drivebench.py                     every mounted work drive (Extreme, Expansion, Seagate, internal)
    python3 drivebench.py Extreme internal    just these
    python3 drivebench.py --save              also write the caps to drives.json (renderq reads them)
    python3 drivebench.py --runs 2 --save     each drive twice, caps from the average (the drives are shared with live
                                              builds, so one pass is noisy)

Each drive gets four short tests at 1, 2, 3, 4 and 6 streams at once, about 5 s per level, uncached
(F_NOCACHE, so the RAM cache cannot flatter a drive):
  read    sequential 1 MB reads, each stream its own file (a decoder reading footage)
  write   sequential 1 MB writes to new files (an encoder or ProRes intermediate)
  mixed   n steps, each one reader plus one writer (a render reading its source and writing its output)
  frames  each stream writes 2 MB files one after another (a frame dump to PNG/JPG)
Test files go in <drive>/_renderq_bench/ (internal: /tmp) and are deleted at the end, also on Ctrl-C.

CAP RULE (drives.json "caps"), on the mixed test averaged over the runs: the most steps at once at which every step
still gets NEED_MBS (a frame dump writes ~90 MB/s, a 4K decode reads 20-60 MB/s) AND the drive's total is still at
least COLLAPSE of its best total (an SSD near full, or a disk seeking, gets slower in total when shared too widely).
Measured 2026-10-20 on a busy Mac: Handoffs/results-20261020-renderq-drives.md.
"""
import fcntl
import json
import os
import shutil
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "drives.json"
F_NOCACHE = 48
BLOCK = 1 << 20
FRAME = 2 << 20
LEVEL_S = 5.0
LEVELS = (1, 2, 3, 4, 6)
NEED_MBS = 60.0              # a heavy step's I/O: a 4K 10-bit decode (~20-40 MB/s) plus ProRes/x264 output
COLLAPSE = 0.6
PREP_MB = 768                # per read file
WRITE_CAP_MB = 4096          # most one level may write in total (Extreme runs near full)
RESERVE_GB = 25              # never bench a drive with less free than this


def work_drives():
    out = [("internal", Path("/tmp"))]
    for name in ("Extreme", "Expansion", "Seagate"):
        p = Path("/Volumes") / name
        if p.is_dir() and os.path.ismount(str(p)):
            out.append((name, p))
    return out


def _open(path, flags):
    fd = os.open(str(path), flags, 0o644)
    try:
        fcntl.fcntl(fd, F_NOCACHE, 1)
    except OSError:
        pass
    return fd


def _reader(path, stop, tally, k):
    fd = _open(path, os.O_RDONLY)
    size, off, n = os.fstat(fd).st_size, 0, 0
    try:
        while not stop.is_set():
            b = os.pread(fd, BLOCK, off)
            if not b:
                off = 0
                continue
            off += len(b)
            n += len(b)
    finally:
        os.close(fd)
        tally[k] = n


def _writer(path, cap, stop, tally, k):
    fd = _open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    buf, n = os.urandom(BLOCK), 0
    try:
        while not stop.is_set() and n < cap:
            n += os.write(fd, buf)
            if n % (64 * BLOCK) == 0:
                os.fsync(fd)                                # flush inside the timed window, not after it
        stop.set()                                          # a stream at its byte cap ends the level for all
        os.fsync(fd)
    finally:
        os.close(fd)
        tally[k] = n


def _framer(folder, cap, stop, tally, k):
    folder.mkdir(parents=True, exist_ok=True)
    buf, n, i = os.urandom(FRAME), 0, 0
    while not stop.is_set() and n < cap:
        fd = _open(folder / "f{:05d}.png".format(i), os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        try:
            n += os.write(fd, buf)
        finally:
            os.close(fd)
        i += 1
    stop.set()
    tally[k] = n


def _level(jobs):
    """Run jobs [(fn, args)] together for LEVEL_S; fn(*args, stop, tally, k). Returns (total MB/s, [per stream])."""
    stop, tally = threading.Event(), {}
    threads = [threading.Thread(target=fn, args=tuple(args) + (stop, tally, k)) for k, (fn, args) in enumerate(jobs)]
    t0 = time.time()
    for t in threads:
        t.start()
    stop.wait(LEVEL_S)
    el = time.time() - t0                                   # until the time limit or the first stream at its cap
    stop.set()
    for t in threads:
        t.join()
    per = [tally.get(k, 0) / el / 1e6 for k in range(len(jobs))]
    return round(sum(per), 1), [round(x, 1) for x in per]


def bench(name, root):
    free_gb = shutil.disk_usage(str(root)).free / 1e9
    if free_gb < RESERVE_GB + 8:
        return dict(skipped="only {:.0f} GB free".format(free_gb))
    base = (root / "_renderq_bench") if name != "internal" else Path("/tmp/_renderq_bench")
    shutil.rmtree(str(base), ignore_errors=True)
    base.mkdir(parents=True)
    res = dict(free_gb=round(free_gb), read={}, write={}, mixed={}, frames={})
    try:
        top = max(LEVELS)
        for k in range(top):                                # read files, written uncached so reads hit the drive
            fd = _open(base / "r{}.bin".format(k), os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            buf = os.urandom(BLOCK)
            for _ in range(PREP_MB):
                os.write(fd, buf)
            os.fsync(fd)
            os.close(fd)
        for n in LEVELS:
            res["read"][n] = _level([(_reader, (base / "r{}.bin".format(k),)) for k in range(n)])
            cap = WRITE_CAP_MB * BLOCK // n
            res["write"][n] = _level([(_writer, (base / "w{}.bin".format(k), cap)) for k in range(n)])
            for k in range(n):
                (base / "w{}.bin".format(k)).unlink()
            # n heavy steps, each reading its source and writing its output: 2n streams
            jobs = [(_reader, (base / "r{}.bin".format(k),)) for k in range(n)]
            jobs += [(_writer, (base / "m{}.bin".format(k), cap)) for k in range(n)]
            res["mixed"][n] = _level(jobs)
            for p in base.glob("m*.bin"):
                p.unlink()
            res["frames"][n] = _level([(_framer, (base / "fr{}".format(k), cap)) for k in range(n)])
            for k in range(n):
                shutil.rmtree(str(base / "fr{}".format(k)), ignore_errors=True)
            sys.stderr.write("  {} x{}: read {} write {} mixed {} frames {} MB/s\n".format(
                name, n, res["read"][n][0], res["write"][n][0], res["mixed"][n][0], res["frames"][n][0]))
    finally:
        shutil.rmtree(str(base), ignore_errors=True)
    return res


def cap_from(runs):
    """Most heavy steps at once on this drive (see CAP RULE above), from one or more runs of bench()."""
    mixed = {n: sum(r["mixed"][n][0] for r in runs) / len(runs) for n in LEVELS}
    peak, cap = max(mixed.values()), 1
    for n in LEVELS:
        if n > 1 and (mixed[n] / n < NEED_MBS or mixed[n] < COLLAPSE * peak):
            break
        cap = n
    return cap


def main(argv):
    save = "--save" in argv
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 1
    names = [a for a in argv if not a.startswith("--") and not a.isdigit()]
    drives = [(n, p) for n, p in work_drives() if not names or n in names]
    out = _load()
    for name, root in drives:
        got = []
        for k in range(runs):
            sys.stderr.write("benchmarking {} (run {} of {}) ...\n".format(name, k + 1, runs))
            r = bench(name, root)
            if "skipped" in r:
                sys.stderr.write("  skipped: {}\n".format(r["skipped"]))
                break
            got.append(r)
        if not got:
            continue
        cap = cap_from(got)
        out["drives"][name] = dict(runs=got, cap=cap, measured=time.strftime("%Y-%m-%d %H:%M"),
                                   kind="hdd" if name in ("Expansion", "Seagate") else "ssd")
        out["caps"][name] = cap
        print(json.dumps({name: dict(cap=cap, mixed_avg={n: round(sum(r["mixed"][n][0] for r in got) / len(got))
                                                         for n in LEVELS})}))
    if save:
        tmp = OUT.with_suffix(".tmp")
        tmp.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
        os.replace(tmp, OUT)
        print("saved caps to {}: {}".format(OUT, out["caps"]))
    return 0


def _load():
    try:
        d = json.loads(OUT.read_text())
    except (OSError, ValueError):
        d = {}
    d.setdefault("drives", {})
    d.setdefault("caps", {})
    return d


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
