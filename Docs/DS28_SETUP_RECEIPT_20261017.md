# CONTENT: Meal Prep SFC Setup

Updated: 2026-10-17. Job: DS-28. Status: covers ready for Dan's pick; no upload or scheduling performed.

## Approved film

Use the exact finalized R5 film. The project and Extreme master/SRT copies were hashed in this task and match the recorded approval at `Handoffs/video-editing/DS-28-R5-approval.json`.

- Master: `Short-form video content/Meal Prep - DS-28/Meal Prep SFC R5 - complete Short.mp4`
- Master SHA-256: `200afaaab059109b3fc168624136c0bb074d809d521d733ffee5b94ddf4298da`
- SRT SHA-256: `1e0c6077df27e05a6f22b04325269c8a0d82962ac21e8bf0ccd6ad8eebfe5d18`
- Exact closing words: "Subscribe for more ways to make time to get in shape."
- Classification: CONTENT, organic dedicated Short. The R5 approval and its historical measurements remain as recorded. No film, audio or caption edits were made.

## Cover review

Working folder: `Short-form video content/Meal Prep - DS-28/covers/round1/`.

Review sheet: `REVIEW-meal-prep-five-covers.jpg`. Full-size files: `youtube/1-meal-prep-cover.jpg` through `youtube/5-meal-prep-cover.jpg`, with separate matching Instagram layouts under `instagram/`. Both layouts are 1080x1920 RGB JPEG, and each file is under 2 MB. The sheet pairs YouTube's complete cover with Instagram's center profile crop. All five share the headline "Stop Cooking Your Meals".

1. Real pool photo: `photo-247_CUTOUT.png`, editorial serif headline, red rule and poolside prepared meals.
2. Real studio photo: `studio-blue-222_CUTOUT.png`, yellow/white condensed display type, green backdrop, white portrait keyline and large meal trays.
3. AI Dan: generated from `studio-white-23_FINAL_PRIMARY.jpg`, navy kitchen, prepared meals in hand, lower white/gold headline.
4. AI choice: overhead prepared meals, cream/orange composition and geometric green headline.
5. AI choice: microwave and clock, cinematic navy/blue composition and left condensed headline.

The two real portraits are original cutout pixels resized and composited in code over Codex backgrounds. They were not AI-redrawn. No website mark or real-photo label appears on a cover. AI provenance remains in the manifest. The AI reference reads as Dan and keeps his lean reference-size physique.

Generation: five calls through `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`, on the Codex subscription. No paid image API calls. Reported Codex tokens: 91,060. Prompts and generation logs are beside the assets. Generated plates were upscaled locally using Real-ESRGAN x4plus before the final cover export; the photographic cutouts were not upscaled by AI. The build recipe and manifest preserve text placement and source crops.

## Current setup state

- Local configs, waitlist, approval and receipts were inspected. A live Blotato schedule snapshot was saved privately as `live-queue-before.json`. It held 195 schedules and no exact DS-28 or "Stop Cooking" match. Capacity and actual release dates must be checked fresh after the pick.
- No cover has been approved yet. Selected option: PENDING.
- Google Drive filing, media uploads, the TikTok technical cover-first copy, platform copy, approved-cover URL verification, Facebook installer registration and four saved schedules all wait for Dan's pick.
- No YouTube holding upload. Blotato will create the organic YouTube release.
- The master fits Instagram without an encode. Use the maintained `tiktok_cover` helper only for TikTok's technical first-frame requirement, with copied audio and absolute paths.
- Pinned question: PENDING. Save one topical question in the final config; the existing daily routine posts and pins after release.
- Article: dedicated Short, deferred to `sixpackabs-article-gap-daily` after release, or its documented skip.
- Public cover verification: outstanding until release on YouTube, Facebook, Instagram and TikTok. The existing all-platform cover monitor handles the checks. Queued intentions are not proof of public tiles.
- Edit Queue: remains finalized. Do not mark uploaded unless all four saved schedules exist and read back correctly. If capacity is insufficient, use the shared waitlist and preserve finalized state.
- Dispatcher remains paused. Victory Dashboard untouched.

## Option 3 text revision, 2026-10-17

Dan selected the image concept for option 3 and requested larger text near the edges on its tall cover, plus clearer treatments for its shorter profile thumbnail. Final text approval is still pending; this is not authorization to upload the earlier files.

Revised assets: `Short-form video content/Meal Prep - DS-28/covers/round2/`.

- Tall: `3-tall-larger-text.jpg`. Two lines span about 1,010 px of the 1,080 px canvas, leaving about 35 px at either edge. The shorter second line is also enlarged to match the first line's width.
- Shorter A: `3-short-A-clean-navy.jpg`, larger white/gold Manrope on a clear navy field.
- Shorter B: `3-short-B-gold-panel.jpg`, dark condensed display text on a solid gold panel.
- Shorter C: `3-short-C-bold-display.jpg`, large condensed white/gold text with strong contrast and shadow.
- Review: `REVIEW-option-3-text-variations.jpg`, one revised tall cover, three 3:4 profile previews and three phone-size comparisons.

The exact existing AI image is reused. No new generation or film edit. Four full-size files decode as 1080x1920 RGB JPEG, are under 2 MB, and preserve face, hair, abdominal definition and the held meal trays. Text bounds are recorded in `manifest.json`; Instagram text ends by y=1620. Sources, outputs and the review sheet are backed up on Extreme with matching hashes. Recipe: `Handoffs/video-editing/DS-28-cover-review/round2-build.py` (pass the absolute round2 media folder as its positional argument).

Next: record Dan's shorter-cover pick A/B/C and updated tall-cover approval, then resume the original setup handoff. The film remains finalized; no uploads or schedules exist from this setup task.

## Exact next action

Record Dan's chosen cover number, then execute steps 3-8 of `Handoffs/handoff-20261017-ds28-meal-prep-setup.md`. Preserve the exact approved film. Complete backup filing and organic setup on YouTube, Facebook, Instagram @danrosefit and TikTok through the maintained Blotato clients. Reuse existing IDs on resume. No extra format, new film edit, per-video scheduling routine or direct Public YouTube upload.

Rebuild the covers from the tracked recipe with:

```bash
python3 Handoffs/video-editing/DS-28-cover-review/build.py "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/Meal Prep - DS-28/covers/round1"
```

The media, source plates and real photos stay out of the public Git repository.
