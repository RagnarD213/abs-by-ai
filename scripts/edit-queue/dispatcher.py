#!/usr/bin/env python3
"""Overnight edit queue dispatcher. A plain script: it is not an AI and costs nothing to run.

launchd runs `dispatcher.py tick` every 15 minutes. Each tick it counts the build slots in use, parks
stale claims as `stalled`, checks every stop condition, and launches at most the free slots' worth of
jobs from Handoffs/video-editing/jobs.json through runner.py. Design: Handoffs/handoff-20260917-overnight-edit-queue.md §4.

  dispatcher.py tick              # what launchd runs
  dispatcher.py tick --dry-run    # print what it WOULD do; changes nothing, launches nothing
  dispatcher.py status            # the same facts, short
  dispatcher.py pause | resume    # Dan's off switch (the PAUSE file)
  dispatcher.py pause-group AV claude --reason "captions drift"   # circuit breaker
  dispatcher.py resume-group AV claude
  dispatcher.py launch-one AV-01  # fire one job by hand through the same checks (Phase 0 proof runs)
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eq_common as eq                                          # noqa: E402
eq.unshadow()
q = eq.sibling("queue")

BUILD_PS = re.compile(r"ffmpeg|whisper|render\.py|gate\.py|qc_style")     # 00-RULES.md §1.3
BUILD_PS_SKIP = re.compile(r"grep|Renderer")
MEDIA_EXT = (".mp4", ".mov", ".mxf", ".wav", ".m4a", ".png", ".jpg")


# ================================================================ facts (the only impure part)

def ps_table():
    out = subprocess.run(["ps", "-Ao", "pid=,ppid=,command="], capture_output=True, text=True).stdout
    rows = {}
    for line in out.splitlines():
        m = re.match(r"\s*(\d+)\s+(\d+)\s+(.*)", line)
        if m:
            rows[int(m.group(1))] = (int(m.group(2)), m.group(3))
    return rows


def foreign_builds(ps, claim_pids):
    """Builds that are NOT ours: Dan's own sessions and hand-fired jobs still count toward the two.
    A build process whose ancestor is a claimed runner is already counted by its claim. Foreign build
    processes are grouped by parent, so a decode|encode pipe counts once. Over-counting is the safe side."""
    parents = set()
    for pid, (ppid, cmd) in ps.items():
        if not BUILD_PS.search(cmd) or BUILD_PS_SKIP.search(cmd):
            continue
        p, ours, hops = pid, False, 0
        while p in ps and hops < 40:
            if p in claim_pids:
                ours = True
                break
            p, hops = ps[p][0], hops + 1
        if not ours:
            parents.add(ppid)
    return len(parents)


def hid_idle_seconds():
    try:
        out = subprocess.run(["ioreg", "-c", "IOHIDSystem"], capture_output=True, text=True, timeout=15).stdout
        m = re.search(r'"HIDIdleTime"\s*=\s*(\d+)', out)
        return int(m.group(1)) / 1e9 if m else 0.0      # unknown = assume Dan is here
    except Exception:
        return 0.0


def volume_free_gb(volume):
    if not os.path.ismount(volume):
        return None
    return shutil.disk_usage(volume).free / 1e9


def read(path):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return ""


def gather(cfg, data):
    claim_pids = {j["claim"]["pid"] for j in data["jobs"] if j.get("claim")}
    execs = sorted(set(v for k, v in cfg["routing"].items() if not k.startswith("_")))
    return {
        "now": datetime.datetime.now(),
        "pause_file": os.path.exists(eq.PAUSE_FILE),
        "free_gb": volume_free_gb(cfg["stop"]["volume"]),
        "idle_seconds": hid_idle_seconds(),
        "foreign_builds": foreign_builds(ps_table(), claim_pids),
        "auth": {e: eq.auth_ok(e, cfg) for e in execs},
        "pid_alive": q.pid_alive,
        "master": read(q.MASTER),
        "board": read(os.path.join(eq.ROOT, "AI_COORDINATION.md")),
        "work_dirs": {j["id"]: eq.existing_work_dirs(cfg, j["id"]) for j in data["jobs"]},
        "missing_sources": {j["id"]: missing_sources(j, cfg) for j in data["jobs"]
                            if j["state"] in cfg["unattended"]["launch_states"]},
    }


def missing_sources(job, cfg):
    """Source files a job doc names that are not on disk. Only paths we can resolve with confidence:
    absolute /Volumes or /Users paths, and repo-relative media paths whose first folder exists.
    Output names, placeholders (<slug>), the job's own work directory and anything from the doc's
    `## Deliver` section down (that is what the job will MAKE) are not sources."""
    doc = os.path.join(q.DIR, job.get("file", ""))
    if not job.get("file") or not os.path.exists(doc):
        return [f"job doc {job.get('file') or '(none)'}"]
    missing, own = [], eq.work_dir(cfg, job["id"]).lower()
    body = re.split(r"^## (?:Deliver|Starter prompts)", read(doc), flags=re.M)[0]
    for raw in re.findall(r"`([^`\n]+)`", body):
        p = raw.replace("\\|", "|").strip()
        if any(c in p for c in "<>*") or " → " in p or job["id"].lower() in p.lower():
            continue
        if p.startswith(("/Volumes/", "/Users/")):
            if p.rstrip("/").lower().startswith(own):
                continue
            full = p
        elif "/" in p and p.lower().endswith(MEDIA_EXT) and os.path.isdir(os.path.join(eq.ROOT, p.split("/")[0])):
            full = os.path.join(eq.ROOT, p)
        else:
            continue
        if not os.path.exists(full):
            missing.append(p)
    return missing


# ================================================================ decisions (pure; unit-tested)

def your_calls_jobs(master_text):
    """Job ids with an open row in 00-MASTER.md's 'Your calls' table."""
    m = re.search(r"^## Your calls.*?$(.*?)^(?:## |---)", master_text, re.S | re.M)
    ids = set()
    for line in (m.group(1) if m else "").splitlines():
        if line.startswith("|") and not line.startswith("|---") and not line.startswith("| job"):
            ids.update(re.findall(r"\b[A-Z]{2}-\d{2}\b", line.split("|")[1]))
    return ids


def board_active_jobs(board_text):
    m = re.search(r"^# ACTIVE\s*$(.*?)^# ", board_text, re.S | re.M)
    return set(re.findall(r"\b[A-Z]{2}-\d{2}\b", m.group(1) if m else ""))


def night_start(now, rollover_hour):
    d = now.replace(hour=rollover_hour, minute=0, second=0, microsecond=0)
    return d if now >= d else d - datetime.timedelta(days=1)


def ineligible_reason(job, cfg, facts, calls, active):
    un, jid = cfg["unattended"], job["id"]
    ex = eq.executor_for(jid, cfg)
    if job["state"] not in un["launch_states"]:
        return f"state is {job['state']}"
    if ex is None:
        return "group is not routed to the queue"
    if eq.group_of(jid) not in un["groups"]:
        return f"group {eq.group_of(jid)} is not in the unattended pilot yet"
    if job.get("size") not in un["sizes"]:
        return f"size {job.get('size')} is not in the unattended pilot yet"
    if job.get("unattended") is False:
        return "marked unattended:false (needs Dan, e.g. a fresh recording)"
    if job.get("claim"):
        return "already claimed"
    if jid in calls:
        return "open 'Your calls' row in 00-MASTER.md"
    if jid in active:
        return "named in AI_COORDINATION.md ACTIVE (another session owns it)"
    if job["state"] == "ready" and facts["work_dirs"].get(jid) and not job.get("queue_revision"):
        return f"work directory already exists ({facts['work_dirs'][jid][0]}): in flight or half-built, needs a look"
    why = eq.paused_reason(jid, ex, cfg)
    if why:
        return f"group paused for {ex}: {why}"
    miss = facts["missing_sources"].get(jid)
    if miss:
        return f"source not on disk: {miss[0]}"
    return None


def decide(data, cfg, facts, scoreboard):
    """Everything the tick will do, as data. No side effects."""
    now, jobs = facts["now"], data["jobs"]
    out = {"stalls": [], "stops": [], "executor_stops": {}, "launches": [], "skipped": {}, "slots": {}}

    # 1-2. slots by CLAIMS, not by processes; a stale claim becomes `stalled`, never a restart
    live = []
    for j in jobs:
        if not j.get("claim") or j["state"] == "stalled":
            continue
        if q.claim_is_live(j, now, cfg["claims"]["stale_minutes"], facts["pid_alive"]):
            live.append(j)
        else:
            out["stalls"].append((j["id"], f"no heartbeat since {j['claim'].get('heartbeat')} and pid "
                                           f"{j['claim'].get('pid')} is gone (claimed by {j['claim'].get('by')})"))
    dan_here = facts["idle_seconds"] < cfg["slots"]["dan_idle_minutes"] * 60
    auto_max = cfg["slots"]["when_dan_is_at_the_machine"] if dan_here else cfg["slots"]["max"]
    free = min(auto_max - len(live), cfg["slots"]["max"] - len(live) - facts["foreign_builds"])
    out["slots"] = {"live_claims": [j["id"] for j in live], "foreign_builds": facts["foreign_builds"],
                    "dan_at_machine": dan_here, "automated_max": auto_max, "free": max(free, 0)}

    # 3. stop conditions: any one of them and nothing launches
    if facts["pause_file"]:
        out["stops"].append("PAUSE file present (Dan's off switch)")
    if facts["free_gb"] is None:
        out["stops"].append(f"{cfg['stop']['volume']} is not mounted")
    elif facts["free_gb"] < cfg["stop"]["min_free_gb"]:
        out["stops"].append(f"{cfg['stop']['volume']} has {facts['free_gb']:.0f} GB free, under {cfg['stop']['min_free_gb']}")
    waiting = [j["id"] for j in jobs if j["state"] in cfg["stop"]["review_queue_states"]]
    if len(waiting) >= cfg["stop"]["review_queue_limit"]:
        out["stops"].append(f"Dan's review queue holds {len(waiting)} (limit {cfg['stop']['review_queue_limit']}): {waiting}")
    since = night_start(now, cfg["unattended"]["night_rolls_over_at_hour"])
    tonight = [r for r in scoreboard["runs"] if datetime.datetime.fromisoformat(r["started"]) >= since]
    cap_left = cfg["unattended"]["nightly_launch_cap"] - len(tonight)
    if cap_left <= 0:
        out["stops"].append(f"nightly launch cap reached ({len(tonight)} since {since:%a %H:%M})")
    if free <= 0:
        out["stops"].append(f"no free slot ({len(live)} queue job(s) + {facts['foreign_builds']} other build(s)"
                            f"{'; Dan is at the machine' if dan_here else ''})")

    # per-executor: signed out, or backing off after a usage limit (2 h, then one try)
    back = datetime.timedelta(hours=cfg["stop"]["usage_backoff_hours"])
    for ex, (ok, why) in facts["auth"].items():
        if not ok:
            out["executor_stops"][ex] = why
            continue
        runs = [r for r in scoreboard["runs"] if r["executor"] == ex and r.get("ended")]
        if runs and runs[-1]["outcome"] in ("usage_limited", "auth_failed"):
            until = datetime.datetime.fromisoformat(runs[-1]["ended"]) + back
            if now < until:
                out["executor_stops"][ex] = f"{ex}: {runs[-1]['outcome']} on its last launch; backing off until {until:%H:%M}"

    # 4. candidates, lowest `order` first, frames_approved before ready
    calls, active = your_calls_jobs(facts["master"]), board_active_jobs(facts["board"])
    rank = {s: i for i, s in enumerate(cfg["unattended"]["launch_states"])}
    cands = []
    # Finish an approved stage-one cut before any ready work; within ready, Dan's revision goes first.
    for j in sorted(jobs, key=lambda j: (rank.get(j["state"], 99),
                                         0 if j.get("queue_revision") else 1, j.get("order", 9999))):
        why = ineligible_reason(j, cfg, facts, calls, active)
        ex = eq.executor_for(j["id"], cfg)
        if not why and ex in out["executor_stops"]:
            why = out["executor_stops"][ex]
        if why:
            if j["state"] in rank:
                out["skipped"][j["id"]] = why
        else:
            cands.append((j, ex))
    out["eligible"] = [(j["id"], ex) for j, ex in cands]
    if out["stops"]:
        return out

    # prefer one of each executor: spreads the allowance, and one build's Python overlaps the other's encode
    busy = [j["claim"]["by"] for j in live]
    for _ in range(min(free, cap_left)):
        pick = next((c for c in cands if c[1] not in busy), None) or (cands[0] if cands else None)
        if not pick:
            break
        cands.remove(pick)
        busy.append(pick[1])
        out["launches"].append((pick[0]["id"], pick[1]))
    return out


# ================================================================ acting

def launch(job_id, executor, cfg, by_hand=False, no_budget=False):
    """Claim first, launch second, so two ticks can never take the same job."""
    runner = os.path.join(eq.HERE, "runner.py")
    with q.locked():
        data = q.load()
        ok, why = q.claim_job(data, job_id, executor, os.getpid(), states=tuple(cfg["unattended"]["launch_states"]))
        if not ok:
            return False, why
        job = q.find(data, job_id)
        launch_state = job["state"]
        prior = eq.scoreboard_latest(job_id) if launch_state == "frames_approved" else None
        reuse_row = bool(prior and prior.get("asset_flow", {}).get("stage_one_ended") and
                         not prior.get("asset_flow", {}).get("finishing_ended"))
        if reuse_row:
            row = prior
            flow = dict(row.get("asset_flow") or {})
            flow.update(finishing_started=q.now_iso(), launch_state="frames_approved")
            eq.scoreboard_update(row["run_id"], outcome="running", ended=None, asset_flow=flow)
        else:
            row = eq.new_run_row(job, executor, cfg)
        wd = eq.work_dir(cfg, job_id)
        os.makedirs(wd, exist_ok=True)
        budget_doc = eq.start_budget(job, cfg, wd, row["run_id"], no_budget=no_budget,
                                     preserve_renders=reuse_row)
        budget_row = eq.scoreboard_budget(budget_doc)
        if reuse_row:
            prior_budget = row.get("budget") or {}
            budget_row["hours_allowed"] += float(prior_budget.get("hours_allowed") or 0)
            budget_row["hours_used"] = float(prior_budget.get("hours_used") or 0)
            budget_row["review_hours_used"] = float(prior_budget.get("review_hours_used") or 0)
            eq.scoreboard_update(row["run_id"], budget=budget_row)
        else:
            row["by_hand"] = by_hand
            row["budget"] = budget_row
            eq.scoreboard_add(row)
        log = open(os.path.join(wd, "queue-runner.log"), "a")
        runner_cmd = ["/usr/bin/caffeinate", "-i", sys.executable, runner, job_id, executor,
                      row["run_id"], launch_state]
        if no_budget:
            runner_cmd.append("--no-budget")
            log.write(f"{q.now_iso()} launch-one --no-budget: per-size time and render caps lifted; "
                      f"{cfg['claims']['max_job_hours']} h outer ceiling remains\n")
            log.flush()
        proc = subprocess.Popen(runner_cmd,
                                stdin=subprocess.DEVNULL, stdout=log, stderr=log, cwd=eq.ROOT, start_new_session=True)
        job["claim"]["pid"] = proc.pid
        job["claim"]["launch_state"] = launch_state
        job["queue_owned"] = True
        q.set_state(data, job_id, "in_progress", f"edit queue ({executor})")
        q.save(data)
    q.master_status(job_id, q.STATES["in_progress"])
    q.push_drive(q.load())
    lifted = "; budget lifted by --no-budget" if no_budget else ""
    return True, f"launched {job_id} with {executor} (runner pid {proc.pid}){lifted}; log {wd}/queue-run.log"


def apply_stalls(stalls):
    for jid, why in stalls:
        subprocess.run([sys.executable, os.path.join(eq.HERE, "queue.py"), "stall", jid, "--note", "STALLED: " + why])
        row = eq.scoreboard_latest(jid)
        if row and row["outcome"] == "running":
            eq.scoreboard_update(row["run_id"], outcome="stalled", ended=q.now_iso())


def report(d, dry):
    s = d["slots"]
    lines = [f"[{datetime.datetime.now():%Y-%m-%d %H:%M}] edit-queue tick{' (DRY RUN: nothing is changed or launched)' if dry else ''}",
             f"  slots: {len(s['live_claims'])} queue job(s) {s['live_claims']}, {s['foreign_builds']} other build(s), "
             f"Dan at machine: {s['dan_at_machine']}, free: {s['free']}"]
    for jid in s["live_claims"]:
        try:
            budget = eq.load_budget(eq.work_dir(eq.load_config(), jid))
            started = datetime.datetime.fromisoformat(budget["started"])
            now = datetime.datetime.now(started.tzinfo) if started.tzinfo else datetime.datetime.now()
            used = max(0.0, (now - started).total_seconds() / 3600)
            if budget.get("enabled", True):
                lines.append(f"  budget: {jid}  {used:.1f}/{budget['hours_allowed']:g} h · "
                             f"{budget['renders_used']}/{budget['max_full_renders']} renders")
            else:
                lines.append(f"  budget: {jid}  lifted · {budget['renders_used']} full renders")
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            lines.append(f"  budget: {jid}  unavailable")
    lines += [f"  STALE -> stalled: {j}: {w}" for j, w in d["stalls"]]
    lines += [f"  STOP: {x}" for x in d["stops"]]
    lines += [f"  EXECUTOR OFF: {w}" for w in d["executor_stops"].values()]
    lines += [f"  eligible: {d.get('eligible', [])}"]
    lines += [f"  {'WOULD LAUNCH' if dry else 'LAUNCH'}: {j} -> {ex}" for j, ex in d["launches"]]
    if not d["launches"]:
        lines.append("  launching nothing")
    return "\n".join(lines)


def tick(dry_run=False, verbose=False):
    cfg, data = eq.load_config(), q.load()
    d = decide(data, cfg, gather(cfg, data), eq.scoreboard_load())
    print(report(d, dry_run))
    if verbose:
        for j, w in d["skipped"].items():
            print(f"    skip {j}: {w}")
    if dry_run:
        return d
    apply_stalls(d["stalls"])
    for jid, ex in d["launches"]:
        print("  ", launch(jid, ex, cfg)[1])
    try:
        eq.sibling("review_page").build()
    except Exception as e:      # the page never blocks the queue
        print(f"  review page not rebuilt: {e}")
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tick"); t.add_argument("--dry-run", action="store_true"); t.add_argument("-v", "--verbose", action="store_true")
    sub.add_parser("status"); sub.add_parser("pause"); sub.add_parser("resume")
    pg = sub.add_parser("pause-group"); pg.add_argument("group"); pg.add_argument("executor"); pg.add_argument("--reason", required=True)
    rg = sub.add_parser("resume-group"); rg.add_argument("group"); rg.add_argument("executor")
    lo = sub.add_parser("launch-one"); lo.add_argument("id"); lo.add_argument("--executor")
    lo.add_argument("--ignore-pilot-limits", action="store_true", help="allow a group/size outside the pilot (Phase 0 proof runs)")
    lo.add_argument("--no-budget", action="store_true", help="lift the per-size clock and render cap; the absolute outer ceiling remains")
    a = ap.parse_args()

    if a.cmd == "tick":
        tick(a.dry_run, a.verbose)
    elif a.cmd == "status":
        tick(dry_run=True, verbose=True)
    elif a.cmd == "pause":
        open(eq.PAUSE_FILE, "w").write(f"paused {q.now_iso()}\nDelete this file (or run: dispatcher.py resume) to let the queue launch jobs again.\n")
        print("PAUSED. Running jobs finish; nothing new launches.")
    elif a.cmd == "resume":
        if os.path.exists(eq.PAUSE_FILE):
            os.remove(eq.PAUSE_FILE)
        print("RESUMED. The next 15-minute tick may launch jobs.")
    elif a.cmd == "pause-group":
        cfg = eq.load_config()
        cfg["paused_groups"].append({"group": a.group.upper(), "executor": a.executor, "reason": a.reason, "date": datetime.date.today().isoformat()})
        eq.save_config(cfg)
        print(f"{a.group.upper()} paused for {a.executor}: {a.reason}")
    elif a.cmd == "resume-group":
        cfg = eq.load_config()
        cfg["paused_groups"] = [p for p in cfg["paused_groups"] if not (p["group"] == a.group.upper() and p["executor"] == a.executor)]
        eq.save_config(cfg)
        print(f"{a.group.upper()} resumed for {a.executor}")
    elif a.cmd == "launch-one":
        cfg, data = eq.load_config(), q.load()
        if a.ignore_pilot_limits:
            cfg["unattended"]["groups"].append(eq.group_of(a.id)); cfg["unattended"]["sizes"] += ["S", "M", "L"]
        if a.executor:
            cfg["routing"][eq.group_of(a.id)] = a.executor
        facts = gather(cfg, data)
        d = decide(data, cfg, facts, eq.scoreboard_load())
        stops = [s for s in d["stops"] if not s.startswith(("PAUSE", "nightly"))]   # by hand: Dan's pause and the cap don't apply
        why = d["skipped"].get(a.id) or (stops[0] if stops else None)
        if why or (a.id, eq.executor_for(a.id, cfg)) not in d.get("eligible", []):
            sys.exit(f"NOT launching {a.id}: {why or 'not eligible'}")
        print(launch(a.id, eq.executor_for(a.id, cfg), cfg, by_hand=True, no_budget=a.no_budget)[1])


if __name__ == "__main__":
    main()
