#!/bin/zsh
# after cut_r3.py: bed at the new length, the mix from the cut voice (same chain as voice A + bed), then the master chain
set -e
B=/Volumes/Expansion/_edit_work/RO-21; cd $B
LEN=$(python3 -c "import json;print(json.load(open('round3/cut_r3.json'))['new_seconds'])")
python3 recipe/bed_r3.py $LEN
EQ='highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7,equalizer=f=120:t=q:w=0.8:g=3'
NOEXP='DS-40 R1 blind listening on this same lav and room reported clipped word tails with the expander; RO-24 (same set) kept the no-expander voice. RO-21 voice A approved by Dan 2026-10-29 with this exact chain.'
python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py" --in audio/film/film_voice_raw_r3b.wav --pull anull --out audio/film/film_mix_r3d.wav --work audio/film/_mix_r3d --eq "$EQ" --no-expander-because "$NOEXP" --bed audio/bed/bed_full.wav --bed-db -31.5 --frame-lock round3/final/picture.mp4 --target -14.0 --tp -2.5 --oversample 4 > audio/film/mix_r3d.log 2>&1
tail -2 audio/film/mix_r3d.log
cd round3/final; rm -rf watch_v3; mv watch watch_v3; cp logs/findings.json logs/findings_v3.json; cd $B
rm -f round3/final/RO21_MASTER.mp4 round3/final/RO21_MASTER.mp4.*
zsh recipe/master_r3.sh
