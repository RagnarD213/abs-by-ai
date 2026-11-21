# Ad 13 "The Cost Of Getting Abs": thumbnail, YouTube and Google Ads for the approved vertical and its 59 second cut

Written 2026-10-03, rewritten 2026-10-04 for **Codex** at Dan's request. Recommended: **GPT-6.1 Sol, High** (one matching
thumbnail from an approved design, then a checklist of uploads and API calls). Sidebar name:
`The Cost Of Getting Abs V/Sh Ad Setup`.

Dan approved everything on the round 3 page on 2026-10-03: *"All right, everything is looking good. Everything is
approved. Give me the handoff to install or upload these and set these up."* On 2026-10-04: *"Change both of these
handoffs to be for Codex."* The approval is recorded with file hashes in
`/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review3/decisions.json`.

**Where things are.** This handoff, the two videos and the thumbnail sources are in the MAIN project folder,
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/`, and this handoff is not on GitHub yet (the main folder's push
is stopped, see Traps). If you work in a worktree, read and write the media, thumbnails and this file by that absolute
path; every relative path below is relative to that folder.

Read first: `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (in full), `Handoffs/video-editing/00-RULES.md` (Codex
column and environment table), `.claude/skills/ad-setup/SKILL.md` (the method), `Docs/DGEN_CONVERSION_CAMPAIGN.md`
(sections "2026-10-02: new thumbnails on the trial campaign's 12 ad videos" and "2026-10-02: RA-01 1:1 square added to
the trial campaign": that square is the model for adding a format to an existing group), `Docs/AD_VIDEO_IDS.md`. The
Ad 6 setup handoff written the same week is the nearest worked example:
`Handoffs/handoff-20261004-ad6-formats-thumbnails-and-setup-codex.md`.

## The two approved files

Folder: `Muhammad Ad Videos/i added up what getting abs was supposed to cost - ad 13/` (main project folder, not in git).

| file | size, length | sha256 |
|---|---|---|
| `i added up what getting abs was supposed to cost \| claude \| 9x16 \| ad 13.mp4` | 1080x1920, 4:04.878 | `4a6f058e203dbd41965f34b0ebc4b5d1c9a90badf0bec96bd9afda1da472df60` |
| `i added up what getting abs was supposed to cost \| claude \| 9x16 59s \| ad 13.mp4` | 1080x1920, 0:54.288 | `8bb442a0331c9884a49472bea1678ca41ab4f787922a724c4d0aba65f2bfc5e7` |

Each has its delivery gate (2.4.0, 39 rows) and audio gate stamp beside it, both PASS, and every cut was watched by
independent judges with 0 open defects. **Re-hash both before uploading. If a hash differs, stop and say so.** Do not
re-encode, trim or re-mux them.

## Not part of this task

- **The new horizontal and the square files.** Dan approved their look, but neither is final: the horizontal still
  needs zoom steps at three cuts and a gate pass, and no square file exists yet. They are built in
  `Handoffs/handoff-20261003-ad13-round4-horizontal-and-square-codex.md` and set up afterwards the same way as here.
- Muhammad's 16:9 master, already live as `-SuKGXGcbIg`. Leave it and its ad exactly as they are.

## Work, in order

1. **Classify from the file.** The full ad and the cut both end "Tap the button below to get started." That is an ad:
   `/ad-setup` only, **Unlisted**, never Public, never organic, never Blotato. Filing is already done.

2. **Titles, descriptions, tags.** The 16:9's description is `youtube-description.md` in the ad folder. The full
   vertical shares the 16:9's timeline exactly (the same 7,339 frames), so its chapters carry over; the 59 second file
   gets no chapters. Write one description file per upload beside the existing one, named the way the Ad 8 folder names
   its own (`youtube-description-vertical.md`, `youtube-description-vertical-59s.md`). Titles follow the pattern the
   other ads' verticals use in `Docs/AD_VIDEO_IDS.md`. `--synthetic true` on both (the new AI robot opener and
   Muhammad's AI clips; the 16:9 is set the same way).

3. **One 9:16 thumbnail that matches the approved Ad 13 design (no five-choice round, no stop).** Dan already picked
   Ad 13's thumbnail for the trial campaign: option **13-R3B**, installed on the 16:9 as
   `social media graphics/youtube/thumbnails/_trial-campaign-20261001/FINAL APPROVED/Ad 13 | 16x9 | FINAL.jpg`. Every
   other ad in that campaign carries its one approved design in each shape it runs (`Ad 3 | 9x16`, `Ad 10 | 9x16`,
   `RA-01 | 9x16` in the same folder), and on 2026-10-04 Dan asked for exactly this on Ad 6 ("create the thumbnail
   images matching the other ones"). So:
   - Build **`Ad 13 | 9x16 | FINAL.jpg`** in the 13-R3B design: the same approved picture elements, plate, type and
     accent, laid out for 9:16 the way the other ads' 9:16 finals are. Build code and sources:
     `scripts/covers/trial-campaign-20261001/` (`round3/` holds 13-R3B; `round2-square/build.py` shows how a new shape
     was made from an existing plate with no new generation).
   - Reuse the approved elements exactly. If the plate has to be extended for the taller frame, that background
     extension is the only image generation allowed, and it goes through the Codex subscription image tool
     (`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`), never a paid API. **Use the Codex
     subscription to generate the images.** Any real photo of Dan in the design is never redrawn: his cutout and the
     type are layered on in code.
   - No new wording and no claims in thumbnail copy: the words are the ones on the approved 16:9.
   - Check it beside the other ads' 9:16 finals: head and text inside the frame, nothing cut, same weight and spacing.
     Save it in `social media graphics/youtube/thumbnails/Ad 13 What Getting Abs Cost/trial-20261001/` and copy it into
     `_trial-campaign-20261001/FINAL APPROVED/`.
   - The one 9:16 thumbnail serves both uploads. Show Dan the image in the final report; a thumbnail can be swapped
     later with `scripts/youtube/set-thumbnail.js`. (The 1:1 version waits for the square files.)

4. **Upload both Unlisted** with `scripts/youtube/upload.js --privacy unlisted --synthetic true --thumbnail <file>`
   (the script refuses Public). Read back on each: `privacyStatus: unlisted`, `processingStatus: succeeded`,
   `embeddable: true`, not made for kids, the custom thumbnail served (save a `readback-<id>.jpg` beside the final, as
   the 10-02 install did). Never use YouTube's scheduling or publish-at path.

5. **Google Ads: the trial campaign `24316364155` only.** Ad 13's group is `204553316830`; its live ad is the 16:9
   `826635661894`.
   - Add two ads to that EXISTING group, one per new video, the way the RA-01 square was added
     (`scripts/ads/api/dgen-ra01-square.js` with `dgen-ads/ra01-square.json`; readback `ra01-square.result.json`).
     Headlines, long headlines and descriptions are **read back from the live ad `826635661894` and reused unchanged**
     (Dan rewrote them himself on 10-01; write no new line). Final URLs follow the campaign's pattern:
     `utm_campaign=dgen-trial-ad13&utm_content=claude-vertical-vsl` and `claude-vertical-59s-vsl` (match the exact
     spelling the Ad 10 vertical ads in this campaign use).
   - `validateOnly` first, then apply. Ads ENABLED inside the existing group. **Budget, bids, audience, the 16:9 ad
     and every other ad stay exactly as they are.** Never enable a paused campaign.
   - Then bring the two PAUSED remarketing copies (`24305381214`, `24316408288`) in step, as the doc's "Keeping it in
     step with the cold campaign" note says: `node scripts/ads/api/dgen-rmktg-campaigns.js a --no-frequency-cap
     --apply`. It adds only the missing ads. They stay paused.
   - Leave alone: the old Demand Gen campaign `24243839443` (PAUSED; it holds older Ad 13 groups) and Performance Max
     `24308574894` (at its five-video limit with the Ad 13 16:9 among them). If you think a new format should replace a
     video there, say so in the report as an option; do not change it.
   - Run `node scripts/ads/api/client.js policy 24316364155` after the apply and record each new ad's status.

6. **Record it.** `Docs/AD_VIDEO_IDS.md` (two rows), a dated section in `Docs/DGEN_CONVERSION_CAMPAIGN.md` (video ids,
   asset ids, ad ids, URLs, policy status, the recheck date one day later), the Edit Queue (`python3
   scripts/edit-queue/queue.py set AV-11 uploaded --by "Codex"`, then `queue.py push`; `AS-10` stays open until the
   square exists), your own board line in `AI_COORDINATION.md` (the Ad 13 line in its HANDOFFS section: keep the round
   4 half, drop the setup half), and this handoff's row in `Handoffs/README.md`. Check off a dashboard row only if
   every ad that row names is now in.

7. **Report to Dan in plain language:** the two YouTube links, the thumbnail (send the image), what was added to which
   ad group, that the budget is unchanged, that nothing was posted organically, each new ad's policy status, and the
   date of the policy recheck.

## Traps

- **An ad never goes organic and never uploads Public.** "All platforms" in any wording is not authorization.
- Nothing here authorizes pausing, replacing or editing the live 16:9 `-SuKGXGcbIg` or its ad.
- A new thumbnail or a new ad can sit in `REVIEW_IN_PROGRESS` for a day; that is normal. If one comes back limited or
  disapproved, follow the retry rule in `Docs/DGEN_CONVERSION_CAMPAIGN.md` (tamer copy is not yours to write here:
  report it).
- In the 59 second cut the same trainer-on-his-phone clip appears at 0:12 and again at 0:24. Dan was shown this and
  approved the cut as is.
- Secrets come from `~/.absbyai-secrets.env` and the Railway CLI. Never ask Dan for a key and never paste one.
- The main project folder's push has been stopped by other sessions' uncommitted edits since 10-01 (see the board).
  From a Codex worktree, commit only your own files and push with plain git. Do not touch the unpushed kit commits.
- No em dashes in anything written (titles, descriptions, docs, the report).

## Starter prompt

> Read `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20261003-ad13-vertical-setup-codex.md`
> and the files it lists. Name this session "The Cost Of Getting Abs V/Sh Ad Setup". Set up the two approved Ad 13
> files (9:16 and 9:16 59s): make the 9:16 thumbnail that matches the approved Ad 13 design and the other ads'
> thumbnails (use the Codex subscription for any image generation), upload both to YouTube Unlisted, and add them to
> the Ad 13 group in the trial campaign in Google Ads without changing the budget or the live 16:9 ad. Do not post
> anything organically. No em dashes.

Model and effort: GPT-6.1 Sol, High.
