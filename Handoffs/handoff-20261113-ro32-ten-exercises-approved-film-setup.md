# I'm 41. Here Are The 10 Exercises I Do Every Week LFC Setup, 2026-11-13

**Type: CONTENT, long-form (LFC). Owner: Codex (setup rule, Dan 2026-11-07). Not started.**

Goal: take the approved film to fully set up and scheduled (or on the shared waitlist) on YouTube, Facebook, Instagram @danrosefit and TikTok.

Dan approved the exact round 3 film on 2026-11-13: "Okay, it looks good. This is approved. Proceed to setup." This also settles his one open call: the man in the red cap behind him in the chest-fly clip (3:26 to 3:30) stays unblurred. Do not re-render, re-grade or touch the audio.

Read first: `.claude/skills/video-setup/SKILL.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`, `Docs/PINNED_COMMENTS.md`, `Docs/LONGFORM_RELEASE_CALENDAR.md`. Current AGENTS.md rules win over anything older here.

## Exact approved files

Project archive (internal drive): `claude edited long form content/31 - I'm 41. Here Are The 10 Exercises I Do Every Week/`
- `FINAL_RO-32_Im-41-10-Exercises.mp4` SHA256 `414b54da03280c49683dbe8d7bc4962ebceae13ab5bea16a6bbcffb3f03ef10d`, 766,808,132 bytes, 4:37.18, 1920x1080, 30000/1001 fps, AAC stereo.
- `FINAL_RO-32_Im-41-10-Exercises.srt` SHA256 `60bc63fdf43c2a3c4bec6f43bc420d8c43579ec24ddd255ad5e4e9fa693ebd6c` (sidecar subtitles, not burned in).
- `chapters.txt` (YouTube chapters, 13 entries from 0:00 to the 4:04 Recap).
- `ROUND-3-REVIEW.md` (independent review; its two must-fix mouth clicks were removed in this exact file, video stream unchanged).

Working copy and recipe: `/Volumes/Extreme/_edit_work/RO-32/round1/final_r3/RO32_MASTER.mp4` (same hash). Round journal: `/Volumes/Extreme/_edit_work/RO-32/round2-plan/README.md`.

Gate: 35 pass, 4 explained fails (voice tone = Dan's approved bass lift; jump_cut false positive at 4:13/4:19, lower-third changes in one continuous take; two caption rows = graphic text, no burned captions). Accept these through the documented override path; never change the film to clear them.

## What the film contains (for metadata and disclosure)

- Dan's real gym B-roll from the Oct 23 shoot plus his studio presenter footage. **No AI-generated imagery or AI clips** (the two AI ideas were cut in round 1).
- Real photos only, labelled on screen "Real Photos Of Me, Not AI-Generated" (opening before/after graphic, two studio portraits later).
- Two background gym members have blurred faces (leg press 1:18 to 1:35, glute bridge 1:50 to 2:05).
- Gym footage, not kitchen: fine for phase 3 (January blitz).

## Release slot

Fri Jan 29, 2027, YouTube 9 AM America/Chicago (phase 3, January blitz). Facebook, Instagram and TikTok Sat Jan 30, noon, only after the YouTube video is verified public. Calendar row currently says "Not booked": mark it booked. Inspect the live Blotato queue; if it is full, put it on the shared waitlist (`scripts/blotato/video_waitlist.json`, gym flag, not kitchen) for the daily top-up. No per-video routine, no native YouTube scheduling, never upload Public.

## Setup steps (Codex)

1. Backups: hash-verified copy of the mp4 + srt on the Extreme long-form archive and Google Drive (anyone with the link can view).
2. Thumbnails: the five-design mix (two AI Dan acting the topic out, one real pool or studio photo, two guided by his approved-cover history) plus three unlabeled Google options; Google subscription attempt first, Codex subscription images required, blind pick page, inspect every AI face. Stop for Dan's pick. Record pick and hashes.
3. After the pick: title (start from the filmed title "I'm 41. Here Are The 10 Exercises I Do Every Week"), description in Dan's voice with the chapters and UTM link, tags, pinned question comment in the Blotato config, organic classification/ad guard, upload gate on the exact hash, Blotato media for all four platforms with cover URLs, readback of every schedule or waitlist entry, setup receipt `Docs/RO32_SETUP_RECEIPT_<date>.md`.
4. Edit Queue: stays `finalized` until verified scheduling, then `uploaded`.
5. Later, separate job: three Shorts from this film via `/shorts` after it is set up (LFC gets Shorts only).

## Starter prompt

Set up the approved film "I'm 41. Here Are The 10 Exercises I Do Every Week" (RO-32, LFC) from `Handoffs/handoff-20261113-ro32-ten-exercises-approved-film-setup.md`. Dan approved this exact file on 2026-11-13; do not change the film. Make the thumbnail choices and stop for my pick, then finish metadata, backups, Blotato or shared waitlist for Fri Jan 29 2027 9 AM (socials Sat Jan 30 noon) and the setup receipt.

Model: Codex newest stable Sol (GPT-6.1 Sol), high.
