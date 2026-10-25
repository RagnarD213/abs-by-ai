#!/usr/bin/env python3
"""Active edit cap: at most 5 video edits doing production work at once, Claude and Codex together (Dan, 2026-10-21).

The render queue (renderq) caps heavy STEPS; this caps how many EDITS feed it. An edit that is fired while 5 are
active registers as waiting and starts on its own when a slot frees. Waiters start in release-date order
(Docs/LONGFORM_RELEASE_CALENDAR.md, Docs/SHORTS_RELEASE_CALENDAR.md), not firing order. Ads (RA-xx) rank with the
nearest upcoming release. Undated and 2027 work goes last. Rule: VIDEO-RULES.md, "Active edit cap".

    editcap.py acquire JOB [--title T] [--type LFC|SFC|SFL|AD] [--release YYYY-MM-DD]
                                    exit 0 = go (slot held, also refreshes it), 3 = waiting (do not produce)
    editcap.py wait JOB [--max-hours 24]
                                    blocks until JOB holds a slot, then exits 0 (run it in the background:
                                    the session is re-invoked when it exits). Exit 4 = gave up after max hours.
    editcap.py release JOB [--review]
                                    --review: the edit now waits on Dan (review page up, awaiting picks): slot freed,
                                    acquire again when his notes arrive. Without it: the edit is finished.
    editcap.py status [--json]      read-only: active edits, waiting list in start order and why
    editcap.py wakes [--claim] [--ai claude|codex]
                                    promoted waiters whose auto-start process is not running (send them a message)
    editcap.py forget JOB           drop an entry (cleanup)
    editcap.py selftest

Production work = renderq jobs, AI generation, builds. Setup/upload tasks and thumbnail picks are exempt and never
call this. Fail-open: if the registry cannot be read or locked, it warns and allows; it never blocks an edit forever.

Slot accounting. In use = edits marked active, plus waiters promoted into a free slot (reserved until they start),
plus any video that has a step holding or waiting in the render queue right now (registered or not: an edit that
never called acquire still loads the Mac). An active edit with no acquire and no render-queue activity for 3 hours
loses its slot ("stalled"); a promoted waiter that does not start within 90 minutes loses its reservation.
"""
import contextlib
import datetime as dt
import errno
import fcntl
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent
REPO = SHARED.parents[2]
# /tmp, like renderq: Codex's workspace-write sandbox can write /tmp but not ~. All sessions must share one folder.
DIR = Path(os.environ.get("EDITCAP_DIR") or "/tmp/absbyai-editcap")
CAP = int(os.environ.get("EDITCAP_MAX") or 5)
LEASE_S = 3 * 3600          # an active edit with no acquire and no render-queue activity this long loses its slot
RESERVE_S = 90 * 60         # a promoted waiter that has not started this long loses its reservation
RECENT_RQ_S = 20 * 60       # a render-queue grant this recent refreshes an active edit's lease
LOCK_TIMEOUT_S = 15.0
POLL_S = float(os.environ.get("EDITCAP_POLL") or 30.0)
EXIT_GO, EXIT_WAIT, EXIT_TIMEOUT = 0, 3, 4
LONGFORM_CAL = REPO / "Docs" / "LONGFORM_RELEASE_CALENDAR.md"
SHORTS_CAL = REPO / "Docs" / "SHORTS_RELEASE_CALENDAR.md"
JOBS_FILE = REPO / "Handoffs" / "video-editing" / "jobs.json"
UNDATED = "9999-12-31"
LATER = "2027-01-01"        # "2027, tentative" rows sort after every dated 2026 release
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov",
                                      "dec"], 1)}


def warn(msg):
    sys.stderr.write("editcap: " + msg + "\n")


# ------------------------------------------------------------------------------------------------ job codes
_CODE = re.compile(r"^([A-Za-z]{2,3})-?(\d{1,3}[A-Za-z]?)(?![0-9])")


def job_code(name):
    """'RO-27', 'work:ro27', 'DS-40-codex', 'sl05-short1' -> 'RO-27', 'RO-27', 'DS-40', 'SL-05'. Not a job -> None."""
    if not name:
        return None
    s = str(name).strip()
    if s.startswith("work:"):
        s = s[5:]
    elif ":" in s:
        return None                                    # pg:12345 and similar process-group fallbacks
    batch = re.match(r"^SHOOT-(\d{8})(?![0-9])", s, re.IGNORECASE)
    if batch:
        return "SHOOT-" + batch.group(1)
    m = _CODE.match(s)
    if not m:
        return None
    num = m.group(2)
    return "{}-{}".format(m.group(1).upper(), num[:-1] + num[-1].upper() if num[-1].isalpha() else num)


# ------------------------------------------------------------------------------------------------ release dates
def _date(month, day, year=None):
    mo = MONTHS.get(month[:3].lower())
    if not mo:
        return None
    if year is None:                                  # the calendars run Oct 2026 onwards
        year = 2026 if mo >= 10 else 2027
    try:
        return dt.date(int(year), mo, int(day)).isoformat()
    except ValueError:
        return None


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _put(out, code, date):
    if code and date and (code not in out or date < out[code]):
        out[code] = date


def parse_longform(text):
    out, later = {}, False
    for line in text.splitlines():
        if line.startswith("**2027"):
            later = True
        if later:
            for c in re.findall(r"\b(RO-\d+[A-Z]?)\b", line):
                _put(out, c, LATER)
            continue
        if not line.startswith("|"):
            continue
        cells = _cells(line)
        if len(cells) < 2:
            continue
        m = re.match(r"(?:[A-Za-z]{3}\s+)?([A-Za-z]{3})\w*\s+(\d{1,2})$", cells[0])
        if not m:
            continue
        d = _date(m.group(1), m.group(2))
        code = re.search(r"\b(RO-\d+[A-Z]?)\b", cells[1])        # only the Video cell's first code
        if code:
            _put(out, code.group(1), d)
        v = re.search(r"\bVideo (\d+)\b", cells[1])
        if v:
            _put(out, "VIDEO-" + v.group(1), d)
    return out


def parse_shorts(text):
    out, offsets = {}, [0, 1, 3, 4, 5]                # Mon, Tue, Thu, Fri, Sat columns
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = _cells(line)
        m = re.match(r"([A-Za-z]{3})\w*\s+(\d{1,2})$", cells[0]) if cells else None
        if not m:
            continue
        week = _date(m.group(1), m.group(2))
        if not week:
            continue
        monday = dt.date.fromisoformat(week)
        for off, cell in zip(offsets, cells[1:]):
            for raw in re.findall(r"\(([A-Za-z]{2,3}-?\d{1,3}[A-Za-z]?)[^)]*\)", cell):
                _put(out, job_code(raw), (monday + dt.timedelta(days=off)).isoformat())
    return out


def _read_text(p):
    try:
        return Path(p).read_text()
    except OSError:
        return ""


def load_jobs():
    try:
        return {j["id"]: j for j in json.loads(_read_text(JOBS_FILE) or "{}").get("jobs", []) if j.get("id")}
    except (ValueError, AttributeError, TypeError):
        return {}


class Calendar(object):
    """Release date for a job code, and the reason, from the two calendars and the job list."""

    def __init__(self, longform=None, shorts=None, jobs=None, today=None):
        self.lf = parse_longform(_read_text(LONGFORM_CAL) if longform is None else longform)
        self.sh = parse_shorts(_read_text(SHORTS_CAL) if shorts is None else shorts)
        self.jobs = load_jobs() if jobs is None else jobs
        self.today = (today or (dt.date.fromisoformat(os.environ["EDITCAP_TODAY"]) if os.environ.get("EDITCAP_TODAY")
                                else dt.date.today())).isoformat()

    def nearest(self):
        future = sorted(d for d in list(self.lf.values()) + list(self.sh.values()) if d >= self.today and d < LATER)
        return future[0] if future else None

    def date(self, job, explicit=None):
        """(YYYY-MM-DD, why)"""
        if explicit:
            return explicit, "date given at registration"
        found = [(self.sh[job], "shorts calendar")] if job in self.sh else []
        if job in self.lf:
            found.append((self.lf[job], "2027 tentative list" if self.lf[job] == LATER else "long-form calendar"))
        if found:
            return min(found)
        title = (self.jobs.get(job) or {}).get("title", "")
        if job.startswith("SL-"):
            parent = re.search(r"\b(RO-\d+[A-Z]?)\b", title)
            key = parent.group(1) if parent else None
            if not key:
                v = re.search(r"\bVideo (\d+)\b", title)
                key = "VIDEO-" + v.group(1) if v else None
            if key and key in self.lf:
                d = self.lf[key]
                if d != LATER:
                    d = (dt.date.fromisoformat(d) + dt.timedelta(days=1)).isoformat()
                return d, "day after its long-form {}".format(key)
        if job.startswith("RA-"):
            n = self.nearest()
            if n:
                return n, "ad: ranks with the nearest release"
        return UNDATED, "not on a release calendar"


# ------------------------------------------------------------------------------------------------ render queue
def renderq_activity(now=None):
    """{job: {"live": n steps holding or waiting now, "last": time of the latest grant/hold}} from renderq; {} on error."""
    now = now or time.time()
    out = {}
    if os.environ.get("EDITCAP_NO_RENDERQ"):                   # tests
        return out
    try:
        sys.path.insert(0, str(SHARED / "renderq"))
        import renderq                                          # noqa: E402
        states, tickets = renderq.slot_states(), renderq._tickets()
        rq_dir = renderq.DIR
    except Exception as e:                                      # fail-open: no queue info, no counting
        warn("render queue not readable ({}); counting registered edits only".format(e))
        return out

    def bump(group, live, t):
        j = job_code(group)
        if not j:
            return
        o = out.setdefault(j, {"live": 0, "last": 0.0})
        o["live"] += live
        o["last"] = max(o["last"], t or 0.0)
    for s in states:
        info = s.get("info") or {}
        if s.get("held"):
            bump(info.get("group"), 1, now)
        elif info.get("ended"):
            bump(info.get("group"), 0, info["ended"])
    for t in tickets:
        bump(t.get("group"), 1, now)
    try:
        with open(Path(rq_dir) / "events.log", "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 400000))
            tail = f.read().decode("utf-8", "replace").splitlines()[1:]
        for line in tail:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("event") == "granted" and now - e.get("t", 0) < RECENT_RQ_S:
                bump(e.get("group"), 0, e["t"])
    except OSError:
        pass
    return out


# ------------------------------------------------------------------------------------------------ registry
def _empty():
    return {"version": 1, "edits": {}, "log": []}


def _load():
    p = DIR / "registry.json"
    try:
        with open(p) as f:
            reg = json.load(f)
        if not isinstance(reg.get("edits"), dict):
            raise ValueError("no edits table")
        reg.setdefault("log", [])
        return reg
    except FileNotFoundError:
        return _empty()
    except (OSError, ValueError, AttributeError) as e:
        bad = p.with_name("registry.corrupt-{}.json".format(int(time.time())))
        warn("registry unreadable ({}); set aside as {} and starting fresh".format(e, bad.name))
        try:
            os.replace(p, bad)
        except OSError:
            pass
        return _empty()


def _save(reg):
    p = DIR / "registry.json"
    reg["log"] = reg["log"][-200:]
    tmp = p.with_name("registry.{}.tmp".format(os.getpid()))
    with open(tmp, "w") as f:
        json.dump(reg, f, indent=1)
        f.write("\n")
    os.replace(tmp, p)
    try:
        os.chmod(p, 0o666)
    except OSError:
        pass


class LockTimeout(Exception):
    pass


@contextlib.contextmanager
def _locked():
    DIR.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(DIR / "registry.lock"), os.O_RDWR | os.O_CREAT, 0o666)
    try:
        t0 = time.time()
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as e:
                if e.errno not in (errno.EAGAIN, errno.EACCES) or time.time() - t0 > LOCK_TIMEOUT_S:
                    raise LockTimeout(str(e))
                time.sleep(0.1)
        yield
    finally:
        os.close(fd)


def _alive(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, TypeError):
        return False


def _who():
    """(ai, wake address) of the calling session."""
    if os.environ.get("CLAUDE_CODE_HOST_SESSION_ID"):
        return "claude", os.environ["CLAUDE_CODE_HOST_SESSION_ID"]
    if os.environ.get("CLAUDE_CODE_SESSION_ID"):
        return "claude", os.environ["CLAUDE_CODE_SESSION_ID"]
    for k in ("CODEX_THREAD_ID", "CODEX_SESSION_ID"):
        if os.environ.get(k):
            return "codex", os.environ[k]
    if any(k.startswith("CODEX") for k in os.environ):
        return "codex", ""
    return "", ""


def _note(reg, now, job, event, **kw):
    kw.update(t=round(now, 1), job=job, event=event)
    reg["log"].append(kw)


def order(reg, cal):
    """Waiting edits in start order: release date, then firing order."""
    w = [e for e in reg["edits"].values() if e["state"] == "waiting"]
    return sorted(w, key=lambda e: (cal.date(e["job"], e.get("release"))[0], e.get("waiting_since", 0)))


def occupancy(reg, rq):
    held = {j for j, e in reg["edits"].items() if e["state"] in ("active", "promoted")}
    return held | {j for j, a in rq.items() if a["live"] > 0}


def settle(reg, now, rq, cal):
    """Reap stale slots, then promote waiters into free slots. Mutates reg; returns it."""
    for j, e in reg["edits"].items():
        a = rq.get(j, {})
        if e["state"] == "active":
            if a.get("live") or a.get("last", 0) > e.get("last_seen", 0):
                e["last_seen"] = now if a.get("live") else a["last"]
            if now - e.get("last_seen", now) > LEASE_S:
                e.update(state="stalled", since=now, reason="no acquire or render-queue activity for 3 h; slot freed")
                _note(reg, now, j, "stalled")
        elif e["state"] == "promoted" and now - e.get("since", now) > RESERVE_S and not a.get("live"):
            e.update(state="stalled", since=now, reason="was given a slot but did not start within 90 min")
            _note(reg, now, j, "reservation expired")
    used = occupancy(reg, rq)
    free = CAP - len(used)
    for e in order(reg, cal):
        if e["job"] not in used:                        # a waiter already running in the render queue is counted
            if free <= 0:
                continue
            free -= 1
        e.update(state="promoted", since=now, wake_sent=0, reason="a slot freed; starting")
        _note(reg, now, e["job"], "promoted")
    return reg


def _context(today=None):
    return time.time(), renderq_activity(), Calendar(today=today)


def _entry(reg, job, now, args):
    e = reg["edits"].get(job)
    if not e:
        e = reg["edits"][job] = {"job": job, "registered": now, "state": "new"}
    ai, wake = _who()
    for k, v in (("title", args.get("title")), ("type", args.get("type")), ("release", args.get("release"))):
        if v:
            e[k] = v
    if ai:
        e["ai"] = ai
    if wake:
        e["wake"] = wake
    return e


def acquire(job, title=None, type_=None, release=None, today=None, ctx=None):
    """(exit code, message). 0 = go, 3 = waiting."""
    job = job_code(job) or job
    try:
        with _locked():
            now, rq, cal = ctx or _context(today)
            reg = settle(_load(), now, rq, cal)
            e = _entry(reg, job, now, dict(title=title, type=type_, release=release))
            st = e.get("state")
            if st in ("active", "promoted"):
                if st == "promoted":
                    _note(reg, now, job, "started")
                e.update(state="active", last_seen=now, reason="")
                e.setdefault("active_since", now)
                if st == "promoted":
                    e["active_since"] = now
            elif rq.get(job, {}).get("live"):
                e.update(state="active", since=now, active_since=now, last_seen=now,
                         reason="already running in the render queue")
                _note(reg, now, job, "active (already running)")
            else:
                used = len(occupancy(reg, rq))
                if used < CAP:
                    e.update(state="active", since=now, active_since=now, last_seen=now, reason="")
                    _note(reg, now, job, "active")
                else:
                    if st != "waiting":
                        e.update(state="waiting", since=now, waiting_since=now, reason="all {} slots in use".format(CAP))
                        _note(reg, now, job, "waiting")
            _save(reg)
            if e["state"] == "active":
                return EXIT_GO, "{}: edit slot held. Go.".format(job)
            line = [x["job"] for x in order(reg, cal)]
            d, why = cal.date(job, e.get("release"))
            return EXIT_WAIT, ("{}: WAITING, number {} of {} in line (release {}, {}). All {} edit slots are in use. "
                               "Do not render, generate or build. Arm the auto-start (Claude: `editcap.py wait {}` in the "
                               "background; Codex: a heartbeat that runs `editcap.py acquire {}`), tell Dan, then stop."
                               .format(job, line.index(job) + 1, len(line), d if d != UNDATED else "undated", why, CAP,
                                       job, job))
    except (LockTimeout, OSError) as ex:
        warn("registry not available ({}); allowing the edit (fail-open)".format(ex))
        return EXIT_GO, "{}: edit cap unavailable, allowed.".format(job)


def release(job, review=False, ctx=None, today=None):
    job = job_code(job) or job
    try:
        with _locked():
            now, rq, cal = ctx or _context(today)
            reg = _load()
            e = reg["edits"].get(job)
            if e is None and review:
                e = _entry(reg, job, now, {})
            if e is not None:
                if review:
                    e.update(state="with-dan", since=now, reason="waiting on Dan's review or picks")
                    _note(reg, now, job, "with Dan")
                else:
                    reg["edits"].pop(job, None)
                    _note(reg, now, job, "finished")
            settle(reg, now, rq, cal)
            _save(reg)
            wakes = pending_wakes(reg)
    except (LockTimeout, OSError) as ex:
        warn("registry not available ({}); nothing released".format(ex))
        return EXIT_GO, "{}: edit cap unavailable.".format(job)
    msg = ["{}: slot released{}.".format(job, " (with Dan)" if review else " (finished)")]
    if rq.get(job, {}).get("live"):
        msg.append("Note: {} still has {} step(s) in the render queue; they count as a slot until they finish."
                   .format(job, rq[job]["live"]))
    for w in wakes:
        msg.append(wake_line(w))
    return EXIT_GO, "\n".join(msg)


def wait(job, max_hours=24.0, poll=POLL_S, ctx_fn=None):
    """Block until JOB holds a slot. Records this process as the job's auto-start waiter."""
    job = job_code(job) or job
    t0 = time.time()
    while True:
        try:
            with _locked():
                now, rq, cal = ctx_fn() if ctx_fn else _context()
                reg = settle(_load(), now, rq, cal)
                e = reg["edits"].get(job)
                if e is None or e["state"] in ("with-dan", "stalled"):
                    _save(reg)
                    code, msg = None, None
                else:
                    e["waiter_pid"] = os.getpid()
                    e["waiter_seen"] = now
                    _save(reg)
                    code = "go" if e["state"] in ("promoted", "active") else "wait"
        except (LockTimeout, OSError) as ex:
            warn("registry not available ({}); allowing the edit (fail-open)".format(ex))
            print("{}: edit cap unavailable, allowed. Go.".format(job))
            return EXIT_GO
        if code is None:                       # not registered (or registry wiped): register now
            c, m = acquire(job, ctx=ctx_fn() if ctx_fn else None)
            if c == EXIT_GO:
                print(m)
                return EXIT_GO
        elif code == "go":
            c, m = acquire(job, ctx=ctx_fn() if ctx_fn else None)
            print(m)
            return c
        if time.time() - t0 > max_hours * 3600:
            print("{}: still waiting after {} h; run `editcap.py wait {}` again.".format(job, max_hours, job))
            return EXIT_TIMEOUT
        time.sleep(poll)


def pending_wakes(reg, ai=None):
    """Promoted edits whose auto-start waiter is not running and that were not messaged yet."""
    out = []
    for e in reg["edits"].values():
        if e["state"] != "promoted" or e.get("wake_sent") or _alive(e.get("waiter_pid")):
            continue
        if ai and e.get("ai") != ai:
            continue
        out.append(e)
    return out


def wake_line(e):
    msg = ("A video edit slot is free for {}. Run `python3 .claude/skills/_shared/editcap/editcap.py acquire {}`, "
           "then continue the edit.".format(e["job"], e["job"]))
    if e.get("ai") == "claude" and e.get("wake"):
        return "WAKE claude {} :: {}".format(e["wake"], msg)
    if e.get("ai") == "codex" and e.get("wake"):
        return "WAKE codex {} :: {}".format(e["wake"], msg)
    return "WAKE unknown ({}) :: {}".format(e["job"], msg)


def wakes(claim=False, ai=None):
    try:
        with _locked():
            now, rq, cal = _context()
            reg = settle(_load(), now, rq, cal)
            out = pending_wakes(reg, ai)
            if claim:
                for e in out:
                    e["wake_sent"] = now
                    _note(reg, now, e["job"], "wake claimed")
            _save(reg)
    except (LockTimeout, OSError) as ex:
        warn("registry not available ({})".format(ex))
        return []
    return [wake_line(e) for e in out]


def forget(job):
    job = job_code(job) or job
    with _locked():
        reg = _load()
        reg["edits"].pop(job, None)
        _note(reg, time.time(), job, "forgotten")
        _save(reg)


# ------------------------------------------------------------------------------------------------ status
def _ago(t, now):
    if not t:
        return "?"
    s = max(0, now - t)
    return "{} min".format(int(s // 60)) if s < 5400 else "{:.1f} h".format(s / 3600)


def _pretty(d):
    if d == UNDATED:
        return "undated"
    if d == LATER:
        return "2027 (tentative)"
    return dt.date.fromisoformat(d).strftime("%a %b %-d")


def view(today=None, ctx=None):
    """The registry as it would be after settling, without writing anything."""
    now, rq, cal = ctx or _context(today)
    try:
        with open(DIR / "registry.json") as f:
            reg = json.load(f)
        reg.setdefault("log", [])
    except FileNotFoundError:
        reg = _empty()
    except (OSError, ValueError) as e:
        warn("registry unreadable ({})".format(e))
        reg = _empty()
    return settle(reg, now, rq, cal), now, rq, cal


def status(as_json=False, ctx=None):
    reg, now, rq, cal = view(ctx=ctx)
    used = occupancy(reg, rq)
    ed = reg["edits"]
    jobs = cal.jobs
    title = lambda j: (ed.get(j, {}).get("title") or (jobs.get(j) or {}).get("title") or "").strip()
    line = order(reg, cal)
    if as_json:
        return json.dumps(dict(cap=CAP, in_use=sorted(used), edits=ed, waiting_order=[e["job"] for e in line],
                               renderq=rq, dates={j: cal.date(j, ed.get(j, {}).get("release")) for j in
                                                  set(ed) | set(rq)}), indent=1)
    out = ["Edit slots: {} at once (Claude and Codex together). In use: {}. Free: {}.".format(
        CAP, len(used), max(0, CAP - len(used)))]
    out.append("")
    out.append("ACTIVE (doing production work)")
    n = 0
    for j in sorted(used, key=lambda j: ed.get(j, {}).get("active_since", ed.get(j, {}).get("since", now))):
        n += 1
        e = ed.get(j)
        a = rq.get(j, {})
        rqtxt = ", {} render-queue step(s) running or waiting".format(a["live"]) if a.get("live") else ""
        if e is None:
            out.append("  {}. {} {}: not registered, counted because it has steps in the render queue{}".format(
                n, j, title(j), rqtxt))
        elif e["state"] == "promoted":
            out.append("  {}. {} {} [{}]: slot reserved {} ago, starting{}".format(
                n, j, title(j), e.get("ai", "?"), _ago(e.get("since"), now),
                "" if _alive(e.get("waiter_pid")) else " (no auto-start process running: needs a wake message)"))
        elif e["state"] == "active":
            out.append("  {}. {} {} [{}]: active {}, last activity {} ago{}".format(
                n, j, title(j), e.get("ai", "?"), _ago(e.get("active_since", e.get("since")), now),
                _ago(e.get("last_seen"), now), rqtxt))
        else:
            out.append("  {}. {} {} [{}]: marked {} but still has steps in the render queue{}".format(
                n, j, title(j), e.get("ai", "?"), e["state"], rqtxt))
    if not n:
        out.append("  (none)")
    out.append("")
    out.append("WAITING, in start order (soonest release first)")
    for i, e in enumerate(line, 1):
        d, why = cal.date(e["job"], e.get("release"))
        armed = ("auto-start armed" if _alive(e.get("waiter_pid")) else
                 "codex heartbeat" if e.get("ai") == "codex" else "no auto-start process running")
        out.append("  {}. {} {} [{}]: release {} ({}), waiting {}, {}".format(
            i, e["job"], title(e["job"]), e.get("ai", "?"), _pretty(d), why, _ago(e.get("waiting_since"), now), armed))
    if not line:
        out.append("  (none)")
    rest = [e for e in ed.values() if e["state"] in ("with-dan", "stalled")]
    if rest:
        out.append("")
        out.append("NOT HOLDING A SLOT")
        for e in sorted(rest, key=lambda e: e["state"]):
            out.append("  {} {} [{}]: {} {} ago: {}".format(
                e["job"], title(e["job"]), e.get("ai", "?"), "with Dan" if e["state"] == "with-dan" else "stalled",
                _ago(e.get("since"), now), e.get("reason", "")))
    return "\n".join(out)


def summary_line(ctx=None):
    """One line for renderq status."""
    reg, now, rq, cal = view(ctx=ctx)
    used = sorted(occupancy(reg, rq))
    line = [e["job"] for e in order(reg, cal)]
    return "Edit slots: {} of {} in use ({}){}. Details: editcap.py status".format(
        len(used), CAP, ", ".join(used) or "none",
        "; {} waiting: {}".format(len(line), ", ".join(line)) if line else "; nobody waiting")


# ------------------------------------------------------------------------------------------------ CLI
def _opts(rest, names):
    o, pos, k = {}, [], 0
    while k < len(rest):
        x = rest[k]
        if x in names:
            if names[x]:
                o[x] = rest[k + 1] if k + 1 < len(rest) else ""
                k += 2
                continue
            o[x] = True
        else:
            pos.append(x)
        k += 1
    return o, pos


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "selftest":
        sys.path.insert(0, str(HERE))
        import selftest                                       # noqa: E402
        return selftest.main()
    if cmd == "status":
        o, _ = _opts(rest, {"--json": False})
        print(status(as_json=bool(o.get("--json"))))
        return 0
    if cmd == "wakes":
        o, _ = _opts(rest, {"--claim": False, "--ai": True})
        for w in wakes(claim=bool(o.get("--claim")), ai=o.get("--ai")):
            print(w)
        return 0
    o, pos = _opts(rest, {"--title": True, "--type": True, "--release": True, "--review": False, "--max-hours": True})
    if not pos:
        sys.exit("usage: editcap.py {} JOB".format(cmd))
    job = pos[0]
    if cmd in ("acquire", "heartbeat"):
        if o.get("--release") and not re.match(r"\d{4}-\d{2}-\d{2}$", o["--release"]):
            sys.exit("--release must be YYYY-MM-DD")
        code, msg = acquire(job, o.get("--title"), o.get("--type"), o.get("--release"))
        print(msg)
        return code
    if cmd == "release":
        code, msg = release(job, review=bool(o.get("--review")))
        print(msg)
        return code
    if cmd == "wait":
        return wait(job, max_hours=float(o.get("--max-hours") or 24))
    if cmd == "forget":
        forget(job)
        print("{}: forgotten.".format(job))
        return 0
    sys.exit("unknown command: " + cmd)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except Exception as ex:                                    # fail-open on any bug
        warn("unexpected error ({}: {}); allowing (fail-open)".format(type(ex).__name__, ex))
        sys.exit(0)
