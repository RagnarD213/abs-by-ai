#!/bin/zsh
# gates9b.sh <9x16|1x1> [cut] : after the watch judge wrote findings -> fold it in, rebuild the plan (same sha), run THE gate.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
A=$1; CUT=$2; SFX=""; [ "$A" = "1x1" ] && SFX="_sq"; FMT="ad9x16"; [ "$A" = "1x1" ] && FMT="ad1x1"
cd /Volumes/Extreme/_edit_work/AV-03
if [ -n "$CUT" ]; then D="cut$SFX"; V="ad4_${A}_59s.mp4"; PL="plan.json"; else D="."; V="ad4_${A}.mp4"; PL="plan$SFX.json"; fi
python3 plan9.py --aspect $A ${CUT:+--cut} 2>&1 | tail -1
( cd $D && python3 "$SK/deliver/gate.py" $V --format $FMT --plan $PL > logs/gate$SFX.log 2>&1; grep -E "FAIL|NOT MEASURED|UNCONFIGURED|NEEDS|VERDICT|verdict|PASS " logs/gate$SFX.log | tail -40 )
echo "GATE $A ${CUT:-master} done $(date +%H:%M:%S)"
