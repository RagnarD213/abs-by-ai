#!/usr/bin/env python3
"""Locate a phrase on the TIGHT timeline. Search AFTER a time, never globally:
a repeated line matches the wrong occurrence otherwise (an /ad-edit rev-5 lesson)."""
import json, re, sys
W = json.load(open("/Volumes/Extreme/_edit_work/abwheel/r2/words_tight.json"))
def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower())
TOK = [norm(w["w"]) for w in W]
def find(phrase, after=0.0):
    p = norm(phrase).split()
    for i in range(len(W) - len(p) + 1):
        if W[i]["t"] < after: continue
        if TOK[i:i+len(p)] == p:
            return round(W[i]["t"], 2), round(W[i+len(p)-1]["e"], 2)
    return None
if __name__ == "__main__":
    for arg in sys.argv[1:]:
        after, _, ph = arg.partition("|")
        try: after = float(after)
        except ValueError: ph, after = arg, 0.0
        r = find(ph, after)
        m = (lambda t: f"{int(t//60)}:{t%60:05.2f}")
        print(f"{(m(r[0])+' - '+m(r[1])) if r else 'NOT FOUND':>20s}  {ph!r}")
