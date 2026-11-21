#!/bin/zsh
# RO-08 round 3, third render: the post-render chain for a render that differs from an already chained one only inside one AI clip.
# Runs on the exact master: audio gate, SRT/chapters/plan (finish08.py), watch pass. Reused from the second render's chain, and only if the
# decoded sound is bit for bit the same: the finished-film transcript (final.whisper.json), the dense hair check (qc/hair.json: talking-head
# frames, none of which changed) and the graphics checks (checks/: lower thirds, none of which changed). r3_carry.py proves which frames changed.
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro08/round3
M="RO-08 round 3 - full film.mp4"
mkdir -p logs
A=$(ffmpeg -nostdin -v error -i "$M" -vn -f s16le -ac 2 - | md5); B=$(ffmpeg -nostdin -v error -i "render2/$M" -vn -f s16le -ac 2 - | md5)
echo "decoded audio md5: this $A  second render $B"
[ "$A" = "$B" ] || { echo AUDIO_DIFFERS_RUN_THE_FULL_CHAIN; exit 1; }
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" "$M" --untreated "$M.audio_untreated.json" --ab "RO-08 audio AB (reference then ours).mp4" > logs/audio_gate.log 2>&1 || echo AUDIO_GATE_NONZERO
grep -E "AUDIO GATE|FAIL" logs/audio_gate.log
python3 ../recipe/finish08.py "$M" > logs/finish.log 2>&1 || { echo FINISH_FAILED; tail -5 logs/finish.log; }
tail -3 logs/finish.log
python3 "$P/.claude/skills/_shared/deliver/watch.py" "$M" --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || echo WATCH_NONZERO
grep -E "naked|graphics present|frozen|black" logs/watch.log || true
cp render2/logs/hair.log render2/logs/checks.log logs/ 2>/dev/null
echo CHAIN_DONE
