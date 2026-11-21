#!/bin/bash
# RA-05 setup: the watch pass on the approved master with the setup plan (judged afterwards by a fresh independent judge).
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$REPO/Media/video_edit/bin:$PATH"
M="$REPO/Claude Ad Videos/how ai can get you real six pack abs - RA-05/how ai can get you real six pack abs | claude | 9x16 | RA-05.mp4"
S=/Volumes/Extreme/_edit_work/ra05/setup
python3 -c "import sys; sys.path.insert(0,'$REPO/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-05 setup watch')"
rm -rf "$S/watch"
python3 "$REPO/.claude/skills/_shared/deliver/watch.py" "$M" --plan "$S/plan.json" --out "$S/watch" --log "$S/watch/logs/watch_pass.json"
