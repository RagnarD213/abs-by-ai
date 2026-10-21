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
    root = Path(os.path.realpath(tempfile.mkdtemp(prefix="renderq-selftest-")))
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
        wait_for(lambda: starts(log), 10)
        gr = [json.loads(l) for l in (Path(d) / "events.log").read_text().splitlines()]
        gr = [g["t"] for g in gr if g["event"] == "granted" and g.get("group") == "W"]
        check("kill -9 the holder: the next job gets the slot within a second", gr and gr[0] - t_kill < 1.0,
              gr and round(gr[0] - t_kill, 2))
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

        # 11. per-drive caps: a waiter whose drive is full steps aside for one on another drive
        da, db = root / "driveA", root / "driveB"
        for x in (da, db):
            (x / "_edit_work").mkdir(parents=True)
        dmap = "{}=FakeA,{}=FakeB".format(da, db)
        d = root / "drives"
        log = root / "drives.log"
        e = env_for(d, heavy=3, GATE_DRIVE_MAP=dmap, GATE_DRIVES="FakeA=1,FakeB=1")
        spawn([PY, RQ, "run", "--group", "A1", "--"] + stamp_cmd(log, "A1", 1.5), e, cwd=str(da))
        wait_for(lambda: starts(log), 5)
        spawn([PY, RQ, "run", "--group", "A2", "--"] + stamp_cmd(log, "A2", 0.2), e, cwd=str(da))
        time.sleep(0.4)
        spawn([PY, RQ, "run", "--group", "B1", "--"] + stamp_cmd(log, "B1", 0.2), e, cwd=str(db))
        wait_for(lambda: len(starts(log)) == 3, 10)
        got = [s[0] for s in starts(log)]
        s = dict((n, t) for n, t in starts(log))
        check("a job on a free drive goes past one waiting for its full drive", got == ["A1", "B1", "A2"], got)
        check("... and the full drive never runs two at once", s.get("A2", 0) - s.get("A1", 0) >= 1.4,
              round(s.get("A2", 0) - s.get("A1", 0), 2))

        # 11b. a slot held by the older queue code (no drives recorded) still counts against its folder's drive
        d = root / "olddrive"
        log = root / "olddrive.log"
        e = env_for(d, heavy=3, GATE_DRIVE_MAP=dmap, GATE_DRIVES="FakeA=1,FakeB=1")
        (d / "slots").mkdir(parents=True)
        old = ("import fcntl,json,os,sys,time; d=sys.argv[1]; fd=os.open(d+'/slots/heavy.0.lock',os.O_RDWR|os.O_CREAT);"
               "fcntl.flock(fd,fcntl.LOCK_EX); json.dump(dict(pid=os.getpid(),ppid=os.getppid(),pool='heavy',i=0,"
               "label='old build',group='OLD',start=time.time(),cwd=sys.argv[2],cmd='python3 build.py'),"
               "open(d+'/slots/heavy.0.json','w')); time.sleep(2)")
        spawn([PY, "-c", old, str(d), str(da)], e)
        time.sleep(0.5)
        spawn([PY, RQ, "run", "--group", "A3", "--"] + stamp_cmd(log, "A3", 0), e, cwd=str(da))
        spawn([PY, RQ, "run", "--group", "B2", "--"] + stamp_cmd(log, "B2", 0), e, cwd=str(db))
        wait_for(lambda: len(starts(log)) == 2, 10)
        got = [s[0] for s in starts(log)]
        check("an old-format slot holder counts against the drive it runs on", got == ["B2", "A3"], got)

        # 12. the quick lane: heavy work on a short clip does not wait behind long renders
        real = str(renderq.REAL_FFMPEG if renderq.REAL_FFMPEG.exists() else renderq.BIN / "ffmpeg")
        clips = {}
        for name, secs in (("short", 2), ("long", 30)):
            clips[name] = root / "{}.mp4".format(name)
            subprocess.run([real, "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=64x64:rate=10", "-t",
                            str(secs), "-c:v", "libx264", "-preset", "ultrafast", str(clips[name])],
                           env=dict(os.environ, GATE_OFF="1"), check=True)
        sec = renderq.media_seconds(str(clips["short"])), renderq.media_seconds(str(clips["long"]))
        check("clip length is read from the file header", abs(sec[0] - 2) < 0.2 and abs(sec[1] - 30) < 0.2, sec)
        d = root / "quick"
        e = env_for(d)
        holder = spawn([PY, RQ, "run", "--", "sleep", "3"], e)
        time.sleep(0.5)
        t = time.time()
        r = subprocess.run(shim + ["-y", "-i", str(clips["short"]), "-c:v", "libx264", "q.mp4"], env=e, timeout=10)
        check("a short clip's encode or frame dump does not wait behind a long render",
              r.returncode == 0 and time.time() - t < 1.5, round(time.time() - t, 2))
        t = time.time()
        r = subprocess.run(shim + ["-y", "-i", str(clips["long"]), "-c:v", "libx264", "l.mp4"], env=e, timeout=15)
        check("... while a long clip's encode still waits its turn", time.time() - t > 1.5, round(time.time() - t, 2))
        holder.wait()
        cls = [(["-i", str(clips["short"]), "-vf", "fps=24", str(root / "f%03d.png")], "quick"),
               (["-i", str(clips["long"]), "-vf", "fps=24", str(root / "f%03d.png")], "heavy"),
               (["-ss", "60", "-i", str(clips["long"]), "-t", "12", "-c:v", "libx264", "x.mp4"], "quick"),
               (["-i", str(clips["long"]), "-frames:v", "240", "x.mp4"], "quick"),
               (["-f", "lavfi", "-i", "testsrc", "-c:v", "libx264", "x.mp4"], "heavy")]
        bad = [(" ".join(a)[-60:], renderq.classify(a)[0], w) for a, w in cls if renderq.classify(a)[0] != w]
        check("short media goes in the quick lane, long media stays heavy", not bad, bad)

        # 13. work folders: a job keeps its folder; a new job goes to the least busy drive with room
        (db / "_edit_work" / "JOB-OLD").mkdir()
        d = root / "workdir"
        e = env_for(d, heavy=3, GATE_DRIVE_MAP=dmap, GATE_DRIVES="FakeA=2,FakeB=2", GATE_WORK_RESERVE_GB=0)
        r = subprocess.run([PY, RQ, "workdir", "job-old", "--need", "0"], env=e, capture_output=True, text=True)
        check("a job that has a work folder keeps it (any drive, any case)",
              r.stdout.strip() == str(db / "_edit_work" / "JOB-OLD"), r.stdout + r.stderr[-200:])
        holder = spawn([PY, RQ, "run", "--", "sleep", "3"], e, cwd=str(da))
        time.sleep(0.6)
        r = subprocess.run([PY, RQ, "workdir", "JOB-NEW", "--need", "0"], env=e, capture_output=True, text=True)
        check("a new job's folder goes on the drive with less heavy work",
              r.stdout.strip() == str(db / "_edit_work" / "JOB-NEW") and (db / "_edit_work" / "JOB-NEW").is_dir(),
              r.stdout + r.stderr[-200:])
        e2 = dict(e, GATE_WORK_RESERVE_GB="1000000")
        r = subprocess.run([PY, RQ, "workdir", "JOB-FULL", "--need", "0", "--no-create"], env=e2, capture_output=True,
                           text=True)
        check("... and with no room anywhere it still answers (most free space)", r.returncode == 0 and r.stdout.strip(),
              r.stderr[-200:])
        holder.wait()

        # 14. scratch: the internal SSD while it has room, the job's own drive when it does not; old ones pruned
        sc = root / "scratch"
        e = env_for(d, GATE_DRIVE_MAP=dmap, GATE_SCRATCH=str(sc), GATE_WORK_RESERVE_GB=0, GATE_SCRATCH_RESERVE_GB=0)
        stale = sc / "STALE"
        stale.mkdir(parents=True)
        (stale / "f001.png").write_text("x")
        old_t = time.time() - 3 * 86400
        os.utime(str(stale / "f001.png"), (old_t, old_t))
        os.utime(str(stale), (old_t, old_t))
        r = subprocess.run([PY, RQ, "scratch", "JOB-OLD"], env=e, capture_output=True, text=True)
        check("scratch goes on the internal SSD while it has room", r.stdout.strip() == str(sc / "JOB-OLD"),
              r.stdout + r.stderr[-200:])
        check("... and scratch folders untouched for two days are deleted", not stale.exists(), list(sc.iterdir()))
        r = subprocess.run([PY, RQ, "scratch", "JOB-OLD"], env=dict(e, GATE_SCRATCH_RESERVE_GB="1000000"),
                           capture_output=True, text=True)
        check("... and inside the job's own folder when the internal SSD is short of space",
              r.stdout.strip() == str(db / "_edit_work" / "JOB-OLD" / "_scratch"), r.stdout + r.stderr[-200:])

        # 15. the census of work outside the queue: a busy Python counts; one waiting in line for its encode does not
        d = root / "census"
        e = env_for(d)
        e.pop("GATE_UNMANAGED")
        burn = "import time\nt=time.time()\nwhile time.time()-t<20: pass\n"
        # four busy processes in one build: one alone can show under 30% CPU when the Mac is saturated
        burn4 = "import os\nfor _ in range(3):\n    if os.fork() == 0: break\n" + burn
        outside = spawn([PY, "-c", burn4], e, start_new_session=True)      # its own build
        spawn([PY, RQ, "run", "--", "sleep", "20"], dict(e, GATE_UNMANAGED="0"))
        time.sleep(0.5)
        waiter = spawn([PY, "-c", "import subprocess,sys,threading,time\n"
                        "threading.Thread(target=lambda: exec({!r}), daemon=True).start()\n"
                        "subprocess.call([sys.executable, {!r}, 'run', '--', 'true'])\n".format(burn, RQ)],
                       dict(e, GATE_UNMANAGED="0"), start_new_session=True)
        wait_for(lambda: tickets(d), 10)                    # the waiter is in line
        time.sleep(3.0)                                     # ps's CPU figure is an average: let it rise
        code = ("import json,sys; sys.path.insert(0,%r); import renderq; "
                "print(json.dumps([b['pids'] for b in renderq._unmanaged(renderq.slot_states())]))" % str(HERE))
        r = subprocess.run([PY, "-c", code], env=e, capture_output=True, text=True, timeout=30)
        try:
            found = [p for b in json.loads(r.stdout.strip().splitlines()[-1]) for p in b]
        except (ValueError, IndexError):
            found = r.stderr[-300:]
        check("a busy Python outside the queue counts against the heavy pool", outside.pid in found,
              (found, subprocess.run(["ps", "-o", "pid=,pcpu=", "-g", str(outside.pid)], capture_output=True,
                                     text=True).stdout.split()))
        check("... but not a build whose next step is waiting in line", waiter.pid not in found, found)
        os.killpg(outside.pid, signal.SIGKILL)
        waiter.kill()
        subprocess.run(["pkill", "-f", "^sleep 20$"])
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
