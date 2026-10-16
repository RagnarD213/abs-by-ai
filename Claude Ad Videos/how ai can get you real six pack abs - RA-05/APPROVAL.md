# RA-05 "How AI Can Get You REAL Six Pack Abs": 9:16 APPROVED

**Dan, 2026-10-14**, after the round 3 page (http://127.0.0.1:8838/): *"Everything looks great. This ad is approved. Give me the
handoff for setup."*

| | |
|---|---|
| file | `how ai can get you real six pack abs \| claude \| 9x16 \| RA-05.mp4` |
| sha256 | `c0a57092fc85b01575d507ec3dcedf28cd1d60b35c1e56ef96f9a298acbcaceb` (faststart stream copy of the reviewed `round3/draft_9x16.mp4`, `eb19a240b473eb03...`, same streams) |
| length | 58.36 s, 1,749 frames, 1080x1920, 30000/1001, H.264 BT.709 + AAC 320k, about 95 MB |
| closing line | "Tap the button below to see how great you look with abs and to get your AI fitness plan to make your dream body real." (button CTA: an AD) |
| gates so far | audio gate PASS on this file (-14.2 LUFS, -2.4 dBTP). Three independent reviews of the two AI items (couch clip, vertical scan), all notes fixed. Delivery gate + watch pass: owed, step 1 of the setup handoff. |

Approved with it, all three round 3 decisions: the whole 9:16, the couch clip motion, the vertical body scan. Setup:
`Handoffs/handoff-20261014-ra05-setup.md`. Only the 9:16 exists; the 16:9 is a separate edit job.

## Delivery checks (setup, 2026-10-15/16)

- Watch pass: a fresh Opus 5.5 judge looked at all 55 images and flagged 8 items, all present in the approved file (phone URL pill at 0.4 s, half title at 1.9 s, two sways with one arm at the frame edge at 9.0 s and 37.3 s, Step 1 / Step 2 / button graphics across his chest on the wide shot, a one-frame take change at 51.42 s). Dan saw them as frames (`social media graphics/youtube/thumbnails/RA-05 .../RA-05 gate findings.jpg`) and, on 2026-10-16: *"And the video is good as is."* Recorded as `accepted_by_dan` in `/Volumes/Extreme/_edit_work/ra05/setup/watch/logs/findings_dan_accepted.json`.
- Delivery gate `ad9x16`: PASS, 39 passed, 0 failed, 3 not applicable; stamp beside the master (`.deliver_gate.json`). Plan: `/Volumes/Extreme/_edit_work/ra05/setup/plan.json`, built by `.claude/skills/ad-edit/reference/ra05/setup/s93_gateplan.py`.

## Set up (2026-10-16)

- YouTube `0DswKDBFW2E` (https://youtu.be/0DswKDBFW2E), Unlisted, embeddable, processing succeeded, AI flag true, channel `UC236gjadarHAhEhOMYNGJ9g`. Title "How AI Can Get You Real Six Pack Abs" (the all-caps REAL fails the ad copy lint). Thumbnail: option 6, AI Dan with a hologram coach, WHY AI IS THE ULTIMATE TRAINER (Dan: "Let's go with 6"), set and read back.
- Google Ads trial campaign `24316364155`: ad group `199904676174` "RA-05 Real Six Pack Abs", ad `828398569805`, budget unchanged at $30/day. Policy 10-16: REVIEW_IN_PROGRESS. Detail: `Docs/DGEN_CONVERSION_CAMPAIGN.md`.
- Edit queue RA-05 `uploaded`. Review page 8838 and the `Videos to Review/` copy removed.
