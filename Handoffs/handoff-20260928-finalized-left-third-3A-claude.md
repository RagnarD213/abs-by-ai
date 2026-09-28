# Claude handoff: finalized left-third graphic style 3A

Prepared September 28, 2026. Recommended Claude model: Opus 5.5, High effort.

## Goal

Imitate the exact approved WV-01 option 3A for left-third text and list graphics going forward. Change the content to suit the new video while preserving the visual design, hierarchy, opacity and restrained reveal. This is a reusable reference handoff, not a request to revise existing approved videos or assemble the VSL.

The design evolved through rounds 7 and 8, but the final selection is round10-opacity option3-A. Dan said "Let's go with 3A." Approval is recorded in `/Volumes/Extreme/_edit_work/wv01-edit/round10-plan/dan-review-locks.json` and carried into the round12 assembly handoff. Earlier alternatives are historical, not substitutes.

## Open these exact references first

- Screenshot: `/Volumes/Extreme/_edit_work/wv01-edit/round10-opacity/graphics/option3-A.jpg`
- Approved clip with surrounding speech: `/Volumes/Extreme/_edit_work/wv01-edit/round10-opacity/previews/option3-A-context.mp4`
- Clip SHA256: `34aedf99b942811f98661288b6912ac2c5c3e33372741e30e6a4abce11f74ba6`
- Renderer: `/Volumes/Extreme/_edit_work/wv01-edit/round10-opacity/recipe/build.py`
- Font and presenter helper: `/Volumes/Extreme/_edit_work/wv01-edit/round4/recipe/graphics.py`
- Fonts: `Media/codex-video-trial/assets/fonts/Poppins-Bold.ttf` and `Poppins-Regular.ttf` in the project root.

Watch the whole clip. The card appears about 5.64 seconds into the contextual clip and ends about 19.59 seconds. The screenshot shows the fully revealed state. Do not use the entire contextual video as an overlay in a new edit: recreate its graphic layer over the correct new footage.

## Exact design at 1920 x 1080

One rounded local navy card on the left, with the presenter visible on the right. No second background field stretching to the frame edges. The camera picture remains visible outside the card and faintly through it.

| Element | Approved setting |
| --- | --- |
| Card bounds | x36, y42 to x752, y789 |
| Card fill | RGBA 10,38,72,232; approximately 91% opaque |
| Corner radius | 32px |
| Border | RGBA 99,176,224,180; 2px |
| Heading | Poppins Bold, 60px; RGB 151,223,253; full opacity |
| Heading positions | x64, y64 and y139 for the two lines |
| Divider | White, x65 to722, y228 to231 |
| Body | Poppins Bold, 38px; white; full opacity |
| Numbers | Poppins Bold, 38px; cyan RGB151,223,253; plain 1.,2.,3. |
| Number column | x68; starts at y264 |
| Body column | x113; first row starts at y260 |
| Body wrapping | Maximum590px; 49px line spacing |
| Gap after each item | 30px after its wrapped lines |
| Visible top/bottom padding | Equal37px around actual text pixels |

The title and list live inside the same card. Keep the integrated heading, divider and plain cyan numbers. No number badges, separate title pill, text shadow, extra decorative field or new color palette. Do not make the text translucent when changing card opacity. Alpha218/3B and alpha249 are unselected alternatives.

The example heading is "How AI Customizes" / "The Plan Just For You". Its three items explain the current picture, goal picture, and AI plan. For new content, write a self-contained heading and useful distilled points. Match the font, proportions and hierarchy. Resize card height to the actual content while retaining balanced padding; do not force this example's wording or create a large empty card. Scale coordinates proportionally for other output sizes. If a different aspect ratio needs a different composition, retain this design family and show a short contextual sample before full assembly.

## Motion and presenter placement

The exact renderer reveals complete list items at t0, t0.25 and t0.50 seconds relative to card entry. It does not type letters or slide the presenter. Preserve this restrained behavior; do not invent whooshes, swipes, bouncing numbers or elaborate entrances.

Place Dan in a fixed composition in the remaining right-hand space. Preserve hair, arms, gestures and body throughout the moving shot. His head should have approximately equal room between the card edge and right frame edge. The original helper shifts this specific source composition about300px using empty wall pixels. Adapt the placement to the new source rather than blindly using that crop on unrelated footage. No animated tracking, panning or zooming in16:9.

## Scope and verification

Read `.claude/skills/_shared/VIDEO-RULES.md` in full and `GRAPHICS-STANDARDS.md` before video work. This3A reference refines the standard rounded Soft Blue Light left-third text/list card. Full-screen graphics, standalone phone demos and the Motivation lower third keep their separately approved designs. The WV-01 five-benefit sequence is independently approved and is not to be rewritten automatically to this exact card layout.

Before editing a complete new video, render one short sample with surrounding speech. Compare its full-size still against option3-A.jpg and its moving reveal against option3-A-context.mp4. Check cyan/white hierarchy, card opacity, equal padding, legibility, intact hair/arms, static presenter and complete narration. Use the existing approval for unchanged style; present materially different layout choices before full assembly. Never use an em dash in new copy.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20260928-finalized-left-third-3A-claude.md`. Use the exact approved WV-01 option3-A screenshot, contextual clip and renderer as the reference for all new left-third text/list graphics. Preserve the navy card alpha232, cyan Poppins Bold heading/plain numbers, white body/divider, balanced padding and fixed presenter composition. Adapt only content and necessary dimensions. Build one short contextual sample before a full edit. Keep separately approved phone, full-screen and lower-third treatments intact.
