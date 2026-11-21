# How To Do Chest Flies On SFC R1 (DS-78): editor notes

CONTENT (SFC). Delivered 2026-11-07 for Dan's review; not approved, uploaded or scheduled.
Master: review/How To Do Chest Flies On SFC R1 - 1080p.mp4, sha256 d12e90f5664bb785b9f288010bc022f154e1acbb304d1c9db44fae1dae67697d, 51.45 s, 1080x1920.
Page: http://127.0.0.1:9708/ (review_server, port 9708). VLC copy: Videos to Review/How To Do Chest Flies On SFC R1 - complete Short.mp4.

- Build = DS-77 T-Bar Rows R1 recipe (same roll C1882): colour F, voice B Fuller Bass, Original Portrait (Dan's DS-77 picks), options F/E/B, A-D, 1-3 on the page.
- Takes (C1882 s): 268.75-278.75, 280.67-293.80, 297.45-300.10, 304.25-314.30, 317.85-333.45; reasons in recipe/prepare.py. Listener (Gemini 3.1 Pro, 2/2) chose seat join X, "low risk" read 2, ad-lib read 2. Ad-lib "As far back as you can go, but no farther" kept and disclosed.
- Clips: B0665-B0668 only (visual plan records/visual-plan.json). Windows, not full screen: a 9:16 crop cuts both hands at the stretch. No seat-setting or starting-position close-up exists in rolls C1844-C1846 (excluded-source-ranges.json); B0691/B0692 are the rear-delt machine. B03 = 1.05 s (B0666 head leaves the top after 7.1 s). B04 avoids B0668 4.0-5.3 (hands off handles). Open-palm presses are his technique.
- Fixes before Dan: "f-For" join (P4 end 314.48 -> 314.30), clipped final "s" (P5 end + 80 ms fade), G01 copy echoed speech then wrapped too low, G03 raised to top_y 1590 (build.py now takes per-graphic top_y and keeps captions 55 px above the bar).
- Reviews: independent r1 DOES NOT SHIP -> re-review 2 SHIP (evidence/independent/ROUND-1-REVIEW.md). Watch judge 43/43 images, 0 defects.
- Gate 2.6.3: 35/39; open framing:no_wide_level, framing:push_coverage, captions:burned, captions:sync (same 4 as approved DS-77/DS-76). Audio: verbatim of voice-selected.wav PASS; reference gate fails only the known tone row (bass lift).
- Spend: about $0.10 (Gemini listens). No AI clips or images.
- Lesson for shorts skill (on approval): for fly-type exercises (arms wide) a 9:16 full-screen crop loses the hands; plan windows from the start. Prefer one ffmpeg pass with fps= over per-frame select calls for strip sheets (per-frame select timed out).
