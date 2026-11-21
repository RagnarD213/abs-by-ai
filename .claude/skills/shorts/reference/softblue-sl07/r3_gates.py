#!/usr/bin/env python3
"""run rungate.sh for each short in turn, after any gate already running has finished (matches by argv, never its own line)"""
import subprocess, sys, time
NEEDLE = "deliver/" + "gate" + ".py"
def busy():
    out = subprocess.run(["ps", "-Ao", "command"], capture_output=True, text=True).stdout
    return any(NEEDLE in l or ("rungate" + ".sh") in l for l in out.splitlines() if "r3_gates" not in l)
for S in sys.argv[1:]:
    while busy(): time.sleep(20)
    subprocess.run(["./rungate.sh", S], stdout=open(f"r3probe/gate_{S}.txt", "w"), stderr=subprocess.STDOUT)
    print(S, "gate done", flush=True)
