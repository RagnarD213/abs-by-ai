# Trial Campaign AD Thumbnails R3

Written October 1, 2026 from Dan's review of round 2.
Recommended model: **GPT-6 Astra, High**.
Name the new session **Trial Campaign AD Thumbnails R3**.
**Use the Codex subscription to generate the images.**

## Goal and stopping point

Make only the two remaining thumbnail revisions for campaign `24316364155`: remove the black top stripe from Ad 13's robot design, and show a subtly aged variation of Ad 6's jeans-and-glasses photo. Preserve the four approved ads exactly. Show one review page, then stop for Dan to confirm Ad 13 and choose the Ad 6 version. No final exports, final picks.json, YouTube installation, Google Ads changes or organic publishing in this round.

This is a targeted revision, not another five-choice concept batch. This document supersedes round 2's pending-picks instructions. Do not reopen settled choices.

## Approved choices, keep unchanged

| Ad | Approved option | Real source photo | Approved existing layouts |
|---|---|---|---|
| RA-01: AI Got Me Abs | `RA-R2A` | `studio-blue-53` | 16:9, 9:16 |
| Ad 10: Busy Dad Fitness | `10-R2A` | `studio-white-25` | 16:9, 9:16 |
| Ad 4: Stop Wasting Money On Supplements | `4-R2A`, Confident Smirk | `studio-gray-55` | 16:9 |
| Ad 3: Stop Paying Human Trainers | `3-R2A` | `studio-blue-173` | 16:9, 9:16, 1:1 |

Dan explicitly approved RA-01, Ad 10 and Ad 3, and selected Ad 4's Confident Smirk. These four are locked. Existing JPG hashes were checked against the round-2 manifest when this handoff was written. Preserve the original bytes; do not rerender or change their copy, colour, face, cropping or backgrounds.

Ad 13's robot direction is selected subject to the background fix. Ad 6's real `6-R2A` is the preferred baseline, with a new age variation requested before the final pick. Do not treat either unseen revision as approved.

## Files and current state

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
All paths below are relative to that root.

- **P:** `social media graphics/youtube/thumbnails/_trial-campaign-20261001/`
- **R2:** `P/round2/`
- **Photos:** `photos/finalized social media photos/`
- Full photo: `Photos/<photo-id>_FINAL_PRIMARY.jpg`
- Studio cutout: `Photos/_cutouts/<photo-id>_CUTOUT.png`
- Approved layouts: `R2/options/<approved-option>-<aspect>.jpg`
- Round-2 sources, layout records and prompts: `R2/manifest.json`
- Durable recipe: `scripts/covers/trial-campaign-20261001/round2/build.py` and `review.py`
- Receipt: `Docs/TRIAL_THUMBNAIL_REVIEW_R2_20261001.md`
- Review: http://127.0.0.1:8811/round2/
- Backup ZIP: https://drive.google.com/file/d/19eXv0-yNXxXdUH6LL15DoO4Eb9NI9a68/view
- Shared Drive folder: https://drive.google.com/drive/folders/1kaaQ7aqUc3TT7-40p_KesEf0n_EAj5gb

Round 2 used exactly three Codex subscription generations and no paid image API calls. Recipe commit `d77b1c6` deployed successfully on Railway; homepage and `/health` returned HTTP 200. No final thumbnail exports or installation have happened.

Read `AGENTS.md`, `AI_COORDINATION.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, `.claude/skills/_shared/IMAGE-GENERATION.md` and the imagegen skill before image work. Use the original and round-2 handoffs only for supporting history; this document controls the new work.

## Revision 1: Ad 13, extend the gray background to the top

Dan: "I like the design of the robot trainer 13-R2B" and "extend that gray design in the background all the way to the top like you did in the first one." He explicitly wants "No black stripe at the top."

Create **13-R3B**, one corrected version of `R2/options/13-R2B-16x9.jpg`.

- Preserve the robot trainer, training props, real `photo-10` portrait, waistband crop, white outline, yellow accents and exact headline: **HUMAN TRAINERS / HATE THIS AI**.
- Match the continuous dark-gray background treatment in `R2/options/13-R2A-16x9.jpg`. Its original plate is `P/generated/ad13-B.png`.
- Robot plate: `R2/generated/ad13-robot.png`. Pool mask: `P/masks/photo-10_FINAL_PRIMARY.mask.png`.
- Extend the gray background texture continuously across the upper background to the top edge. No solid black horizontal strip, obvious pasted panel, seam or flat fill band.
- Keep the robot's head clear of the headline and preserve the liked composition. Do not move the robot back up into the words to hide the stripe.

Known cause: the round-2 builder moved the robot plate down 75 pixels and filled the exposed area with solid `#020304`. Fix the exposed area with matching background texture, and make the surrounding upper negative space read as continuous gray. Do not merely change the flat strip to another flat colour. Inspect both rendered thumbnails before deciding the precise blend.

Prefer a local, scene-only compositing repair using the existing gray plate's clean background area, with a natural blend and no imported expense props. If a natural repair genuinely needs a Codex background edit, state that extra generation before running it. Never send Dan's finished composite for regeneration; preserve the real portrait and code-set type.

## Revision 2: Ad 6, subtly age the jeans-and-glasses photo

Dan: "I like 6-R2A but I want to see a second variation of that, with me aged like you did in 6-R2B." He wants the aging "a little more subtle, like salt and pepper, rather than straight gray hair."

Create **6-R3B**, an age variation of `R2/options/6-R2A-16x9.jpg`. Keep unchanged **6-R2A** beside it as the real-photo comparison.

- Correct source: **studio-blue-171**, the jeans-and-glasses person in `6-R2A`.
- Do not use `studio-blue-221`, the different person/pose source used for the previous `6-R2B` age edit.
- Preserve glasses, identity, expression, gaze, haircut shape, head angle, pose, physique, abs, hands, fingers, jeans, belt and all composition details.
- Add modest age-related face/neck texture and mixed dark-and-gray hair. Keep the dark hair clearly dominant, with believable salt-and-pepper strands and temples. The overall aging must be visibly more subtle than the previous `6-R2B`, not uniform silver or straight gray.
- Keep the exact B gym background `P/generated/ad6-B.png`, white outline, yellow accent and headline **HOW MEN 40+ / GET ABS**.
- Generate the age edit on the Codex subscription. Inspect the original full photo first. Composite just the edited hair, face and neck back onto the original cutout where practical, leaving body, hands and clothing unchanged. Adapt the mask to this new photo; do not reuse studio-blue-221's mask coordinates blindly.
- Label the review card **AI age edit**, outside the thumbnail. Do not add a disclosure headline to the artwork.

The explicit aging request is a narrow exception to the real-photo no-redrawing rule, scoped only to this new variant. It is not permission to enhance or reshape the body.

## Build, review and delivery

Plan **one new Codex generation**, the subtle age edit. The Ad 13 repair should reuse existing assets. State the count before starting, generate no spares, and record any necessary extra generation. Use `.claude/skills/_shared/codex-image.sh`; no paid image API.

Preserve rounds 1 and 2. Save new work in `P/round3/` and reusable code under `scripts/covers/trial-campaign-20261001/round3/`. Do not run the round-2 builder unchanged, because it overwrites that round's review files.

Produce two new horizontal review JPGs at 1280x720, each under 2 MB. Keep source compositions adaptable. Check `Docs/AD_VIDEO_IDS.md` for newly completed formats before delivery, but do not take over another video task or silently redesign approved layouts.

Build one review page at `P/round3/index.html`, served as http://127.0.0.1:8811/round3/. If the server stopped, run:

```bash
python3 -m http.server 8811 --bind 127.0.0.1 --directory "social media graphics/youtube/thumbnails/_trial-campaign-20261001"
```

Open with a short "What I decided (overrule anything)" section. Show the corrected Ad 13 with its previous version available as reference. Show Ad 6's unchanged `6-R2A` beside new `6-R3B`, with your recommended pick and a brief reason. Keep the four approved ads in a compact locked-reference section, not another approval request. Include enlarged and 320-pixel phone views, source labels, and a copyable reply for the two pending decisions. Use a new round-3 localStorage key.

Verify the gray background reaches the top without a seam; the robot and text remain clear; the aging retains glasses, identity and original physique; full head/hair and abs remain visible; text is exact; all image links and controls work. Preserve an offline review and a manifest with source paths, hashes, prompts, generation count and approvals. Back up new assets to the existing Drive folder with anyone-with-link viewing.

Save a receipt, use `scripts/git/safe-push.sh` for only this task's files, and verify deployment according to project rules. Re-read the board and update only this task's entry; run `scripts/board-check.sh`. No dashboard row unless Dan asks.

Stop after delivering this review. The separate installation handoff, `Handoffs/handoff-20261001-trial-campaign-ad-thumbnails-install-claude.md`, remains blocked until the remaining picks and final exports exist. All ad videos stay Unlisted.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20261001-trial-campaign-ad-thumbnails-round3.md` and execute it. Name this session "Trial Campaign AD Thumbnails R3". Use the Codex subscription to generate the images. Remove the black top stripe from Ad 13's 13-R2B robot design by extending the gray background to the top. Add a subtly aged salt-and-pepper variation of Ad 6's 6-R2A jeans-and-glasses photo, preserving its glasses and real physique. Keep RA-R2A, 10-R2A, 4-R2A and 3-R2A approved and unchanged. Show one review page, then stop for my remaining picks before final exports or installation.
