#!/usr/bin/env python3
"""The two-build cap, counted in BUILDS (VIDEO-RULES.md "Video builds: never run more than two at once").

    python3 buildcap.py              the other builds this process would wait behind, right now
    python3 buildcap.py --selftest   the cases below, on made-up process tables

SINCE 2026-10-20 THE CAP IS ENFORCED BY THE RENDER QUEUE, `renderq/renderq.py` (`python3 renderq/renderq.py status`).
`wait(label)` now gets in line there. This file still does the counting the queue uses to see builds that bypass
it (`builds()`), and `python3 buildcap.py` still lists every build by its processes.

WHY THIS FILE EXISTS (2026-10-13). The counter this replaces matched command lines, one process at a time:

  * It counted the SHELL that launched the gate. `zsh -c "... python3 .claude/.../gate.py ..."` holds the gate's
    command in its own command line, so with one other match the gate saw two builds and waited for itself:
    74 minutes at 0 % CPU on RO-19 round 4, 22 minutes on SL-07 the same day. The shell lives until the gate
    exits, so that wait never ends.
  * It counted every ffmpeg process as a build. One render is a decoder and an encoder, so one render filled
    both slots.
  * Waiting tools counted each other. Three of them with nothing running would each see two "builds" and none
    would ever start.

WHAT COUNTS NOW.

  A WORKER is a process doing build work, told by its EXECUTABLE, never by text somewhere in a command line:
  ffmpeg, a Whisper binary, or Python running a script whose path matches BUILD_SCRIPT (the same four names
  as before). A shell is never a worker, whatever its command line says. Neither is grep, tail, nice or a
  watcher.

  A BUILD is every worker in one PROCESS GROUP: one launched command and everything it started. A render's
  Python, its decoder and its encoder are one build. If the group's leader is an application that starts
  commands without giving them a group of their own, the build is the launched command instead (the topmost
  shell or Python above the worker).

  THE CALLER'S OWN BUILD NEVER COUNTS: its process group, and the group of anything above or below it in the
  process tree.

  A WAITING build does not hold a slot. While `wait()` sleeps it keeps a child process alive whose command
  line carries MARK and the time the wait began, so every session sees it with `ps` and no file is shared.
  Waiters go first come, first served: a waiter counts running builds plus the waiters that began before it.

The cap itself is unchanged: two (Dan, measured 2026-08-27).
"""
import os
import re
import subprocess
import sys
import time

CAP = 2
POLL_S = 20
SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "csh", "tcsh", "fish"}
BUILD_SCRIPT = re.compile(r"whisper|render\.py|gate\.py|qc_style", re.I)
MARK = "buildcap:waiting:"
_OPTS = r"\s*(?:-(?![mc]\b)\S+\s+)*"


def read_table():
    """{pid: dict(ppid, pgid, stat, exe, cmd)} for every process. Two reads because the executable path and the
    command line both hold spaces (this project's folder does) and only the last `ps` column may."""
    def ps(cols):
        return subprocess.run(["ps", "-ww", "-Ao", cols], capture_output=True, text=True).stdout.splitlines()
    table = {}
    for line in ps("pid=,ppid=,pgid=,stat=,comm="):
        f = line.strip().split(None, 4)
        if len(f) == 5 and f[0].isdigit():
            table[int(f[0])] = dict(ppid=int(f[1]), pgid=int(f[2]), stat=f[3], exe=f[4], cmd="")
    for line in ps("pid=,command="):
        f = line.strip().split(None, 1)
        if len(f) == 2 and f[0].isdigit() and int(f[0]) in table:
            table[int(f[0])]["cmd"] = f[1]
    return table


def _base(p):
    return os.path.basename(p["exe"] or (p["cmd"].split() or [""])[0]).lstrip("-").lower()


def _script(p):
    """The script (or -m module) a Python process is running. Arguments after it are not read: a page server
    started with `--words final.whisper.json` is not a build."""
    cmd, exe = p["cmd"], p["exe"]
    args = cmd[len(exe):] if exe and cmd.startswith(exe) else (cmd.split(None, 1) + ["", ""])[1]   # an empty command line (a process mid-exit) has no args
    m = re.match(_OPTS + r"-m\s+(\S+)", args)
    if m:
        return m.group(1)
    if re.match(_OPTS + r"-c(?:\s|$)", args):
        return None
    m = re.search(r"(.+?\.py)(?=\s|$)", args)
    return m.group(1) if m else (args.split() or [None])[0]


def is_worker(p):
    base = _base(p)
    if base in SHELLS:
        return False
    if base == "ffmpeg" or "whisper" in base:
        return True
    if base.startswith("python"):
        s = _script(p)
        # the roll indexer yields to builds; it never holds a slot itself (its ffmpeg and Whisper children do)
        return bool(s and BUILD_SCRIPT.search(s) and "roll_sidecar.py" not in p["cmd"])
    return False


def _is_runner(p):
    base = _base(p)
    return base in SHELLS or base.startswith("python") or is_worker(p)


def _key(table, pid):
    """Which build a process belongs to."""
    p = table[pid]
    lead = table.get(p["pgid"])
    if lead is None or _is_runner(lead):
        return ("group", p["pgid"])
    top, seen = pid, {pid}
    while True:
        up = table[top]["ppid"]
        if up in seen or up not in table or not _is_runner(table[up]):
            return ("command", top)
        top = up
        seen.add(up)


def builds(table=None, me=None, since=None):
    """The OTHER builds that hold a slot against this process, one entry per build:
    dict(key, pids, cmd, waiting). `since` is when this process began waiting (default: now, so every build
    already waiting is ahead of it)."""
    table = read_table() if table is None else table
    table = {pid: p for pid, p in table.items() if "Z" not in p["stat"]}
    me = os.getpid() if me is None else me
    since = time.time() if since is None else since

    mine, pid, seen = set(), me, set()
    while pid in table and pid not in seen:                   # this process and everything above it
        seen.add(pid)
        mine.add(_key(table, pid))
        pid = table[pid]["ppid"]
    kids = {}
    for pid, p in table.items():
        kids.setdefault(p["ppid"], []).append(pid)
    below, stack = set(), [me]
    while stack:                                              # and everything below it
        for k in kids.get(stack.pop(), []):
            if k not in below:
                below.add(k)
                stack.append(k)
                mine.add(_key(table, k))

    groups = {}
    for pid, p in table.items():
        if is_worker(p):
            groups.setdefault(_key(table, pid), []).append(pid)
    waiting = {}                                              # build -> when its wait began
    for pid, p in table.items():
        m = re.search(re.escape(MARK) + r"(\d+)", p["cmd"])
        if m and p["ppid"] in table:
            k = _key(table, p["ppid"])
            waiting[k] = min(waiting.get(k, float("inf")), int(m.group(1)) / 1000.0)

    out = []
    for k, pids in sorted(groups.items()):
        if k in mine:
            continue
        # a build that is encoding is running, whatever else in it is waiting
        w = waiting.get(k) if not any(_base(table[q]) == "ffmpeg" for q in pids) else None
        if w is not None and (w, min(pids)) > (since, me):
            continue                                          # it began waiting after this process did
        lead = min(pids, key=lambda q: (_base(table[q]) == "ffmpeg", q))
        out.append(dict(key=k, pids=sorted(pids), cmd=table[lead]["cmd"], waiting=w is not None))
    return out


def describe(found):
    return "\n".join("    {} {} {:<7} pids {}: {}".format(
        b["key"][0], b["key"][1], "WAITING" if b["waiting"] else "running", ",".join(map(str, b["pids"])), b["cmd"][:150])
        for b in found) or "    none"


def _renderq():
    import importlib.util
    spec = importlib.util.spec_from_file_location("absbyai_renderq", os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "renderq", "renderq.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def wait(label, cap=CAP, quiet=False, poll=POLL_S, pool="heavy"):
    """Since 2026-10-20 a thin wrapper over the render queue (`renderq/renderq.py`): get in line, return at this
    caller's turn. The steps that follow are gated again at their own heavy work (the ffmpeg wrapper, Whisper,
    HyperFrames) and rank as a continuation of this video. `cap` and `poll` are kept for old callers only.
    If the queue cannot load, falls back to the old process count so a build is never stopped by it."""
    try:
        rq = _renderq()
    except Exception:
        return _wait_counting(label, cap, quiet, poll)
    rq.wait_turn(label, pool=pool, quiet=quiet)


def _wait_counting(label, cap=CAP, quiet=False, poll=POLL_S):
    """The pre-queue wait: return when fewer than `cap` other builds hold a slot."""
    since, told = time.time(), 0.0
    while True:
        found = builds(since=since)
        if len(found) < cap:
            return
        if not quiet and time.time() - told >= 600:
            print("WAIT {}: {} other builds hold the cap of {}; not taking another slot\n{}".format(
                label, len(found), cap, describe(found)), flush=True)
            told = time.time()
        try:                                                  # the sleep IS the marker other sessions read
            subprocess.run([sys.executable, "-c", "import sys,time; time.sleep(float(sys.argv[1]))",
                            str(poll), MARK + str(int(since * 1000))], stdin=subprocess.DEVNULL)
        except OSError:
            time.sleep(poll)


# ---------------------------------------------------------------------------------------------- selftest
def _selftest():
    PY = "/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python"
    FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
    GATE = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py"

    def table(*rows):
        return {pid: dict(ppid=ppid, pgid=pgid, stat="S", exe=exe, cmd=(exe + " " + args).strip())
                for pid, ppid, pgid, exe, args in rows}

    app = [(10, 1, 10, "/Applications/Claude.app/Contents/MacOS/Claude", ""),
           (11, 10, 11, "/Users/danielrose/Library/Application Support/Claude/claude-code/claude", "--model x")]
    # the two builds that were live when this was written: a render (Python, decoder, encoder, a third ffmpeg)
    # whose shell had exited, and a chain script running a sampler that runs ffmpeg
    render = [(100, 1, 99, PY, "recipe/r3_render.py"), (101, 100, 99, FF, "-v error -i base.mp4 -f rawvideo -"),
              (102, 100, 99, FF, "-y -f rawvideo -i - out.mp4"), (103, 100, 99, FF, "-ss 1.000 -i broll.mp4")]
    chain = [(200, 1, 200, "/bin/bash", "/Volumes/Extreme/_edit_work/ra07/r1_chain_b.sh"),
             (201, 200, 200, PY, "s62_sample.py"), (202, 201, 200, FF, "-nostdin -y -i roll.mp4 out.wav")]
    # the gate typed inline, by relative path, as it was on RO-19 round 4
    inline = "-c cd film && nice -n 5 python3 .claude/skills/_shared/deliver/gate.py film.mp4 --format longform"
    gate = [(300, 11, 300, "/bin/zsh", inline), (301, 300, 300, PY, GATE + " film.mp4 --format longform")]

    def waiter(pid, pgid, ms):
        return [(pid, 11, pgid, "/bin/zsh", "-c ./rungate.sh"), (pid + 1, pid, pgid, PY, GATE + " x.mp4"),
                (pid + 2, pid + 1, pgid, PY, "-c import sys,time; time.sleep(float(sys.argv[1])) 20 " + MARK + str(ms))]

    cases = []

    def case(name, got, want):
        cases.append((name, got == want, got, want))

    n = lambda rows, me, since=None: len(builds(table(*rows), me=me, since=since))        # noqa: E731

    case("the gate does not count the shell that launched it", n(app + gate, 301), 0)
    case("the gate with one render running sees one build, not four", n(app + gate + render, 301), 1)
    case("a render and a chain script are two builds, and the gate waits", n(app + gate + render + chain, 301), 2)
    case("a decoder and an encoder under one script are one build", n(app + chain, 301), 1)
    case("a build's own ffmpeg children are not counted against it", n(app + render, 100), 0)
    case("a gate run BY a render is that render's build", n(app + render + [(110, 100, 99, PY, GATE + " f.mp4")], 110), 0)
    case("a gate launched by absolute path, with spaces in it, is seen by another build", n(app + gate + render, 100), 1)
    case("a watcher that greps for gate.py is not a build",
         n(app + [(400, 11, 400, "/bin/zsh", "-c while pgrep -f gate.py; do sleep 5; done"),
                  (401, 400, 400, "/usr/bin/grep", "gate.py"), (402, 11, 402, "/usr/bin/tail", "-f logs/gate.log")], 301), 0)
    case("a page server whose arguments mention whisper is not a build",
         n(app + [(500, 11, 500, PY, "review_server.py 8867 --words final.whisper.json")], 301), 0)
    case("the whisper command line tool is a build",
         n(app + [(510, 11, 510, "/opt/homebrew/bin/python3.11", "/opt/homebrew/bin/whisper a.wav --model small")], 301), 1)
    case("python -m whisper is a build", n(app + [(520, 11, 520, PY, "-u -m whisper a.wav")], 301), 1)
    case("the roll indexer holds no slot until it starts ffmpeg",
         n(app + [(530, 11, 530, PY, "roll_sidecar.py build clip.mp4 --whisper")], 301), 0)
    case("a zombie is not a build",
         len(builds(dict(list(table(*app).items()) + [(600, dict(ppid=11, pgid=600, stat="Z", exe=FF, cmd="(ffmpeg)"))]),
                    me=301)), 0)
    # commands started by an application that gives them no process group of their own
    flat = [(700, 11, 11, "/bin/zsh", "-c python3 a_render.py"), (701, 700, 11, PY, "a_render.py"),
            (702, 701, 11, FF, "-i a"), (703, 701, 11, FF, "-i b"),
            (710, 11, 11, "/bin/zsh", "-c python3 b_render.py"), (711, 710, 11, PY, "b_render.py"),
            (720, 11, 11, "/bin/zsh", "-c python3 gate.py"), (721, 720, 11, PY, "gate.py f.mp4")]
    case("with no process groups, each launched command is its own build", n(app + flat, 721), 2)
    # waiting builds
    case("three waiters with nothing running: the first one goes",
         n(app + waiter(800, 800, 1000) + waiter(810, 810, 2000) + waiter(820, 820, 3000), 801, since=1.0), 0)
    case("... the second counts only the first",
         n(app + waiter(800, 800, 1000) + waiter(810, 810, 2000) + waiter(820, 820, 3000), 811, since=2.0), 1)
    case("... the third counts both and waits",
         n(app + waiter(800, 800, 1000) + waiter(810, 810, 2000) + waiter(820, 820, 3000), 821, since=3.0), 2)
    case("a newcomer does not jump the queue", n(app + gate + waiter(800, 800, 1000) + waiter(810, 810, 2000), 301), 2)
    case("a waiter does not count its own marker", n(app + waiter(800, 800, 1000), 801, since=1.0), 0)
    case("a build that is encoding is running even if part of it waits",
         n(app + waiter(800, 800, 9000) + [(805, 800, 800, FF, "-i x")], 301, since=1.0), 1)

    for name, ok, got, want in cases:
        print("{}  {}{}".format("ok  " if ok else "FAIL", name, "" if ok else "   got {}, want {}".format(got, want)))
    bad = sum(not c[1] for c in cases)
    print("\nbuildcap selftest: {} of {} pass".format(len(cases) - bad, len(cases)))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    found = builds()
    print("{} other build(s) hold a slot against this process (cap {}):\n{}".format(len(found), CAP, describe(found)))
