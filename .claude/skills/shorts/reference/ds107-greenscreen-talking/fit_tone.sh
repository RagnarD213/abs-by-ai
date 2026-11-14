#!/bin/bash
# try one BAL_EQ on the Balanced voice and print the voice-alone reference rows
W=/Volumes/Extreme/_edit_work/DS-107/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
BAL_EQ="$1" VOICES_ONLY=balanced python3 recipe/prep.py > logs/fit_tone.log 2>&1 || { tail -3 logs/fit_tone.log; exit 1; }
cd main && python3 "$R/.claude/skills/_shared/audio/audio_gate.py" voice-balanced.wav --video "review/Metabolism Not The Reason SFC R1.mp4" --no-stamp --reference-rows-only 2>&1 | grep -E "Hz|tone|comb|damage|stop|clean between"
