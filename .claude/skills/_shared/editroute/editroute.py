#!/usr/bin/env python3
"""Two-Mac edit routing: which Mac takes the next video edit, and why (handoff 03, Dan 2026-11-12, built 2026-11-14).

The M6 is Dan's Mac (2 edit slots, fast, he reviews there). The M2 Pro is the headless edit machine on the
Thunderbolt cable (3 slots, holds the Extreme and Seagate drives). Numbers live in hosts.json beside this file.
Rule: VIDEO-RULES.md, "Two Macs". README.md beside this file.

    editroute.py pick JOB [--kind SFC|SFL|LFC|AD|ADCUT|VSL|EXDEMO|REV|OTHER] [--round N] [--chroma]
                          [--host m6|m2 [--move]] [--dry-run] [--json]
            First line: m6, m2 or wait. Then why. Records the decision (decisions.jsonl). Exit 0 = go to that Mac
            (then run editcap.py acquire THERE), 3 = both Macs full: in the combined line (run `wait`).
    editroute.py wait JOB [--max-hours 24]
            Blocks until the first free slot on either Mac is JOB's (oldest first), prints the Mac, exits 0.
    editroute.py where JOB      which Mac holds JOB's work folder / edit slot (rule 1)
    editroute.py status [--json]
                                one table for both Macs: slots, cores, load, line, review pages from the M2
    editroute.py fetch JOB SRC [SRC ...] [--to DIR]
            On the M6: copy footage from the M2's drives (read only there) into this Mac's job folder.
    editroute.py push PATH [PATH ...]
            On the M2: copy finished files into the M6's project folder at the same place (an older copy there
            is kept as NAME.m6-before-<time>). Nothing is ever deleted on either Mac.
    editroute.py mirror-review PORT DIR
            On the M2: open the review page on the M6 as well (review_server.py does this by itself on the M2).
    editroute.py free-port [--from 9800]
                                a review port free on both Macs
    editroute.py local-status [--job JOB] --json
                                this Mac only (what the other Mac reads over ssh)

Rules (Dan, handoff 03): 1 a job with a work folder stays on its Mac; 2 a Mac Dan names; 3 short interactive work
(Shorts, ad cutdowns, later-round revisions) to the M6 first; 4 long unattended work (long-form R1, full chroma key,
exercise-demo batches) to the M2 first; 5 a full preferred Mac (or an M6 under Dan's own load) sends the edit to the
other; 6 anything else to the Mac with the smaller share of its slots in use, the M6 on a tie, so from idle:
M6, M2, M2, M6, M2; 7 both full: the combined line, oldest first. An unreachable Mac counts as full.
"""
import datetime as dt
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent
REPO = SHARED.parents[2]
sys.path.insert(0, str(HERE))
import hostcfg                                                       # noqa: E402

VERSION = 1
EXIT_GO, EXIT_WAIT, EXIT_TIMEOUT, EXIT_ERR = 0, 3, 4, 1
POLL_S = float(os.environ.get("EDITROUTE_POLL") or 30.0)
WAITER_STALE_S = 5 * 60            # a combined-line entry whose wait loop has not looked in this long is skipped
REMEMBER_S = 24 * 3600             # a job routed this recently is sent to the same Mac again
KINDS = {"SFC": "SFC", "DS": "SFC", "SHORT": "SFC", "SFL": "SFL", "SL": "SFL", "LFC": "LFC", "RO": "LFC",
         "LONGFORM": "LFC", "AD": "AD", "RA": "AD", "SP": "AD", "ADCUT": "ADCUT", "CUTDOWN": "ADCUT", "AV": "ADCUT",
         "AS": "ADCUT", "VERTICAL": "ADCUT", "SQUARE": "ADCUT", "VSL": "VSL", "WV": "VSL", "EXDEMO": "EXDEMO",
         "DEMO": "EXDEMO", "DEMOS": "EXDEMO", "REV": "REV", "REVISION": "REV", "CHROMA": "CHROMA", "OTHER": "OTHER"}
KIND_WORDS = {"SFC": "a dedicated Short", "SFL": "Shorts from a long-form", "LFC": "a long-form first cut",
              "AD": "an ad edit", "ADCUT": "an ad cutdown", "VSL": "a website VSL", "EXDEMO": "an exercise-demo batch",
              "REV": "a later-round revision Dan is waiting on", "CHROMA": "a full chroma key", "OTHER": "an edit"}


def warn(msg):
    sys.stderr.write("editroute: " + msg + "\n")


def cfg():
    return hostcfg.load()


def me():
    return hostcfg.this_host()


def label(h, c=None):
    return ((c or cfg()).get("hosts", {}).get(h) or {}).get("label", h)


# ------------------------------------------------------------------------------------------------ job codes
def job_code(job):
    try:
        sys.path.insert(0, str(SHARED / "editcap"))
        import editcap                                               # noqa: E402
        return editcap.job_code(job) or job
    except Exception:
        return job


def infer_kind(job):
    """Kind from the job code, else from the edit queue's group. 'OTHER' when unknown."""
    j = job.upper()
    if j.startswith(("EXDEMO", "REALDEMOS", "DEMOS")):
        return "EXDEMO"
    m = re.match(r"^([A-Z]{2,3})-\d", j)
    if m and m.group(1) in KINDS:
        return KINDS[m.group(1)]
    try:
        jobs = json.loads((REPO / "Handoffs" / "video-editing" / "jobs.json").read_text()).get("jobs", [])
        g = next((x.get("group", "") for x in jobs if x.get("id") == job), "")
        return {"Dedicated shorts": "SFC", "Shorts from long-forms": "SFL", "Organic long-form": "LFC",
                "Short-form ads": "AD", "Ad verticals": "ADCUT", "Ad squares": "ADCUT",
                "Website VSLs": "VSL"}.get(g, "OTHER")
    except (OSError, ValueError, AttributeError):
        return "OTHER"


def route_class(kind, rnd=1, chroma=False):
    """The class the preference lists use: CHROMA, REV (round 2+), else the kind."""
    if chroma:
        return "CHROMA"
    if rnd and int(rnd) >= 2:
        return "REV"
    return kind


# ------------------------------------------------------------------------------------------------ state folder
def state_dir():
    """~/.absbyai-editroute (handoff); /tmp/absbyai-editroute when the home folder is not writable (Codex sandbox)."""
    for d in (Path(os.environ["EDITROUTE_DIR"]) if os.environ.get("EDITROUTE_DIR") else None,
              Path.home() / ".absbyai-editroute", Path("/tmp/absbyai-editroute")):
        if d is None:
            continue
        try:
            d.mkdir(parents=True, exist_ok=True)
            probe = d / ".w"
            probe.write_text("")
            return d
        except OSError:
            continue
    return Path("/tmp")


def _read_json(p, default):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return default


def _write_json(p, value):
    p = Path(p)
    tmp = p.with_name(".{}.{}.tmp".format(p.name, os.getpid()))
    tmp.write_text(json.dumps(value, indent=1, sort_keys=True) + "\n")
    os.replace(str(tmp), str(p))


class _Lock(object):
    def __init__(self, d):
        self.path = Path(d) / "route.lock"

    def __enter__(self):
        import fcntl
        self.fd = os.open(str(self.path), os.O_RDWR | os.O_CREAT, 0o666)
        t0 = time.time()
        while True:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.time() - t0 > 15:
                    return self                      # fail open: route without the lock
                time.sleep(0.1)

    def __exit__(self, *a):
        os.close(self.fd)


def decisions(d=None, since_s=REMEMBER_S, now=None):
    now = now or time.time()
    out = []
    try:
        with open(str((d or state_dir()) / "decisions.jsonl")) as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if now - e.get("t", 0) <= since_s:
                    out.append(e)
    except OSError:
        pass
    return out


def record(entry, d=None):
    try:
        with open(str((d or state_dir()) / "decisions.jsonl"), "a") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
    except OSError as e:
        warn("decision not recorded ({})".format(e))


# ------------------------------------------------------------------------------------------------ this Mac
def _editcap():
    sys.path.insert(0, str(SHARED / "editcap"))
    import editcap                                                   # noqa: E402
    return editcap


def _renderq():
    sys.path.insert(0, str(SHARED / "renderq"))
    import renderq                                                   # noqa: E402
    return renderq


def _pressure():
    try:
        r = subprocess.run(["sysctl", "-n", "kern.memorystatus_vm_pressure_level"], capture_output=True, text=True,
                           timeout=2)
        return int(r.stdout.strip())
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def _free_gb(p):
    try:
        st = os.statvfs(str(p))
        return round(st.f_bavail * st.f_frsize / 1e9)
    except OSError:
        return None


def find_job_folders(job):
    """Every work folder of JOB on this Mac: internal ~/Projects/_edit_work and each plugged-in work drive."""
    out = []
    try:
        rq = _renderq()
        roots = [("internal", Path(rq.INTERNAL_WORK).parent, (Path(rq.INTERNAL_WORK).name,))]
        roots += [(n, r, tuple(rq.WORK_FOLDERS)) for n, r in rq.mounted_work_drives()]
    except Exception:
        roots = [("internal", Path.home() / "Projects", ("_edit_work",))]
    for name, root, folders in roots:
        for folder in folders:
            try:
                names = os.listdir(str(Path(root) / folder))
            except OSError:
                continue
            for n in names:
                if n.lower() != job.lower():
                    continue
                p = Path(root) / folder / n
                try:
                    if p.is_dir():
                        out.append(dict(drive=name, path=str(p), entries=len(os.listdir(str(p))),
                                        mtime=p.stat().st_mtime))
                except OSError:
                    continue
    return out


def local_status(job=None):
    """This Mac's state, as plain data (also what the other Mac reads over ssh)."""
    h = me()
    c = cfg()
    hc = (c.get("hosts") or {}).get(h) or {}
    now = time.time()
    st = dict(host=h, version=VERSION, time=now, reachable=True, ncpu=os.cpu_count(), load=list(os.getloadavg()),
              pressure=_pressure(), label=hc.get("label", h))
    idle = hostcfg.idle_seconds()
    pres, why = hostcfg.presence(h, idle=idle)
    st.update(idle_s=idle, presence=pres, presence_why=why)
    try:
        ec = _editcap()
        reg, _, rq_act, cal = ec.view()
        used = sorted(ec.occupancy(reg, rq_act))
        st["editcap"] = dict(cap=ec.CAP, in_use=used, waiting=[e["job"] for e in ec.order(reg, cal)],
                             edits={j: e.get("state") for j, e in reg["edits"].items()},
                             titles={j: e.get("title", "") for j, e in reg["edits"].items()})
    except Exception as e:                                           # report, do not guess
        st["editcap"] = dict(error=str(e))
    try:
        rq = _renderq()
        states = rq.slot_states()
        st["renderq"] = dict(budget=rq.core_budget(), cores_in_use=rq.cores_in_use(states),
                             holders=sorted({(s["info"] or {}).get("group") or "?" for s in states if s["held"]}),
                             waiting=len(rq._tickets()))
    except Exception as e:
        st["renderq"] = dict(error=str(e))
    drives = [dict(drive="internal", free_gb=_free_gb(Path.home()))]
    try:
        drives += [dict(drive=n, free_gb=_free_gb(r)) for n, r in _renderq().mounted_work_drives()]
    except Exception:
        pass
    st["drives"] = drives
    try:
        g = subprocess.run(["git", "-C", str(REPO), "rev-list", "--left-right", "--count", "HEAD...origin/main"],
                           capture_output=True, text=True, timeout=3)
        a, b = g.stdout.split()
        st["git"] = dict(ahead=int(a), behind=int(b))
    except Exception:
        st["git"] = None
    if job:
        st["job"] = dict(folders=find_job_folders(job), editcap=(st.get("editcap") or {}).get("edits", {}).get(job))
    st["reviews"] = _read_json(state_dir() / "reviews.json", {})
    return st


def under_load(st, hc):
    """(bool, why): the M6 under real load from Dan's own work counts as full for new edits (rule 5)."""
    if not hc.get("load_guard") or not st.get("reachable"):
        return False, ""
    p = st.get("pressure")
    if p not in (None, 1):
        return True, "memory pressure is {} (not normal)".format({2: "warning", 4: "critical"}.get(p, p))
    load5, ncpu = (st.get("load") or [0, 0, 0])[1], st.get("ncpu") or 1
    if load5 > ncpu:
        return True, "5-minute load {:.1f} is above its {} cores".format(load5, ncpu)
    return False, ""


# ------------------------------------------------------------------------------------------------ the other Mac
def remote_status(h, job=None, c=None):
    c = c or cfg()
    hc = c["hosts"][h]
    script = "{}/.claude/skills/_shared/editroute/editroute.py".format(hc["repo"])
    cmd = "python3 {} local-status --json{}".format(shlex.quote(script), " --job " + shlex.quote(job) if job else "")
    t0 = time.time()
    try:
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout={}".format(c.get("remote_connect_s", 3)),
                            hc.get("ssh", h), cmd], capture_output=True, text=True,
                           timeout=float(c.get("remote_timeout_s", 8)))
        if r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip()
                               else "exit {}".format(r.returncode))
        st = json.loads(r.stdout)
        st["reachable"], st["rtt_s"] = True, round(time.time() - t0, 2)
        return st
    except (OSError, ValueError, subprocess.SubprocessError, RuntimeError, IndexError) as e:
        return dict(host=h, reachable=False, error=str(e) or type(e).__name__, rtt_s=round(time.time() - t0, 2))


def gather(job=None, c=None):
    """{host: status} for both Macs: this one directly, the other over ssh (in parallel)."""
    c = c or cfg()
    here = me()
    out = {}
    threads = []
    for h in c.get("hosts", {}):
        if h == here:
            continue
        def run(h=h):
            out[h] = remote_status(h, job, c)
        t = threading.Thread(target=run)
        t.start()
        threads.append(t)
    if here:
        try:
            out[here] = local_status(job)
        except Exception as e:
            out[here] = dict(host=here, reachable=False, error="local status failed: {}".format(e))
    for t in threads:
        t.join()
    return out


# ------------------------------------------------------------------------------------------------ the rules
def holder(job, statuses):
    """(host, why) of the Mac that already holds JOB (rule 1), or (None, '')."""
    live = ("active", "promoted", "waiting")
    found = {}
    for h, st in statuses.items():
        j = st.get("job") or {}
        if j.get("folders") or j.get("editcap"):
            found[h] = j
    if not found:
        return None, ""
    def desc(h):
        j = found[h]
        parts = ["{} ({} items)".format(f["path"], f["entries"]) for f in j.get("folders", [])]
        if j.get("editcap"):
            parts.append("edit slot: {}".format(j["editcap"]))
        return "{}: {}".format(h, "; ".join(parts))
    if len(found) == 1:
        h = next(iter(found))
        return h, "rule 1: {} already has its work on the {} ({}). A job never moves mid-flight.".format(
            job, h, desc(h))
    for test, why in ((lambda j: j.get("editcap") in live, "its edit slot is live there"),
                      (lambda j: j.get("editcap") == "with-dan", "it is with Dan from there")):
        hit = [h for h in found if test(found[h])]
        if len(hit) == 1:
            return hit[0], "rule 1: {} has work on both Macs ({}); {} because {}.".format(
                job, " | ".join(desc(h) for h in found), hit[0], why)
    best = max(found, key=lambda h: (sum(f["entries"] for f in found[h].get("folders", [])),
                                     max([f["mtime"] for f in found[h].get("folders", [])] or [0])))
    return best, "rule 1: {} has work folders on both Macs ({}); {} holds the most, so it stays there.".format(
        job, " | ".join(desc(h) for h in found), best)


def capacity(statuses, c, reserved=None):
    """{host: dict(slots, used, free, why)}. Unreachable = full. Reserved = routed here, not started yet."""
    reserved = reserved or {}
    out = {}
    for h, hc in c.get("hosts", {}).items():
        st = statuses.get(h) or {"reachable": False, "error": "no status"}
        slots = int(hc.get("slots") or 0)
        if not st.get("reachable"):
            out[h] = dict(slots=slots, used=slots, free=0, why="unreachable ({}), counted as full".format(
                st.get("error", "?")))
            continue
        ecs = st.get("editcap") or {}
        if ecs.get("error"):
            used = 0
        else:
            used = len(ecs.get("in_use", [])) + len(ecs.get("waiting", []))
        res = [j for j in reserved.get(h, []) if j not in (ecs.get("edits") or {})]
        used += len(res)
        why = "{} of {} slots in use{}".format(min(used, slots), slots,
                                                " (incl. {} routed, not started: {})".format(len(res), ", ".join(res))
                                                if res else "")
        if ecs.get("waiting"):
            why += ", {} waiting there".format(len(ecs["waiting"]))
        loaded, lwhy = under_load(st, hc)
        if loaded:
            out[h] = dict(slots=slots, used=slots, free=0, why="under Dan's own load: {}; counted as full".format(lwhy))
            continue
        out[h] = dict(slots=slots, used=used, free=max(0, slots - used), why=why)
    return out


def decide(job, kind, rnd, chroma, named, move, statuses, c, reserved=None):
    """(host | 'wait', [reasons]). Pure: no I/O, so every rule is unit-tested."""
    reasons = []
    hosts = list(c.get("hosts", {}))
    held, why = holder(job, statuses)
    if held and not (named and move and named != held):
        if named and named != held:
            reasons.append("Dan named the {}, but {} (add --move only if Dan says to move it).".format(named, why[8:]))
        reasons.append(why)
        return held, reasons
    if held:
        reasons.append("Dan asked to move {} from the {} to the {} ({}).".format(job, held, named, why))
    if named:
        if named not in hosts:
            raise ValueError("unknown Mac {!r}; hosts.json knows {}".format(named, ", ".join(hosts)))
        cap = capacity(statuses, c, reserved)[named]
        reasons.append("rule 2: Dan named the {}.".format(named))
        if cap["free"] <= 0:
            reasons.append("Note: the {} is {}; the edit waits for a slot there (editcap.py acquire).".format(
                named, cap["why"]))
        return named, reasons
    cap = capacity(statuses, c, reserved)
    rc = route_class(kind, rnd, chroma)
    pref = next((h for h in hosts if rc in (c["hosts"][h].get("first") or [])), None)
    if pref:
        other = [h for h in hosts if h != pref]
        rule = "rule 3" if pref == c.get("primary", "m6") else "rule 4"
        if cap[pref]["free"] > 0:
            reasons.append("{}: {} goes to the {} first; it has a free slot ({}).".format(
                rule, KIND_WORDS.get(rc, rc), pref, cap[pref]["why"]))
            return pref, reasons
        for o in other:
            if cap[o]["free"] > 0:
                reasons.append("rule 5: {} prefers the {}, but it is full ({}); the {} has room ({}).".format(
                    KIND_WORDS.get(rc, rc), pref, cap[pref]["why"], o, cap[o]["why"]))
                return o, reasons
    else:
        open_ = [h for h in hosts if cap[h]["free"] > 0]
        if open_:
            tie = c.get("tie", c.get("primary", "m6"))
            best = min(open_, key=lambda h: (cap[h]["used"] / float(cap[h]["slots"] or 1), h != tie))
            reasons.append("rule 6: {} has no preferred Mac; the {} has the smaller share of its slots in use ({}{}).".format(
                KIND_WORDS.get(rc, rc), best, "; ".join("{} {}".format(h, cap[h]["why"]) for h in hosts),
                "; tie goes to the " + tie if len({round(cap[h]["used"] / float(cap[h]["slots"] or 1), 3)
                                                   for h in open_}) == 1 and len(open_) > 1 else ""))
            return best, reasons
    reasons.append("rule 7: both Macs are full ({}). The edit waits in the combined line and starts on whichever "
                   "Mac frees first, oldest first.".format("; ".join("{} {}".format(h, cap[h]["why"]) for h in hosts)))
    return "wait", reasons


def reservations(entries, now=None):
    """{host: [jobs]} routed in the last reserve_min minutes (not counting waits)."""
    now = now or time.time()
    limit = float(cfg().get("reserve_min", 30)) * 60
    out, last = {}, {}
    for e in entries:
        last[e["job"]] = e
    for j, e in last.items():
        if e.get("host") in ("wait", None) or now - e.get("t", 0) > limit or e.get("dry"):
            continue
        out.setdefault(e["host"], []).append(j)
    return out


# ------------------------------------------------------------------------------------------------ commands
def _forward(argv):
    """On a Mac that is not the primary, run routing commands on the primary (it keeps the line and the log).
    Returns the exit code, or None when the primary cannot be reached (then decide here)."""
    c = cfg()
    p = c.get("primary")
    if not p or me() in (None, p) or os.environ.get("EDITROUTE_LOCAL"):
        return None
    hc = c["hosts"][p]
    script = "{}/.claude/skills/_shared/editroute/editroute.py".format(hc["repo"])
    try:
        probe = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout={}".format(c.get("remote_connect_s", 3)),
                                hc.get("ssh", p), "test -f " + shlex.quote(script)], timeout=8)
        if probe.returncode != 0:
            return None
    except (OSError, subprocess.SubprocessError):
        return None
    return subprocess.call(["ssh", "-o", "BatchMode=yes", hc.get("ssh", p),
                            " ".join(["python3", shlex.quote(script)] + [shlex.quote(a) for a in argv])])


def cmd_pick(job, kind=None, rnd=1, chroma=False, named=None, move=False, dry=False, as_json=False):
    job = job_code(job)
    kind = KINDS.get((kind or "").upper()) or infer_kind(job)
    c = cfg()
    d = state_dir()
    with _Lock(d):
        now = time.time()
        past = decisions(d, now=now)
        prev = [e for e in past if e.get("job") == job and e.get("host") not in ("wait", None) and not e.get("dry")]
        statuses = gather(job, c)
        held, _ = holder(job, statuses)
        if prev and not named and not held and now - prev[-1]["t"] < float(c.get("reserve_min", 30)) * 60:
            host, reasons = prev[-1]["host"], ["{} was routed to the {} {} min ago ({}); same Mac again.".format(
                job, prev[-1]["host"], int((now - prev[-1]["t"]) // 60), prev[-1].get("why", [""])[0])]
        else:
            res = reservations([e for e in past if e.get("job") != job], now)
            host, reasons = decide(job, kind, rnd, chroma, named, move, statuses, c, res)
        for h, st in statuses.items():
            if not st.get("reachable"):
                reasons.append("Note: the {} did not answer ({}).".format(h, st.get("error")))
        entry = dict(t=round(now, 1), job=job, kind=kind, round=int(rnd or 1), chroma=bool(chroma), named=named,
                     host=host, why=reasons, by=me(), dry=bool(dry))
        if not dry:
            record(entry, d)
            line = _read_json(d / "waiting.json", {})
            if host == "wait":
                line.setdefault(job, dict(job=job, kind=kind, round=int(rnd or 1), chroma=bool(chroma),
                                          since=round(now, 1)))
            else:
                line.pop(job, None)
            _write_json(d / "waiting.json", line)
    if as_json:
        print(json.dumps(entry, indent=1))
    else:
        print(host)
        for r in reasons:
            print("  " + r)
        if host == "wait":
            print("  Next: run `python3 .claude/skills/_shared/editroute/editroute.py wait {}` in the background; it "
                  "exits 0 and prints the Mac when a slot is free for this job. Do no production work until then."
                  .format(job))
        elif host != me():
            print("  Next: start this edit ON THE {} (Claude: a new session on the SSH connection `{}`; Codex: "
                  "`ssh {} codex exec ...`, see editroute/README.md). There, run editcap.py acquire {} first."
                  .format(host.upper(), host, host, job))
        else:
            print("  Next: on this Mac, `python3 .claude/skills/_shared/editcap/editcap.py acquire {}`.".format(job))
    return EXIT_WAIT if host == "wait" else EXIT_GO


def cmd_wait(job, max_hours=24.0, poll=POLL_S):
    job = job_code(job)
    d = state_dir()
    t0 = time.time()
    while True:
        with _Lock(d):
            now = time.time()
            line = _read_json(d / "waiting.json", {})
            if job not in line:
                prev = [e for e in decisions(d, now=now) if e.get("job") == job and not e.get("dry")]
                if prev and prev[-1].get("host") not in ("wait", None):
                    print(prev[-1]["host"])
                    print("  {} was already routed to the {}.".format(job, prev[-1]["host"]))
                    return EXIT_GO
                warn("{} is not in the combined line; run `editroute.py pick {}` first".format(job, job))
                return EXIT_ERR
            line[job]["seen"] = round(now, 1)
            line[job]["pid"] = os.getpid()
            _write_json(d / "waiting.json", line)
            c = cfg()
            statuses = gather(None, c)
            res = reservations(decisions(d, now=now), now)
            for w in sorted(line.values(), key=lambda w: w.get("since", 0)):
                if w["job"] != job and now - w.get("seen", 0) > WAITER_STALE_S:
                    continue                                   # nobody is waiting on it any more
                host, reasons = decide(w["job"], w["kind"], w.get("round", 1), w.get("chroma"), None, False,
                                       statuses, c, res)
                if host == "wait":
                    if w["job"] == job:
                        break
                    continue                                   # an older waiter that cannot start yet
                if w["job"] != job:
                    res.setdefault(host, []).append(w["job"])  # an older waiter gets this slot first
                    continue
                record(dict(t=round(now, 1), job=job, kind=w["kind"], round=w.get("round", 1),
                            chroma=bool(w.get("chroma")), named=None, host=host, why=reasons, by=me(),
                            dry=False, from_line=True), d)
                line.pop(job, None)
                _write_json(d / "waiting.json", line)
                print(host)
                for r in reasons:
                    print("  " + r)
                return EXIT_GO
        if time.time() - t0 > max_hours * 3600:
            print("{}: still waiting after {} h; run `editroute.py wait {}` again.".format(job, max_hours, job))
            return EXIT_TIMEOUT
        time.sleep(poll)


def cmd_where(job):
    job = job_code(job)
    statuses = gather(job)
    h, why = holder(job, statuses)
    past = [e for e in decisions(since_s=7 * 86400) if e.get("job") == job and not e.get("dry")]
    if h:
        print(h)
        print("  " + why)
    elif past:
        print(past[-1]["host"])
        print("  No work folder yet; routed to the {} {} ago.".format(past[-1]["host"], _ago(past[-1]["t"])))
    else:
        print("none")
        print("  {} has no work folder or edit slot on either Mac and was never routed.".format(job))
    for k, st in statuses.items():
        if not st.get("reachable"):
            print("  Note: the {} did not answer ({}); a folder there would not show.".format(k, st.get("error")))
    return EXIT_GO


def _ago(t):
    s = max(0, time.time() - (t or 0))
    return "{} min".format(int(s // 60)) if s < 5400 else "{:.1f} h".format(s / 3600)


def status_text(statuses, c, line=None, recent=None, reviews=None):
    hosts = list(c.get("hosts", {}))
    cap = capacity(statuses, c, reservations(recent or []))
    rows = []

    def row(name, f):
        rows.append([name] + [f(h, statuses.get(h) or {}) for h in hosts])

    def ec(st, k):
        return (st.get("editcap") or {}).get(k) or []

    def reach(h, st):
        return "yes ({} s)".format(st["rtt_s"]) if st.get("reachable") and st.get("rtt_s") is not None else \
            ("yes" if st.get("reachable") else "NO: " + str(st.get("error", "?"))[:40])
    row("Reachable", reach)
    row("Edit slots", lambda h, st: "{} of {} in use".format(min(cap[h]["used"], cap[h]["slots"]), cap[h]["slots"])
        if st.get("reachable") else "counted as full")
    row("Active edits", lambda h, st: ", ".join(ec(st, "in_use")) or "-")
    row("Waiting there", lambda h, st: ", ".join(ec(st, "waiting")) or "-")
    row("Routed, not started", lambda h, st: ", ".join(j for j in reservations(recent or []).get(h, [])
                                                       if j not in ((st.get("editcap") or {}).get("edits") or {}))
        or "-")
    row("With Dan (no slot)", lambda h, st: str(sum(1 for v in ((st.get("editcap") or {}).get("edits") or {}).values()
                                                     if v == "with-dan")))
    row("Cores for edits", lambda h, st: "{} of {} ({})".format((st.get("renderq") or {}).get("budget", "?"),
                                                                st.get("ncpu", "?"), st.get("presence_why", ""))
        if st.get("reachable") else "-")
    row("Render queue", lambda h, st: "{} cores held, {} steps waiting".format(
        (st.get("renderq") or {}).get("cores_in_use", "?"), (st.get("renderq") or {}).get("waiting", "?"))
        if st.get("reachable") else "-")
    row("Load (5 min)", lambda h, st: "{:.1f} on {} cores".format(st["load"][1], st.get("ncpu"))
        if st.get("load") else "-")
    row("Memory pressure", lambda h, st: {1: "normal", 2: "WARNING", 4: "CRITICAL"}.get(st.get("pressure"), "?")
        if st.get("reachable") else "-")
    row("New edits", lambda h, st: "full: " + cap[h]["why"] if cap[h]["free"] <= 0 else "{} free".format(cap[h]["free"]))
    def gb(x):
        v = x.get("free_gb") or 0
        return "{:.1f} TB".format(v / 1000.0) if v >= 1000 else "{} GB".format(v)
    row("Free space", lambda h, st: ", ".join("{} {}".format(x["drive"], gb(x)) for x in st.get("drives", [])) or "-")
    row("Git vs GitHub", lambda h, st: ("level" if not (st["git"]["ahead"] or st["git"]["behind"]) else
                                        "ahead {} / behind {}".format(st["git"]["ahead"], st["git"]["behind"]))
        if st.get("git") else "-")
    widths = [max(len(str(r[i])) for r in rows + [[""] + [label(h, c) for h in hosts]]) for i in range(len(hosts) + 1)]
    widths = [min(w, 46) for w in widths]
    out = ["Two Macs: edit routing (numbers in editroute/hosts.json)   {}".format(
        dt.datetime.now().strftime("%a %b %-d %-I:%M %p")), ""]
    out.append("  ".join([" " * widths[0]] + [label(h, c).ljust(widths[i + 1]) for i, h in enumerate(hosts)]))
    for r in rows:
        out.append("  ".join(str(x)[:widths[i]].ljust(widths[i]) for i, x in enumerate(r)))
    out.append("")
    for k in ("SFC", "LFC", "OTHER"):
        h, why = decide("__probe__", k, 1, False, None, False, statuses, c, reservations(recent or []))
        out.append("Next {} would go to: {}".format(KIND_WORDS.get(k, k), h))
    out.append("")
    line = line or {}
    out.append("Combined waiting line (both Macs full): " + (", ".join(
        "{} ({}, waiting {})".format(w["job"], w["kind"], _ago(w.get("since"))) for w in
        sorted(line.values(), key=lambda w: w.get("since", 0))) or "nobody"))
    if reviews:
        out.append("")
        out.append("Review pages from M2 jobs, open on the M6 (same link on both):")
        for port, r in sorted(reviews.items(), key=lambda kv: -kv[1].get("t", 0))[:15]:
            out.append("  http://127.0.0.1:{}/  {}  (mirrored {} ago from {})".format(
                port, r.get("job", ""), _ago(r.get("t")), r.get("source", "")))
    return "\n".join(out)


def cmd_status(as_json=False):
    c = cfg()
    statuses = gather(None, c)
    d = state_dir()
    primary = c.get("primary")
    line, recent, reviews = {}, [], {}
    if me() == primary:
        line, recent = _read_json(d / "waiting.json", {}), decisions(d)
        reviews = _read_json(d / "reviews.json", {})
    elif statuses.get(primary, {}).get("reachable"):
        reviews = statuses[primary].get("reviews") or {}
    if as_json:
        print(json.dumps(dict(hosts=statuses, waiting=line, capacity=capacity(statuses, c, reservations(recent))),
                         indent=1, default=str))
    else:
        print(status_text(statuses, c, line, recent, reviews))
    return EXIT_GO


# ------------------------------------------------------------------------------------------------ files between Macs
def _remote_path(p):
    """A path for openrsync's remote side (it passes it to the remote shell): escape spaces and shell characters."""
    return re.sub(r"([ '\"()&;$`!*?\[\]{}<>|\\])", r"\\\1", str(p))


def _rsync(src, dst, backup=False):
    cmd = ["rsync", "-a", "--partial"]
    if backup:
        cmd += ["--backup", "--suffix=.m6-before-{}".format(dt.datetime.now().strftime("%Y%m%d-%H%M%S"))]
    r = subprocess.run(cmd + [src, dst], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("rsync failed ({}): {}".format(r.returncode, (r.stderr or "").strip()[-400:]))


def _ssh(h, command, timeout=60):
    c = cfg()
    hc = c["hosts"][h]
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout={}".format(c.get("remote_connect_s", 3)),
                           hc.get("ssh", h), command], capture_output=True, text=True, timeout=timeout)


def cmd_fetch(job, srcs, to=None):
    """M6: copy footage from the M2 (read only there) into this Mac's job folder."""
    c = cfg()
    here = me()
    other = next((h for h in c.get("hosts", {}) if h != here), None)
    if here != c.get("primary") or not other:
        print("This is the {}: the footage is on this Mac's own drives; use it in place.".format(here))
        return EXIT_ERR
    job = job_code(job)
    dest = Path(to) if to else Path(_renderq().workdir(job)) / "footage"
    dest.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for s in srcs:
        _rsync("{}:{}".format(c["hosts"][other].get("ssh", other), _remote_path(s)), str(dest) + "/")
        print(str(dest / Path(s.rstrip("/")).name))
    print("  copied {} item(s) from the {} in {:.0f} s; the originals on the {} were only read.".format(
        len(srcs), other, time.time() - t0, other))
    return EXIT_GO


def cmd_push(paths, dest_host=None):
    """M2: copy finished files into the M6's project folder at the same relative place (older copy kept)."""
    c = cfg()
    dest_host = dest_host or c.get("primary")
    if me() == dest_host:
        print("This is the {} already; the files are in its project folder.".format(dest_host))
        return EXIT_ERR
    repo = Path(REPO).resolve()
    rrepo = c["hosts"][dest_host]["repo"]
    for p in paths:
        ap = Path(p).resolve()
        try:
            rel = ap.relative_to(repo)
        except ValueError:
            print("skipped (not inside the project folder {}): {}".format(repo, p))
            continue
        target = "{}/{}".format(rrepo, rel.as_posix())
        r = _ssh(dest_host, "mkdir -p " + shlex.quote(str(Path(target).parent)))
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip())
        src = str(ap) + ("/" if ap.is_dir() else "")
        _rsync(src, "{}:{}".format(c["hosts"][dest_host].get("ssh", dest_host),
                                   _remote_path(target + ("/" if ap.is_dir() else ""))), backup=True)
        print("{} -> {}:{}".format(rel, dest_host, target))
    return EXIT_GO


def _hub_cache(port):
    return Path.home() / "Library/Application Support/AbsByAI Reviews" / str(port) / "page"


def mirror_review(port, root, job=None):
    """On the M2: copy the review page's cached files (only what the page links) to the M6 and serve them there on
    the same port, so the link Dan gets opens on his Mac. Returns the M6 link, or raises."""
    c = cfg()
    hc = hostcfg.host(me(), c) or {}
    dest_host = hc.get("mirror_reviews_to")
    if not dest_host:
        return None
    cache = _hub_cache(port)
    if not cache.is_dir():
        raise RuntimeError("no cached page for port {} on this Mac (run review_server.py first)".format(port))
    job = job or job_code(next((x for x in Path(root).parts[::-1] if re.match(r"^[A-Za-z]{2,3}-?\d", x)), "")) or ""
    rel = "Library/Application Support/AbsByAI Reviews/m2-mirror/{}".format(port)
    r = _ssh(dest_host, "mkdir -p " + shlex.quote(rel))
    if r.returncode != 0:
        raise RuntimeError("cannot reach the {}: {}".format(dest_host, (r.stderr or "").strip()))
    _rsync(str(cache) + "/", "{}:{}/".format(c["hosts"][dest_host].get("ssh", dest_host), _remote_path(rel)))
    drepo = c["hosts"][dest_host]["repo"]
    note = json.dumps(dict(job=job, source="{}:{}".format(me(), root), port=port))
    cmd = ("cd ~ && ABS_REVIEW_NO_MIRROR=1 python3 {srv} {port} {dir} && python3 {er} note-review {port} {note}"
           .format(srv=shlex.quote(drepo + "/.claude/skills/_shared/review_server.py"), port=int(port),
                   dir=shlex.quote(rel), er=shlex.quote(drepo + "/.claude/skills/_shared/editroute/editroute.py"),
                   note=shlex.quote(note)))
    r = _ssh(dest_host, cmd, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("the {} could not serve it: {}".format(dest_host, (r.stderr or r.stdout).strip()[-300:]))
    return "http://127.0.0.1:{}/".format(int(port))


def mirror_review_if_remote(port, root):
    """Called by review_server.py after it serves a page. Prints one line; never raises."""
    try:
        if not (hostcfg.host() or {}).get("mirror_reviews_to"):
            return None
        link = mirror_review(port, root)
        if link:
            print("Also open on the M6 (Dan's Mac): {}  (same link; this page was made on the M2)".format(link))
        return link
    except Exception as e:
        print("Note: this page was NOT mirrored to the M6 ({}). Dan can still open it through `editroute.py "
              "mirror-review {} <dir>` once the M6 answers.".format(e, port))
        return None


def cmd_note_review(port, note):
    d = state_dir()
    with _Lock(d):
        r = _read_json(d / "reviews.json", {})
        e = json.loads(note)
        e["t"] = round(time.time(), 1)
        r[str(port)] = e
        _write_json(d / "reviews.json", r)
    return EXIT_GO


def _port_used_here(port):
    with socket.socket() as s:
        s.settimeout(0.3)
        if s.connect_ex(("127.0.0.1", port)) == 0:
            return True
    hub = Path.home() / "Library/Application Support/AbsByAI Review Hub/pages" / "{}.json".format(port)
    agent = Path.home() / "Library/LaunchAgents" / "com.absbyai.review.{}.plist".format(port)
    return hub.exists() or agent.exists()


def cmd_free_port(start=9800, local_only=False):
    c = cfg()
    for port in range(int(start), 65000):
        if _port_used_here(port):
            continue
        if local_only:
            print(port)
            return EXIT_GO
        ok = True
        for h in c.get("hosts", {}):
            if h == me():
                continue
            r = _ssh(h, "python3 {} free-port --from {} --local".format(
                shlex.quote(c["hosts"][h]["repo"] + "/.claude/skills/_shared/editroute/editroute.py"), port))
            if r.returncode != 0 or r.stdout.strip() != str(port):
                ok = False
                break
        if ok:
            print(port)
            return EXIT_GO
    return EXIT_ERR


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
        import unittest
        suite = unittest.defaultTestLoader.discover(str(HERE / "tests"))
        return 0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1
    if cmd == "local-status":
        o, _ = _opts(rest, {"--json": False, "--job": True})
        print(json.dumps(local_status(job_code(o["--job"]) if o.get("--job") else None), default=str))
        return 0
    if cmd == "status":
        o, _ = _opts(rest, {"--json": False})
        return cmd_status(bool(o.get("--json")))
    if cmd in ("pick", "wait"):
        f = _forward(argv)
        if f is not None:
            return f
    if cmd == "pick":
        o, pos = _opts(rest, {"--kind": True, "--round": True, "--chroma": False, "--host": True, "--move": False,
                              "--dry-run": False, "--json": False})
        if not pos:
            sys.exit("usage: editroute.py pick JOB [--kind K] [--round N] [--chroma] [--host m6|m2]")
        if o.get("--kind") and o["--kind"].upper() not in KINDS:
            sys.exit("--kind must be one of: " + ", ".join(sorted(set(KINDS.values()))))
        named = (o.get("--host") or "").lower() or None
        return cmd_pick(pos[0], o.get("--kind"), int(o.get("--round") or 1), bool(o.get("--chroma")), named,
                        bool(o.get("--move")), bool(o.get("--dry-run")), bool(o.get("--json")))
    if cmd == "wait":
        o, pos = _opts(rest, {"--max-hours": True})
        return cmd_wait(pos[0], float(o.get("--max-hours") or 24))
    if cmd == "where":
        return cmd_where(rest[0])
    if cmd == "fetch":
        o, pos = _opts(rest, {"--to": True})
        if len(pos) < 2:
            sys.exit("usage: editroute.py fetch JOB SRC [SRC ...] [--to DIR]")
        return cmd_fetch(pos[0], pos[1:], o.get("--to"))
    if cmd == "push":
        o, pos = _opts(rest, {"--to-host": True})
        return cmd_push(pos, o.get("--to-host"))
    if cmd == "mirror-review":
        print(mirror_review(int(rest[0]), Path(rest[1]).resolve()) or "This Mac does not mirror review pages.")
        return 0
    if cmd == "note-review":
        return cmd_note_review(rest[0], rest[1])
    if cmd == "free-port":
        o, _ = _opts(rest, {"--from": True, "--local": False})
        return cmd_free_port(int(o.get("--from") or 9800), bool(o.get("--local")))
    if cmd == "whoami":
        h = me()
        print(h or "unknown Mac (hosts.json does not know it)")
        print("  slots {}, cores now {}, {}".format(hostcfg.slots(), hostcfg.core_budget(), hostcfg.presence()[1]))
        return 0
    sys.exit("unknown command: " + cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
