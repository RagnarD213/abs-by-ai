#!/bin/zsh
# REV 2 stage 2: everything after the 4K base -- tight (4K) -> hard splices -> plan -> pip -> punch
# -> mix -> audio3 (gated chain, bed -44) -> captions. QC, the gate and the watch pass run after.
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== tight (4K)"; cp tight_cuts.json rev1/tight_cuts_before_stage2.json; RENDER=1 python3 tight.py
python3 - <<'EOF'
import json
a=json.load(open("rev1/tight_cuts.json")); b=json.load(open("tight_cuts.json"))
assert a["keeps"]==b["keeps"] and abs(a["dur"]-b["dur"])<1e-6, "tight cut changed vs rev 1 -- the EDL/env must be identical"
print("tight_cuts.json identical to rev 1:", len(b["keeps"]), "keeps,", b["dur"], "s")
EOF
echo "== hard splices"; python3 hard_splices.py tight.mov tight_cuts.json hard_splices.json
echo "== plan";  python3 layout.py plan
echo "== pip";   python3 layout.py pip
echo "== punch"; python3 layout.py punch
echo "== before (rebuilt at its final length)"; FORCE=1 python3 gfx2.py before
echo "== mix";   python3 layout.py mix
echo "== audio"; MUSIC_DB=-44 COMP=0 python3 audio3.py
echo "== captions"; python3 captions.py
echo "STAGE2 DONE"
