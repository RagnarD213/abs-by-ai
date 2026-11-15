#!/usr/bin/env python3
"""Bring a shared, dirty checkout level with GitHub without losing or overwriting anyone's uncommitted edits.

    python3 scripts/two-mac/reconcile-checkout.py --dry     what it would do; writes only the backup folder
    python3 scripts/two-mac/reconcile-checkout.py           do it
    ... --take-github=PATH   by hand only, for a blocked file with NO live owner (untouched 2 hours or more, such as
                             a stale generated file): take GitHub's version; the local copy goes to the backup folder

Built 2026-11-14 for the M2's own checkout (two Macs, two checkouts; the M2 was 28 commits behind and `git pull`
refused because sessions there hold uncommitted edits). Only for a checkout with NO commits GitHub lacks (it refuses
otherwise; scripts/two-mac/checkout-sync.py pushes those first, through a merge that never touches this folder).
It never stashes, never rebases and never touches a file GitHub did not change. For each file GitHub changed:
  - not edited locally: updated to GitHub's version;
  - edited locally and identical to GitHub's: left alone, just recorded as up to date;
  - edited on both sides: three-way merged; the local edit stays on top as an uncommitted change. If the merge
    conflicts but the local copy adds nothing GitHub lacks, GitHub's version is taken; in a file .gitattributes marks
    merge=union (the board, the handoff index) both sides' lines are kept; the edit queue's jobs.json is merged job
    by job (jobsmerge.py); in .md, .txt and .json record files the collisions that need no judgement are settled
    (textmerge.py: one side contains the other, different lines of one block, two additions at one spot). Any other
    conflict stops the run before
    anything has moved (exit 3, every such file is named);
  - a local copy that equals an EARLIER GitHub version of the file (a hand copy from the other Mac that GitHub has
    since moved past): GitHub's current version is taken;
  - new on GitHub with a different local copy: the local copy is left as it is;
  - deleted on GitHub (2026-11-15): removed here only when the local copy is unedited (it is copied to the backup
    first); an edited local copy stays on disk; a copy already gone locally needs nothing.
Another session's staged changes are kept as they are; the run refuses (exit 3) only when a staged file is one
GitHub also changed. Every file in the last four groups is first copied to tmp/checkout-reconcile-<date>-<time>/.
The branch moves with a compare-and-swap, so a commit a session makes during the run is never dropped.
Exit codes: 0 levelled (or already level), 1 refused or failed, 3 stopped on a named file.
"""
import subprocess, sys, os, shutil, time
def git(*a, check=True, inp=None):
    r = subprocess.run(("git",) + a, capture_output=True, text=True, input=inp)
    if check and r.returncode != 0:
        raise SystemExit("git {} failed: {}".format(" ".join(a[:3]), r.stderr.strip()[:400]))
    return r.stdout
def stop(msg):
    print("STOPPED: " + msg); sys.exit(3)
def blob(ref, p):
    return subprocess.run(["git", "rev-parse", "-q", "--verify", "{}:{}".format(ref, p)], capture_output=True, text=True).stdout.strip() or None
def wt(p):
    if os.path.islink(p):                        # git stores a link as its target text
        return subprocess.run(["git", "hash-object", "--stdin"], input=os.readlink(p).encode(), capture_output=True).stdout.decode().strip()
    return git("hash-object", p).strip() if os.path.isfile(p) else None
def show(ref, p): return subprocess.run(["git", "show", "{}:{}".format(ref, p)], capture_output=True, check=True).stdout
JOBS = "Handoffs/video-editing/jobs.json"
TAKE = {a.split("=", 1)[1] for a in sys.argv if a.startswith("--take-github=")}
def status():
    raw = git("status", "--porcelain=v1", "-z").split("\0"); st = {}; i = 0
    while i < len(raw):
        e = raw[i]
        if e:
            if e[0] in "RC": i += 1
            st[e[3:]] = e[:2]
        i += 1
    return st
os.chdir(git("rev-parse", "--show-toplevel").strip())
if "--no-fetch" not in sys.argv: git("fetch", "-q", "origin")
OLD, NEW = git("rev-parse", "HEAD").strip(), git("rev-parse", "origin/main").strip()
a, b = git("rev-list", "--left-right", "--count", "HEAD...origin/main").split()
if a != "0": raise SystemExit("{} local commit(s) GitHub lacks; push them first (scripts/two-mac/checkout-sync.py)".format(a))
if b == "0": print("already level"); sys.exit(0)
gd = git("rev-parse", "--git-dir").strip()
if any(os.path.exists(os.path.join(gd, m)) for m in ("MERGE_HEAD", "index.lock", "rebase-merge", "rebase-apply", "CHERRY_PICK_HEAD")):
    raise SystemExit("a merge, rebase, cherry-pick or another git command is in progress; try again later")
st = status()
up = git("diff", "--name-status", "-z", "--no-renames", OLD, NEW).split("\0")
upf = {up[i + 1]: up[i] for i in range(0, len(up) - 1, 2)}
odd = {p: c for p, c in upf.items() if c not in ("M", "A", "D")}
if odd: stop("GitHub changes these in a way this tool does not handle; do them by hand: {}".format(odd))
staged = sorted(p for p in git("diff", "--cached", "--name-only", "-z", "--no-renames").split("\0") if p in upf)
if staged: stop("staged by a session here AND changed on GitHub; its owner commits or unstages first: {}".format(staged))
udirs = [p for p, c in st.items() if c == "??" and p.endswith("/")]
same, both, clean, gone_rm, gone_keep, gone_idx, lost = [], [], [], [], [], [], []
for p, c in sorted(upf.items()):
    local = p in st or any(p.startswith(u) for u in udirs) or (os.path.lexists(p) and blob(OLD, p) is None)
    if c == "D":
        if not os.path.lexists(p): gone_idx.append(p)
        elif not local and wt(p) == blob(OLD, p): gone_rm.append(p)
        else: gone_keep.append(p)
    elif not local: clean.append(p)
    elif not os.path.lexists(p): lost.append(p)                 # deleted locally, changed on GitHub: stays deleted here
    else: (same if wt(p) == blob(NEW, p) else both).append(p)
print("behind {} | upstream files {} | untouched locally {} | identical to GitHub {} | both changed {} | deleted on GitHub: removed here {}, edited copy kept {} | deleted locally, kept so {}".format(
    b, len(upf), len(clean), len(same), both, gone_rm, gone_keep, lost))
bk = "tmp/checkout-reconcile-{}".format(time.strftime("%Y%m%d-%H%M%S"))
os.makedirs(bk, exist_ok=True)
for p in same + both + gone_rm + gone_keep:
    os.makedirs(os.path.join(bk, os.path.dirname(p)), exist_ok=True); shutil.copy2(p, os.path.join(bk, p), follow_symlinks=False)
open(os.path.join(bk, "README.txt"), "w").write("Checkout reconcile {}\nfrom {} to {}\nidentical to GitHub: {}\nboth changed (3-way merged): {}\ndeleted on GitHub, removed here (copy kept in this folder): {}\ndeleted on GitHub, edited local copy left on disk: {}\n".format(
    time.ctime(), OLD, NEW, same, both, gone_rm, gone_keep))
merged, stuck = {}, []
for p in both:                                   # 3-way merge must be clean before anything moves
    base, theirs = os.path.join(bk, p + ".base"), os.path.join(bk, p + ".github")
    open(theirs, "wb").write(show(NEW, p))
    mine = wt(p)
    if p in TAKE:                                   # named by hand: a stale generated file with no live owner
        print("  {}: taking GitHub's version as asked (local copy kept in the backup)".format(p))
        merged[p] = show(NEW, p); continue
    if any(blob(c, p) == mine for c in git("log", "--format=%H", "{}..{}".format(OLD, NEW), "--", p).split()):
        print("  {}: local copy is an earlier GitHub version (a hand copy); taking GitHub's current one".format(p))
        merged[p] = show(NEW, p); continue
    if blob(OLD, p) is None:                     # new on GitHub AND a different local copy: its owner is live, keep theirs
        print("  {}: new on GitHub, local copy differs; local copy left as it is (shows as modified)".format(p))
        continue
    open(base, "wb").write(show(OLD, p))
    r = subprocess.run(["git", "merge-file", "-p", p, base, theirs], capture_output=True)
    if r.returncode != 0 and git("--attr-source=" + NEW, "check-attr", "merge", "--", p).strip().endswith(": union"):
        r = subprocess.run(["git", "merge-file", "-p", "--union", p, base, theirs], capture_output=True)   # .gitattributes: keep both sides' lines
        print("  {}: both sides changed the same spot; both sides' lines kept (union file)".format(p))
    if r.returncode != 0 and p == JOBS:                 # the edit queue list merges job by job, newer rev wins
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import jobsmerge
        m = jobsmerge.merge(show(OLD, p), open(p, "rb").read(), show(NEW, p))
        if m is not None:
            print("  {}: merged job by job (a job changed on both sides keeps the newer rev)".format(p))
            merged[p] = m; continue
    if r.returncode != 0:                                # record files: settle the collisions that need no judgement
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import textmerge
        m, note = textmerge.merge(p, show(OLD, p), open(p, "rb").read(), show(NEW, p))
        if m is not None:
            print("  {}: {} (every local line kept)".format(p, note))
            merged[p] = m; continue
    if r.returncode != 0:
        # a conflict is still safe when the local copy adds nothing GitHub lacks (GitHub = local edit + more)
        d = subprocess.run(["git", "diff", "--no-index", "--", theirs, p], capture_output=True, text=True, errors="replace").stdout
        extra = [l for l in d.splitlines() if l.startswith("+") and not l.startswith("+++") and l[1:].strip()]
        if extra:
            stuck.append("{} ({} local-only lines, last edited {:.1f} h ago)".format(p, len(extra), (time.time() - os.path.getmtime(p)) / 3600))
            continue
        print("  {}: local edit is already inside GitHub's version; taking GitHub's (local copy kept in the backup)".format(p))
        merged[p] = open(theirs, "rb").read()
    else:
        merged[p] = r.stdout
if stuck:
    stop("edited here and on GitHub in the same lines: {}. Nothing changed. Each file's owner commits it with safe-push.sh (any session may once it is older than 2 h), then run again".format("; ".join(stuck)))
if "--dry" in sys.argv: print("dry run: backup in {}; nothing changed".format(bk)); sys.exit(0)
st2 = status()
moved = sorted(p for p in upf if st.get(p) != st2.get(p))
if moved: raise SystemExit("files changed while planning ({}); nothing moved, run again".format(moved[:5]))
# compare-and-swap: fails, changing nothing, if a session committed since OLD was read
git("update-ref", "-m", "reconcile-checkout: level with GitHub", "HEAD", NEW, OLD)
try:
    if clean: git("checkout", NEW, "--pathspec-from-file=-", "--pathspec-file-nul", inp="\0".join(clean))
    idx = same + both + lost + gone_rm + gone_keep + gone_idx
    if idx: git("reset", "-q", NEW, "--pathspec-from-file=-", "--pathspec-file-nul", inp="\0".join(idx))
except SystemExit:
    subprocess.run(["git", "update-ref", "HEAD", OLD, NEW]); raise
for p, data in merged.items():
    if wt(p) != git("hash-object", os.path.join(bk, p)).strip():
        open(os.path.join(bk, p + ".merged"), "wb").write(data)
        print("  {} changed during the merge; left as is, merged copy is {}/{}.merged".format(p, bk, p)); continue
    tmp = p + ".reconcile.tmp"; open(tmp, "wb").write(data); shutil.copymode(p, tmp); os.replace(tmp, p)
for p in gone_rm:
    if wt(p) == git("hash-object", os.path.join(bk, p)).strip(): os.remove(p)
    else: print("  {} changed during the run; left on disk".format(p))
print("HEAD", git("rev-parse", "--short", "HEAD").strip(), "| vs GitHub", git("rev-list", "--left-right", "--count", "HEAD...origin/main").split(), "| backup", bk)
