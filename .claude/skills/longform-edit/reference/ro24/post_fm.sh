#!/bin/bash
# RO-24 round 1 checks on the exact first-minute export (after chain_fm.sh)
set -uo pipefail
W=/Volumes/Expansion/_edit_work/RO-24/round1; R="$W/recipe"; FM="$W/review/first-minute"; NAME="DRAFT - RO-24 round 1 - first minute"; C="$W/checks"
A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
echo "== hair clearance, 1080p and 540p"
python3 "$R/hairclear16.py" "$FM/$NAME.mp4" "$FM/$NAME.mp4.build.json" --out "$C/hair-1080.json" --proof "$C/hair-1080-worst.jpg" | tail -12
python3 "$R/hairclear16.py" "$FM/$NAME - REVIEW 540p.mp4" "$FM/$NAME.mp4.build.json" --upscale --out "$C/hair-540.json" --proof "$C/hair-540-worst.jpg" | grep -E "verdict|min_top"
echo "== audio gate"
python3 "$A/audio/audio_gate.py" "$FM/$NAME.mp4" --ab "$FM/$NAME - audio AB.mp4" > "$C/audio_gate.log" 2>&1; tail -18 "$C/audio_gate.log"
echo "== lower-third checks"
python3 "$A/hyperframes/checks.py" "$W/hf/manifest.json" --film "$FM/$NAME.mp4" --film-t0 0 --out "$C/hf" > "$C/hf.log" 2>&1; tail -6 "$C/hf.log"
echo "== context stills and the VLC copy"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real"
"$FF" -v error -y -ss 32.6 -i "$FM/$NAME.mp4" -frames:v 1 -q:v 2 "$W/review/context/G01.jpg"
"$FF" -v error -y -ss 57.2 -i "$FM/$NAME.mp4" -frames:v 1 -q:v 2 "$W/review/context/G02.jpg"
V="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Videos to Review"; mkdir -p "$V"; cp "$FM/$NAME.mp4" "$V/Celebrity Ozempic LFC R1 - first minute.mp4"
echo "POST FM DONE"
