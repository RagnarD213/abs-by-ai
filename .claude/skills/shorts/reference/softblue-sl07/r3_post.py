#!/usr/bin/env python3
"""round 3, after each render: deliver.py copy (audio gate, REVIEW 540p, transcript, plan) then the watch pass, in one build slot."""
import os, subprocess, sys, time
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap
WATCH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py"
NAME = {"A": "short1_stop-trying-to-lose-1-pound-a-week", "B": "short2_weigh-yourself-every-morning", "D": "short3_work-out-every-morning", "E": "short4_the-3-pound-rule", "F": "short5_track-your-calories-with-a-photo"}
args = sys.argv[1:]
for S in args:
    if S.startswith("pid="):                                            # wait for that render process (r3_render.py renders and scans) to end
        pid = int(S[4:])
        while True:
            try: os.kill(pid, 0); time.sleep(15)
            except OSError: break
        continue
    buildcap.wait(f"SL-07 r3 deliver {S}")
    if os.environ.get("SKIPCOPY") != "1": subprocess.run([sys.executable, "deliver.py", "copy", S])
    G = f"build/{S}/gate"; os.makedirs(G + "/logs", exist_ok=True)
    V = f"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/belly-fat-90-days-{NAME[S]}.mp4"
    with open(f"{G}/watch_run.log", "w") as lg:
        subprocess.run([sys.executable, WATCH, V, "--plan", f"{G}/plan.json", "--out", f"{G}/watch", "--log", f"{G}/logs/watch_pass.json"], stdout=lg, stderr=subprocess.STDOUT)
    subprocess.run([sys.executable, "deliver.py", "plan", S])
    print(S, "post done", flush=True)
open("r3probe/post.done", "w").write("ok")
