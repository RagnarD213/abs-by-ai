#!/usr/bin/env python3
"""Move a folder out of iCloud Drive piece by piece, keeping every old path working.

evacuate.py SRC DST [--log FILE] [--only NAME ...]

For each child of SRC: rename it to DST/child (a same-volume rename; macOS asks iCloud first, which takes a few
seconds and fails with ETIMEDOUT if the subtree changes meanwhile; a failed rename changes nothing), then put a
symlink SRC/child -> DST/child. A busy or very large folder is split: its children are moved the same way.
When every child of SRC is a symlink, SRC itself is swapped for a symlink to DST. Files that a program re-created
at the old path in the meantime (an atomic save replaces the symlink with a real file) are swept again first, and
once more after the swap, so the newest copy always ends up in DST.

With --only, just those children of SRC are moved and SRC is not swapped.
"""
import errno, os, subprocess, sys, time

LOG = None
BIG = 40000          # items: split instead of moving whole
BUSY_MIN = 3         # minutes: a subtree with a file changed this recently is split


def log(*a):
    line = time.strftime("%F %T ") + " ".join(str(x) for x in a)
    print(line, flush=True)
    if LOG:
        with open(LOG, "a") as f:
            f.write(line + "\n")


def count_and_busy(path):
    n, busy, cut = 0, False, time.time() - BUSY_MIN * 60
    for root, dirs, files in os.walk(path):
        n += len(dirs) + len(files)
        if not busy:
            for f in files:
                try:
                    if os.lstat(os.path.join(root, f)).st_mtime > cut:
                        busy = True
                        break
                except OSError:
                    pass
        if n > BIG and busy:
            break
    return n, busy


def is_dataless(path):
    try:
        return bool(os.lstat(path).st_flags & 0x40000000)  # SF_DATALESS
    except OSError:
        return False


def try_rename(src, dst, tries=2):
    for i in range(tries):
        t = time.time()
        try:
            os.rename(src, dst)
            return True, time.time() - t
        except OSError as e:
            if e.errno in (errno.ETIMEDOUT, errno.EBUSY, errno.EAGAIN, errno.EDEADLK):
                log("  retry", os.path.basename(src), e.strerror, f"{time.time()-t:.0f}s")
                time.sleep(5)
                continue
            raise
    return False, 0


def place_link(src, dst):
    # src no longer exists; point it at dst. If something re-created src in the gap, sweep handles it later.
    try:
        os.symlink(dst, src)
    except FileExistsError:
        pass


def move_child(src, dst):
    """Move one entry src -> dst (dst must not exist as a non-symlink dir unless merging)."""
    if os.path.islink(src):
        target = os.readlink(src)
        if os.path.realpath(src) == os.path.realpath(dst) or target == dst:
            return True  # already done
        # a symlink that belongs to the project (e.g. footage on Extreme): recreate it at dst, point src at dst
        if os.path.lexists(dst):
            os.remove(dst)
        os.symlink(target, dst)
        tmp = src + ".evac-link"
        os.symlink(dst, tmp)
        os.rename(tmp, src)
        return True
    if is_dataless(src):
        log("  SKIP cloud-only", src)
        return False
    if os.path.isdir(src):
        if os.path.isdir(dst) and not os.path.islink(dst):
            return evacuate(src, dst)  # dst already started earlier: merge into it
        n, busy = count_and_busy(src)
        if n > BIG or busy:
            log("  split", os.path.basename(src), f"items={n}", "busy" if busy else "")
            return evacuate(src, dst)
        ok, secs = try_rename(src, dst)
        if ok:
            place_link(src, dst)
            log("  moved dir", os.path.basename(src), f"items={n} {secs:.1f}s")
            return True
        log("  split after failed rename", os.path.basename(src))
        return evacuate(src, dst)
    # a file: newest copy wins
    ok, secs = try_rename(src, dst, tries=6)
    if ok:
        place_link(src, dst)
        return True
    log("  FAILED file", src)
    return False


def sweep(src, dst):
    """Move anything in src that is not a symlink into dst (newer content replaces older)."""
    again = 0
    for name in sorted(os.listdir(src)):
        s, d = os.path.join(src, name), os.path.join(dst, name)
        if os.path.islink(s) and os.readlink(s) == d:
            continue
        again += 1
        if not move_child(s, d):
            return -1
    return again


def evacuate(src, dst, only=None):
    os.makedirs(dst, exist_ok=True)
    try:
        st = os.stat(src)
        os.chmod(dst, st.st_mode & 0o7777)
    except OSError:
        pass
    names = sorted(os.listdir(src))
    if only:
        names = [n for n in names if n in only]
    # folders first (static ones are quick), files last so the time a file spends as a symlink is short
    names.sort(key=lambda n: (not os.path.isdir(os.path.join(src, n)) or os.path.islink(os.path.join(src, n)), n))
    ok = True
    for name in names:
        s, d = os.path.join(src, name), os.path.join(dst, name)
        if os.path.islink(s) and os.readlink(s) == d:
            continue
        if not move_child(s, d):
            ok = False
    if only or not ok:
        return ok
    for _ in range(5):
        r = sweep(src, dst)
        if r < 0:
            return False
        if r == 0:
            break
    # swap src for a symlink to dst
    parent, base = os.path.split(src)
    old = os.path.join(parent, "." + base + ".evacuated")
    tmp = os.path.join(parent, "." + base + ".evac-link")
    if os.path.lexists(tmp):
        os.remove(tmp)
    os.symlink(dst, tmp)
    os.rename(src, old)
    os.rename(tmp, src)
    # anything written into the old folder between the last sweep and the swap
    for _ in range(3):
        r = sweep(old, dst)
        if r <= 0:
            break
    leftovers = [n for n in os.listdir(old) if not os.path.islink(os.path.join(old, n))]
    if leftovers:
        log("  LEFTOVER in", old, leftovers[:5])
        return False
    for n in os.listdir(old):
        os.remove(os.path.join(old, n))
    os.rmdir(old)
    log("swapped", src, "->", dst)
    return True


def main():
    global LOG
    a = sys.argv[1:]
    only = None
    if "--log" in a:
        i = a.index("--log"); LOG = a[i + 1]; del a[i:i + 2]
    if "--only" in a:
        i = a.index("--only"); only = set(a[i + 1:]); a = a[:i]
    src, dst = a
    log("evacuate", src, "->", dst, "only=" + ",".join(sorted(only)) if only else "")
    ok = evacuate(src, dst, only)
    log("RESULT", "OK" if ok else "INCOMPLETE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
