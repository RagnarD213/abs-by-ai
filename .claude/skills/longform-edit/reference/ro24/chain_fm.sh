#!/bin/bash
# RO-24 round 1: first minute + look options + key comparisons, after K1-K3 and the two lower thirds exist. Run as ONE queued step:
#   renderq.py run --group RO-24 -- bash recipe/chain_fm.sh
set -euo pipefail
W=/Volumes/Expansion/_edit_work/RO-24/round1; R="$W/recipe"; FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FM="$W/review/first-minute"; mkdir -p "$FM" "$W/review/key" "$W/review/look" "$W/review/context" "$W/review/voice" "$W/checks"
NAME="DRAFT - RO-24 round 1 - first minute"
echo "== picture"
python3 "$R/assemble16.py" "$W/edl_fm.json" "$FM/_picture.mp4" --bg depth --grade warm --hf "$W/hf/manifest.json" --stills 30,800,1100,1700
echo "== mux voice B (already finished by the shared chain; padded/trimmed to the picture)"
DUR=$(python3 -c "import json;print(json.load(open('$FM/_picture.mp4.build.json'))['frames']*1001/30000)")
"$FF" -v error -y -i "$FM/_picture.mp4" -i "$W/audio/fm_voice_B.wav" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -af apad -t "$DUR" -movflags +faststart "$FM/$NAME.mp4"
cp "$FM/_picture.mp4.build.json" "$FM/$NAME.mp4.build.json"
echo "== review copy"
"$FF" -v error -y -i "$FM/$NAME.mp4" -vf scale=960:540 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k -movflags +faststart "$FM/$NAME - REVIEW 540p.mp4"
"$FF" -v error -y -ss 1.5 -i "$FM/$NAME.mp4" -frames:v 1 -vf scale=960:540 -q:v 3 "$FM/$NAME.jpg"
echo "== context clips for the two lower thirds (3 s either side)"
for spec in G01:23.55:37.62 G02:49.62:60.88; do id=${spec%%:*}; r=${spec#*:}; a=${r%:*}; b=${r#*:}
  "$FF" -v error -y -ss "$a" -to "$b" -i "$FM/$NAME.mp4" -vf scale=960:540 -c:v libx264 -crf 21 -preset medium -c:a aac -b:a 160k -movflags +faststart "$W/review/context/$id-context - REVIEW 540p.mp4"
done
echo "== look options"
python3 "$R/options16.py" "$W/key/fm/K1_refined.mkv" 420 "$W/review/look"
echo "CHAIN FM DONE"
