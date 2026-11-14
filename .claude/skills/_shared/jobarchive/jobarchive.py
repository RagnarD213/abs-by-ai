#!/usr/bin/env python3
"""Nightly cleanup of finished edit folders (Dan, 2026-11-14).

Moves edit work folders that nobody is using off this Mac's internal drive and the Extreme onto the Seagate
(Expansion), so both Macs always have room to edit on fast drives. A folder is removed ONLY after every file has
been copied and re-read from the Seagate with a matching SHA-256 (reads bypass the disk cache, because the Seagate
silently corrupted copies on 2026-11-01 to 11-03). Rule: AGENTS.md, "Where work happens"; VIDEO-RULES.md.

    jobarchive.py scan [--json]           dry run: what would move tonight, and why each other folder stays
    jobarchive.py run [--limit N] [--until HH]
                                          archive eligible folders (stops starting new ones after HH, default 8)
    jobarchive.py restore JOB [--to DIR]  copy an archived job back (default: its original folder)
    jobarchive.py list                    archived jobs
    jobarchive.py install [--hour H]      LaunchAgent on this Mac (default 2 AM nightly), plus a private copy of
                                          this script in ~/.absbyai-jobarchive so a git checkout never breaks it
    jobarchive.py selftest

A folder stays when ANY of these holds:
  * something changed in it in the last IDLE_DAYS (14) days
  * it is an edit the edit cap (editcap) lists as active, starting or waiting for a slot
  * it is with Dan for review (edit cap "with-dan"/"stalled", or a board line naming it with REVIEW, AWAITING,
    BUILDING, NEEDS DAN or PICK), unless untouched for STALE_DAYS (30) days
  * the render queue has a live step for it, or a running process has it open or in its command line
  * its name is in keep.txt beside this script or in ~/.absbyai-jobarchive/keep.txt (one name per line)

Where they go: /Volumes/Expansion/_finished_edit_jobs/<mac>-<drive>/<JOB>/. The Seagate is plugged into the M2;
the M6 sends its folders over the Thunderbolt cable (ssh m2). Symlinks are not copied (exFAT cannot hold them):
each job's manifest records them. Every move appends one line to _finished_edit_jobs/index.jsonl.
"""
import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
import plistlib
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HOME = Path.home()
STATE = Path(os.environ.get("JOBARCHIVE_STATE") or HOME / ".absbyai-jobarchive")
IDLE_DAYS = float(os.environ.get("JOBARCHIVE_IDLE_DAYS") or 14)
STALE_DAYS = float(os.environ.get("JOBARCHIVE_STALE_DAYS") or 30)
SEAGATE = Path(os.environ.get("JOBARCHIVE_SEAGATE") or "/Volumes/Expansion")
ARCHIVE_DIR = "_finished_edit_jobs"
REMOTE = os.environ.get("JOBARCHIVE_REMOTE", "m2")          # the Mac the Seagate is plugged into
LOW_FREE_GB = 150
LABEL = "com.absbyai.jobarchive"
F_NOCACHE = 48
BOARD_WORDS = re.compile(r"REVIEW|AWAITING|BUILDING|NEEDS DAN|PICK", re.I)
DEFAULT_ROOTS = [("internal", HOME / "Projects" / "_edit_work"), ("internal", HOME / "_edit_work"),
                 ("Extreme", Path("/Volumes/Extreme/_edit_work"))]

HASHER = r'''
import fcntl, hashlib, json, os, sys
root = sys.argv[1]
out = {}
for d, dirs, files in os.walk(root):
    for f in files:
        p = os.path.join(d, f)
        rel = os.path.relpath(p, root)
        if rel == ".jobarchive-manifest.json" or os.path.islink(p) or not os.path.isfile(p):
            continue
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            try:
                fcntl.fcntl(fh.fileno(), 48, 1)
            except OSError:
                pass
            for b in iter(lambda: fh.read(4 << 20), b""):
                h.update(b)
        out[rel] = [os.path.getsize(p), h.hexdigest()]
print(json.dumps(out))
'''


def log(msg):
    line = "{} {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        with open(STATE / "jobarchive.log", "a") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def host():
    n = socket.gethostname().lower()
    if os.environ.get("JOBARCHIVE_HOST"):
        return os.environ["JOBARCHIVE_HOST"]
    return "m2" if ("m2" in n or "mac-mini" in n) else "m6"


def on_local_disk(path):
    """False for a drive shared over the network (the M6 mounts the M2's Extreme and Seagate over SMB):
    only the Mac the drive is plugged into cleans it up."""
    try:
        out = subprocess.run(["mount"], capture_output=True, text=True, timeout=20).stdout
    except (OSError, subprocess.TimeoutExpired):
        return True
    best, kind = "", ""
    target = os.path.realpath(str(path))
    for line in out.splitlines():
        m = re.match(r".+ on (.+) \((\w+)", line)
        if m and (target == m.group(1) or target.startswith(m.group(1).rstrip("/") + "/")) \
                and len(m.group(1)) > len(best):
            best, kind = m.group(1), m.group(2)
    return kind not in ("smbfs", "nfs", "afpfs", "webdav", "macfuse", "osxfuse")


def roots():
    env = os.environ.get("JOBARCHIVE_ROOTS")       # "label=/path;label=/path" for tests
    pairs = [tuple(x.split("=", 1)) for x in env.split(";")] if env else DEFAULT_ROOTS
    seen, out = set(), []
    for label, p in pairs:
        p = Path(p)
        if p.is_dir() and not p.is_symlink() and on_local_disk(p):
            r = p.resolve()
            if r not in seen:
                seen.add(r)
                out.append((label, p))
    return out


def repo():
    if os.environ.get("JOBARCHIVE_REPO"):
        return Path(os.environ["JOBARCHIVE_REPO"])
    try:
        return Path(json.loads((STATE / "config.json").read_text())["repo"])
    except (OSError, ValueError, KeyError):
        return Path(__file__).resolve().parents[4]


def tree_stats(folder):
    """(newest mtime of anything in the tree, total bytes of regular files, symlinks list)."""
    newest, total, links = os.lstat(folder).st_mtime, 0, []
    for d, dirs, files in os.walk(folder):
        for name in dirs + files:
            p = os.path.join(d, name)
            try:
                st = os.lstat(p)
            except OSError:
                continue
            newest = max(newest, st.st_mtime)
            if os.path.islink(p):
                links.append([os.path.relpath(p, folder), os.readlink(p)])
            elif name in files:
                total += st.st_size
    return newest, total, links


def norm(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def editcap_states():
    if os.environ.get("JOBARCHIVE_EDITCAP_JSON"):
        data = json.loads(os.environ["JOBARCHIVE_EDITCAP_JSON"])
    else:
        script = repo() / ".claude/skills/_shared/editcap/editcap.py"
        try:
            out = subprocess.run([sys.executable, str(script), "status", "--json"], capture_output=True,
                                 text=True, timeout=60).stdout
            data = json.loads(out)
        except (OSError, ValueError, subprocess.TimeoutExpired):
            return None                                       # unknown: callers keep everything recent
    states = {norm(j): e.get("state", "") for j, e in (data.get("edits") or {}).items()}
    live = {norm(j) for j, r in (data.get("renderq") or {}).items() if r.get("live")}
    return states, live


def board_review_names():
    try:
        text = (repo() / "AI_COORDINATION.md").read_text(errors="replace")
    except OSError:
        return ""
    return "\n".join(line for line in text.splitlines() if BOARD_WORDS.search(line))


def on_board(name, board_text):
    if len(norm(name)) < 3:
        return False
    pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(name).replace(r"\-", "[-_ ]?") + r"(?![A-Za-z0-9])", re.I)
    return bool(pat.search(board_text))


def busy_paths():
    """Command lines and working folders of running processes (one blob to search)."""
    if os.environ.get("JOBARCHIVE_BUSY") is not None:
        return os.environ["JOBARCHIVE_BUSY"]
    parts = []
    for cmd in (["ps", "-axww", "-o", "args="], ["lsof", "-n", "-d", "cwd", "-Fn"]):
        try:
            parts.append(subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout)
        except (OSError, subprocess.TimeoutExpired):
            pass
    return "\n".join(parts)


REF_RE = re.compile(r"_edit_work/([A-Za-z0-9._-]+)")
REF_EXT = (".py", ".sh", ".js", ".mjs", ".json", ".md", ".txt", ".yaml", ".yml", ".html")


def referenced_names():
    """Folder names that skills, scripts and the standing rules point at (approved masters, locked recipes,
    shared tools such as _edit_work/bin, clip-library catalog entries). Moving one would break a tool or a standard, so they stay."""
    base = repo()
    names = set()
    places = [base / ".claude" / "skills", base / "scripts", base / "Media" / "clip-library",
              base / "Media" / "footage-index"]
    files = [base / "AGENTS.md", base / "CLAUDE.md"]
    for place in places:
        for d, dirs, fs in os.walk(str(place)):
            dirs[:] = [x for x in dirs if x not in ("node_modules", ".git", "__pycache__")]
            files.extend(Path(d) / f for f in fs if f.endswith(REF_EXT))
    for f in files:
        try:
            if f.stat().st_size > 60_000_000:
                continue
            names |= {norm(m) for m in REF_RE.findall(f.read_text(errors="ignore"))}
        except OSError:
            pass
    return names


def keep_names():
    names = set()
    for p in (Path(__file__).resolve().parent / "keep.txt", STATE / "keep.txt"):
        try:
            names |= {norm(x) for x in p.read_text().splitlines() if x.strip() and not x.startswith("#")}
        except OSError:
            pass
    return names


def decide(now=None):
    now = now or time.time()
    ec = editcap_states()
    board = board_review_names()
    busy = busy_paths()
    keep = keep_names()
    refs = referenced_names()
    rows = []
    for label, root in roots():
        for entry in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if not entry.is_dir() or entry.is_symlink() or entry.name.startswith((".", "_")):
                continue
            newest, size, links = tree_stats(entry)
            idle = (now - newest) / 86400
            key = norm(entry.name)
            why = None
            if idle < IDLE_DAYS:
                why = "changed {:.1f} days ago".format(idle)
            elif key in keep:
                why = "on the keep list"
            elif key in refs:
                why = "a skill, script or standing rule points at it"
            elif ec is None:
                why = "edit cap unreadable; keeping everything tonight"
            elif ec[0].get(key) in ("active", "promoted", "waiting", "new"):
                why = "edit cap lists it as {}".format(ec[0][key])
            elif key in ec[1]:
                why = "render queue step is live"
            elif str(entry) in busy or str(entry.resolve()) in busy:
                why = "a running process uses it"
            elif idle < STALE_DAYS and ec[0].get(key) in ("with-dan", "stalled"):
                why = "with Dan for review (edit cap)"
            elif idle < STALE_DAYS and on_board(entry.name, board):
                why = "with Dan for review (board)"
            rows.append({"job": entry.name, "path": str(entry), "drive": label, "idle_days": round(idle, 1),
                         "gb": round(size / 1e9, 2), "links": links, "move": why is None, "why": why or ""})
    return rows


def seagate_local():
    return (SEAGATE / ".").exists() and os.path.ismount(str(SEAGATE)) and on_local_disk(SEAGATE)


def ssh(args, **kw):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", REMOTE] + args, **kw)


def hash_tree(folder, remote=False):
    if remote:
        r = ssh(["/usr/bin/python3", "-", folder], input=HASHER, capture_output=True, text=True)
    else:
        r = subprocess.run([sys.executable, "-", folder], input=HASHER, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("hashing failed: " + (r.stderr or "")[-500:])
    return json.loads(r.stdout)


def write_remote_text(path, text, remote):
    if remote:
        r = ssh(["/usr/bin/python3", "-c",
                 "import sys;open(sys.argv[1],'w').write(sys.stdin.read())", path],
                input=text, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(r.stderr[-300:])
    else:
        with open(path, "w") as fh:
            fh.write(text)


def append_index(base, record, remote):
    line = json.dumps(record) + "\n"
    path = base + "/index.jsonl"
    if remote:
        ssh(["/usr/bin/python3", "-c", "import sys;open(sys.argv[1],'a').write(sys.stdin.read())", path],
            input=line, capture_output=True, text=True)
    else:
        with open(path, "a") as fh:
            fh.write(line)


def archive_one(row, base, remote):
    src = Path(row["path"])
    dest = "{}/{}-{}/{}".format(base, host(), row["drive"], src.name)
    before = tree_stats(src)[0]
    log("{}: copying {:.1f} GB from {} to the Seagate".format(src.name, row["gb"], row["drive"]))
    src_hash = hash_tree(str(src))
    if remote:
        ssh(["mkdir", "-p", dest], check=True, capture_output=True)
        target = "{}:{}/".format(REMOTE, dest)
        cmd = ["rsync", "-rt", "-e", "ssh -o BatchMode=yes", str(src) + "/", target]
    else:
        os.makedirs(dest, exist_ok=True)
        cmd = ["rsync", "-rt", str(src) + "/", dest + "/"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("copy failed: " + (r.stderr or "")[-500:])
    dst_hash = hash_tree(dest, remote)
    missing = sorted(set(src_hash) - set(dst_hash))
    bad = sorted(k for k in src_hash if k in dst_hash and dst_hash[k] != src_hash[k])
    if missing or bad:
        raise RuntimeError("verify failed: {} missing, {} mismatched (e.g. {}); source kept".format(
            len(missing), len(bad), (missing + bad)[:3]))
    if tree_stats(src)[0] != before:
        raise RuntimeError("folder changed during the copy; source kept, will retry another night")
    manifest = {"job": src.name, "from": str(src), "mac": host(), "drive": row["drive"],
                "archived": dt.datetime.now().isoformat(timespec="seconds"), "files": src_hash,
                "symlinks_not_copied": row["links"]}
    write_remote_text(dest + "/.jobarchive-manifest.json", json.dumps(manifest, indent=1), remote)
    shutil.rmtree(src)
    rec = {k: manifest[k] for k in ("job", "from", "mac", "drive", "archived")}
    rec.update(to=dest, files=len(src_hash), gb=row["gb"])
    append_index(base, rec, remote)
    log("{}: verified {} files on the Seagate, removed from {}".format(src.name, len(src_hash), row["drive"]))
    return dest


def free_gb(path):
    try:
        return shutil.disk_usage(str(path)).free / 1e9
    except OSError:
        return None


def warn_low_space():
    for label, p in (("internal drive", HOME), ("Extreme", Path("/Volumes/Extreme"))):
        f = free_gb(p) if p.exists() else None
        if f is not None and f < LOW_FREE_GB:
            msg = "{} on {} has only {:.0f} GB free".format(label, host().upper(), f)
            log("WARNING " + msg)
            if host() == "m6":
                subprocess.run(["osascript", "-e", 'display notification "{}" with title "Edit drive space"'
                                .format(msg)], capture_output=True)


def cmd_scan(args):
    rows = decide()
    if args.json:
        print(json.dumps(rows, indent=1))
        return 0
    move = [r for r in rows if r["move"]]
    for r in rows:
        print("{:5} {:8} {:7.1f} GB  idle {:6.1f} d  {}  {}".format(
            "MOVE" if r["move"] else "keep", r["drive"], r["gb"], r["idle_days"], r["job"], r["why"]))
    print("\n{} of {} folders would move ({:.0f} GB).".format(len(move), len(rows), sum(r["gb"] for r in move)))
    return 0


def cmd_run(args):
    STATE.mkdir(parents=True, exist_ok=True)
    lock = open(STATE / "run.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log("another cleanup is already running; exiting")
        return 0
    remote = not seagate_local()
    base = str(SEAGATE / ARCHIVE_DIR)
    if remote:
        if ssh(["test", "-d", str(SEAGATE)], capture_output=True).returncode:
            log("Seagate not reachable on {}; nothing moved".format(REMOTE))
            warn_low_space()
            return 1
        ssh(["mkdir", "-p", base], capture_output=True)
    else:
        os.makedirs(base, exist_ok=True)
    rows = [r for r in decide() if r["move"]]
    rows.sort(key=lambda r: -r["idle_days"])
    done = errors = 0
    for r in rows:
        if args.limit and done >= args.limit:
            break
        if args.until is not None and args.until <= dt.datetime.now().hour < args.until + 12:
            log("past {}:00; the rest wait for tomorrow night".format(args.until))
            break
        try:
            archive_one(r, base, remote)
            done += 1
        except (RuntimeError, OSError, subprocess.CalledProcessError) as ex:
            errors += 1
            log("ERROR {}: {}".format(r["job"], ex))
    log("done: {} moved, {} errors, {} left for later".format(done, errors, len(rows) - done - errors))
    warn_low_space()
    return 1 if errors else 0


def read_index():
    remote = not seagate_local()
    path = str(SEAGATE / ARCHIVE_DIR / "index.jsonl")
    if remote:
        r = ssh(["cat", path], capture_output=True, text=True)
        text = r.stdout if r.returncode == 0 else ""
    else:
        text = Path(path).read_text() if Path(path).exists() else ""
    return [json.loads(l) for l in text.splitlines() if l.strip()], remote


def cmd_list(args):
    rows, _ = read_index()
    for r in rows:
        print("{}  {:24} {:6.1f} GB  {} -> {}".format(r["archived"], r["job"], r.get("gb", 0), r["from"], r["to"]))
    return 0


def cmd_restore(args):
    rows, remote = read_index()
    hits = [r for r in rows if norm(r["job"]) == norm(args.job)]
    if not hits:
        print("No archived job named {}".format(args.job))
        return 2
    r = hits[-1]
    to = args.to or r["from"]
    if Path(to).exists():
        print("{} already exists; pass --to another folder".format(to))
        return 2
    os.makedirs(to)
    src = ("{}:{}/".format(REMOTE, r["to"]) if remote else r["to"] + "/")
    cmd = ["rsync", "-rt"] + (["-e", "ssh -o BatchMode=yes"] if remote else []) + [src, to + "/"]
    subprocess.run(cmd, check=True)
    log("{}: restored to {}".format(r["job"], to))
    return 0


def cmd_install(args):
    STATE.mkdir(parents=True, exist_ok=True)
    me = Path(__file__).resolve()
    copy = STATE / "jobarchive.py"
    if me != copy:
        shutil.copy2(str(me), str(copy))
    (STATE / "config.json").write_text(json.dumps({"repo": str(args.repo or me.parents[4])}))
    plist = HOME / "Library/LaunchAgents" / (LABEL + ".plist")
    payload = {"Label": LABEL, "ProgramArguments": ["/usr/bin/python3", str(copy), "run", "--until", "8"],
               "StartCalendarInterval": {"Hour": args.hour, "Minute": 15},
               "StandardOutPath": str(STATE / "launchd.log"), "StandardErrorPath": str(STATE / "launchd.log"),
               "WorkingDirectory": str(STATE), "LowPriorityIO": True, "Nice": 10}
    plist.write_bytes(plistlib.dumps(payload))
    dom = "gui/{}".format(os.getuid())
    subprocess.run(["launchctl", "bootout", dom + "/" + LABEL], capture_output=True)
    subprocess.run(["launchctl", "bootstrap", dom, str(plist)], check=True)
    log("installed {} on {}: nightly at {}:15".format(LABEL, host(), args.hour))
    return 0


def cmd_selftest(args):
    tmp = Path(tempfile.mkdtemp(prefix="jobarchive-test-"))
    try:
        work, sea = tmp / "work", tmp / "Expansion"
        for job in ("OLD-1", "NEW-1", "DS-99", "RO-77", "KEEPME"):
            (work / job / "sub").mkdir(parents=True)
            (work / job / "sub" / "a.bin").write_bytes(os.urandom(2000))
            (work / job / "b.txt").write_text(job)
        os.symlink("b.txt", str(work / "OLD-1" / "link"))
        old = time.time() - 40 * 86400
        for job in ("OLD-1", "DS-99", "RO-77", "KEEPME"):
            for d, ds, fs in os.walk(work / job):
                for n in ds + fs + [""]:
                    p = os.path.join(d, n) if n else d
                    os.utime(p, (old, old), follow_symlinks=False)
        sea.mkdir()
        board = tmp / "repo"
        board.mkdir()
        (board / "AI_COORDINATION.md").write_text("**RO-77:DAN-REVIEW-R2:2026-11-14:Claude.** page\n")
        (tmp / "state").mkdir()
        (tmp / "state" / "keep.txt").write_text("KEEPME\n")
        env = dict(os.environ, JOBARCHIVE_ROOTS="internal=" + str(work), JOBARCHIVE_SEAGATE=str(sea),
                   JOBARCHIVE_STATE=str(tmp / "state"), JOBARCHIVE_REPO=str(board), JOBARCHIVE_BUSY="",
                   JOBARCHIVE_STALE_DAYS="60", JOBARCHIVE_HOST="m6",
                   JOBARCHIVE_EDITCAP_JSON=json.dumps({"edits": {"DS-99": {"state": "active"}}, "renderq": {}}))
        me = str(Path(__file__).resolve())
        rows = json.loads(subprocess.run([sys.executable, me, "scan", "--json"], env=env, capture_output=True,
                                         text=True, check=True).stdout)
        verdict = {r["job"]: r["move"] for r in rows}
        assert verdict == {"DS-99": False, "KEEPME": False, "NEW-1": False, "OLD-1": True, "RO-77": False}, verdict
        # Seagate check uses os.path.ismount; force local mode by pointing REMOTE at a host that cannot exist
        # and making the test Seagate look mounted is not possible, so exercise archive_one directly.
        global SEAGATE, STATE
        SEAGATE, STATE = sea, tmp / "state"
        os.environ.update(JOBARCHIVE_HOST="m6")
        row = [r for r in rows if r["job"] == "OLD-1"][0]
        base = str(sea / ARCHIVE_DIR)
        os.makedirs(base)
        dest = archive_one(row, base, remote=False)
        assert not (work / "OLD-1").exists()
        man = json.loads(Path(dest, ".jobarchive-manifest.json").read_text())
        assert len(man["files"]) == 2 and man["symlinks_not_copied"] == [["link", "b.txt"]], man
        assert Path(dest, "sub", "a.bin").exists()
        # A corrupted copy must keep the source.
        row2 = dict(row, job="RO-77", path=str(work / "RO-77"))
        real = hash_tree
        def corrupt(folder, remote=False):
            h = real(folder, remote)
            if folder.startswith(base) and h:
                k = sorted(h)[0]
                h[k] = [h[k][0], "0" * 64]
            return h
        globals()["hash_tree"] = corrupt
        try:
            archive_one(row2, base, remote=False)
            raise AssertionError("corrupt copy was accepted")
        except RuntimeError as ex:
            assert "verify failed" in str(ex), ex
        finally:
            globals()["hash_tree"] = real
        assert (work / "RO-77").exists()
        print("selftest ok")
        return 0
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scan")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("run")
    s.add_argument("--limit", type=int, default=0)
    s.add_argument("--until", type=int, default=None)
    s = sub.add_parser("restore")
    s.add_argument("job")
    s.add_argument("--to")
    sub.add_parser("list")
    s = sub.add_parser("install")
    s.add_argument("--hour", type=int, default=2)
    s.add_argument("--repo")
    sub.add_parser("selftest")
    a = ap.parse_args()
    fn = {"scan": cmd_scan, "run": cmd_run, "restore": cmd_restore, "list": cmd_list, "install": cmd_install,
          "selftest": cmd_selftest}.get(a.cmd)
    if not fn:
        ap.print_help()
        return 2
    return fn(a)


if __name__ == "__main__":
    sys.exit(main())
