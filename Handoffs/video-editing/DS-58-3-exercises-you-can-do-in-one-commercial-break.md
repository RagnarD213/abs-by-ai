**SFC.** Task name: `Commercial Break Workout SFC R1`.

# DS-58: "3 Exercises You Can Do In One Commercial Break", first cut from raw footage

**Dedicated short · 10/15 shoot · BLOCKED: home B-roll: the couch when the game cuts to a commercial, then the exercises in front of the projector.** Added 2026-10-16 at Dan's request. Read `00-RULES.md` first.

## Source (10/15 shoot, called the 10/17 shoot in the planning docs)
Folder: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/`
Read `Docs/SHOOT_1015_FOOTAGE_REPORT.md` first (roll map, measurements, editor warnings). Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709). The lav is on the **left channel only**; use `pick_lav.py`'s map. **The lav flat-tops at -0.49 dBFS on loud words**: listen to emphatic lines and prefer a clean take. Every roll has a sidecar beside it (`roll_sidecar.py show`): full transcript, takes, contact sheet.
Scripts: the editing copy with every cue is the shoot doc `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`; what Dan read is Teleprompter 3 - Outside By The Pool `1yc2xg1sG4lTncvcAmkA17SN-JZnQSsbB9Q-fpEbXotg` (filmed in the studio instead).

## This video
Rolls: **C1777 1:37 to the end, C1778 0:00 to 1:16**.
Set: Studio set, **shot 16:9**, so the approved wide crop with both tube lights (`Docs/STUDIO_BLUE_LIGHT_CROP_DEFAULT.md`) is impossible: a 9:16 crop is 1215 px wide. Use a medium crop on Dan and say so in round 1. Exercise demos come from the pool B-roll rolls (C1737 to C1754, shirtless, same shoot).
Deliverable: 1080x1920, 45 to 66 s, J2 captions, Soft Blue Light HyperFrames graphics. A dedicated short: nothing is derived from it. Cover images are a separate setup task.

- B-roll on this shoot: the pool demos and equipment (C1732 to C1754, listed in the report). Clip library first for anything else.
- B-roll not filmed yet: the couch and projector scene (home).
- The short is built on that scene.
- **Blocked on:** home B-roll: the couch when the game cuts to a commercial, then the exercises in front of the projector. Do not start until it exists.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-58-3-exercises-you-can-do-in-one-commercial-break.md`: cut "3 Exercises You Can Do In One Commercial Break" from 10/15 roll C1777-C1778 with /shorts. Best take of every line, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-58-3-exercises-you-can-do-in-one-commercial-break.md` with `$long-form-content-edit` for take selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Deliver, send Dan the review copy, update `00-MASTER.md`.
