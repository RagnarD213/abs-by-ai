#!/bin/zsh
# post.sh S : deliver + hair + cut scan + fresh watch pass + junk on the delivered file
S=$1; cd /Volumes/Expansion/_edit_work/SL-10
N=$(python3 -c "import plans;print(plans.NAME['$S'])"); V="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/alcohol-$N.mp4"
python3 deliver.py copy $S 2>&1 | grep -E "GATE|plan "
python3 hairv.py $S "$V" 2>&1 | tail -1; python3 scan.py $S 2>&1 | grep frames
rm -rf build/$S/gate/watch build/$S/gate/findings.json
zsh runwatch.sh $S; python3 deliver.py plan $S > /dev/null 2>&1
python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/cut/junk.py" "$V" > build/$S/gate/junk_run.log 2>&1
echo "POST $S $(tail -1 build/$S/gate/watch_run.log)"
