# Muhammad dedicated Shorts Batch B: setup receipt, 2026-10-27

Category: CONTENT (SFC). Organic: none has a button CTA. Handoff: `Handoffs/handoff-20261026-muhammad-shorts-batch-b-sfc-setup.md`. Task: Muhammad Shorts Batch B SFC Setup (Claude, Opus 5.5).

| Job | Title | Release (9 AM Central, all four) | State | Cover | AI flag | Config | Master sha256 (16) |
|---|---|---|---|---|---|---|---|
| DS-13 | The #1 Change I Made To Get Abs At 40 | Thu Jan 7, 2027 | waiting list | A | yes | `scripts/blotato/configs/ds13-the-1-change-i-made-to-get-abs-at-40.json` | `6d17332ad24649cd` |
| DS-06 | What Every Body Fat Percentage Looks Like | Thu Jan 14, 2027 | waiting list | A-r2 | yes | `scripts/blotato/configs/ds06-what-every-body-fat-percentage-looks-like.json` | `b61220f661dbd0c4` |
| DS-10 | Top 3 Non-Weight Loss Benefits Of Zepbound | Thu Jan 21, 2027 | waiting list | A-r2 | yes | `scripts/blotato/configs/ds10-top-3-non-weight-loss-benefits-of-zepbound.json` | `e215e1b010107020` |

- **Files:** Muhammad HDs, measured frame-identical to the approved cuts on 10-19 (DS-06 = V4, DS-10 = V3, DS-13 = V3). Project folder and Extreme copies sha256-identical. Google Drive (anyone with the link): [DS-06](https://drive.google.com/open?id=1KJUkfEce2_HPAuBOzAmjRPcKTEBsulqb), [DS-10](https://drive.google.com/open?id=1cau-588loNHYt5iiCOwPimbI5e3DiUqi), [DS-13](https://drive.google.com/open?id=1EzrlnPXRyJjvqFn7IYvRin9qICTvyAek); byte counts match.
- **AI flag true** on all three: each carries labelled realistic AI footage (body fat lineup men, opener party/office/sleep scenes, chipotle cups and steak eater).
- **Covers (Dan, 2026-10-27):** A for all three. DS-06 A revised: poster higher, wider body-type range (Codex redrew the silhouettes; the poster was moved locally with Dan's pixels kept, `scripts/covers/muhammad-batch-b-20261026/move_poster.py`). DS-10 A revised: title "Top 3 Non-Weight Loss Benefits Of Zepbound", which is also the post title. Dan approved both revised files before install. Files: `Short-form video content/covers/approved-muhammad-batch-b/`; hashes in each config (`cover_ig_sha256`, `cover_yt_sha256`), matched against the review manifests. Five-choice set: 15 GPT-6.1 Sol high calls on the Codex subscription plus one edit; recipe `scripts/covers/muhammad-batch-b-20261026/`.
- **Media:** master, TikTok cover-first copy, Instagram PNG and YouTube JPEG (under 2 MB) uploaded per Short and downloaded back, sha256-matched: `scripts/covers/muhammad-batch-b-20261026/media-uploads.json`. TikTok copies: frames +1, audio packets identical, cover PSNR 47.9 to 48.6 dB.
- **Facebook cover:** three rows in `scripts/blotato/fb_reel_covers.json` and the live installer copy, covers in `fb_covers/` and `~/.absbyai/fb-reel-covers/covers/`.
- **Queue:** Blotato 192/200. Dry run of `organic_short_queue.py` clean for all three (4 posts each, no clash). Left on the shared waiting list because the daily top-up gives the 8 free slots to RO-19 and RO-07 (Nov 4) first. The daily `social-queue-daily-refresh` queues them on their saved dates.
- **Pinned comments:** in each config (`pinned_comment`, written by dan-voice-writer). Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- **Article:** nothing at setup for Shorts; routine sixpackabs-article-gap-daily decides after release.
- **Calendar:** `Docs/SHORTS_RELEASE_CALENDAR.md` note of 2026-10-27; DS-16 moves to Jan 28, DS-01 to Feb 4.
- **Ad guard scan:** CLEAN before and after.

## Still open
- Edit Queue rows DS-06/10/13 go to `uploaded` only after the queue read-back (when the routine schedules them).
- ⚠ In this main folder the waiting list's DS-40 and five SL-08 config files are missing (they are on GitHub; the folder is 67 commits behind during the merge jam). `video_topup.py` crashes when it reaches them; the jam merge restores them.
