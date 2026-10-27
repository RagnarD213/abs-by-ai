# Top 5 Ab Exercises For Six Pack Abs (DS-01): setup receipt, 2026-10-27

Category: CONTENT (SFC). Organic: ends "Comment and let me know which ab exercise is your favorite", no button CTA. Handoff: `Handoffs/handoff-20261027-top5-ab-exercises-sfc-setup.md`. Task: Top 5 Ab Exercises SFC Setup (Claude, Opus 5.5).

| Release (9 AM Central, YouTube, Facebook, Instagram @danrosefit, TikTok) | State | Cover | AI flag | Config |
|---|---|---|---|---|
| Thu Jan 28, 2027 | shared waiting list | B | no | `scripts/blotato/configs/ds01-top-5-ab-exercises.json` |

- **File:** R4 master `Short-form video content/ds-01_top-5-ab-exercises.mp4`, 1080x1920, 29.97 fps, 52.55 s, sha256 `b00f9b6b066fbd3c43c9a94d28ab6579ed80ccf14b39ed2ef191f9f2d0d14597`. Extreme copy identical. Google Drive (anyone with the link): https://drive.google.com/open?id=16NfOx3wgH7jYtJ89fIcSRzH-vbkQRD6L, md5 matches.
- **AI flag false:** every shot is real footage of Dan; no AI imagery in the film.
- **Title:** Top 5 Ab Exercises For Six Pack Abs. Keyword ABS. Caption and YouTube description from Dan's filmed script; no em dashes.
- **Covers (Dan, 2026-10-27, "let's go with B"):** B, AI Dan doing a kneeling cable crunch in a dark gym, white and cyan Impact. Five-choice set: 5 GPT-6.1 Sol high calls on the Codex subscription (A, B, D, E AI Dan with an identity reference; C real photo studio-white-62 over a Codex plate). Files and hashes: `Short-form video content/covers/approved-ds01/picks.json`. Recipe: `scripts/covers/ds01-20261027/`.
- **Media:** master, TikTok cover-first copy (frames 1575 to 1576, audio packets identical, cover PSNR 48.7 dB), Instagram PNG and YouTube JPEG (320,826 bytes) uploaded and downloaded back, sha256-matched: `scripts/covers/ds01-20261027/media-uploads.json`.
- **Facebook cover:** row in `scripts/blotato/fb_reel_covers.json` and the live installer copy; image in `scripts/blotato/fb_covers/` and `~/.absbyai/fb-reel-covers/covers/`.
- **Queue:** live Blotato 189/200, no post on Jan 28. `organic_short_queue.py` dry run clean (4 posts, 193/200 after). Left on the shared waiting list so the earlier releases get the free slots first; `video_topup.py --assume-free 200` places DS-01 on Thu 2027-01-28 9 AM Central.
- **Pinned comment:** "Ab wheel, spiderman plank, cable crunch, V-sit twist or toe touch. Which one is your favorite ab exercise?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- **Article:** nothing at setup for Shorts; routine sixpackabs-article-gap-daily decides after release.
- **Calendar:** `Docs/SHORTS_RELEASE_CALENDAR.md` note of 2026-10-27; DS-16 moves to Feb 4.
- **Ad guard scan:** CLEAN.

## Still open
- Edit Queue DS-01 goes to `uploaded` after the routine schedules it and the posts read back.
- After release: check the public Shorts tile and the other three covers (monitor `check-youtube-shorts-covers`).
