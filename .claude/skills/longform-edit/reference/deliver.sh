set -e
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content"
mkdir -p "$D"
cp "/Volumes/Extreme/_edit_work/DELIVERY.md" "$D/README.md"
i=1
for pair in "spraytan:01 - My First Spray Tan" "zepbound:02 - My Honest Zepbound Update" "supplements:03 - The Supplements I Actually Take"; do
  s="${pair%%:*}"; name="${pair#*:}"
  mkdir -p "$D/$name"
  # no audio-gate stamp for THIS build = not deliverable (2026-09-02)
  python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/require_stamp.py" "/Volumes/Extreme/_edit_work/$s/roughcuts/FINAL_$s.mp4" || exit 1
  cp "/Volumes/Extreme/_edit_work/$s/roughcuts/FINAL_$s.mp4"          "$D/$name/"
  cp "/Volumes/Extreme/_edit_work/$s/roughcuts/FINAL_$s.srt"          "$D/$name/"
  cp "/Volumes/Extreme/_edit_work/$s/roughcuts/FINAL_$s.chapters.txt" "$D/$name/"
  cp "/Volumes/Extreme/_edit_work/$s/roughcuts/CUT_v1_graded.mp4"     "$D/$name/CUT_v1_graded_NO-GRAPHICS.mp4"
  cp "/Volumes/Extreme/_edit_work/$s/edl.json"                        "$D/$name/"
  cp "/Volumes/Extreme/_edit_work/$s/ranges.py"                       "$D/$name/"
  cp "/Volumes/Extreme/_edit_work/$s/chips.py"                        "$D/$name/"
done
echo "--- delivered ---"; ls -R "$D" | head -40; du -sh "$D"
