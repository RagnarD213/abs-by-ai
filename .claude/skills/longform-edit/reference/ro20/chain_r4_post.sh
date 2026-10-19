#!/bin/zsh
# RO-20 round 4 post-picture chain for one video: audio (finish-only + bed), audio gate, Whisper on the delivered audio, SRT/chapters/plan, watch pass.
# usage: chain_r4_post.sh v1 [bed_db]
setopt null_glob
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$P/Media/video_edit/bin:$PATH"
V=$1; BED=${2:--30}; W=/Volumes/Extreme/_edit_work/ro20; D=$W/round4/$V; cd $D
for f in MASTER.mp4 MASTER.mp4.* plan.json RO*.srt RO*.chapters.txt logs watch; do [ -L "$f" ] && rm "$f"; done   # links to the first pass (r4a/) for its reviewers
rm -f final.whisper.json final16k.wav; mkdir -p logs
python3 -c "import sys;sys.path.insert(0,'$P/.claude/skills/_shared');import buildcap;buildcap.wait('RO-20 R4 post $V')"
nice -n 5 python3 $W/recipe/films_r4.py audio $V $BED > logs/audio.log 2>&1 || { echo AUDIO_FAILED; tail -5 logs/audio.log; exit 1; }
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" MASTER.mp4 --ab "audio AB (reference then ours).mp4" > logs/audio_gate.log 2>&1 || echo AUDIO_GATE_NONZERO
grep -E "AUDIO GATE|FAIL" logs/audio_gate.log | cut -c1-220
[ -f final.whisper.json ] || ffmpeg -nostdin -v error -y -i MASTER.mp4 -vn -ac 1 -ar 16000 final16k.wav
[ -f final.whisper.json ] || nice -n 10 python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > logs/tx.log 2>&1 || echo TX_NONZERO
python3 $W/recipe/finish_r4.py $V > logs/finish.log 2>&1 || { echo FINISH_FAILED; tail -8 logs/finish.log; }
tail -30 logs/finish.log
rm -rf watch; python3 "$P/.claude/skills/_shared/deliver/watch.py" MASTER.mp4 --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || echo WATCH_NONZERO
tail -12 logs/watch.log
echo POST_DONE $V
