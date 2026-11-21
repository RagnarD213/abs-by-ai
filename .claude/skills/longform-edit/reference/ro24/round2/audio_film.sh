#!/bin/bash
# round 2 film voice: cut the lav to edl_film.json (15 ms fades in measured silence), then Dan's pick A (Bill Maher voice plus
# the bass lift: Balanced EQ + 3 dB at 120 Hz, no expander), -14.1 LUFS, -1.5 dBTP, oversample 4: the exact round 1 option.
set -euo pipefail
W=/Volumes/Expansion/_edit_work/RO-24/round2; R=$W/recipe
python3 $R/voice_cut.py $W/edl_film.json $W/audio/film_voice_raw.wav | tail -2
EQ='highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7,equalizer=f=120:t=q:w=0.8:g=3'
NOEXP="DS-40 R1 blind listening on this same lav and room reported clipped word tails with the expander; Dan kept the no-expander voice there."
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py" --in $W/audio/film_voice_raw.wav --pull anull \
  --out $W/audio/film_voice_A.wav --work $W/audio/_A --target -14.1 --tp -1.5 --oversample 4 --eq "$EQ" --no-expander-because "$NOEXP" | tail -3
echo AUDIO DONE
