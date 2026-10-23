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
echo "== picture"; python3 "$R/assemble16.py" "$W/edl_film_pic.json" "$FM/_picture.mp4" --bg depth --grade warm $HF --g1 $G1 --stills 30,800,1100,1700
DUR=$(python3 -c "print($G1*1001/30000)")
"$FF" -v error -y -i "$FM/_picture.mp4" -i "$W/audio/film_voice_A.wav" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -t "$DUR" -movflags +faststart "$FM/$NAME.mp4"
cp "$FM/_picture.mp4.build.json" "$FM/$NAME.mp4.build.json"; cp "$W/audio/film_voice_A.wav.audio_untreated.json" "$FM/$NAME.mp4.audio_untreated.json"
"$FF" -v error -y -i "$FM/$NAME.mp4" -vf scale=960:540 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k -movflags +faststart "$FM/$NAME - REVIEW 540p.mp4"
"$FF" -v error -y -ss 1.5 -i "$FM/$NAME.mp4" -frames:v 1 -vf scale=960:540 -q:v 3 "$FM/$NAME.jpg"
mkdir -p "$FM/_build"; mv "$FM"/_picture* "$FM/_build/" 2>/dev/null || true
echo "== hair clearance"; python3 "$R/hairclear16.py" "$FM/$NAME.mp4" "$FM/$NAME.mp4.build.json" --skip-opaque "$W/film_manifest.json" --out "$C/hair-1080.json" --proof "$C/hair-1080-worst.jpg" | grep -E "verdict|min_top"
python3 "$R/hairclear16.py" "$FM/$NAME - REVIEW 540p.mp4" "$FM/$NAME.mp4.build.json" --upscale --skip-opaque "$W/film_manifest.json" --out "$C/hair-540.json" --proof "$C/hair-540-worst.jpg" | grep -E "verdict|min_top"
echo "== audio gate"; python3 "$A/audio/audio_gate.py" "$FM/$NAME.mp4" --ab "$FM/$NAME - audio AB.mp4" > "$C/audio_gate.log" 2>&1; tail -16 "$C/audio_gate.log"
if [ -n "$HF" ]; then echo "== graphics checks"; python3 "$A/hyperframes/checks.py" "$W/film_manifest.json" --film "$FM/$NAME.mp4" --film-t0 0 --out "$C/hf" > "$C/hf.log" 2>&1; tail -6 "$C/hf.log"; fi
V="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Videos to Review"; cp "$FM/$NAME.mp4" "$V/Celebrity Ozempic LFC R2 - first minute.mp4"
echo "R2 FM PICTURE DONE"
