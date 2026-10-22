# AI Changing World AD setup, October 22, 2026

**AD.** RA-09 "Do You Think AI Is Changing The World?" R1 9:16, approved by Dan 2026-10-22 ("Okay, everything looks good as is. This is approved. Proceed to setup."). Closing words, transcribed from the exact file: "Tap the button below now to get started." Only the 9:16 exists; no 16:9 film was built.

Master `Claude Ad Videos/do you think ai is changing the world - RA-09/do you think ai is changing the world | claude | 9x16 | RA-09.mp4`, SHA-256 `225018256b1c6d0013bd1108b28529ebbb04e9217894b5318393e980de26c2d2`, checked before the upload. Uploaded unchanged; no render. Delivery checks were already done on this file (stamps beside it).

## Thumbnails

Round 1: five designs by Codex (gpt-6.1-sol, high) through `codex-image.sh`, headline AI IS CHANGING THE WORLD / USE IT FOR ABS: (1) real pool photo-247 on a blue-hour pool, cyan DIN; (2) real studio-gray-67 in front of an orange-wired globe, Arial Black on orange blocks; (3) AI Dan at a self-adjusting cable machine, racing red; (4) a giant robot supervising a dumbbell curl; (5) a giant laptop turned home gym. Dan liked 2's feel and asked for three new real-photo designs with "Use AI to get real abs" on his left and, larger than usual, the real-photo disclosure on his right.

Round 2 (Codex plans and plates, real studio cutouts): A gray-67 midnight city cyan; B white-59 circuit mountains lime; C blue-150 crimson data centre. Dan: three pool-shoot photos with their natural background instead, same text, and in the vertical the headline on top and the label at the bottom.

Round 3: real pool photos 247, 230 and 13 with their own backgrounds. Where the frame was wider or taller than the photo, Codex continued the photo's own scenery into the empty area and the real photo was pasted back over its region (Dan never redrawn). Dan picked C (photo 13): "In the vertical, move me up slightly so that the 'real photo of me' text doesn't block my abs. In the horizontal, make the photo of me slightly bigger and make the text to my left significantly larger, like double the size." Done: vertical photo up 120 px (reusing the same Codex scenery), horizontal photo 10% larger and the headline on four lines at about 1.9x. Label wording is the house standard "Real photo of me, not AI-generated".

Files: `social media graphics/youtube/thumbnails/RA-09 Do You Think AI Is Changing The World/FINAL-APPROVED/` (9:16 installed, 16:9 kept). Every file passed text clearance and the 2 MB limit. No paid image API; Replicate only for the transcript (cents).

## YouTube

| YouTube | Thumbnail | Status read back |
|---|---|---|
| [RToVv-Xgfj8](https://youtu.be/RToVv-Xgfj8) | Round 3 C, pool photo-13, USE AI TO GET REAL ABS | unlisted, processing succeeded, embeddable |

Channel `UC236gjadarHAhEhOMYNGJ9g` (Dan Rose Fitness). Title "Do You Think AI Is Changing The World?", category 26, not made for kids, synthetic=true (robot opener 0-2.4 s, AI goal picture 9.3-11.8 s, app generation 16.6-23.2 s, analysis card 25.1-31.9 s, AI trainer demo 31.9-36.8 s, AI sling/closed gym/home workout clips 43.9-51.2 s), tags ab workout, abs by ai, ai fitness, six pack abs, ai fitness coach, ai six pack abs. Description has no chapters, links the homepage with `dgen-trial-ra09` UTMs, carries the AI sentence, no em dash. Served thumbnail read back and checked by eye.

## Google Ads

Trial campaign `24316364155`, ad group `200913806626` "RA-09 Do You Think AI Is Changing The World", ENABLED, $40 target CPA (RA-14 reference), Audience `359952376`, US + CA, English. Ad `829196685786`, ENABLED, REVIEW_IN_PROGRESS. Final URL on absbyai.com/start with `utm_content=claude-9x16-vsl`, HTTP 200. validateOnly passed before apply. Budget `15911255930` read $30/day before and after; campaign status untouched. Policy report 10-22: nothing in the campaign disapproved or limited. Recheck 10-23: `node scripts/ads/api/client.js policy 24316364155`.

A trial (tap-the-button) ad, so not one of the engagement "AT ·" ads that go in all three engagement campaigns.

## Records

Edit queue RA-09 set to `uploaded` after the readback and the Ads entry (Drive status file and artifact db v5). Setup handoff removed from the OPEN index. No organic posting, public upload or pinned comment. Victory Dashboard skipped (paused).

Recipe: `.claude/skills/ad-setup/reference/ra09-setup-20261022/` (build.py round 1, r2/build_r2.py, r3/prep_r3.py + r3/build_r3.py, Codex plans and prompts, QC, generation receipts, policy). Config/result: `scripts/ads/api/dgen-ads/ra09.json`, `ra09.result.json`.
