# Queue covers: photo crops and grid-safe shift for three Codex covers

Prepared 2026-09-28 by Claude at Dan's request. Recommended model: Claude Opus 5.5, medium effort.

**Deadline: the 8 Hours in Bed reel and TikTok release Tue Sep 29, 5:00 PM CT. Do that one first.**

## Background

The earlier session finished installing all finalized covers. Every queued video from Sep 29 to Nov 5 now carries
a new-format cover on Instagram, TikTok, YouTube and Facebook. Dan reviewed the release page
(https://claude.ai/artifact/NU8UswGuNhdYFjTfo8WptC) and said "the rest are looking good." Two jobs remain, both
authorized by Dan in chat on 2026-09-28. Do not redesign anything or ask for design approval again.

Report and backups from the earlier session: `Short-form video content/covers/review/queue-bakeoff-20260924/final-installation-20260928/installation/`
(`INSTALLATION_REPORT.md`, `backup/schedules_after_round2_20260928.json` is the current queue snapshot).

## Job 1: shift three covers down so the grid shows the whole headline (Dan: "Yes, move the designs down so the grid shows the headline")

The covers are the Codex YouTube files in `Short-form video content/covers/review/next-five-redesign-20260922/finalized/upload/`:
`03-sleep-o1v3wPkNI2I.jpg`, `04-vacuum-QuswpGj635A.jpg`, `05-knee-bi_fpkW-3eE.jpg` (1080x1920).
Their first headline line sits around y 200 to 300. Instagram and TikTok profile grids keep only y 240 to 1680, so the top line is clipped.

- Make an Instagram/TikTok layout of each: the same image moved down so the badge and both headline lines sit at or below y 250,
  filling the top with the design's own dark top band and cropping the bottom photo edge. Keep everything else the same.
  Do not change copy, photo, colours or type. Check the 3:4 grid crop (y 240 to 1680) shows the full headline and that no text
  touches Dan's face or hair. Save beside the originals as `*-grid.jpg`. Do not overwrite the originals.
- Install the grid versions:
  - Instagram @danrosefit: schedules `3793987` (Sep 29), `3876754` (Oct 1) and `3876763` (Oct 6). Upload with
    `blotato_create_presigned_upload_url`, then call `blotato_update_schedule` in place with the WHOLE post and only
    `coverImageUrl` changed. Method: `.claude/skills/coverimage/SKILL.md`, the "SCHEDULED reel" section.
  - TikTok: schedules `4553182`, `4553187` and `4553194`. Rebuild frame 0 with `tiktok_cover.build()` from the ORIGINAL
    uncovered sources below, never the queued file. Upload the result, then update in place with the new `mediaUrls`
    and `videoCoverTimestamp: 0`.
    - Sleep: `.../cc405ea9-a393-4e85-93f8-bcacd6c277f5.mp4`
    - Vacuum: `.../78d23978-b285-4071-956e-eab86993bc7f.mp4`
    - Knee: `.../9fa9c84e-8448-4c59-9f52-6d4168f8f8ba.mp4`
    - All three sit under `https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/`.
    - The build must show frames +1, audio packets equal and cover PSNR at least 30.
- Leave YouTube and Facebook on the full-frame originals. Neither crops the grid that way.

## Job 2: tighten three photo posts (Dan's words below)

> "Crop the unnecessary space above my head into my side so that way it's a little bit more even with the way we crop the bottom.
> Just crop the front, the top, and the sides as much as possible while keeping Instagram dimensions."

The bottoms were already cropped at the waistband on 2026-09-27 (Speedo rule, `VIDEO-RULES.md`). Now trim the top and the sides
so the framing matches that tight bottom. Keep a little headroom and never cut hair. Keep the aspect between 0.8 and 1.91 so
Instagram accepts it; a tighter 4:5-to-1:1 frame is the likely target. Work from the queued image (below) unless a higher-resolution
original of the same crop exists.

| Post | Platform | Schedule | Releases (UTC) | Current image (uuid under the public_media path above, `.jpeg`) |
|---|---|---|---|---|
| Never start your day with carbs | Instagram | 4888428 | 2026-10-02 22:00 | `e781fdfe-a684-4767-9bd4-48fd295e9eca` (1080x980) |
| Never start your day with carbs | Facebook | 4888430 | 2026-10-07 22:00 | `bf2b393f-5b43-433e-bbbc-7bce1ec7a121` (1207x1098) |
| Weigh yourself every single day | Instagram | 4888434 | 2026-10-19 22:00 | `f1a94631-33e9-4b6a-902a-d8ecbdd264c0` (1000x688) |
| Weigh yourself every single day | Facebook | 4888439 | 2026-11-04 23:00 | `5208e40a-c943-4a4a-9c33-e624c4fc3951` (1000x688) |

Dan named "carbs" twice and "weigh" once. Apply each crop to both the Instagram and Facebook copies of that photo, so the
two platforms match. Swap with `blotato_update_schedule` in place, changing only `mediaUrls`.

## Verify, record, report

- Back up the full schedule list first. Afterwards, diff every record: only the intended field may differ.
  Run `python3 scripts/blotato/ad_guard.py --scan` before and after.
- Re-read every changed record. Download each new cover, TikTok frame 0 and photo, and look at it next to the grid crop.
- Republish the review page with the new images. Its source and builder are in the earlier session's scratchpad, which may be gone.
  If so, rebuild from the live queue and update the same artifact URL above.
- Facebook reel covers are set after publishing by the LaunchAgent `com.absbyai.fb-reel-covers`, which runs from
  `~/.absbyai/fb-reel-covers/`. Photo posts are not involved. No change is needed there for this job.
- Keep photos out of Git. Commit only scripts or notes. Then update this handoff, `Handoffs/README.md` and the
  "Queue covers" entry in `AI_COORDINATION.md`.

## Still open for Dan (do not act on it)

Row 16: the Sep 27 @danrosefit arm-workout reel (Blotato post 739230) failed to post, so the R5 cover has no destination.
Dan has not yet decided whether to re-post it with R5.

## Ready-to-paste starter prompt

> Execute `Handoffs/handoff-20260928-queue-cover-crops-and-grid-shift.md` in the Abs By AI project. First, before Tue Sep 29 at 5 PM CT, shift the 8 Hours, Stomach Vacuum and Knee covers down so the Instagram and TikTok grids show the full headline, and install them on those Instagram and TikTok schedules. Then tighten the top and sides of the "Never start your day with carbs" and "Weigh yourself every single day" photo posts on Instagram and Facebook, keeping Instagram dimensions. Verify every record and republish the review page. No redesign.
