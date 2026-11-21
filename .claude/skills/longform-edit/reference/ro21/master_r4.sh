#!/bin/zsh
# RO-21 round 4 master: spliced picture + round 3's approved mix (audio unchanged), audio gate, finish (same transcript, so the same SRT), watch scan.
set -e
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"; export PATH="$P/Media/video_edit/bin:$PATH"; export GATE_GROUP=RO-21
B=/Volumes/Expansion/_edit_work/RO-21; O=$B/round4/final; M=$O/RO21_MASTER.mp4; mkdir -p $O/logs
cp $O/picture.build.json $M.build.json
ffmpeg.real -v error -y -i $O/picture.mp4 -i $B/audio/film/film_mix_r3d.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart $M
echo "MASTER $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 $M | head -1) frames"
cp $B/audio/film/film_mix_r3d.wav.audio_untreated.json $M.audio_untreated.json; cp $B/audio/film/film_mix_r3d.wav.voice_chain.json $M.voice_chain.json
cd $O
python3 "$SH/audio/audio_gate.py" $M --untreated $M.audio_untreated.json --ab "RO-21 audio AB vs reference.mp4" > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log || true
cp $B/round3/final/final.whisper.json .
python3 $B/recipe/finish_r3.py $M > logs/finish.log 2>&1; tail -2 logs/finish.log
cmp RO21.srt $B/round3/final/RO21.srt && echo SRT_SAME
python3 "$SH/deliver/watch.py" $M --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || true
tail -3 logs/watch.log
ffmpeg -v error -y -i $M -vf scale=960:540 -c:v libx264 -crf 24 -preset medium -c:a aac -b:a 128k -movflags +faststart "RO-21 round 4 - full film - REVIEW 540p.mp4"
ffmpeg -v error -y -i "RO-21 round 4 - full film - REVIEW 540p.mp4" -t 62 -c copy -movflags +faststart first-minute-540p.mp4
echo MASTER_R4_DONE
