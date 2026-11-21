#!/usr/bin/env python3
"""round 3: blind listener on the studio-lav pickups (B, D) with the round 2 film-only and film-join controls. N runs, names shuffled."""
import json, random, shutil, subprocess, os, sys, re
L = os.path.dirname(os.path.abspath(__file__)); N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
SRC = os.environ.get("SRC", "B_r3pickup,D_r3pickup,A_film,A_filmjoin,E_film").split(","); TAG = os.environ.get("TAG", "4")
res = {s: [] for s in SRC}
for k in range(N):
    d = f"{L}/trial{TAG}_{k}"; os.makedirs(d, exist_ok=True); names = random.sample("ABCDEGHKMNPRST", len(SRC)); mp = {}
    for n, s in zip(names, SRC): shutil.copy(f"{L}/src_{s}.mp3", f"{d}/clip_{n}.mp3"); mp[n] = s
    order = sorted(mp); json.dump(mp, open(f"{d}/map.json", "w"))
    out = subprocess.run([sys.executable, f"{L}/gemini_listen.py", f"{L}/q.txt"] + [f"{d}/clip_{n}.mp3" for n in order], capture_output=True, text=True).stdout
    open(f"{d}/answer.txt", "w").write(out)
    m = re.search(r"\{.*\}", out, re.S); j = json.loads(m.group(0)); j = j.get("clips", j)
    for n in order:
        v = next((v for kk, v in j.items() if f"clip_{n}" in kk), None)
        if v: res[mp[n]].append([v.get("match"), v.get("pickup"), v.get("differs", "")])
    print(k, {s: res[s][-1][:2] for s in SRC if res[s]}, flush=True)
json.dump(res, open(f"{L}/trials{TAG}.json", "w"), indent=0)
for s in SRC: print(s, "called a pickup %d of %d, match median %s" % (sum(1 for r in res[s] if r[1]), len(res[s]), sorted(r[0] for r in res[s])[len(res[s]) // 2] if res[s] else "-"))
