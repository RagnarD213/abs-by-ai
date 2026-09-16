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

States: ready, needs, blocked, in_progress, delivered, finalized, uploaded.
"""
import argparse, datetime, json, os, re, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DIR = os.path.join(ROOT, "Handoffs", "video-editing")
JOBS = os.path.join(DIR, "jobs.json")
MASTER = os.path.join(DIR, "00-MASTER.md")
EXPORT = os.path.join(ROOT, "tmp", "edit-queue-export")  # git-ignored; Artifact file_path must sit under the repo
STATES = {
    "ready": "READY", "needs": "**NEEDS DAN**", "blocked": "BLOCKED",
    "in_progress": "IN PROGRESS", "delivered": "DELIVERED — awaiting Dan",
    "finalized": "FINALIZED", "uploaded": "UPLOADED",
}
RCLONE = os.path.expanduser("~/bin/rclone")
DRIVE_PATH = "gdrive:Abs By AI automation/edit-queue-status.json"   # Drive file id 1RX-GqepEKqB1LgJqJFRyRU2lOJMnRFgg
DB_FIELDS = ("id", "list", "group", "sub", "title", "roll", "size", "file", "claudeModel", "claude",
             "codexModel", "codex", "state", "note", "order", "updated", "by", "rev")


def load():
    with open(JOBS) as f:
        return json.load(f)


def save(data):
    with open(JOBS, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")


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
        json.dump({"schema": 1, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
                   "jobs": [{k: j.get(k, "") for k in DB_FIELDS} for j in data["jobs"]]}, f, ensure_ascii=False)
    import subprocess
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
    args = ap.parse_args()
    data = load()

    if args.cmd == "set":
        j = find(data, args.id)
        j["state"] = args.state
        if args.note is not None:
            j["note"] = args.note
        j["updated"] = datetime.date.today().isoformat()
        j["by"] = args.by
        j["rev"] = j.get("rev", 0) + 1
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
    elif args.cmd == "show":
        print(json.dumps(find(data, args.id), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
