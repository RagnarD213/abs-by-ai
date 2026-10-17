#!/bin/bash
# RA-07 round 6 stage 2: assemble with O1 real -> first-30 identity -> cuts -> mux -> audio gate -> chips -> checks -> negative sheet
set -e
cd /Volumes/Extreme/_edit_work/ra07
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FP="${FF%ffmpeg}ffprobe"
S="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
M="round6/deliver/fire your trainer | claude | 9x16 | RA-07.mp4"
mkdir -p round6/deliver/logs round6/logs
python3 -c "
import sys; sys.path.insert(0,'$S')
import buildcap; buildcap.wait('ra07 r6s2 assemble')"
python3 s86r6_assemble.py work
echo WORK_DONE
"$FF" -v error -i round6/work/picture_9x16.mp4 -frames:v 903 -f framemd5 - | grep -v "^#" | awk -F, '{print $6}' > round6/r6.md5
cmp -s round6/r6.md5 round3/r2.md5 && echo "FIRST30 IDENTICAL" || echo "FIRST30 DIFFERS"
python3 s86r6_assemble.py cuts
echo CUTS_DONE
rm -f "$M".*.json; rm -rf round6/deliver/watch round6/deliver/logs/watch_pass.json round6/deliver/logs/findings.json
"$FF" -nostdin -y -v error -i round6/work/picture_9x16.mp4 -i round3/mix_bass_r3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart "$M"
"$FP" -v error -count_frames -show_entries stream=codec_name,nb_read_frames -of compact "$M"
shasum -a 256 "$M" | cut -c1-16
python3 "$S/audio/audio_gate.py" "$M" --ab "round6/deliver/fire your trainer | AB audio ref-vs-ours 9x16 | RA-07.mp4" --untreated mix_bass.wav.audio_untreated.json 2>&1 | tail -3 || true
python3 s92r6_chips.py | tail -3
python3 s92r6b_k1push.py
PLAN=beats_r6.json PIC=round6/work/picture_9x16.mp4 python3 s88r6_checks.py 2>&1 | tail -3
"$FF" -nostdin -y -v error -i "$M" -vf "fps=40/52.686,scale=216:384,tile=10x4" -frames:v 1 round6/neg_v6.jpg
echo CHAIN_S2_DONE
