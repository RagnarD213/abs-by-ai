---
name: thumbnail-design-system
description: "Abs By AI YouTube thumbnail/graphic style — banner-derived black + white Manrope + red bar, and the shoot's 16:9 crop limitation"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5a46d012-95fe-4d60-a74f-a6d9e553001a
  modified: 2026-08-09T20:54:49.921Z
---

Dan's settled visual system for YouTube thumbnails (2026-08-07), derived from the channel banner at `social media graphics/youtube/channel banners/Abs-By-AI-YouTube-Banner-2560x1440.png`. He rejected an Arial-Black-with-heavy-stroke-over-blurred-photo version and directed that thumbnails match the banner instead.

- Background solid `rgb(5,7,11)`; **never a blur effect**.
- White headline, left-aligned, caps; red accent bar `rgb(201,48,45)` to its left.
- Logo lockup `logos/03-symbol-left-text.png` top-left — **artwork is dark, recolor to white keeping alpha** or it vanishes on black.
- Font **Manrope ExtraBold**, `~/Library/Fonts/Manrope.ttf`. The variable file defaults to **ExtraLight** — must call `set_variation_by_name("ExtraBold")`.
**REVISED 2026-08-08 — the type stays, the black slab is gone.** Dan on the first V4 pass: *"too much black, and I'm shoved over too much to the side… I want my image more centered in the frame, as centered as possible given the text, and less black."*

- **Fill the frame with the photo, not a black rectangle.** Portrait source → cut the subject out at full height, place at ~0.63 width, and put a **darkened scenery-only crop of the same photo** behind. Landscape source → cover-crop straight to 16:9, no background layer at all.
- **The scenery crop must come from a part of the frame Dan is NOT in** (e.g. `x 0.00–0.26`). A centre crop leaves a ghost duplicate of his torso behind the text.
- Legibility from a **gradient scrim** (horizontal for side text, top-left corner ramp for top text) — still never a blur.
- **Text must sit on empty background.** For a horizontal pose the only clear region is the **top band**: 2-line headline, bias the cover crop upward (`ybias≈0.12`) for headroom, cap the font ~84, and check the measured text bottom against where his body starts.

**Standing rule (Dan, 2026-08-08): every video gets TWO thumbnails built as a deliberate A/B test**, shown side by side before install, both loaded after publish. When the video is a workout, **one variation must show him actually doing an exercise** — the 7-31-26 shoot's exercise frames are raw **39–66** (60–66 Spider-Man planks are landscape + face-to-camera, the best); note they live in the raw shoot folder and are **not retouched**.

**Two hard constraints, both learned the expensive way:**
1. The 7-31-26 pool shoot's *finalized* files are 2747×4096 portrait, so a straight 16:9 crop **cannot** contain Dan's face and abs simultaneously (needs ~3900px width). Thumbnails from those must be composites. The **raw** frames include 6720×4480 landscape shots, which crop to 16:9 losing only ~15% — use those when you need edge-to-edge.
2. Dan's rule: **abs must be visible in every variation, and text must never overlap them.**

Working build scripts: `YouTube Long Form Video Content/v4-1min-ab-workout/build-thumbs-v4.py` (current — `scene` + full-bleed layouts); `six-ways-ai-abs/build-thumbs.py` (the older black-panel version).

Standing instruction from the same session: **installing fonts needs no permission.**

Related: [[repo-is-public]] — `social media graphics/` and `photos/` are gitignored because they hold shirtless photos of Dan.
