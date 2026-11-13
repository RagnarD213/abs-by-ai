CONTENT (SFL) | What To Cut Shorts | SL-21 | Cover choices and setup

# What To Cut SFL Setup

**HOLD: fire once Shorts 1 and 2 are approved (one new AI clip each is in round 2). Codex newest Sol, high effort.** Not executed yet. One Codex setup task does the covers and setup for all three Shorts together (setup owner rule, Dan 2026-11-07). Setup and cover tasks are exempt from the edit cap.

## Approval and exact files

Dan reviewed Round 1 at http://127.0.0.1:9621/ on November 13, 2026:

- **Short 3: "Short 3 is approved as is."** FINAL. Do not re-edit, re-render or ask for edit approval again. Preserve the file byte for byte.
- **Short 1: "Everything else in short one is approved"**, except one new lip-synced AI clip he asked for (the excuse guy at a restaurant, 0:01.5 to 0:05.7). In round 2 with Claude.
- **Short 2: "Everything else in short 2 approved"**, except one new lip-synced AI clip (the excuse guy on a tropical beach, about 0:02.6 to 0:05.9). In round 2 with Claude.

His approval covers the hair at the top edge (camera roll C1511 framing, same as the approved film and the Invest In Your Health Shorts) and Short 2's key point wording.

| # | Approved title | File in `Short-form video content/` | Seconds | AI flag | SHA256 |
|---|---|---|---|---|---|
| 1 | Restaurants Don't Care About Your Fitness Goals | `whattocut-short1_restaurants-dont-care-about-your-fitness-goals.mp4` | 52.3 (round 1) | will be **true** once the AI excuse clip is in | PENDING round 2: do not use the round 1 file |
| 2 | You Don't Deserve A Vacation Until You're Ripped | `whattocut-short2_you-dont-deserve-a-vacation-until-youre-ripped.mp4` | 51.6 (round 1) | will be **true** once the AI excuse clip is in | PENDING round 2: do not use the round 1 file |
| 3 | If You Can't Afford A Gym, You Can't Afford Therapy | `whattocut-short3_if-you-cant-afford-a-gym-you-cant-afford-therapy.mp4` | 49.8 | false | `b6bd0e5666ab58497e36bc31acc11f3349f53e7b8ed6b81cb5963818965ec2fa` |

Claude fills in the Short 1 and 2 hashes and flips this handoff to "fire now" when Dan approves them. All three are 1080x1920 at 30000/1001 with one-line captions burned in (no second burned set). Notes: `Short-form video content/whattocut-SHORTS.md`. Build, reviews and gate stamps: `/Users/danielrose/Projects/_edit_work/SL-21/` (recipe copy in git: `.claude/skills/shorts/reference/softblue-sl21/`). Word timings: `build/<A|D|E>/words.json` and `cues.json` (A = Short 1, D = Short 2, E = Short 3).

**Not done:** covers, Drive backup, the Extreme copy, media uploads, metadata, schedules.

## QA history (honest)

- Three independent review rounds per Short (Short 2 a fourth for captions); final verdicts SHIP with 0 open defects on all three round 1 files.
- Audio: the film's own mix, verbatim (audio gate PASS). Measured, not listened to.
- Delivery gate 2.6.3: 37 of 39 rows pass on each; the two misses are `framing:hair_top` and `framing:headroom` (source framing, accepted by Dan above). Do not rebuild or alter stamps to satisfy a row.

## What ships

Organic Shorts cut from What To Cut To Afford Getting In Shape (RO-20B). Each ends on a teaching line with no button CTA: use `/video-setup`, never `/ad-setup` or Google Ads. They are already the Shorts: no derivatives. Parent config and receipt: `scripts/blotato/configs/` (ro20b) and `Docs/RO20_RO20B_SETUP_RECEIPT_20261020.md`.

## Release phase: February, kitchen flag

Kitchen footage (Aug 3 kitchen set). The job doc's "Short 1 airs Mon Nov 30" is stale: under Dan's Oct 28 calendar the parent film now releases on YouTube **Fri Dec 11, 2026** (waitlist, `Docs/LONGFORM_RELEASE_CALENDAR.md`). Default: these three go to **phase 4, from Feb 1, 2027, Mon to Sat 9 AM Central**, after the Invest In Your Health Shorts (Feb 1/3/5), spaced apart and away from other kitchen Shorts on the same day (`Docs/SHORTS_RELEASE_CALENDAR.md`, `scripts/blotato/release_phases.py`). If Dan asks for December instead, kitchen Shorts are allowed Dec 12 to 25 after the parent is public. A Short never posts before its parent is public. Order: Short 1 (restaurants), Short 2 (vacation), Short 3 (therapy). If Blotato is full, add all three to `scripts/blotato/video_waitlist.json` with `kitchen: true`.

## Execute

1. **Read and verify.** Current `AGENTS.md`, `AI_COORDINATION.md`, full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `_shared/IMAGE-GENERATION.md` (Google subscription first, blind Google test), `_shared/WRITING-RULES.md`, both release calendars, `Docs/PINNED_COMMENTS.md`, recent approved-cover picks. Verify the three files against the hashes above. Look for existing `sl21*` configs or another owner and resume rather than duplicate.
2. **Five Codex covers per Short (15) plus three unlabeled Google options per Short**, Instagram and YouTube layouts. Per Short: two distinct AI images of Dan acting out the topic, one real pool or studio photo (original person pixels kept), two concepts guided by his approved-cover history. The cover copy is the approved title in title case. Real identity reference, lean and shredded not bulky, inspect every face. No claims, no frowning default, no text on the face or hair. Show the checked sheet and stop for his picks.
3. **After his picks:** Extreme copy and Google Drive backup (anyone with the link can view), verify bytes; `content_type: organic`, `ad_guard.py --scan` before and after; per Short title, description, tags, UTMs and an easy `pinned_comment` question from the transcript; `ai_generated` true for Shorts 1 and 2 (realistic AI excuse clip), false for Short 3; covers to `Short-form video content/covers/approved-sl21/`; TikTok cover-first copies; Facebook cover registry entries; one config per Short at `scripts/blotato/configs/sl21-short<N>-<slug>.json`; `organic_short_queue.py` dry, then `--apply` or the shared waitlist; read back all four platforms. Never a direct Public upload or YouTube native scheduling. Once the parent is public, add YouTube's Related Video link to RO-20B.
4. **Record** a receipt `Docs/SL21_SETUP_RECEIPT_<date>.md`, set SL-21 `uploaded` only after live read-backs, remove this handoff from the OPEN list and push owned changes with `scripts/git/safe-push.sh`. Dashboard stays paused.

## Starter prompt (use once this file says "fire now")

What To Cut SFL Setup. Read `Handoffs/handoff-20261113-sl21-what-to-cut-shorts-covers-and-setup.md` and execute it with the /video-setup method. All three What To Cut Shorts are approved by Dan; verify each file against the hashes in the handoff and preserve the finals byte for byte. Dan has authorized the whole setup: do not stop to ask him anything except his cover picks. Make five unique cover choices for each Short (two AI images of Dan acting out the topic, one real pool or studio photo, two of your choice from his pick history) plus the three unlabeled Google options, in Instagram and YouTube layouts, show the checked sheet and stop for his picks. After the picks, complete backups, metadata and Blotato setup in February Short slots after the parent film is public (Fri Dec 11), or the shared waitlist if Blotato is full.
