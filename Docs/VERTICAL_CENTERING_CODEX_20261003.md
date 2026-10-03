# Codex vertical centering adopted

Completed 2026-10-03. New 9:16 presenter crops now land on Dan after a cut, then hold until he moves outside the 3.3% band. Corrections use the shared `landing.py`, with 0.75-second easing and scaled limits. Takes with small movement keep their first-frame centre. The end is not pulled back to centre.

## Before and after

Isolated crop-only excerpt from the existing Ad 2 vertical source, 35.002 seconds, 1,049 frames at the original 30000/1001 frame rate. Both clips use the same graded picture conform and are muted to isolate framing. Existing approved exports and build directories were not written to.

- Before: `/Volumes/Extreme/_edit_work/vertical-centering-codex-proof-20261003/before.mp4`
- After: `/Volumes/Extreme/_edit_work/vertical-centering-codex-proof-20261003/after.mp4`
- Review page: `/Volumes/Extreme/_edit_work/vertical-centering-codex-proof-20261003/index.html`
- Cut starts and biggest lean: `cuts-and-largest-lean.jpg` in that folder.

| Measurement | Before | After |
| --- | ---: | ---: |
| Total crop travel | 1,594 px | 733 px |
| P90 pan speed | 119.9 px/s | 59.9 px/s |
| Time moving | 62.2% | 43.8% |
| Head distance from centre, median / maximum | 11.7 / 58.9 px | 20.6 / 69.0 px |

The crop travels 54% less. Dan has more room to move naturally before the crop follows him. Measurements use source pixels in the 608-pixel-wide crop, exclude jumps between takes, and define moving as over 5 source pixels/second. Head centre was detected on every native frame, not estimated from the crop position. The four groups are total travel, p90 speed, moving time, and median/maximum head distance.

All eight starts land within 0.49 source pixels of the measured head centre after integer pixel rounding. The closest detected face edge is 97.1 source pixels inside the crop. I inspected rendered cut-start frames and the largest lean visually: his head and hair have clear space. Geometry was checked across every frame. Continuous playback was not available to the assistant; the original-frame-rate clips are provided for judging motion. This is a crop-method proof, not a new delivered ad or a delivery-gate PASS.

## Skills and scripts changed

- `Media/codex-video-trial/skills/abs-edit-ad/SKILL.md`
- `Media/codex-video-trial/skills/long-form-content-edit/SKILL.md`
- `Media/codex-video-trial/skills/vsl-edit/SKILL.md`
- `Media/codex-video-trial/05-recipes/shared/standards.md`

The installed `~/.codex/skills/` entries are links to those project skills, so the live copies adopt the same change. `abs-edit-organic` is already an alias to `long-form-content-edit`; it inherits the rule and needs no duplicate skill.

The shared framing document and VIDEO-RULES contain one authoritative named section, reconciled with the rule pushed by the other session. `landing.py` provides scaled vertical presets, exact-cut measurement checks, native-frame interpolation and motion reports. Its small-wander shortcut now anchors the first frame in vertical mode; its legacy square behavior stays unchanged.

Reusable generators `kit_track.py`, `facetrack4.py`, `a6/zcrop.py`, `a7/zcrop_ad5.py`, `a8_ad4/zcrop.py`, and presenter-window rendering in `render.py` use the shared method. The older `facetrack3.py` refuses new builds and directs them to the exact-frame generator. `subject.py` is marked calibration only. Layout returns and punch boundaries require measured landing frames. Missing measurements stop a new build with the frame to measure. Existing frozen copies under approved build directories and historical Codex 16:9 tracking scripts remain untouched; they are not new vertical generators. Squares, horizontal framing, graphics, audio and delivery-gate thresholds are unchanged.

## Verification

`landing.py selftest` passes, including the first-frame fixed-take regression. Five additional checks pass for scale, cut separation, speed cap, missing cut measurements, crop geometry and the renderer's actual window expression. All changed scripts compile. The proof hashes and per-frame measurements are saved beside the clips. No video was uploaded.
