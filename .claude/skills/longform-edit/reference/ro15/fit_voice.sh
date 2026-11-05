#!/bin/bash
# The approved 9/23 studio voice (audio B: the chain's own fit on this roll's whole assembled voice + 0.9 dB at 150 Hz, no dereverb)
# and B + the standard bass lift (+3 dB at 120 Hz, VIDEO-RULES 2026-10-12), as on RO-14, RO-17, RO-18.
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; W=/Volumes/Extreme/_edit_work/RO-15/round1
export PATH="$P/Media/video_edit/bin:$PATH"; cd $W
python3 "$P/.claude/skills/_shared/audio/voice_chain.py" --in assembled_untreated.wav --out fit/fit_full.wav --no-dereverb --work fit/work > logs/fit.log 2>&1; echo "FIT EXIT $?"
python3 - <<'PY'
import json
W='/Volumes/Extreme/_edit_work/RO-15/round1/fit/'
d=json.load(open(W+'fit_full.wav.voice_chain.json'))
eq=d['eq']; B=eq+",bass=g=0.9:f=150:width_type=q:width=0.7"; B3=B+",equalizer=f=120:t=q:w=0.8:g=+3.0"
open(W+'eq_B.txt','w').write(B); open(W+'eq_B_bass3.txt','w').write(B3)
print('EQ', d.get('eq_gains'), 'edt', d.get('edt_raw'), 'lufs', d.get('lufs'))
PY
