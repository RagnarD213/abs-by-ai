#!/usr/bin/env python3
"""Three-way merge for record files (.md, .txt, .json) that settles the collisions two busy Macs produce all day.

    python3 scripts/two-mac/textmerge.py PATH-NAME BASE OURS THEIRS > merged      exit 1 = a person has to decide

git stops whenever both sides touch the same spot. For status lists, calendars and registries most of those stops
need no judgement, and this settles exactly three kinds, hunk by hunk, never dropping a line either side wrote:
  S  one side's lines contain the other's (both added the same entries, one added more): the fuller side;
  L  both sides edited DIFFERENT lines of the same block (neighbouring table rows, a row added beside a row the
     other side changed): every edit is applied;
  U  .md/.txt only: both sides added different lines at the same spot and nothing was there before: both, ours first;
  J  a .json file that is one list of entries: merged entry by entry (both sides' new entries kept, in place).
Anything else (the same line changed two ways, code files, a .json result that no longer parses) is refused.
Used by checkout-sync.py (commits) and reconcile-checkout.py (unsaved edits). Tests: test_checkout_sync.py.
"""
import collections, difflib, json, os, subprocess, sys, tempfile

TYPES = (".md", ".txt", ".json")
MARK = 31                                           # long conflict markers: no real line looks like one


def _subseq(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)


def _separate_lines(o, b, t):
    """Rule L: each side's edits to the block, as (start, end, new lines) against base. They merge when no edit of
    one side touches a base line the other side edited (an insertion beside a changed line is fine)."""
    if not b: return None
    def edits(new):
        return [(i1, i2, new[j1:j2]) for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, b, new, autojunk=False).get_opcodes() if tag != "equal"]
    eo, et = edits(o), edits(t)
    for a1, a2, la in eo:
        for c1, c2, lc in et:
            if (a1, a2, la) == (c1, c2, lc): continue
            if a1 == a2 and c1 == c2:
                if a1 == c1: return None                              # two different insertions at one point
            elif a1 == a2:
                if c1 < a1 < c2: return None                          # insertion inside the other side's change
            elif c1 == c2:
                if a1 < c1 < a2: return None
            elif max(a1, c1) < min(a2, c2): return None               # both changed the same base line(s)
    out, pos = [], 0
    for i1, i2, new in sorted(set((i1, i2, tuple(n)) for i1, i2, n in eo + et), key=lambda e: (e[0], e[0] != e[1], e[1])):
        out += b[pos:i1] + list(new); pos = max(pos, i2)
    return out + b[pos:]


def _hunk(o, b, t, union_ok):
    nb = lambda ls: [l.rstrip() for l in ls if l.strip()]
    no, nbb, nt = nb(o), nb(b), nb(t)
    if no == nt: return o, "same"
    if _subseq(nt, no): return o, "S"
    if _subseq(no, nt): return t, "S"
    res = _separate_lines(o, b, t)
    if res is not None: return res, "L"
    if union_ok and not nbb: return o + t, "U"
    return None, None


def _run(style, names):
    return subprocess.run(["git", "merge-file", "-p", style, "--marker-size={}".format(MARK)] + names, capture_output=True)


def _settle(raw, path):
    try: text = raw.decode("utf-8")
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
    return merged, "settled {} spot(s): {}".format(len(kinds), "+".join(sorted(set(kinds))))


def dedupe_union(merged, ours, theirs):
    """A merge=union file (the board, the handoff index) keeps both sides' lines, so an entry both sides hold can come
    out twice. Drop only the copies the merge added: a line never appears more often than it did on either side."""
    try: mo, oo, tt = merged.decode("utf-8"), ours.decode("utf-8"), theirs.decode("utf-8")
    except UnicodeDecodeError: return merged
    co, ct, seen, out = collections.Counter(oo.splitlines()), collections.Counter(tt.splitlines()), collections.Counter(), []
    for line in mo.splitlines(keepends=True):
        k = line.rstrip("\r\n")
        if len(k.strip()) >= 30:
            seen[k] += 1
            if seen[k] > max(co[k], ct[k], 1): continue
        out.append(line)
    return "".join(out).encode("utf-8")


def _json_list(base, ours, theirs):
    """Rule J: a .json file that is one list of entries (waitlist, cover registry). Merged entry by entry, so two Macs
    that each append an entry, or write the file with different escaping, no longer collide. Returns bytes or None."""
    try:
        raw_t = theirs.decode("utf-8")
        b, o, t = (json.loads(x.decode("utf-8")) if x.strip() else [] for x in (base, ours, theirs))
    except (ValueError, UnicodeDecodeError):
        return None
    if not all(isinstance(d, list) and all(isinstance(e, dict) for e in d) for d in (b, o, t)): return None
    fmt = next(((i, a) for i in (1, 2, 4, None) for a in (False, True)
                if json.dumps(t, indent=i, ensure_ascii=a) in (raw_t, raw_t.rstrip("\n"))), None)
    if fmt is None: return None                                      # unknown layout: do not rewrite the file
    key = lambda e: json.dumps(e, sort_keys=True)
    kb, ko, kt = ([key(e) for e in d] for d in (b, o, t))
    if any(len(set(k)) != len(k) for k in (kb, ko, kt)): return None  # duplicate entries: positions are ambiguous
    sb, so, st = set(kb), set(ko), set(kt)
    ids = [k for k in ("config", "id", "slug", "schedule") if all(k in e for d in (b, o, t) for e in d)
           and all(len({json.dumps(e[k]) for e in d}) == len(d) for d in (b, o, t))]
    if ids:                                                           # one entry changed two ways must not become two entries
        i = ids[0]; mb, mo, mt = ({json.dumps(e[i]): key(e) for e in d} for d in (b, o, t))
        if any(k in mb and mo[k] != mb[k] and mt[k] != mb[k] and mo[k] != mt[k] for k in set(mo) & set(mt)): return None
        if any(k not in mb and mo[k] != mt[k] for k in set(mo) & set(mt)): return None
        replaced = {mt[k] for k in set(mo) & set(mt) if mo[k] != mt[k] and mb.get(k) == mt[k]}   # ours changed it
        keep_theirs = {mo[k] for k in set(mo) & set(mt) if mo[k] != mt[k] and mb.get(k) == mo[k]}  # theirs changed it
    else:
        replaced, keep_theirs = set(), set()
    out = [k for k in kt if not (k in sb and k not in so) and k not in replaced]   # drop what ours deleted or replaced
    have = set(out)
    for n, k in enumerate(ko):                                        # add what ours added, right after its neighbour
        if k in have or k in sb or k in keep_theirs: continue
        prev = next((x for x in reversed(ko[:n]) if x in have), None)
        out.insert(out.index(prev) + 1 if prev is not None else len(out), k); have.add(k)
    order = {key(e): e for d in (t, o) for e in d}                    # keep each entry's own field order
    text = json.dumps([order[k] for k in out], indent=fmt[0], ensure_ascii=fmt[1])
    return (text + ("\n" if raw_t.endswith("\n") else "")).encode("utf-8")


def merge(path, base, ours, theirs):
    """bytes x3 -> (merged bytes or None, short note). A clean git merge is returned as it is."""
    d = tempfile.mkdtemp(prefix="textmerge-")
    try:
        names = []
        for n, data in (("ours", ours), ("base", base), ("theirs", theirs)):
            names.append(os.path.join(d, n))
            with open(names[-1], "wb") as f: f.write(data)
        r = _run("--zdiff3", names)
        if r.returncode == 0: return r.stdout, "clean"
        if r.returncode < 0 or r.returncode > 127 or not path.lower().endswith(TYPES): return None, "not a record file"
        m, note = _settle(r.stdout, path)             # tight hunks first: best for "one side contains the other"
        if m is None:
            m, note = _settle(_run("--diff3", names).stdout, path)   # whole blocks: lets rule L line rows up
        if m is None and path.lower().endswith(".json"):
            m = _json_list(base, ours, theirs)
            if m is not None: note = "list of entries merged entry by entry (J)"
        return m, note
    finally:
        for n in os.listdir(d): os.remove(os.path.join(d, n))
        os.rmdir(d)


if __name__ == "__main__":
    m, note = merge(sys.argv[1], *(open(p, "rb").read() for p in sys.argv[2:5]))
    if m is None:
        sys.stderr.write(note + "\n"); sys.exit(1)
    sys.stdout.buffer.write(m)
