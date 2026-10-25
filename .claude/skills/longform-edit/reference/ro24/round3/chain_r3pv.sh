#!/bin/bash
# RO-24 round 3 preview: the first 2:50 (intro, Sharon Osbourne with her E! News clip, into Fat Joe with his Page Six clip)
# on the shared green-screen background template; then the 540p copy, hair report, audio gate, graphics checks, VLC copy.
set -uo pipefail
R3=/Volumes/Expansion/_edit_work/RO-24/round3; R="$R3/recipe"; A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; PV="$R3/review/preview"; C="$R3/checks"
mkdir -p "$PV/_build" "$C"
NAME="DRAFT - RO-24 round 3 - first 2m50s"; G1=${G1:-5111}     # ends after "...he admitted that he used weight loss medication." (G03 out)
REUSE_ARGS=(); [ -n "${REUSE:-}" ] && REUSE_ARGS=(--reuse "$REUSE" --redo "$REDO")     # REUSE=<earlier picture> REDO=BG03,BG05: compose only those again
echo "== picture"; python3 "$R/assemble_r3.py" "$PV/_build/picture.mp4" --g1 $G1 --stills 300,560,1700,2350,2700,3050,3500,3870,4120,4980 "${REUSE_ARGS[@]}" || { echo "RENDER FAILED (picture)"; exit 1; }
DUR=$(python3 -c "print($G1*1001/30000)")
"$FF" -v error -y -i "$PV/_build/picture.mp4" -i "$R3/audio/film_voice_r3.wav" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -t "$DUR" -movflags +faststart "$PV/$NAME.mp4"
cp "$PV/_build/picture.mp4.build.json" "$PV/$NAME.mp4.build.json"
"$FF" -v error -y -i "$PV/$NAME.mp4" -vf scale=960:540 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k -movflags +faststart "$PV/$NAME - REVIEW 540p.mp4"
"$FF" -v error -y -ss 7.0 -i "$PV/$NAME.mp4" -frames:v 1 -vf scale=960:540 -q:v 3 "$PV/$NAME.jpg"
echo "== hair"; python3 "$R/hair_r3.py" "$PV/$NAME.mp4.build.json" "$C/hair.json" "$C/hair-worst.jpg" "$PV/$NAME.mp4" | grep -E "verdict|min_top"
echo "== audio gate"; python3 "$A/audio/audio_gate.py" "$PV/$NAME.mp4" --ab "$PV/$NAME - audio AB.mp4" > "$C/audio_gate.log" 2>&1; tail -16 "$C/audio_gate.log"
echo "== graphics checks"; python3 "$A/hyperframes/checks.py" "$R3/film_manifest_r3.json" --film "$PV/$NAME.mp4" --film-t0 0 --out "$C/hf" > "$C/hf.log" 2>&1; tail -8 "$C/hf.log"
V="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Videos to Review"; cp "$PV/$NAME.mp4" "$V/Celebrity Ozempic LFC R3 - first 2m50s.mp4"
echo "RENDER COMPLETE"
