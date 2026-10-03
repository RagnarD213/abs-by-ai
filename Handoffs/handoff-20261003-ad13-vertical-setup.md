# Ad 13 "The Cost Of Getting Abs": set up the approved vertical and its 59 second cut

Written 2026-10-03. Recommended: **Claude Opus 5.5, Medium** (thumbnails and ad copy need judgment; the uploads are a
checklist). Sidebar name: `The Cost Of Getting Abs AD Setup`.

Dan approved everything on the round 3 page on 2026-10-03: *"All right, everything is looking good. Everything is
approved. Give me the handoff to install or upload these and set these up."* Recorded with file hashes in
`/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review3/decisions.json`.

**Use the Codex subscription to generate the images.**

## What is ready to set up now (two files)

Folder: `Muhammad Ad Videos/i added up what getting abs was supposed to cost - ad 13/`

| file | length | sha256 | gates |
|---|---|---|---|
| `i added up what getting abs was supposed to cost \| claude \| 9x16 \| ad 13.mp4` | 4:04.878, 1080x1920 | `4a6f058e203dbd41965f34b0ebc4b5d1c9a90badf0bec96bd9afda1da472df60` | delivery gate PASS (39 rows), audio gate PASS, label check; stamps beside the file |
| `i added up what getting abs was supposed to cost \| claude \| 9x16 59s \| ad 13.mp4` | 0:54.288, 1080x1920 | `8bb442a0331c9884a49472bea1678ca41ab4f787922a724c4d0aba65f2bfc5e7` | delivery gate PASS (39 rows), audio gate PASS; stamps beside the file |

Re-hash both before uploading. If a hash differs, stop and say so.

## What is NOT ready (do not upload these in this task)

- **The new horizontal** (`round3/h16x9/DRAFT - Ad 13 16x9 Soft Blue Light round 3b - full.mp4`): approved in look, but
  Dan's approval includes adding zoom steps at three of Muhammad's cuts, and it has not passed the delivery gate.
- **The square and its 59 second cut:** only the look is approved; no square file exists yet.

Both are built in `Handoffs/handoff-20261003-ad13-round4-after-round3-page.md`. When that task delivers them with a
gate PASS, run this same setup on them (the horizontal is a NEW unlisted video and a new ad; it never replaces the live
`-SuKGXGcbIg`, which keeps running until Dan says to pause it).

## Work, in order (follow `/ad-setup`; read `.claude/skills/_shared/VIDEO-RULES.md` first)

1. **Classify from the file.** The full ad and the cut both end "Tap the button below to get started." That is an ad:
   `/ad-setup` only, Unlisted, never organic, never Blotato. Step 1 (filing) is already done.
2. **Titles, descriptions, tags.** Ad 13's 16:9 description is in the ad folder (`youtube-description.md`); adapt it
   for the vertical and for the 59 second cut (`youtube-description-vertical.md`, `youtube-description-vertical-59s.md`,
   as in the Ad 8 folder). Chapters only on the full vertical. `--synthetic true`: both files contain realistic AI
   footage (the new robot opener and Muhammad's AI clips).
3. **Thumbnails: five choices at 9:16, then stop for Dan's pick.** Standing rule (VIDEO-RULES, 2026-10-02): one pool
   photo, one studio photo, three AI designs of Codex's choice, made with
   `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. A real photo of Dan is never redrawn
   (Codex makes the background; his cutout and the type are layered in code). No claims in thumbnail copy (memory
   `thumbnail-no-claims`). Ad 13's approved 16:9 thumbnail is the trial-campaign robot design (`13-R3B` in
   `Docs/DGEN_CONVERSION_CAMPAIGN.md`); a 9:16 version of that design is a natural one of the three AI choices. The
   same pick serves the full vertical and the cut unless Dan says otherwise.
4. **Upload both Unlisted** with `scripts/youtube/upload.js --privacy unlisted`, set the thumbnail, read back
   `privacyStatus: unlisted`, `processingStatus: succeeded`, `embeddable: true`. Uploads may run before the thumbnail
   pick; install the thumbnail after Dan picks.
5. **Google Ads.** Ad 13 already runs as the 16:9 `-SuKGXGcbIg` in the Demand Gen conversion campaign `24243839443`
   and in the trial campaign `24316364155` (ids in `Docs/DGEN_CONVERSION_CAMPAIGN.md`). Add the two new videos as
   more `videos` entries on the existing Ad 13 config (`scripts/ads/api/dgen-ads/`), dry run, then `--apply`; the
   builder reuses the groups, audience and copy. Keep the shared budget exactly as it is and never enable a paused
   campaign. For the trial campaign and its paused remarketing copies, follow that doc's "Keeping it in step" note and
   the five-video limit per ad it records: if adding these would pass a limit, list the options for Dan, do not drop
   a running video yourself. Copy: reuse Ad 13's current headlines (Dan rewrote the trial ads' headlines himself on
   10-01; do not overwrite his lines).
6. **Record it:** `Docs/AD_VIDEO_IDS.md` (two rows), a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the Edit
   Queue (`AV-11` to `uploaded`; `AS-10` stays open until the square exists), the board line, and the policy re-check
   date. Check off the dashboard row only if every ad it names is in.
7. Report in plain language: the two links, what was added where, the budget unchanged, that nothing was posted
   organically, and the thumbnail choices waiting for his pick.

## Traps

- Nothing here authorizes pausing or replacing the live horizontal `-SuKGXGcbIg`.
- The Blotato ad guard knows ad titles; this ad never goes near Blotato.
- The main folder's push is currently stopped by other sessions' uncommitted edits (`VIDEO-RULES.md`,
  `framing-motion.md`, `render.py`); `scripts/git/safe-push.sh` will say so. Report it, do not work around it.
- No em dashes in anything written.

## Starter prompt

> Read `Handoffs/handoff-20261003-ad13-vertical-setup.md` and the files it lists. Name this session "The Cost Of
> Getting Abs AD Setup". Set up the approved Ad 13 vertical and its 59 second cut: descriptions, five 9:16 thumbnail
> choices (use the Codex subscription to generate the images) and stop for my pick, upload both to YouTube Unlisted,
> and add them to the Ad 13 groups in Google Ads without changing the budget. Do not post anything organically and do
> not touch the live horizontal.

Model and effort: Claude Opus 5.5, Medium.
