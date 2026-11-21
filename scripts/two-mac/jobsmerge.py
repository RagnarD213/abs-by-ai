#!/usr/bin/env python3
"""Three-way merge of Handoffs/video-editing/jobs.json, job by job, for the two-Mac checkout sync.

    python3 scripts/two-mac/jobsmerge.py BASE OURS THEIRS > merged.json      exit 1 = a real conflict, nothing printed

git merges this file line by line, so two sessions that update DIFFERENT fields of one job, or neighbouring jobs,
collide. Here every job (by "id") and every field is merged on its own:
  - changed on one side only: that side's value;
  - the same field of the same job changed on both sides: the side with the higher "rev" wins (queue.py raises rev
    on every change); equal rev is a real conflict and the merge refuses;
  - a job changed on both sides gets rev = the higher one and syncedRev = the lower one, so the queue syncs it again.
Output is written the way scripts/edit-queue/queue.py writes it (indent 1, UTF-8).
"""
import json, sys

MISSING = object()


def three(b, o, t):
    """Plain value-level 3-way; returns (value, ok)."""
    if o == t: return o, True
    if o == b: return t, True
    if t == b: return o, True
    return None, False


def merge_job(b, o, t):
    if o == t: return o
    if o == b: return t
    if t == b: return o
    if o is None or t is None or b is None:          # deleted on one side and changed on the other, or added twice differently
        if b is None and o is not None and t is not None: b = {}
        else: return MISSING
    ro, rt = o.get("rev", 0), t.get("rev", 0)
    out = {}
    for k in list(t.keys()) + [k for k in o.keys() if k not in t]:
        vb, vo, vt = b.get(k, MISSING), o.get(k, MISSING), t.get(k, MISSING)
        v, ok = three(vb, vo, vt)
        if not ok:
            if k in ("rev", "syncedRev"): v = None
            elif ro == rt: return MISSING
            else: v = vo if ro > rt else vt
        if v is not MISSING: out[k] = v
    out["rev"] = max(ro, rt)
    if "syncedRev" in o or "syncedRev" in t:
        out["syncedRev"] = min(o.get("syncedRev", 0), t.get("syncedRev", 0))
    return out


def merge(base, ours, theirs):
    """bytes, bytes, bytes -> merged bytes, or None when a human has to decide."""
    try:
        b, o, t = (json.loads(x.decode("utf-8")) for x in (base, ours, theirs))
        jb, jo, jt = ({j["id"]: j for j in d["jobs"]} for d in (b, o, t))
        if any(len(m) != len(d["jobs"]) for m, d in ((jb, b), (jo, o), (jt, t))): return None      # duplicate ids
    except (ValueError, KeyError, TypeError, AttributeError):
        return None
    out = {}
    for k in list(t.keys()) + [k for k in o.keys() if k not in t]:
        if k == "jobs": out[k] = None; continue
        v, ok = three(b.get(k, MISSING), o.get(k, MISSING), t.get(k, MISSING))
        if not ok: return None
        if v is not MISSING: out[k] = v
    jobs = []
    for i in [j["id"] for j in t["jobs"]] + [j["id"] for j in o["jobs"] if j["id"] not in jt]:
        m = merge_job(jb.get(i), jo.get(i), jt.get(i))
        if m is MISSING: return None
        if m is not None: jobs.append(m)
    out["jobs"] = jobs
    return (json.dumps(out, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


if __name__ == "__main__":
    r = merge(*(open(p, "rb").read() for p in sys.argv[1:4]))
    if r is None: sys.exit(1)
    sys.stdout.buffer.write(r)
