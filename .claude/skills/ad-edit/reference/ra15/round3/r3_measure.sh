#!/bin/bash
# RA-15 round 3: measurements on one delivered master: CTC word timing, a fresh Whisper transcript, the junk pass.  r3_measure.sh 9x16|16x9 <master>
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
KEY=$1; M=$2
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 measure $KEY')"
python3 s09_align.py "$M" round3/speech_$KEY.json > logs/align_$KEY.log 2>&1 || { echo "ALIGN FAIL"; exit 1; }
python3 round3/s15_txmaster.py $KEY "$M" > logs/tx_$KEY.log 2>&1 || { echo "TX FAIL"; exit 2; }
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut/junk.py" "$M" --out round3/junk_$KEY.json > logs/junk_$KEY.log 2>&1 || { echo "JUNK FAIL"; exit 3; }
echo "MEASURE_COMPLETE $KEY"
