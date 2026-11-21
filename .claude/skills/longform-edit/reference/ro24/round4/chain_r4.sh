#!/bin/bash
# RO-24 round 4: the WHOLE film (8:38) on the locked green-screen background template; then mux the approved voice (round 3's
# film_voice_r4.wav: round 3 voice A with clip inserts, Tracy retimed by retime_r4.py), 540p review copy, hair reports (main + corner), audio gate, graphics checks.
# REUSE=<earlier full render> REDO=BG12,BG19 re-composes only those background segments (README: assemble --reuse/--redo).
set -uo pipefail
R4=/Volumes/Expansion/_edit_work/RO-24/round4; R3=/Volumes/Expansion/_edit_work/RO-24/round3; R="$R4/recipe"
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; A="$P/.claude/skills/_shared"; FF="$P/Media/video_edit/bin/ffmpeg"
OUT="$R4/final"; C="$R4/checks"; mkdir -p "$OUT/_build" "$C"
NAME="${NAME:-RO24_R4_MASTER}"
REUSE_ARGS=(); [ -n "${REUSE:-}" ] && REUSE_ARGS=(--reuse "$REUSE" --redo "$REDO")
echo "== picture"; python3 "$R/assemble_r4.py" "$OUT/_build/picture.mp4" ${REUSE_ARGS[@]+"${REUSE_ARGS[@]}"} || { echo "RENDER FAILED (picture)"; exit 1; }
N=$(python3 -c "import json;print(json.load(open('$R4/edl_r4.json'))['items'][-1]['o1'])"); DUR=$(python3 -c "print($N*1001/30000)")
"$FF" -v error -y -i "$OUT/_build/picture.mp4" -i "$R4/audio/film_voice_r4b.wav" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -t "$DUR" -movflags +faststart "$OUT/$NAME.mp4" || { echo "RENDER FAILED (mux)"; exit 1; }
cp "$OUT/_build/picture.mp4.build.json" "$OUT/$NAME.mp4.build.json"
"$FF" -v error -y -i "$OUT/$NAME.mp4" -vf scale=960:540 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k -movflags +faststart "$OUT/$NAME - REVIEW 540p.mp4"
echo "== hair"; python3 "$R/hair_r4.py" "$OUT/$NAME.mp4.build.json" "$C/hair.json" "$C/hair-worst.jpg" "$OUT/$NAME.mp4" | grep -E "verdict|min_top|none_detected"
python3 "$R/hair_corner_r4.py" "$OUT/$NAME.mp4.build.json" "$C/hair_corner.json"
echo "== audio gate"; python3 "$A/audio/audio_gate.py" "$OUT/$NAME.mp4" --ab "$OUT/$NAME - audio AB.mp4" > "$C/audio_gate.log" 2>&1; tail -18 "$C/audio_gate.log"
echo "== graphics checks"; python3 "$A/hyperframes/checks.py" "$R4/film_manifest_r4.json" --film "$OUT/$NAME.mp4" --film-t0 0 --out "$C/hf" > "$C/hf.log" 2>&1; tail -8 "$C/hf.log"
ls -la "$OUT/$NAME.mp4"; echo "RENDER COMPLETE"
