# Glycine LFC Setup: Sleep Better With Glycine (RO-15)

**CONTENT (LFC), organic long-form, Claude edit, 9/23 studio roll C1709 (tube-light studio, not kitchen). No ads, no Google Ads, no unlisted upload.**
**READY 2026-11-06, start now.** Recommended: Claude Opus 5.5, high. **Use the Codex subscription to generate the images.**

## Approval
Dan approved round 2 as final on 2026-11-06: "This is approved. Give me the handoff or setup."
Record with his words, the hash, the standing defaults and QA limits: `/Volumes/Extreme/_edit_work/RO-15/round2/approval-r2.json`.
Defaults he did not overrule, so they stand: only two AI clips (The Thermal Camera 1:02, The Thermostat War 3:07); the rejected takes for
the other six AI ideas stay out (Dan on camera there); side-list line "A Couple Grams A Day In Food"; stock Oura sleeper and the
"thick build" ad-lib kept. Do not reopen the edit.

## Approved files
| what | path | note |
|---|---|---|
| Final master | `claude edited long form content/30 - Sleep Better With Glycine/FINAL - Sleep Better With Glycine.mp4` | sha256 `46dfc4240eeb08cb5a1e4c3e0d20680d1d0d03813fb1402a599d3e7aa13e290e`, 1920x1080 29.97, 5:23.99, -14.2 LUFS, -1.9 dBTP. Same bytes as `/Volumes/Extreme/_edit_work/RO-15/round2/final/RO15_R2_MASTER.mp4` |
| Captions (sidecar, never burned) | same folder, `FINAL - Sleep Better With Glycine.srt` | "Oura Ring" and "AbsByAI.com" spelled right |
| Chapters | same folder, `chapters.txt` | 0:00 Why Glycine Helped Me Sleep / 0:24 What Glycine Is / 0:49 How It Helps You Sleep / 1:16 The Research / 1:49 Who It's Good For / 2:34 What Happened When I Took It / 3:44 The Bigger Point / 4:22 How To Take It / 4:52 Wrap-Up |
| Independent review | same folder, `independent review R2.md` | verdict SHIP |

Folder number is 30 because 29 is How To Get Rid Of Man Boobs. QA limits (say so honestly in any receipt): no human listening pass;
delivery gate 34/39, red rows are the voice tone (Dan's bass lift), headroom +2 px on one 2 s hold at 4:31.5, splice visibility (planned
size cuts), SRT cues over the research card at 1:16 to 1:24, burned-captions false positive (set bulb).

## Facts for setup
- **AI footage: yes.** The Thermal Camera (1:02.2 to 1:06.4, motion built in code from Codex-made AI frames) and The Thermostat War
  (3:07.5 to 3:11.5, Veo Omni from Codex frames). Both carry the AI-GENERATED label. YouTube altered/synthetic flag and TikTok
  `ai_generated` = true. Everything else is real footage; the Oura sleeper is stock.
- Products named: glycine (supplement), Oura Ring. No drug names.
- Release: **Wed Dec 23, 2026, 9 AM America/Chicago** (phase 2; `Docs/LONGFORM_RELEASE_CALENDAR.md` row "Wed Dec 23", currently "Not booked":
  update it to booked once queued). Facebook, Instagram, TikTok Thu Dec 24 noon, after YouTube reads public. Not kitchen.
- 3 Shorts get cut from it later: register the SL job (next free SL number, title "Sleep Better With Glycine (RO-15; 3 Shorts; parent
  Dec 23 9AM Central planned)", state READY, propose segments before rendering), same as SL-36 for RO-31.

## Steps
1. `/video-setup` for a long-form: verify the hash, Drive backup (anyone with the link), Extreme copy.
2. Thumbnails: five Codex designs (two AI Dan acting the topic, one real pool or studio photo, two history-guided) plus three unlabeled
   Google options; newest stable Sol, high; Title Case on every word; stop once for Dan's pick.
3. Title, description with the chapters above and the AbsByAI.com UTM link, tags, pinned question comment in the Blotato config.
4. Queue YouTube Dec 23 9 AM and socials Dec 24 noon in Blotato, or the shared waiting list (`scripts/blotato/video_waitlist.json`) if
   Blotato is full; re-read the saved schedules.
5. Edit queue `uploaded` only after the queue read-back. Save `Docs/RO15_SETUP_RECEIPT_<date>.md`. Register the SL job. Remove this from
   `Handoffs/README.md` OPEN once done.

## Starter prompt
> Glycine LFC Setup. Read `Handoffs/handoff-20261106-ro15-glycine-lfc-setup.md` and execute it: set up "Sleep Better With Glycine" (RO-15) for release Wed Dec 23 2026. Verify the final's hash, back it up, make five thumbnails plus the three Google options (use the Codex subscription to generate the images), stop for my pick, then title, description, chapters, pinned comment and queue it in Blotato or the waiting list.
