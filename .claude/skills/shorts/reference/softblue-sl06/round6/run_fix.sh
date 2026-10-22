#!/bin/bash
# fix/run_fix.sh S TAKE [static boxes...]: vial label restore (+ background statics) from the corrected R6 frame; no face patching
cd /Volumes/Extreme/_edit_work/sl06/round6
S=$1; T=$2; shift 2
N=$(python3 -c "print({'A':99,'B':111,'C':68,'D':79,'E':76,'F':60}['$S'])")
VL=$(python3 -c "import json;d=json.load(open('labels_h.json'))['$S'];print(','.join(map(str,d['vial']))+':'+','.join(map(str,d['label'])))")
ST=""; for b in "$@"; do ST="$ST --static $b"; done
python3 fix/fix_take.py veo/$T.mp4 frames/${S}_r6h.jpg fix/${S}_intro.mp4 --frames ${OFF:-0}:$((${OFF:-0}+N-1)) --seconds $(python3 -c "print($N/24)") --vial $VL $ST --log fix/${S}_fix.json
