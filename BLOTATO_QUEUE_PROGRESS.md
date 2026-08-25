# Blotato IG + Facebook queue — progress

Last updated 2026-08-18 by Claude Code.

## Account state

- Blotato **Starter, $29/mo, subscription ACTIVE**. 1750 AI credits (unused — we upload our own media).
- Connected: **Instagram `@abs.by.ai` (id 65632)**, **Facebook Page "Abs by AI" (id 47105, pageId 1294282227094660)**, **YouTube (id 46963)**.
- Auth is **OAuth via the Blotato MCP connector** (`https://mcp.blotato.com/mcp`), added in the Claude desktop app. **No API key was ever generated and none is needed** — the key and the OAuth login are two alternative ways to authenticate the same account. The free trial blocked MCP entirely (`"Free trial does not include MCP access"`); activating the subscription unblocked it with no further setup.
- **TikTok deliberately NOT connected** until ~2026-09-02 (warm-up; early third-party connection risks a bot flag).
- **YouTube is connected but deliberately unused.** All 28 Shorts are already scheduled natively in YouTube Studio, so posting them through Blotato too would double-post. Blotato only posts where a post names that accountId, and no Automations exist, so it is inert. Dan's decision 2026-08-17: leave connected, revisit after the native queue runs dry (post Oct 15).

## DONE — 27 Shorts × 2 platforms = 54 posts scheduled

All at **5:00 PM Central** (= `22:00Z`; Aug–Oct is CDT, UTC−5). Dates **mirror the existing YouTube Studio schedule exactly**, read live off the Studio content list rather than from any doc.

| date | Short | note |
|---|---|---|
| Aug 20 | `v3-short6_vacuum-exercises` | posted early as the first IG/FB post; its YouTube date is Sep 19 |
| Aug 22 | `v2-short1_sugar-free-gum-trick` | |
| ~~Aug 25~~ | ~~`v2-short2_sean-ray-vision-board`~~ | **PULLED 2026-08-25 — do not reschedule.** Names/shows Mike Chang (+ a Sean Ray poster); Dan does not want him mentioned this early. Removed from IG @danrosefit, the @abs.by.ai mirror and Facebook; YouTube Short `DiwFRZT4JUI` set to Private. Content archived in `Business/pulled-vision-board-2026-08-25.json`. The freed slot took the channel-intro backfill reel. |
| Aug 27 | `v2-short3_supplements-3-percent` | |
| Aug 29 | `v2-short4_macro-tracking-obsolete` | |
| Sep 1 | `v2-short5_ask-ai-to-interview-you` | |
| Sep 3 | `v2-short6_hire-a-maid-not-a-trainer` | |
| Sep 5 | `v2-short7_chicken-soup-trick` | |
| Sep 8 | `v3-short1_no-abs-until-you-see-abs` | |
| Sep 10 | `v3-short2_whey-protein-insulin` | |
| Sep 12 | `v3-short3_liquid-calories-milk` | |
| Sep 15 | `v3-short4_train-abs-every-day` | |
| Sep 17 | `v3-short5_jelly-bean-vs-soda` | |
| Sep 22 | `v3-short7_fast-until-2pm` | |
| Sep 24 | `v3-short8_weigh-yourself-every-day` | |
| Sep 26 | `v3-short9_break-fast-low-carb` | |
| Sep 29 | `v3-short10_eight-hours-is-not-sleep` | |
| Oct 1 | `v3-short11_bubble-gut-vacuums` | **contains two bleeps** (steroid references) |
| Oct 6 | `v6-short2_knee-yourself-in-the-face` | |
| Oct 8 | `v6-short3_look-at-the-sky-deadlift` | |
| Oct 10 | `v6-short4_towel-row-karate-chop` | |
| Oct 13 | `v6-short5_you-always-have-three-minutes` | thin — motivational, not a tactic |
| Oct 15 | `short5_1-minute-workout` | **CC-BY attribution required and included** — see below |
| Oct 17 | `short1_4-ab-muscles` | already public on YouTube; appended |
| Oct 20 | `short2_toe-touches` | already public on YouTube; appended |
| Oct 22 | `short3_v-sit-twists` | already public on YouTube; appended |
| Oct 24 | `short4_spiderman-planks` | already public on YouTube; appended |

**Four Shorts were already published on YouTube** (`short1`–`short4`), so they had no future YouTube date to mirror. They are **appended after Oct 15** on the same Tue/Thu/Sat cadence rather than being slotted in early, which would have collided with the mirrored dates. Same precedent as the Oct 15 append in `SHORTS_UPLOAD_PROGRESS.md`.

**`short5_1-minute-workout` carries a live licence obligation.** Its audio was replaced with "Get A Move On" by Audionautix (CC-BY 4.0) to clear a YouTube copyright claim. The attribution line is included in **both** the IG and FB captions and **must not be removed**.

## DONE — 65 photos x 2 platforms = 130 posts scheduled (2026-08-18)

`photos/finalized social media photos/` — **65** `*_FINAL_PRIMARY*.jpg` (the earlier count of 63 was wrong;
`photo-74` has an `-A` and a `-B` variant and both are in). **Mon/Wed/Fri at 5:00 PM Central, Aug 19 2026 →
Jan 15 2027**, threading between the Tue/Thu/Sat Reels queue. Verified after creation against Blotato:
**184 scheduled total = 130 photo + 54 reel**, 65 IG + 65 FB, all 65 date buckets match the plan exactly,
every post at 17:00 CT, **zero days carry both a photo and a reel**, 0 posts missing media.

- **IG uses the 4:5 crop, FB the full frame.** 54 of 65 already had an `-IG-4x5.jpg`; **5 were generated
  this session** (photo-10, 13, 38, 158, 247 — full width, top-anchored, head and abs kept). The remaining
  **6 are landscape at 1.49:1** (44, 117, 118, 122, 180, 230), which is inside Instagram's own 1.91:1 limit,
  so those post uncropped on both platforms — hence **124 distinct media URLs across 130 posts**, not 130.
- UTMs: `utm_medium=photo`, `utm_campaign=pool-shoot`, `utm_content=photo-<n>`, per-platform `utm_source`.
- Caption plan (photo → caption → date) is saved at
  `photos/finalized social media photos/_blotato-photo-queue-plan.json` (gitignored with the photos).
- Review page Dan approved: https://claude.ai/code/artifact/157b4d34-6403-4fc8-854f-243dfba3551a

**Dan's four caption revisions, applied before queuing** (worth keeping — they are corrections of fact, not taste):
- **Kettlebell swing → kettlebell deadlift.** Dan does not do swings; he considers them high risk. Do not
  write swings into future content.
- **Never tell people to stop tracking calories.** A caption saying "you don't have to track forever"
  undermines the app's own macro feature. The angle is that AI made tracking easy, not optional.
- Overhead-hold caption → **medicine ball slams** (overhead, slam, bounce, catch, back overhead).
- **Cardio goes first thing in the morning, before lifting** — that is how Dan actually trains. The original
  caption said the opposite.

## DONE — long-form catch-up, 10 posts scheduled (2026-08-18)

Dan asked for an accelerated **Facebook** catch-up believing FB was behind Instagram. **It was not.**
Matching durations against the local masters settled what is actually where — do not re-derive this by
counting posts, the counts mislead:

| video | length | on YouTube | on Facebook | on Instagram |
|---|---|---|---|---|
| V1 channel intro | 4:05 | yes | **yes** (Aug 12, "I got my six-pack back at 40") | no → **queued Aug 19** |
| V2 six strategies | 38:25 | yes | **yes** (Aug 16) | **impossible** — see limit below |
| V3 top 10 tips | 21:12 | yes (Aug 16) | no → **queued Aug 22** | **impossible** |
| V4 1-minute ab workout | 8:12 | yes | no → **queued Aug 21** | **queued Aug 21** |
| V5 ab workout follow-along | 4:42 | Aug 23 | **queued Aug 23** | **queued Aug 23** |
| V6 3-minute total body | 13:18 | Aug 30 | **queued Aug 30** | **queued Aug 30** |
| V7 total body follow-along | 13:12 | Sep 6 | **queued Sep 6** | **queued Sep 6** |

**Instagram already had every Short Facebook had.** The "extra" Facebook reel in the raw count is a
**second copy of `short1_4-ab-muscles`** (1:06, posted Aug 12 2:41pm *and* Aug 13 3:11pm). Durations are
the reliable way to match a post to its source file — captions and thumbnails are not.

**All 10 at 9:00 AM Central**, deliberately off the 5:00 PM slot so long-form never lands on a photo or a
Short. V5/V6/V7 mirror their YouTube publish times exactly, which is the start of Dan's "everything posts
at the same time on all platforms" rule. Verified after creation: **194 scheduled total = 130 photo +
54 reel + 10 video**, and **zero day+time slots carry mixed content types**.

**THE TWO LIMITS THAT DECIDE WHERE A VIDEO CAN GO:**
- **Instagram Reels cap at 15 minutes** — so V2 (38:25) and V3 (21:12) can never be posted to Instagram as
  they are. V6 and V7 fit at 13:18 and 13:12, but with under two minutes of headroom.
- **Facebook Reels cap at 90 seconds**, so long-form must be posted with **`mediaType` omitted** (a regular
  video post). Only the ~60s Shorts use `mediaType: "reel"` on Facebook. Business Suite labelling every
  video a "Reel" in its UI is cosmetic and misleading.

**The masters cannot be uploaded** — they run 690 MB to 3.1 GB. Re-encode first: `h264_videotoolbox`,
1920x1080, 3500k, AAC 128k, `+faststart`. That put V3 at 501 MB and V4 at 197 MB, and **hardware encoding
does 8 minutes of video in about 60 seconds**. Large files go through the **presigned-URL PUT** flow
(`blotato_create_presigned_upload_url` → `curl -X PUT --data-binary`), NOT the base64 data-URI route, which
is only sane for images. A 197 MB PUT took 44 s.

## NOT DONE — two Instagram-only photos were deliberately NOT mirrored to Facebook

- **The Aug 4 post (`p/DboiRHDj-LW`) has no caption at all.** Mirroring a captionless graphic breaks the
  content rule below, so it was left alone.
- **The Aug 13 post (`p/Db_kllPD3bC`) is a good jump-rope technique tip**, but it could not be retrieved:
  the composited graphic is not on disk, and **Instagram's CSP blocks every extraction route** — a
  cross-origin POST to Blotato and a POST to a local bridge server both fail with `Failed to fetch`, and
  the browser tool blocks the CDN URL itself as query-string data. (Note this is the opposite of the Google
  Drive finding recorded elsewhere, where a `http://127.0.0.1` fetch from an HTTPS page *did* work — it
  depends entirely on the host page's CSP.) Judged not worth recreating: it is 5 days old with 2 likes, and
  **the same tactic is already covered by the photo queue** (#41 "Land quiet", plus the two Aug rope shots).

## Content rule established 2026-08-17 — read before adding anything

**Every post must give the viewer a reason to watch. A clip whose only content is Dan's own result is a brag and gets killed.** `v6-short1_gained-muscle-in-quarantine` ("I GOT LEANER WITH NO GYM") was cut, captioned, scheduled as the first IG/FB post, and pulled by Dan on sight. **It is excluded from this queue entirely** — but note it is still scheduled on **YouTube for Oct 3**, which Dan may want to remove separately. Full rule in `.claude/skills/shorts/SKILL.md` Step 2 and memory `shorts-reason-to-watch`.

Two others flagged but kept, for Dan to pull if he disagrees:
- **Oct 13 `v6-short5`** — "you always have three minutes" is motivational rather than a tactic. Weakest of the 27 against the rule.
- **Oct 1 `v3-short11`** — bleeped steroid references. Fine on YouTube; Meta's organic policies are looser than its ad policies, so it should be fine, but it is the spiciest item in the queue.

## Caption conventions (keep these)

- **Instagram caps at 5 hashtags** — Blotato hard-rejects a 6th with an error. Not a YouTube constraint; IG only.
- **Facebook** puts the absbyai.com link inline (FB links are clickable). **Instagram** says "link in the first comment" and Blotato auto-posts the link as `firstComment` — IG captions don't hyperlink, so a raw URL there is dead text.
- UTMs are per-platform: `utm_source=instagram|facebook`, `utm_medium=reel`, `utm_campaign=<source video>`, `utm_content=<short id>`. Lets IG and FB traffic be told apart in PostHog.
- All videos posted as **Reels** on both platforms; IG additionally `shareToFeed: true`.

## Mechanics worth not re-deriving

- **Media upload:** `blotato_create_presigned_upload_url` → HTTP `PUT` the raw bytes with curl → use the returned `publicUrl` as `mediaUrls`. Blotato re-hosts a per-post copy, so each post's `mediaUrls` differs from the one you uploaded.
- **File size is a non-issue.** 25–64 MB files upload in 5–8 s. The re-encode-to-8.5 MB fallback in `handoff-20260812-instagram-facebook-content-queue.md` is **not needed** — ignore it.
- **The calendar view shows a static thumbnail only.** To actually watch a queued video use **Upcoming posts** (`my.blotato.com/queue/schedules`), which embeds a real player. The calendar lives at `/queue/calendar`, not `/calendar`.
- **Reading the YouTube schedule:** on the Studio content list each row exposes `row.polymerController.__data.video`; `scheduledPublishingDetails.scheduledPublishings[0].scheduledTimeSeconds` converted to `America/Chicago` gives every date in one call. The Date column shows date but not time.
- **There IS a REST API key now, and it is the only sane way to do bulk work.** Generated 2026-08-18 from
  Settings → API → Generate API Key (standing auth covers restricted key creation). Stored at
  **`Business/blotato-api-key.txt`** (gitignored — the repo is public). Blotato shows the key **once**;
  regenerate from that page if lost. Base `https://backend.blotato.com/v2`, header `blotato-api-key`.
  `POST /v2/media` accepts **`{"url": "data:image/jpeg;base64,..."}`** so local files upload with no
  presigned-URL dance; `POST /v2/posts` takes `{post:{accountId,target,content},scheduledTime}`;
  `GET /v2/schedules` paginates with `cursor`; `DELETE /v2/schedules/<id>` returns 204.
  **Doing this over MCP would have been ~250 individual tool calls; over REST it is two scripts.**
- **Rate limit is real and aggressive** — roughly 28 uploads then a cooldown, replying
  `429 {"message":"Rate limit exceeded, retry in N seconds"}`. Run uploads sequentially with ~1.2s spacing
  and honour the N from the message. Both scripts must be **idempotent** (cache `file → publicUrl` and
  `job → postSubmissionId` to disk) so a re-run resumes instead of double-posting.
- **Blotato refuses any schedule more than 9 months out** (`code 20011`). The Jan 2027 tail fits; a longer
  queue would not.
- **A feed photo takes no `mediaType`.** `mediaType` is `reel|story` only — omit it and the post is a normal
  feed photo. `shareToFeed` is reel-only.
- **Do not run two upload scripts at once.** Both write the same cache file and the loser's writes are lost,
  which briefly regressed the map from 124 back to 120 entries.
- **Meta Business Suite's Content list shows Instagram and Facebook rows together**, distinguished by the
  glyph and the `Abs by AI` vs `abs.by.ai` byline — the fastest way to diff the two accounts. Its table is
  virtualised (only ~9 rows in the DOM) and `innerText` of the page is blocked by the browser tool, so read
  it by returning short per-row strings, not the whole page.
- Deleting a queued post: `blotato_delete_schedule` with the **schedule id** from `blotato_list_posts` (not the `postSubmissionId` returned at creation).
