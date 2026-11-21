#!/bin/zsh
# DS-44 R1 QA on the delivered master: audio gate (+ untreated stash), gate plan (delivered ASR), watch pass, delivery gate.
cd /Volumes/Expansion/_edit_work/DS-44/r2
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
M="review/Hormozi Fat Guy SFC R2 - complete Short.mp4"
python3 -c "import sys;sys.path.insert(0,'$R/.claude/skills/_shared/audio');import common as C;C.stash_untreated('mix-untreated.wav',C.pcm('mix-untreated.wav',af='pan=mono|c0=0.5*c0+0.5*c1'),note='untreated timeline: the clip original sound (same segments as the film) + the raw C1730 lav pieces, pan mono')"
python3 "$R/.claude/skills/_shared/audio/audio_gate.py" "$M" --untreated mix-untreated.wav --ab "review/Hormozi Fat Guy SFC R2 - audio AB.mp4" > audio_gate.log 2>&1; grep -E "FAIL|AUDIO GATE|loudness|clipping" audio_gate.log
python3 recipe/gateplan.py > gateplan.log 2>&1 || { echo GATEPLAN FAIL; tail -5 gateplan.log; exit 1; }; tail -1 gateplan.log | cut -c1-160
rm -rf qa; mkdir -p qa
python3 "$R/.claude/skills/_shared/deliver/watch.py" "$M" --plan gate-plan.json --out qa --log qa/watch_pass.json --clips > qa/watch.log 2>&1; grep -E "scan|frozen|naked|graphics present|boundaries" qa/watch.log
echo CHAIN QA DONE
