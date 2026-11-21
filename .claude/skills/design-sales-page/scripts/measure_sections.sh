#!/bin/bash
# Measure the height of every top-level section of a plain measurement page in headless Chrome.
# Usage: measure_sections.sh <measure_page.html> <out.json>
# The page must render its sections as direct children of #root, each with a data-k="<key>" attribute,
# and end with the MEASURE script from reference/round2-letter/gen.py (measure_page). Output: [[key, px], ...].
set -e
page="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1280,1000 --virtual-time-budget=15000 --dump-dom "file://$page" 2>/dev/null \
  | grep -o 'MEASURE\[.*\]END' | sed 's/MEASURE//;s/END//' > "$2"
python3 -c "
import json, sys
r = json.load(open('$2'))
assert r, 'no sections measured: check data-k attributes and the MEASURE script'
print(len(r), 'sections,', sum(h for _, h in r), 'px total')"
