#!/usr/bin/env python3
"""Three-way merge for record files (.md, .txt, .json) that settles the collisions two busy Macs produce all day.

    python3 scripts/two-mac/textmerge.py PATH-NAME BASE OURS THEIRS > merged      exit 1 = a person has to decide

git stops whenever both sides touch the same spot. For status lists, calendars and registries most of those stops
need no judgement, and this settles exactly three kinds, hunk by hunk, never dropping a line either side wrote:
  S  one side's lines contain the other's (both added the same entries, one added more): the fuller side;
  L  both sides changed DIFFERENT lines of the same block (neighbouring table rows): each line from the side that
     changed it;
  U  .md/.txt only: both sides added different lines at the same spot and nothing was there before: both, ours first.
Anything else (the same line changed two ways, code files, a .json result that no longer parses) is refused.
Used by checkout-sync.py (commits) and reconcile-checkout.py (unsaved edits). Tests: test_checkout_sync.py.
"""
import json, os, subprocess, sys, tempfile

TYPES = (".md", ".txt", ".json")
MARK = 31                                           # long conflict markers: no real line looks like one


def _subseq(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)


def _hunk(o, b, t, union_ok):
    nb = lambda ls: [l.rstrip() for l in ls if l.strip()]
    no, nbb, nt = nb(o), nb(b), nb(t)
    if no == nt: return o, "same"
    if _subseq(nt, no): return o, "S"
    if _subseq(no, nt): return t, "S"
    if len(o) == len(b) == len(t):
        out = []
        for lo, lb, lt in zip(o, b, t):
            if lo == lt or lt == lb: out.append(lo)
            elif lo == lb: out.append(lt)
            else: return None, None
        return out, "L"
    if union_ok and not nbb: return o + t, "U"
    return None, None


def merge(path, base, ours, theirs):
    """bytes x3 -> (merged bytes or None, short note). A clean git merge is returned as it is."""
    d = tempfile.mkdtemp(prefix="textmerge-")
    try:
        names = []
        for n, data in (("ours", ours), ("base", base), ("theirs", theirs)):
            names.append(os.path.join(d, n))
            with open(names[-1], "wb") as f: f.write(data)
        r = subprocess.run(["git", "merge-file", "-p", "--zdiff3", "--marker-size={}".format(MARK)] + names, capture_output=True)
    finally:
        for n in os.listdir(d): os.remove(os.path.join(d, n))
        os.rmdir(d)
    if r.returncode == 0: return r.stdout, "clean"
    if r.returncode < 0 or r.returncode > 127 or not path.lower().endswith(TYPES): return None, "not a record file"
    try: text = r.stdout.decode("utf-8")
    except UnicodeDecodeError: return None, "not text"
    S, B, M, E = "<" * MARK + " ", "|" * MARK + " ", "=" * MARK, ">" * MARK + " "
    out, cur, state, kinds = [], None, None, []
    for line in text.splitlines(keepends=True):
        if cur is None:
            if line.startswith(S): cur, state = {"o": [], "b": [], "t": []}, "o"
            else: out.append(line)
        elif line.startswith(B): state = "b"
        elif line.rstrip("\r\n") == M: state = "t"
        elif line.startswith(E):
            res, kind = _hunk(cur["o"], cur["b"], cur["t"], path.lower().endswith((".md", ".txt")))
            if res is None: return None, "the same lines were changed two ways"
            out += res; kinds.append(kind); cur = None
        else: cur[state].append(line)
    if cur is not None: return None, "unreadable conflict"
    merged = "".join(out).encode("utf-8")
    if path.lower().endswith(".json"):
        try: json.loads(merged.decode("utf-8"))
        except ValueError: return None, "merged .json would not parse"
    return merged, "settled {} spot(s): {}".format(len(kinds), "".join(sorted(set(kinds))))


if __name__ == "__main__":
    m, note = merge(sys.argv[1], *(open(p, "rb").read() for p in sys.argv[2:5]))
    if m is None:
        sys.stderr.write(note + "\n"); sys.exit(1)
    sys.stdout.buffer.write(m)
