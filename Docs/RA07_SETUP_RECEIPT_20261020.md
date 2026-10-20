# Fire Your Trainer AD setup, October 20, 2026

**AD.** RA-07 "Fire Your Trainer!" R6 9:16, approved by Dan 2026-10-18 ("All right, this is approved. Go ahead and do the setup in the next round."). Closing words, transcribed from the exact file: "Tap the button below to take the first step." Only the 9:16 exists; no 16:9 was built.

Master `Claude Ad Videos/fire your trainer - RA-07/fire your trainer | claude | 9x16 | RA-07.mp4`, SHA-256 `ca75555c9736d7cea4bf1336f21e672e40496039ee34ed698a263ec046edcfae`, checked before the uploads. Uploaded unchanged; no render.

## Thumbnails

Round 1: five designs by Codex (gpt-6.1-sol, high) through `codex-image.sh`. (1) real pool photo-221, pink-slip type; (2) real studio-blue-28 smirk, TRAINERS DESPISE HIM over angry trainers; (3) AI Dan fist-bumping a robot coach; (4) orange robot coach; (5) robot hands tearing a workout sheet. Codex planned options 3 to 5. Cooper Black is not installed, so option 4 used Arial Rounded Bold. Round 2, Dan's words: "For 2, make all the text horizontal... keep the despising text the same. For 'Fire Your Trainer,' make the text significantly bigger, only one word per line... as big as possible." Built 2b (level banner) and 3b (FIRE / YOUR / TRAINER). Dan: "Let's go with 2B and 3B. Install an A/B test with 2B and 3B."

Files: `social media graphics/youtube/thumbnails/RA-07 Fire Your Trainer/FINAL-APPROVED/` (9:16 installed, 16:9 kept). Every file passed text clearance (face, hair, abs) and the 2 MB limit. Codex usage was 235,437 subscription tokens. No paid image API was used, and Replicate was used only for the cutout and the transcript, cents each.

## YouTube

YouTube Test & Compare does not run on Shorts or unlisted videos, so, as on RA-14, the film went up twice, one thumbnail each:

| Copy | YouTube | Thumbnail | Status read back |
|---|---|---|---|
| A | [bpv5HSRqzDo](https://youtu.be/bpv5HSRqzDo) | 2b TRAINERS DESPISE HIM | unlisted, processing succeeded, embeddable |
| B | [AWh8cOd80Ic](https://youtu.be/AWh8cOd80Ic) | 3b FIRE YOUR TRAINER | unlisted, processing succeeded, embeddable |

Channel `UC236gjadarHAhEhOMYNGJ9g` (Dan Rose Fitness). Both uploads were made with title "Fire Your Trainer", category 26, not made for kids, synthetic=true (AI fired-trainer, robot spotter and injury scenes), tags ab workout, abs by ai, ai fitness, six pack abs, personal trainer, ai trainer. The description has no chapters (per the handoff), links the homepage with `dgen-trial-ra07` UTMs and carries the AI sentence. Both served thumbnails were read back and checked by eye.

## Google Ads

Trial campaign `24316364155`, ad group `204215057191` "RA-07 Fire Your Trainer", ENABLED, $40 target CPA (RA-14 reference), Audience `359952376`, US + CA, English. Ads `828608015181` (A) and `828655819900` (B), ENABLED, REVIEW_IN_PROGRESS. Final URLs on absbyai.com/start with `utm_content=claude-9x16-thumbA-vsl` / `thumbB-vsl`, HTTP 200. validateOnly passed before apply. Budget `15911255930` read $30/day before and after; campaign status untouched. Policy report 10-20: nothing in the campaign disapproved or limited. Recheck 10-21.

This is a trial (tap-the-button) ad, so it is not one of the engagement "AT ·" ads that go in all three engagement campaigns.

## Records

Edit queue RA-07 set to `uploaded` after both readbacks and the Ads entry (Drive status file and artifact db v19). The queue file merged the newest records from the main folder (RO-20C, RO-24, RO-27, SL-19 were ahead there) so the Drive push dropped nobody's status. Setup handoff removed from the OPEN index. No organic posting, public upload or pinned comment. Victory Dashboard skipped (paused).

Recipe: `.claude/skills/ad-setup/reference/ra07-setup-20261020/` (build.py, Codex plan and prompts, QC, generation receipts, Ads apply log, policy). Config/result: `scripts/ads/api/dgen-ads/ra07.json`, `ra07.result.json`.
