# Muhammad dedicated shorts, all nine: covers, release queue and the ad check

**Category: CONTENT. Dedicated Shorts (`SFC`), edited by Muhammad. Written 2026-10-13 by Claude (Opus 5.5).
Task name: `Muhammad Shorts Batch SFC Setup`.** One Claude handoff covers covers, picks, filing and queue
(Dan's rule, 2026-10-01). **Use the Codex subscription to generate the images.**

**Recommended model: Claude Opus 5.5, high effort** (cover design is judgment work; the queue half is scripted).

**This is the only handoff to fire for Muhammad's shorts.** It replaces
`handoff-20261012-muhammad-shorts-covers-and-setup.md` (superseded 10-13, do not run it) and is self-contained.

## Why this exists
Dan asked on 10-13 for a check that everything Muhammad delivered is in the ad campaigns, then for one handoff that
covers everything.
- Muhammad's 13 ads are all on YouTube unlisted and all have ads in Google Ads. Nothing to upload, and they are out of scope here.
- Muhammad's short-form batch is 22 dedicated Shorts, **every one CONTENT, not an ad** (each ends on a comment call to
  action; he named files "Ad 08", "Ad 09", "Ad 13" but they are DS-08, DS-09, DS-13). None is on YouTube yet. They go
  through `/video-setup` only, never `/ad-setup`. The engagement campaigns pick each one up by themselves at release
  (`scripts/ads/ytads/instant.js`, memory `ytads-retired-manual-management`).

## Goal
Take nine Muhammad shorts to "queued for release on YouTube, Facebook, Instagram @danrosefit and TikTok", each with a
cover Dan picked, then confirm each one got its engagement ads once it is public.

| Group | Shorts | What stands between it and covers |
|---|---|---|
| A, ready | DS-12, DS-23, DS-08, DS-09, DS-22 | Nothing. HD files in hand and proven |
| B, HD arrived 10-13 | DS-14 Reduce Alcohol, DS-24 Rear Delt Flys | Download and prove the HD file (section 2) |
| C, new file 10-13 | DS-21 Hammer Curls | Three checks, then Dan's OK to finalize (section 3) |
| D, HD owed | DS-05 Fat Millionaire | Find or request the HD file (section 4) |

**Not in this task:** DS-25 How To Do M100s (`blocked`, Dan is filming the B-roll) and the 12 shorts still in revision
rounds.

## Decisions already made
- Dan finalized DS-08, 09, 12, 14, 22, 23, 24 on 10-10 and 10-12, and DS-05 on 10-02. DS-21 is `in_progress`.
- Completed videos only: a short gets covers and a queue slot only once it is finalized and its HD file is proven.
- Never re-render or re-edit these files. Muhammad's audio is delivered untouched.
- Run the classification step and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full.
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop, five choices).
3. `/video-setup`, "Shorts" section, the waitlist section and "YouTube Shorts cover verification".
4. `Docs/PINNED_COMMENTS.md` and `Docs/YTADS.md` ("CURRENT BEHAVIOR").
5. Closest worked example: `Handoffs/handoff-20261008-sl03-daily-salad-shorts-covers-and-setup.md` and its receipt.
6. `revision docs/shorts-hd-check-muhammad-10-12-26.summary.md` (how the HD files were proven).

## 1. Group A: the five files ready now
In `/Volumes/Extreme/_edit_work/revisions-20261012/muhammad/dl/<folder>/`. All 1080x1920, about 30 fps, 10.6 to 12.9
Mbps, captions burned in. Re-hash before any use; a mismatch means stop and tell Dan.

| Job | Title | Folder | Length | sha256 (first 16) | Drive id | AI clips inside? |
|---|---|---|---|---|---|---|
| DS-12 | Top 3 Ways To Looksmax | `01_looksmax_hd` | 57.0 s | `6d8ba7e870ad2bc6` | `156EDpDaeEGr_pzJnIyKWgjCU2ZAlSPFa` | Yes (opener, cliff couple, jawline) |
| DS-23 | How To Do Side Laterals | `02_sidelaterals_hd` | 49.6 s | `1b3e9e9517452377` | `1k9UGUaIhrFG-Ds8sJUm49q4w5sqoG8ut` | No |
| DS-08 | I Was 200 Pounds At 38 | `04_ad08_hd` | 50.3 s | `83575ea52d874723` | `10xDY9fZ-FWAcZwXx7PTx_yVniHn1BxPP` | Check the cut (not confirmed) |
| DS-09 | How To Make Time To Work Out | `05_ad09_hd` | 63.7 s | `cc06dcb57d182511` | `1wp3aCo0SrXNdsrcWI9FljCAYWYybBkTd` | Yes (opener, student, robot) |
| DS-22 | How To Use The Ab Wheel | `07_abwheel_hd` | 44.6 s | `75fd5b4fa1997000` | `1KOmiZVmBN8zBWm_by9qh_3tw9N9WB07E` | No |

- **AI flag:** set YouTube synthetic and TikTok `ai_generated` to true only on shorts with realistic AI video clips
  (confirm DS-08 from its contact sheet). A labeled still goal image alone does not set it.
- **DS-09 is 63.7 s.** Check each platform's Shorts or Reels length limit in `/video-setup` before queuing it; if a
  platform refuses it, tell Dan. Do not trim it.
- Scripts and what each short is about: `Handoffs/video-editing/DS-<nn>-*.md`.

## 2. Group B: DS-14 and DS-24, HD files arrived 2026-10-13
Muhammad's message of 10-13 09:42 UTC, Gmail id `1a134a751d5802e9` (read with `get_message` PLAIN_TEXT and resolve the
links; never trust a Drive search for his files). Links labeled "3 Ways To Reduce Alcohol HD" and "How to do Rare Delt
HD". Not yet downloaded or checked.
- Prove each export is the finalized cut:
  `/Volumes/Extreme/_edit_work/revisions-20261012/muhammad/light.sh <name> <new file> <review copy>` then
  `python3 fd.py <name>` in that folder (same frame count; average difference under 3; largest pixel difference under
  about 40). Review copies: `dl/06_alcohol_hd` and `dl/03_reardelt_hd`. Also confirm HD class bitrate (about 10 Mbps).
- Reduce Alcohol has AI clips (opener and seltzer): AI flag true. Rear Delt Flys: false.
- A fail: stop on that short, give Dan a paste-ready message for Muhammad in his voice (memory `editor-message-voice`),
  carry on with the rest.

## 3. Group C: DS-21 How To Do Hammer Curls
- One open note from the 10-12 check: the caption at 0:02.5 said "brax", asked to be "bracs".
- Same 10-13 message, third link, labeled "How to do Hammer Curls" (no "HD" in his label).
- Check: (a) HD class size and bitrate, not the 3.3 Mbps review size; (b) the 0:02.5 caption now reads "bracs";
  (c) nothing else changed, using `light.sh` and `fd.py` against `dl/08_hammercurls_hd` (expect a difference only
  around 0:02.5).
- All three pass: tell Dan in one line, set the Edit Queue row to `finalized` on his OK, and it joins the covers.
  Any fail: paste-ready message for Muhammad, and the task goes on without it. No AI clips recorded: flag false
  unless the contact sheet shows one.

## 4. Group D: DS-05 Why Having Abs Beats Being A Fat Millionaire
- `finalized` (Dan approved Muhammad's V3 on 10-02). Edit Queue note: "HQ export owed". No HD file on record.
- Search Muhammad's Upwork notification emails since 10-02
  (`from:room_49041dfecc20c11fb2d7b9b0b8aac744@email.upwork.com`) for an HD link for this title. Found: prove it
  against the approved V3 with the same frame check.
- Not found: give Dan this line to send, and carry on without it:
  "Hey Muhammad, can you send me the high quality export of Why Having Abs Beats Being A Fat Millionaire? That one is
  finalized, I just need the HD file. Thanks!"

## 5. File them
Follow `/video-setup` and `/editor-deliveries` naming: copy each proven file into the project's short-form delivery
folder under the standard name, to the Extreme drive, and to Google Drive (anyone with the link can view). Update the
Edit Queue row only at the end (`uploaded` is set after the queue write is read back, never before).

## 6. Covers (first half; stop for Dan's picks)
Five choices per short, each in both layouts (Instagram grid and YouTube), which count as one choice:
1. one real pool-shoot photo of Dan,
2. one real studio-shoot photo of Dan,
3. to 5. three AI-generated images, **each a different design** of Codex's choice (different layout, type treatment,
   color and concept; not one layout with three backgrounds).

- Make them with `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No Gemini or other outside
  image model. A real photo of Dan is never redrawn: Codex makes the background only, his real cutout and the type are
  layered in code.
- Rules that bite: no frowning photo, Speedo photos cropped at the waistband, text never over his face or any of his
  hair, abs visible, no "Real picture of me" label and no AbsByAI.com on a cover, no claims in cover copy.
- Exercise how-to shorts (Side Laterals, Ab Wheel, Rear Delt Flys, Hammer Curls): at least one choice shows the
  exercise itself.
- **One review page for every short that passed its checks**, one numbered sheet per short, so Dan answers in one line
  per short. Then **stop for Dan's picks**. A short still waiting on Muhammad gets its covers in a second pass.

## 7. Queue (second half, after his picks)
- Write each short's Blotato config (title, description, tags, cover, AI flag, `"content_type": "organic"`,
  `"pinned_comment"` with one easy question about that video).
- **Blotato is at its 200 cap.** Do not create a scheduled task or routine to queue a single video. Add each config to
  `scripts/blotato/video_waitlist.json` as `"kind": "short"`; the daily `social-queue-daily-refresh` routine
  (`scripts/blotato/video_topup.py`) queues them on Tue/Thu/Sat as room frees. If room exists today, queue directly
  through the `/video-setup` scripts instead, dry run before every `--apply`.
- YouTube: Blotato only. Never upload organic content to YouTube ourselves, never Public, never native scheduling.
- TikTok takes no cover image through the API; follow `/video-setup` for the cover-first copy or the phone step.
- After any Blotato write, re-read the saved schedule and run the ad guard scan.

## 8. Ad check (after each release)
Releases are spread over weeks, so this step outlives the session: write a setup receipt in `Docs/` listing each
short's release date, and put one board line with the first check date. Engagement campaigns: tier 2 `24122099676`,
tier 1 `24163535721`, remarketing `24169507109`. For each short, once its YouTube video is public:

```
node scripts/ads/api/client.js search "SELECT campaign.id, campaign.name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.id, ad_group_ad.ad.demand_gen_video_responsive_ad.videos FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED'" --json
```

and match the video's asset (asset query on `asset.youtube_video_asset.youtube_video_id`) against the rows. Expect one
ENABLED ad per campaign within minutes of going public. Missing: look for `created` / `error` events with
`via: "instant"` and the Railway log line "YTADS instant". Do not pause, enable or remove anything on this path;
report what is missing to Dan.

## Out of scope (Dan, 2026-10-13)
This task is the dedicated Shorts only. Do not touch Muhammad's 13 long ads: do not add, move, enable or copy any of them
into the trial campaign or any other campaign, and do not create or edit any ad by hand. The only Google Ads work here
is the read-only check in section 8.

## Open risks
- The Extreme drive must be mounted; the Drive ids in the table are the fallback source for group A.
- Groups B, C and D depend on Muhammad's files passing; each can drop to a second pass without holding the others.
- Up to 45 covers in one review is a lot: keep the page to one line of answer per short.
- Spend: covers are on the Codex subscription, no paid image calls. No other spend is expected.

## Exact next action
Rename the task `Muhammad Shorts Batch SFC Setup`, read the files in "Read first", re-hash the five group A files, open
Gmail message `1a134a751d5802e9`, download the three new files and run the checks in sections 2 and 3.

## Starter prompt (also in the chat message)
> Execute `Handoffs/handoff-20261013-muhammad-shorts-batch2-setup-and-ads-check.md`. Task name: `Muhammad Shorts Batch SFC Setup`. Category: CONTENT, nine dedicated Shorts (SFC) from Muhammad. Five are ready (Looksmax, Side Laterals, 200 Pounds At 38, Make Time To Work Out, Ab Wheel). Check the three files he sent 10-13 (Reduce Alcohol HD, Rear Delt Flys HD, and Hammer Curls with the "bracs" caption fix), and find or request the HD file for Why Having Abs Beats Being A Fat Millionaire. M100s is not part of this task. Make five cover choices per short (one pool photo, one studio photo, three different AI designs), show them all on one page and stop for my picks. Use the Codex subscription to generate the images. After my picks, file them and queue them for release. Then, as each one goes public, confirm it got its engagement ads in Google Ads and tell me about any that did not.
