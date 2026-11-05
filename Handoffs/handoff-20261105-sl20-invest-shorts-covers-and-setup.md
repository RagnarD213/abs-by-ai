CONTENT (SFL) | Invest In Your Health Shorts | SL-20 | Cover choices and setup

# Invest In Your Health SFL Setup

**Ready to start now. One Claude setup task, Opus 5.5, high effort.** Not executed yet. **Use the Codex subscription to generate the images.** The image helper's supported baseline is `gpt-6.1-sol` at high effort; verify the newest supported stable Sol in the execution client before generating. Keep all cover work inside this one task. Setup and cover tasks are exempt from the edit cap.

## Approval and exact files

Dan reviewed Round 1 at http://127.0.0.1:9471/ and said on November 5, 2026: **"All approved"**. That also settles the page calls: the slim-husband clip in Short 2 (0:01-0:05) stays, all three open on Dan talking, and Short 3's captions read "going to" where he says "gonna". All three edits are FINAL: do not re-edit, re-render or ask for edit approval again. Preserve each file byte for byte.

Manifest with hashes: `Short-form video content/invest-SHORTS-final-manifest.json`; notes `Short-form video content/invest-SHORTS.md`. Build, recipe, reviews and gate stamps: `/Volumes/Expansion/_edit_work/SL-20/` (recipe copy in git: `.claude/skills/shorts/reference/softblue-sl20/`).

| # | Approved title | File in `Short-form video content/` | Seconds | AI flag | SHA256 |
|---|---|---|---|---|---|
| 1 | Don't Bother Dating Unless You're Ripped | `invest-short1_dont-bother-dating-unless-youre-ripped.mp4` | 57.93 | true: AI dating-app phone 0:41.8-0:49.5 (film clip) | `1f1882ee39a692566b3ce3c69fc18ad4ee8d1cce3278e7e20f48d4b818d22b80` |
| 2 | Why Being Fat Destroys Your Relationship | `invest-short2_why-being-fat-destroys-your-relationship.mp4` | 47.16 | true: AI poolside cafe clip 0:22.5-0:25.0 (A0032) | `47e4fea32717c7daef827d53b37f64282871ef2bc52420365f69260640463a28` |
| 3 | You Can't Afford To NOT Work Out | `invest-short3_you-cant-afford-to-not-work-out.mp4` | 56.90 | false | `51f0aeb1e8df1cc23cfc3aba0771e4604c519b4e5890385a61c6306e0aedc63a` |

All 1080x1920 at 30000/1001 with one-line captions burned in (no second burned set); word timings in each build's `words.json`/`cues.json` under `build/<C|B|G>/`. Hash every file before use. Keep Dan's capital "NOT" in Short 3's title.

**Not done:** covers, Drive backup, the Extreme copy (finals are only in the project folder and on the Expansion work drive), media uploads, metadata, schedules. Queue SL-20 is `finalized`; edit slot released finished; VLC copies removed. Review service 9471 retires on its own when idle.

## QA history (honest)

- Three independent review rounds per Short; the final verdicts were SHIP with 0 open defects for all three.
- Audio: the film's own mix, verbatim (audio gate PASS on all three).
- Delivery gate: every row passes except `framing:hair_top` / `framing:headroom` (camera roll C1511 framed the hair at the top row through the whole film; the approved RO-20 fails the same two). `compliance:banned_screen` was NOT MEASURED on the final Short 1 and Short 3 files because its reference recording (`screen_capture_TAKE2.MP4`) was moved off the Mac by the footage offload; none of the three contains an app screen recording. Do not rebuild or alter stamps to satisfy a row.

## What ships

Organic Shorts cut from Why You Should Invest More In Your Health (RO-20). Each ends on a teaching line, with no button CTA: use `/video-setup`, never `/ad-setup` or Google Ads. They are already the Shorts: no derivatives. Parent config: `scripts/blotato/configs/ro20-invest-in-your-health.json` (keyword COACH); receipt `Docs/RO20_RO20B_SETUP_RECEIPT_20261020.md`.

## Release phase: February, kitchen flag

This is kitchen footage (Aug 3 kitchen set). Under Dan's Oct 28 calendar the Invest In Your Health Shorts go to **phase 4, from Feb 1, 2027, Mon to Sat 9 AM Central** (`Docs/SHORTS_RELEASE_CALENDAR.md`, `scripts/blotato/release_phases.py`). The parent RO-20 is on the shared waitlist for **Wed Dec 9, 2026** (`Docs/LONGFORM_RELEASE_CALENDAR.md`). A Short never posts before its parent is public. Check the live Blotato queue, the waitlist and the channel first. Order: Short 1 (dating) first, then Short 2 (relationship), then Short 3 (money), on the first free February slots, spaced apart and away from other kitchen Shorts on the same day. If Blotato is full, add all three to `scripts/blotato/video_waitlist.json` with `kind: short`, `kitchen: true` and the RO-20 parent dependency. Never a per-video routine.

## Execute

1. **Read and verify.** Current `AGENTS.md`, `AI_COORDINATION.md`, full `.claude/skills/_shared/VIDEO-RULES.md`, `/video-setup`, `/coverimage`, `_shared/IMAGE-GENERATION.md` (including the blind Google test), `_shared/WRITING-RULES.md`, both release calendars, `Docs/PINNED_COMMENTS.md`, recent approved-cover picks. Verify the three files against the manifest. Look for existing `sl20*` configs or another owner and resume rather than duplicate.
2. **Five Codex covers per Short (15) plus three unlabeled Google options per Short.** Per Short: two distinct AI images of Dan acting out the topic, one real pool or studio photo (original person pixels kept: cutout plus generated background plus type in code), two concepts guided by his approved-cover history. Five genuinely different designs per Short, with one design line each before building. The cover copy is the approved title in title case. Real identity reference, lean and shredded not bulky, inspect every face. No website mark, no claims, no real-photo label on the cover, no frowning default, no text on the face or hair. Topic directions: a ripped man getting matches while others are ignored on a dating app; a couple at dinner where the partner has let himself go; money against health (a wealthy man who is unhealthy). Instagram and YouTube layouts for each. Check them at feed size and at native scale, with grid-safe text and the YouTube JPEG under 2 MB. **Use the Codex subscription to generate the images** with `.claude/skills/_shared/codex-image.sh`. Show the checked sheet and **stop for Dan's picks** before any upload or scheduling.
3. **After his picks:**
   - Copy the finals to `/Volumes/Extreme/Short-form video content/` and do the Google Drive backup (anyone with the link can view) with the approved covers; verify the bytes.
   - CONTENT classification: `content_type: organic`, the exact `source`, and `ad_guard.py --scan` before and after.
   - Per Short: title, description, tags, UTMs and an easy topic `pinned_comment` question taken from the transcript (no link, under 180 characters). `ai_generated` is true for Shorts 1 and 2 and false for Short 3.
   - Export covers to `Short-form video content/covers/approved-sl20/`. Build TikTok cover-first copies with `tiktok_cover.build()` (stream-copy the approved audio) and add the Facebook cover registry entries.
   - Write one config per Short at `scripts/blotato/configs/sl20-short<N>-<slug>.json`. Run `organic_short_queue.py` dry, then `--apply`. Read back YouTube, Facebook, Instagram @danrosefit and TikTok. Never a direct Public upload or YouTube native scheduling.
   - Once the parent is public, add YouTube's Related Video link to RO-20.
4. **Record** a receipt `Docs/SL20_SETUP_RECEIPT_<date>.md`: master and cover hashes, three-copy verification, Drive link, metadata, pinned questions, media URLs, and the schedule IDs or the honest waitlist state. Set SL-20 `uploaded` only after live read-backs. Remove this handoff from the OPEN list and push owned changes with `scripts/git/safe-push.sh`. Dashboard stays paused.

## Starter prompt

Invest In Your Health SFL Setup. Read `Handoffs/handoff-20261105-sl20-invest-shorts-covers-and-setup.md` and execute it with /video-setup. All three Invest In Your Health Shorts are approved; preserve the finals byte for byte. Use the Codex subscription to generate the images. Make five unique cover choices for each Short (two AI images of me acting out the topic, one real pool or studio photo, two of Codex's choice) plus the three unlabeled Google options, in Instagram and YouTube layouts, show me the checked sheet and stop for my picks. After the picks, complete backups, metadata and Blotato setup in February Short slots after the parent film is public, or the shared waitlist if Blotato is full.
