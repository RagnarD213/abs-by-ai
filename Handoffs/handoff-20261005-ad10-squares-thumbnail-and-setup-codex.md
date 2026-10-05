# Ad 10 "My Dad Bod At 38, My Dad Bod At 40": the two squares, thumbnail, YouTube and Google Ads

Written 2026-10-05 for **Codex**. Recommended: **GPT-6.1 Sol, High** (one matching thumbnail from an approved design, then a
checklist of two uploads and API calls). Sidebar name: `My Dad Bod At 38 S/Sh Ad Setup`.

**Category: AD.** Both files end "tap the button below", so they are ads: `/ad-setup` only, **Unlisted**, never Public, never
organic, never Blotato.

Dan approved both files on 2026-10-05: *"Okay, these are approved. Give me the handoff document for Codex to set these up
and add them to YouTube and Google Ads."* Recorded with the file hashes in `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40
- ad 10/approval_20261005.json`. The same words say: use the Codex subscription to generate the images (only if an image has to
be generated; see step 3).

**Where things are.** This handoff, the two videos and the thumbnail sources are in the MAIN project folder,
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/`. The main folder's push is stopped by other sessions' edits, so this
handoff and the delivery commit (`34d6878`) are not on GitHub yet. If you work in a worktree, read and write the media,
thumbnails and this file by that absolute path; every relative path below is relative to that folder.

Read first: `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (in full), `Handoffs/video-editing/00-RULES.md` (Codex column and
environment table), `.claude/skills/ad-setup/SKILL.md` (the method), `Docs/DGEN_CONVERSION_CAMPAIGN.md` (the sections "2026-10-04:
four approved Ad 6 formats added to the trial campaign" and "2026-10-04: four approved Ad 4 formats added to the trial
campaign": those are the model for this job), `Docs/AD_VIDEO_IDS.md`.

**The Victory Dashboard is PAUSED (Dan, 2026-10-05): do not read, write or check off anything on it.** Skip every dashboard step
in any skill.

## The two approved files

Folder: `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/` (main project folder, not in git).

| file | size, length | sha256 |
|---|---|---|
| `my dad bod at 38 my dad bod at 40 \| claude \| 1x1 \| ad 10.mp4` | 1080x1080, 3:01.615, 240 MB | `f2c98162b8aa3ced8abeeeacf6008fa22bd856e80d17912aa626ac1e18ca22eb` |
| `my dad bod at 38 my dad bod at 40 \| claude \| 1x1 59s \| ad 10.mp4` | 1080x1080, 0:57.124, 70 MB | `fa7c29462157ef9cda50eb8c45f5065e61a83d3c064aee9777782752109bf480` |

Each has its delivery gate (2.4.0) and audio gate (2.0.0) stamp beside it, both PASS, and an independent review verdict of
SHIP (`ROUND-2-REVIEW-square-full.md`, `ROUND-2-REVIEW-square-cutdown.md` in the folder). Each square's audio is the approved
vertical's AAC stream byte for byte. **Re-hash both before uploading. If a hash differs, stop and say so.** Do not re-encode,
trim or re-mux them. The two `REVIEW 540p 1x1` files are Dan's review copies, not for upload.

## Work, in order

1. **Classify from the file.** An ad, as above. Filing is already done.

2. **Titles, descriptions, tags.** Titles follow the Ad 10 verticals' pattern (`Handoffs/handoff-20260925-ad10-verticals-youtube-google-ads.md`):
   - `My Dad Bod at 38. My Dad Bod at 40. (Square)` and `My Dad Bod at 38. My Dad Bod at 40. (Square 59s)`.
   - Descriptions: the 16:9's is `youtube-description.md` in the ad folder; the 9:16 59 second one is
     `youtube-description-vertical-59s.md`. The full square shares the vertical's timeline (5,443 frames, 3:01.615), so the
     chapters carry over from `youtube-description.md`; the 59 second square gets no chapters. Write
     `youtube-description-square.md` and `youtube-description-square-59s.md` beside them. Keep the AI disclosure paragraph and the
     tracked link (`utm_campaign=dgen-conv-ad10`). **Replace the long dash in the "See what YOU would look like..." line with a
     hyphen** (new writing never carries an em dash; the old files keep theirs).
   - Tags: read them from the live 16:9 `Sg3vcEY2P_8` and reuse them.
   - `--synthetic true` on both (Muhammad's AI clips and the AI goal pictures; the 16:9 and the verticals are set the same way).
     YouTube omits that field from API readback, so verify "AI use: Yes" in Studio for both, as the Ad 4 and Ad 6 setups did.

3. **Thumbnail: one new image, `Ad 10 | 1x1 | FINAL.jpg`, matching the others.** Ad 10 has `Ad 10 | 16x9 | FINAL.jpg` and
   `Ad 10 | 9x16 | FINAL.jpg` (option **10-R2A**, the approved trial-campaign design) in
   `social media graphics/youtube/thumbnails/Ad 10 My Dad Bod/trial-20261001/` and in
   `social media graphics/youtube/thumbnails/_trial-campaign-20261001/FINAL APPROVED/`. There is no square yet.
   - Build the square in that same design: same approved cutout, same plate, same type, same accent, laid out for 1:1 the way
     the other ads' `1x1` finals are (`Ad 3 | 1x1`, `Ad 4 | 1x1`, `Ad 6 | 1x1`, `Ad 13 | 1x1`, `RA-01 | 1x1`).
   - The model is how Ad 4 and Ad 6 did it: `scripts/covers/trial-campaign-20261001/ad4-formats/build.py` and
     `ad6-formats/build.py` recompose the EXISTING plate and cutout with the other ads' rendering functions, **no image
     generation and no paid image call**. Add `ad10-formats/build.py` the same way and a hash receipt.
   - **Reuse the approved 10-R2A cutout exactly. Do not regenerate or re-edit Dan's photo.** If the plate truly cannot be
     recomposed to a square, extending the background is the only generation allowed, and it goes through the Codex
     subscription image tool (`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`), never a paid API.
     **Use the Codex subscription to generate the images** if any image is generated.
   - No new wording and no claims in the thumbnail copy: the words are the ones on the approved 16:9 and 9:16.
   - Check it beside the other ads' 1x1 finals: head and text inside the frame, nothing cut, same weight and spacing, zero
     text-over-person overlap. Save it in the Ad 10 thumbnail folder above and copy it into `FINAL APPROVED/`.
   - It serves both square uploads. Do not stop for a pick (Dan asked for matching thumbnails and setup in one task); show him
     the image in the final report. A thumbnail can be swapped later with `scripts/youtube/set-thumbnail.js`.

4. **Upload both Unlisted** with `scripts/youtube/upload.js --privacy unlisted --synthetic true --thumbnail <file>` (the script
   refuses Public). Read back on each: `privacyStatus: unlisted`, `processingStatus: succeeded`, `embeddable: true`, not made
   for kids, category 26, the custom thumbnail served (save a `readback-<id>.jpg` beside the finals, as the 10-02 install
   did). Never use YouTube's scheduling or publish-at path.

5. **Google Ads: the trial campaign `24316364155` only.** Ad 10's group is `202248166482` ("Ad 10 Busy Dad Fitness"); its three
   live ads are the 16:9 `826635657832`, the 9:16 `826635657835` and the 9:16 59s `826635657838`.
   - Add **two** ads to that EXISTING group, one per new video, the way the Ad 4 and Ad 6 formats were added
     (`scripts/ads/api/dgen-ad4-formats.js` and `dgen-ad6-formats.js` with their `dgen-ads/*-formats.json`; readback
     `*-formats.result.json`). Build `dgen-ad10-squares.js` and `dgen-ads/ad10-squares.json` the same way.
   - Headlines, long headlines, descriptions, logo, business name and CTA are **read back from the live 16:9 ad
     `826635657832` and reused unchanged** (Dan rewrote the Ad 10 headlines himself on 10-01 and the long copy on 10-02; write
     no new line). Run `node scripts/ads/api/client.js policy 24316364155` first and record the live twin's status. If a line
     on it is DISAPPROVED, copy it anyway and report it to Dan; the retry rule in `Docs/DGEN_CONVERSION_CAMPAIGN.md` applies and
     rewriting copy is not yours to do here.
   - Final URLs: `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad10&utm_content=claude-square-vsl`
     and `...utm_content=claude-square-59s-vsl` (the square spelling Ad 4, Ad 6 and RA-01 use; Ad 10's own verticals use
     `claude-9x16-vsl` and `claude-9x16-59s-vsl`: compare against `scripts/ads/api/dgen-ads/` for the exact string).
   - `validateOnly` first, then apply. Ads ENABLED inside the existing group, create operations only. **Budget (`15911255930`,
     $30/day), bids, target CPA, audience, the 16:9 ad, the two 9:16 ads and every other ad stay exactly as they are.** Take a
     before/after comparison as the Ad 4 and Ad 6 setups did. Never enable a paused campaign.
   - Run `node scripts/ads/api/client.js policy 24316364155` after the apply and record each new ad's status.
   - **Remarketing: do not touch it.** Dan's 10-05 "yes, also put them in the live conversion remarketing" was for Ad 4 only.
     The enabled conversion remarketing campaign `24305381214` (groups Website visitors `206411886211` and YouTube viewers
     `201604959278`) and the engagement campaign `24316408288` stay as they are. In the report, offer Dan the option "also add
     these two squares to conversion remarketing `24305381214` as for Ad 4" and wait for his answer.
   - Leave alone: the old Demand Gen campaign `24243839443` (PAUSED; its Ad 10 groups are `206979993984` and `206979994264`)
     and Performance Max `24308574894` (it is at its five-video limit and already holds the Ad 10 9:16 `4nDWFmdjzQQ`). If you
     think a square should replace a video there, say so as an option; do not change it.

6. **Record it.** `Docs/AD_VIDEO_IDS.md` (two rows), a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md` (video ids, asset
   ids, ad ids, URLs, policy status, the recheck date one day later, and the remarketing option), the Edit Queue (`python3
   scripts/edit-queue/queue.py set AS-06 uploaded`, then `queue.py push`), a board line in `AI_COORDINATION.md` (replace the
   "AS-06 Ad 10 squares" line in its ACTIVE section; delete this handoff's line in HANDOFFS and its row in `Handoffs/README.md`
   when done). No dashboard step.

7. **Report to Dan in plain language:** the two YouTube links, the new square thumbnail (send the image), what was added to
   which ad group, that the budget is unchanged, that nothing was posted organically, each new ad's policy status, the date of
   the policy recheck, and the remarketing question.

## Traps

- **An ad never goes organic and never uploads Public.** "All platforms" in any wording is not authorization.
- Nothing here authorizes pausing, replacing or editing the live 16:9 `Sg3vcEY2P_8`, the verticals `4nDWFmdjzQQ` and
  `CR4WAVmSuXY`, or any of the three live Ad 10 ads.
- A new ad can sit in `REVIEW_IN_PROGRESS` for a day; that is normal.
- The 16:9 chapters end at 2:51 and the full square is 3:01.6: the last chapter simply runs to the end.
- Secrets come from `~/.absbyai-secrets.env` and the Railway CLI. Never ask Dan for a key and never paste one.
- The main project folder's push is stopped by other sessions' uncommitted edits (see the board). From a Codex worktree,
  commit only your own files and push with plain git. Do not touch the unpushed kit commits.
- No em dashes in anything written (titles, descriptions, docs, the report).

## What Dan left open from the review (not part of this task)

He approved the files as delivered. The review points listed for him (the phone-holding man's cropped clip, the uncaptioned
"40", the deck-chair opener, the orange flare on the beach runner, the two label styles) were not raised; do not act on them.

## Starter prompt

> Read `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20261005-ad10-squares-thumbnail-and-setup-codex.md`
> and the files it lists. Name this session "My Dad Bod At 38 S/Sh Ad Setup". Set up the two approved Ad 10 squares (1:1 and
> 1:1 59s): make the 1:1 thumbnail that matches the approved Ad 10 design and the other ads' square thumbnails (recompose the
> existing plate; use the Codex subscription for any image generation), upload both to YouTube Unlisted, and add them to the
> Ad 10 group in the trial campaign in Google Ads without changing the budget or any live ad. Do not touch remarketing: ask Dan.
> Do not post anything organically. Do not use the dashboard. No em dashes.

Model and effort: GPT-6.1 Sol, High.
