#!/bin/zsh
# wait until fewer than 2 OTHER video builds run (00-RULES machine cap), then build
cd "${0:A:h}"
while true; do
  n=$(ps -Ao command | grep -E 'gate\.py|render\.(py|js)|whisper|qc_style|ffmpeg .*-(c:v|f rawvideo)' | grep -v -E 'grep|sl04' | awk '{print $0}' | grep -c -E 'gate\.py|render\.|whisper|qc_style')
  [ "$n" -lt 2 ] && break
  sleep 30
done
date; ./build.sh "$@" 2>&1 | tail -20; date
