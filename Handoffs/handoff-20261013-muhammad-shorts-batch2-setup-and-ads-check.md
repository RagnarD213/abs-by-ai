# Muhammad shorts batch 2 (Hammer Curls, Fat Millionaire): setup, plus the ad check for all nine

**Category: CONTENT. Dedicated Shorts (`SFC`), edited by Muhammad. Written 2026-10-13 by Claude (Opus 5.5).
Task name: `Muhammad Shorts Batch 2 SFC Setup`.** One Claude handoff covers covers, picks, upload and queue
(Dan's rule, 2026-10-01). **Use the Codex subscription to generate the images.**

**Recommended model: Claude Opus 5.5, high effort.**

## Why this exists
Dan asked on 10-13 for a check that everything Muhammad delivered is in the ad campaigns. Result of that audit:

- **Muhammad's 13 ads (Ads 1 to 10, 13, 14, 15) are all on YouTube unlisted and all have ads in Google Ads.** Nothing to
  upload. Read live from the API on 10-13 (227 ad rows). Detail in "Audit record" below.
- **Muhammad's short-form batch is 22 dedicated Shorts, and every one is CONTENT, not an ad** (each ends on a comment
  call to action; he named three files "Ad 08", "Ad 09", "Ad 13" but they are DS-08, DS-09, DS-13). None is on YouTube
  yet, so none is in a campaign yet. They never go through `/ad-setup`. They go through `/video-setup`, and the
  engagement campaigns pick each one up by themselves at release (`scripts/ads/ytads/instant.js`, memory
  `ytads-retired-manual-management`).
- `Handoffs/handoff-20261012-muhammad-shorts-covers-and-setup.md` already covers seven of the finished shorts
  (DS-08, 09, 12, 22, 23 now; DS-14, DS-24 when their HD files arrive, and those arrived 10-13).
- **Two finished or nearly finished shorts are in no handoff: DS-21 and DS-05.** This doc covers them, and adds the
  one step no handoff has: proving each released short got its engagement ads.

## Goal
1. DS-21 How To Do Hammer Curls and DS-05 Why Having Abs Beats Being A Fat Millionaire: verify the HD file, make
   covers, stop for Dan's picks, then file and queue on YouTube, Facebook, Instagram @danrosefit and TikTok.
2. After any of the nine Muhammad shorts is public on YouTube, confirm it has ENABLED ads in the engagement campaigns.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full.
2. `Handoffs/handoff-20261012-muhammad-shorts-covers-and-setup.md` (same method: sections 2, 3, 4; do not repeat its videos).
3. `/video-setup` (Shorts section, waitlist section), `/coverimage`, `.claude/skills/_shared/IMAGE-GENERATION.md`.
4. `Docs/PINNED_COMMENTS.md`, `Docs/YTADS.md` ("CURRENT BEHAVIOR").

## 1. DS-21 How To Do Hammer Curls
- State: `in_progress`. One open note from the 10-12 check: the caption at 0:02.5 said "brax", asked to be "bracs".
- Muhammad sent a new file on 2026-10-13 09:42 UTC, labeled "How to do Hammer Curls" (no "HD" in his label; the other
  two links in that message say HD). Message: Gmail id `1a134a751d5802e9`, read it with `get_message` PLAIN_TEXT and
  resolve the third link. Never trust a Drive search for his files.
- Check before anything else: (a) size and bitrate are HD class (about 10 Mbps, not the 3.3 Mbps review size);
  (b) the 0:02.5 caption now reads "bracs"; (c) nothing else changed from V2, using
  `/Volumes/Extreme/_edit_work/revisions-20261012/muhammad/light.sh` and `fd.py` against `dl/08_hammercurls_hd`
  (expect a difference only around 0:02.5).
- All three pass: tell Dan in one line and set the Edit Queue row to `finalized` on his OK, then continue to covers.
  Any fail: stop, give Dan a paste-ready message for Muhammad in his voice (memory `editor-message-voice`).
- No AI clips recorded in this short: AI flag false unless the contact sheet shows one.

## 2. DS-05 Why Having Abs Beats Being A Fat Millionaire
- State: `finalized` (Dan approved Muhammad's V3 on 10-02). Edit Queue note: "HQ export owed". No HD file is on record.
- Search Muhammad's Upwork notification emails since 10-02 (`from:room_49041dfecc20c11fb2d7b9b0b8aac744@email.upwork.com`)
  for an HD link for this title. Found: prove it matches the approved V3 with the same frame subtraction check.
- Not found: give Dan this line to send, and carry on with DS-21 alone:
  "Hey Muhammad, can you send me the high quality export of Why Having Abs Beats Being A Fat Millionaire? That one is
  finalized, I just need the HD file. Thanks!"

## 3. Covers, picks, file, queue
Exactly as sections 2 to 4 of the 10-12 handoff: five cover choices per short (one pool photo, one studio photo, three
different AI designs, GPT-6.1 Sol high through `codex-image.sh`), one review page, stop for Dan's picks. Then upload
non-public, write the `"pinned_comment"` into each Blotato config, add to `scripts/blotato/video_waitlist.json` if
Blotato is full (never a one-off scheduled task), run `ad_guard.py --scan` before and after every Blotato write.
If the 10-12 task has not shown its cover page yet, offer Dan one combined review.

## 4. Ad check for all nine Muhammad shorts (after each release)
The three engagement campaigns: tier 2 `24122099676`, tier 1 `24163535721`, remarketing `24169507109`.
For each short, once its YouTube video is public:

```
node scripts/ads/api/client.js search "SELECT campaign.id, campaign.name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED'" --json
```

then match the video's asset (asset query: `asset.youtube_video_asset.youtube_video_id`) against the rows. Expect one
ENABLED ad per campaign, created within minutes of going public. Missing: look for `created` / `error` events with
`via: "instant"` and the Railway log line "YTADS instant". Do not pause, enable or remove anything on this path; report
what is missing to Dan. Nine shorts: DS-05, 08, 09, 12, 14, 21, 22, 23, 24.

## Audit record, Muhammad's ads in Google Ads (read 2026-10-13)
| Ad | YouTube 16:9 | Where it has ads | Running now? |
|---|---|---|---|
| 3 Stop Paying Human Trainers | `86jbUhqBTUQ` + 3 formats | trial campaign `24316364155` and conversion campaign | Yes |
| 4 Stop Wasting Money On Supplements | `R08TPEtkjuQ` + 4 formats | trial | Yes |
| 6 You're Not Too Old | `Je2yvk00SHE` + 4 formats | trial | Yes |
| 10 My Dad Bod At 38 / 40 | `Sg3vcEY2P_8` + 4 formats | trial | Yes |
| 13 What Getting Abs Was Supposed To Cost | Codex R4 `NQeyZ2jylVU` + 4 formats (Muhammad's `-SuKGXGcbIg` retired 10-05) | trial | Yes |
| 1 This Picture Got Me Abs | `lf46ytHacss` + 4 formats | conversion campaign only | No, campaign is paused |
| 2 Stop Wasting Money On Nutritionists | `Dtk5knWM7c8` + 2 formats | conversion campaign only | No |
| 7 In 2010 I Photoshopped My Face | `92A3JhaU4wE` | conversion campaign only | No |
| 8 AI Showed Me My Two Futures | `HMZdiJMAI3Y` + 2 formats | conversion campaign only | No |
| 9 I Tried To Get Abs With ChatGPT | `zvVk680kSfo` | conversion campaign only | No |
| 14 I Watched 400 Workout Videos | `SGJoPjnl6AU` (+ Codex R4 `ACfVyQqPK08`) | conversion campaign only | No |
| 15 The Dad Who Swam In A T-Shirt | `5GQQHP8bpM4` | conversion campaign only | No |
| 5 Every Diet You've Tried Failed | `bwfSQopZy1w` | one paused ad in the paused engagement remarketing campaign | No, and it has no conversion or trial ad |

All ads read APPROVED. "Conversion campaign" is `[DGEN] [CONVERSION] MU 25-54 | US+CA`, paused at campaign level.
Moving any of the eight idle ads into the live trial campaign is Dan's call and is not part of this task.

## Open risks
- Extreme drive must be mounted for the frame check scripts.
- DS-21 may still be review size; then the task is covers only after a second file from Muhammad.
- Spend: none expected (covers are on the Codex subscription).

## Exact next action
Rename the task `Muhammad Shorts Batch 2 SFC Setup`, read the files in "Read first", open Gmail message
`1a134a751d5802e9`, download the Hammer Curls file and run the three checks in section 1.

## Starter prompt (also in the chat message)
> Execute `Handoffs/handoff-20261013-muhammad-shorts-batch2-setup-and-ads-check.md`. Task name: `Muhammad Shorts Batch 2 SFC Setup`. Category: CONTENT, two dedicated Shorts (SFC) from Muhammad: Hammer Curls (new file arrived 10-13, check the "bracs" caption and that it is HD) and Why Having Abs Beats Being A Fat Millionaire (finalized, find or request the HD file). Make five cover choices per short, show them on one page and stop for my picks. Use the Codex subscription to generate the images. After my picks, upload and queue them for release. Then, as each of the nine Muhammad shorts goes public, confirm it got its engagement ads in Google Ads and tell me about any that did not.
