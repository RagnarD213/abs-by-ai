#!/bin/bash
# RA-12 round 1 chain B: plan (twice, with hold-start samples), graphics sheet + HyperFrames renders, phone + clip cards, captions,
# Dan holds, the working composite, the frame-locked mix, then the whole-ad review cut and the per-item context clips.
cd /Volumes/Expansion/_edit_work/ra12
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
mkdir -p round1/logs
python3 -c "import sys; sys.path.insert(0,'$SH'); import buildcap; buildcap.wait('RA-12 chain b')"
echo "SLOT $(date +%T)"
set -x
python3 s84_plan.py > round1/logs/plan1.log 2>&1 || exit 1
python3 s04b_holdstart.py beats.json > round1/logs/s04b.log 2>&1 || exit 2
python3 s84_plan.py > round1/logs/plan2.log 2>&1 || exit 3
python3 s84b_sheet.py > round1/logs/sheet.log 2>&1 || exit 4
python3 "$SH/hyperframes/vertical.py" --sheet round1/gfx_sheet.json --out round1/gfx --render --snap > round1/logs/gfx.log 2>&1 || exit 5
python3 s83_phone.py > round1/logs/s83.log 2>&1 || exit 6
python3 s83b_clips.py > round1/logs/s83b.log 2>&1 || exit 7
python3 s85_captions.py 9x16 > round1/logs/s85.log 2>&1 || exit 8
python3 s82_holds.py > round1/logs/s82.log 2>&1 || exit 9
python3 s86_assemble.py work > round1/logs/s86w.log 2>&1 || exit 10
EQ=$(cat eq_ra14_approved.txt)
python3 "$SH/audio/voice_chain.py" --in cut_audio.wav --out mix_bass_r1.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_bass_r1 --eq "$EQ" --frame-lock round1/work/picture_9x16.mp4 > round1/logs/mixlock.log 2>&1 || exit 11
python3 s86_assemble.py cuts > round1/logs/s86c.log 2>&1 || exit 12
echo "CHAIN_B_COMPLETE $(date +%T)"
