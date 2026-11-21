# Home Arm Workout Instagram cover: more ripped variation only

Prepared 2026-09-28. Recommended model: GPT-6 Astra, high effort.

## Goal and current state

Build one more aggressively retouched variation of row 16's Instagram cover for the same **2-minute home arm workout long-form video**. Dan asked: "touch me up a little bit more aggressively and make me look a little bit more ripped." This is the only remaining cover revision.

Dan approved the round 4 Biggest Ab Wheel Mistake, How to Do Ab Wheel Rollouts and Ab Wheel Workout Tip covers on 2026-09-28. Both Instagram and YouTube exports for rows 12-14 are now locked. All earlier selections remain locked, including row 16's original horizontal YouTube thumbnail. Do not regenerate or show those approved rows again. Do not build a row 16 YouTube portrait variation.

No new retouch was generated while writing this handoff. No installed cover, queue, schedule or publishing account was changed. This task produces a review candidate, not an installation batch.

## Read and locate

Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, `.claude/skills/coverimage/SKILL.md` and the available `imagegen` skill before image editing. The explicit stronger-retouch request here supersedes the earlier "subtle" retouch direction for this one image only.

Read `Docs/QUEUE_COVERS_APPROVALS_20260928.json`, the current approval authority. It combines 30 approved replacement exports and four originals retained unchanged. Verify all 34 hashes before and after the new work. Preserve the earlier approval record as history.

Shared media root, use this absolute path even from a worktree:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/queue-bakeoff-20260924/`

Current row 16 comparison:

- `round4-unfinished-20260926/covers/16-A-instagram.jpg`
- SHA256: `061cf2b4949862cc61ad099e9243ef6d8c3150dc1c52934e4d4ff21f3dde5ed6`
- Literal grid preview: `round4-unfinished-20260926/grid-crops/16-A-grid.png`
- Builder and geometry: `round4-unfinished-20260926/build_round4.py`, `manifest.json`
- Current review: `round4-unfinished-20260926/index.html`, previously at `http://127.0.0.1:8794/index.html#row-16`

Editable photographic input:

- `round4-unfinished-20260926/inputs/row16-generated-retouch.png`
- SHA256: `81e3d96edd8db76c36ab642cbb802bd572d59a5cfcb8df99584a657b4a279f49`
- Identical earlier input: `round3-platform-layouts-20260925-fbd1/inputs/row16-generated-retouch.png`
- Original real frame: `round2-20260925/sources/row16-original.png`
- Finished source: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Zeeshan Content Videos/arms and shoulders home workout - video 2/arms and shoulders home workout | zeeshan | 16x9 | video 2.mp4`, at 475.3 seconds.

This is the pool photo used in horizontal round 2 16-A. Its clean subject is usable, but the wider input still has the workout list burned on the left. The R4 crop excludes that list. Do not bring cropped fragments of it back into view.

## Retouch direction

Use the image-generation editing tool on the photographic input. Inspect it before editing. Do not try to edit a flattened thumbnail with the title baked in. Make one stronger candidate, with a retry only if the first has a clear defect.

Make Dan noticeably more ripped than the current R4 cover, especially sharper six-pack separation and obliques, with stronger chest, shoulder and arm definition. Use deeper natural muscle shadows and controlled highlights. Keep believable skin texture and the source's sunlit color. This should be a visible upgrade at phone size, not a barely noticeable contrast adjustment.

Preserve Dan's recognizable face, sunglasses, hair, expression, pose, hands, clothing and overall proportions. Keep the pool scene, equipment and photographic realism. Avoid swollen muscles, a new body shape, extra anatomy, plastic skin, excessive orange color and dark muddy shadows. Preserve the full head and both arms.

Suggested editing prompt:

> Edit this same real poolside portrait of Dan. Create a noticeably stronger, more ripped retouch than the existing image. Sharpen his six-pack and oblique definition with deeper believable muscle separation and natural highlight shaping; also bring out chest, shoulder and arm definition. Keep real skin texture and the sunny photographic lighting. Preserve his exact recognizable face, sunglasses, hair, expression, pose, hands, clothing, overall body proportions, pool, house and dumbbells. Do not create a different person, bulk him up, change his pose, add anatomy, add text or crop the image. The result should look like a more assertive professional fitness-photo retouch of this same moment.

Retouch only the photo. Keep the exact title `2-minute home arm workout` and the R4 Instagram design unchanged so Dan can judge the physique change directly.

## Preserve the R4 layout

Adapt the existing row 16 branch of `build_round4.py` in a new private folder; do not rerun the old builder or overwrite its approved exports.

- Canvas: 1080 x 1920 RGB.
- Source crop: `(560,0,1290,941)` on the 1672 x 941 input.
- Photo output box: `(105,542,974,1662)`, 869 x 1120, preserve the full portrait and visible right-hand dumbbell pair.
- Title: Impact 130, two lines `2-minute home` / `arm workout`.
- Exact title boxes: `(60,280,864,387)` and `(60,401,732,506)`.
- Photo starts at y=542 beneath the type. Keep the olive divider and photo border, background and title clear of hair and face.
- If the tool changes input resolution, scale the source coordinates proportionally before applying the same output geometry. Do not stretch the portrait.
- Instagram grid must be a literal centered crop `(0,240,1080,1680)` of the actual exported cover. Essential title and the complete portrait must survive.

## Build, review and deliver

Save under the shared root in `round5-row16-retouch-20260928/`. Preserve all prior packages and inputs. Keep source, edited input, prompt, generation/cost record, build recipe, manifest and export hashes there. These photos and production recipes remain Git ignored.

Deliver one 1080 x 1920 stronger Instagram cover and its actual 1080 x 1440 grid preview. Show a compact browser gallery containing **only Instagram row 16**: the unchanged R4 cover and grid preview beside the new stronger cover and grid preview, with full-size links. Label it "Instagram cover for Home Arm Workout long-form video." Do not show the locked horizontal YouTube thumbnail or any other row for selection.

Inspect the new photographic source and rendered cover at full size and phone size. Compare the degree of definition, identity, skin, anatomy, full hair, arms, equipment, exact copy and crop. Verify all 34 locked hashes remain unchanged. Check every gallery link and open the gallery for Dan to review. Record checks honestly.

Use the existing standing generation authorization. State a metered cost estimate before paid calls and record actual cost; do not use production-generation paths or user credits. Earlier built-in R2 image editing did not report a separate dollar charge, so do not invent its historical cost or relabel it as zero. No spend was incurred in preparing this handoff. Follow the current skill and project budget limits if a metered provider is needed.

Keep installed covers and every publishing queue unchanged. Do not generate the variation in the handoff-writing task. In the execution task, build it directly and finish at the new row 16 review gallery.

## Starter prompt

Execute `Handoffs/handoff-20260928-home-arm-workout-instagram-more-ripped.md`. Build one noticeably more ripped retouch variation of the 2-minute home arm workout Instagram cover, preserving the exact R4 title, photo choice and composition. All other cover selections, including rows 12-14 and the original horizontal YouTube row 16, are approved and locked. Show only Instagram row 16's current and stronger covers with their actual grid crops. Preserve all installed covers and publishing queues.
