#!/usr/bin/env python3
"""Status helper for the video edit queue (Handoffs/video-editing/).

jobs.json is the source of truth. Every `set`/`add` also uploads the status file to Dan's
Google Drive ("Abs By AI automation/edit-queue-status.json", read live by the Abs By AI
Edit Queue page), so Claude, Codex and Grok Bot all update the page the same way. Claude
sessions additionally mirror changes into the artifact's `jobs` db (`Artifact write_db`),
the page's fallback when a viewer's Drive connector isn't available.

  queue.py set RA-01 finalized --by "Claude" [--note "Dan finalized 09-18"]
  queue.py add new-job.json              # one job object, or a list of them
  queue.py pending                       # jobs changed since the last artifact sync
  queue.py export [ID ...]               # write db-ready JSON files, print write_db entries
  queue.py mark-synced ID [ID ...]       # after write_db succeeded
  queue.py push                          # re-upload the Drive status file
  queue.py show ID

Overnight-queue commands (scripts/edit-queue/README.md). A claim is what holds one of the two build slots:
  queue.py claim AV-01 --by codex --pid 1234   # atomic; refuses a job with a live claim or a non-launchable state
  queue.py heartbeat AV-01                     # the runner touches this every few minutes (no Drive push, no rev bump)
  queue.py release AV-01                       # drop the claim, leave the state alone
  queue.py stall AV-01 --note "why"            # state -> stalled, claim kept for the record; never auto-restarted

States: ready, draft_review, frames_approved, needs, blocked, in_progress, delivered,
finalized, uploaded, stalled.
"""
import argparse, contextlib, datetime, fcntl, json, os, re, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DIR = os.environ.get("EDIT_QUEUE_DIR") or os.path.join(ROOT, "Handoffs", "video-editing")  # env override: tests only
JOBS = os.path.join(DIR, "jobs.json")
MASTER = os.path.join(DIR, "00-MASTER.md")
EXPORT = os.path.join(ROOT, "tmp", "edit-queue-export")  # git-ignored; Artifact file_path must sit under the repo
STATES = {
    "ready": "READY", "needs": "**NEEDS DAN**", "blocked": "BLOCKED",
    "draft_review": "DRAFT — asset choices waiting for Dan",
    "frames_approved": "ASSETS APPROVED — finishing queued",
    "in_progress": "IN PROGRESS", "delivered": "DELIVERED — awaiting Dan",
    "finalized": "FINALIZED", "uploaded": "UPLOADED",
    "stalled": "**STALLED — needs a look**",
}
LAUNCHABLE = ("frames_approved", "ready")   # frames_approved arrives with Phase 2; it goes first
LOCK = os.path.join(DIR, ".jobs.lock")
RCLONE = os.path.expanduser("~/bin/rclone")
DRIVE_PATH = "gdrive:Abs By AI automation/edit-queue-status.json"   # Drive file id 1RX-GqepEKqB1LgJqJFRyRU2lOJMnRFgg
DB_FIELDS = ("id", "list", "group", "sub", "title", "roll", "size", "file", "claudeModel", "claude",
             "codexModel", "codex", "state", "note", "order", "updated", "by", "rev")


def load():
    with open(JOBS) as f:
        return json.load(f)


def save(data):
    tmp = JOBS + ".tmp"          # atomic: a reader never sees a half-written list
    with open(tmp, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, JOBS)


@contextlib.contextmanager
def locked():
    """One writer at a time: the dispatcher, a runner's heartbeat and an editing session all write jobs.json."""
    with open(LOCK, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def now_iso():
    return datetime.datetime.now().isoformat(timespec="seconds")


def pid_alive(pid):
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError, TypeError):
        return False
    return True


def claim_is_live(job, now=None, stale_minutes=45, alive=pid_alive):
    """A claim holds a slot until it is released. It only goes STALE when the heartbeat is older than
    `stale_minutes` AND the pid is gone: a session that is thinking for an hour is still a live build."""
    c = job.get("claim")
    if not c:
        return False
    now = now or datetime.datetime.now()
    beat = datetime.datetime.fromisoformat(c.get("heartbeat") or c["started"])
    return alive(c.get("pid")) or (now - beat) < datetime.timedelta(minutes=stale_minutes)


def claim_job(data, jid, by, pid, states=LAUNCHABLE):
    """Claim first, launch second. Returns (ok, reason). Caller holds `locked()` and saves."""
    j = find(data, jid)
    if j.get("claim"):
        return False, f"{jid} already has a claim by {j['claim'].get('by')} (pid {j['claim'].get('pid')})"
    if j["state"] not in states:
        return False, f"{jid} is {j['state']}, not one of {list(states)}"
    t = now_iso()
    j["claim"] = {"by": by, "pid": int(pid), "started": t, "heartbeat": t}
    return True, "claimed"


def find(data, jid):
    for j in data["jobs"]:
        if j["id"] == jid:
            return j
    sys.exit(f"unknown job id {jid} (see {JOBS})")


def master_status(jid, label):
    """Rewrite the status cell (second-to-last) of the job's row in 00-MASTER.md."""
    if not os.path.exists(MASTER):
        return False
    lines = open(MASTER).read().split("\n")
    pat = re.compile(r"^\| \[" + re.escape(jid) + r"\]\(")
    for i, line in enumerate(lines):
        if pat.match(line):
            cells = line.split("|")  # ['', ' [ID](f) ', ..., ' status ', ' size ', '']
            cells[-3] = f" {label} "
            lines[i] = "|".join(cells)
            open(MASTER, "w").write("\n".join(lines))
            return True
    return False


def push_drive(data):
    """Upload the page's status file to Drive. Best-effort: a failure never blocks the repo update."""
    os.makedirs(EXPORT, exist_ok=True)
    path = os.path.join(EXPORT, "edit-queue-status.json")
    with open(path, "w") as f:
        json.dump({"schema": 2, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
                   "stateLabels": STATES, "assetApprovalSchema": 1,
                   "jobs": [{k: j.get(k, "") for k in DB_FIELDS} for j in data["jobs"]]}, f, ensure_ascii=False)
    import subprocess
    if os.environ.get("EDIT_QUEUE_NO_DRIVE"):   # tests
        return True
    try:
        r = subprocess.run([RCLONE, "copyto", path, DRIVE_PATH], capture_output=True, text=True, timeout=120)
        ok = r.returncode == 0
    except Exception as e:  # rclone missing, timeout
        ok, r = False, e
    print("Drive status file (page updates on next open/refresh):", "uploaded" if ok else f"FAILED ({getattr(r, 'stderr', r)!s:.200}); run `queue.py push` later")
    return ok


def export(jobs):
    os.makedirs(EXPORT, exist_ok=True)
    entries = []
    for j in jobs:
        path = os.path.join(EXPORT, j["id"] + ".json")
        with open(path, "w") as f:
            json.dump({k: j.get(k, "") for k in DB_FIELDS}, f, ensure_ascii=False)
        entries.append({"op": "set", "collection": "jobs", "doc_id": j["id"], "file_path": path})
    return entries


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("set"); s.add_argument("id"); s.add_argument("state", choices=STATES)
    s.add_argument("--note"); s.add_argument("--by", default="")
    a = sub.add_parser("add"); a.add_argument("json_file")
    sub.add_parser("pending")
    e = sub.add_parser("export"); e.add_argument("ids", nargs="*")
    m = sub.add_parser("mark-synced"); m.add_argument("ids", nargs="+")
    sh = sub.add_parser("show"); sh.add_argument("id")
    sub.add_parser("push")
    c = sub.add_parser("claim"); c.add_argument("id"); c.add_argument("--by", required=True)
    c.add_argument("--pid", type=int, required=True)
    sub.add_parser("heartbeat").add_argument("id")
    sub.add_parser("release").add_argument("id")
    st = sub.add_parser("stall"); st.add_argument("id"); st.add_argument("--note", default="")
    args = ap.parse_args()
    if args.cmd in ("show", "pending", "export", "push"):
        return run(args)
    with locked():
        return run(args)


def set_state(data, jid, state, by="", note=None):
    j = find(data, jid)
    j["state"] = state
    if note is not None:
        j["note"] = note
    j["updated"] = datetime.date.today().isoformat()
    j["by"] = by
    j["rev"] = j.get("rev", 0) + 1
    return j


def run(args):
    data = load()

    if args.cmd == "set":
        j = set_state(data, args.id, args.state, args.by, args.note)
        save(data)
        row = master_status(args.id, STATES[args.state])
        print(f"{args.id} -> {args.state} (rev {j['rev']}); 00-MASTER.md row {'updated' if row else 'NOT FOUND'}")
        push_drive(data)
        print("Claude sessions also mirror it to the artifact db (write_db set):")
        print(json.dumps(export([j])[0]))
    elif args.cmd == "add":
        new = json.load(open(args.json_file))
        new = new if isinstance(new, list) else [new]
        top = max(j.get("order", 0) for j in data["jobs"])
        for n in new:
            if any(j["id"] == n["id"] for j in data["jobs"]):
                sys.exit(f"{n['id']} already exists")
            top += 1
            n.setdefault("order", top); n.setdefault("state", "ready"); n.setdefault("note", "")
            n.setdefault("sub", ""); n["updated"] = datetime.date.today().isoformat()
            n["rev"] = 1; n["syncedRev"] = 0
            data["jobs"].append(n)
        save(data)
        push_drive(data)
        print(f"added {[n['id'] for n in new]}; also add their rows to 00-MASTER.md. Claude sessions mirror to the artifact db:")
        print(json.dumps(export(new)))
    elif args.cmd == "pending":
        p = [j for j in data["jobs"] if j.get("rev", 0) > j.get("syncedRev", 0)]
        print(json.dumps(export(p)) if p else "[]")
        print(f"{len(p)} job(s) to sync: {[j['id'] for j in p]}", file=sys.stderr)
    elif args.cmd == "export":
        js = [find(data, i) for i in args.ids] if args.ids else data["jobs"]
        print(json.dumps(export(js)))
    elif args.cmd == "mark-synced":
        for i in args.ids:
            j = find(data, i); j["syncedRev"] = j.get("rev", 0)
        save(data)
        print("synced:", args.ids)
    elif args.cmd == "push":
        push_drive(data)
    elif args.cmd == "claim":
        ok, why = claim_job(data, args.id, args.by, args.pid)
        if ok:
            save(data)
        print(why)
        sys.exit(0 if ok else 3)
    elif args.cmd == "heartbeat":
        j = find(data, args.id)
        if not j.get("claim"):
            sys.exit(f"{args.id} has no claim")
        j["claim"]["heartbeat"] = now_iso()
        save(data)
    elif args.cmd == "release":
        find(data, args.id).pop("claim", None)
        save(data)
        print(f"{args.id}: claim released")
    elif args.cmd == "stall":
        j = set_state(data, args.id, "stalled", "edit-queue dispatcher", args.note or None)
        save(data)
        master_status(args.id, STATES["stalled"])
        push_drive(data)
        print(f"{args.id} -> stalled. Never auto-restarted: look at its work directory first, then `queue.py release` + `set ... ready`.")
    elif args.cmd == "show":
        print(json.dumps(find(data, args.id), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
