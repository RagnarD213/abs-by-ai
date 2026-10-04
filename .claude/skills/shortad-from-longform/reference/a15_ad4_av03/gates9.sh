#!/bin/zsh
# gates9.sh <9x16|1x1> [cut] : plan -> audio gate (his mix, verbatim) -> watch scan + boundary strips, on the exact file.
# The watch judge and the delivery gate run afterwards (gates9b.sh), once every strip has a verdict.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
A=$1; CUT=$2; SFX=""; [ "$A" = "1x1" ] && SFX="_sq"
cd /Volumes/Extreme/_edit_work/AV-03
if [ -n "$CUT" ]; then D="cut$SFX"; V="ad4_${A}_59s.mp4"; PL="plan.json"; else D="."; V="ad4_${A}.mp4"; PL="plan$SFX.json"; fi
mkdir -p $D/logs
T=$D/transcript_words.json; [ -n "$CUT" ] && O="cut_sq/transcript_words.json" || O="transcript_words.json"
if [ ! -f $T ]; then python3 ztranscribe9.py $D/$V $T > $D/logs/transcribe$SFX.log 2>&1; tail -1 $D/logs/transcribe$SFX.log; fi
python3 plan9.py --aspect $A ${CUT:+--cut} 2>&1 | tail -1
( cd $D && python3 "$SK/audio/audio_gate.py" $V --reference-mix his_mix.wav --verbatim --ab "AB_audio_his-vs-ours_${A}${CUT:+_59s}.mp4" > logs/audio_gate$SFX.log 2>&1; tail -3 logs/audio_gate$SFX.log )
( cd $D && rm -rf watch$SFX && python3 "$SK/deliver/watch.py" $V --plan $PL --out watch$SFX --log logs/watch_pass$SFX.json > logs/watch$SFX.log 2>&1; tail -6 logs/watch$SFX.log )
echo "GATES9 $A ${CUT:-master} scan done $(date +%H:%M:%S)"
