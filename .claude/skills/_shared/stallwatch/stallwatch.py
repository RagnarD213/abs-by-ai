#!/usr/bin/env python3
"""Stall watchdog for video edit jobs (Dan, 2026-11-05). Rule: VIDEO-RULES.md, "Chains are watched by their exit".

Why: on 2026-11-04 the RO-31 R3 chain died at 8:22 PM on a SyntaxError in its finish step. The error went to
final/logs/finish.log; the session's background watcher only grepped chain.log for DONE/error, so it never fired
and the job sat dead for 11 hours until Dan asked.

Two layers:
  1. Every chain runs under `stallwatch.py run`, in the background, so the session is woken by the EXIT, whatever
     the logs say:
        python3 stallwatch.py run RO-31 -- bash chain_r3c.sh
     It records the run, passes the exit code through, and on exit prints CHAIN_DONE or CHAIN_FAILED with the tail
     of the newest log in the folder.
  2. A routine runs `stallwatch.py scan --claim --json` every 15 minutes. A job is STALLED when no process for it is
     alive (render queue, `ps` by work folder, its recorded run), its logs have not changed for 20+ minutes, and its
     newest log ends without a DONE marker (or it ended in CHAIN_FAILED / a non-zero exit). The routine messages the
     owning Claude session (at most 2 nudges, 30 min apart), then tells Dan. Codex-owned jobs go to Dan directly
     (nothing on the Claude side can post into a Codex thread); Codex heartbeats can call `check`.

    stallwatch.py run JOB [--log FILE] -- CMD...   run a chain, record it, report on exit (exit code passed through)
    stallwatch.py scan [--json] [--claim]          every watched job and its state; --claim records nudges as sent
    stallwatch.py check JOB                        exit 0 running/done/idle, 5 stalled (prints why)
    stallwatch.py ok JOB                           "I know, it is fine": silence this stall until the job moves again
    stallwatch.py unsent JOB                       undo the last claimed nudge (delivery failed)
    stallwatch.py selftest

Read-only towards jobs: it never kills, restarts or edits anything. State: /tmp/absbyai-stallwatch/ (STALLWATCH_DIR).
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent
DIR = Path(os.environ.get("STALLWATCH_DIR") or "/tmp/absbyai-stallwatch")
QUIET_S = float(os.environ.get("STALLWATCH_QUIET_MIN") or 20) * 60     # logs unchanged this long = suspicious
RECENT_S = 24 * 3600            # only work active in the last day is watched
NUDGE_GAP_S = 30 * 60           # between nudges, and before telling Dan
MAX_NUDGES = 2
EXIT_STALLED = 5
WORK_FOLDERS = ("_edit_work", "Abs By AI Edit Work")
SKIP_DIRS = re.compile(r"frame|cache|clips_graded|_scratch|node_modules|\.git|hyperframes_out", re.I)
WATCHERS = {"tail", "grep", "egrep", "fgrep", "rg", "sleep", "cat", "less", "more", "head", "watch", "fswatch",
            "caffeinate", "ps", "lsof", "pgrep", "wc", "find", "ls", "stat", "osascript"}
WATCHER_PY = re.compile(r"review_server|http\.server|stallwatch|editcap\.py|renderq\.py\s+(status|why|drives)")
SHELLS = {"bash", "sh", "zsh", "dash", "fish"}
DONE_RE = re.compile(r"(^|[^A-Za-z])(\w*_)?DONE\b")    # DONE, ALL DONE, R3_DONE: counts only on the last line
CHAIN_DONE_RE = re.compile(r"\bCHAIN(_\w+)?_DONE\b")     # CHAIN_DONE, CHAIN_R3_DONE: anywhere in the tail
FAIL_RE = re.compile(r"\bCHAIN(_\w+)?_FAILED\b")
ERR_RE = re.compile(r"Traceback|[A-Za-z]+Error\b|Exception\b|CHAIN_FAILED|No such file|Killed|command not found|"
                    r"Segmentation fault|\bERROR\b|exit (code |status )?[1-9]")


def _now():
    return time.time()


# ------------------------------------------------------------------------------------------------ helpers
def _editcap():
    try:
        if str(SHARED / "editcap") not in sys.path:
            sys.path.insert(0, str(SHARED / "editcap"))
        import editcap                                           # noqa: E402
        return editcap
    except Exception:
        return None


def job_code(name):
    ec = _editcap()
    try:
        return (ec.job_code(name) if ec else None) or name
    except Exception:
        return name


def _who():
    if os.environ.get("CLAUDE_CODE_HOST_SESSION_ID"):
        return "claude", os.environ["CLAUDE_CODE_HOST_SESSION_ID"]
    for k in ("CODEX_THREAD_ID", "CODEX_SESSION_ID"):
        if os.environ.get(k):
            return "codex", os.environ[k]
    if any(k.startswith("CODEX") for k in os.environ):
        return "codex", ""
    return "", ""


def _read_json(p, default):
    try:
        with open(p) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".{}.tmp".format(os.getpid()))
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, p)
    try:
        os.chmod(p, 0o666)
    except OSError:
        pass


def _alive(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, TypeError):
        return False


def _clock(t):
    return time.strftime("%-I:%M %p", time.localtime(t)) if t else "?"


def _ago(t, now):
    s = max(0, now - (t or now))
    return "{} min".format(int(s // 60)) if s < 5400 else "{:.1f} h".format(s / 3600)


# ------------------------------------------------------------------------------------------------ runs
def _runs_dir():
    return DIR / "runs"


def runs():
    out = []
    try:
        names = os.listdir(str(_runs_dir()))
    except OSError:
        return out
    for n in names:
        if n.endswith(".json"):
            r = _read_json(_runs_dir() / n, None)
            if isinstance(r, dict) and r.get("job"):
                out.append(r)
    return out


def _tail_lines(path, n=15):
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 16000))
            lines = f.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return []
    return [l for l in lines if l.strip()][-n:]


def run(job, cmd, log=None):
    """Run a chain, recording it so the watchdog knows its pid, folder and outcome. Returns the command's exit code."""
    job = job_code(job)
    ai, wake = _who()
    cwd = os.getcwd()
    key = "{}-{}".format(re.sub(r"[^A-Za-z0-9_-]", "_", job), int(_now() * 1000))
    rec = dict(job=job, cmd=" ".join(cmd), cwd=cwd, log=log, ai=ai, wake=wake, start=_now(), pid=None, end=None,
               exit=None, key=key)
    path = _runs_dir() / (key + ".json")
    env = dict(os.environ, STALLWATCH_JOB=job)
    if not env.get("GATE_GROUP"):
        env["GATE_GROUP"] = job
    try:
        p = subprocess.Popen(cmd, env=env)
    except OSError as e:
        print("CHAIN_FAILED {}: could not start ({})".format(job, e))
        return 127
    rec["pid"] = p.pid
    _write_json(path, rec)
    try:
        code = p.wait()
    except KeyboardInterrupt:
        p.terminate()
        code = p.wait()
    rec.update(end=_now(), exit=code)
    _write_json(path, rec)
    newest = newest_logs(Path(log).parent if log else Path(cwd), limit=1, extra=[log] if log else [])
    where = newest[0][1] if newest else None
    if code == 0:
        print("CHAIN_DONE {} (exit 0)".format(job))
    else:
        print("CHAIN_FAILED {} exit {}{}".format(job, code, " - newest log: " + where if where else ""))
        for line in _tail_lines(where, 20) if where else []:
            print("  " + line)
    return code


# ------------------------------------------------------------------------------------------------ logs
def newest_logs(root, limit=3, max_depth=5, extra=()):
    """[(mtime, path)] of the newest *.log files under root, newest first. Skips frame/cache folders."""
    found = []
    for x in extra or ():
        try:
            if x:
                found.append((os.stat(x).st_mtime, str(x)))
        except OSError:
            pass
    root = str(root)
    stack = [(root, 0)]
    while stack:
        d, depth = stack.pop()
        try:
            with os.scandir(d) as it:
                entries = list(it)
        except OSError:
            continue
        if len(entries) > 3000:                     # a frame dump, not a log folder
            continue
        for e in entries:
            try:
                if e.is_dir(follow_symlinks=False):
                    if depth < max_depth and not SKIP_DIRS.search(e.name) and not e.name.startswith("."):
                        stack.append((e.path, depth + 1))
                elif e.name.endswith(".log") or e.name in ("CHAIN_DONE", "DONE"):
                    found.append((e.stat().st_mtime, e.path))
            except OSError:
                continue
    found = sorted(set(found), reverse=True)
    return found[:limit]


def log_verdict(logs):
    """('done'|'failed'|None, hint line) from the newest logs."""
    if not logs:
        return None, ""
    t0, newest = logs[0]
    if os.path.basename(newest) in ("CHAIN_DONE", "DONE"):
        return "done", ""
    verdict = None
    tail = _tail_lines(newest, 15)
    for line in tail:                               # the explicit markers, whichever came last
        if FAIL_RE.search(line):
            verdict = "failed"
        elif CHAIN_DONE_RE.search(line):
            verdict = "done"
    if verdict is None and tail and DONE_RE.search(tail[-1]):
        verdict = "done"                            # per-step "DONE" lines higher up do not count
    hint = ""
    for _t, p in logs:
        errs = [l.strip() for l in _tail_lines(p, 40) if ERR_RE.search(l)]
        if errs:
            hint = "{}: {}".format(os.path.basename(p), errs[-1][:240])
            break
    return verdict, hint


# ------------------------------------------------------------------------------------------------ processes
def process_table():
    """[{pid, ppid, cmd, cwd}] for every process (cwd from one lsof call; empty where not allowed)."""
    procs = {}
    try:
        r = subprocess.run(["ps", "-Ao", "pid=,ppid=,command="], capture_output=True, text=True, timeout=20)
        for line in r.stdout.splitlines():
            f = line.strip().split(None, 2)
            if len(f) >= 2 and f[0].isdigit():
                procs[int(f[0])] = dict(pid=int(f[0]), ppid=int(f[1]), cmd=f[2] if len(f) > 2 else "", cwd="")
    except (OSError, subprocess.TimeoutExpired):
        return []
    try:
        r = subprocess.run(["lsof", "-nP", "-a", "-d", "cwd", "-Fpn"], capture_output=True, text=True, timeout=30)
        pid = None
        for line in r.stdout.splitlines():
            if line.startswith("p"):
                pid = int(line[1:]) if line[1:].isdigit() else None
            elif line.startswith("n") and pid in procs:
                procs[pid]["cwd"] = line[1:]
    except (OSError, subprocess.TimeoutExpired):
        pass
    return list(procs.values())


def _argv0(cmd):
    first = cmd.split()[0] if cmd.split() else ""
    return os.path.basename(first).lstrip("-")


def _kind(p):
    """'watcher', 'shell' or 'worker'."""
    b = _argv0(p["cmd"])
    if b in WATCHERS:
        return "watcher"
    if b.lower().startswith("python") and WATCHER_PY.search(p["cmd"]):
        return "watcher"
    if b in SHELLS:
        return "shell"
    return "worker"


def _shell_has_script(cmd):
    """bash chain.sh -> True; bash, -zsh, zsh -l, bash -c '...' -> False."""
    parts = cmd.split()[1:]
    if "-c" in parts:
        return False
    return any(not x.startswith("-") for x in parts)


def job_processes(table, dirs, job, run_pids):
    """Live working processes of one job: anything whose cwd or command is in the job's folders, or that descends
    from its recorded run. Watchers (tail/grep/sleep loops, review servers) do not count; a shell counts only if it
    runs a script file or has a working child."""
    dirs = [x for d in dirs if d and _is_work_folder(d)
            for x in {str(d).rstrip("/") + "/", os.path.realpath(str(d)).rstrip("/") + "/"}]
    kids = {}
    for p in table:
        kids.setdefault(p["ppid"], []).append(p)
    under_run = set(run_pids)
    stack = list(run_pids)
    while stack:
        for c in kids.get(stack.pop(), []):
            if c["pid"] not in under_run:
                under_run.add(c["pid"])
                stack.append(c["pid"])

    def descendants(pid):
        out, stack, seen = [], [pid], set()
        while stack:
            for c in kids.get(stack.pop(), []):
                if c["pid"] not in seen:
                    seen.add(c["pid"])
                    out.append(c)
                    stack.append(c["pid"])
        return out

    def in_job(p):
        if p["pid"] in under_run:
            return True
        cwd = (p.get("cwd") or "").rstrip("/") + "/"
        if any(cwd.startswith(d) for d in dirs):
            return True
        if any(d in p["cmd"] or d.rstrip("/") + " " in p["cmd"] + " " for d in dirs):
            return True
        return bool(re.search(r"--group[ =]{}(\s|$)".format(re.escape(job)), p["cmd"]))

    working = []
    for p in table:
        if not in_job(p):
            continue
        k = _kind(p)
        if k == "worker":
            working.append(p)
        elif k == "shell":
            if _shell_has_script(p["cmd"]) or any(_kind(c) == "worker" for c in descendants(p["pid"])):
                working.append(p)
    return working


def _is_work_folder(d):
    return any("/{}/".format(f) in str(d) + "/" for f in WORK_FOLDERS)


# ------------------------------------------------------------------------------------------------ jobs
def work_roots():
    env = os.environ.get("STALLWATCH_WORKROOTS")
    if env is not None:
        return [Path(x) for x in env.split(":") if x]
    out = []
    try:
        for n in os.listdir("/Volumes"):
            out.append(Path("/Volumes") / n)
    except OSError:
        pass
    return out


def find_dirs(job):
    """Every work folder of a job on the plugged-in drives (Codex suffixes like DS-40-codex included)."""
    hits = []
    for root in work_roots():
        for folder in WORK_FOLDERS:
            base = root / folder
            try:
                names = os.listdir(str(base))
            except OSError:
                continue
            for n in names:
                if n.startswith((".", "_")):
                    continue
                if (n.lower() == job.lower() or job_code(n) == job) and (base / n).is_dir():
                    hits.append(base / n)
    return hits


def editcap_entries():
    """{job: entry} from the edit cap registry (state, ai, wake), without settling or writing anything."""
    p = Path(os.environ.get("EDITCAP_DIR") or "/tmp/absbyai-editcap") / "registry.json"
    reg = _read_json(p, {})
    ed = reg.get("edits") if isinstance(reg, dict) else None
    return ed if isinstance(ed, dict) else {}


def renderq_live():
    """{job: live step count} from the render queue; {} if unreadable."""
    if os.environ.get("STALLWATCH_NO_RENDERQ"):
        return {}
    try:
        return {j: a.get("live", 0) for j, a in _editcap().renderq_activity().items()}
    except Exception:
        return {}


def assess(now=None, table=None, entries=None, live=None, run_list=None):
    """One row per watched job: status running | done | stalled | idle | quiet, with owner and evidence."""
    now = now or _now()
    table = process_table() if table is None else table
    entries = editcap_entries() if entries is None else entries
    live = renderq_live() if live is None else live
    run_list = runs() if run_list is None else run_list
    by_job = {}
    for r in run_list:
        if now - (r.get("end") or r.get("start") or 0) < RECENT_S or _alive(r.get("pid")):
            by_job.setdefault(r["job"], []).append(r)
    jobs = {j for j, e in entries.items() if e.get("state") in ("active", "promoted", "stalled")} | set(by_job)
    rows = []
    for job in sorted(jobs):
        e = entries.get(job, {})
        if e.get("state") in ("with-dan", "waiting"):
            continue
        rs = sorted(by_job.get(job, []), key=lambda r: r.get("start", 0))
        last_run = rs[-1] if rs else None
        dirs = find_dirs(job)
        for r in rs:
            m = re.search(r"^(.*/(?:_edit_work|Abs By AI Edit Work)/[^/]+)", r.get("cwd") or "")
            d = Path(m.group(1)) if m else (Path(r["log"]).parent if r.get("log") else Path(r.get("cwd") or "/x"))
            if d not in dirs:
                dirs.append(d)
        ai = e.get("ai") or (last_run or {}).get("ai") or ""
        wake = e.get("wake") or (last_run or {}).get("wake") or ""
        if last_run and last_run.get("wake") and last_run.get("start", 0) >= e.get("since", 0):
            ai, wake = last_run.get("ai") or ai, last_run["wake"]
        row = dict(job=job, title=e.get("title", ""), ai=ai, session=wake, editcap=e.get("state", ""),
                   dirs=[str(d) for d in dirs])
        run_pids = {r["pid"] for r in rs if r.get("pid") and _alive(r["pid"]) and r.get("end") is None}
        procs = job_processes(table, dirs, job, run_pids)
        logs = []
        for d in dirs:
            logs += newest_logs(d, extra=[(r.get("log")) for r in rs if r.get("log")])
        # Only work done since the edit took its current slot counts: older logs belong to an earlier round.
        since = e.get("active_since", 0) - 120 if e.get("state") in ("active", "promoted", "stalled") else 0
        logs = [x for x in sorted(set(logs), reverse=True) if x[0] >= since][:3]
        rs = [r for r in rs if (r.get("end") or r.get("start") or 0) >= since or _alive(r.get("pid"))]
        last_run = rs[-1] if rs else None
        verdict, hint = log_verdict(logs)
        last = max([t for t, _ in logs] + [r.get("end") or r.get("start") or 0 for r in rs] + [0])
        row.update(last_activity=last, newest_log=logs[0][1] if logs else "", hint=hint,
                   processes=[dict(pid=p["pid"], cmd=p["cmd"][:160]) for p in procs][:5],
                   renderq=live.get(job, 0))
        if last_run and last_run.get("end") and (not logs or last_run["end"] >= logs[0][0] - 5):
            verdict = "done" if last_run.get("exit") == 0 else "failed"
            if last_run.get("exit"):
                hint = hint or "exit {} from `{}`".format(last_run["exit"], last_run.get("cmd", "")[:120])
        elif last_run and last_run.get("end") is None and not _alive(last_run.get("pid")) and \
                last_run.get("start", 0) >= (logs[0][0] if logs else 0) - 5:
            verdict, hint = "failed", hint or "its process disappeared without an exit code (killed or app quit)"
        quiet = now - last if last else None
        if live.get(job) or procs:
            status, why = "running", ("{} render-queue step(s)".format(live[job]) if live.get(job) else
                                      "process {} alive".format(procs[0]["pid"]))
        elif verdict == "done":
            status, why = "done", "finished cleanly"
        elif not last or quiet > RECENT_S:
            status, why = "idle", ("no log or run since the edit took its slot" if since > 0 else
                                   "no log or run in the last 24 h")
        elif quiet >= QUIET_S:                      # a failed chain gets the same grace: its own run woke it
            status = "stalled"
            why = "{}nothing running for {}, logs last changed {}".format(
                "the chain failed; " if verdict == "failed" else "", _ago(last, now), _clock(last))
        else:
            status, why = "quiet", "no process, logs changed {} ago (stalled at {} min)".format(
                _ago(last, now), int(QUIET_S // 60))
        row.update(status=status, why=why, signature="{}|{}".format(row["newest_log"], int(last)))
        rows.append(row)
    return rows


# ------------------------------------------------------------------------------------------------ nudges
def _state():
    s = _read_json(DIR / "state.json", {})
    return s if isinstance(s, dict) and isinstance(s.get("jobs"), dict) else {"jobs": {}}


def _message(row, n):
    where = row["newest_log"] or (row["dirs"][0] if row["dirs"] else "its work folder")
    return ("Stall watchdog: {job}{title} looks dead. {why}. Newest log: {where}.{hint} Nothing for this job is "
            "running in the render queue or `ps`, and there is no DONE marker. Read that log (and the other logs in "
            "the folder), fix the cause, and restart the failed step from its checkpoint without redoing finished "
            "steps; run it under `python3 .claude/skills/_shared/stallwatch/stallwatch.py run {job} -- ...` in the "
            "background so its exit wakes you. If the job is actually finished or waiting on Dan, run "
            "`python3 .claude/skills/_shared/stallwatch/stallwatch.py ok {job}` (or `editcap.py release {job} "
            "--review`) and reply in one line. Nudge {n} of {max}; after that the watchdog tells Dan."
            .format(job=row["job"], title=" ({})".format(row["title"]) if row["title"] else "", why=row["why"],
                    where=where, hint=" Last error line: " + row["hint"] + "." if row["hint"] else "", n=n,
                    max=MAX_NUDGES))


def _dan_message(row, reason):
    return ("Video job {job}{title} has stopped and is not being restarted ({reason}). {why}. Newest log: {where}. "
            "Owner: {owner}. Open that session and tell it to restart the job, or tell me to."
            .format(job=row["job"], title=" ({})".format(row["title"]) if row["title"] else "", reason=reason,
                    why=row["why"], where=row["newest_log"] or "none",
                    owner="{} {}".format(row["ai"] or "unknown AI", row["session"] or "(no session recorded)")))


def plan(rows, now=None, claim=False):
    """Nudge/notify actions for stalled rows. claim=True records them as sent (the routine delivers them)."""
    now = now or _now()
    st = _state()
    actions = []
    seen = set()
    for row in rows:
        job = row["job"]
        seen.add(job)
        j = st["jobs"].get(job)
        if row["status"] != "stalled":
            if j and row["status"] in ("running", "done", "idle"):
                st["jobs"].pop(job, None)
            continue
        if j and j.get("acked") == row["signature"]:
            row["status"], row["why"] = "acked", "stall acknowledged by its session (`ok`)"
            continue
        if not j or j.get("signature") != row["signature"]:
            j = st["jobs"][job] = dict(signature=row["signature"], nudges=0, last=0, dan=0)
        if row["ai"] == "claude" and row["session"].startswith("local_"):
            if j["nudges"] < MAX_NUDGES and (j["nudges"] == 0 or now - j["last"] >= NUDGE_GAP_S):
                n = j["nudges"] + 1
                actions.append(dict(kind="nudge", job=job, ai="claude", session=row["session"], n=n,
                                    message=_message(row, n)))
                if claim:
                    j.update(nudges=n, last=now)
                continue
            if j["nudges"] >= MAX_NUDGES and not j["dan"] and now - j["last"] >= NUDGE_GAP_S:
                actions.append(dict(kind="dan", job=job, message=_dan_message(
                    row, "its Claude session was nudged {} times and the job is still dead".format(MAX_NUDGES))))
                if claim:
                    j["dan"] = now
        elif not j["dan"]:
            reason = ("owned by Codex thread {}; Claude cannot post into a Codex thread".format(row["session"])
                      if row["ai"] == "codex" else "no Claude session is recorded for it")
            actions.append(dict(kind="dan", job=job, message=_dan_message(row, reason)))
            if claim:
                j["dan"] = now
    for job in list(st["jobs"]):
        if job not in seen and not st["jobs"][job].get("acked"):
            st["jobs"].pop(job, None)
    if claim:
        _write_json(DIR / "state.json", st)
        if any(a["kind"] == "dan" for a in actions) and not os.environ.get("STALLWATCH_NO_NOTIFY"):
            for a in actions:
                if a["kind"] == "dan":
                    _mac_notify("Video job {} has stopped".format(a["job"]), a["message"])
    return actions


def _mac_notify(title, body):
    try:
        subprocess.run(["osascript", "-e", "display notification {} with title {}".format(
            json.dumps(body[:220]), json.dumps(title))], capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        pass


def ack(job):
    job = job_code(job)
    rows = [r for r in assess() if r["job"] == job]
    st = _state()
    sig = rows[0]["signature"] if rows else ""
    st["jobs"].setdefault(job, {})["acked"] = sig
    _write_json(DIR / "state.json", st)
    return "{}: stall acknowledged; the watchdog stays quiet until the job's logs or runs change.".format(job)


def unsent(job):
    job = job_code(job)
    st = _state()
    j = st["jobs"].get(job)
    if j and j.get("nudges"):
        j["nudges"] -= 1
        j["last"] = 0
        _write_json(DIR / "state.json", st)
        return "{}: last nudge marked unsent.".format(job)
    return "{}: nothing to undo.".format(job)


def scan_text(rows, actions, now):
    out = ["Stall watchdog: {} watched job(s), {} stalled, {} action(s).".format(
        len(rows), sum(r["status"] == "stalled" for r in rows), len(actions))]
    for r in rows:
        out.append("  {} [{} {}] {}: {}".format(r["job"], r["ai"] or "?", (r["session"] or "")[:14], r["status"],
                                                r["why"]))
    for a in actions:
        out.append("ACTION {} {} {}".format(a["kind"], a["job"], a.get("session", "dan")))
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------ CLI
def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "selftest":
        sys.path.insert(0, str(HERE))
        import selftest                                         # noqa: E402
        return selftest.main()
    if cmd == "run":
        if "--" not in rest or rest.index("--") == 0:
            sys.exit("usage: stallwatch.py run JOB [--log FILE] -- CMD...")
        i = rest.index("--")
        head, command = rest[:i], rest[i + 1:]
        log = head[head.index("--log") + 1] if "--log" in head else None
        return run(head[0], command, log=log)
    if cmd == "scan":
        now = _now()
        rows = assess(now)
        actions = plan(rows, now, claim="--claim" in rest)
        if "--json" in rest:
            print(json.dumps(dict(now=now, jobs=rows, actions=actions), indent=1))
        else:
            print(scan_text(rows, actions, now))
        return 0
    if not rest:
        sys.exit("usage: stallwatch.py {} JOB".format(cmd))
    if cmd == "check":
        job = job_code(rest[0])
        rows = [r for r in assess() if r["job"] == job]
        if not rows:
            print("{}: not watched (no active edit slot or recorded run in the last 24 h).".format(job))
            return 0
        print("{}: {}: {}{}".format(job, rows[0]["status"], rows[0]["why"],
                                    " | " + rows[0]["hint"] if rows[0]["hint"] else ""))
        return EXIT_STALLED if rows[0]["status"] == "stalled" else 0
    if cmd == "ok":
        print(ack(rest[0]))
        return 0
    if cmd == "unsent":
        print(unsent(rest[0]))
        return 0
    sys.exit("unknown command: " + cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
