#!/bin/zsh
# RO-21 round 3 master: join the picture chunks (same encoder settings, stream copy), mux the round 3 mix (voice A + bed),
# audio gate, Whisper on the delivered audio, finish (SRT + plan), watch pass scan. Judging and the gate follow.
set -e
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"; export PATH="$P/Media/video_edit/bin:$PATH"; export GATE_GROUP=RO-21
B=/Volumes/Expansion/_edit_work/RO-21; O=$B/round3/final; M=$O/RO21_MASTER.mp4; mkdir -p $O/logs
cd $B/round3/film
rm -f list.txt; for k in 0 1 2 3 4 5 6; do echo "file 'chunk$k.mp4'" >> list.txt; done
[ -f $O/picture.mp4 ] || ffmpeg.real -v error -y -f concat -safe 0 -i list.txt -c copy $O/picture.mp4
cp $O/picture.build.json $M.build.json   # written by splice_r3.sh (chunks + label-fix patches)
ffmpeg.real -v error -y -i $O/picture.mp4 -i $B/audio/film/film_mix_r3d.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart $M
echo "MASTER $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 $M | head -1) frames"
cp $B/audio/film/film_mix_r3d.wav.audio_untreated.json $M.audio_untreated.json; cp $B/audio/film/film_mix_r3d.wav.voice_chain.json $M.voice_chain.json
cd $O
python3 "$SH/audio/audio_gate.py" $M --untreated $M.audio_untreated.json --ab "RO-21 audio AB vs reference.mp4" > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log || true
ffmpeg.real -v error -y -i $M -vn -ac 1 -ar 16000 final16k.wav
python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > logs/tx.log 2>&1; echo TX_DONE
python3 $B/recipe/finish_r3.py $M > logs/finish.log 2>&1; tail -2 logs/finish.log
python3 "$SH/deliver/watch.py" $M --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || true
tail -5 logs/watch.log
echo MASTER_CHAIN_DONE
