#!/usr/bin/env python3
"""Bring a shared, dirty checkout level with GitHub without losing or overwriting anyone's uncommitted edits.

    python3 scripts/two-mac/reconcile-checkout.py --dry     what it would do; writes only the backup folder
    python3 scripts/two-mac/reconcile-checkout.py           do it

Built 2026-11-14 for the M2's own checkout (two Macs, two checkouts; the M2 was 28 commits behind and `git pull`
refused because sessions there hold uncommitted edits). Only for a checkout with NO local commits (it refuses
otherwise; a checkout with its own commits pushes with scripts/git/safe-push.sh, which merges). It never stashes,
never rebases and never touches a file GitHub did not change. For each file GitHub changed:
  - not edited locally: updated to GitHub's version;
  - edited locally and identical to GitHub's: left alone, just recorded as up to date;
  - edited on both sides: three-way merged; the local edit stays on top as an uncommitted change. If the merge
    conflicts but the local copy adds nothing GitHub lacks, GitHub's version is taken. Any other conflict stops the
    run before anything has moved;
  - new on GitHub with a different local copy: the local copy is left as it is.
Every file in the last three groups is first copied to tmp/checkout-reconcile-<date>-<time>/.
"""
import subprocess, sys, os, shutil, time
def git(*a, check=True, inp=None):
    r = subprocess.run(("git",) + a, capture_output=True, text=True, input=inp)
    if check and r.returncode != 0:
        raise SystemExit("git {} failed: {}".format(" ".join(a[:3]), r.stderr.strip()[:400]))
    return r.stdout
def blob(ref, p):
    return subprocess.run(["git", "rev-parse", "-q", "--verify", "{}:{}".format(ref, p)], capture_output=True, text=True).stdout.strip() or None
def wt(p): return git("hash-object", p).strip() if os.path.isfile(p) else None
git("fetch", "-q", "origin")
OLD, NEW = git("rev-parse", "HEAD").strip(), git("rev-parse", "origin/main").strip()
a, b = git("rev-list", "--left-right", "--count", "HEAD...origin/main").split()
assert a == "0", "local commits exist; not a fast-forward"
if b == "0": raise SystemExit("already level")
assert subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0, "something is staged"
assert not os.path.exists(".git/MERGE_HEAD") and not os.path.exists(".git/index.lock")
raw = git("status", "--porcelain=v1", "-z").split("\0"); st = {}; i = 0
while i < len(raw):
    e = raw[i]
    if e:
        if e[0] in "RC": i += 1
        st[e[3:]] = e[:2]
    i += 1
up = git("diff", "--name-status", "-z", "--no-renames", OLD, NEW).split("\0")
upf = {up[i + 1]: up[i] for i in range(0, len(up) - 1, 2)}
assert all(c in ("M", "A") for c in upf.values()), "upstream deletes files; handle by hand: {}".format({p: c for p, c in upf.items() if c not in "MA"})
udirs = [p for p, c in st.items() if c == "??" and p.endswith("/")]
same, both, clean = [], [], []
for p, c in sorted(upf.items()):
    local = p in st or any(p.startswith(u) for u in udirs) or (os.path.exists(p) and blob(OLD, p) is None)
    if not local: clean.append(p); continue
    (same if wt(p) == blob(NEW, p) else both).append(p)
print("behind {} | upstream files {} | untouched locally {} | identical to GitHub {} | both changed {}".format(b, len(upf), len(clean), len(same), both))
bk = "tmp/checkout-reconcile-{}".format(time.strftime("%Y%m%d-%H%M%S"))
os.makedirs(bk, exist_ok=True)
for p in same + both:
    os.makedirs(os.path.join(bk, os.path.dirname(p)), exist_ok=True); shutil.copy2(p, os.path.join(bk, p))
open(os.path.join(bk, "README.txt"), "w").write("Checkout reconcile {}\nfrom {} to {}\nidentical to GitHub: {}\nboth changed (3-way merged): {}\n".format(time.ctime(), OLD, NEW, same, both))
merged = {}
for p in both:                                   # 3-way merge must be clean before anything moves
    base, theirs = os.path.join(bk, p + ".base"), os.path.join(bk, p + ".github")
    open(theirs, "w").write(git("show", "{}:{}".format(NEW, p)))
    if blob(OLD, p) is None:                     # new on GitHub AND a different local copy: its owner is live, keep theirs
        print("  {}: new on GitHub, local copy differs; local copy left as it is (shows as modified)".format(p))
        continue
    open(base, "w").write(git("show", "{}:{}".format(OLD, p)))
    r = subprocess.run(["git", "merge-file", "-p", p, base, theirs], capture_output=True, text=True)
    if r.returncode != 0:
        # a conflict is still safe when the local copy adds nothing GitHub lacks (GitHub = local edit + more)
        d = subprocess.run(["git", "diff", "--no-index", "--", theirs, p], capture_output=True, text=True).stdout
        extra = [l for l in d.splitlines() if l.startswith("+") and not l.startswith("+++") and l[1:].strip()]
        if extra: raise SystemExit("merge of {} has {} conflicts and {} local-only lines; nothing changed".format(p, r.returncode, len(extra)))
        print("  {}: local edit is already inside GitHub's version; taking GitHub's (local copy kept in the backup)".format(p))
        merged[p] = open(theirs).read()
    else:
        merged[p] = r.stdout
if "--dry" in sys.argv: raise SystemExit("dry run: backup in {}; nothing changed".format(bk))
git("reset", "--soft", NEW)
try:
    if clean: git("checkout", NEW, "--pathspec-from-file=-", "--pathspec-file-nul", inp="\0".join(clean))
    git("reset", "-q", NEW, "--pathspec-from-file=-", "--pathspec-file-nul", inp="\0".join(same + both))
except SystemExit:
    subprocess.run(["git", "reset", "--soft", OLD]); raise
for p, text in merged.items():
    if wt(p) != git("hash-object", os.path.join(bk, p)).strip(): raise SystemExit("{} changed during the merge; left as is, merged copy in {}".format(p, bk))
    tmp = p + ".reconcile.tmp"; open(tmp, "w").write(text); shutil.copymode(p, tmp); os.replace(tmp, p)
print("HEAD", git("rev-parse", "--short", "HEAD").strip(), "| vs GitHub", git("rev-list", "--left-right", "--count", "HEAD...origin/main").split(), "| staged clean:", subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0, "| backup", bk)
