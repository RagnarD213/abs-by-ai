#!/usr/bin/env python3
"""Keep this Mac's main project folder level with GitHub, both ways, without touching anyone's uncommitted edits.

    python3 scripts/two-mac/checkout-sync.py             push local commits, then level the folder
    python3 scripts/two-mac/checkout-sync.py --dry       say what it would do, change nothing
    python3 scripts/two-mac/checkout-sync.py --status    the last run on this Mac
    python3 scripts/two-mac/checkout-sync.py --install   install or refresh the every-30-minutes job on this Mac
    python3 scripts/two-mac/checkout-sync.py --uninstall

Why (2026-11-15): two Macs, one checkout each, many sessions in each. Commits piled up locally (M2 17, M6 56)
because safe-push.sh stops when another session's uncommitted edit is in the way of GitHub's changes. This job
removes that dependency:

 1. PUSH. Local commits GitHub lacks are merged with GitHub's main inside git's object store
    (`git merge-tree --write-tree`): no working folder is read or written, so uncommitted edits cannot block it.
    A clean merge is pushed as a merge commit. Collisions in record files that need no judgement are settled by
    rule (.gitattributes union for the board and handoff index, jobsmerge.py, textmerge.py). A real conflict (the
    same line changed two ways, or any code file) is never guessed at: the job stops, names the files and leaves everything as it was. A session then
    merges by hand in a clean checkout (scripts/two-mac/README.md, "When the sync stops").
 2. LEVEL. Once nothing local is missing from GitHub, reconcile-checkout.py brings the folder up to GitHub's
    version, keeping every uncommitted edit (three-way merge, backups under tmp/checkout-reconcile-*).

safe-push.sh stays the normal way a session pushes; this job is the net under it. --install copies the two tools to
~/.absbyai-checkout-sync/bin/ and the job runs that copy (refreshed from GitHub's main each run), so it keeps working
while the folder itself is behind. It never stashes, resets --hard,
rebases, force-pushes or runs `git add`. State and log: ~/.absbyai-checkout-sync/ (status.txt starts OK or STOPPED;
scripts/git/drift-check.sh shows a STOPPED line to sessions).
Exit codes: 0 level or nothing to do, 1 could not run, 3 stopped (conflict or a file in the way), 4 push failed.
"""
import fcntl, os, plistlib, socket, subprocess, sys, time

LABEL = "com.absbyai.checkout-sync"
INTERVAL = 1800
HOME = os.path.expanduser("~")
STATE = os.environ.get("CHECKOUT_SYNC_STATE") or os.path.join(HOME, ".absbyai-checkout-sync")
HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(STATE, "bin")                           # the job runs its own copy, so a folder that is behind still syncs
REPO = os.environ.get("CHECKOUT_SYNC_REPO") or os.path.dirname(os.path.dirname(HERE))
TOOLS = ("checkout-sync.py", "reconcile-checkout.py", "jobsmerge.py", "textmerge.py")
JOBS = "Handoffs/video-editing/jobs.json"
HOST = os.environ.get("CHECKOUT_SYNC_HOST") or socket.gethostname().split(".")[0]
DRY = "--dry" in sys.argv
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_SSH_COMMAND=os.environ.get("GIT_SSH_COMMAND", "ssh -o BatchMode=yes -o ConnectTimeout=20"),
           PATH="/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin")


def git(*a, check=True):
    r = subprocess.run(("git", "-C", REPO) + a, capture_output=True, text=True, env=ENV)
    if check and r.returncode != 0:
        raise RuntimeError("git {} failed: {}".format(" ".join(a[:3]), (r.stderr or r.stdout).strip()[:400]))
    return r


def log(line):
    os.makedirs(STATE, exist_ok=True)
    path = os.path.join(STATE, "sync.log")
    with open(path, "a") as f:
        f.write("{} {} {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), HOST, line))
    if os.path.getsize(path) > 400000:                      # keep the log small: last 2,000 lines
        keep = open(path).read().splitlines()[-2000:]
        open(path, "w").write("\n".join(keep) + "\n")


def finish(code, word, detail):
    line = "{} {} | {} | {}".format(word, time.strftime("%Y-%m-%d %H:%M"), HOST, detail)
    print(line)
    if not DRY:
        log(line)
        tmp = os.path.join(STATE, "status.txt.tmp")
        open(tmp, "w").write(line + "\n")
        os.replace(tmp, os.path.join(STATE, "status.txt"))
    sys.exit(code)


def counts():
    a, b = git("rev-list", "--left-right", "--count", "HEAD...origin/main").stdout.split()
    return int(a), int(b)


def fetch():
    for attempt in (1, 2, 3):                               # another session fetching at the same moment locks the ref
        r = git("fetch", "-q", "origin", check=False)
        if r.returncode == 0:
            return
        time.sleep(3 * attempt)
    raise RuntimeError("git fetch failed: " + r.stderr.strip()[:300])


def settle_conflicts(conflict_tree, base, head, files):
    """Settle conflicts that need no judgement (jobsmerge.py, textmerge.py). Returns (finished tree, None) or (None, first file a person must merge)."""
    sys.path.insert(0, HERE)
    import jobsmerge, textmerge
    blob = lambda ref, f: subprocess.run(["git", "-C", REPO, "show", ref + ":" + f], capture_output=True, env=ENV).stdout
    mb = git("merge-base", base, head).stdout.strip()
    index = os.path.join(STATE, "merge-index.{}".format(os.getpid()))
    env = dict(ENV, GIT_INDEX_FILE=index)
    try:
        subprocess.run(["git", "-C", REPO, "read-tree", conflict_tree], capture_output=True, env=env, check=True)
        for f in files:
            if f == JOBS:
                merged = jobsmerge.merge(blob(mb, f), blob(head, f), blob(base, f))
            else:
                merged = textmerge.merge(f, blob(mb, f), blob(base, f), blob(head, f))[0]
            if merged is None:
                return None, f
            oid = subprocess.run(["git", "-C", REPO, "hash-object", "-w", "--stdin"], input=merged, capture_output=True, env=ENV, check=True).stdout.decode().strip()
            mode = (git("ls-tree", base, "--", f).stdout.split() or ["100644"])[0]
            subprocess.run(["git", "-C", REPO, "update-index", "--add", "--cacheinfo", "{},{},{}".format(mode, oid, f)], capture_output=True, env=env, check=True)
        return subprocess.run(["git", "-C", REPO, "write-tree"], capture_output=True, text=True, env=env, check=True).stdout.strip(), None
    except subprocess.CalledProcessError:
        return None, files[0]
    finally:
        if os.path.exists(index):
            os.remove(index)


def tidy_union_files(tree, base, head):
    """After the merge: in merge=union files both sides changed, drop entry lines the union merge doubled."""
    sys.path.insert(0, HERE)
    import textmerge
    mb = git("merge-base", base, head).stdout.strip()
    changed = lambda ref: set(git("diff", "--name-only", "--no-renames", mb, ref).stdout.splitlines())
    blob = lambda ref, f: subprocess.run(["git", "-C", REPO, "show", ref + ":" + f], capture_output=True, env=ENV).stdout
    fixes = {}
    for f in sorted(changed(base) & changed(head)):
        if not git("--attr-source=" + base, "check-attr", "merge", "--", f).stdout.strip().endswith(": union"):
            continue
        now = blob(tree, f); tidy = textmerge.dedupe_union(now, blob(base, f), blob(head, f))
        if tidy != now:
            fixes[f] = tidy
    if not fixes:
        return tree
    index = os.path.join(STATE, "merge-index.{}".format(os.getpid()))
    env = dict(ENV, GIT_INDEX_FILE=index)
    try:
        subprocess.run(["git", "-C", REPO, "read-tree", tree], capture_output=True, env=env, check=True)
        for f, data in fixes.items():
            oid = subprocess.run(["git", "-C", REPO, "hash-object", "-w", "--stdin"], input=data, capture_output=True, env=ENV, check=True).stdout.decode().strip()
            mode = (git("ls-tree", base, "--", f).stdout.split() or ["100644"])[0]
            subprocess.run(["git", "-C", REPO, "update-index", "--add", "--cacheinfo", "{},{},{}".format(mode, oid, f)], capture_output=True, env=env, check=True)
        return subprocess.run(["git", "-C", REPO, "write-tree"], capture_output=True, text=True, env=env, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        return tree
    finally:
        if os.path.exists(index):
            os.remove(index)


def push_local_commits():
    """Merge HEAD with origin/main in the object store and push the result. Returns a short description."""
    for attempt in (1, 2, 3):
        head = git("rev-parse", "HEAD").stdout.strip()
        base = git("rev-parse", "origin/main").stdout.strip()
        ahead = int(git("rev-list", "--count", "origin/main..HEAD").stdout)
        if ahead == 0:
            return "nothing to push"
        if int(git("rev-list", "--count", "HEAD..origin/main").stdout) == 0:
            new, how = head, "{} commit(s) pushed as they are".format(ahead)      # plain fast-forward of GitHub
        else:
            r = git("--attr-source=" + base, "merge-tree", "--write-tree", "--name-only", "--no-messages", base, head, check=False)
            out = r.stdout.splitlines()
            settled = ""
            if r.returncode == 1:
                files = [l for l in out[1:] if l.strip()]
                tree, unsettled = settle_conflicts(out[0], base, head, files)   # record files: no judgement needed
                if tree:
                    out, r, settled = [tree], None, "; settled by rule: " + ", ".join(files)
            if r is not None and r.returncode == 1:
                files = [unsettled] + [f for f in files if f != unsettled]
                finish(3, "STOPPED", "{} local commit(s) cannot be merged with GitHub automatically: the same lines changed on both sides in {}. Nothing was changed. Fix: hand merge in a clean checkout, scripts/two-mac/README.md".format(ahead, ", ".join(files[:12])))
            if r is not None and (r.returncode != 0 or not out):
                raise RuntimeError("git merge-tree failed: " + (r.stderr or r.stdout).strip()[:300])
            msg = "Merge the {} checkout's {} local commit(s) into main (automatic checkout sync)".format(HOST, ahead)
            new = git("commit-tree", tidy_union_files(out[0], base, head), "-p", base, "-p", head, "-m", msg).stdout.strip()
            how = "{} commit(s) merged with GitHub and pushed ({}){}".format(ahead, new[:7], settled)
        if DRY:
            return "would push: " + how
        r = git("push", "origin", new + ":refs/heads/main", check=False)
        fetch()
        if git("merge-base", "--is-ancestor", new, "origin/main", check=False).returncode == 0:
            return how                                      # GitHub has it (a push can report an error and still land)
        log("push attempt {} did not land: {}".format(attempt, r.stderr.strip()[:200]))
        time.sleep(5)
    finish(4, "STOPPED", "push to GitHub failed three times (network or SSH key); local commits are safe, next run retries")


def level():
    r = subprocess.run([sys.executable, os.path.join(HERE, "reconcile-checkout.py"), "--no-fetch"] + (["--dry"] if DRY else []),
                       cwd=REPO, capture_output=True, text=True, env=ENV)
    tail = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()]
    return r.returncode, (tail[-1] if tail else "no output")[:600], "\n".join(tail)


def refresh_installed_copy():
    """The installed copy follows GitHub's main, so a fix pushed from either Mac reaches both jobs."""
    if os.path.realpath(HERE) != os.path.realpath(BIN):
        return
    for name in TOOLS:
        r = subprocess.run(["git", "-C", REPO, "show", "origin/main:scripts/two-mac/" + name], capture_output=True, env=ENV)
        path = os.path.join(BIN, name)
        if r.returncode != 0 or not r.stdout.strip() or (os.path.exists(path) and r.stdout == open(path, "rb").read()):
            continue
        try:
            compile(r.stdout, name, "exec")
        except SyntaxError:
            log("not refreshing {}: GitHub's copy does not compile".format(name)); continue
        open(path + ".tmp", "wb").write(r.stdout); os.replace(path + ".tmp", path)
        log("refreshed installed {} from GitHub".format(name))


def run():
    os.makedirs(STATE, exist_ok=True)
    lock = open(os.path.join(STATE, "lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("another checkout-sync run is going; nothing done")
        sys.exit(0)
    try:
        gd = git("rev-parse", "--absolute-git-dir").stdout.strip()
        if git("symbolic-ref", "--quiet", "--short", "HEAD", check=False).stdout.strip() != "main":
            finish(1, "STOPPED", "the project folder is not on branch main")
        busy = [m for m in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply") if os.path.exists(os.path.join(gd, m))]
        if busy:
            finish(1, "STOPPED", "a merge or rebase is in progress in the project folder ({}); its owner finishes it".format(busy[0]))
        fetch()
        if not DRY:
            refresh_installed_copy()
        pushed = push_local_commits()
        ahead, behind = counts()
        if ahead:                                           # a session committed while we pushed: next run takes it
            finish(0, "OK", "{}; {} newer local commit(s) wait for the next run".format(pushed, ahead))
        if not behind:
            finish(0, "OK", "{}; folder level with GitHub".format(pushed))
        code, last, full = level()
        log("reconcile exit {}:\n{}".format(code, full))
        if code == 0:
            a2, b2 = counts()
            finish(0, "OK", "{}; {} ({} behind before, ahead {} / behind {} now)".format(pushed, "would level" if DRY else "levelled", behind, a2, b2))
        if code == 3:
            finish(3, "STOPPED", "{}; commits are on GitHub, but the folder stays {} behind: {}".format(pushed, behind, last.replace("STOPPED: ", "")))
        finish(1, "STOPPED", "{}; levelling did not run ({} behind): {}".format(pushed, behind, last))
    except RuntimeError as e:
        finish(1, "STOPPED", str(e))


def install(remove=False):
    plist = os.path.join(HOME, "Library", "LaunchAgents", LABEL + ".plist")
    dom = "gui/{}".format(os.getuid())
    subprocess.run(["launchctl", "bootout", dom + "/" + LABEL], capture_output=True)
    if remove:
        if os.path.exists(plist):
            os.rename(plist, plist + ".off")
        print("job removed (plist kept as {}.off)".format(plist))
        return
    os.makedirs(BIN, exist_ok=True)
    for name in TOOLS:
        if os.path.realpath(HERE) != os.path.realpath(BIN):
            open(os.path.join(BIN, name), "wb").write(open(os.path.join(HERE, name), "rb").read())
    spec = {"Label": LABEL, "ProgramArguments": ["/usr/bin/python3", os.path.join(BIN, "checkout-sync.py")], "StartInterval": INTERVAL,
            "EnvironmentVariables": {"CHECKOUT_SYNC_REPO": REPO},
            "RunAtLoad": False, "ProcessType": "Background", "LowPriorityIO": True, "Nice": 10,
            "StandardOutPath": os.path.join(STATE, "launchd.log"), "StandardErrorPath": os.path.join(STATE, "launchd.log")}
    with open(plist, "wb") as f:
        plistlib.dump(spec, f)
    r = subprocess.run(["launchctl", "bootstrap", dom, plist], capture_output=True, text=True)
    ok = subprocess.run(["launchctl", "print", dom + "/" + LABEL], capture_output=True).returncode == 0
    print("installed {} (every {} min): {}".format(plist, INTERVAL // 60, "loaded" if ok else "NOT loaded: " + r.stderr.strip()))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    if "--install" in sys.argv:
        install()
    elif "--uninstall" in sys.argv:
        install(remove=True)
    elif "--status" in sys.argv:
        p = os.path.join(STATE, "status.txt")
        print(open(p).read().strip() if os.path.exists(p) else "no run recorded on this Mac yet")
    else:
        run()
