#!/bin/bash
# Measures every plain page in m/ with headless Chrome and writes heights.json; "shots" also saves a PNG per page.
set -e
cd "$(dirname "$0")"
rm -rf m; python3 gen.py measure m
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
echo "{" > heights.tmp
first=1
for f in m/*.html; do
  n=$(basename "$f" .html)
  w=420; case "$n" in *Desktop*) w=1200;; *Notes) w=600;; esac
  h=$("$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=$w,1000 --virtual-time-budget=15000 --dump-dom "file://$PWD/$f" 2>/dev/null | grep -o 'MEASURE\[[0-9]*\]END' | grep -o '[0-9]*')
  [ $first = 1 ] || echo "," >> heights.tmp; first=0
  echo "\"$n.dc.html\": $h" >> heights.tmp
  echo "$n $h"
  if [ "$1" = "shots" ]; then
    "$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=$w,$((h+40)) --virtual-time-budget=15000 --screenshot="$PWD/m/$n.png" "file://$PWD/$f" >/dev/null 2>&1
  fi
done
echo "}" >> heights.tmp
mv heights.tmp heights.json
