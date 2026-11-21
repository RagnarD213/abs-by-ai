#!/bin/zsh
# ./deliver.sh F short2_do-this-before-you-take-your-shirt-off
# copy build -> delivery name, audio gate (verbatim vs his same cut), delivered-audio ASR + CTC, plan.
set -e
cd "${0:A:h}"
S=$1; NAME=$2; l=${S:l}
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
D="$P/Short-form video content"; V="$D/arms-shoulders-$NAME.mp4"
FF="$P/Media/video_edit/bin/ffmpeg"
setopt NULL_GLOB; rm -f "$V" "$V".*.json
cp out/${l}_*.mp4 "$V"
nice python3 "$P/.claude/skills/_shared/audio/audio_gate.py" "$V" --reference-mix build/$S/his_mix.wav --verbatim \
  --ab "$D/AB_his-vs-ours_arms-shoulders-$NAME.mp4" | grep -E "AUDIO GATE"
"$FF" -nostdin -v error -y -i "$V" -vn -ac 1 -ar 16000 -c:a libmp3lame -b:a 64k gate/${S}_deliv.mp3
node ../whisper_words.js gate/${S}_deliv.mp3 gate/${S}_asr.json
python3 gate/ctc_delivered.py $S "$V" 2>&1 | grep -v -i warn | tail -2
mkdir -p gate/$S
"$FF" -v error -y -i "$V" -vf "fps=1,scale=160:-2,tile=12x5" -frames:v 1 gate/$S/neg.jpg
python3 make_plan.py $S "$V"
echo "$V"
