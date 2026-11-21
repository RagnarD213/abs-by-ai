CONTENT (SFL). Invest In Your Health Shorts (SL-20), three Shorts cut from "Why You Should Invest More In Your Health" (RO-20). **HOLD: shared waitlist.** Setup complete; nothing scheduled yet.

Updated: 2026-11-06

## Why the waitlist

Blotato read 194/200 at Short 1 and 198/200 at Short 2, with 60+ earlier-dated videos already waiting and the parent RO-20 itself on the waitlist (YouTube Wed Dec 9 2026). Each entry carries `after` and `parent_config` = `scripts/blotato/configs/ro20-invest-in-your-health.json`, so no Short posts before the parent. Kitchen footage (Aug 3 set): phase 4, Mon to Sat 9 AM from Feb 1. The daily `social-queue-daily-refresh` top-up (`video_topup.py`) queues all four destinations per Short on its saved slot or the next free one.

| Short | Title | Planned | Cover | Config |
|---|---|---|---|---|
| 1 | Don't Bother Dating Unless You're Ripped | Mon Feb 1 2027, 9 AM Central | round 2 N1, Dan: "All right, I like N1 for short one" | `scripts/blotato/configs/sl20-short1-dont-bother-dating-unless-youre-ripped.json` |
| 2 | Why Being Fat Destroys Your Relationship | Wed Feb 3 2027, 9 AM Central | round 3 N5, Dan: "Let's go with N5. Go ahead and install N5." | `scripts/blotato/configs/sl20-short2-why-being-fat-destroys-your-relationship.json` |
| 3 | You Can't Afford To NOT Work Out | Fri Feb 5 2027, 9 AM Central | round 1 A (label X7), Claude's default under Dan's standing rule; Dan may swap before release | `scripts/blotato/configs/sl20-short3-you-cant-afford-to-not-work-out.json` |

## Masters (byte for byte, approved 2026-11-05 "All approved")

SHA256 (project folder, Extreme `Short-form video content/invest SL-20/`, Google Drive MD5 match):
- Short 1 `1f1882ee39a692566b3ce3c69fc18ad4ee8d1cce3278e7e20f48d4b818d22b80`
- Short 2 `47e4fea32717c7daef827d53b37f64282871ef2bc52420365f69260640463a28`
- Short 3 `51f0aeb1e8df1cc23cfc3aba0771e4604c519b4e5890385a61c6306e0aedc63a`

Drive (anyone with the link): https://drive.google.com/open?id=1YloGfjjV5UbYv7PGq9DTpHf8aQdmcDN3 (approved covers in `Short-form video content/covers/approved-sl20/` locally).

## Covers and media

Approved files, hashes, TikTok copies and upload URLs: `Short-form video content/covers/approved-sl20/picks.json`. Covers made with Codex gpt-6.1-sol high on the subscription (round 1 also had Google blind options; rounds 2 and 3 Codex only, Dan named the count). Review history: `Docs/SL20_COVER_REVIEW_20261105.md`.

- TikTok cover-first copies in `/Volumes/Expansion/_edit_work/sl20-publish/`: one cover frame prepended (1737/1414/1706 frames), audio packets identical, zero decode errors, frame-zero PSNR 47.7 to 48.1 dB, each first frame inspected.
- Master, TikTok copy, Instagram PNG and YouTube JPEG (under 2 MB) per Short uploaded to Blotato and each downloaded back with a matching SHA256 (`uploads.json` in the publish folder).
- Facebook covers: rows in `scripts/blotato/fb_reel_covers.json` (images in `scripts/blotato/fb_covers/`) and the live installer `~/.absbyai/fb-reel-covers/`.

## Metadata

Copy is Dan's filmed wording, no em or en dashes. Keyword COACH (parent), UTM campaign `invest-in-your-health`, absbyai.com root links, "Full video on this channel: Why You Should Invest More In Your Health". `ai_generated` true for Shorts 1 and 2 (AI dating-app phone, AI poolside cafe clip) with the on-screen AI line; false for Short 3.

Pinned comments (post and pin automatically after release, routine youtube-pinned-comment-daily):
- Short 1: "Did your matches go up when you got in better shape?"
- Short 2: "Have you seen a relationship fall apart after one of them let themselves go?"
- Short 3: "Are you trading your health for money right now?"

Article: none at setup (Shorts); the sixpackabs-article-gap-daily routine decides after release.

## Checks

ad_guard `--scan` CLEAN before and after; `cover_audit.py` zero issues; organic_short_queue dry runs built all four targets per Short (Short 2's refused only on the 200 cap, as expected for the waitlist).

## After release (owners: existing routines and the release check)

Verify each YouTube Short is public and its tile shows the approved cover on `@danrosefit/shorts` (Studio upload if not), add YouTube's Related Video link to RO-20, check FB/IG/TikTok covers, pinned comments. Edit Queue SL-20 stays `finalized` until the top-up creates and reads back the schedules (same practice as SL-10, DS-49).

Note for whoever runs the top-up: this folder lacked `scripts/blotato/configs/ro23-ab-exercise-ranking.json` (present on GitHub) on 2026-11-06, which made `video_topup.py` stop; merging main fixes it.
