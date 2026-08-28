#!/usr/bin/env python3
"""Place B-roll against the TRANSCRIPT, not against a slot number.

Dan's rule from the spray-tan revision is "generally there shouldn't be more than 30
seconds without a clip or some kind of graphic", and the gate wants ≥40 % coverage. On a
30- or 53-minute programme that is 130–230 inserts, and hand-authoring each one against
the line it illustrates — which `spec_example_abwheel.py` does, and which is the right way
at 26 inserts — stops being possible.

So the CHOICE stays transcript-driven and only the bookkeeping is automated: for every free
slot, read the words that are actually spoken across it, score them against a topic table,
and take the best-matching unused clip from that topic's pool. A slot whose words match
nothing gets a clip from the `generic` pool rather than a wrong one — an insert that
contradicts the line is worse than a neutral one.

Occupied windows are the chips AND the cards: a full-frame insert HIDES a lower third, and
that assertion has caught a real collision before.

usage:
  plan_inserts.py --srt captions.srt --occupied windows.json --stock stock_ids.txt
                  --topics topics.json --dur 1827.7 --out inserts.json
                  [--gap 11] [--len 4.4] [--start 8] [--pad 1.2]
"""
import argparse, json, re, sys


def read_srt(path):
    cues = []
    for blk in open(path).read().strip().split("\n\n"):
        L = blk.split("\n")
        if len(L) < 3: continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", L[1])
        if not m: continue
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        cues.append((a, b, " ".join(L[2:]).lower()))
    return cues


def text_between(cues, a, b):
    return " ".join(t for (ca, cb, t) in cues if cb > a and ca < b)


def free_slots(occupied, dur, start, length, gap, pad):
    occ = sorted((a - pad, b + pad) for a, b in occupied)
    slots, t = [], start
    while t + length < dur - 6:
        clash = next(((a, b) for a, b in occ if not (t + length <= a or t >= b)), None)
        if clash:
            t = clash[1] + 0.4
            continue
        slots.append(round(t, 2))
        t += length + gap
    return slots


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--occupied", required=True)
    ap.add_argument("--stock", required=True, help="'<id> <name>' per line")
    ap.add_argument("--topics", required=True,
                    help='{"topic": {"words": [...], "clips": ["name-substring", ...]}}')
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--gap", type=float, default=11.0)
    ap.add_argument("--len", dest="length", type=float, default=4.4)
    ap.add_argument("--start", type=float, default=8.0)
    ap.add_argument("--pad", type=float, default=1.2)
    ap.add_argument("--cooldown", type=float, default=420.0,
                    help="seconds before a clip may appear again")
    A = ap.parse_args()

    cues = read_srt(A.srt)
    occ = [(w[1], w[2]) for w in json.load(open(A.occupied))]
    T = json.load(open(A.topics))
    stock = [l.split(None, 1) for l in open(A.stock) if l.strip()]
    names = [n.strip() for _, n in stock]

    pools = {}
    for topic, cfg in T.items():
        pools[topic] = [n for n in names
                        if any(s in n for s in cfg.get("clips", []))]
    unclaimed = [n for n in names if not any(n in p for p in pools.values())]
    pools.setdefault("generic", [])
    pools["generic"] += unclaimed

    slots = free_slots(occ, A.dur, A.start, A.length, A.gap, A.pad)
    # A clip may come back, but only FAR apart -- the spray-tan build reused eight clips
    # and every reuse was more than ten minutes from its first appearance. A hard
    # "never twice" set instead simply runs out: 111 slots against a 7-clip topic pool
    # left 35 slots unfilled and dropped coverage to 33%.
    last, plan, nomatch, reused = {}, [], 0, 0
    for t in slots:
        txt = text_between(cues, t - 2.5, t + A.length + 1.5)
        best, score = None, 0
        for topic, cfg in T.items():
            sc = sum(txt.count(w) for w in cfg["words"])
            if sc > score: best, score = topic, sc
        pool = list(pools.get(best) or [])
        def take(cands):
            fresh = [n for n in cands if n not in last]
            if fresh: return fresh[0]
            ok = [n for n in cands if t - last[n] >= A.cooldown]
            return min(ok, key=lambda n: last[n]) if ok else None
        pick = take(pool)
        if pick is None:
            nomatch += 1
            pick = take(pools["generic"] + pool)
        if pick is None:
            pick = min(pool or pools["generic"] or names, key=lambda n: last.get(n, -1e9))
        if pick in last: reused += 1
        last[pick] = t
        plan.append({"t": t, "dur": A.length, "key": pick, "topic": best or "generic",
                     "line": txt[:90]})
    json.dump(plan, open(A.out, "w"), indent=1)
    cov = (len(plan) * A.length + sum(b - a for a, b in occ)) / A.dur
    print(f"{len(slots)} free slots -> {len(plan)} inserts "
          f"({nomatch} had no topic match and took a generic clip; {reused} are repeats "
          f"at least {A.cooldown/60:.0f} min apart)")
    print(f"nominal coverage incl. graphics: {cov*100:.0f}% of {A.dur/60:.1f} min")
    from collections import Counter
    for topic, n in Counter(x["topic"] for x in plan).most_common():
        print(f"   {topic:<14} {n}")
