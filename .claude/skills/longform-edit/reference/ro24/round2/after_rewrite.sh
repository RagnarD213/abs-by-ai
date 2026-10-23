#!/bin/bash
# RO-24 round 2 first minute (film frames 0-1889 of the whole-film timeline): the approved DS-40 Claude R2 key (RIM 4 for this
# roll), warm, depth background, Dan's voice A, the round 2 graphics. Then checks, key comparisons and the measure of the keys.
set -uo pipefail
W=/Volumes/Expansion/_edit_work/RO-24/round2; R="$W/recipe"; D="$R/ds40key"; A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FM="$W/review/first-minute"; C="$W/checks"
mkdir -p "$FM" "$W/review/key" "$W/review/context" "$C"
NAME="DRAFT - RO-24 round 2 - first minute"; G1=1884   # ends after "overdosing." (source 18424, as round 1)
python3 "$R/pic_edl.py"
python3 -c "import json; M=json.load(open('$W/hf/manifest.json'))+json.load(open('$W/broll/broll_manifest.json')); json.dump(M,open('$W/film_manifest.json','w'),indent=1)"
HF="--hf $W/film_manifest.json"
echo "== swap in the v2 plates (faint-speck rule), old ones kept in key/v1"
mkdir -p $W/key/v1
for f in $W/key/v2/*.mkv; do n=$(basename $f); [ -f $W/key/$n ] && mv $W/key/$n $W/key/v1/ && mv $W/key/$n.json $W/key/v1/; mv $f $W/key/; mv $f.json $W/key/; done
ls $W/key/*.mkv | wc -l
bash "$R/chain_r2fm_pic.sh"
echo "== key comparisons (round 1 key | round 2 key)"
python3 "$R/compare_r2.py" 9.0 21.0 "$W/review/key/compare-hook.mp4"
python3 "$R/compare_r2.py" 38.5 45.0 "$W/review/key/compare-hands-0m40.mp4" --zoom
python3 "$R/compare_r2.py" 47.2 53.0 "$W/review/key/compare-hands-0m51.mp4" --zoom
python3 "$R/compare_r2.py" 24.0 27.0 "$W/review/key/compare-shorts-0m25.mp4" --zoom
for f in "$W"/review/key/compare-*.mp4; do "$FF" -v error -y -ss 1.0 -i "$f" -frames:v 1 -q:v 3 "${f%.mp4}.jpg"; done
echo "== measures on the four first-minute keys (pale, navy renders; rim, see-through, specks, motion-free flicker)"
mkdir -p "$C/keys"
for spec in R01:16084:793 R02:17081:527 R03:17635:210 R04a:17942:676; do k=${spec%%:*}; r=${spec#*:}; f0=${r%%:*}; n=${r#*:}
  python3 "$D/render16.py" "$W/key/$k.mkv" 0 $n "$C/keys/$k" pale,navy,pink | tail -1
  python3 "$D/measure16.py" "$C/keys/$k pale.mp4" "$C/keys/$k navy.mp4" "$C/keys/m_$k.json" $f0 $n | tail -1
  python3 "$D/mcflicker16.py" "$C/keys/$k pale.mp4" "$C/keys/mc_$k.json" $f0 $n 2>/dev/null | tail -1
done
python3 "$R/ctx_r2.py"
echo "AFTER REWRITE DONE"
