#!/bin/bash
# RO-37 round 2, stage 2b (heavy slot): the remaining lower thirds, every context range rendered with voice A, the context
# clips and stills, colour stills in the new layout, the review page media.
set -eo pipefail
R=/Volumes/Expansion/_edit_work/RO-37/round2; cd $R/recipe; mkdir -p $R/ctx
python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg/hfbg.py" $R/bg_plan.json $R/hf/bg --render
rm -f $R/review/scenes/BG*.jpg; python3 stills.py
python3 lt2.py --render --only G06,G07,G08,G09,G10,G12,G13,G15,G16,G17,G18,G19,G21,G22,G23,G25
python3 - <<PY
import json, subprocess
R = json.load(open("$R/context_ranges.json"))
for n, (a, b) in enumerate(R):
    out = f"$R/ctx/range{n:02d}.mp4"
    subprocess.run(["python3", "assemble.py", f"$R/ctx/pic{n:02d}.mp4", "--t0", str(a), "--t1", str(b)], check=True)
    subprocess.run(["bash", "mux.sh", f"$R/ctx/pic{n:02d}.mp4", "/Volumes/Expansion/_edit_work/RO-37/round1/voice_A_full.wav", str(a), out], check=True)
    print("range", n, a, b, flush=True)
PY
python3 context.py
python3 colour.py
echo CHAIN2B_DONE
