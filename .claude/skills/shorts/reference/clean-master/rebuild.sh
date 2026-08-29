#!/bin/bash
# Full rebuild on the corrected (container) timeline. Ordered so each step's inputs exist.
set -e
cd "$(dirname "$0")"
echo "== preflight =="            && python3 work/preflight.py
echo "== words =="                && python3 work/mkwords.py work/whisper-a.json work/words.json
echo "== speech gaps (vad) =="    && python3 work/vad.py work/audio48k.wav work/gaps_vad.json
echo "== gaps (intersected) =="   && python3 work/gaps.py
echo "== word onsets =="          && python3 work/fixonsets.py
echo "== segments =="             && REPORT=1 node segments.js
echo "== shots =="                && node detect-shots.js
echo "== crops =="                && python3 work/mkcrops.py
echo "== plan =="                 && python3 work/mkplan.py && node plan.js
echo "== captions =="             && node captions.js
echo "== assets =="               && python3 build-assets.py > /dev/null && echo "assets ok"
echo "== render =="               && node render.js
echo "== audio finish =="         && python3 finishaudio.py
echo "DONE"
