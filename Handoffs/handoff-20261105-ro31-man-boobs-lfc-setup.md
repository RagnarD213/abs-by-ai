# Man Boobs LFC Setup: How To Get Rid Of Man Boobs (RO-31)

**CONTENT (LFC), organic long-form, Claude edit, 10/15 studio roll C1775 (not kitchen). No ads, no Google Ads, no unlisted upload.**
**READY 2026-11-05, start now.** Recommended: Claude Opus 5.5, high. **Use the Codex subscription to generate the images.**

## Approval
Dan approved round 4 as final on 2026-11-05 ("Approve as final") on the review page (port 9644, now retired).
Record with his words, the hash and QA limits: `/Volumes/Expansion/_edit_work/RO-31/round4-plan/approval-r4.json`.
Open questions he did not answer, so the defaults stand: the Pool Shirt and T-Shirt Double Take AI clips stay out (he is on camera there),
the "Real Photos Of Me, Not AI-Generated" label stays where it is. Do not reopen the edit.

## Approved files
| what | path | note |
|---|---|---|
| Final master | `claude edited long form content/29 - How To Get Rid Of Man Boobs/FINAL - How To Get Rid Of Man Boobs.mp4` (link to `/Volumes/Expansion/_internal-offload-20261031/claude edited long form content/29 - How To Get Rid Of Man Boobs/`) | sha256 `bce049d0d1defeb95f9e56de7b3787d039689653261310647c0b81904a62e8ef`, 1920x1080 29.97, 3:52.3, -14.3 LUFS, -1.2 dBTP |
| Captions (sidecar, never burned) | same folder, `FINAL - How To Get Rid Of Man Boobs.srt` | Zepbound, AbsByAI.com, SixPackAbs.com spelled right |
| Chapters | same folder, `chapters.txt` | 0:00 Man boobs or chest fat? / 0:19 The two kinds / 0:48 How to check which one you have / 1:11 The fix for chest fat / 2:01 Step 2: Build your chest / 2:23 The fix for true gynecomastia / 3:18 Recap |

QA limits (say so honestly in any receipt): no human listening pass; delivery gate red rows are the voice tone (Dan's bass lift), B-roll share 35%,
caption card collision (label vs caption band), burned-captions false positive; banned_screen NOT MEASURED (reference file unreadable; no screen capture in this film).

## Facts for setup
- **AI footage: yes.** Three Veo/Omni clips (locker-room opener 0:00, doctor visit 1:05, bodybuilder 2:41) plus library AI clips (talk to your doctor 1:35, calorie app 1:49). YouTube altered/synthetic flag and TikTok `ai_generated` = true.
- Drug name Zepbound is said and captioned (organic, allowed). Graphics say "Appetite Meds".
- Release: **Sun Jan 24, 2027, 9 AM America/Chicago** (phase 3, January blitz; `Docs/LONGFORM_RELEASE_CALENDAR.md` row "RO-31"). Facebook, Instagram, TikTok Mon Jan 25 noon, after YouTube reads public.
- 3 Shorts get cut from it later (SFL job, separate).

## Steps
1. `/video-setup` for a long-form: verify the hash, Drive backup (anyone with the link), Extreme copy.
2. Thumbnails: five Codex designs (two AI Dan acting the topic, one real pool or studio photo, two history-guided) plus three unlabeled Google options; newest stable Sol, high; Title Case on every word; stop once for Dan's pick.
3. Title, description with the chapters above and the AbsByAI.com UTM link, tags, pinned question comment in the Blotato config.
4. Queue YouTube Jan 24 9 AM and socials Jan 25 noon in Blotato, or the shared waiting list (`scripts/blotato/video_waitlist.json`) if Blotato is full; re-read the saved schedules.
5. Edit queue `uploaded` only after the queue read-back. Save `Docs/RO31_SETUP_RECEIPT_<date>.md`. Remove the RO-31 board entry once pushed.

## Starter prompt
> Man Boobs LFC Setup. Read `Handoffs/handoff-20261105-ro31-man-boobs-lfc-setup.md` and execute it: set up "How To Get Rid Of Man Boobs" (RO-31) for release Sun Jan 24 2027. Verify the final's hash, back it up, make five thumbnails plus the three Google options (use the Codex subscription to generate the images), stop for my pick, then title, description, chapters, pinned comment and queue it in Blotato or the waiting list.
