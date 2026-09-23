#!/bin/zsh
cd /Volumes/Extreme/_edit_work/ro05
EQ='highpass=f=70,equalizer=f=110:t=q:w=1.3:g=-0.63,equalizer=f=194:t=q:w=1.3:g=+1.76,equalizer=f=316:t=q:w=1.3:g=+1.30,equalizer=f=490:t=q:w=1.3:g=-0.18,equalizer=f=735:t=q:w=1.3:g=-1.76,equalizer=f=1122:t=q:w=1.3:g=-0.84,equalizer=f=2775:t=q:w=1.3:g=+0.79,equalizer=f=3400:t=q:w=1.2:g=-1.5,equalizer=f=4387:t=q:w=1.3:g=-1.00,treble=g=+0,deesser=i=0.25:m=0.5:f=0.5:s=o'
rm -rf audio/chain
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py" --in audio/voice_raw.wav --video PICTURE.mp4 --frame-lock PICTURE.mp4 --bed audio/bed.wav --bed-db -40 --extra audio/sfx.wav --eq "$EQ" --oversample 4 --tp -4.0 --out out/RO05_r10.mp4 --work audio/chain > logs/voice_chain_r10.log 2>&1
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py" out/RO05_r10.mp4 --ab out/AB_muhammad-vs-ours.mp4 > logs/audio_gate_r10.log 2>&1
export PATH=/Volumes/Extreme/_edit_work/ro05/bin:$PATH
bin/ffmpeg -v error -y -i out/RO05_r10.mp4 -vn -ac 1 -ar 16000 audio/final16k.wav
rm -f audio/final.whisper.json; python3 tx.py audio/final16k.wav audio/final.whisper.json > audio/tx_r10.log 2>&1
python3 build_plan.py out/RO05_r10.mp4 subtitles.srt
rm -rf watch logs/watch_pass.json
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" out/RO05_r10.mp4 --plan plan.json --out watch --log logs/watch_pass.json > logs/watch_r10.log 2>&1
echo R10_ALL_DONE >> logs/watch_r10.log; echo R10_ALL_DONE >> logs/r10.done
