#!/bin/bash
# RA-12 chain A: cut audio + chain default mix, RA-14's APPROVED voice on this roll (fitted EQ + 3 dB at 120 Hz), CTC alignment, head track.
cd /Volumes/Expansion/_edit_work/ra12
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH_A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-12 chain a')"
echo "SLOT $(date +%T)"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py > logs/s08.log 2>&1 || exit 1
EQ=$(cat eq_ra14_approved.txt)
python3 "$SH_A/voice_chain.py" --in cut_audio.wav --out mix_bass.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_bass --eq "$EQ" > logs/s08_bass.log 2>&1 || exit 2
python3 s09_align.py mix_bass.wav words_aligned.json > logs/s09.log 2>&1 || exit 3
python3 s04_track.py > logs/s04.log 2>&1 || exit 4
echo "CHAIN_A_COMPLETE $(date +%T)"
