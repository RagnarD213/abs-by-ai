#!/bin/bash
# RA-05 setup: measurements on the delivered master (RA-04 round 4 r4_measure.sh method).
#   CTC word timing on the delivered audio (round3/s09_align.py, run read-only from round3: it reads cut.json, writes only
#   the path given), a fresh Whisper transcript of the file, and the junk pass in delivered mode. Outputs in setup/.
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$REPO/Media/video_edit/bin:$PATH"
M="$REPO/Claude Ad Videos/how ai can get you real six pack abs - RA-05/how ai can get you real six pack abs | claude | 9x16 | RA-05.mp4"
S=/Volumes/Extreme/_edit_work/ra05/setup; HERE="$REPO/.claude/skills/ad-edit/reference/ra05/setup"
python3 -c "import sys; sys.path.insert(0,'$REPO/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-05 setup measure')"
(cd /Volumes/Extreme/_edit_work/ra05/round3 && python3 s09_align.py "$M" "$S/speech_9x16.json") > "$S/logs/align.log" 2>&1 || { echo ALIGN FAIL; exit 1; }
python3 "$HERE/s91_txmaster.py" "$M" > "$S/logs/tx.log" 2>&1 || { echo TX FAIL; exit 2; }
python3 "$REPO/.claude/skills/_shared/cut/junk.py" "$M" --out "$S/junk_9x16.json" > "$S/logs/junk.log" 2>&1 || { echo JUNK FAIL; exit 3; }
tail -3 "$S/logs/align.log"; head -1 "$S/logs/tx.log" | tail -1; grep -E "candidates|confirmed" "$S/logs/junk.log" | head -3
echo MEASURE_COMPLETE
