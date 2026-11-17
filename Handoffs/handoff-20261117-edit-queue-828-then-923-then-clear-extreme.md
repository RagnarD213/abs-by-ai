# Edit order for the 8/28 and 9/23 shoots, then clear them off the Extreme drive (2026-11-17)

Dan's decision, 2026-11-17: finish the last edits that still need the 8/28 and 9/23 raw footage, then move each shoot off the Extreme drive to the Seagate and Google Drive. Everything below is CONTENT (dedicated shorts `SFC`, one long-form `LFC`); no ads.

## Cancelled and removed from the edit queue (no handoffs written)
- **8/28 ads, all five:** RA-02 How To Generate Abs With AI, RA-03 Watch AI Put Abs On Me In 30 Seconds, RA-08 Why Are Trainers Going Out Of Business?, RA-10 AI Is Changing The World, RA-11 What Would You Look Like With Abs?. (Follows Dan's 2026-11-15 "no more Abs By AI ads".) Their job docs stay in `Handoffs/video-editing/` as history; the raw takes stay safe on the Seagate and Drive.
- **9/23:** WV-02 "VSL 2: /start landing-page video".
- DS-26 and DS-29 are unblocked (state `ready`): Dan's footage already exists (see their handoffs).

## The seven handoffs, in order
Run each in its own task, in this order. Each edit task runs `editroute.py pick` then `editcap.py acquire` first (rules in `AGENTS.md`). The two clear handoffs run only after Dan has approved the edits above them.

**A. 8/28 shoot (229 GB)**
1. `How To Do M100s SFC R1`: `Handoffs/video-editing/DS-25-how-to-do-m100s.md` (B-roll found: roll C1736 on the 10/15 shoot). Claude Opus 5.5, high.
   > Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-25-how-to-do-m100s.md` including its 2026-11-17 update: cut the dedicated short "How To Do M100s" (SFC) from its 8/28 raw takes and the 10/15 C1736 B-roll. Best take of every line, 1080x1920, 45-66 s, J2 captions, every B-roll cue filled, corrected and checked in the render, lav picked per file, 8/28 S-Log3 conversion. Every gate, independent audit, deliver, send me the review copy, update the queue.
2. `Pushup Masterclass LFC R2`: `Handoffs/video-editing/RO-09-pushup-masterclass.md`. Claude Opus 5.5, high.
   > Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-09-pushup-masterclass.md` including its 2026-11-17 update: cut the Pushup Masterclass (LFC, 16:9) from 8/28 rolls C1680, C1681, GoPro angles and the 10/15 pickup C1732. First search once more for the spoken teaching; if it is not found, build the demonstration-only film with level cards and say so in the review. Every gate, independent audit, deliver, send me the review copy, update the queue.
3. `Clear 8-28 Shoot Setup`: `Handoffs/handoff-20261117-clear-828-shoot-from-extreme.md`. Claude Sonnet 5.5, medium. **Fire only after I have approved both 8/28 edits.**
   > Read `Handoffs/handoff-20261117-clear-828-shoot-from-extreme.md` and execute it: confirm the gate, verify every file by SHA-256 on the Seagate and by rclone check on Google Drive, then remove the 8/28 shoot from the Extreme drive, leaving the receipt and restore pointers, and push the receipt.

**B. 9/23 shoot (195 GB)**
4. `AI Job SFC R1`: `Handoffs/video-editing/DS-32-ai-job-short.md` (roll C1720). Claude Opus 5.5, high.
   > Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-32-ai-job-short.md` including its 2026-11-17 update: cut the dedicated short "AI Job" from 9/23 roll C1720 with /shorts. Best take of every line, 1080x1920, 45-66 s, J2 captions, every gate, independent audit, deliver, send me the review copy, update the queue.
5. `Wispr Flow SFC R1`: `Handoffs/video-editing/DS-26-wispr-flow-short.md` (roll C1719; demo recording B0730 and take B0731 attached, both from RO-18). Claude Opus 5.5, high.
   > Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-26-wispr-flow-short.md` including its 2026-11-17 update: cut the dedicated short "Wispr Flow" from 9/23 roll C1719, using the Wispr Flow screen recording (library B0730, top 190 px cropped) as the proof beat. Best take of every line, 1080x1920, 45-66 s, J2 captions, every gate, independent audit, deliver, send me the review copy, update the queue.
6. `Robot Lawn Mower SFC R1`: `Handoffs/video-editing/DS-29-robot-lawn-mower-short.md` (roll C1720; real mower footage B0726-B0729 and the portrait originals attached, from RO-18). Claude Opus 5.5, high.
   > Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-29-robot-lawn-mower-short.md` including its 2026-11-17 update: cut the dedicated short "Robot Lawn Mower" from 9/23 roll C1720, using Dan's real mower footage (portrait originals tone-mapped and graded) and his final numbers ($100-$200 a visit, about $3,000 a year). Best take of every line, 1080x1920, 45-66 s, J2 captions, every gate, independent audit, deliver, send me the review copy, update the queue.
7. `Clear 9-23 Shoot Setup`: `Handoffs/handoff-20261117-clear-923-shoot-from-extreme.md`. Claude Sonnet 5.5, medium. **Fire only after I have approved DS-32, DS-26 and DS-29.**
   > Read `Handoffs/handoff-20261117-clear-923-shoot-from-extreme.md` and execute it: confirm the gate, verify every file by SHA-256 on the Seagate and by rclone check on Google Drive, then remove the 9/23 shoot from the Extreme drive, leaving the receipt and restore pointers, and push the receipt.

## Where this stands
- The general Extreme cleanup (finished edit jobs moved to the Seagate) is a separate task, `Handoffs/handoff-20261117-clear-extreme-drive.md`; its receipt is `Docs/EXTREME_CLEANUP_RECEIPT_20261117.md`. These raw shoots (424 GB together, with another 311 GB on the 10:15, 10:23 and 11:13 shoots still waiting on 80+ other jobs) are the next block of space after it.
- Footage already verified on both copies: 8/28 (Seagate 2026-10-07, Drive 2026-10-09), 9/23 (Seagate 2026-10-07, Drive 2026-10-09). Each clear handoff re-verifies before it removes anything.
