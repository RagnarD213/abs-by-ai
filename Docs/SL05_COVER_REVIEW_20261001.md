# SL-05 Stop Deadlifting cover review

Status: Dan rejected this round on 2026-10-01. Current review: [round 2 deadlift designs](SL05_COVER_REVIEW_R2_20261001.md). No final cover exports, uploads or scheduling.

25 visual options, each with separate Instagram and YouTube layouts: A pool photo, B real studio portrait on red barbell scene, C a different real studio portrait on blue safer-machine scene, D enhanced authentic approved parent-video screenshot, E clean editorial designer choice. Approved copy is identical across each short's five options. The screenshot sources are clothed; the authentic black tank top, glasses, physique and gesture are preserved. The other options show defined abs.

Local paired gallery: http://127.0.0.1:8799/

Build folder: `Short-form video content/covers/review/sl05-covers-20261001/`

Review sheets:

- `REVIEW_sl05_five-options_instagram.jpg`
- `REVIEW_sl05_five-options_youtube.jpg`

The folder includes assets, exact generation prompts, original frame candidates, source and export hashes in `manifest.json`, 50 native PNGs, phone previews, literal Instagram grid crops, five paired review sheets, and `quality-checks.json`. All 50 rendered files passed: RGB 1080x1920, two-line headline, safe type and abs placement, source hashes, exact grid crop, and Apple Vision person-mask text clearance. Minimum text/person clearance: 109px, zero overlap. Both sheets and every paired/grid sheet were visually inspected. Built-in image generation made two topic scene plates and five screenshot enhancements; it did not report a dollar cost. No external metered generation was used.

Recipe: `scripts/covers/sl05-five-options-20261001/`. Derived from the SL-04 five-option workflow. `build.py` owns both platform layouts and one copy table. `review.py` makes the gallery and review sheets; `qc.py` checks every rendered file against Apple Vision masks. Media remains local and ignored by Git.

Next: Dan chooses one letter A-E for each short 1-5. Copy those exact approved review files to `posted covers/`, their `posted covers/youtube/` twins and `approved-sl05-for-Claude/`; write the final paths and hashes to `Docs/SL05_COVER_FINALS_<date>.md`. Do not upload or schedule.
