#!/bin/bash
W=/Volumes/Expansion/_edit_work/ro28/round1; cd $W
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$P/Media/video_edit/bin:$PATH"; export GATE_GROUP=RO-28
python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS $(grep -c . logs/stills.log)"
python3 -u recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT done ($(grep -c '^context' logs/context.log)) exit $?"
python3 recipe/review_media.py verify > logs/verify.log 2>&1 || true; echo "VERIFY done"
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
echo "CHAIN C COMPLETE"
