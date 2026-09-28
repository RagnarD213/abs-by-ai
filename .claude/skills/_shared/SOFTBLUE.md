# Soft Blue Light graphics: how to build them (2026-09-26)

What the look is and when it applies: [GRAPHICS-STANDARDS.md](GRAPHICS-STANDARDS.md). This page is the
how. Code: [`softblue.py`](softblue.py). It is the default for every new or revised graphic in every
Claude video skill (/ad-edit, /longform-edit, /website-video, /shorts, /shortad-from-longform, /make-ad),
in 16:9, 9:16 and 1:1.

## Selecting it in a build

```python
import sys; sys.path.insert(0, ".claude/skills/_shared"); import softblue as B
```

| Need | Call | Output |
|---|---|---|
| Full-screen photo + fact card (before picture, a stat) | `B.render_scene(out, dur, lambda t: B.scene_fact(t, w, h, photo, eyebrow, headline, detail, label), w, h)` | opaque H.264 insert |
| Three portraits (only format for three photos) | `B.scene_portraits(t, w, h, [p1, p2, p3], "Real pictures of me. Not AI-generated.")` | frame; wrap in `render_scene` |
| One photo (horizontal photos: one scene each, cut in sequence) | `B.scene_photo(t, w, h, photo, label)` | frame |
| CTA | `B.scene_cta(t, w, h, eyebrow, "Line one\nline two", button)` | frame |
| Custom full-screen graphic (list, diagram, comparison) | start from `B.field(t, w, h)`, add `B.glass(...)`, `B.text(...)`, `B.photo_card(...)`, `B.disclosure(...)` | frame |
| Left-third text/list card (3A, all videos) | `B.left_third(B.shift_presenter(im, dx, c0, wall_w), t, heading, [points], dur=d)` per frame via `render_over_footage`; `B.left_third_box(w, h, heading, points)` gives the card box for placement checks | footage with graphic |
| Lower third on a short clip | `B.render_over_footage(src, out, dur, lambda im, t: B.lower_third(im, t, TOPIC, POINT, dur=d), start, w, h, vf=crop)` | footage with graphic |
| Lower third inside a long film | `path, x, y = B.lower_third_patch(base, out, start, dur, TOPIC, POINT, w, h)` then `-itsoffset start -i path` and `overlay=x:y:enable='between(t,start,start+dur)'` | opaque patch of the band only |

- `w, h` is the canvas: 1920x1080, 1080x1920 or 1080x1080. Layout unit `u = min(w, h)/540`; at 16:9 every
  component reproduces the approved reference geometry exactly.
- `TOPIC` adapts to the narration (MOTIVATION, WORKOUTS, `KEY POINT` for a single distilled point). `POINT`
  follows the key-point writing rule in VIDEO-RULES. Long points wrap and the strip grows.
- Default lower-third placement: 16:9 and 1:1 at the bottom (captions lift above, the 2026-09-02 rule);
  9:16 with its bottom at 68 % of the height, above the 70-84 % caption band. Override with
  `box=(x0, y_top, x1)` after measuring the moving presenter and the real captions.
- The glass blurs the actual picture beneath it, so lower thirds are composited on the graded,
  caption-free base, never as a pre-baked alpha MOV. `lower_third_patch` must be overlaid on the same base
  it was rendered from.
- Semantic teaching colours: `B.GOOD` (green, correct form) and `B.BAD` (red, the mistake).
- Not in the module on purpose: the phone shell (round 3's was rejected; wait for an approved WV-01
  round-4 shell), background panels behind side lists (lists beside Dan are bold text straight over the
  shot), and any presenter movement.

## 3A left-third card (2026-09-28)

`left_third()` reproduces WV-01 option3-A pixel for pixel at 1920x1080: 0.0 mean difference against the
approved `round10-opacity/recipe/build.py` overlay on four frames spanning the item reveals, including
`shift_presenter()` at its defaults (the WV-01 W2 shift). For another source, pick `dx` (shift), `c0`
(where the moved picture starts) and `wall_w` (empty wall only) so Dan's head sits centred between the
card edge (x752) and the frame edge. 9:16 and 1:1 use the full-width adaptation locked by Dan on 2026-09-28: `B.left_third(frame, t, heading,
points, dur=d)` on the full-frame portrait (or square) footage puts the card at the bottom by default.
Approved samples: `/Volumes/Extreme/_edit_work/softblue-rollout/left3a/left3a_r2_v3_full_frame_graphic_bottom.mp4`
and `left3a_r2_sq_graphic_bottom.mp4` (builder `make_left3a_r2.py` beside them). `B.stack_vertical()` (card
above or below a horizontal crop) was shown and NOT selected; use it only if Dan asks for that layout.

## What is historical now

`motionlib.py` palettes (`GREEN`, `J2AD`, `MIL`, `PAPER`), J2/olive panels and chips, and components
rebuilt from Muhammad's graphics stay in the repo so approved films and their recipes still rebuild. Use
them only to reproduce or format-convert an approved export whose graphics are not being revised.
Muhammad remains the reference for audio, colour and transitions.

## Verification (2026-09-26)

- Parity against the private reference renderer `wv01-edit/round3/recipe/blueglass.py`: `field()` is
  pixel-identical to `background(t, style=0)`; `lower_third()` differs from `lower_layer()` by 0.11 mean
  levels (below the 2.0 noise between that renderer and its own encoded `G-motivation.mp4`); the patch
  path matches a direct render within encoder noise.
- Template demos (existing approved media, no paid generation), private on the SSD:
  `/Volumes/Extreme/_edit_work/softblue-rollout/demo/softblue_demo_{16x9,9x16,1x1}.mp4`, each a fact card
  with disclosure, a lower third over moving footage (the 9:16 is full-frame portrait C1720), and the CTA.
  Builder: `/Volumes/Extreme/_edit_work/softblue-rollout/make_demo.py`. These are template checks, not a
  film approval; every new use still needs its own moving-picture inspection and delivery gate.
