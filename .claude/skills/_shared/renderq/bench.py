"""Throughput bench for the render queue: N dummy jobs, three ways.

    python3 bench.py [--jobs 30] [--modes gate,pair,all] [--out results.json]

  gate  every job started at once through `renderq.py run` (production pool sizes, a private queue folder)
  pair  the old way: two at a time by hand, first come first served
  all   every job at once with no queue

Job mix, in arrival order, repeating: an x264 encode (multi-core, like a picture pass), a Python-fed pipe render
(numpy frames into x264, like softblue/composite renders: one Python core plus a starved encoder), and a light
single-threaded job (like Whisper or PIL graphics). Uses the REAL ffmpeg binary, never the wrapper, and writes
only to a scratch folder. Records makespan, when each job finished, how long each ran, load and CPU idle."""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import renderq  # noqa: E402

FF = str(renderq.REAL_FFMPEG if renderq.REAL_FFMPEG.exists() else renderq.BIN / "ffmpeg")
PY = sys.executable
PIPE_SRC = r'''
import sys, subprocess, numpy as np
ff, out, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
p = subprocess.Popen([ff, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1280x720", "-r", "30",
                      "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out],
                     stdin=subprocess.PIPE)
base = np.random.RandomState(1).randint(0, 255, (720, 1280, 3)).astype(np.float32)
for k in range(n):
    f = base * (0.5 + 0.5 * np.sin(k / 9.0)) + np.roll(base, k, axis=1) * 0.3
    for _ in range(3):
        f = np.clip(f * 1.01 - 1.0, 0, 255)
    p.stdin.write(f.astype(np.uint8).tobytes())
p.stdin.close()
sys.exit(p.wait())
'''
LIGHT_SRC = "import time\nt=time.time()\nx=0\nwhile time.time()-t<float(__import__('sys').argv[1]): x+=1\n"


def job_cmd(kind, k, work):
    out = str(work / "j{:02d}.mp4".format(k))
    if kind == "x264":
        return [FF, "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30", "-t", "20",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out]
    if kind == "pipe":
        return [PY, str(work / "pipe.py"), FF, out, "150"]
    return [PY, str(work / "light.py"), "8"]


def kinds(n):
    order = ["x264", "pipe", "light"]
    return [order[k % 3] for k in range(n)]


def sampler(stop, rows):
    prev = renderq._ticks()
    while not stop.is_set():
        time.sleep(1.0)
        cur = renderq._ticks()
        d = [b - a for a, b in zip(prev, cur)]
        prev = cur
        rows.append(dict(t=time.time(), load=os.getloadavg()[0], idle=d[2] / float(sum(d) or 1)))


def run_mode(mode, n, work, qdir):
    env = dict(os.environ, GATE_DIR=str(qdir), GATE_UNMANAGED="0")
    for k in ("GATE_HELD", "GATE_OFF", "GATE_PRIORITY", "GATE_POOLS"):
        env.pop(k, None)
    ks = kinds(n)
    rec = [dict(kind=ks[k]) for k in range(n)]
    stop, rows = threading.Event(), []
    th = threading.Thread(target=sampler, args=(stop, rows))
    th.start()
    t0 = time.time()

    def one(k):
        cmd = job_cmd(ks[k], k, work)
        if mode == "gate":
            cmd = [PY, str(HERE / "renderq.py"), "run", "--quiet"] + \
                  (["--light"] if ks[k] == "light" else []) + ["--group", "j{}".format(k), "--"] + cmd
        rec[k]["submit"] = time.time() - t0
        p = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        _, err = p.communicate()
        rec[k]["end"] = time.time() - t0
        rec[k]["rc"] = p.returncode
        if p.returncode:
            rec[k]["err"] = err.decode(errors="replace")[-300:]

    if mode == "pair":
        lock, nxt = threading.Lock(), [0]

        def worker():
            while True:
                with lock:
                    k = nxt[0]
                    nxt[0] += 1
                if k >= n:
                    return
                one(k)
        ts = [threading.Thread(target=worker) for _ in range(2)]
    else:
        ts = [threading.Thread(target=one, args=(k,)) for k in range(n)]
    for t in ts:
        t.start()
        if mode != "pair":
            time.sleep(0.02)
    for t in ts:
        t.join()
    stop.set()
    th.join()
    # how long each job actually ran (for the gated mode, from the queue's own history)
    if mode == "gate":
        hist = [json.loads(l) for l in (qdir / "history.jsonl").read_text().splitlines() if l.strip()]
        byg = {h["group"]: h for h in hist}
        for k, r in enumerate(rec):
            h = byg.get("j{}".format(k))
            if h:
                r["ran"] = round(h["dur"], 2)
                r["waited"] = round(h["start"] - t0 - r["submit"], 2)
    for r in rec:
        r.setdefault("ran", round(r["end"] - r["submit"], 2))
    span = max(r["end"] for r in rec)
    loads = [x["load"] for x in rows]
    idles = [x["idle"] for x in rows]
    summ = dict(mode=mode, jobs=n, makespan_s=round(span, 1),
                mean_finish_s=round(sum(r["end"] for r in rec) / n, 1),
                median_finish_s=round(sorted(r["end"] for r in rec)[n // 2], 1),
                mean_ran_s={kd: round(sum(r["ran"] for r in rec if r["kind"] == kd) /
                                      max(1, sum(r["kind"] == kd for r in rec)), 1) for kd in ("x264", "pipe", "light")},
                failures=sum(1 for r in rec if r.get("rc")),
                load_mean=round(sum(loads) / max(1, len(loads)), 1), load_max=round(max(loads or [0]), 1),
                idle_mean=round(sum(idles) / max(1, len(idles)), 3))
    return summ, rec, rows


def main(argv):
    n, modes, out = 30, ["gate", "pair", "all"], None
    k = 0
    while k < len(argv):
        if argv[k] == "--jobs":
            n = int(argv[k + 1])
            k += 1
        elif argv[k] == "--modes":
            modes = argv[k + 1].split(",")
            k += 1
        elif argv[k] == "--out":
            out = argv[k + 1]
            k += 1
        k += 1
    work = Path(tempfile.mkdtemp(prefix="renderq-bench-"))
    (work / "pipe.py").write_text(PIPE_SRC)
    (work / "light.py").write_text(LIGHT_SRC)
    results = []
    for mode in modes:
        qdir = work / ("q-" + mode)
        print("running {} ({} jobs) ...".format(mode, n), flush=True)
        summ, rec, rows = run_mode(mode, n, work, qdir)
        summ["background_before"] = os.getloadavg()[0]
        print(json.dumps(summ), flush=True)
        results.append(dict(summary=summ, jobs=rec, samples=rows))
        time.sleep(10)
    if out:
        Path(out).write_text(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
