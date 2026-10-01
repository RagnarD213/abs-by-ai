# SL-05 round 2 deadlift covers

Dan rejected round 1 and explicitly requested one new AI-generated powerlifter image and two designs for each short. This replaces the original five-choice photo mix. Five new photographs reference the approved parent's straining powerlifter frame; both designs use each short's same photograph and approved copy.

Output: `Short-form video content/covers/review/sl05-covers-20261001/round2-deadlift/`

- `build.py`: twenty RGB 1080x1920 review covers, separate Instagram and YouTube layouts. A color with red X; B monochrome with prohibition mark. Source width and lower action preserved. Faces clear of warnings.
- `review.py`: paired local gallery, two platform sheets and five individual sheets with literal Instagram profile crops.
- `qc.py`: checks exact rendered files against Apple Vision accurate person masks, separate text masks, dimensions, hashes, 40px text clearance, head and action retention, safe placement and exact grid crops. Requires Pillow, NumPy and SciPy.

Run all three with Python3 from this tracked recipe directory. Apple Vision person masks are generated with `.claude/skills/shorts/reference/recentre/personmask`, excluding the separate text and warning layers for rendered files. Mask files and exact generation prompts are included in the ignored output folder. Build and QC use a path relative to this tracked script location.

All twenty passed; minimum text/person clearance72px, zero overlap. All paired and platform sheets visually inspected. Generation used five built-in imagegen calls; no dollar cost was reported and no external metered calls were used.

Dan approved A for all five shorts on 2026-10-01. `export.py` copies the exact selected review files to the final directories, verifies source and export hashes, writes the receipt and final paths document. No upload or scheduling.
