#!/usr/bin/env python3
"""ETA for every video edit, shown on Dan's Edit Queue page (Dan, 2026-11-18).

No AI tokens: an editing session reports its plan and each step with one command, and a plain script
(launchd, every 10 minutes on the M6) turns that plus the render queue and the edit slots of BOTH Macs into
a time range, then uploads one small file the page reads.

Editing sessions (Claude or Codex, either Mac) run these on the Mac doing the work:
  eta.py plan  JOB "Take map:20" "Key 14 pieces:180" "Build film:60" "Review page:10"   # name:minutes
  eta.py step  JOB 3 [--expect 45]     # step 3 starts now (finishes the one before, records its real time)
  eta.py left  JOB 40                  # "about 40 minutes left in this step" when you can measure it
  eta.py retry JOB "audio check failed, re-rendering"   # a step is being redone: clock restarts, range widens
  eta.py done  JOB                     # delivered for review (also cleared by editcap release)

Read it:
  eta.py estimate [--json]             # jobs on THIS Mac
  eta.py show                          # both Macs, plain words (what the page shows)
  eta.py refresh [--force]             # both Macs -> Drive file for the page (launchd runs this)

Data: ~/.absbyai-eta/<JOB>.json per Mac, ~/.absbyai-eta/history.jsonl (real step times, for learning).
"""
import argparse, datetime, json, os, re, statistics, subprocess, sys, time
from pathlib import Path

REPO = Path(os.environ["ETA_REPO"]) if os.environ.get("ETA_REPO") else Path(__file__).resolve().parents[4]
DIR = Path(os.environ.get("ETA_DIR") or Path.home() / ".absbyai-eta")
HISTORY = DIR / "history.jsonl"
EDITCAP = REPO / ".claude/skills/_shared/editcap/editcap.py"
RENDERQ = REPO / ".claude/skills/_shared/renderq/renderq.py"
HOSTS = REPO / ".claude/skills/_shared/editroute/hosts.json"
RCLONE = os.path.expanduser("~/bin/rclone")
DRIVE_REMOTE = os.environ.get("EDIT_QUEUE_DRIVE_REMOTE", "gdrive_backup:").rstrip(":") + ":"
DRIVE_PATH = DRIVE_REMOTE + "Abs By AI automation/edit-queue-eta.json"
OUT = REPO / "tmp" / "edit-queue-export" / "edit-queue-eta.json"
ORPHAN_S = 60 * 60     # a plan with no edit slot and no render work for this long belongs to a finished edit
STALL_MIN = 45          # no sign of life for this long and nothing rendering -> "may be stuck"
PUSH_EVERY_S = 30 * 60  # re-upload at least this often even if nothing changed (page shows "checked at")


# ------------------------------------------------------------------ progress files (one per job, per Mac)
def _path(job):
    return DIR / (re.sub(r"[^A-Za-z0-9._-]", "_", job) + ".json")


def load(job):
    try:
        return json.loads(_path(job).read_text())
    except (OSError, ValueError):
        return None


def save(job, rec):
    DIR.mkdir(parents=True, exist_ok=True)
    rec["updated"] = time.time()
    tmp = _path(job).with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, indent=1))
    os.replace(tmp, _path(job))


def norm(name):
    """'Key 14 pieces' and 'key 9 pieces' learn from each other: drop numbers and punctuation."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z ]", " ", name.lower())).strip()


def record_history(job, step, now):
    if not step.get("started"):
        return
    dur = (now - step["started"]) / 60.0
    if dur < 0.2:
        return
    DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY, "a") as f:
        f.write(json.dumps(dict(job=job, kind=job.split("-")[0], step=norm(step["name"]), expect=step.get("expect"),
                                minutes=round(dur, 1), retries=step.get("retries", 0), t=now)) + "\n")


def learned(name, kind=None, lines=None):
    """Median real minutes for this kind of step (same job prefix first, then any job). None = no history."""
    if lines is None:
        try:
            lines = HISTORY.read_text().splitlines()[-2000:]
        except OSError:
            lines = []
    key, same, anyk = norm(name), [], []
    for line in lines:
        try:
            h = json.loads(line)
        except ValueError:
            continue
        if h.get("step") == key:
            anyk.append(h["minutes"])
            if kind and h.get("kind") == kind:
                same.append(h["minutes"])
    use = (same if len(same) >= 2 else anyk)[-10:]
    return statistics.median(use) if len(use) >= 2 else None


def cmd_plan(job, steps, now=None):
    now = now or time.time()
    out = []
    for s in steps:
        name, _, mins = s.rpartition(":")
        if not name:
            name, mins = s, ""
        try:
            exp = float(mins)
        except ValueError:
            exp = None
        out.append(dict(name=name.strip(), expect=exp))
    rec = dict(job=job, steps=out, current=1, plan_at=now, retries=0, left=None, host=os.uname().nodename)
    out[0]["started"] = now
    save(job, rec)
    return rec


def cmd_step(job, n, expect=None, now=None):
    now = now or time.time()
    rec = load(job)
    if not rec:
        sys.exit("no plan for {}: run `eta.py plan {} \"Step:minutes\" ...` first".format(job, job))
    if not 1 <= n <= len(rec["steps"]):
        sys.exit("step {} is outside the plan's {} steps".format(n, len(rec["steps"])))
    cur = rec["steps"][rec["current"] - 1]
    if n != rec["current"] and not cur.get("ended"):
        cur["ended"] = now
        record_history(job, cur, now)
    for s in rec["steps"][:n - 1]:            # skipped steps count as done
        s.setdefault("ended", now)
    st = rec["steps"][n - 1]
    st["started"] = now
    st.pop("ended", None)
    if expect is not None:
        st["expect"] = expect
    rec.update(current=n, left=None)
    save(job, rec)
    return rec


def cmd_left(job, minutes, now=None):
    rec = load(job) or sys.exit("no plan for " + job)
    rec["left"] = dict(minutes=float(minutes), at=now or time.time())
    save(job, rec)
    return rec


def cmd_retry(job, why, now=None):
    now = now or time.time()
    rec = load(job) or sys.exit("no plan for " + job)
    st = rec["steps"][rec["current"] - 1]
    st["retries"] = st.get("retries", 0) + 1
    st["started"] = now
    rec["retries"] = rec.get("retries", 0) + 1
    rec["retry_note"] = why
    rec["left"] = None
    save(job, rec)
    return rec


def cmd_done(job, now=None):
    rec = load(job)
    if rec:
        now = now or time.time()
        cur = rec["steps"][rec["current"] - 1]
        if not cur.get("ended"):
            cur["ended"] = now
            record_history(job, cur, now)
        try:
            _path(job).unlink()
        except OSError:
            pass
    return rec


# ------------------------------------------------------------------ the estimate (pure, testable)
def step_expect(step, kind, hist_lines=None):
    """(minutes, source): history beats the session's guess once there are 2+ real runs of this step."""
    h = learned(step["name"], kind, hist_lines)
    if h is not None and step.get("expect"):
        return (0.5 * h + 0.5 * step["expect"]), "history"
    if h is not None:
        return h, "history"
    if step.get("expect"):
        return float(step["expect"]), "plan"
    return None, "none"


def estimate_job(rec, now, hist_lines=None, render=None):
    """Returns dict(low_min, high_min, mid_min, basis, step, of, step_name, retries, note)."""
    kind = rec["job"].split("-")[0]
    steps, n = rec["steps"], rec["current"]
    cur = steps[n - 1]
    el = (now - cur.get("started", now)) / 60.0
    exp, src = step_expect(cur, kind, hist_lines)
    unknown = 0
    basis = "estimate"
    left = rec.get("left")
    if left:
        since = (now - left["at"]) / 60.0
        cur_left = max(left["minutes"] - since, 0.15 * left["minutes"])
        basis = "measured"
    elif exp is None:
        cur_left, unknown = 30.0, 1                      # nothing known: say so with a wide range
    elif el < exp:
        cur_left = exp - el
    else:
        cur_left = max(0.35 * el, 0.25 * exp)            # running over: the overrun keeps the range honest
        basis = "running long"
    if render and render.get("waiting"):
        cur_left += render.get("wait_min", 0)
    rest = 0.0
    for s in steps[n:]:
        e, _ = step_expect(s, kind, hist_lines)
        if e is None:
            unknown += 1
            e = 20.0
        rest += e
    mid = cur_left + rest
    tail_share = rest / mid if mid else 0
    spread_hi = 1.25 + 0.5 * tail_share + 0.3 * unknown + 0.25 * min(rec.get("retries", 0), 3)
    spread_lo = 0.85 if basis == "measured" and tail_share < 0.2 else 0.7
    if basis == "measured" and tail_share < 0.2:
        spread_hi = min(spread_hi, 1.25)
    return dict(low_min=round(mid * spread_lo), high_min=round(mid * spread_hi), mid_min=round(mid),
                basis="rough" if unknown else basis, step=n, of=len(steps), step_name=cur["name"],
                retries=rec.get("retries", 0), retry_note=rec.get("retry_note", ""), elapsed_min=round(el))


# ------------------------------------------------------------------ gathering one Mac's view
def _json_cmd(argv, timeout=60):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


RQ_HISTORY = Path(os.environ.get("GATE_DIR") or "/tmp/absbyai-renderq") / "history.jsonl"


def render_medians():
    """{(project, pool): median seconds} from the render queue's own history; (None, pool) = any project."""
    try:
        lines = RQ_HISTORY.read_text().splitlines()[-3000:]
    except OSError:
        return {}
    by = {}
    for line in lines:
        try:
            h = json.loads(line)
        except ValueError:
            continue
        if h.get("dur", 0) <= 1:
            continue
        for key in ((h.get("project"), h.get("pool")), (None, h.get("pool"))):
            by.setdefault(key, []).append(h["dur"])
    return {k: statistics.median(v[-12:]) for k, v in by.items() if len(v) >= (1 if k[0] is None else 2)}


def local_view(now=None):
    """Everything this Mac knows, as plain JSON: progress estimates, edit slots, render activity."""
    now = now or time.time()
    cap = _json_cmd([sys.executable, str(EDITCAP), "status", "--json"]) or {}
    rq = _json_cmd([sys.executable, str(RENDERQ), "status", "--json"]) or {}
    try:
        hist = HISTORY.read_text().splitlines()[-2000:]
    except OSError:
        hist = []
    med = render_medians()
    render = {}
    for s in rq.get("slots", []):
        if s.get("held"):
            info = s.get("info", {})
            j = (info.get("project") or info.get("display_job") or info.get("group") or "").replace("work:", "")
            r = render.setdefault(j, dict(running=0, waiting=0, wait_min=0, label="", work_min=0.0))
            r["running"] += 1
            r["label"] = info.get("label", "")[:80]
            m = med.get((j, s.get("pool")), med.get((None, s.get("pool")), 300.0))
            el = now - info.get("start", now)
            r["work_min"] += max(m - el, 0.2 * m) / 60.0
    for w in rq.get("waiting", []):
        j = (w.get("project") or w.get("display_job") or w.get("group") or "").replace("work:", "")
        r = render.setdefault(j, dict(running=0, waiting=0, wait_min=0, label="", work_min=0.0))
        r["waiting"] += 1
        r["wait_min"] = max(r["wait_min"], round(w.get("eta_s", 0) / 60.0))
        r["work_min"] += med.get((j, w.get("pool")), med.get((None, w.get("pool")), 300.0)) / 60.0
    for r in render.values():
        r["work_min"] = round(r["work_min"] + (r["wait_min"] if not r["running"] else 0))
    jobs = {}
    for f in DIR.glob("*.json") if DIR.exists() else []:
        try:
            rec = json.loads(f.read_text())
        except ValueError:
            continue
        if not rec.get("steps"):
            continue
        jobs[rec["job"]] = dict(estimate_job(rec, now, hist, render.get(rec["job"])), updated=rec.get("updated"))
    edits = {}
    for code, e in (cap.get("edits") or {}).items():
        edits[code] = dict(state=e.get("state"), title=e.get("title", ""), ai=e.get("ai", ""),
                           last_seen=e.get("last_seen"), since=e.get("since"), reason=e.get("reason", ""))
    for code, a in (cap.get("renderq") or {}).items():
        if code in edits and a.get("last"):
            edits[code]["last_seen"] = max(edits[code].get("last_seen") or 0, a["last"])
    return dict(host=os.uname().nodename, now=now, progress=jobs, edits=edits, render=render,
                waiting_order=cap.get("waiting_order", []))


def remote_view(host):
    try:
        cfg = json.loads(HOSTS.read_text())["hosts"][host]
    except Exception:
        return None
    # Runs THIS Mac's copy of eta.py on the other Mac (sent over ssh), so the two never disagree on version.
    cmd = 'cd "{0}" && ETA_REPO="{0}" python3 - estimate --json'.format(cfg["repo"])
    try:
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes", cfg.get("ssh", host), cmd],
                           input=Path(__file__).read_text(), capture_output=True, text=True, timeout=90)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


# ------------------------------------------------------------------ combining into what the page shows
def clock(ts, to=1):
    """3:40 PM; to=5 rounds to the nearest 5 minutes (an ETA never pretends to the minute)."""
    if to > 1:
        ts = round(ts / (60 * to)) * 60 * to
    return datetime.datetime.fromtimestamp(ts).strftime("%-I:%M %p")


def _dayword(ts, now):
    d, today = datetime.date.fromtimestamp(ts), datetime.date.fromtimestamp(now or ts)
    if d == today:
        return ""
    if d - today == datetime.timedelta(1):
        return "tomorrow "
    return datetime.date.fromtimestamp(ts).strftime("%a ")


def when(ts, now=None):
    """'3:40 PM', 'tomorrow 9:15 AM', 'Fri 12:55 PM' (rounded to 5 minutes)."""
    return _dayword(ts, now) + clock(ts, 5)


def span(lo, hi, now=None):
    a, b = clock(lo, 5), clock(hi, 5)
    same_day = datetime.date.fromtimestamp(lo) == datetime.date.fromtimestamp(hi)
    if a == b and same_day:
        return when(lo, now)
    if same_day:
        if a[-2:] == b[-2:]:
            a = a[:-3]
        return _dayword(lo, now) + "{} to {}".format(a, b)
    return "{} to {}".format(when(lo, now), when(hi, now))


def _round(m):
    return int(round(m)) if m < 60 else int(5 * round(m / 5.0))


def describe(job, macs, now):
    """One page row for one job, from whichever Mac holds it."""
    for mac, v in macs.items():
        e = (v.get("edits") or {}).get(job)
        p = (v.get("progress") or {}).get(job)
        r = (v.get("render") or {}).get(job) or {}
        if not e and not p:
            continue
        if p and not e and not r and now - (p.get("updated") or 0) > ORPHAN_S:
            continue                     # edit finished (slot released) and nothing is rendering: old plan, not shown
        state = (e or {}).get("state")
        title = (e or {}).get("title", "")
        base = dict(job=job, mac=mac, title=title)
        if state == "with-dan":
            since = (e or {}).get("since")
            since_txt = " since " + _day(since, now) if since else ""
            return dict(base, kind="dan", text="Waiting on you" + since_txt, detail="your review or picks")
        if state == "waiting":
            pos = (v.get("waiting_order") or []).index(job) + 1 if job in (v.get("waiting_order") or []) else None
            return dict(base, kind="slot", text="Waiting for an edit slot" + (" (#{} in line)".format(pos) if pos else ""))
        last = max(x for x in [(e or {}).get("last_seen") or 0, (p or {}).get("updated") or 0] if x is not None)
        quiet = (now - last) / 60.0 if last else None
        if not r.get("running") and quiet is not None and quiet > STALL_MIN:
            return dict(base, kind="stuck", text="May be stuck: no activity for {}".format(_ago(quiet)),
                        detail=(p or {}).get("step_name", ""))
        if not p:
            work = r.get("work_min") or 0
            if work >= 1:
                # No plan from the session: the render steps it has queued give a floor, never the whole story.
                steps = r.get("running", 0) + r.get("waiting", 0)
                return dict(base, kind="floor", text="Not before about " + when(now + 60 * work, now),
                            detail="{} render step{} left in the queue, about {} of render time; the editor has not "
                                   "reported the rest of its plan".format(steps, "" if steps == 1 else "s", _dur(work)),
                            confidence="render queue only", low=round(now + 60 * work), high=round(now + 60 * work))
            return dict(base, kind="noplan", text="Working, no ETA reported yet",
                        detail="No render steps queued and no plan reported by the editor")
        lo, hi = now + 60 * p["low_min"], now + 60 * p["high_min"]
        rng = when(lo, now) if p["high_min"] - p["low_min"] < 6 else span(lo, hi, now)
        detail = "Step {} of {}: {}".format(p["step"], p["of"], p["step_name"])
        if p.get("retries"):
            detail += " · redoing after a failed check" + (" ({})".format(p["retry_note"]) if p.get("retry_note") else "")
        if r.get("waiting") and not r.get("running"):
            detail += " · waiting in the render line"
        label = {"measured": "measured", "running long": "running long", "rough": "rough guess"}.get(p["basis"], "estimate")
        return dict(base, kind="eta", text=rng, detail=detail, confidence=label,
                    low=round(lo), high=round(hi), minutes=[_round(p["low_min"]), _round(p["high_min"])])
    return None


def _day(ts, now):
    d = datetime.datetime.fromtimestamp(ts)
    if d.date() == datetime.date.fromtimestamp(now):
        return clock(ts)
    return d.strftime("%b %-d")


def _dur(m):
    m = int(round(m))
    return "{} min".format(m) if m < 60 else "{} h {:02d} min".format(m // 60, m % 60)


def _ago(m):
    return "{} min".format(int(m)) if m < 90 else "{:.1f} h".format(m / 60.0)


def combine(macs, now=None):
    now = now or time.time()
    names = []
    for v in macs.values():
        for j in list((v.get("edits") or {})) + list((v.get("progress") or {})):
            if j not in names:
                names.append(j)
    rows = [d for d in (describe(j, macs, now) for j in names) if d]
    order = {"eta": 0, "floor": 0, "stuck": 1, "noplan": 2, "slot": 3, "dan": 4}
    rows.sort(key=lambda d: (order.get(d["kind"], 9), d.get("high", 0)))
    return dict(schema=1, generated=round(now), checked=clock(now),
                macs={k: bool(v) for k, v in macs.items()}, jobs={d["job"]: d for d in rows}, order=[d["job"] for d in rows])


def gather():
    macs = {"m6": local_view()}
    macs["m2"] = remote_view("m2") or {}
    return macs


def refresh(force=False):
    data = combine(gather())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    body = {k: v for k, v in data.items() if k not in ("generated", "checked")}
    old = None
    try:
        old = json.loads(OUT.read_text())
    except (OSError, ValueError):
        pass
    same = old and {k: v for k, v in old.items() if k not in ("generated", "checked")} == body
    mark = OUT.with_suffix(".uploaded")          # last successful Drive upload
    fresh = mark.exists() and time.time() - mark.stat().st_mtime < PUSH_EVERY_S
    tmp = OUT.with_suffix(".tmp")                 # always refreshed locally: the edit desk reads it every minute
    tmp.write_text(json.dumps(data, ensure_ascii=False))
    os.replace(tmp, OUT)
    if same and fresh and not force:
        print("no change; not uploaded")
        return data
    if os.environ.get("ETA_NO_DRIVE"):
        return data
    try:
        r = subprocess.run([RCLONE, "copyto", str(OUT), DRIVE_PATH], capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            mark.touch()
        print("uploaded" if r.returncode == 0 else "upload FAILED: " + r.stderr[:200])
    except Exception as e:
        print("upload FAILED:", e)
    return data


def show(data):
    if not data["order"]:
        print("No edits running or waiting on either Mac.")
    for j in data["order"]:
        d = data["jobs"][j]
        line = "{} {} [{}]: {}".format(j, d.get("title", ""), d["mac"].upper(), d["text"])
        if d.get("detail"):
            line += ". " + d["detail"]
        if d.get("confidence"):
            line += " ({})".format(d["confidence"])
        print(line)
    print("Checked", data["checked"], "· Macs reached:", ", ".join(k for k, ok in data["macs"].items() if ok))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("job"); p.add_argument("steps", nargs="+")
    s = sub.add_parser("step"); s.add_argument("job"); s.add_argument("n", type=int); s.add_argument("--expect", type=float)
    l = sub.add_parser("left"); l.add_argument("job"); l.add_argument("minutes", type=float)
    r = sub.add_parser("retry"); r.add_argument("job"); r.add_argument("why", nargs="?", default="")
    d = sub.add_parser("done"); d.add_argument("job")
    e = sub.add_parser("estimate"); e.add_argument("--json", action="store_true")
    sub.add_parser("show")
    f = sub.add_parser("refresh"); f.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        rec = cmd_plan(a.job, a.steps)
        print("{}: plan saved, {} steps, step 1 ({}) started".format(a.job, len(rec["steps"]), rec["steps"][0]["name"]))
    elif a.cmd == "step":
        rec = cmd_step(a.job, a.n, a.expect)
        print("{}: step {} of {} ({}) started".format(a.job, a.n, len(rec["steps"]), rec["steps"][a.n - 1]["name"]))
    elif a.cmd == "left":
        cmd_left(a.job, a.minutes); print("{}: about {:g} min left in this step".format(a.job, a.minutes))
    elif a.cmd == "retry":
        cmd_retry(a.job, a.why); print("{}: step restarted (retry)".format(a.job))
    elif a.cmd == "done":
        cmd_done(a.job); print("{}: ETA cleared".format(a.job))
    elif a.cmd == "estimate":
        v = local_view()
        print(json.dumps(v) if a.json else json.dumps(v, indent=1))
    elif a.cmd == "show":
        show(combine(gather()))
    elif a.cmd == "refresh":
        show(refresh(a.force))


if __name__ == "__main__":
    main()
