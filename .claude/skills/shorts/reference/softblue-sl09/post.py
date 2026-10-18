#!/usr/bin/env python3
"""SL-09 R2, after each render: deliver.py copy (audio gate --verbatim, REVIEW 540p, delivered transcript, plan) then the watch pass
(watch.py, sheets + strips for the judge), then the plan again. Waits for each short's render log to say 'rendered'."""
import os, subprocess, sys, time
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap
WATCH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py"
import plans as P
for S in sys.argv[1:]:
    log = f"logs_render_{S}.txt"
    while not (os.path.exists(log) and "rendered" in open(log).read()): time.sleep(20)
    buildcap.wait(f"SL-09 deliver {S}")
    subprocess.run([sys.executable, "deliver.py", "copy", S])
    G = f"build/{S}/gate"; os.makedirs(G + "/logs", exist_ok=True)
    V = f"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/{P.NAME[S]}.mp4"
    with open(f"{G}/watch_run.log", "w") as lg:
        subprocess.run([sys.executable, WATCH, V, "--plan", f"{G}/plan.json", "--out", f"{G}/watch", "--log", f"{G}/logs/watch_pass.json"], stdout=lg, stderr=subprocess.STDOUT)
    subprocess.run([sys.executable, "deliver.py", "plan", S])
    print(S, "post done", time.strftime("%H:%M:%S"), flush=True)
print("POSTDONE", flush=True)
