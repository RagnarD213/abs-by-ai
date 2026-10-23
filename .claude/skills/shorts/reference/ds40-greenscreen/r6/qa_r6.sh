#!/bin/zsh
# DS-40 R6 QA on the delivered master: gate inputs (untreated mix, SRT, delivered ASR, plan), audio gate + A/B, junk report,
# watch pass (judged later by the independent reviewer), delivery gate.
set -e
cd /Volumes/Expansion/_edit_work/ds40/r6
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
D="$R/Short-form video content/Fat 90 Year Old - DS-40"
M="$D/Fat 90 Year Old SFC R6 - complete Short.mp4"
python3 gateplan_r6.py "$M" 2>&1 | grep -v Warn | tail -1
python3 -c "import sys;sys.path.insert(0,'$R/.claude/skills/_shared/audio');import common as C;C.stash_untreated('mix-untreated.wav',C.pcm('mix-untreated.wav',af='pan=mono|c0=0.5*c0+0.5*c1'),note='untreated timeline: the clip original sound (same 581 frames) + the raw C1730 lav pieces cut like the film, pan mono')"
python3 "$R/.claude/skills/_shared/audio/audio_gate.py" "$M" --untreated mix-untreated.wav --ab "$D/Fat 90 Year Old SFC R6 - audio AB.mp4" > audio_gate.log 2>&1 || true; grep -E "FAIL|AUDIO GATE|loudness|clipping" audio_gate.log | head
python3 "$R/.claude/skills/_shared/cut/junk.py" "$M" --out junk_report.json --quiet > junk.log 2>&1 || true; tail -2 junk.log
rm -rf qa; mkdir -p qa
python3 "$R/.claude/skills/_shared/deliver/watch.py" "$M" --plan gate-plan.json --out qa --log qa/watch_pass.json --clips > qa/watch.log 2>&1 || true; grep -E "scan|frozen|naked|graphics present|boundaries" qa/watch.log | head
"$R/Media/video_edit/bin/ffmpeg" -v error -y -i "$M" -vf "scale=540:960" -c:v libx264 -crf 24 -preset medium -c:a aac -b:a 128k -movflags +faststart "$D/Fat 90 Year Old SFC R6 - REVIEW 540p.mp4"
echo QA DONE
