#!/bin/bash
# RO-37 round 1 first-minute draft: base picture -> voice A (approved pool-set voice) -> HyperFrames overlays + audio.
set -e
W=/Volumes/Expansion/_edit_work/RO-37/round1; R=$W/recipe; FM=$W/review/first-minute; T1=61.0944
FF="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
rm -rf $FM/base.mp4.segs; python3 $R/build.py range 0 $T1 $FM/base.mp4
python3 - <<PY
import wave
w = wave.open("$W/assembled_untreated.wav"); sr = w.getframerate(); n = round($T1 * sr)
o = wave.open("$FM/voice_raw.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(w.readframes(n)); o.close()
PY
cd $R && python3 -c "import build as B; B.voice('$FM/voice_raw.wav', '$FM/voice_A.wav', 'A')"
python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/composite.py" $W/hf/manifest.json --base $FM/base.mp4 --base-t0 0 --out "$FM/DRAFT - First Time At The Gym R1 - first minute.mp4" --audio $FM/voice_A.wav
"$FF" -nostdin -v error -y -i "$FM/DRAFT - First Time At The Gym R1 - first minute.mp4" -vf scale=960:540 -c:v libx264 -crf 23 -c:a aac -b:a 160k -movflags +faststart "$FM/DRAFT - First Time At The Gym R1 - first minute - REVIEW 540p.mp4"
echo FIRST_MINUTE_DONE
