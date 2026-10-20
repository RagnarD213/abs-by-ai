"""`python3 renderq.py selftest`: the queue's promises, checked with real processes in a throwaway queue folder.
No video is touched; a fake ffmpeg stands in for the real one. Takes about half a minute."""
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RQ = str(HERE / "renderq.py")
PY = sys.executable
sys.path.insert(0, str(HERE))
import renderq  # noqa: E402

CASES = []


def check(name, ok, detail=""):
    CASES.append((name, bool(ok), detail))
    print("{}  {}{}".format("ok  " if ok else "FAIL", name, "" if ok else "   " + str(detail)), flush=True)


def env_for(d, heavy=1, light=1, **extra):
    e = dict(os.environ, GATE_DIR=str(d), GATE_POOLS="heavy={},light={}".format(heavy, light), GATE_UNMANAGED="0")
    for k in ("GATE_HELD", "GATE_OFF", "GATE_PRIORITY", "GATE_GROUP"):
        e.pop(k, None)
    e.update({k: str(v) for k, v in extra.items()})
    return e


def stamp_cmd(log, name, hold=0.0):
    """A job that writes when it started, then holds for `hold` seconds."""
    code = ("import sys,time,json; open(sys.argv[1],'a').write(json.dumps([sys.argv[2], time.time()])+'\\n'); "
            "time.sleep(float(sys.argv[3]))")
    return [PY, "-c", code, str(log), name, str(hold)]


def starts(log):
    try:
        return [json.loads(l) for l in Path(log).read_text().splitlines() if l.strip()]
    except OSError:
        return []


def wait_for(pred, timeout):
    t = time.time()
    while time.time() - t < timeout:
        if pred():
            return True
        time.sleep(0.05)
    return False


def tickets(d):
    return [p for p in (Path(d) / "queue").glob("*.json") if not p.name.startswith(".")]


def main():
    root = Path(tempfile.mkdtemp(prefix="renderq-selftest-"))
    procs = []

    def spawn(args, env, **kw):
        p = subprocess.Popen(args, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw)
        procs.append(p)
        return p

    try:
        # 1. first come, first served; a priority job goes next without stopping the running one
        d = root / "order"
        log = root / "order.log"
        e = env_for(d)
        spawn([PY, RQ, "run", "--group", "A", "--"] + stamp_cmd(log, "A", 1.5), e)
        wait_for(lambda: starts(log), 5)
        for n in "BCD":
            spawn([PY, RQ, "run", "--group", n, "--"] + stamp_cmd(log, n, 0.2), e)
            time.sleep(0.25)
        spawn([PY, RQ, "run", "--priority", "--group", "P", "--"] + stamp_cmd(log, "P", 0.2), e)
        wait_for(lambda: len(starts(log)) == 5, 15)
        got = [s[0] for s in starts(log)]
        check("first come, first served, and a priority job goes next", got == list("APBCD"), got)
        s = starts(log)
        gaps = [s[k + 1][1] - s[k][1] for k in range(len(s) - 1)]
        check("never two running at once in a one-slot pool", all(g >= 0.18 for g in gaps[1:]) and gaps[0] >= 1.4,
              [round(g, 2) for g in gaps])

        # 2. kill -9 the slot holder: the next job starts within a second
        d = root / "kill"
        log = root / "kill.log"
        e = env_for(d)
        holder = spawn([PY, RQ, "run", "--group", "H", "--", "sleep", "30"], e)
        wait_for(lambda: any(json.loads(p.read_text() or "{}").get("pid") == holder.pid
                             for p in (Path(d) / "slots").glob("heavy.*.json")), 5)
        spawn([PY, RQ, "run", "--group", "W", "--"] + stamp_cmd(log, "W", 0), e)
        time.sleep(1.0)
        check("a waiter does not start while the slot is held", not starts(log), starts(log))
        t_kill = time.time()
        os.kill(holder.pid, signal.SIGKILL)
        wait_for(lambda: starts(log), 5)
        s = starts(log)
        check("kill -9 the holder: the next job starts within a second", s and s[0][1] - t_kill < 1.0,
              s and round(s[0][1] - t_kill, 2))
        subprocess.run(["pkill", "-f", "^sleep 30$"])

        # 3. a waiter killed with -9 leaves no ticket behind
        d = root / "deadwaiter"
        e = env_for(d)
        spawn([PY, RQ, "run", "--", "sleep", "3"], e)
        time.sleep(0.5)
        w = spawn([PY, RQ, "run", "--", "true"], e)
        wait_for(lambda: len(tickets(d)) == 1, 5)
        os.kill(w.pid, signal.SIGKILL)
        w.wait()
        env_status = dict(e)
        subprocess.run([PY, RQ, "status"], env=env_status, capture_output=True)
        check("a killed waiter's ticket is cleared at the next look", not tickets(d), tickets(d))

        # 4. nesting: a gated step inside a slot runs straight through (one-slot pool, so a deadlock would hang)
        d = root / "nest"
        e = env_for(d)
        inner = "'{}' '{}' run -- '{}' '{}' run -- true".format(PY, RQ, PY, RQ)
        r = subprocess.run([PY, RQ, "run", "--", "/bin/sh", "-c", inner], env=e, timeout=20, capture_output=True)
        check("a gated step inside a slot does not wait for a second slot", r.returncode == 0, r.stderr[-300:])
        # ... even when the environment that says so was dropped on the way down
        inner = "env -u GATE_HELD '{}' '{}' run -- true".format(PY, RQ)
        r = subprocess.run([PY, RQ, "run", "--", "/bin/sh", "-c", inner], env=e, timeout=20, capture_output=True)
        check("... even when GATE_HELD was stripped (the holder is an ancestor)", r.returncode == 0, r.stderr[-300:])
        # ... and the old buildcap.wait() inside a slot returns at once
        code = "import sys; sys.path.insert(0, %r); import buildcap; buildcap.wait('nested')" % str(HERE.parent)
        r = subprocess.run([PY, RQ, "run", "--", PY, "-c", code], env=e, timeout=20, capture_output=True)
        check("... and buildcap.wait() inside a slot returns at once", r.returncode == 0, r.stderr[-300:])

        # 5. the ffmpeg wrapper: exempt calls never wait, heavy calls wait, exit codes pass through
        d = root / "shim"
        e = env_for(d)
        fake = root / "ffmpeg.fake"
        flog = root / "fake.log"
        fake.write_text("#!/bin/sh\necho \"$(date +%s.%N 2>/dev/null) $*\" >> '{}'\n"
                        "case \"$*\" in *SLEEP*) sleep 2;; esac\n"
                        "case \"$*\" in *EXIT3*) exit 3;; esac\nexit 0\n".format(flog))
        os.chmod(fake, 0o755)
        shim = [PY, str(HERE / "ffshim.py"), str(fake)]
        holder = spawn([PY, RQ, "run", "--", "sleep", "3"], e)
        time.sleep(0.5)
        t = time.time()
        r = subprocess.run(shim + ["-ss", "5", "-i", "a.mp4", "-frames:v", "1", "x.jpg"], env=e, timeout=10)
        check("a frame grab never waits", r.returncode == 0 and time.time() - t < 1.5, round(time.time() - t, 2))
        t = time.time()
        r = subprocess.run(shim + ["-i", "a.mp4", "-vn", "-c:a", "pcm_s16le", "a.wav"], env=e, timeout=10)
        check("an audio extract never waits", r.returncode == 0 and time.time() - t < 1.5, round(time.time() - t, 2))
        t = time.time()
        r = subprocess.run(shim + ["-y", "-i", "a.mp4", "-c:v", "libx264", "EXIT3", "o.mp4"], env=e, timeout=15)
        waited = time.time() - t
        check("a heavy encode waits for the slot", waited > 1.5, round(waited, 2))
        check("the real ffmpeg's exit code comes back unchanged", r.returncode == 3, r.returncode)
        holder.wait()
        out = subprocess.run(shim + ["-i", "a.mp4", "-frames:v", "1", "x.png"], env=e, capture_output=True)
        check("the wrapper prints nothing of its own", out.stdout == b"" and out.stderr == b"", out.stderr[:200])

        # 6. the two ends of a pipe share one slot (a one-slot pool would deadlock otherwise)
        d = root / "pipe"
        e = env_for(d)
        sh = ("{s} -v error -i a.mp4 -f rawvideo SLEEP - | {s} -y -f rawvideo -i - -c:v libx264 SLEEP o.mp4"
              .format(s=" ".join("'{}'".format(x) for x in shim)))
        t = time.time()
        r = subprocess.run(["/bin/sh", "-c", sh], env=e, timeout=30)
        check("a decoder | encoder pipe runs on one slot, no deadlock", r.returncode == 0 and time.time() - t < 8,
              round(time.time() - t, 2))

        # 6b. ... even when both ends were waiting in line at the same moment (seen live on DS-33, 2026-10-20)
        d = root / "pipe2"
        e = env_for(d, heavy=2)
        spawn([PY, RQ, "run", "--", "sleep", "2"], e)
        spawn([PY, RQ, "run", "--", "sleep", "2"], e)
        time.sleep(0.5)
        r = subprocess.run(["/bin/sh", "-c", sh], env=e, timeout=30)
        ev = [json.loads(l) for l in (d / "events.log").read_text().splitlines()]
        grants = [x for x in ev if x["event"] == "granted" and x["label"].startswith("ffmpeg")]
        check("two ends of a pipe that queued together take one slot, not two", r.returncode == 0 and len(grants) == 1,
              [g["label"] for g in grants])

        # 7. the light pool does not wait behind the heavy pool
        d = root / "pools"
        e = env_for(d)
        spawn([PY, RQ, "run", "--", "sleep", "3"], e)
        time.sleep(0.5)
        t = time.time()
        r = subprocess.run([PY, RQ, "run", "--light", "--", "true"], env=e, timeout=10)
        check("a light job runs beside a heavy one", r.returncode == 0 and time.time() - t < 1.5,
              round(time.time() - t, 2))

        # 7b. an extra slot opens only while the CPU is idle
        d = root / "burst"
        spawn([PY, RQ, "run", "--", "sleep", "3"], env_for(d, heavy="1:2", GATE_IDLE=0.1, GATE_SETTLE=0))
        time.sleep(0.5)
        t = time.time()
        r = subprocess.run([PY, RQ, "run", "--", "true"], env=env_for(d, heavy="1:2", GATE_IDLE=0.1, GATE_SETTLE=0),
                           timeout=10)
        check("a busy Mac opens no extra slot", time.time() - t > 2.0, round(time.time() - t, 2))
        d = root / "burst2"
        spawn([PY, RQ, "run", "--", "sleep", "3"], env_for(d, heavy="1:2", GATE_IDLE=0.9, GATE_SETTLE=0))
        time.sleep(0.5)
        t = time.time()
        r = subprocess.run([PY, RQ, "run", "--", "true"], env=env_for(d, heavy="1:2", GATE_IDLE=0.9, GATE_SETTLE=0),
                           timeout=10)
        check("an idle Mac opens an extra slot", time.time() - t < 1.5, round(time.time() - t, 2))

        # 8. GATE_OFF skips the queue
        t = time.time()
        r = subprocess.run([PY, RQ, "run", "--", "true"], env=env_for(d, GATE_OFF=1), timeout=10)
        check("GATE_OFF=1 runs at once", r.returncode == 0 and time.time() - t < 1.5, round(time.time() - t, 2))

        # 9. a started video's next step goes ahead of new videos
        d = root / "group"
        log = root / "group.log"
        e = env_for(d)
        spawn([PY, RQ, "run", "--group", "V1", "--"] + stamp_cmd(log, "V1a", 1.0), e)
        wait_for(lambda: starts(log), 5)
        spawn([PY, RQ, "run", "--group", "V2", "--"] + stamp_cmd(log, "V2a", 0.2), e)
        time.sleep(0.3)
        spawn([PY, RQ, "run", "--group", "V1", "--"] + stamp_cmd(log, "V1b", 0.2), e)
        wait_for(lambda: len(starts(log)) == 3, 10)
        got = [s[0] for s in starts(log)]
        check("a video already running goes before one not yet started", got == ["V1a", "V1b", "V2a"], got)

        # 10. classification of real command lines from the pipeline
        cls = [
            ("-version", "exempt"),
            ("-v error -ss 10 -i a.mp4 -frames:v 1 x.jpg", "exempt"),
            ("-nostdin -threads 0 -i a.mp4 -f s16le -ac 1 -acodec pcm_s16le -ar 16000 -", "exempt"),
            ("-y -f concat -safe 0 -i l.txt -c copy out.mp4", "exempt"),
            ("-y -i a.mp4 -c:v h264_videotoolbox -b:v 8M -c:a copy out.mp4", "exempt"),
            ("-y -i a.mp4 -af loudnorm -f null -", "light"),
            ("-y -i a.mp4 -vf scale=1920:1080 -c:v libx264 -preset medium -crf 18 -c:a aac out.mp4", "heavy"),
            ("-v error -i a.mp4 -vf scale=in_color_matrix=bt709 -f rawvideo -pix_fmt rgb24 -", "heavy"),
            ("-y -i a.mov -i b.mp4 -filter_complex overlay -c:v qtrle p.mov", "heavy"),
        ]
        bad = [(a, renderq.classify(a.split())[0], w) for a, w in cls if renderq.classify(a.split())[0] != w]
        check("ffmpeg command lines are sorted into exempt, light and heavy", not bad, bad)
    finally:
        for p in procs:
            if p.poll() is None:
                p.kill()
        subprocess.run(["pkill", "-f", "^sleep 30$"])

    failed = sum(not c[1] for c in CASES)
    print("\nrenderq selftest: {} of {} pass".format(len(CASES) - failed, len(CASES)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
