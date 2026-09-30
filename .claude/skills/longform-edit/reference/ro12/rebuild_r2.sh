#!/bin/zsh
# RO-12 round 2 (after independent review r1): picture -> master -> audio B (fitted EQ) -> audio gate -> transcript -> SRT/plan ->
# graphic-free BASE -> watch pass. Every step writes into out/; old picture chunks are cleared first.
set -e
export PATH=/Volumes/Extreme/_edit_work/ro12/bin:$PATH
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; FF="$P/Media/video_edit/bin/ffmpeg"
W=/Volumes/Extreme/_edit_work/ro12; cd $W/recipe
rm -f $W/out/chunks/PICTURE_* $W/out/chunks/BASE_* $W/out/PICTURE.mp4 $W/out/BASE.mp4 $W/out/MASTER.mp4* $W/out/FINAL.mp4*
python3 build.py timeline > $W/logs/timeline_r2.log
python3 build.py picture > $W/logs/picture_r2.log 2>&1; echo PICTURE_DONE
cd $W/out
"$FF" -v error -y -i PICTURE.mp4 -map 0:v -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart MASTER.mp4
echo MASTER_DONE
python3 ../recipe/build.py audio MASTER.mp4 FINAL > $W/logs/audio_r2.log 2>&1
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" FINAL.mp4 --untreated FINAL.mp4.audio_untreated.json --ab AB_muhammad-vs-ours.mp4 > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log
"$FF" -v error -y -i FINAL.mp4 -vn -ac 1 -ar 16000 final16k.wav
python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > /dev/null 2>&1
echo TX_DONE
python3 ../recipe/finish.py FINAL.mp4
(cd ../recipe && RO12_BASE=1 python3 build.py picture --name BASE > $W/logs/base_r2.log 2>&1)
echo BASE_DONE
rm -rf watch logs/watch_pass.json
python3 "$P/.claude/skills/_shared/deliver/watch.py" FINAL.mp4 --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || true
tail -12 logs/watch.log
echo CHAIN_DONE
