#!/bin/bash
# RA-12 round 1, rebuild after the independent review (D2 word endings, D4 G1 push, D5 P1 entry, D7 plan text).
cd /Volumes/Expansion/_edit_work/ra12
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'$SH'); import buildcap; buildcap.wait('RA-12 chain c')"
echo "SLOT $(date +%T)"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py > round1/logs/c_s08.log 2>&1 || exit 1
EQ=$(cat eq_fit_r1.txt)
python3 "$SH/audio/voice_chain.py" --in cut_audio.wav --out mix_fit_b1.5.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_fit_r2 --eq "$EQ,equalizer=f=120:t=q:w=0.8:g=+1.5" > round1/logs/c_mix.log 2>&1 || exit 2
python3 s09_align.py mix_fit_b1.5.wav words_aligned.json > round1/logs/c_s09.log 2>&1 || exit 3
python3 s84_plan.py > round1/logs/c_plan1.log 2>&1 || exit 4
python3 s04b_holdstart.py beats.json > round1/logs/c_s04b.log 2>&1 || exit 5
python3 s84_plan.py > round1/logs/c_plan2.log 2>&1 || exit 6
python3 s84b_sheet.py > round1/logs/c_sheet.log 2>&1 || exit 7
python3 "$SH/hyperframes/vertical.py" --sheet round1/gfx_sheet.json --out round1/gfx --render --snap --force > round1/logs/c_gfx.log 2>&1 || exit 8
python3 s83_phone.py > round1/logs/c_s83.log 2>&1 || exit 9
python3 s83b_clips.py > round1/logs/c_s83b.log 2>&1 || exit 10
python3 s85_captions.py 9x16 > round1/logs/c_s85.log 2>&1 || exit 11
rm -f round1/seg/*.mp4 round1/seg/holds.json
python3 s82_holds.py > round1/logs/c_s82.log 2>&1 || exit 12
python3 s86_assemble.py work > round1/logs/c_s86w.log 2>&1 || exit 13
N=$(python3 -c "import json;print(json.load(open('beats.json'))['total_frames'])"); D=$(python3 -c "print(f'{$N*1001/30000:.6f}')")
"$FF" -nostdin -v error -y -i mix_fit_b1.5.wav -af "apad,atrim=0:$D" -c:a pcm_s16le mix_bass_r1.wav || exit 14
python3 s86_assemble.py cuts > round1/logs/c_s86c.log 2>&1 || exit 15
echo "CHAIN_C_COMPLETE $(date +%T)"
