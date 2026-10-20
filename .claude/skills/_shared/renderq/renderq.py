#!/usr/bin/env python3
"""The render queue: every heavy video step on this Mac waits its turn here (VIDEO-RULES.md, "Video builds").

    python3 renderq.py status                 who holds a slot, who is waiting, in order, with estimated starts
    python3 renderq.py run [opts] -- CMD...   run CMD once a slot is free (heavy by default; --light, --priority,
                                              --group VIDEO, --label TEXT)
    python3 renderq.py wait [--light]         get in line, return when it is this caller's turn (holds nothing)
    python3 renderq.py install-shim           put the ffmpeg wrapper in front of Media/video_edit/bin/ffmpeg
    python3 renderq.py uninstall-shim         put the real ffmpeg back
    python3 renderq.py selftest               queue order, priority, kill -9, nesting, exempt calls

In Python:  `with renderq.slot("RO-27 picture pass"):` (heavy) or `renderq.slot(label, pool="light")`.

WHY (handoff 2026-10-20). The two-build cap was an honour system: only two shared tools waited, ten sessions that
started together all saw a free slot in the same second, and the Mac ran at load 40-160. Now the cap is a lock.

HOW.

* SLOTS are files under /tmp/absbyai-renderq/slots, one per slot, held with flock(). The kernel drops the lock the
  moment the holder exits for any reason (kill -9 included), so there is nothing to clean up and no PID file.
* The QUEUE is one ticket file per waiter, numbered from a shared counter, each flock()ed by its waiter. A ticket
  whose lock can be taken belongs to a dead waiter and is deleted on sight.
* Only the waiter at the HEAD of its pool's line may take a slot. Order: --priority / GATE_PRIORITY=1 first, then
  CONTINUATIONS (a video that holds a slot, or let one go in the last two minutes, so a started video finishes
  before new ones begin), then first come, first served.
* Two POOLS. HEAVY: an x264 encode, a full render, a HyperFrames render (each wants most of the 10 cores).
  LIGHT: Whisper, QC passes, single-threaded Python; they overlap a heavy encode almost for free. Sizes come
  from the measurement in Handoffs/results-20261020-render-scheduler.md.
* Builds that bypass the queue (an old script, another ffmpeg) and are using CPU count against the heavy pool,
  so the cap holds even before every tool is wired in.
* NESTING: a slot holder exports GATE_HELD; anything gated beneath it (a render's own encoder, a gate's own
  Whisper) runs straight through. A process whose parent or ancestor holds a slot also runs through, and so
  do the two ends of a pipe (decoder | encoder) once either end holds the slot.
* Work inside a slot runs at nice 10, so Chrome, review pages and the sessions themselves stay responsive.
* GATE_OFF=1 skips everything (debugging only).
"""
import fcntl
import json
import os
import re
import signal
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent
REPO = SHARED.parents[2]
# /tmp, not the home folder: Codex's workspace-write sandbox (the overnight queue's default) may write /tmp but not
# ~ (tested 2026-10-20). Every session must use the same folder or the line splits in two.
DIR = Path(os.environ.get("GATE_DIR") or "/tmp/absbyai-renderq")

# (always open, most at once). Slots past the first number open only while the Mac has spare CPU (see _burst_ok).
# Measured 2026-10-20, Handoffs/results-20261020-render-scheduler.md. GATE_POOLS="heavy=2:4,light=2:3" overrides.
POOLS = {"heavy": (2, 4), "light": (2, 3)}
IDLE_MIN = 0.40                         # an extra slot opens only if at least this share of the CPU sat idle ...
IDLE_WINDOW_S = 4.0                     # ... over this long ...
SETTLE_S = 15.0                         # ... and nothing started in that pool this recently (let it ramp up)
RESERVE_S = 0.6                         # a slot just let go stays with its build this long (its next step)
GRACE_S = 120                           # a video that let a slot go this recently is a continuation
POLL_HEAD_S = 0.2
POLL_S = 1.0
NICE = 10
UNMANAGED_CPU = 30.0                    # % CPU before a build outside the queue counts against the heavy pool
UNMANAGED_EVERY_S = 3.0
DEFAULT_DUR = {"heavy": 300.0, "light": 120.0}
REMIND_S = 600

BIN = REPO / "Media" / "video_edit" / "bin"
REAL_FFMPEG = BIN / "ffmpeg.real"


# ------------------------------------------------------------------------------------------------ plumbing
def pool_sizes():
    """{pool: (always open, most at once)}"""
    out = dict(POOLS)
    for part in filter(None, (os.environ.get("GATE_POOLS") or "").split(",")):
        k, v = part.split("=")
        lo, _, hi = v.partition(":")
        out[k.strip()] = (int(lo), int(hi or lo))
    return out


def pools():
    """{pool: most slots at once}"""
    return {k: v[1] for k, v in pool_sizes().items()}


def _ensure():
    for d in ("slots", "queue", "riders"):
        (DIR / d).mkdir(parents=True, exist_ok=True)


def _read(p):
    try:
        with open(p) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _write(p, obj):
    tmp = p.with_name("{}.{}.tmp".format(p.name, os.getpid()))
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, p)


def _trylock(path):
    """An fd holding an exclusive flock on `path`, or None if someone else holds it."""
    fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 0o666)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except OSError:
        os.close(fd)
        return None


def _locked(path):
    fd = _trylock(path)
    if fd is None:
        return True
    os.close(fd)
    return False


@contextmanager
def _mutex():
    fd = os.open(str(DIR / "admit.lock"), os.O_RDWR | os.O_CREAT, 0o666)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def _alive(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, TypeError):
        return False


def _log(event, **kw):
    try:
        kw.update(t=round(time.time(), 3), event=event)
        with open(DIR / "events.log", "a") as f:
            f.write(json.dumps(kw) + "\n")
    except OSError:
        pass


def _session():
    for k in ("CLAUDE_CODE_SESSION_ID", "CODEX_SESSION_ID", "CODEX_THREAD_ID"):
        if os.environ.get(k):
            return "{}:{}".format("codex" if k.startswith("CODEX") else "claude", os.environ[k][:8])
    return "codex" if any(k.startswith("CODEX") for k in os.environ) else ""


def default_group():
    """Which video a step belongs to: GATE_GROUP, else the _edit_work job folder it runs in, else its command."""
    g = os.environ.get("GATE_GROUP")
    if g:
        return g
    m = re.search(r"/_edit_work/([^/]+)", os.getcwd())
    if m:
        return "work:" + m.group(1)
    return "pg:{}".format(os.getpgid(0))


def _ps():
    """{pid: (ppid, pgid)} from one ps call."""
    out = {}
    r = subprocess.run(["ps", "-Ao", "pid=,ppid=,pgid="], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        f = line.split()
        if len(f) == 3 and f[0].isdigit():
            out[int(f[0])] = (int(f[1]), int(f[2]))
    return out


def _ancestors(pid, table):
    seen, out = set(), []
    while pid in table and pid not in seen and pid > 1:
        seen.add(pid)
        pid = table[pid][0]
        out.append(pid)
    return out


# ------------------------------------------------------------------------------------------------ CPU
_LIB = []
_SAMPLES = []


def _ticks():
    """Cumulative CPU ticks for the whole Mac: [user, system, idle, nice] (host_statistics, no subprocess)."""
    import ctypes
    if not _LIB:
        lib = ctypes.CDLL("/usr/lib/libSystem.dylib")
        lib.mach_host_self.restype = ctypes.c_uint
        _LIB.append(lib)
    lib = _LIB[0]
    arr, cnt = (ctypes.c_uint * 4)(), ctypes.c_uint(4)
    if lib.host_statistics(lib.mach_host_self(), 3, arr, ctypes.byref(cnt)) != 0:
        raise OSError("host_statistics failed")
    return list(arr)


def cpu_idle(window=IDLE_WINDOW_S):
    """Share of the CPU that sat idle over roughly the last `window` seconds, from samples this process takes
    each time it looks at the line; None until it has watched that long."""
    if os.environ.get("GATE_IDLE"):                       # tests
        return float(os.environ["GATE_IDLE"])
    try:
        now, tk = time.time(), _ticks()
    except Exception:
        return None
    _SAMPLES.append((now, tk))
    while _SAMPLES and now - _SAMPLES[0][0] > 30:
        _SAMPLES.pop(0)
    old = [x for x in _SAMPLES if now - x[0] >= window]
    if not old:
        return None
    d = [b - a for a, b in zip(old[-1][1], tk)]
    tot = sum(d)
    return d[2] / float(tot) if tot > 0 else None


def _burst_ok(pool, idle):
    """May a slot past the always-open ones start now? Only while the Mac has spare CPU, and only once the
    last job started in this pool has had time to show its real load."""
    last = _read(DIR / "admits.json").get(pool, 0)
    settle = float(os.environ.get("GATE_SETTLE", SETTLE_S))
    return idle is not None and idle >= IDLE_MIN and time.time() - last >= settle


def _admitted(pool):
    p = DIR / "admits.json"
    d = _read(p)
    d[pool] = time.time()
    _write(p, d)


# ------------------------------------------------------------------------------------------------ slots
def _slot_paths(pool, i):
    return DIR / "slots" / "{}.{}.lock".format(pool, i), DIR / "slots" / "{}.{}.json".format(pool, i)


def _history(pool):
    durs = []
    try:
        with open(DIR / "history.jsonl") as f:
            lines = f.readlines()[-400:]
    except OSError:
        lines = []
    for line in lines:
        try:
            h = json.loads(line)
        except ValueError:
            continue
        if h.get("pool") == pool and h.get("dur", 0) > 0.5:
            durs.append(h["dur"])
    durs = durs[-30:]
    return sorted(durs)[len(durs) // 2] if durs else DEFAULT_DUR.get(pool, 300.0)


def _finish(info, info_path, end):
    """Record that a slot was let go (once)."""
    if not info.get("start") or info.get("ended"):
        return
    info["ended"] = end
    _write(info_path, info)
    try:
        with open(DIR / "history.jsonl", "a") as f:
            f.write(json.dumps(dict(pool=info.get("pool"), label=info.get("label"), group=info.get("group"),
                                    start=info["start"], end=end, dur=round(end - info["start"], 2))) + "\n")
    except OSError:
        pass


def slot_states():
    """Every slot: dict(pool, i, lock, path, held, info). Marks newly freed slots as ended."""
    _ensure()
    out, now = [], time.time()
    for pool, n in pools().items():
        for i in range(n):
            lock, path = _slot_paths(pool, i)
            info = _read(path)
            held = _locked(lock)
            if not held and info.get("start") and not info.get("ended"):
                _finish(info, path, now)
            out.append(dict(pool=pool, i=i, lock=lock, path=path, held=held, info=info))
    return out


def held_by_me():
    """True if GATE_HELD names a slot that is really held right now by a living holder."""
    v = os.environ.get("GATE_HELD", "")
    m = re.match(r"(\d+):(\w+)\.(\d+)$", v)
    if not m:
        return False
    pid, pool, i = int(m.group(1)), m.group(2), int(m.group(3))
    lock, path = _slot_paths(pool, i)
    return _alive(pid) and _read(path).get("pid") == pid and _locked(lock)


def _holder_pids(states):
    return {s["info"].get("pid") for s in states if s["held"] and s["info"].get("pid")}


def _riders():
    """Pids running through on someone else's slot (pipe partners), still alive."""
    out = set()
    d = DIR / "riders"
    for p in d.glob("*.lock") if d.exists() else []:
        if _locked(p):
            try:
                out.add(int(p.stem))
            except ValueError:
                pass
        else:
            try:
                p.unlink()
            except OSError:
                pass
    return out


def pipe_partner_holds(states=None):
    """Is the other end of this process's pipe (a sibling under the same parent) holding a slot?"""
    states = slot_states() if states is None else states
    ppid = os.getppid()
    return any(s["held"] and s["info"].get("pipe") and s["info"].get("ppid") == ppid
               and s["info"].get("pid") != os.getpid() for s in states)


def covered_by_holder(states=None, table=None, pipe=False):
    """Is this process inside someone's slot already? Its parent or an ancestor holds one (even if GATE_HELD was
    dropped from its environment), or it is one end of a pipe whose other end holds one."""
    states = slot_states() if states is None else states
    holders = {s["info"]["pid"] for s in states if s["held"] and s["info"].get("pid")}
    if not holders:
        return False
    if pipe and pipe_partner_holds(states):
        return True
    table = _ps() if table is None else table
    return any(a in holders for a in _ancestors(os.getpid(), table))


# ------------------------------------------------------------------------------------------------ unmanaged
def _unmanaged(states):
    """Builds using CPU that hold no slot and sit under no holder: an old script, a tool not wired in yet.
    Cached for a few seconds in the queue folder so waiters do not all run ps."""
    if os.environ.get("GATE_UNMANAGED") == "0":
        return []
    cache = DIR / "unmanaged.json"
    c = _read(cache)
    if time.time() - c.get("t", 0) < UNMANAGED_EVERY_S:
        return c.get("builds", [])
    builds = []
    try:
        sys.path.insert(0, str(SHARED))
        import buildcap
        table = buildcap.read_table()
        managed = _holder_pids(states) | _riders()
        kids = {}
        for pid, p in table.items():
            kids.setdefault(p["ppid"], []).append(pid)
        stack = list(managed)
        while stack:                                        # everything under a holder is inside its slot
            for k in kids.get(stack.pop(), []):
                if k not in managed:
                    managed.add(k)
                    stack.append(k)
        cpu = {}
        r = subprocess.run(["ps", "-Ao", "pid=,pcpu="], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            f = line.split()
            if len(f) == 2 and f[0].isdigit():
                try:
                    cpu[int(f[0])] = float(f[1])
                except ValueError:
                    pass
        members = {}                                        # every process of a build, its Python included
        for pid in table:
            if "Z" not in table[pid]["stat"]:
                members.setdefault(buildcap._key(table, pid), []).append(pid)
        for b in buildcap.builds(table=table, me=os.getpid()):
            pids = members.get(b["key"], b["pids"])
            if b.get("waiting") or any(p in managed for p in pids):
                continue
            if b["key"][0] == "group" and table.get(b["key"][1], {}).get("exe", "").endswith(("claude", "Claude")):
                pids = b["pids"]                            # never charge a whole app to one build
            use = sum(cpu.get(p, 0.0) for p in pids)
            if use >= UNMANAGED_CPU:
                builds.append(dict(pids=b["pids"], cpu=round(use), cmd=b["cmd"][:160]))
    except Exception as e:                                  # never let the census stop a build
        _log("unmanaged_error", error=repr(e))
    try:
        _write(cache, dict(t=time.time(), builds=builds))
    except OSError:
        pass
    return builds


# ------------------------------------------------------------------------------------------------ queue
def _tickets(pool=None):
    """Living tickets (dead ones deleted), as dicts with path."""
    out = []
    for p in sorted((DIR / "queue").glob("*.json")):
        if p.name.startswith("."):
            continue
        if pool and not p.name.startswith(pool + "."):
            continue
        if not _locked(p):
            try:
                p.unlink()
            except OSError:
                pass
            continue
        t = _read(p)
        if t:
            t["path"] = p
            out.append(t)
    return out


def _active_groups(states):
    now, out = time.time(), set()
    for s in states:
        info = s["info"]
        if not info.get("group"):
            continue
        if s["held"] or now - info.get("ended", 0) < GRACE_S:
            out.add(info["group"])
    return out


def _rank(tickets, states):
    groups = _active_groups(states)

    def key(t):
        cls = 0 if t.get("priority") else (1 if t.get("group") in groups else 2)
        return (cls, t["seq"])
    return sorted(tickets, key=key)


def _next_seq():
    p = DIR / "seq"
    try:
        n = int(p.read_text().strip() or 0) + 1
    except (OSError, ValueError):
        n = 1
    p.write_text(str(n))
    return n


class Ticket(object):
    def __init__(self, pool, label, group, priority, pipe=False):
        _ensure()
        with _mutex():
            self.seq = _next_seq()
        self.info = dict(pid=os.getpid(), ppid=os.getppid(), pool=pool, label=label[:200], group=group,
                         priority=bool(priority), seq=self.seq, created=time.time(), cwd=os.getcwd()[:200],
                         session=_session(), pipe=pipe)
        name = "{}.{:010d}.{}.json".format(pool, self.seq, os.getpid())
        tmp = DIR / "queue" / (".tmp." + name)
        with open(tmp, "w") as f:
            json.dump(self.info, f)
        self.fd = _trylock(tmp)                            # locked before it becomes visible
        self.path = DIR / "queue" / name
        os.replace(tmp, self.path)

    def close(self):
        try:
            self.path.unlink()
        except OSError:
            pass
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


def estimate(states=None, tickets=None):
    """{ticket path: seconds until it should start}, simulated from recent durations."""
    states = slot_states() if states is None else states
    out, now = {}, time.time()
    for pool, (base, _most) in pool_sizes().items():
        med = _history(pool)
        free = []
        for s in states:
            if s["pool"] != pool:
                continue
            if s["held"]:
                el = now - s["info"].get("start", now)
                free.append(max(med - el, 0.1 * med))
            elif s["i"] < base:
                free.append(0.0)
        free = free or [0.0]
        if pool == "heavy":
            free = sorted(free)
            for _ in _read(DIR / "unmanaged.json").get("builds", [])[:len(free)]:
                free[free.index(min(free))] = max(min(free), med / 2)
        ts = _rank([t for t in (tickets if tickets is not None else _tickets(pool)) if t["pool"] == pool], states)
        for t in ts:
            if not free:
                break
            k = free.index(min(free))
            out[str(t["path"])] = free[k]
            free[k] += med
    return out


def _admit(ticket, pool, group, idle=None):
    """One look at the line. Returns (fd, slot) when this waiter takes a slot, else (None, position)."""
    with _mutex():
        states = slot_states()
        line = _rank(_tickets(pool), states)
        pos = next((k for k, t in enumerate(line) if t["path"] == ticket.path), len(line))
        if pos:
            return None, pos
        base, most = pool_sizes()[pool]
        mine = [s for s in states if s["pool"] == pool]
        occupied = sum(s["held"] for s in mine)
        if occupied >= most:
            return None, 0
        if pool == "heavy":
            occupied += len(_unmanaged(states))
            if occupied >= most:
                return None, 0
        if occupied >= base and not _burst_ok(pool, idle):
            return None, 0
        now = time.time()
        for s in mine:
            if s["held"]:
                continue
            info = s["info"]
            # just let go by a build that is still running: give its next step a moment to claim it
            if (info.get("group") != group and info.get("ended") and now - info["ended"] < RESERVE_S
                    and _alive(info.get("parent_alive_pid") or info.get("ppid"))):
                continue
            fd = _trylock(s["lock"])
            if fd is None:
                continue
            _admitted(pool)
            return fd, s
        return None, 0


class Hold(object):
    def __init__(self, fd, slot, pool, label, group, waited):
        self.fd, self.slot, self.pool = fd, slot, pool
        self.name = "{}.{}".format(pool, slot["i"])
        self.info = dict(pid=os.getpid(), ppid=os.getppid(), pgid=os.getpgid(0), pool=pool, i=slot["i"],
                         label=label[:200], group=group, start=time.time(), waited=round(waited, 1),
                         cwd=os.getcwd()[:200], session=_session())

    def publish(self, **extra):
        self.info.update(extra)
        _write(self.slot["path"], self.info)
        _log("granted", slot=self.name, label=self.info["label"], group=self.info["group"],
             waited=self.info["waited"])

    def release(self):
        if self.fd is None:
            return
        _finish(dict(self.info), self.slot["path"], time.time())
        os.close(self.fd)
        self.fd = None
        _log("released", slot=self.name, label=self.info["label"])


def _say(quiet, msg):
    if not quiet:
        sys.stderr.write("renderq: " + msg + "\n")
        sys.stderr.flush()


def _fmt(s):
    s = int(max(0, s))
    return "{} s".format(s) if s < 90 else "{} min".format(int(round(s / 60.0)))


def acquire(label, pool="heavy", group=None, priority=None, quiet=False, pipe=False, passthrough=None):
    """Wait in line for a slot in `pool`. Returns a Hold, or None if this caller is already inside a slot (or the
    queue is switched off). `passthrough()` is re-checked while waiting: True means run without a slot."""
    if pool not in pools():
        raise ValueError("unknown pool " + pool)
    group = group or default_group()
    priority = os.environ.get("GATE_PRIORITY") == "1" if priority is None else priority
    _ensure()
    if covered_by_holder(pipe=pipe):                      # a parent, ancestor or pipe partner holds a slot
        return None
    ticket = Ticket(pool, label, group, priority, pipe=pipe)
    t0, told, said, head = time.time(), 0.0, False, False
    try:
        while True:
            fd, got = _admit(ticket, pool, group, idle=cpu_idle() if head else None)
            if fd is not None:
                ticket.close()
                hold = Hold(fd, got, pool, label, group, time.time() - t0)
                if said:
                    _say(quiet, "{} slot granted to {} after {}".format(pool, label, _fmt(time.time() - t0)))
                return hold
            if passthrough and passthrough():
                return None
            if time.time() - told >= REMIND_S:
                with _mutex():
                    eta = estimate().get(str(ticket.path))
                _say(quiet, "{} waiting for a {} slot ({} in line{}). See: python3 {} status".format(
                    label, pool, "next" if got == 0 else "#{}".format(got + 1),
                    ", about {} to go".format(_fmt(eta)) if eta is not None else "", Path(__file__)))
                told, said = time.time(), True
            head = got == 0
            time.sleep(POLL_HEAD_S if head else (POLL_S if got < 3 else 3 * POLL_S))
    except BaseException:
        ticket.close()
        raise


@contextmanager
def slot(label, pool="heavy", group=None, priority=None, quiet=False):
    """Hold a slot for the body of a `with`. Inside it, GATE_HELD tells every gated step below to run through,
    and this process runs at nice 10. Already inside a slot (or GATE_OFF=1): runs straight through."""
    hold = None
    if os.environ.get("GATE_OFF") != "1":
        try:
            if not held_by_me():
                hold = acquire(label, pool=pool, group=group, priority=priority, quiet=quiet)
        except Exception as e:                              # a queue problem never stops a build
            _log("slot_error", error=repr(e), label=label)
            hold = None
    if hold is None:
        yield None
        return
    prev = os.environ.get("GATE_HELD")
    hold.publish(kind="python", cmd=" ".join(sys.argv)[:300])
    os.environ["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)
    try:
        if os.getpriority(os.PRIO_PROCESS, 0) < NICE:
            os.setpriority(os.PRIO_PROCESS, 0, NICE)
    except OSError:
        pass
    try:
        yield hold
    finally:
        hold.release()
        if prev is None:
            os.environ.pop("GATE_HELD", None)
        else:
            os.environ["GATE_HELD"] = prev


_KEEP = []


def hold_until_exit(label, pool="heavy", group=None, priority=None, quiet=False):
    """For a script that is one step from start to finish: take a slot now and keep it until the process ends.
    The kernel lets it go however the script ends; children run straight through. Returns the Hold or None."""
    try:
        if os.environ.get("GATE_OFF") == "1" or held_by_me():
            return None
        hold = acquire(label, pool=pool, group=group, priority=priority, quiet=quiet)
    except Exception as e:                                  # a queue problem never stops a build
        _log("hold_error", error=repr(e), label=label)
        return None
    if hold is None:
        return None
    hold.publish(kind="script", cmd=" ".join(sys.argv)[:300])
    os.environ["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)
    try:
        if os.getpriority(os.PRIO_PROCESS, 0) < NICE:
            os.setpriority(os.PRIO_PROCESS, 0, NICE)
    except OSError:
        pass
    _KEEP.append(hold)
    import atexit
    atexit.register(hold.release)
    return hold


guard = slot


def wait_turn(label, pool="heavy", quiet=False):
    """The old buildcap.wait(): get in line, return at this caller's turn, hold nothing afterwards. The work
    that follows is gated again at its own heavy steps, and ranks as a continuation of this video."""
    try:
        if os.environ.get("GATE_OFF") == "1" or held_by_me():
            return
        hold = acquire(label, pool=pool, quiet=quiet)
    except Exception as e:                                  # a queue problem never stops a build
        _log("wait_error", error=repr(e), label=label)
        return
    if hold is not None:
        hold.publish(kind="wait", cmd=" ".join(sys.argv)[:300])
        hold.release()


def run(cmd, label=None, pool="heavy", group=None, priority=None, quiet=False):
    """Run `cmd` inside a slot; returns its exit code. Signals are passed on to it."""
    label = label or " ".join(os.path.basename(c) if k == 0 else c for k, c in enumerate(cmd))[:120]
    env = dict(os.environ)
    hold = None
    try:
        if env.get("GATE_OFF") != "1" and not held_by_me():
            hold = acquire(label, pool=pool, group=group, priority=priority, quiet=quiet)
    except Exception as e:                                  # a queue problem never stops a build
        _log("run_error", error=repr(e), label=label)
        _say(quiet, "queue unavailable ({}); running without it".format(e))
        hold = None
    if hold is not None:
        hold.publish(kind="run", cmd=" ".join(cmd)[:300])
        env["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)

    def lower():
        try:
            if os.getpriority(os.PRIO_PROCESS, 0) < NICE:
                os.setpriority(os.PRIO_PROCESS, 0, NICE)
        except OSError:
            pass
    try:
        child = subprocess.Popen(cmd, env=env, preexec_fn=lower)
    except OSError as e:
        if hold:
            hold.release()
        _say(False, "could not start {}: {}".format(cmd[0], e))
        return 127

    def forward(sig, _frame):
        try:
            child.send_signal(sig)
        except OSError:
            pass
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, forward)
    try:
        rc = child.wait()
    finally:
        if hold:
            hold.release()
    return rc if rc >= 0 else 128 - rc


# ------------------------------------------------------------------------------------------------ ffmpeg calls
_IMG = re.compile(r"\.(jpe?g|png|webp|bmp|tiff?|gif)$", re.I)
_AUD = re.compile(r"\.(wav|mp3|m4a|aac|flac|opus|ogg|aiff?|caf)$", re.I)
_HW = re.compile(r"videotoolbox", re.I)
_FLAGS = set("""-y -n -nostdin -hide_banner -an -vn -sn -dn -shortest -stats -nostats -re -copyts -start_at_zero
-benchmark -benchmark_all -accurate_seek -noaccurate_seek -autorotate -noautorotate -ignore_unknown -report -xerror
-copytb_ -dump -hex -debug_ts -bitexact -apad_ -abort_on_ -print_graphs -stdin -noautoscale -autoscale""".split())
_AUDIO_FMTS = {"s16le", "s16be", "f32le", "f32be", "s32le", "u8", "wav", "mp3", "adts", "flac", "ogg", "opus",
               "aiff", "caf", "ipod_audio_"}


def _num(v):
    try:
        if ":" in v:
            secs = 0.0
            for part in v.split(":"):
                secs = secs * 60 + float(part)
            return secs
        return float(v.rstrip("s"))
    except ValueError:
        return None


def classify(args):
    """What an ffmpeg command line costs: ("exempt", why) | ("light", why) | ("heavy", why), and whether it is
    one end of a pipe. Exempt calls never wait (VIDEO-RULES: probes, frame grabs, stills, audio, stream copies,
    the hardware setup encode, anything a few seconds long)."""
    a = list(args)
    if "-i" not in a:
        return "exempt", "no input (version, help, filter list)", False
    inputs, outputs, opts = [], [], {}
    k = 0
    while k < len(a):
        x = a[k]
        if x == "-i" and k + 1 < len(a):
            inputs.append(a[k + 1])
            k += 2
        elif x.startswith("-") and x != "-" and not re.match(r"-\d", x):
            if x in _FLAGS or k + 1 >= len(a):
                opts.setdefault(x, []).append(None)
                k += 1
            else:
                opts.setdefault(x, []).append(a[k + 1])
                k += 2
        else:
            outputs.append(x)
            k += 1
    pipe = any(p in ("-", "pipe:", "pipe:0", "pipe:1") for p in inputs + outputs)
    vals = lambda *names: [v for n in names for v in opts.get(n, []) if v is not None]   # noqa: E731
    for v in vals("-frames:v", "-vframes", "-frames"):
        n = _num(v)
        if n is not None and n <= 30:
            return "exempt", "a few frames", pipe
    if outputs and all(_IMG.search(o) and "%" not in o for o in outputs):
        return "exempt", "a still image", pipe
    video_out = re.compile(r"\.(mp4|mov|mkv|m4v|avi|webm|mxf|ts|y4m|yuv|nut|gif)$", re.I)
    if "-vn" in opts or (outputs and all(_AUD.search(o) for o in outputs)) \
            or (vals("-f") and all(f in _AUDIO_FMTS for f in vals("-f"))):
        return "exempt", "audio only", pipe
    if inputs and all(_AUD.search(i) for i in inputs) and not any(video_out.search(o) for o in outputs):
        return "exempt", "audio only", pipe
    codecs = vals("-c:v", "-vcodec", "-codec:v", "-c", "-codec", "-c:v:0")
    if codecs and all(c == "copy" for c in codecs) and not vals("-vf", "-filter_complex", "-lavfi", "-filter:v"):
        return "exempt", "stream copy", pipe
    if any(_HW.search(c) for c in codecs):
        return "exempt", "hardware encoder (setup copy)", pipe
    durs = [n for n in (_num(v) for v in vals("-t")) if n is not None]
    if durs and max(durs) <= 5.0:
        return "exempt", "under five seconds", pipe
    fmts = vals("-f")
    if "null" in fmts or any(o in ("/dev/null", "NUL") for o in outputs):
        return "light", "analysis pass", pipe
    return "heavy", "video encode or decode", pipe


def _rider(fd_keep):
    """Register this process as running on a partner's slot; the lock goes with it through exec."""
    _ensure()
    p = DIR / "riders" / "{}.lock".format(os.getpid())
    fd = _trylock(p)
    if fd is not None:
        os.set_inheritable(fd, True)
        fd_keep.append(fd)


def ffmpeg_main(real, args):
    """Entry from the ffmpeg wrapper. Decides, waits if it must, then becomes the real ffmpeg (exec), which
    inherits the slot's lock: the slot is free the instant ffmpeg exits. Never writes to stdout or stderr
    (voice_chain parses ffmpeg's stderr) unless GATE_VERBOSE=1."""
    keep = []
    env = os.environ
    try:
        if env.get("GATE_OFF") != "1" and not held_by_me():
            pool, why, pipe = classify(args)
            if pool != "exempt":
                label = "ffmpeg {} -> {}".format(
                    os.path.basename(args[args.index("-i") + 1]) if "-i" in args[:-1] else "?",
                    os.path.basename(args[-1]) if args else "?")
                quiet = env.get("GATE_VERBOSE") != "1"
                hold = acquire(label, pool=pool, quiet=quiet, pipe=pipe,
                               passthrough=pipe_partner_holds if pipe else None)
                if hold is None:
                    _rider(keep)
                else:
                    hold.publish(kind="ffmpeg", cmd=("ffmpeg " + " ".join(args))[:300], pipe=pipe, why=why,
                                 parent_alive_pid=os.getppid())
                    os.set_inheritable(hold.fd, True)
                    env["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)
                    try:
                        if os.getpriority(os.PRIO_PROCESS, 0) < NICE:
                            os.setpriority(os.PRIO_PROCESS, 0, NICE)
                    except OSError:
                        pass
    except Exception as e:                                  # the queue must never break a build
        _log("shim_error", error=repr(e), args=" ".join(args)[:200])
    os.execv(str(real), [str(real)] + list(args))


# ------------------------------------------------------------------------------------------------ shim install
SHIM = """#!/bin/sh
# Render queue wrapper (.claude/skills/_shared/renderq/README.md). The real ffmpeg is ffmpeg.real beside this file.
# Heavy calls wait their turn; probes, frame grabs, audio and stream copies run at once. GATE_OFF=1 skips the queue.
REAL="{real}"
PY="{shimpy}"
if [ "$GATE_OFF" = "1" ] || [ ! -f "$PY" ] || [ ! -x /usr/bin/python3 ]; then exec "$REAL" "$@"; fi
exec /usr/bin/python3 -E -s "$PY" "$REAL" "$@"
"""


def install_shim():
    ff = BIN / "ffmpeg"
    if not REAL_FFMPEG.exists():
        if not ff.exists() or ff.stat().st_size < 1000000:
            sys.exit("no real ffmpeg binary at {}".format(ff))
        os.link(ff, REAL_FFMPEG)                          # a second name for the same file: no gap
    elif ff.exists() and ff.stat().st_size > 1000000:
        sys.exit("both ffmpeg and ffmpeg.real are real binaries; sort that out by hand")
    tmp = BIN / ".ffmpeg.shim.tmp"
    tmp.write_text(SHIM.format(real=REAL_FFMPEG, shimpy=HERE / "ffshim.py"))
    os.chmod(tmp, 0o755)
    os.replace(tmp, ff)
    print("installed: {} -> queue -> {}".format(ff, REAL_FFMPEG))


def uninstall_shim():
    ff = BIN / "ffmpeg"
    if REAL_FFMPEG.exists():
        os.replace(REAL_FFMPEG, ff)
        print("restored the real ffmpeg at {}".format(ff))
    else:
        print("nothing to undo")


# ------------------------------------------------------------------------------------------------ status
def _ago(t):
    return _fmt(time.time() - t) if t else "?"


def status(as_json=False):
    _ensure()
    with _mutex():
        states = slot_states()
        tickets = _tickets()
    unmanaged = _unmanaged(states)
    eta = estimate(states, tickets)
    if as_json:
        return json.dumps(dict(slots=[dict(pool=s["pool"], i=s["i"], held=s["held"],
                                           info=s["info"] if s["held"] else {}) for s in states],
                               unmanaged=unmanaged,
                               waiting=[dict({k: v for k, v in t.items() if k != "path"},
                                             eta_s=eta.get(str(t["path"]))) for t in _rank(tickets, states)]),
                          indent=1)
    lines, p = [], pools()
    z = pool_sizes()
    lines.append("Render queue. Heavy (renders, encodes): {} slots always open, up to {} while the Mac has spare CPU."
                 .format(*z["heavy"]))
    lines.append("Light (Whisper, checks): {} always open, up to {}.".format(*z["light"]))
    for pool in p:
        lines.append("")
        lines.append(pool.upper())
        for s in [x for x in states if x["pool"] == pool]:
            if s["held"]:
                i = s["info"]
                lines.append("  slot {}: {}  [{}]  running {}{}{}".format(
                    s["i"] + 1, i.get("label", "?"), i.get("group", ""), _ago(i.get("start")),
                    ", waited {} first".format(_fmt(i["waited"])) if i.get("waited", 0) >= 1 else "",
                    ", " + i["session"] if i.get("session") else ""))
            else:
                lines.append("  slot {}: free".format(s["i"] + 1))
        if pool == "heavy":
            for b in unmanaged:
                lines.append("  outside the queue (counts as a heavy slot): {}% CPU, pid {}: {}".format(
                    b["cpu"], b["pids"][0], b["cmd"][:110]))
        line = _rank([t for t in tickets if t["pool"] == pool], states)
        if line:
            lines.append("  waiting, in order:")
        for n, t in enumerate(line, 1):
            e = eta.get(str(t["path"]))
            lines.append("   {:>2}. {}  [{}]  waiting {}{}{}".format(
                n, t.get("label", "?"), t.get("group", ""), _ago(t.get("created")),
                ", starts in about {}".format(_fmt(e)) if e is not None else "",
                "  PRIORITY" if t.get("priority") else ""))
    return "\n".join(lines)


# ------------------------------------------------------------------------------------------------ CLI
def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "status":
        print(status(as_json="--json" in rest))
        return 0
    if cmd in ("run", "wait"):
        opts = dict(pool="heavy", group=None, priority=None, label=None, quiet=False)
        k = 0
        while k < len(rest) and rest[k] != "--":
            x = rest[k]
            if x == "--light":
                opts["pool"] = "light"
            elif x == "--heavy":
                opts["pool"] = "heavy"
            elif x == "--priority":
                opts["priority"] = True
            elif x == "--quiet":
                opts["quiet"] = True
            elif x in ("--group", "--label") and k + 1 < len(rest):
                opts[x[2:]] = rest[k + 1]
                k += 1
            elif cmd == "run":
                break
            k += 1
        if cmd == "wait":
            wait_turn(opts["label"] or "wait", pool=opts["pool"], quiet=opts["quiet"])
            return 0
        command = rest[k + 1:] if k < len(rest) and rest[k] == "--" else rest[k:]
        if not command:
            sys.exit("usage: renderq.py run [--light] [--priority] [--group G] [--label L] -- command ...")
        return run(command, label=opts["label"], pool=opts["pool"], group=opts["group"], priority=opts["priority"],
                   quiet=opts["quiet"])
    if cmd == "install-shim":
        install_shim()
        return 0
    if cmd == "uninstall-shim":
        uninstall_shim()
        return 0
    if cmd == "selftest":
        sys.path.insert(0, str(HERE))
        import selftest
        return selftest.main()
    sys.exit("unknown command {}; try: status, run, wait, install-shim, selftest".format(cmd))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
