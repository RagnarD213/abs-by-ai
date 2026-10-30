#!/bin/bash
cd /Volumes/Expansion/_edit_work/RO-29/round1
export PATH="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 recipe/stills.py > logs/stills.log 2>&1
python3 -u recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT exit $? ($(ls review/context | grep -c 540p))"
python3 recipe/review_media.py verify > logs/verify.log 2>&1; echo "VERIFY exit $?"
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
