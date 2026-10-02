# Trial Campaign AD Thumbnails R3, October 1, 2026

Status: all six choices approved by Dan on October 2, 2026. Ten final JPGs exported as byte-identical copies of approved review files. No installation or publishing performed.

Review: http://127.0.0.1:8811/round3/
Backup: https://drive.google.com/file/d/1JKH6pyR2HZwuQqBOiW_euDmzYhwGyX8V/view
Shared folder: https://drive.google.com/drive/folders/1kaaQ7aqUc3TT7-40p_KesEf0n_EAj5gb

## Changes

- 13-R3B replaces the exposed black top stripe with the original ad13-B plate's clean gray texture. A smooth feather from y100 to y245 joins it to the existing robot scene. The robot stays shifted down 75 pixels, clear of the headline. All scene pixels below y245 stay unchanged before portrait and type composition. Original photo-10 portrait, waistband crop, outline and exact headline are reused.
- 6-R3B uses one Codex subscription generation on studio-blue-171, the correct jeans-and-glasses photo. Dark hair stays dominant, with salt-and-pepper strands and temples plus mild facial and neck texture. Only the head/neck area is composited onto the original cutout. Original body, arms, fingers, jeans and belt remain unchanged. Every cutout pixel below 32.6% of source height is verified identical. Original B gym and type are reused. Review card says AI age edit.
- 6-R2A remains unchanged for comparison. RA-R2A, 10-R2A, 4-R2A and 3-R2A are approved and locked, across eight existing layouts. SHA256 verification against the round-2 manifest passed; reference copies are byte-identical.

Recommendations: confirm 13-R3B and choose 6-R3B. The restrained age detail supports the 40+ message while keeping the preferred pose. These are creative judgments, not measured ad results.

## Generation and verification

One generation through `.claude/skills/_shared/codex-image.sh`, 17,204 helper-reported Codex tokens. Zero paid image API calls or spares. Original source inspected before generation. Full prompt, source hashes, generation hash and layout records are in the manifest and durable recipe.

Both review JPGs are 1280x720 and below 2 MB: 13-R3B is 337,927 bytes; 6-R3B is 332,405 bytes. Full-size, detail and phone views inspected. No visible top seam, robot/headline collision or cropped hair. Headline/person mask overlap is zero. Original physique and glasses retained. Fourteen unique image URLs returned HTTP 200. Phone-view toggle, enlarged preview, previous-version disclosure, selection-to-reply, copy and clear controls checked in the browser; test selections cleared. Offline HTML embeds all review images.

Docs/AD_VIDEO_IDS.md checked October 1: no additional completed Ad 13, Ad 6 or Ad 4 formats were listed. Other video tasks retain ownership of pending formats.

## Files and next action

Work folder: `social media graphics/youtube/thumbnails/_trial-campaign-20261001/round3/`.
Durable recipe: `scripts/covers/trial-campaign-20261001/round3/`.
Run `build.py`, then `review.py`, after restoring round-1/round-2 inputs and this round's generated age source. Earlier builders are never executed. The backup contains review assets, original approved reference copies, offline HTML, prompt, manifest and recipe.

Dan approved 13-R3B and chose 6-R3B on October 2, retaining RA-R2A, 10-R2A, 4-R2A and 3-R2A unchanged. The ten final images are in `social media graphics/youtube/thumbnails/_trial-campaign-20261001/FINAL APPROVED/`, with matching canonical copies in each ad folder's `trial-20261001/` directory. `picks.json` maps all twelve YouTube IDs to their approved files; a tracked copy is `scripts/covers/trial-campaign-20261001/round3/final-picks.json`. All ten source hashes and output dimensions verified. The existing installation handoff now has its required inputs, but was not executed: this request was to show the final images in Finder.
