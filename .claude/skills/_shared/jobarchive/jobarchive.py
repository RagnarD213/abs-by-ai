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
    BUILDING, NEEDS DAN or PICK), regardless of age
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
import shlex
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HOME = Path.home()
STATE = Path(os.environ.get("JOBARCHIVE_STATE") or HOME / ".absbyai-jobarchive")
IDLE_DAYS = float(os.environ.get("JOBARCHIVE_IDLE_DAYS") or 14)
# Dan-approved explicit moves (run --approved): named jobs skip the idle-days and "a skill/script points at it" guards
# and may be removed after the Seagate copy alone verifies. Live, review, board, keep-list and process guards still apply.
APPROVED=set()
KEEP_FILES={}
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
        # ._* are macOS metadata sidecars that exFAT shows as files; rsync carries the metadata, not the sidecar.
        if rel == ".jobarchive-manifest.json" or f.startswith("._") or f == ".DS_Store" \
                or os.path.islink(p) or not os.path.isfile(p):
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
        return False
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
        raise RuntimeError("board unreadable; reference evidence incomplete")
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
            result=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
            if result.returncode:raise RuntimeError('process-reference command failed: '+cmd[0])
            parts.append(result.stdout)
        except (OSError, subprocess.TimeoutExpired) as e:
            raise RuntimeError('process-reference evidence incomplete: '+str(e))
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
    required=places[:3]+files
    if any(not p.exists() for p in required):raise RuntimeError('reference evidence incomplete: required rules/library/scripts missing')
    errors=[]
    for place in places:
        if not place.exists():continue
        for d, dirs, fs in os.walk(str(place),onerror=lambda e:errors.append(str(e))):
            dirs[:] = [x for x in dirs if x not in ("node_modules", ".git", "__pycache__")]
            files.extend(Path(d) / f for f in fs if f.endswith(REF_EXT))
    for f in files:
        try:
            if f.stat().st_size > 60_000_000:
                errors.append('reference file too large to inspect: '+str(f));continue
            names |= {norm(m) for m in REF_RE.findall(f.read_text(errors="ignore"))}
        except OSError as e:
            errors.append(str(e))
    if errors:raise RuntimeError('reference evidence incomplete: '+errors[0])
    return names


def review_paths():
    """Registered durable reviews protect their source roots and linked relative paths, regardless of age."""
    paths=[]
    for entry in (HOME/'Library/Application Support/AbsByAI Review Hub/pages').glob('*.json'):
        try:
            x=json.loads(entry.read_text());root=Path(x['root']).resolve();paths.append(root)
            port=entry.stem;rdir=HOME/'Library/Application Support/AbsByAI Reviews'/port;manifest=rdir/'manifest.json'
            # A review whose whole folder is gone is retired: its recorded root stays protected, but there are no linked files to read.
            if not rdir.exists():continue
            m=json.loads(manifest.read_text())
            paths += [(root/f['path']).resolve() for f in m.get('files',[])]
        except (OSError,ValueError,KeyError,TypeError) as e:raise RuntimeError('review reference evidence incomplete: '+str(e))
    for plist in (HOME/'Library/LaunchAgents').glob('com.absbyai.review.*.plist'):
        try:
            x=plistlib.loads(plist.read_bytes());args=x.get('ProgramArguments',[])
            source=x.get('EnvironmentVariables',{}).get('ABS_REVIEW_SOURCE_ROOT')
            if not source and len(args)>3:source=args[3]
            if not source:raise RuntimeError('legacy review source unknown')
            paths.append(Path(source).resolve())
        except (OSError,ValueError,plistlib.InvalidFileException) as e:raise RuntimeError('legacy review evidence incomplete: '+str(e))
    return paths


def keep_names():
    names = set()
    for p in (Path(__file__).resolve().parent / "keep.txt", STATE / "keep.txt",
              repo()/'.claude/skills/_shared/jobarchive/keep.txt'):
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
    reviews=review_paths()
    rows = []
    for label, root in roots():
        for entry in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if not entry.is_dir() or entry.is_symlink() or entry.name.startswith((".", "_")):
                continue
            newest, size, links = tree_stats(entry)
            idle = (now - newest) / 86400
            key = norm(entry.name)
            why = None
            if idle < IDLE_DAYS and key not in APPROVED:
                why = "changed {:.1f} days ago".format(idle)
            elif key in keep:
                why = "on the keep list"
            elif key in refs and key not in APPROVED:
                why = "a skill, script or standing rule points at it"
            elif any(p==entry.resolve() or entry.resolve() in p.parents for p in reviews):
                why = 'registered unresolved review points at this folder'
            elif ec is None:
                why = "edit cap unreadable; keeping everything tonight"
            elif ec[0].get(key) in ("active", "promoted", "waiting", "new"):
                why = "edit cap lists it as {}".format(ec[0][key])
            elif key in ec[1]:
                why = "render queue step is live"
            elif str(entry) in busy or str(entry.resolve()) in busy:
                why = "a running process uses it"
            elif ec[0].get(key) in ("with-dan", "stalled"):
                why = "with Dan for review (edit cap)"
            elif on_board(entry.name, board):
                why = "with Dan for review (board)"
            rows.append({"job": entry.name, "path": str(entry), "drive": label, "idle_days": round(idle, 1),
                         "gb": round(size / 1e9, 2), "links": links, "move": why is None, "why": why or ""})
    return rows


def seagate_local():
    return (SEAGATE / ".").exists() and os.path.ismount(str(SEAGATE)) and on_local_disk(SEAGATE)


def ssh(args, **kw):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", REMOTE,
                           ' '.join(shlex.quote(str(a)) for a in args)], **kw)


def hash_tree(folder, remote=False):
    if remote:
        r = ssh(["/usr/bin/python3", "-", folder], input=HASHER, capture_output=True, text=True)
    else:
        r = subprocess.run([sys.executable, "-", folder], input=HASHER, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("hashing failed: " + (r.stderr or "")[-500:])
    return json.loads(r.stdout)


def io_python(code, args, remote=False, text=None):
    cmd=['/usr/bin/python3' if remote else sys.executable,'-c',code]+[str(a) for a in args]
    r=ssh(cmd,input=text,capture_output=True,text=True) if remote else subprocess.run(cmd,input=text,capture_output=True,text=True)
    if r.returncode:raise RuntimeError('archive I/O failed: '+r.stderr[-500:])
    return r.stdout


def mount_identity(remote=False):
    code="""import os,sys,json,subprocess,re
p=sys.argv[1]
r=subprocess.run(['mount'],capture_output=True,text=True,check=True)
line=next((l for l in r.stdout.splitlines() if ' on '+p+' (' in l),None)
if not line or any(k in line for k in ['smbfs','nfs','afpfs','webdav']):raise RuntimeError('actual attached Seagate mount missing')
s=os.stat(p)
print(json.dumps([line,s.st_dev]))
"""
    identity=json.loads(io_python(code,[SEAGATE],remote))
    volume_code="import subprocess,plistlib,sys,json;x=plistlib.loads(subprocess.run(['diskutil','info','-plist',sys.argv[1]],capture_output=True,check=True).stdout);print(json.dumps([x.get('VolumeName'),x.get('VolumeUUID')]))"
    volume=json.loads(io_python(volume_code,[SEAGATE],remote))
    expected=json.loads((STATE/'config.json').read_text()).get('seagate_uuid')
    if not expected or volume!=['Expansion',expected]:raise RuntimeError('Seagate UUID unverified or wrong volume mounted')
    return identity+[volume[1]]


def check_mount(identity,remote):
    if mount_identity(remote)!=identity:raise RuntimeError('Seagate mount identity changed; source retained')


def read_text(path,remote):
    return io_python("import pathlib,sys;p=pathlib.Path(sys.argv[1]);print(p.read_text() if p.exists() else '',end='')",[path],remote)


def write_remote_text(path, text, remote):
    io_python("""import os,sys,pathlib
p=pathlib.Path(sys.argv[1]);tmp=p.with_name(p.name+'.tmp-'+str(os.getpid()))
with tmp.open('w') as f:f.write(sys.stdin.read());f.flush();os.fsync(f.fileno())
os.replace(tmp,p)
""",[path],remote,text)
    if read_text(path,remote)!=text:raise RuntimeError('manifest read-back mismatch')


def append_index(base, record, remote):
    path=base+'/index.jsonl';line=json.dumps(record)+'\n'
    existing=read_text(path,remote)
    if record in [json.loads(l) for l in existing.splitlines() if l.strip()]:return
    io_python("""import os,sys,fcntl
with open(sys.argv[1],'a') as f:
 fcntl.flock(f,fcntl.LOCK_EX);f.write(sys.stdin.read());f.flush();os.fsync(f.fileno())
""",[path],remote,line)
    if record not in [json.loads(l) for l in read_text(path,remote).splitlines() if l.strip()]:
        raise RuntimeError('index read-back mismatch; source retained')


def second_copy_verified(src,files):
    try:
        copies=json.loads((STATE/'verified-second-copies.json').read_text())
        other=Path(copies[str(src)])
        if other.resolve()==src.resolve() or src.resolve() in other.resolve().parents:return False
        if SEAGATE.resolve()==other.resolve() or SEAGATE.resolve() in other.resolve().parents:return False
        return hash_tree(str(other))==files
    except (OSError,ValueError,KeyError):return False


def archive_one(row, base, remote):
    src=Path(row['path']);dest='{}/{}-{}/{}'.format(base,host(),row['drive'],src.name)
    identity=mount_identity(remote);check_mount(identity,remote)
    before=tree_stats(src)
    src_hash=hash_tree(str(src))
    old=read_text(dest+'/.jobarchive-manifest.json',remote)
    manifest=json.loads(old) if old else None
    if manifest:
        if manifest['from']!=str(src) or any(manifest['files'].get(k)!=v for k,v in src_hash.items()):
            raise RuntimeError('retry conflicts with original full manifest; source retained')
        # A partially removed source is never allowed to replace the original full manifest.
    else:
        log('{}: copying {:.1f} GB from {} to the Seagate'.format(src.name,row['gb'],row['drive']))
        io_python('import os,sys;os.makedirs(sys.argv[1],exist_ok=True)',[dest],remote)
        target='{}:{}/'.format(REMOTE,shlex.quote(dest)) if remote else dest+'/'
        cmd=['rsync','-rt','--exclude=._*','--exclude=.DS_Store']+(['-e','ssh -o BatchMode=yes'] if remote else [])+[str(src)+'/',target]
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode:raise RuntimeError('copy failed: '+r.stderr[-500:])
        manifest=dict(job=src.name,**{'from':str(src)},mac=host(),drive=row['drive'],
                      archived=dt.datetime.now().isoformat(timespec='seconds'),files=src_hash,
                      symlinks_not_copied=before[2])
    check_mount(identity,remote)
    if hash_tree(dest,remote)!=manifest['files']:raise RuntimeError('verify failed: file set or bytes differ; source kept')
    if tree_stats(src)!=before or hash_tree(str(src))!=src_hash:
        raise RuntimeError('source changed during copy; source kept')
    write_remote_text(dest+'/.jobarchive-manifest.json',json.dumps(manifest,indent=1),remote)
    rec={k:manifest[k] for k in ('job','from','mac','drive','archived')}
    rec.update(to=dest,files=len(manifest['files']),gb=round(sum(v[0] for v in manifest['files'].values())/1e9,2))
    append_index(base,rec,remote)
    # Recheck live/review/keep references immediately before removing any source.
    fresh=next((r for r in decide() if r['path']==str(src)),None)
    if not fresh or not fresh['move']:raise RuntimeError('source became protected or reference evidence missing; retained')
    check_mount(identity,remote)
    if hash_tree(dest,remote)!=manifest['files'] or hash_tree(str(src))!=src_hash:
        raise RuntimeError('last removal check changed; source retained')
    if not second_copy_verified(src,manifest['files']) and norm(src.name) not in APPROVED:
        log(src.name+': archive verified and indexed; source RETAINED until independent second copy verified')
        return dest
    def gone_ok(func,path,exc):
        if not isinstance(exc[1],FileNotFoundError):raise exc[1]
    keepers={}
    for rel in KEEP_FILES.get(norm(src.name),[]):
        f=src/rel
        if f.is_file():keepers[rel]=f.read_bytes()
        elif f.is_dir():
            for g in f.rglob('*'):
                if g.is_file() and not g.is_symlink():keepers[str(g.relative_to(src))]=g.read_bytes()
    shutil.rmtree(str(src),onerror=gone_ok)
    for rel,data in keepers.items():
        t=src/rel;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(data)
        if hashlib.sha256(t.read_bytes()).hexdigest()!=hashlib.sha256(data).hexdigest():raise RuntimeError('kept file write-back mismatch: '+rel)
    if keepers:log('{}: kept {} small referenced file(s) in place'.format(src.name,len(keepers)))
    log('{}: verified {} files, durable index and second copy; source removed'.format(src.name,len(manifest['files'])))
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
    try:mount_identity(remote)
    except (RuntimeError,OSError) as e:
        log('archive mount unavailable: '+str(e));return 1
    base = str(SEAGATE / ARCHIVE_DIR)
    if remote:
        if ssh(["test", "-d", str(SEAGATE)], capture_output=True).returncode:
            log("Seagate not reachable on {}; nothing moved".format(REMOTE))
            warn_low_space()
            return 1
        ssh(["mkdir", "-p", base], capture_output=True)
    else:
        os.makedirs(base, exist_ok=True)
    if getattr(args,"approved",None):
        APPROVED.update(norm(x) for x in args.approved.split(',') if x.strip())
        for spec in getattr(args,"keep_file",None) or []:
            job,_,rel=spec.partition(':');KEEP_FILES.setdefault(norm(job),[]).append(rel)
    rows = [r for r in decide() if r["move"] and (not APPROVED or norm(r["job"]) in APPROVED)]
    rows.sort(key=lambda r: -r["idle_days"])
    done = errors = retained = 0
    for r in rows:
        if args.limit and done + retained >= args.limit:
            break
        if args.until is not None and args.until <= dt.datetime.now().hour < args.until + 12:
            log("past {}:00; the rest wait for tomorrow night".format(args.until))
            break
        try:
            archive_one(r, base, remote)
            if Path(r['path']).exists():retained += 1
            else:done += 1
        except (RuntimeError, OSError, subprocess.CalledProcessError) as ex:
            errors += 1
            log("ERROR {}: {}".format(r["job"], ex))
    log("done: {} moved, {} verified copies with source retained, {} errors, {} left for later".format(
        done,retained,errors,len(rows)-done-retained-errors))
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
    if Path(to).exists() and (not Path(to).is_dir() or any(Path(to).iterdir())):
        print("{} is not empty; pass --to another folder".format(to))
        return 2
    os.makedirs(to,exist_ok=True)
    src = ("{}:{}/".format(REMOTE, shlex.quote(r["to"])) if remote else r["to"] + "/")
    cmd = ["rsync", "-rt"] + (["-e", "ssh -o BatchMode=yes"] if remote else []) + [src, to + "/"]
    identity=mount_identity(remote)
    manifest=json.loads(read_text(r['to']+'/.jobarchive-manifest.json',remote))
    subprocess.run(cmd,check=True)
    check_mount(identity,remote)
    if hash_tree(to)!=manifest['files']:raise RuntimeError('restored file set or hashes differ; restore incomplete')
    unresolved=[]
    for rel,target in manifest.get('symlinks_not_copied',[]):
        link=Path(to)/rel
        if Path(rel).is_absolute() or '..' in Path(rel).parts:raise RuntimeError('invalid link path')
        link.parent.mkdir(parents=True,exist_ok=True)
        if link.exists() or link.is_symlink():raise RuntimeError('restore link collision')
        link.symlink_to(target)
        if not link.exists():unresolved.append(rel)
    if unresolved:raise RuntimeError('restored bytes verified; unresolved links: '+repr(unresolved))
    log('{}: restored bytes and links verified at {}'.format(r['job'],to))
    return 0


def cmd_install(args):
    STATE.mkdir(parents=True, exist_ok=True)
    me = Path(__file__).resolve()
    copy = STATE / "jobarchive.py"
    if me != copy:
        shutil.copy2(str(me), str(copy))
    volume_code="import subprocess,plistlib,json;x=plistlib.loads(subprocess.run(['diskutil','info','-plist','/Volumes/Expansion'],capture_output=True,check=True).stdout);print(json.dumps({'uuid':x.get('VolumeUUID'),'name':x.get('VolumeName')}))"
    remote=not seagate_local()
    volume=json.loads(io_python(volume_code,[],remote))
    if volume.get('name')!='Expansion' or not volume.get('uuid'):raise RuntimeError('cannot establish Seagate identity')
    (STATE / "config.json").write_text(json.dumps({"repo": str(args.repo or me.parents[4]),'seagate_uuid':volume['uuid']}))
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
    import unittest
    suite=unittest.defaultTestLoader.discover(str(Path(__file__).parent),pattern='test_jobarchive.py')
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scan")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("run")
    s.add_argument("--limit", type=int, default=0)
    s.add_argument("--until", type=int, default=None)
    s.add_argument("--approved", help="comma list of jobs Dan approved to move now (Seagate copy only)")
    s.add_argument("--keep-file", action="append", help="JOB:relative/path left in place after the move")
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
    try:return fn(a)
    except (RuntimeError,OSError,ValueError) as e:
        log('BLOCKED: '+str(e)+'; production sources retained')
        return 1


if __name__ == "__main__":
    sys.exit(main())
