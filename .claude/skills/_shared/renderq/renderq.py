#!/usr/bin/env python3
"""The render queue: every heavy video step on this Mac waits its turn here (VIDEO-RULES.md, "Video builds").

    python3 renderq.py status                 who holds a slot, who is waiting, in order, with estimated starts
    python3 renderq.py run [opts] -- CMD...   run CMD once a slot is free (heavy by default; --light, --priority,
                                              --group VIDEO, --label TEXT)
    python3 renderq.py wait [--light]         get in line, return when it is this caller's turn (holds nothing)
    python3 renderq.py workdir JOB [--need GB] [--source PATH]   the job's work folder: its existing one, else a new
                                              one on the least busy drive with room (prints the path, creates it)
    python3 renderq.py scratch JOB [--need GB]  a scratch folder for throwaway frames and test renders: the internal
                                              SSD while it has room, else the job's own drive
    python3 renderq.py drives                 each drive: heavy steps running and waiting on it, its cap, free space
    python3 renderq.py why [TICKET]           why a waiting step has not started (all waiters, or one by its line
                                              number, pid, label or video)
    python3 renderq.py prune [--dry-run]      review servers older than 48 h: launchd-managed ones switch to start
                                              on demand (same link), hand-started ones are stopped and listed
    python3 renderq.py install-shim           put the ffmpeg wrapper in front of Media/video_edit/bin/ffmpeg
    python3 renderq.py uninstall-shim         put the real ffmpeg back
    python3 renderq.py selftest               queue order, priority, kill -9, nesting, exempt calls, drives, quick lane,
                                              core and memory budgets, -threads, RENDERQ_CORES

In Python:  `with renderq.slot("RO-27 picture pass"):` (heavy) or `renderq.slot(label, pool="light")`.
            `renderq.workdir("RO-27")`, `renderq.scratch_dir("RO-27")` return Paths.

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
* Three POOLS. HEAVY: an x264 encode, a full render, a HyperFrames render (each wants most of the 10 cores).
  LIGHT: Whisper, QC passes, single-threaded Python; they overlap a heavy encode almost for free. QUICK (since
  2026-10-20 evening): heavy work on SHORT media, an 8 s AI clip's frame dump, clip check or trim, a graphic of a
  few seconds; first come first served in its own two slots, so a one-second step never waits an hour behind
  long renders. Sizes come from Handoffs/results-20261020-render-scheduler.md and -renderq-drives.md.
* DRIVES. Each heavy step records the drives it reads and writes (Extreme, Expansion, Seagate, internal). A drive
  takes at most its cap of heavy steps at once (drives.json, measured by drivebench.py). A waiter whose drive is
  full steps aside: the next waiter on another drive goes past it, so a busy hard disk never idles the SSD.
* BUDGETS (v3, 2026-10-21, Handoffs/handoff-20261021-render-throughput-plan.md). A slot used to stand for "one
  encode", but a chroma key held one slot with six 1 GB workers: two slots meant 11 processes and 10.5 GB, swap
  filled and 27% of the CPU went to paging. Now every step carries a CORE ALLOWANCE (heavy 4, light 2, quick 2) and
  the line admits by two budgets: the cores in use plus the new step's must fit in the Mac's cores minus 2 (kept
  for the sessions, Chrome and the UI), and MEMORY must have had room for the last 30 s (at least 8 GB free or
  inactive, swap not growing, no memory-pressure warning). The FLOOR (two heavy, one light, two quick) always
  runs whatever the budgets say, so the line never stalls. The allowance is enforced: the holder exports
  RENDERQ_CORES (every Pool( sizes from it); the ffmpeg wrapper can add -threads/-filter_threads to any call that
  sets none (GATE_THREADS=1; off by default since the 10-21 bench, see THREADS_DEFAULT). `status` shows cores and GB per holder and why the line is closed; `why` explains one waiter.
* Builds that bypass the queue (an old script, another ffmpeg) and are using CPU count against the core budget
  (their CPU in whole cores), so the budget holds even before every tool is wired in.
* NESTING: a slot holder exports GATE_HELD; anything gated beneath it (a render's own encoder, a gate's own
  Whisper) runs straight through. A process whose parent or ancestor holds a slot also runs through, and so
  do the two ends of a pipe (decoder | encoder) once either end holds the slot.
* Work inside a slot runs at nice 10, so Chrome, review pages and the sessions themselves stay responsive.
* GATE_OFF=1 skips everything (debugging only).
"""
import ctypes
import fcntl
import json
import os
import re
import shutil
import signal
import struct
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

# (floor: always open whatever the budgets say, most at once). Slots past the floor open only while the core and
# memory budgets have room (see _budget_ok). GATE_POOLS="heavy=1:4,light=1:3" overrides (tests: "heavy=1").
# Heavy floor 2, not the plan's 1: with each heavy step held to 4 cores, two fill the 8-core budget exactly, and on
# 10-21 a floor of 1 ran the ten-step bench 2.1x slower than two at a time while swap still grew from work outside
# the queue (Handoffs/results-20261021-renderq-v3.md).
POOLS = {"heavy": (2, 4), "light": (1, 3), "quick": (2, 2)}
# Cores each step may use (the one table to tune). GATE_ALLOW="heavy=4,light=2,quick=2" overrides. Quick 2, not 1:
# one thread made an 8 s clip's PNG frame dump 3-4x slower (bench10, 10-21).
ALLOW = {"heavy": 4, "light": 2, "quick": 2}
CORES_RESERVED = 2                      # kept for the Claude/Codex sessions, Chrome, review pages and the UI
MEM_AVAIL_MIN_GB = 8.0                  # free + inactive + speculative + purgeable memory needed to start more
SWAP_GROW_MAX_MB = 64.0                 # swapped out more than this in the last 30 s: the Mac is paging; start nothing more
HEADROOM_S = 30.0                       # memory must have had room this long (not a 4 s snapshot: a key runs an hour)
RSS_EVERY_S = 10.0                      # how often holders' memory is measured (one ps for all)
# The wrapper's -threads injection is OFF by default (GATE_THREADS=1 turns it on for a process tree). Measured 10-21
# at load 70-200: capped to 4 threads, an x264 picture pass ran 2.5-3x slower than uncapped, because the rest of the
# Mac (chroma-key pools whose cv2/numpy start their own threads, work outside the queue) is not capped and takes the
# share. Turn it on once Phase 2's key and the other big thread users size themselves from RENDERQ_CORES.
THREADS_DEFAULT = False
QUICK_S = 20.0                          # heavy ffmpeg work on media this short (or capped this short) is QUICK
QUICK_FRAMES = 600                      # ... or this few frames
QUICK_CLIP_S = 15.0                     # clipcheck.py on a clip this short is QUICK
QUICK_HF_S = 10.0                       # a HyperFrames graphic this short is QUICK
DRIVES_FILE = HERE / "drives.json"      # measured per-drive caps (drivebench.py --save)
DRIVE_CAP_DEFAULT = 2                   # a drive drives.json does not know yet
SCRATCH = Path(os.environ.get("GATE_SCRATCH") or "/tmp/absbyai-scratch")   # internal SSD; Codex can write /tmp
SCRATCH_RESERVE_GB = 50.0               # the internal SSD keeps this much free (macOS swap grows into it)
SCRATCH_PRUNE_H = 48                    # a scratch folder nobody touched for this long is deleted
WORK_RESERVE_GB = {"Extreme": 30.0}     # a work drive keeps this much free (default below)
WORK_RESERVE_DEFAULT_GB = 100.0
WORK_DRIVES = ("Extreme", "Expansion", "Seagate")
# Job folders live in <drive>/_edit_work/<job>; Codex rounds also used <drive>/Abs By AI Edit Work/<job> (Expansion).
# Both are found and counted; new folders go in _edit_work.
WORK_FOLDERS = ("_edit_work", "Abs By AI Edit Work")
_JOB_IN_PATH = re.compile(r"/(?:_edit_work|Abs By AI Edit Work)/([^/]+)")
IDLE_WINDOW_S = 4.0                     # cpu_idle()'s window (status only since v3; admission reads the budgets)
SETTLE_S = 15.0                         # past the floor: nothing started in this pool (or heavy) this recently
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
    m = _JOB_IN_PATH.search(os.getcwd())
    if m:
        return "work:" + m.group(1)
    return "pg:{}".format(os.getpgid(0))


def _ps():
    """{pid: (ppid, pgid)} from one ps call; {} where ps is not allowed (Codex's workspace-write sandbox)."""
    out = {}
    try:
        r = subprocess.run(["ps", "-Ao", "pid=,ppid=,pgid="], capture_output=True, text=True)
    except OSError:
        return out
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


def _libsystem():
    if not _LIB:
        lib = ctypes.CDLL("/usr/lib/libSystem.dylib")
        lib.mach_host_self.restype = ctypes.c_uint
        _LIB.append(lib)
    return _LIB[0]


def _ticks():
    """Cumulative CPU ticks for the whole Mac: [user, system, idle, nice] (host_statistics, no subprocess)."""
    lib = _libsystem()
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


# ------------------------------------------------------------------------------------------------ budgets
def _kv_env(name, cast=float):
    out = {}
    for part in filter(None, (os.environ.get(name) or "").split(",")):
        k, _, v = part.partition("=")
        try:
            out[k.strip()] = cast(v)
        except ValueError:
            pass
    return out


def allowance(pool):
    """Cores a step in `pool` may use (exported to it as RENDERQ_CORES)."""
    return max(1, int(_kv_env("GATE_ALLOW", int).get(pool, ALLOW.get(pool, 1))))


def core_budget():
    """Cores the queue may hand out: the Mac's cores minus those kept for sessions and the UI."""
    if os.environ.get("GATE_BUDGET"):
        return int(os.environ["GATE_BUDGET"])
    return max(2, (os.cpu_count() or 10) - CORES_RESERVED)


def held_cores(info, pool):
    """Cores a slot holder was given (older holders did not say: their pool's allowance)."""
    try:
        return int(info.get("cores") or allowance(pool))
    except (TypeError, ValueError):
        return allowance(pool)


def unmanaged_cores(builds):
    """Builds outside the queue count by the cores they burn: 250% CPU is 3 cores."""
    return sum(max(1, int(-(-float(b.get("cpu", 100)) // 100))) for b in builds)


def cores_in_use(states, unmanaged=()):
    return (sum(held_cores(s["info"], s["pool"]) for s in states if s["held"])
            + unmanaged_cores(unmanaged))


_c = ctypes


class _VM64(ctypes.Structure):
    """vm_statistics64 (mach/vm_statistics.h): what vm_stat prints."""
    _fields_ = [("free", _c.c_uint32), ("active", _c.c_uint32), ("inactive", _c.c_uint32), ("wire", _c.c_uint32),
                ("zero_fill", _c.c_uint64), ("reactivations", _c.c_uint64), ("pageins", _c.c_uint64),
                ("pageouts", _c.c_uint64), ("faults", _c.c_uint64), ("cow_faults", _c.c_uint64),
                ("lookups", _c.c_uint64), ("hits", _c.c_uint64), ("purges", _c.c_uint64),
                ("purgeable", _c.c_uint32), ("speculative", _c.c_uint32), ("decompressions", _c.c_uint64),
                ("compressions", _c.c_uint64), ("swapins", _c.c_uint64), ("swapouts", _c.c_uint64),
                ("compressor_pages", _c.c_uint32), ("throttled", _c.c_uint32), ("external", _c.c_uint32),
                ("internal", _c.c_uint32), ("uncompressed_in_compressor", _c.c_uint64)]


def _sysctl(name, ctype):
    lib = _libsystem()
    val, size = ctype(), ctypes.c_size_t(ctypes.sizeof(ctype))
    if lib.sysctlbyname(name.encode(), ctypes.byref(val), ctypes.byref(size), None, ctypes.c_size_t(0)) != 0:
        raise OSError("sysctl " + name)
    return val


def mem_now():
    """dict(avail_gb, swap_used_mb, swapouts (pages, cumulative), pressure (1 normal, 2 warn, 4 critical)) from
    the kernel (host_statistics64 and sysctl: no subprocess). GATE_MEM="avail_gb,swap_grow_mb[,swap_used_mb]" fakes
    it for tests."""
    if os.environ.get("GATE_MEM"):
        f = [float(x) for x in os.environ["GATE_MEM"].split(",")]
        return dict(avail_gb=f[0], fake_grow_mb=f[1], swap_used_mb=f[2] if len(f) > 2 else 0.0, swapouts=0,
                    pressure=1, page=16384)
    lib = _libsystem()
    vm = _VM64()
    cnt = ctypes.c_uint(ctypes.sizeof(_VM64) // 4)
    if lib.host_statistics64(lib.mach_host_self(), 4, ctypes.byref(vm), ctypes.byref(cnt)) != 0:
        raise OSError("host_statistics64 failed")
    page = os.sysconf("SC_PAGESIZE")

    class XSW(ctypes.Structure):
        _fields_ = [("total", ctypes.c_uint64), ("avail", ctypes.c_uint64), ("used", ctypes.c_uint64),
                    ("pagesize", ctypes.c_uint32), ("encrypted", ctypes.c_uint32)]
    try:
        swap_used = _sysctl("vm.swapusage", XSW).used / 1048576.0
    except OSError:
        swap_used = 0.0
    try:
        pressure = _sysctl("kern.memorystatus_vm_pressure_level", ctypes.c_int).value
    except OSError:
        pressure = 1
    avail = (vm.free + vm.inactive + vm.speculative + vm.purgeable) * page / 1e9
    return dict(avail_gb=round(avail, 2), swap_used_mb=round(swap_used), swapouts=int(vm.swapouts),
                pressure=int(pressure), page=page)


def mem_state():
    """Memory now, swap growth over the last 30 s, and how long memory has had room without a break. Samples are
    shared in the queue folder (taken at most once a second by whoever looks), so a new waiter inherits the
    history instead of starting its own clock. A gap of over a minute with nobody looking restarts the clock."""
    p = DIR / "mem.json"
    st = _read(p)
    now = time.time()
    samples = st.get("samples", [])
    if samples and now - samples[-1][0] < 1.0 and st.get("last"):
        return st["last"]
    try:
        m = mem_now()
    except Exception as e:
        _log("mem_error", error=repr(e))
        return dict(ok=True, ok_for=1e9, avail_gb=None, reason="memory unreadable ({})".format(e))
    gap = now - samples[-1][0] if samples else 1e9
    samples = [s for s in samples if now - s[0] <= 45.0] if gap <= 60 else []
    samples.append([now, m["swapouts"]])
    old = [s for s in samples if now - s[0] >= 25.0] or samples[:1]
    grow_mb = m.get("fake_grow_mb", (m["swapouts"] - old[-1][1]) * m["page"] / 1048576.0)
    min_gb = float(os.environ.get("GATE_MEM_MIN_GB") or MEM_AVAIL_MIN_GB)
    if m["avail_gb"] < min_gb:
        reason = "memory: {:.2f} GB free or inactive (needs {:g})".format(m["avail_gb"], min_gb)
    elif grow_mb > SWAP_GROW_MAX_MB:
        reason = "memory: swapping ({:.0f} MB written to swap in the last 30 s; {:.1f} GB swap in use)".format(
            grow_mb, m["swap_used_mb"] / 1024.0)
    elif m["pressure"] >= 2:
        reason = "memory: macOS reports memory pressure ({})".format("critical" if m["pressure"] >= 4 else "warning")
    else:
        reason = ""
    ok_since = st.get("ok_since")
    if reason:
        ok_since = None
    elif ok_since is None or gap > 60:
        ok_since = now
    out = dict(ok=not reason, ok_for=round(now - ok_since, 1) if ok_since else 0.0, reason=reason,
               avail_gb=m["avail_gb"], swap_used_mb=m["swap_used_mb"], swap_grow_mb=round(grow_mb, 1),
               pressure=m["pressure"], t=now)
    try:
        _write(p, dict(samples=samples, ok_since=ok_since, last=out))
    except OSError:
        pass
    return out


def _settled(pool):
    """Past the floor, wait until the last step started in this pool (and the last heavy one) has had time to show
    its real CPU and memory."""
    a = _read(DIR / "admits.json")
    settle = float(os.environ.get("GATE_SETTLE", SETTLE_S))
    last = max(a.get(pool, 0), a.get("heavy", 0) if pool != "quick" else 0)
    return time.time() - last >= settle


def budget_check(pool, states, unmanaged=()):
    """May one more step start in `pool` now? '' when yes, else the reason in plain words. The floor always may."""
    base, most = pool_sizes()[pool]
    occupied = sum(1 for s in states if s["pool"] == pool and s["held"])
    if occupied >= most:
        return "{} slots all in use ({} of {})".format(pool, occupied, most)
    if occupied < base:
        return ""
    need, used, budget = allowance(pool), cores_in_use(states, unmanaged), core_budget()
    if used + need > budget:
        return "cores: {} of {} in use{}, this step needs {}".format(
            used, budget, " ({} by work outside the queue)".format(unmanaged_cores(unmanaged)) if unmanaged else "",
            need)
    if pool == "light" and used + need + allowance("heavy") > budget and _tickets("heavy"):
        return "cores: the last {} free cores are kept for a heavy step waiting in line".format(budget - used)
    m = mem_state()
    if not m["ok"]:
        return m["reason"]
    hold = float(os.environ.get("GATE_HEADROOM_S", HEADROOM_S))
    if m["ok_for"] < hold:
        return "memory: room for {:.0f} s of the {:g} s needed ({:.1f} GB free or inactive)".format(
            m["ok_for"], hold, m["avail_gb"] or 0)
    if not _settled(pool):
        return "settling: a step started under {:g} s ago; its load shows first".format(
            float(os.environ.get("GATE_SETTLE", SETTLE_S)))
    return ""


def _admitted(pool):
    p = DIR / "admits.json"
    d = _read(p)
    d[pool] = time.time()
    _write(p, d)


# ------------------------------------------------------------------------------------------------ drives
_VOL = re.compile(r"/Volumes/([^/]+)")
_VOL_IN_TEXT = re.compile(r"/Volumes/([^/\s'\"]+)/")
_NOT_A_DRIVE = ("Macintosh HD",)


def _test_map():
    """GATE_DRIVE_MAP="/tmp/a=FakeA,/tmp/b=FakeB" (tests): path prefixes that count as named drives."""
    out = []
    for part in filter(None, (os.environ.get("GATE_DRIVE_MAP") or "").split(",")):
        pre, _, name = part.rpartition("=")
        if pre and name:
            out.append((os.path.realpath(pre), name))
    return out


def drive_of(path, cwd=None):
    """The drive a path lives on: the volume name under /Volumes (Extreme, Expansion, Seagate) or "internal"."""
    try:
        p = path if os.path.isabs(path) else os.path.join(cwd or os.getcwd(), path)
        p = os.path.realpath(p)
    except (OSError, ValueError):
        return None
    for pre, name in _test_map():
        if p == pre or p.startswith(pre + "/"):
            return name
    m = _VOL.match(p)
    if m and m.group(1) not in _NOT_A_DRIVE:
        return m.group(1)
    return "internal"


def _path_like(x):
    return bool(x) and x != "-" and not x.startswith(("pipe:", "-", "http:", "https:", "rtmp:", "tcp:", "udp:",
                                                       "srt:", "data:")) and not ("=" in x and "/" not in x)


def _add(out, d):
    if d and d not in out:
        out.append(d)
    return out


def drives_in_text(text, cwd=None):
    """Drives a command line or label names (/Volumes/<drive>/...); if it names none, the drive of the folder it
    runs in (a tool started from the project folder on a clip on Extreme uses Extreme, not the internal disk)."""
    out = []
    for m in _VOL_IN_TEXT.finditer(text or ""):
        if m.group(1) not in _NOT_A_DRIVE:
            _add(out, m.group(1))
    for pre, name in _test_map():
        if pre in (text or ""):
            _add(out, name)
    if not out and cwd:
        _add(out, drive_of(cwd))
    return out


def default_drives():
    """A step's drives when its caller does not say: the folder it runs in, plus any drive its command names."""
    return drives_in_text(" ".join(sys.argv), os.getcwd())


def drive_caps():
    """{drive: most heavy steps at once}. drives.json (measured), then GATE_DRIVES="Extreme=3,Expansion=1"."""
    caps = dict(_read(DRIVES_FILE).get("caps", {}))
    for part in filter(None, (os.environ.get("GATE_DRIVES") or "").split(",")):
        k, _, v = part.partition("=")
        try:
            caps[k.strip()] = int(v)
        except ValueError:
            pass
    return caps


def drive_cap(name, caps):
    return int(caps.get(name, caps.get("default", DRIVE_CAP_DEFAULT)))


def info_drives(info):
    """The drives a slot holder or ticket uses. Older queue code did not record them: read its command and folder."""
    d = info.get("drives")
    if isinstance(d, list):
        return d
    return drives_in_text("{} {}".format(info.get("cmd", ""), info.get("label", "")), info.get("cwd"))


def drive_load(states, pool="heavy"):
    """{drive: heavy steps holding a slot that use it}"""
    load = {}
    for s in states:
        if s["held"] and s["pool"] == pool:
            for d in info_drives(s["info"]):
                load[d] = load.get(d, 0) + 1
    return load


def drive_full(drives, load, caps):
    """The drives in `drives` already running their cap of heavy steps."""
    return [d for d in drives or () if load.get(d, 0) >= drive_cap(d, caps)]


# ------------------------------------------------------------------------------------------------ media length
_SECS = {}


def _mp4_seconds(path):
    """Duration from an MP4/MOV's mvhd box, reading a few headers (no process); None if it cannot tell."""
    with open(path, "rb") as f:
        size = os.fstat(f.fileno()).st_size
        off = 0
        while off + 8 <= size:
            f.seek(off)
            h = f.read(16)
            if len(h) < 8:
                return None
            n, typ = struct.unpack(">I4s", h[:8])
            hl = 8
            if n == 1 and len(h) >= 16:
                n, hl = struct.unpack(">Q", h[8:16])[0], 16
            elif n == 0:
                n = size - off
            if n < 8:
                return None
            if typ == b"moov":
                p, end = off + hl, off + n
                while p + 8 <= end:
                    f.seek(p)
                    cn, ct = struct.unpack(">I4s", f.read(8))
                    if ct == b"mvhd":
                        body = f.read(32)
                        if len(body) < 20:
                            return None
                        if body[0] == 1 and len(body) >= 32:
                            ts, dur = struct.unpack(">IQ", body[20:32])
                        else:
                            ts, dur = struct.unpack(">II", body[12:20])
                        return dur / float(ts) if ts and dur else None
                    if cn < 8:
                        return None
                    p += cn
                return None
            off += n
    return None


def media_seconds(path, cwd=None):
    """How long a video or audio file runs, in seconds, or None. MP4/MOV read directly, others by ffprobe."""
    try:
        p = path if os.path.isabs(path) else os.path.join(cwd or os.getcwd(), path)
        st = os.stat(p)
    except (OSError, ValueError):
        return None
    key = (p, st.st_size, st.st_mtime)
    if key in _SECS:
        return _SECS[key]
    val = None
    try:
        if re.search(r"\.(mp4|mov|m4v|m4a|3gp)$", p, re.I):
            val = _mp4_seconds(p)
        if val is None:
            probe = BIN / "ffprobe"
            r = subprocess.run([str(probe if probe.exists() else "ffprobe"), "-v", "error", "-show_entries",
                                "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True, timeout=5)
            val = float(r.stdout.strip().splitlines()[0]) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        val = None
    _SECS[key] = val
    return val


def pool_for_media(path, default="heavy", short=QUICK_CLIP_S):
    """"quick" when `path` is a clip of at most `short` seconds, else `default`. For tools like clipcheck.py."""
    s = media_seconds(path) if path else None
    return "quick" if s is not None and s <= short else default


def pool_for_hyperframes(project_dir, default="heavy", short=QUICK_HF_S):
    """"quick" for a HyperFrames project whose root data-duration is at most `short` seconds."""
    try:
        html = (Path(project_dir) / "index.html").read_text()
        m = re.search(r'data-duration="([\d.]+)"', html)
        if m and float(m.group(1)) <= short:
            return "quick"
    except (OSError, ValueError):
        pass
    return default


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


def holder_rss(states, force=False):
    """{slot name: dict(pid, mb, peak_mb)}: each holder's resident memory summed over its whole process tree. One ps
    for every holder, at most every RSS_EVERY_S by whoever looks (waiters at the head of a line, `run` holders,
    status), kept with the peak in the queue folder."""
    p = DIR / "rss.json"
    c = _read(p)
    now = time.time()
    held = {"{}.{}".format(s["pool"], s["i"]): s["info"]["pid"] for s in states if s["held"] and s["info"].get("pid")}
    same = {k: v.get("pid") for k, v in c.get("slots", {}).items()} == held
    if not force and same and now - c.get("t", 0) < RSS_EVERY_S:
        return c.get("slots", {})
    try:
        r = subprocess.run(["ps", "-Ao", "pid=,ppid=,rss="], capture_output=True, text=True, timeout=10)
    except Exception:
        return c.get("slots", {})
    kids, rss = {}, {}
    for line in r.stdout.splitlines():
        f = line.split()
        if len(f) == 3 and f[0].isdigit() and f[2].isdigit():
            kids.setdefault(int(f[1]), []).append(int(f[0]))
            rss[int(f[0])] = int(f[2])
    old, out = c.get("slots", {}), {}
    for name, pid in held.items():
        seen, stack, kb = set(), [pid], 0
        while stack:
            q = stack.pop()
            if q not in seen:
                seen.add(q)
                kb += rss.get(q, 0)
                stack += kids.get(q, [])
        mb = int(round(kb / 1024.0))
        prev = old.get(name, {})
        out[name] = dict(pid=pid, mb=mb, peak_mb=max(mb, prev.get("peak_mb", 0)) if prev.get("pid") == pid else mb)
    try:
        _write(p, dict(t=now, slots=out))
    except OSError:
        pass
    return out


def _finish(info, info_path, end):
    """Record that a slot was let go (once), with the cores it had and the most memory it was seen using."""
    if not info.get("start") or info.get("ended"):
        return
    info["ended"] = end
    _write(info_path, info)
    rec = dict(pool=info.get("pool"), label=info.get("label"), group=info.get("group"), start=info["start"], end=end,
               dur=round(end - info["start"], 2), cores=info.get("cores"))
    r = _read(DIR / "rss.json").get("slots", {}).get("{}.{}".format(info.get("pool"), info.get("i")), {})
    if r and r.get("pid") == info.get("pid"):
        rec["peak_mb"] = r.get("peak_mb")
    try:
        with open(DIR / "history.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")
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
    up = _ancestors(os.getpid(), table) if table else [os.getppid()]    # no ps: the parent at least
    return any(a in holders for a in up)


# ------------------------------------------------------------------------------------------------ unmanaged
_BUSY_EXE = re.compile(r"^(ffmpeg(\.real)?|python[\d.]*|.*whisper.*|chrome-headless-shell)$")


def _unmanaged(states):
    """Builds using CPU that hold no slot, sit under no holder and are not waiting in line: an old script, a tool
    not wired in yet, the work a script does after `buildcap.wait()` handed its turn back, HyperFrames' Chrome run
    outside hfbuild, an ffmpeg called by its real name. Any ffmpeg, Python, Whisper or headless-Chrome process tree
    using UNMANAGED_CPU or more counts. Cached for a few seconds in the queue folder so waiters do not all run ps."""
    if os.environ.get("GATE_UNMANAGED") == "0":
        return []
    cache = DIR / "unmanaged.json"
    c = _read(cache)
    # v2: written by code that knows the quick lane and sees ffmpeg.real. Older waiters (still running the code
    # they started with) count quick-lane jobs as outside the queue; their census is not reused here.
    if c.get("v") == 2 and time.time() - c.get("t", 0) < UNMANAGED_EVERY_S:
        return c.get("builds", [])
    builds = []
    try:
        sys.path.insert(0, str(SHARED))
        import buildcap
        table = {pid: p for pid, p in buildcap.read_table().items() if "Z" not in p["stat"]}
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
        key = lambda pid: buildcap._key(table, pid)         # noqa: E731  one launched command and what it started
        members = {}
        for pid in table:
            members.setdefault(key(pid), []).append(pid)
        held = {key(q) for q in managed if q in table}
        waiting = {key(t["pid"]) for t in _tickets() if t.get("pid") in table}
        busy = {}
        for pid, p in table.items():
            if pid in managed or cpu.get(pid, 0.0) < 5.0:
                continue
            base = buildcap._base(p)
            if base in buildcap.SHELLS:
                continue
            if _BUSY_EXE.match(base) or (base == "node" and "hyperframes" in p["cmd"]):
                busy.setdefault(key(pid), []).append(pid)
        for k, pids in busy.items():
            if k in held or k in waiting:
                continue
            use = sum(cpu.get(q, 0.0) for q in pids)
            if use >= UNMANAGED_CPU:
                lead = max(pids, key=lambda q: cpu.get(q, 0.0))
                builds.append(dict(pids=sorted(pids), cpu=round(use), cmd=table[lead]["cmd"][:160]))
    except Exception as e:                                  # never let the census stop a build; where ps is not
        _log("unmanaged_error", error=repr(e))              # allowed (Codex sandbox), keep the last census
        return c.get("builds", [])
    try:
        _write(cache, dict(t=time.time(), builds=builds, v=2))
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


def _rank(tickets, states, pool=None):
    if pool == "quick":                                     # short steps: plain first come, first served, so a
        return sorted(tickets, key=lambda t: (0 if t.get("priority") else 1, t["seq"]))   # build's loop never hogs it
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
    def __init__(self, pool, label, group, priority, pipe=False, drives=None):
        _ensure()
        with _mutex():
            self.seq = _next_seq()
        self.drives = list(drives) if drives is not None else default_drives()
        self.info = dict(pid=os.getpid(), ppid=os.getppid(), pool=pool, label=label[:200], group=group,
                         priority=bool(priority), seq=self.seq, created=time.time(), cwd=os.getcwd()[:200],
                         session=_session(), pipe=pipe, drives=self.drives)
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
    for pool, (base, most) in pool_sizes().items():
        med = _history(pool)
        base = max(base, min(most, core_budget() // allowance(pool)))   # steps the core budget runs side by side
        free = []
        for s in states:
            if s["pool"] != pool:
                continue
            if s["held"]:
                el = now - s["info"].get("start", now)
                free.append(med - el if el < med else max(0.5 * el, 0.1 * med))
            elif s["i"] < base:
                free.append(0.0)
        free = free or [0.0]
        if pool == "heavy":
            free = sorted(free)
            for _ in _read(DIR / "unmanaged.json").get("builds", [])[:len(free)]:
                free[free.index(min(free))] = max(min(free), med / 2)
        ts = _rank([t for t in (tickets if tickets is not None else _tickets(pool)) if t["pool"] == pool], states,
                   pool)
        for t in ts:
            if not free:
                break
            k = free.index(min(free))
            out[str(t["path"])] = free[k]
            free[k] += med
    return out


RIDE = "ride"


def _admit(ticket, pool, group, idle=None, pipe=False):          # idle: unused since v3 (budgets decide)
    """One look at the line. Returns (fd, slot) when this waiter takes a slot, (RIDE, None) when the other end of
    its pipe now holds one, else (None, position). Under the mutex, so two ends of a pipe never both take slots.
    Heavy pool: a waiter whose drive already runs its cap does not count as ahead of anyone (it steps aside), and
    this waiter cannot start while one of its own drives is full."""
    with _mutex():
        states = slot_states()
        if pipe and pipe_partner_holds(states):
            return RIDE, None
        line = _rank(_tickets(pool), states, pool)
        pos = next((k for k, t in enumerate(line) if t["path"] == ticket.path), len(line))
        full = []
        if pool == "heavy":
            load, caps = drive_load(states), drive_caps()
            pos = sum(1 for t in line[:pos] if not drive_full(info_drives(t), load, caps))
            full = drive_full(ticket.drives, load, caps)
        if pos:
            return None, pos
        if full:
            return None, 0
        mine = [s for s in states if s["pool"] == pool]
        base = pool_sizes()[pool][0]
        unmanaged = _unmanaged(states) if sum(s["held"] for s in mine) >= base else []
        if budget_check(pool, states, unmanaged):           # past the floor: cores and memory must have room
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
            # Say who holds it before the mutex opens: a pipe partner or a waiter on the same drive looking a
            # moment later must see this holder, not the last one (two pipe ends took two slots, 2026-10-20).
            _write(s["path"], dict(pid=os.getpid(), ppid=os.getppid(), pgid=os.getpgid(0), pool=pool, i=s["i"],
                                   label=ticket.info["label"], group=group, start=now, cwd=ticket.info["cwd"],
                                   session=ticket.info["session"], drives=ticket.drives, pipe=pipe, kind="starting",
                                   cores=allowance(pool)))
            _admitted(pool)
            return fd, s
        return None, 0


class Hold(object):
    def __init__(self, fd, slot, pool, label, group, waited, drives=None):
        self.fd, self.slot, self.pool = fd, slot, pool
        self.name = "{}.{}".format(pool, slot["i"])
        self.info = dict(pid=os.getpid(), ppid=os.getppid(), pgid=os.getpgid(0), pool=pool, i=slot["i"],
                         label=label[:200], group=group, start=time.time(), waited=round(waited, 1),
                         cwd=os.getcwd()[:200], session=_session(), drives=list(drives or []),
                         cores=allowance(pool))

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


def acquire(label, pool="heavy", group=None, priority=None, quiet=False, pipe=False, passthrough=None, drives=None):
    """Wait in line for a slot in `pool`. Returns a Hold, or None if this caller is already inside a slot (or the
    queue is switched off). `passthrough()` is re-checked while waiting: True means run without a slot.
    `drives`: the drives this step reads and writes (default: its folder and any drive its command line names)."""
    if pool not in pools():
        raise ValueError("unknown pool " + pool)
    group = group or default_group()
    priority = os.environ.get("GATE_PRIORITY") == "1" if priority is None else priority
    _ensure()
    if covered_by_holder(pipe=pipe):                      # a parent, ancestor or pipe partner holds a slot
        return None
    ticket = Ticket(pool, label, group, priority, pipe=pipe, drives=drives)
    t0, told, said, head = time.time(), 0.0, False, False
    try:
        while True:
            fd, got = _admit(ticket, pool, group, pipe=pipe)
            if fd == RIDE:
                ticket.close()
                return None
            if fd is not None:
                ticket.close()
                hold = Hold(fd, got, pool, label, group, time.time() - t0, drives=ticket.drives)
                if said:
                    _say(quiet, "{} slot granted to {} after {}".format(pool, label, _fmt(time.time() - t0)))
                return hold
            if time.time() - told >= REMIND_S:
                with _mutex():
                    eta = estimate().get(str(ticket.path))
                _say(quiet, "{} waiting for a {} slot ({} in line{}). See: python3 {} status".format(
                    label, pool, "next" if got == 0 else "#{}".format(got + 1),
                    ", about {} to go".format(_fmt(eta)) if eta is not None else "", Path(__file__)))
                told, said = time.time(), True
            head = got == 0
            if head and pool != "quick":                        # outside the lock: ps is slow on a loaded Mac
                try:
                    mem_state()                                 # cached 1 s: keeps the shared 30 s memory clock fed
                    holder_rss(slot_states())                   # cached: one ps per RSS_EVERY_S for everyone
                except Exception:
                    pass
            time.sleep(POLL_HEAD_S if head or pipe else (POLL_S if got < 3 else 3 * POLL_S))
    except BaseException:
        ticket.close()
        raise


def _as_drives(drives):
    """None stays None (the default); paths become their drive names; names pass through."""
    if drives is None:
        return None
    if isinstance(drives, (str, Path)):
        drives = [drives]
    out = []
    for d in drives:
        d = str(d)
        _add(out, drive_of(d) if "/" in d else d)
    return out


@contextmanager
def slot(label, pool="heavy", group=None, priority=None, quiet=False, drives=None):
    """Hold a slot for the body of a `with`. Inside it, GATE_HELD tells every gated step below to run through,
    and this process runs at nice 10. Already inside a slot (or GATE_OFF=1): runs straight through.
    `drives`: paths or drive names the step reads and writes (default: its folder and its command line's drives)."""
    hold = None
    if os.environ.get("GATE_OFF") != "1":
        try:
            if not held_by_me():
                hold = acquire(label, pool=pool, group=group, priority=priority, quiet=quiet,
                               drives=_as_drives(drives))
        except Exception as e:                              # a queue problem never stops a build
            _log("slot_error", error=repr(e), label=label)
            hold = None
    if hold is None:
        yield None
        return
    prev, prev_cores = os.environ.get("GATE_HELD"), os.environ.get("RENDERQ_CORES")
    hold.publish(kind="python", cmd=" ".join(sys.argv)[:300])
    os.environ["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)
    os.environ["RENDERQ_CORES"] = str(hold.info["cores"])
    try:
        if os.getpriority(os.PRIO_PROCESS, 0) < NICE:
            os.setpriority(os.PRIO_PROCESS, 0, NICE)
    except OSError:
        pass
    try:
        yield hold
    finally:
        hold.release()
        for k, v in (("GATE_HELD", prev), ("RENDERQ_CORES", prev_cores)):
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


_KEEP = []


def hold_until_exit(label, pool="heavy", group=None, priority=None, quiet=False, drives=None):
    """For a script that is one step from start to finish: take a slot now and keep it until the process ends.
    The kernel lets it go however the script ends; children run straight through. Returns the Hold or None."""
    try:
        if os.environ.get("GATE_OFF") == "1" or held_by_me():
            return None
        hold = acquire(label, pool=pool, group=group, priority=priority, quiet=quiet, drives=_as_drives(drives))
    except Exception as e:                                  # a queue problem never stops a build
        _log("hold_error", error=repr(e), label=label)
        return None
    if hold is None:
        return None
    hold.publish(kind="script", cmd=" ".join(sys.argv)[:300])
    os.environ["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)
    os.environ["RENDERQ_CORES"] = str(hold.info["cores"])
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


def run(cmd, label=None, pool="heavy", group=None, priority=None, quiet=False, drives=None):
    """Run `cmd` inside a slot; returns its exit code. Signals are passed on to it."""
    label = label or " ".join(os.path.basename(c) if k == 0 else c for k, c in enumerate(cmd))[:120]
    env = dict(os.environ)
    hold = None
    try:
        if env.get("GATE_OFF") != "1" and not held_by_me():
            if drives is None:
                drives = drives_in_text(" ".join(cmd), os.getcwd())
            hold = acquire(label, pool=pool, group=group, priority=priority, quiet=quiet, drives=_as_drives(drives))
    except Exception as e:                                  # a queue problem never stops a build
        _log("run_error", error=repr(e), label=label)
        _say(quiet, "queue unavailable ({}); running without it".format(e))
        hold = None
    if hold is not None:
        hold.publish(kind="run", cmd=" ".join(cmd)[:300])
        env["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)
        env["RENDERQ_CORES"] = str(hold.info["cores"])

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
        while True:
            try:
                rc = child.wait(timeout=RSS_EVERY_S if hold else None)
                break
            except subprocess.TimeoutExpired:
                try:
                    holder_rss(slot_states())                   # this holder's memory, for status and history
                    mem_state()                                 # and the memory clock, while anything runs
                except Exception:
                    pass
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


def _parse(args):
    """An ffmpeg command line as inputs [(path, format or None, position)], outputs, {option: [values]} and
    [(option, value, position)] in order."""
    a = list(args)
    inputs, outputs, opts, seq = [], [], {}, []
    k, fmt = 0, None
    while k < len(a):
        x = a[k]
        if x == "-i" and k + 1 < len(a):
            inputs.append((a[k + 1], fmt, k))
            fmt = None
            k += 2
        elif x.startswith("-") and x != "-" and not re.match(r"-\d", x):
            if x in _FLAGS or k + 1 >= len(a):
                opts.setdefault(x, []).append(None)
                seq.append((x, None, k))
                k += 1
            else:
                opts.setdefault(x, []).append(a[k + 1])
                seq.append((x, a[k + 1], k))
                if x == "-f":
                    fmt = a[k + 1]
                k += 2
        else:
            outputs.append(x)
            k += 1
    return inputs, outputs, opts, seq


def _short_work(inputs, opts, seq, cwd=None):
    """Is this heavy call bounded to a short piece of media (QUICK_S seconds or QUICK_FRAMES frames)?"""
    vals = lambda *names: [v for n in names for v in opts.get(n, []) if v is not None]   # noqa: E731
    frames = [n for n in (_num(v) for v in vals("-frames:v", "-vframes", "-frames")) if n is not None]
    if frames and max(frames) <= QUICK_FRAMES:
        return True
    last_in = max([pos for _p, _f, pos in inputs] or [-1])
    ts = [(n, pos) for o, v, pos in seq if o == "-t" for n in [_num(v)] if n is not None]
    if ts and max(n for n, _pos in ts) <= QUICK_S and (any(pos > last_in for _n, pos in ts) or len(ts) >= len(inputs)):
        return True                                         # an output cap, or every input capped
    if "-stream_loop" in opts or "-loop" in opts or len(inputs) > 6:
        return False                                        # a looped input runs as long as it is told to
    total = 0.0
    for path, fmt, _pos in inputs:
        if fmt == "lavfi" or not _path_like(path) or "%" in path:
            return False
        sec = media_seconds(path, cwd)
        if sec is None:
            return False
        total += sec
        if total > QUICK_S:
            return False
    return bool(inputs)


def classify(args, cwd=None, lengths=True):
    """What an ffmpeg command line costs: ("exempt", why) | ("light", why) | ("quick", why) | ("heavy", why), and
    whether it is one end of a pipe. Exempt calls never wait (VIDEO-RULES: probes, frame grabs, stills, audio,
    stream copies, the hardware setup encode, anything a few seconds long). Quick: heavy work on short media.
    lengths=False skips reading clip lengths (exempt or not is all a step inside a holder's slot needs)."""
    a = list(args)
    if "-i" not in a:
        return "exempt", "no input (version, help, filter list)", False
    ins, outputs, opts, seq = _parse(a)
    inputs = [p for p, _f, _k in ins]
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
    try:
        if lengths and _short_work(ins, opts, seq, cwd):
            return "quick", "short media (under {:g} s)".format(QUICK_S), pipe
    except Exception:
        pass
    return "heavy", "video encode or decode", pipe


def ffmpeg_drives(args, cwd=None):
    """The drives an ffmpeg call reads and writes: its file inputs and outputs, else the folder it runs in."""
    ins, outputs, _opts, _seq = _parse(args)
    out = []
    for path, fmt, _k in ins:
        if fmt != "lavfi" and _path_like(path):
            _add(out, drive_of(path, cwd))
    for o in outputs:
        if _path_like(o) and o not in ("/dev/null", "NUL"):
            _add(out, drive_of(o, cwd))
    return out or [drive_of(cwd or os.getcwd())]


_OPTISH = re.compile(r"-[^\d.]")


def _ff_options(real):
    """The options this ffmpeg build lists in `-h full` (-filter_threads moved between versions). Asked once per
    binary and remembered in the queue folder."""
    try:
        st = os.stat(str(real))
    except OSError:
        return set()
    key = "{}:{}:{}".format(real, st.st_size, int(st.st_mtime))
    p = DIR / "ffcaps.json"
    c = _read(p)
    if c.get("key") != key:
        try:
            r = subprocess.run([str(real), "-hide_banner", "-h", "full"], capture_output=True, text=True, timeout=15,
                               env=dict(os.environ, GATE_OFF="1"))
            opts = sorted(set(re.findall(r"^\s*(-[a-z_]+)\s", r.stdout, re.M)))
        except Exception:
            opts = []
        c = dict(key=key, opts=opts)
        try:
            _ensure()
            _write(p, c)
        except OSError:
            pass
    return set(c.get("opts", []))


def with_threads(args, n, real=None):
    """`args` with the step's core allowance made real: `-threads n` before every input (decoder) and every output
    (encoder), plus `-filter_threads n` (and `-filter_complex_threads n` for a filter graph) when this ffmpeg knows
    them. A command that sets any thread count of its own is left exactly as it is. Tested on ffmpeg 6.0: same
    output streams, no new warnings on stderr (x264's info line reports threads=n instead of 7)."""
    a = [str(x) for x in args]
    if n <= 0 or "-i" not in a or any(x.startswith(("-threads", "-filter_threads", "-filter_complex_threads"))
                                      for x in a):
        return a
    at, k = [], 0
    while k < len(a):
        x = a[k]
        if x == "-i" and k + 1 < len(a):
            at.append(k)
            k += 2
        elif x.startswith("-") and x != "-" and _OPTISH.match(x):
            nxt = a[k + 1] if k + 1 < len(a) else None
            # a flag, unless its value follows; a value never looks like an option ("-1", "-0:a" and "-" do not)
            k += 1 if (x in _FLAGS or nxt is None or (nxt != "-" and _OPTISH.match(nxt))) else 2
        else:
            at.append(k)                                    # an output file
            k += 1
    for pos in sorted(at, reverse=True):
        a[pos:pos] = ["-threads", str(n)]
    head = []
    known = _ff_options(real) if real else set()
    if "-filter_threads" in known:
        head += ["-filter_threads", str(n)]
    if "-filter_complex_threads" in known and any(x in ("-filter_complex", "-lavfi", "-filter_complex_script")
                                                  for x in a):
        head += ["-filter_complex_threads", str(n)]
    return head + a


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
    args = list(args)
    try:
        cores = 0
        if env.get("GATE_OFF") == "1":
            pass
        elif held_by_me():                                  # inside a holder's slot: its allowance (RENDERQ_CORES)
            if classify(args, lengths=False)[0] != "exempt":
                cores = int(env.get("RENDERQ_CORES") or 0)
        else:
            pool, why, pipe = classify(args)
            if pool != "exempt":
                label = "ffmpeg {} -> {}".format(
                    os.path.basename(args[args.index("-i") + 1]) if "-i" in args[:-1] else "?",
                    os.path.basename(args[-1]) if args else "?")
                quiet = env.get("GATE_VERBOSE") != "1"
                hold = acquire(label, pool=pool, quiet=quiet, pipe=pipe,
                               passthrough=pipe_partner_holds if pipe else None, drives=ffmpeg_drives(args))
                if hold is None:
                    _rider(keep)
                    # one end of a pipe (or a step under a holder that dropped GATE_HELD): half the pair's allowance
                    cores = int(env.get("RENDERQ_CORES") or 0) or max(1, allowance(pool) // (2 if pipe else 1))
                else:
                    cores = hold.info["cores"]
                    hold.publish(kind="ffmpeg", cmd=("ffmpeg " + " ".join(args))[:300], pipe=pipe, why=why,
                                 parent_alive_pid=os.getppid())
                    os.set_inheritable(hold.fd, True)
                    env["GATE_HELD"] = "{}:{}".format(os.getpid(), hold.name)
                    env["RENDERQ_CORES"] = str(cores)
                    try:
                        if os.getpriority(os.PRIO_PROCESS, 0) < NICE:
                            os.setpriority(os.PRIO_PROCESS, 0, NICE)
                    except OSError:
                        pass
        if cores and (env.get("GATE_THREADS") == "1" or (THREADS_DEFAULT and env.get("GATE_THREADS") != "0")):
            args = with_threads(args, cores, real)
    except Exception as e:                                  # the queue must never break a build
        _log("shim_error", error=repr(e), args=" ".join(args)[:200])
    os.execv(str(real), [str(real)] + list(args))


# ------------------------------------------------------------------------------------------------ work + scratch
def _drive_root(name):
    for pre, n in _test_map():
        if n == name:
            return Path(pre)
    return Path("/Volumes") / name


def mounted_work_drives():
    """[(name, root)] for the work drives plugged in now (tests: GATE_DRIVE_MAP drives too)."""
    out = [(n, Path(p)) for p, n in _test_map()]
    if os.environ.get("GATE_DRIVE_MAP"):
        return out
    for name in WORK_DRIVES:
        root = Path("/Volumes") / name
        if root.is_dir() and os.path.ismount(str(root)):
            out.append((name, root))
    return out


def drive_kind(name):
    k = _read(DRIVES_FILE).get("drives", {}).get(name, {}).get("kind")
    return k or ("hdd" if name in ("Expansion", "Seagate") else "ssd")


def _free_gb(path):
    try:
        return shutil.disk_usage(str(path)).free / 1e9
    except OSError:
        return 0.0


def _recent_jobs(root, hours=3.0):
    """Job folders on a drive touched in the last few hours (the folder or one of its round folders)."""
    n, cut = 0, time.time() - hours * 3600
    jobs = []
    for folder in WORK_FOLDERS:
        try:
            jobs += list(os.scandir(str(root / folder)))
        except OSError:
            pass
    for j in jobs:
        try:
            if not j.is_dir() or j.name.startswith(("_", ".")):
                continue
            t = j.stat().st_mtime
            if t < cut:
                with os.scandir(j.path) as it:
                    t = max([t] + [e.stat().st_mtime for e in it if e.is_dir()])
            n += t >= cut
        except OSError:
            continue
    return n


def find_workdir(job):
    """The job's existing work folder on a plugged-in drive, or None (newest if it is on more than one)."""
    hits = []
    for _name, root in mounted_work_drives():
        for folder in WORK_FOLDERS:
            try:
                names = os.listdir(str(root / folder))
            except OSError:
                continue
            for n in names:                                 # exFAT is case-insensitive: return the real spelling
                p = root / folder / n
                if n.lower() == job.lower() and p.is_dir():
                    hits.append((p.stat().st_mtime, str(p)))
    return Path(max(hits)[1]) if hits else None


def drive_report(states=None, tickets=None):
    """One row per plugged-in work drive (plus internal): running, waiting, cap, free, kind, active jobs, score."""
    if states is None:
        _ensure()
        with _mutex():
            states, tickets = slot_states(), _tickets("heavy")
    caps, load = drive_caps(), drive_load(states)
    wait = {}
    for t in tickets or ():
        if t.get("pool", "heavy") == "heavy":
            for d in info_drives(t):
                wait[d] = wait.get(d, 0) + 1
    rows = []
    for name, root in mounted_work_drives() + [("internal", Path("/tmp"))]:
        cap = drive_cap(name, caps)
        active = _recent_jobs(root) if name != "internal" else 0
        run_, w = load.get(name, 0), wait.get(name, 0)
        rows.append(dict(drive=name, root=str(root), kind=drive_kind(name) if name != "internal" else "ssd",
                         running=run_, waiting=w, cap=cap, free_gb=round(_free_gb(root)), active_jobs=active,
                         score=round((run_ + 0.5 * w) / float(cap) + 0.15 * active, 2)))
    return rows


def workdir(job, need_gb=20.0, source=None, create=True, why=None):
    """The folder a job works in: its existing _edit_work folder (a job never splits across drives), else a new
    one on the plugged-in work drive with room that is least busy (heavy steps running and waiting there against
    its cap, plus job folders active in the last 3 h). SSD before hard disk on a tie; a hard disk that also holds
    the job's source footage counts as busier. `why` (a list) gets the scores."""
    hit = find_workdir(job)
    if hit:
        if why is not None:
            why.append("existing work folder")
        return hit
    src = drive_of(source) if source else None
    best = []
    for r in drive_report():
        if r["drive"] == "internal":
            continue
        reserve = float(os.environ.get("GATE_WORK_RESERVE_GB") or WORK_RESERVE_GB.get(r["drive"],
                                                                                      WORK_RESERVE_DEFAULT_GB))
        room = r["free_gb"] - need_gb - reserve
        score = r["score"] + (0.5 if src == r["drive"] and r["kind"] == "hdd" else 0.0)
        if why is not None:
            why.append("{}: score {:.2f} ({} running, {} waiting, cap {}, {} active jobs), {} GB free{}".format(
                r["drive"], score, r["running"], r["waiting"], r["cap"], r["active_jobs"], r["free_gb"],
                "" if room >= 0 else ", NO ROOM for {} GB + {} GB reserve".format(need_gb, reserve)))
        best.append((room < 0, score, r["kind"] != "ssd", -r["free_gb"], r["drive"], Path(r["root"])))
    if not best:
        raise RuntimeError("no work drive is plugged in (Extreme, Expansion or Seagate)")
    best.sort()
    if best[0][0]:                                          # nowhere has room: the most free space
        best.sort(key=lambda b: b[3])
    path = best[0][5] / "_edit_work" / job
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def _job_name(job=None):
    if job:
        return job
    g = os.environ.get("GATE_GROUP")
    if g:
        return g
    m = _JOB_IN_PATH.search(os.getcwd())
    return m.group(1) if m else "misc"


def _prune_scratch():
    """Delete scratch folders nobody touched for SCRATCH_PRUNE_H hours (looked at once every half hour)."""
    stamp = SCRATCH / ".pruned"
    try:
        if time.time() - stamp.stat().st_mtime < 1800:
            return
    except OSError:
        pass
    try:
        SCRATCH.mkdir(parents=True, exist_ok=True)
        stamp.touch()
        cut = time.time() - SCRATCH_PRUNE_H * 3600
        for j in os.scandir(str(SCRATCH)):
            if not j.is_dir() or j.is_symlink():
                continue
            newest = j.stat().st_mtime
            for base, dirs, files in os.walk(j.path):
                for f in dirs + files:
                    try:
                        newest = max(newest, os.lstat(os.path.join(base, f)).st_mtime)
                    except OSError:
                        pass
                if newest >= cut:
                    break
            if newest < cut:
                shutil.rmtree(j.path, ignore_errors=True)
                _log("scratch_pruned", folder=j.path)
    except OSError:
        pass


def scratch_dir(job=None, need_gb=2.0):
    """A folder for throwaway work: frame dumps, test renders, temporary intermediates nothing reads after the
    step that made them. On the internal SSD (fast, and off the busy external drives) while it keeps
    SCRATCH_RESERVE_GB free after `need_gb`; otherwise `_scratch` inside the job's work folder. Folders untouched
    for SCRATCH_PRUNE_H hours are deleted, so review images and anything Dan sees go in the work folder."""
    if os.environ.get("ABSBYAI_SCRATCH"):
        p = Path(os.environ["ABSBYAI_SCRATCH"])
        p.mkdir(parents=True, exist_ok=True)
        return p
    job = re.sub(r"[^\w.-]+", "_", _job_name(job))[:80]
    _prune_scratch()
    reserve = float(os.environ.get("GATE_SCRATCH_RESERVE_GB") or SCRATCH_RESERVE_GB)
    if _free_gb(SCRATCH.parent if SCRATCH.parent.exists() else "/tmp") - float(need_gb) >= reserve:
        p = SCRATCH / job
    else:
        p = workdir(job, need_gb=need_gb) / "_scratch"
    p.mkdir(parents=True, exist_ok=True)
    return p


# ------------------------------------------------------------------------------------------------ review servers
PRUNE_REVIEW_H = 48.0                   # `prune`: review servers running longer than this
REVIEW_SERVER = SHARED / "review_server.py"
_REVIEW_CMD = re.compile(r"review_server\.py\s+(\d+)(?:\s+(\S+))?|-m http\.server\s+(\d+)")


def _etime_s(v):
    """ps etime ([[dd-]hh:]mm:ss) in seconds."""
    days, _, rest = v.strip().rpartition("-")
    secs = 0
    for part in rest.split(":"):
        secs = secs * 60 + int(part)
    return secs + int(days or 0) * 86400


def review_servers():
    """Every running review page server: dict(pid, port, age_h, cmd, folder, kind) where kind is "on-demand" or
    "always" (a com.absbyai.review.PORT launch agent), "agent:<label>" (another launch agent restarts it) or "hand"
    (started by hand: nothing restarts it). GATE_PRUNE_MATCH (tests) limits it to commands containing that text."""
    import plistlib
    agents_dir = Path.home() / "Library" / "LaunchAgents"
    other = {}
    for pl in agents_dir.glob("*.plist") if agents_dir.is_dir() else []:
        if pl.name.startswith("com.absbyai.review."):
            continue
        try:
            d = plistlib.loads(pl.read_bytes())
        except Exception:
            continue
        args = " ".join(str(x) for x in d.get("ProgramArguments", []))
        m = _REVIEW_CMD.search(args)
        if m:
            other[m.group(1) or m.group(3)] = d.get("Label", pl.stem)
    r = subprocess.run(["ps", "-ww", "-Ao", "pid=,etime=,command="], capture_output=True, text=True)
    match = os.environ.get("GATE_PRUNE_MATCH")
    out = []
    for line in r.stdout.splitlines():
        f = line.split(None, 2)
        if len(f) < 3 or not f[0].isdigit():
            continue
        cmd = f[2]
        m = _REVIEW_CMD.search(cmd)
        if not m or "--remove" in cmd or "--on-demand" in cmd or (match and match not in cmd):
            continue
        port = m.group(1) or m.group(3)
        if not cmd.split()[0].lower().endswith(("python", "python3")) and "python" not in cmd.split()[0].lower():
            continue
        folder = m.group(2) if m.group(1) else None
        dm = re.search(r"--directory\s+(.+?)(?:\s+--|$)", cmd)
        if dm:
            folder = dm.group(1)
        plist = agents_dir / "com.absbyai.review.{}.plist".format(port)
        if plist.exists() and "AbsByAI Reviews/{}/".format(port) in cmd:
            try:
                kind = "on-demand" if "Sockets" in plistlib.loads(plist.read_bytes()) else "always"
            except Exception:
                kind = "always"
        elif port in other:
            kind = "agent:" + other[port]
        else:
            kind = "hand"
        out.append(dict(pid=int(f[0]), port=int(port), age_h=round(_etime_s(f[1]) / 3600.0, 1), cmd=cmd[:300],
                        folder=folder, kind=kind))
    return out


def prune(dry_run=False, hours=PRUNE_REVIEW_H):
    """Review servers running longer than `hours`: an always-running managed one switches to start on demand (same
    link, no process until the page is opened); one started by hand is stopped, and its restart command printed.
    One another launch agent restarts is only listed."""
    rows = [r for r in review_servers() if r["age_h"] >= hours]
    if not rows:
        print("no review server has run longer than {:g} h".format(hours))
        return 0
    verb = "would " if dry_run else ""
    done = 0
    for r in sorted(rows, key=lambda x: -x["age_h"]):
        head = "port {} (pid {}, running {:.0f} h)".format(r["port"], r["pid"], r["age_h"])
        if r["kind"] == "always":
            if dry_run:
                print("{}: {}switch to start on demand (same link)".format(head, verb))
                continue
            p = subprocess.run(["/usr/bin/python3", str(REVIEW_SERVER), str(r["port"]), "--on-demand"],
                               capture_output=True, text=True)
            print("{}: {}".format(head, (p.stdout.strip() or p.stderr.strip()[-200:]).splitlines()[-1]))
            done += p.returncode == 0
        elif r["kind"] == "hand":
            folder = r["folder"] or "."                     # no folder given: it serves the folder it started in
            if not folder.startswith("/"):
                try:
                    cwd = subprocess.run(["lsof", "-a", "-p", str(r["pid"]), "-d", "cwd", "-Fn"], capture_output=True,
                                         text=True).stdout
                    base = next((x[1:] for x in cwd.splitlines() if x.startswith("n")), "")
                    folder = os.path.normpath(os.path.join(base, folder)) if base else folder
                except OSError:
                    pass
            if not dry_run:
                try:
                    os.kill(r["pid"], signal.SIGTERM)
                    for _ in range(20):
                        time.sleep(0.1)
                        if not _alive(r["pid"]):
                            break
                    else:
                        os.kill(r["pid"], signal.SIGKILL)
                    done += 1
                    _log("review_pruned", port=r["port"], pid=r["pid"], folder=folder, age_h=r["age_h"])
                except OSError as e:
                    print("{}: could not stop it ({})".format(head, e))
                    continue
            print("{}: {} (started by hand, nothing restarts it). Folder: {}. Bring it back (it then starts on "
                  "demand) from the project folder with: python3 .claude/skills/_shared/review_server.py {} '{}'"
                  .format(head, "would be stopped" if dry_run else "stopped", folder, r["port"], folder))
        elif r["kind"].startswith("agent:"):
            print("{}: kept (launch agent {} restarts it)".format(head, r["kind"][6:]))
    if not dry_run:
        print("{} review server{} switched or stopped".format(done, "" if done == 1 else "s"))
    return 0


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
    rss = holder_rss(states)
    mem = mem_state()
    closed = {pool: budget_check(pool, states, unmanaged) for pool in pools()}
    budget = dict(cores_budget=core_budget(), cores_in_use=cores_in_use(states, unmanaged),
                  allowance={pool: allowance(pool) for pool in pools()}, memory=mem,
                  closed={k: v for k, v in closed.items() if v})
    if as_json:
        return json.dumps(dict(slots=[dict(pool=s["pool"], i=s["i"], held=s["held"],
                                           info=s["info"] if s["held"] else {},
                                           rss=rss.get("{}.{}".format(s["pool"], s["i"])) if s["held"] else None)
                                      for s in states],
                               budget=budget, unmanaged=unmanaged,
                               waiting=[dict({k: v for k, v in t.items() if k != "path"},
                                             eta_s=eta.get(str(t["path"]))) for t in _rank(tickets, states)],
                               drives=drive_report(states, tickets)),
                          indent=1)
    lines, p = [], pools()
    z = pool_sizes()
    held_mb = sum(r.get("mb", 0) for r in rss.values())
    lines.append("Render queue v3: steps start by CORES and MEMORY. Each step gets cores: heavy {}, light {}, quick {} "
                 "(exported as RENDERQ_CORES; ffmpeg -threads cap {}).".format(allowance("heavy"), allowance("light"),
                                                                  allowance("quick"),
                                                                  "on" if THREADS_DEFAULT else "off"))
    lines.append("Cores: {} of {} in use ({} of the Mac's {} kept for sessions and the UI){}.".format(
        budget["cores_in_use"], budget["cores_budget"], max(0, (os.cpu_count() or 10) - budget["cores_budget"]),
        os.cpu_count() or 10,
        "; {} of them by work outside the queue".format(unmanaged_cores(unmanaged)) if unmanaged else ""))
    if mem.get("avail_gb") is not None:
        lines.append("Memory: {:.1f} GB free or inactive (extra steps need {:g}), swap {:.1f} GB used, {:.0f} MB "
                     "swapped out in the last 30 s; room for {}. Slot holders use {:.1f} GB.".format(
                         mem["avail_gb"], float(os.environ.get("GATE_MEM_MIN_GB") or MEM_AVAIL_MIN_GB),
                         mem["swap_used_mb"] / 1024.0, mem.get("swap_grow_mb", 0),
                         _fmt(mem["ok_for"]) if mem["ok"] else "0 s ({})".format(mem["reason"]), held_mb / 1024.0))
    lines.append("Always open whatever the budgets say: {} heavy, {} light, {} quick. Past that: {}.".format(
        z["heavy"][0], z["light"][0], z["quick"][0],
        "; ".join("{} {}".format(k, "open" if not closed[k] else "closed, " + closed[k]) for k in p
                  if z[k][0] < z[k][1]) or "nothing more"))
    drows = drive_report(states, tickets)
    lines.append("Drives (heavy steps running/cap, waiting): " + "; ".join(
        "{} {}/{}{}, {} GB free".format(r["drive"], r["running"], r["cap"],
                                        ", {} waiting".format(r["waiting"]) if r["waiting"] else "", r["free_gb"])
        for r in drows))
    for pool in p:
        lines.append("")
        lines.append(pool.upper())
        for s in [x for x in states if x["pool"] == pool]:
            if s["held"]:
                i = s["info"]
                r = rss.get("{}.{}".format(s["pool"], s["i"]), {})
                lines.append("  slot {}: {}  [{}]  running {}, {} cores{}{}{}".format(
                    s["i"] + 1, i.get("label", "?"), i.get("group", ""), _ago(i.get("start")),
                    held_cores(i, s["pool"]),
                    ", {:.1f} GB (peak {:.1f})".format(r["mb"] / 1024.0, r["peak_mb"] / 1024.0)
                    if r.get("pid") == i.get("pid") else "",
                    ", waited {} first".format(_fmt(i["waited"])) if i.get("waited", 0) >= 1 else "",
                    ", " + i["session"] if i.get("session") else ""))
            else:
                lines.append("  slot {}: free".format(s["i"] + 1))
        if pool == "heavy":
            for b in unmanaged:
                n = unmanaged_cores([b])
                lines.append("  outside the queue (counts as {} core{}): {}% CPU, pid {}: {}".format(
                    n, "" if n == 1 else "s", b["cpu"], b["pids"][0], b["cmd"][:110]))
        line = _rank([t for t in tickets if t["pool"] == pool], states, pool)
        if pool == "heavy":
            load, caps = drive_load(states), drive_caps()
        if line:
            lines.append("  waiting, in order:")
        for n, t in enumerate(line, 1):
            e = eta.get(str(t["path"]))
            full = drive_full(info_drives(t), load, caps) if pool == "heavy" else []
            lines.append("   {:>2}. {}  [{}]  waiting {}{}{}{}".format(
                n, t.get("label", "?"), t.get("group", ""), _ago(t.get("created")),
                ", starts in about {}".format(_fmt(e)) if e is not None and not full else "",
                "  PRIORITY" if t.get("priority") else "",
                "  (its drive {} is full; later jobs on other drives go first)".format("/".join(full)) if full else ""))
    return "\n".join(lines)


def explain(query=None):
    """Why each waiting step (or the ones matching `query`: line number, pid, seq, label or video) has not started."""
    _ensure()
    with _mutex():
        states = slot_states()
        tickets = _tickets()
        unmanaged = _unmanaged(states)
        load, caps = drive_load(states), drive_caps()
        out = []
        for pool in pools():
            line = _rank([t for t in tickets if t["pool"] == pool], states, pool)
            gate = None
            for n, t in enumerate(line, 1):
                q = str(query or "")
                if q and q not in (str(n), str(t.get("pid")), str(t.get("seq"))) \
                        and q.lower() not in "{} {}".format(t.get("label", ""), t.get("group", "")).lower():
                    continue
                stepped = lambda u: pool == "heavy" and drive_full(info_drives(u), load, caps)   # noqa: E731
                full = drive_full(info_drives(t), load, caps) if pool == "heavy" else []
                ahead = [u for u in line[:n - 1] if not stepped(u)]
                if gate is None:
                    gate = budget_check(pool, states, unmanaged)
                if full:
                    r = ("its drive {} already runs its cap of heavy steps ({}); later steps on other drives go "
                         "first".format("/".join(full), "/".join(str(drive_cap(d, caps)) for d in full)))
                elif ahead:
                    r = "{} step{} ahead of it in the {} line{}".format(
                        len(ahead), "" if len(ahead) == 1 else "s", pool,
                        "; the line itself waits for: " + gate if gate else "")
                else:
                    r = gate or "nothing: it starts at its next look (under a second)"
                out.append("{} #{} {} [{}], waiting {}: {}".format(pool, n, t.get("label", "?"), t.get("group", ""),
                                                                   _ago(t.get("created")), r))
    if not out:
        return "nothing waiting{}".format(" matches " + repr(query) if query else "")
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------ CLI
def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "status":
        print(status(as_json="--json" in rest))
        return 0
    if cmd == "why":
        print(explain(rest[0] if rest else None))
        return 0
    if cmd == "prune":
        return prune(dry_run="--dry-run" in rest,
                     hours=float(rest[rest.index("--hours") + 1]) if "--hours" in rest else PRUNE_REVIEW_H)
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
        if not command or command[0] in ("-h", "--help", "help"):      # `run --help` once queued 70 min for "--help"
            sys.exit("usage: renderq.py run [--light] [--priority] [--group G] [--label L] -- command ...")
        return run(command, label=opts["label"], pool=opts["pool"], group=opts["group"], priority=opts["priority"],
                   quiet=opts["quiet"])
    if cmd in ("workdir", "scratch"):
        opts = dict(need=None, source=None, create=True, why=False)
        pos = []
        k = 0
        while k < len(rest):
            x = rest[k]
            if x in ("--need", "--source") and k + 1 < len(rest):
                opts[x[2:]] = rest[k + 1]
                k += 1
            elif x == "--no-create":
                opts["create"] = False
            elif x == "--why":
                opts["why"] = True
            else:
                pos.append(x)
            k += 1
        job = pos[0] if pos else None
        if cmd == "scratch":
            print(scratch_dir(job, need_gb=float(opts["need"] or 2)))
            return 0
        if not job:
            sys.exit("usage: renderq.py workdir JOB [--need GB] [--source PATH] [--no-create] [--why]")
        why = []
        print(workdir(job, need_gb=float(opts["need"] or 20), source=opts["source"], create=opts["create"], why=why))
        if opts["why"]:
            sys.stderr.write("\n".join(why) + "\n")
        return 0
    if cmd == "drives":
        if "--json" in rest:
            print(json.dumps(drive_report(), indent=1))
            return 0
        for r in drive_report():
            print("{:<10} {:<4} heavy {}/{} running, {} waiting, {:>6} GB free, {} job folders active in 3 h, "
                  "busy score {}".format(r["drive"], r["kind"], r["running"], r["cap"], r["waiting"], r["free_gb"],
                                         r["active_jobs"], r["score"]))
        return 0
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
    sys.exit("unknown command {}; try: status, why, run, wait, workdir, scratch, drives, prune, install-shim, "
             "selftest".format(cmd))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
