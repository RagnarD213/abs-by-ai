#!/usr/bin/env python3
"""round 3: wait for a build slot (buildcap), then render A B D E one after another, then scan them."""
import subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap
for S in sys.argv[1:]:
    buildcap.wait(f"SL-07 r3 render {S}")
    subprocess.run([sys.executable, "batch.py", "render", S], check=True)
    subprocess.run([sys.executable, "scan.py", S])
open("r3probe/render.done", "w").write("ok")
