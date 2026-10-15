#!/bin/bash
# RA-04 round 4: _shared/cut/piccuts.py decide over every audio join of the final EDL (a check: the picture keeps cut.json; each pause
# splice inside a hold already carries a level change, s05_plan04.py asserts it). Any join it returns cover:push + watch goes on the watch list.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 piccuts')"
G=$(python3 -c "import json;print(json.load(open('grade.json'))['filter'])")
R=$(python3 -c "import ra01lib as L;print(L.ROLL)")
mkdir -p round4/piccuts
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut/piccuts.py" decide --build round4/piccuts --mode raw --raw "$R" \
   --grade "$G" --edl round4/edl_audio.json --talk round4/talk_spans.json > logs/r4_piccuts.log 2>&1 || { echo PICCUTS_FAIL; exit 1; }
grep -E "^splice|decided" logs/r4_piccuts.log
echo PICCUTS_COMPLETE
