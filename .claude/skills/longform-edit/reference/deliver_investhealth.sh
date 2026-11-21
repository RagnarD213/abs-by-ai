#!/bin/bash
# Deliver 04 to the project folder, keeping the prior master as *_PRE_REBUILD.
# 2026-09-03: refuses to deliver without the shared audio gate's PASS stamp; ships the stamp,
# the voice_chain sidecar, the A/B clip and the 540p review copy alongside.
set -e
export PATH=/Volumes/Extreme/_edit_work/bin:$PATH
S=/Volumes/Extreme/_edit_work/invest-health-cutdowns/style
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/04 - Why You Should Invest More In Your Health"
SHARED="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"

python3 "$SHARED/require_stamp.py" "$S/FINAL_invest_health.mp4" || { echo "NOT DELIVERABLE: no PASS stamp"; exit 1; }

# the prior master (the 53:17 v3) becomes the PRE_REBUILD copy, named after the new
# deliverable so 04 matches the convention 02 and 03 already use
[ -f "$D/INVEST_HEALTH_v3.mp4" ] && mv "$D/INVEST_HEALTH_v3.mp4" "$D/FINAL_invest_health_PRE_REBUILD.mp4"
[ -f "$D/INVEST_HEALTH_v3.srt" ] && mv "$D/INVEST_HEALTH_v3.srt" "$D/FINAL_invest_health_PRE_REBUILD.srt"
[ -f "$D/INVEST_HEALTH_v3.chapters.txt" ] && mv "$D/INVEST_HEALTH_v3.chapters.txt" "$D/FINAL_invest_health_PRE_REBUILD.chapters.txt"

cp "$S/FINAL_invest_health.mp4"                 "$D/FINAL_invest_health.mp4"
cp "$S/FINAL_invest_health.mp4.audio_gate.json" "$D/FINAL_invest_health.mp4.audio_gate.json"
cp "$S/audio/final_mix_v2.wav.voice_chain.json" "$D/FINAL_invest_health.voice_chain.json"
cp "$S/AB_his-vs-ours_invest_health.mp4"        "$D/AB_his-vs-ours_invest_health.mp4"
cp "$S/REVIEW_540p_invest_health.mp4"           "$D/REVIEW_540p_invest_health.mp4"
cp "$S/../sub30f/out/INVEST_HEALTH_sub30.srt"   "$D/FINAL_invest_health.srt"
cp "$S/chapters.txt"                            "$D/FINAL_invest_health.chapters.txt"
cp "$S/REBUILD_NOTES.md"                        "$D/REBUILD_NOTES.md"
cp "$S/spec.py"                                 "$D/spec.py"
cp "$S/inserts.json"                            "$D/inserts.json"
cp "$S/../sub30f/edl.json"                      "$D/edl.json"

# md5 the delivered master against the build source — a filename check would pass on a
# truncated copy, and this folder has been written by more than one session before
a=$(md5 -q "$S/FINAL_invest_health.mp4"); b=$(md5 -q "$D/FINAL_invest_health.mp4")
[ "$a" = "$b" ] && echo "master md5 OK $a" || { echo "MD5 MISMATCH"; exit 1; }
python3 "$SHARED/require_stamp.py" "$D/FINAL_invest_health.mp4"
ls -la "$D"
