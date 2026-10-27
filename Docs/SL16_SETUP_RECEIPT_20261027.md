# SL-16 Intermittent Fasting Shorts: setup receipt (2026-10-27, Claude)

CONTENT (SFL), four Shorts cut from RO-08 "Intermittent Fasting: The Best Way To Get Abs". Approved films unchanged (hashes re-checked against `Short-form video content/fasting-SHORTS-final-manifest.json`).

## State: SHARED WAITING LIST (not yet scheduled in Blotato)
Blotato 189/200 and the parent RO-08 is itself still on the waiting list for Wed Nov 18, 2026 (its config `main`; the Jan 24, 2027 date in `Docs/RO08_SETUP_RECEIPT_20261014.md` is stale). Each Short entry carries `after` + `parent_config` = RO-08, so the daily `social-queue-daily-refresh` top-up queues it only once RO-08 is on Blotato and never on or before Nov 18. A dry run on GitHub's current main (temporary worktree, 2026-10-27) slots all four exactly on the dates below.

⚠ The main project folder is 67 commits behind GitHub (board JAM entry). Its `video_waitlist.json` names DS-40 and SL-08 configs that exist only on GitHub, so `video_topup.py` run from the main folder crashes until that merge lands. Nothing here changes that.

| # | Title (YouTube) | Release 9 AM Central | Cover | Config |
|---|---|---|---|---|
| 1 | How To Start Fasting: Just Skip Breakfast | Tue Dec 15, 2026 | F | `scripts/blotato/configs/sl16-short1-just-skip-breakfast.json` |
| 2 | Why Carbs Destroy Your Productivity | Fri Dec 4, 2026 | A2 | `scripts/blotato/configs/sl16-short2-why-carbs-destroy-your-productivity.json` |
| 3 | Never Break Your Fast With Alcohol | Mon Dec 7, 2026 | A2 | `scripts/blotato/configs/sl16-short3-never-break-your-fast-with-alcohol.json` |
| 4 | Why You Need A Simple Nutrition Plan | Tue Jan 12, 2027 | F | `scripts/blotato/configs/sl16-short4-why-you-need-a-simple-nutrition-plan.json` |

Dan, 2026-10-27, picks: "Short 1F, dumping breakfast, is approved... Short 2A with the new title is approved. Short 3A revised is approved. Short 4F, eating a salad, is approved." Titles changed by Dan: Short 2 "Why Carbs Destroy Your Productivity" (was Carbs Are Killing Your Workday), Short 4 "Why You Need A Simple Nutrition Plan" (was Life Will Punch You In The Face). Dates: the recommended set (Dan did not object); SL-22 What To Buy 1 moved to Fri Jan 15, 2027 and SL-14 40 vs 25 1 off Dec 4 (its parent is Jan 3, 2027). Calendar note in `Docs/SHORTS_RELEASE_CALENDAR.md`.

## Per Short
### 1. How To Start Fasting: Just Skip Breakfast
- Master `Short-form video content/fasting-short1_just-skip-breakfast.mp4`, 84,078,740 bytes, SHA-256 `e77bd982d5c4fe0113c2312211b77bdb73087af3b8c34afcf5f8c6eebe45b5b3`. AI flag true (true: approved workday time-lapse opener 0:00-0:07.7 (library A0169)).
- Cover F: Instagram `Short-form video content/covers/approved-sl16/Instagram_fasting-short1-how-to-start-fasting-just-skip-breakfast_cover-F.png` SHA `9708e55347b33aeddaff59f31ad35267be2113abc7800683269be5a5d8d39549`; YouTube JPEG 356,543 bytes SHA `3ef4b8f8896a191904958133cbe2776c93c07dbdc5be149a70cb5ae8afe90bda`.
- Blotato media (uploaded, downloaded back, SHA-256 equal): master https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/86118bbe-0b13-4ffe-9ccd-7028c83a7d08.mp4; TikTok cover-first https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/7c7a5cc0-e6cd-4997-aada-711595eb6132.mp4 (SHA `c39af8d594ff6a851f9bf4be869d464ff8f0c4bed5e7b5c6601c6c0ebe1ad132`, audio payload identical, one extra cover frame); IG cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/ee1b8c9d-2124-4245-8951-8ea7fea9dc80.png; YT cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/10ccf9f7-5fcd-4a1d-a38e-8b3800903ca8.jpg.
- UTM `utm_campaign=intermittent-fasting&utm_content=sl16-short1`, keyword FOOD.
- Pinned comment: "What time do you wake up, and what time do you eat your first meal?". Posts and pins automatically after release (routine youtube-pinned-comment-daily).
### 2. Why Carbs Destroy Your Productivity
- Master `Short-form video content/fasting-short2_carbs-are-killing-your-workday.mp4`, 82,792,998 bytes, SHA-256 `9da5c4a23772425ab091fff41fabd51c88434e4317a22e91f155484ed0a4834b`. AI flag true (true: donut-then-asleep AI clip 0:00-0:04 (A5)).
- Cover A2: Instagram `Short-form video content/covers/approved-sl16/Instagram_fasting-short2-why-carbs-destroy-your-productivity_cover-A2.png` SHA `9eb01ee3a122ff36ce93a89befc413ced7c0f609c9f8cc280959eea56cf1d6a0`; YouTube JPEG 357,685 bytes SHA `1b551da21d0ba73be3b9e8f376e37ab652de79e019a8dc8d8965f03577830213`.
- Blotato media (uploaded, downloaded back, SHA-256 equal): master https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/13ad30ab-4c2a-4bca-80b8-b266bfef6991.mp4; TikTok cover-first https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/25150452-7d58-4b98-9b89-a6785d4d9d74.mp4 (SHA `a72c09ed265056f2507d98da218cf28c890768e7d514d585e0ba74ec997ddc77`, audio payload identical, one extra cover frame); IG cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/1c667fe3-8cf7-4c32-a9cb-9c77bd9d323e.png; YT cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/64847440-d9bf-45f1-8bf5-6e7195c965c4.jpg.
- UTM `utm_campaign=intermittent-fasting&utm_content=sl16-short2`, keyword FOOD.
- Pinned comment: "Do you get that food coma feeling after lunch? What do you usually eat?". Posts and pins automatically after release (routine youtube-pinned-comment-daily).
### 3. Never Break Your Fast With Alcohol
- Master `Short-form video content/fasting-short3_never-break-your-fast-with-alcohol.mp4`, 50,188,974 bytes, SHA-256 `0f41a8db9aea880c657ea1d51ac133695b3311944fbd825966c2ca5c5077a452`. AI flag true (true: bar-stool sip 0:00-0:01.4 (library A0174)).
- Cover A2: Instagram `Short-form video content/covers/approved-sl16/Instagram_fasting-short3-never-break-your-fast-with-alcohol_cover-A2.png` SHA `4eea8ab5354e003d540b0f2fd73db207ab835b31e2d03421d90d36c1b41612ab`; YouTube JPEG 329,778 bytes SHA `020c9539f59feb9365b38af380a71d1c2000078027c1ef0c547d911f3c57d7a1`.
- Blotato media (uploaded, downloaded back, SHA-256 equal): master https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/7e9d21f7-3d4e-41d9-90a4-e685a8505f34.mp4; TikTok cover-first https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/b1ea6353-4c3b-462e-a968-52ddc0f8be33.mp4 (SHA `144b6d79fffd561fe1dd72d94def20be7822386688c900fdd9ed5461a89aabef`, audio payload identical, one extra cover frame); IG cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/6ebb69f6-8bd0-44d6-a162-d81b59426923.png; YT cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/bf5f82fc-f4b7-40ee-892e-a4f5adbceecc.jpg.
- UTM `utm_campaign=intermittent-fasting&utm_content=sl16-short3`, keyword FOOD.
- Pinned comment: "Have you ever broken a fast with alcohol? If so, what were you drinking?". Posts and pins automatically after release (routine youtube-pinned-comment-daily).
### 4. Why You Need A Simple Nutrition Plan
- Master `Short-form video content/fasting-short4_life-will-punch-you-in-the-face.mp4`, 76,226,377 bytes, SHA-256 `ae9c7d1ba2088ba20d798b08eb50d2df0bf48d982b852681939ce884bdecb34b`. AI flag true (true: boxing-glove gag 0:06-0:09 (library A0158)).
- Cover F: Instagram `Short-form video content/covers/approved-sl16/Instagram_fasting-short4-why-you-need-a-simple-nutrition-plan_cover-F.png` SHA `b28015951498efbb353ccd19f00e9348a1a60a2e92f53edaeecf81214e803bcd`; YouTube JPEG 290,420 bytes SHA `a0b4d0a239c3c8b2f2a0130fefa09dd1751171973b5fe7dc76aab0798047a426`.
- Blotato media (uploaded, downloaded back, SHA-256 equal): master https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/0de23080-054d-4ee0-a182-f3cf89aba403.mp4; TikTok cover-first https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/2ef9b830-5488-4087-bd01-aef403e73441.mp4 (SHA `bcbb0dd00b69a96e3fed6ded326a2026d094ddfabe67fc304b901f8ec8b0bacb`, audio payload identical, one extra cover frame); IG cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/5285bff7-4625-4ef8-ada0-7993eed7985d.png; YT cover https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/a04b7d56-c093-40d1-b651-1db0fc64e3ec.jpg.
- UTM `utm_campaign=intermittent-fasting&utm_content=sl16-short4`, keyword FOOD.
- Pinned comment: "What knocks you off your diet most: work, family, being sick, or something else?". Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- Photo credit in YouTube description and every caption: "Photo of Mike Tyson: Glenn Francis, www.PacificProDigital.com (CC BY-SA 4.0)".

## Backups
- Google Drive `Short-form video content/fasting SL-16` (anyone with the link): https://drive.google.com/open?id=1bPYc4D7u0bPo-k58GhlLcVNKrYz9Kivq. Masters (byte counts equal), `.srt` sidecars from each build's delivered cue map, approved covers + `picks.json`.
- Extreme `/Volumes/Extreme/Short-form video content/Intermittent Fasting Shorts - SL-16/`: masters (SHA equal), `.srt`, approved covers. Also the build copies in `/Volumes/Extreme/_edit_work/SL-16/build/`.
- Publish work: `/Volumes/Extreme/_edit_work/sl16-publish/` (uploads.json, tiktok-verification.json, prepared-post-plans.json).

## Covers and checks
- Codex `gpt-6.1-sol` high on the subscription: 20 first-round pictures + 6 revisions, no paid API. Round 1 mix: A/B AI Dan, C real studio photo (real pixels, generated background), D wrong-vs-right split, E AI Dan. Review pages: `Short-form video content/covers/review/sl16-20261027/` (index.html, round2.html). Recipe copy: `.claude/skills/shorts/reference/softblue-sl16/setup-recipe/`.
- QC PASS on all 54 files (text 30 px or more clear of the person, grid-safe, YouTube under 2 MB); every AI face checked against the real reference by eye; TikTok frame 0 inspected.
- Facebook covers registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/` (sl16-short1..4); 16 planned posts passed `cover_guard` preflight. `ad_guard.py --scan` CLEAN before and after.

## Still open (owned by routines, not Dan)
- Top-up routine queues the four (4 posts each) after RO-08 is on Blotato; then `queue.py set SL-16 uploaded` + Edit Queue sync, and replace the board entry.
- After each release: public cover check on all four platforms (`check-youtube-shorts-covers`), pinned comment routine, sixpackabs article routine (writes or skips Shorts).
