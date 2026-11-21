#!/bin/zsh
# RO-20 round 3b: the four pickups re-recorded on the shoot lav (C1722, 2026-10-15) laid into video 2's and video 3's first minutes and video 1's ending.
# Context clips are unchanged film (round3/context, built by first_minutes_r3.sh), so only the pickup segments and the joins are rebuilt.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro20; P=round3/pickups; O=round3b/first-minute; mkdir -p $O
python3 -c 'import sys; sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap; buildcap.wait("RO-20 R3b first minutes")'
J1=/Volumes/Extreme/_edit_work/ro20/round3/motion/J1-t3.mp4
python3 recipe/pickups20.py P1 $P/words_P1.json $P/P1.mp4 --audio $P/P1.voice.wav --sheet $P/real_sheet_P1.jpg || echo "P1 FAILED"
python3 recipe/pickups20.py P2 $P/words_P2.json $P/P2.mp4 --audio $P/P2.voice.wav --j1 $J1 --j1-in 6.3 --sheet $P/real_sheet_P2.jpg || echo "P2 FAILED"
python3 recipe/pickups20.py P3 $P/words_P3.json $P/P3.mp4 --audio $P/P3.voice.wav --sheet $P/real_sheet_P3.jpg || echo "P3 FAILED"
python3 recipe/pickups20.py P4 $P/words_P4.json $P/P4.mp4 --audio $P/P4.voice.wav --sheet $P/real_sheet_P4.jpg || echo "P4 FAILED"
python3 recipe/join_r3b.py || echo "JOIN FAILED"
for f in "$O/DRAFT - RO-20B round 3b - video 2 first minute.mp4" "$O/DRAFT - RO-20C round 3b - video 3 first minute.mp4" "$O/DRAFT - RO-20 round 3b - video 1 ending.mp4"; do
  python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py" "$f" --no-stamp > "$f.gate.log" 2>&1; echo "== $f"; grep -E "PASS|FAIL" "$f.gate.log" | cut -c1-170
done
echo CHAIN DONE
