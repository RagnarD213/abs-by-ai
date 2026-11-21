#!/bin/bash
# Two-build cap (VIDEO-RULES): wait until fewer than two other builds run. usage: wait_slot.sh [max_minutes]
MAX=${1:-45}; n=0
while :; do
  c=$(ps -Ao command | grep -E 'deliver/gate\.py|deliver/watch\.py|from_plan\.py|sq_render\.py|square_chain\.py|kit_deliver|asr_assembled|whisper|review_media\.py|build\.py range|finish_chain|qc_style' | grep -v -E 'grep|ro02|wait_slot' | wc -l | tr -d ' ')
  [ "$c" -lt 2 ] && { echo "slot free ($c other builds) after ${n} min"; exit 0; }
  [ "$n" -ge "$MAX" ] && { echo "TIMEOUT: still $c other builds after ${n} min"; exit 1; }
  sleep 60; n=$((n+1))
done
