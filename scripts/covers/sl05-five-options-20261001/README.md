# SL-05 cover recipe

Five visual choices for each of five shorts, in two platform layouts. Review only until Dan picks.

Run from the project root with Python 3, Pillow, NumPy and SciPy installed:

1. `python3 scripts/covers/sl05-five-options-20261001/build.py`
2. Run `.claude/skills/shorts/reference/recentre/personmask` on each platform's 25 rendered PNGs, excluding `.text-mask.png`, into `rendered-masks/<platform>/` in the review folder.
3. `python3 scripts/covers/sl05-five-options-20261001/qc.py`
4. `python3 scripts/covers/sl05-five-options-20261001/review.py`

Assets and generation prompts live in the ignored review folder. Studio cutouts are original real photo pixels. Screenshot enhancement used built-in image generation. No upload or scheduling code. See `Docs/SL05_COVER_REVIEW_20261001.md`.
