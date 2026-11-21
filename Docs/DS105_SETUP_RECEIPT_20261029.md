# Mouthpiece setup receipt, October 29, 2026

**Covers installed and upload/setup complete. On the shared waiting list, not scheduled or published.** Planned release: **Saturday December 26, 2026, 6 PM America/Chicago**, on YouTube, Facebook, Instagram @danrosefit and TikTok. This is the first free slot allowed by the current October 28 phase plan, checked against live posts, existing waitlist entries and the dated calendar. No other post was displaced.

## Approved cover and film

Dan approved: "Approved. Go ahead and install these covers." This applies to the last delivered B3 text revision, **Wear A Mouthpiece When You Work Out.**, in both layouts. Instagram PNG SHA256 `03ffed4da329bea1d268298394a420c9b9060b467cc871b36cf7bb2405f074dc`; YouTube JPG SHA256 `575db73575b5dbb3cd0a2d5479fc3aefeed796c752c747dfbc31581978cc226f`, 434,755 bytes. Original approval and final files: `Short-form video content/covers/approved-ds105/`.

The approved R4 is unchanged: SHA256 `061deb744eb1e83cf1917727095214c8e4ea68ffebf56d9f85042d80694eebe2`, 67,977,674 bytes, 1917 frames. Original master, captions and approval reverified in project, Extreme and current Drive. No recompressed general upload master, second caption layer or audio processing.

## Installation and verification

- Four public media uploads were downloaded and matched by SHA256: original master, TikTok cover-first derivative, Instagram PNG and YouTube JPG.
- TikTok derivative has 1918 frames (one approved cover plus 1917 film frames), 3000 unchanged AAC packets, no decode errors, cover PSNR 48.08 dB. AAC bitstream hashes are identical. Its first frame was independently decoded from the public upload and matched the checked local first frame exactly. This was offline decoding, no audible playback.
- Facebook cover is in both `scripts/blotato/fb_reel_covers.json` and the live installer registry, with matching local image hashes and the exact first caption line. Existing installer applies it after publication.
- All four exact target payloads passed the maintained cover guard. The full live queue cover audit has zero issues; ad guard reports clean before and after.
- `scripts/blotato/configs/ds105-mouthpiece.json` stores approved media/cover URLs, source hash, title, transcript-based descriptions, hashtags/tags, UTMs and pinned question. No free-generation offer. `ai_generated=false` because the film uses real camera footage; an AI cover still does not change that flag.

Pinned comment: **Do you wear a mouthpiece when you work out?** The existing pinned-comment routine handles posting/pinning after release. The existing Shorts article routine handles searchable-topic article creation or a recorded skip after release. Actual public cover tiles remain unobserved until publication; the existing shared checks handle those.

## Queue and backups

Fresh live readback: 196 schedules, zero Mouthpiece schedules. Older pending videos keep queue priority. A single DS-105 entry is installed in the shared waiting list in release order, with `gym=true`, `kitchen=false`, and planned UTC time `2026-12-27T00:00:00.000Z`. The existing daily top-up helper queues all four when its turn arrives; no per-video automation was created. The Shorts calendar now reserves the planned Dec26 evening row.

DS-105 remains **finalized**, rev9, until actual schedules read back. The Drive status upload succeeded; native artifact-db mirror remains unverified and was not marked synced. R4's existing legacy numerical delivery-gate failures remain as originally recorded and were not turned into a synthetic PASS.

The original film/caption/approval and approved cover files are backed up to Drive and Extreme. The separate TikTok copy is also on Drive under Upload assets. Main folder: https://drive.google.com/open?id=1aipysGk8h0rexXO41XKFRKmNlfZ1DAr2 . All hashes, file IDs, public media URLs and target preflights are in `Docs/DS105_SETUP_RECEIPT_20261029.json`; full evidence is `/Volumes/Extreme/_edit_work/ds105-publish/`.

## Next action

No Dan action. Shared daily top-up queues DS-105 in its turn, then normal public-cover, pinned-comment and article release checks follow. No direct YouTube upload, no extra monitor, no Victory Dashboard, no dispatcher restart.
