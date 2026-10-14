#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra06
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
set -x
R=round1; mkdir -p $R/stills
cp draft_9x16.mp4 "$R/DRAFT - RA-06 round 1 - full ad.mp4" || exit 8   # the stamped file itself, not a re-encode
"$FF" -nostdin -y -v error -i draft_9x16.mp4 -vf scale=540:960 -c:v libx264 -crf 22 -preset fast -c:a aac -b:a 128k -movflags +faststart "$R/DRAFT - RA-06 round 1 - full ad - REVIEW 540p.mp4" || exit 9
"$FF" -nostdin -y -v error -ss 0.6 -i draft_9x16.mp4 -frames:v 1 -vf scale=540:960 $R/stills/first30.jpg
python3 page06.py --media > logs/page_d.log 2>&1 || exit 10
python3 "$SH/audio/audio_gate.py" draft_9x16.mp4 --ab "$R/audio A-B - RA-06 round 1.mp4" --untreated mix.wav.audio_untreated.json > logs/agate_d.log 2>&1; echo "audio gate exit $?"
python3 "$SH/cut/junk.py" draft_9x16.mp4 --out logs/junk_draft.json > logs/junk_d.log 2>&1; echo "junk exit $?"
python3 s25_hard.py draft_9x16.mp4 > logs/hard_d.log 2>&1; echo "hard exit $?"
echo CHAIN_D_COMPLETE
