# Why I Stopped Drinking Coconut Water (DS-49): setup receipt, October 29, 2026

CONTENT (SFC). **HOLD: shared waitlist.** Saved slot Mon Dec 21, 2026, 6 PM America/Chicago (2026-12-22T00:00:00Z), phase 2, all four platforms. Blotato was 200/200 at setup, so nothing is scheduled yet; the daily `social-queue-daily-refresh` top-up (`video_topup.py`) queues it when four places free. Dry run (`--assume-free 250`) places it exactly on Mon Dec 21 6 PM. Kept one week after "3 Healthy Foods 1: Coconut Water Is Just Sugar Water" (SL-19, Dec 14); the earlier open Nov 23 slot is held for DS-84. Poolside film, not kitchen.

## Cover
Dan, 2026-10-29: "Let's go with G. Install G on all platforms." Round 2 G: AI Dan (Codex gpt-6.1-sol high, subscription, real identity reference) pouring a coconut water carton into a black sink in an outdoor kitchen at golden hour, thumbs up, yellow band "Why I Stopped Drinking / Coconut Water". Round 1 A (trash can) was liked but the trash made no sense; Dan asked for sink versions. Files and hashes: `Short-form video content/covers/approved-ds49/picks.json` (Instagram PNG a98017ce..., 2,214,449 B; YouTube JPEG 89d2bdfd..., 431,327 B). Copied beside the film on project, Extreme and Drive (`approved covers/`). Review history: `Docs/DS49_COVER_REVIEW_20261029.md`.

## Film and backups
- Approved R2 master unchanged: SHA256 40e0c4d5a2fd4f6daa8a31124b87da0e705120eff76045ef20eb30fc89d342b0, 49,520,670 B, 50.617 s; MD5 dd1f13c9ea8bfeb27c0834fe529ed909. SRT MD5 693f80c60ed8e4c55d0d5ce93c8e502c.
- Three copies: project folder, `/Volumes/Extreme/Short-form video content/Coconut Water - DS-49/` (SHA matches), [Google Drive](https://drive.google.com/open?id=1Vpf09WxGyCKoGQJxpTLwfWpHGVvRmLnx) (MD5s match, anyone with the link).
- TikTok cover-first copy: `/Volumes/Expansion/_edit_work/ds49-publish/Coconut Water SFC R2 - TikTok cover-first.mp4`, SHA256 671222fafec99c0423b87c962de031115cfdae439c6a87a385e0e4afe3319ecf, 1,518 frames (1 cover + 1,517), 2,374 audio packets with identical payload, zero decode errors, frame-zero PSNR 47.95 dB, first frame inspected.

## Blotato
Config `scripts/blotato/configs/ds49-coconut-water.json` (organic, kitchen false, gym false, ai_generated false, keyword FOOD, UTM campaign coconut-water / content ds49-coconut-water). Four uploads downloaded back and SHA-matched (`/Volumes/Expansion/_edit_work/ds49-publish/uploads.json`): master, TikTok copy, Instagram PNG, YouTube JPEG (< 2 MB). Waitlist entry added to `scripts/blotato/video_waitlist.json`. Facebook cover registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/` (hash matches). ad_guard CLEAN, cover_audit zero issues. No direct YouTube upload, no native scheduling. Schedule IDs: none yet (waitlist).

Title: Why I Stopped Drinking Coconut Water. Copy is Dan's filmed wording, per-platform sixpackabs.com UTMs. No em dashes.

Pinned comment: "What do you drink after a workout?". Posts and pins automatically after release (routine youtube-pinned-comment-daily). Written directly in this session, not through dan-voice-writer.

Article: dedicated Short, nothing at setup; the post-release routine writes or skips.

Calendar: `Docs/SHORTS_RELEASE_CALENDAR.md` Mon Dec 21 6 PM row = Waitlist. Edit Queue: DS-49 stays `finalized` until the top-up creates and reads back the four schedules.

Outstanding (existing routines): top-up queues the four posts, then public cover tiles on all four platforms, pinned comment, Facebook cover install.
