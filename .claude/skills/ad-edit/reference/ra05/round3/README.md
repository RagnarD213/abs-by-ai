# RA-05 round 3 (2026-10-14): the couch clip moving, the body scan rebuilt vertical, the whole 9:16

Work dir `/Volumes/Extreme/_edit_work/ra05/round3/` (a copy of round 2's; round 2's page `round2/review/` is untouched). Review page
`round3/review/` (served by `_shared/review_server.py`). Files here differ from `../round2/`; everything else is round 2's.

## Order (run in the work dir)

| # | command | makes |
|---|---|---|
| 1 | `python3 gen_couch.py A <tag>`, `python3 gen_couch.py B <tag>` (prompts `motion/A.txt`, `B.txt`, `*.neg.txt`) | Veo 3.1 Fast takes from the approved frames, hashes asserted, `motion/ledger.json`, $10 cap enforced |
| 2 | `python3 lockscreen.py motion/A2.mp4 motion/A2_locked.mp4 60 motion/A2_lock.json` (and B5) | the phone picture held still |
| 3 | `python3 s06_couch3.py` | `cards_9x16/couch.mp4`: A2 0 to 2.30 s, CUT, B5 0 to 2.14 s, AI chip |
| 4 | `python3 scan3/fit_paths.py`, `python3 s06_scan3.py` (`still T` for a single frame) | `cards_9x16/scan.mp4`: the vertical scan with four Soft Blue notes |
| 5 | `python3 s05_plan05.py` | `beats.json` without the B0435 poses cutaway |
| 6 | `python3 s10_render05.py 9x16`, mux with `mix.wav` (unchanged, same 1,749 frames) | `draft_9x16.mp4` |
| 7 | `python3 check3/selfchange.py cards_9x16/couch.mp4 couch "[[0,68],[69,132]]"` | the self-change map per shot |
| 8 | `python3 page_r3.py --media` | the round 3 page |

## What this round taught

1. **Veo animates a photo on a phone screen like a live photo, every take**, even with "a still photograph, frozen like a printed
   picture" in the prompt and "video playing on the phone" in the negative: the face on the screen smiles, turns, or becomes another
   face. Fix it in code, not with retakes: `lockscreen.py` tracks the phone against FRAME 0 in every frame (SIFT + RANSAC homography,
   a similarity transform when the homography jumps, ECC refinement kept only when it agrees within 3 px), smooths the four corners
   over time, and lays frame 0's screen back in, leaving out the strip where his fingers overlap the screen. ECC chained frame to
   frame drifted as soon as he pushed the phone toward the lens (scale change ~20 %); the jitter before smoothing was up to 20 px.
2. **From a celebratory END frame, Veo adds a fist pump** (3 takes of 3 with "grins... a small proud nod", even with "does not raise
   it or make a fist"). What worked: drop "proud" and "grin", say "smiles warmly... slowly nods his head once... Only his head moves...
   His left hand lies flat on his left knee and does not move at all", and put fist, flexing, celebrating, gesturing in the negative.
   One take of two came back clean (B5). One take also started talking after 2.3 s: say "His lips stay together".
3. **Cropping a 16:9 callout clip to 9:16 cuts its leader lines loose.** Painting them out where they cross skin left visible seams
   (Telea blurs a band; a shifted copy shows bands). What worked: keep the clip's own lines, trace new lines exactly over them
   (`scan3/stub_paths.json`, traced from the lines' own pixels), let them run into the new cards (or turn down at the frame edge to a
   bottom card), and paint only the parts the cards hide. Land the notes while the clip's own lines grow (0 to 0.3 s here), not on
   later words, or the old lines point at nothing until then.
4. **A 1.78x enlargement of an AI scan read fine:** at the same face size it kept about 85 % of the fine detail of the presenter's close
   shot (Laplacian at face height 256: 4.73 against 5.56). Lanczos plus a light unsharp (radius 2, 55 %).
5. **Plans written before 2026-10-14 can still carry a standing-around cutaway.** RA-05's plan had the B0435 physique poses under
   "get the personalized AI fitness plan"; it came out (VIDEO-RULES, "Never a shot of Dan just standing around"). Grep every older
   plan for B0435, B0438 and B0459 before the full build.
