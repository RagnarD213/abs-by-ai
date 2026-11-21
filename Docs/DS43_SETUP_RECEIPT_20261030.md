# Terry Crews Doesn't Eat Until 2 PM. He's Right. (DS-43): setup receipt, October 30, 2026

CONTENT (SFC). **HOLD: shared waitlist.** Saved slot Tue Dec 22, 2026, 6 PM America/Chicago (2026-12-23T00:00:00Z), phase 2, all four platforms. Live Blotato read 197/200, needs four places, 52 videos waiting ahead, so nothing is scheduled yet; the daily `social-queue-daily-refresh` top-up (`video_topup.py`) queues it. Dry run (`--assume-free 250`) places it exactly on Tue Dec 22 6 PM Central. Green screen, not kitchen. Schedule IDs: none yet (waitlist).

## Cover
Dan, 2026-10-30: "That looks great. Go ahead and install it." Round 4 revised C after three rejected rounds. Real cable-crossover frame of Terry (Muscle & Fitness behind the scenes, 74.4 s) full screen; AI Dan (Codex gpt-6.1-sol high, subscription, real identity reference) keyed in the left corner at a laptop in a black tank top; yellow band "Why Terry Crews Doesn't / Eat Until 2 PM". Hashes: `Short-form video content/covers/approved-ds43/picks.json` (Instagram PNG 44850b1b..., YouTube JPEG 4a2bbe0a..., 301,420 B). Copied beside the film on project, Extreme and Drive (`approved covers/`). History: `Docs/DS43_COVER_REVIEW_20261030.md`.

## Film and backups
- Approved off-the-cuff R2 unchanged: SHA256 b689924b939651379d3c991f9a3541002ceb1b77f725920a181d3d3dcc7ebda5, 97,019,454 B, 77.31 s; MD5 1ee19cd7073f96180fe7b5cbe1a1ee53. SRT MD5 a55694b1c8efcd3283461f1dd3abb655.
- Three copies: project folder, `/Volumes/Extreme/Short-form video content/Terry Crews Fasting - DS-43/` (SHA matches), [Google Drive](https://drive.google.com/open?id=1Tf1sUu2KWvFKT7WLGCakLJBZ4jHOzjq8) (MD5s match, anyone with the link).
- TikTok cover-first copy: `/Volumes/Expansion/_edit_work/ds43-publish/Terry Crews Fasting SFC R2 - TikTok cover-first.mp4`, SHA256 44ec6492cc629066e023d6028fa551cd280ad521b8ecf221c33707c666fab8f7, 2,318 frames (1 cover + 2,317), 3,625 audio packets, zero decode errors, builder cover check 48.66 dB.

## Blotato
Config `scripts/blotato/configs/ds43-terry-crews-fasting.json` (organic, kitchen false, gym false, ai_generated false, keyword FOOD, UTM campaign terry-crews-fasting / content ds43-terry-crews-fasting). Four uploads downloaded back and SHA-matched (`/Volumes/Expansion/_edit_work/ds43-publish/uploads.json`). Waitlist entry added. Facebook cover registered in `scripts/blotato/fb_reel_covers.json` and the live installer. ad_guard CLEAN, cover_audit zero issues. No direct YouTube upload, no native scheduling.

Title: Terry Crews Doesn't Eat Until 2 PM. He's Right. Runs 77.31 s: under Facebook's 90 s Reel norm and the other platforms' limits on record; not re-checked against live platform docs. YouTube description credits the clips: Business Insider, Muscle & Fitness, America's Got Talent, Old Spice. No em dashes.

Pinned comment: "What time do you eat your first meal of the day?". Posts and pins automatically after release (routine youtube-pinned-comment-daily). Written directly in this session, not through dan-voice-writer.

Article: dedicated Short, nothing at setup; the post-release routine writes or skips.

Calendar: `Docs/SHORTS_RELEASE_CALENDAR.md` Tue Dec 22 6 PM row = Waitlist. Edit Queue: DS-43 stays `finalized` until the top-up creates and reads back the four schedules.

Outstanding (existing routines): top-up queues the four posts, then public cover tiles on all four platforms, pinned comment, Facebook cover install.
