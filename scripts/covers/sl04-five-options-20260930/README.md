# SL-04 five-option cover review

Dan requested the permanent five-choice mix on 2026-09-30: one pool, two studio, one enhanced video screenshot and one designer choice per video. This batch covers shorts 1, 3, 4 and 5, preserving short 2 approved B.

Review assets and prompts stay outside Git in `Short-form video content/covers/review/sl04-covers-20260930/round2-five-options/`. The directory contains `generation-prompts.json`, `manifest.json`, `quality-checks.json`, raw selected frames, generated scene plates and enhanced screenshots. Real studio cutouts are composited natively and are not repainted. Built-in image_gen did not report dollar cost.

Run `build.py` for 40 platform PNGs, `review.py` for two full sheets, four paired sheets and the gallery. Compile/use the existing `personmask.swift` tool to segment every exact output into `rendered-masks/instagram/` and `rendered-masks/youtube/`, then run `qc.py`. Mask helper: `.claude/skills/shorts/reference/recentre/personmask.swift`. Current checks pass all 40, minimum text/person clearance 49px.

Letters: A pool, B red gym studio, C blue home gym studio, D enhanced exercise screenshot, E clean editorial. Export selected files from this round only after Dan picks. No media in Git. No upload or scheduling.
