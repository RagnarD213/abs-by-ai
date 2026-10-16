#!/bin/bash
# RO-18 round 1, after the re-check: re-render the blocks holding P01, G04, G16, G19, G28, P02 and their neighbours, then checks and page.
W=/Volumes/Extreme/_edit_work/RO-18/round1; cd $W
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$P/Media/video_edit/bin:$PATH"
slot() { (cd "$P" && python3 -c "import sys; sys.path.insert(0,'.claude/skills/_shared'); import buildcap; buildcap.wait('RO-18 $1', quiet=True)"); }
python3 recipe/stills.py G28 > logs/stills_fix2.log 2>&1; echo "STILL G28 $?"
rm -f review/blocks/blk_03.mp4* review/blocks/blk_06.mp4* review/blocks/blk_08.mp4* review/blocks/blk_10.mp4* review/blocks/blk_11.mp4*
rm -rf review/blocks/blk_03.mp4.work review/blocks/blk_06.mp4.work review/blocks/blk_08.mp4.work review/blocks/blk_10.mp4.work review/blocks/blk_11.mp4.work
IDS="G03 G04 G05 C06 G06 C07 T2 C08 C09 C10 C11 C12 G07 C45 G08 C13 C14 G10 G11 T3 C15 C16 C17 C18 G12 C19 C20 C21 G13 G16 G17 C26 T5 C27 G18 C28 C29 G19 G20 C31 C32 C34 C38 G22 A8 C40 C41 G23 P01 C42 C43 P02 G25 A9 G27 G28"
slot context; nice -n 5 python3 -u recipe/review_media.py context_all $IDS > logs/context_fix.log 2>&1; echo "CONTEXT done ($(grep -c '^context' logs/context_fix.log)) exit $?"
python3 recipe/review_media.py verify > logs/verify.log 2>&1 || true; echo "VERIFY $(grep -c PASS logs/verify.log) pass, $(grep -vc PASS logs/verify.log) other"
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; echo "EXTRA $(tail -1 logs/page_extra.log)"; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
echo "CHAIN D COMPLETE"
