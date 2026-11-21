#!/bin/zsh
# RO-20 round 3: first minutes of videos 2 and 3 and video 1's ending, with the re-recorded pickups (2026-10-13).
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro20; P=round3/pickups; C=round3/context; O=round3/first-minute; mkdir -p $O
J1=/Volumes/Extreme/_edit_work/ro20/round3/motion/J1-t3.mp4
python3 recipe/pickups20.py P1 $P/words_P1.json $P/P1.mp4 --audio $P/P1.voice.wav --sheet $P/real_sheet_P1.jpg || echo "P1 FAILED"
python3 recipe/pickups20.py P2 $P/words_P2.json $P/P2.mp4 --audio $P/P2.voice.wav --j1 $J1 --j1-in 6.3 --sheet $P/real_sheet_P2.jpg || echo "P2 FAILED"
python3 recipe/pickups20.py P3 $P/words_P3.json $P/P3.mp4 --audio $P/P3.voice.wav --sheet $P/real_sheet_P3.jpg || echo "P3 FAILED"
python3 recipe/pickups20.py P4 $P/words_P4.json $P/P4.mp4 --audio $P/P4.voice.wav --sheet $P/real_sheet_P4.jpg || echo "P4 FAILED"
python3 recipe/context3.py v2open 3014.45 3026.62 --bare v2film 904.70 944.60 v3film 1420.786 1469.75 v1end 884.0 900.35 || echo "CONTEXT FAILED"
python3 recipe/join_r3.py || echo "JOIN FAILED"      # the joins live in Python: zsh reads $i:a as a path modifier
for f in "$O/DRAFT - RO-20B round 3 - video 2 first minute.mp4" "$O/DRAFT - RO-20C round 3 - video 3 first minute.mp4"; do
  python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py" "$f" --no-stamp > "$f.gate.log" 2>&1; grep -E "PASS|FAIL|tone|floor|dry|lufs|spread" "$f.gate.log" | cut -c1-170
done
ffprobe -v error -show_entries format=duration -of csv=p=0 "$O/DRAFT - RO-20B round 3 - video 2 first minute.mp4" "$O/DRAFT - RO-20C round 3 - video 3 first minute.mp4" "$O/DRAFT - RO-20 round 3 - video 1 ending.mp4" 2>&1
echo CHAIN DONE
