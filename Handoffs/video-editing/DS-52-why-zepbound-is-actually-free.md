**SFC.** Task name: `Zepbound Free SFC R1`.

# DS-52: "Why Zepbound Is Actually Free", first cut from raw footage

**Dedicated short · 10/15 shoot · READY.** Added 2026-10-16 at Dan's request. Read `00-RULES.md` first.

## Source (10/15 shoot, called the 10/17 shoot in the planning docs)
Folder: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/`
Read `Docs/SHOOT_1015_FOOTAGE_REPORT.md` first (roll map, measurements, editor warnings). Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709). The lav is on the **left channel only**; use `pick_lav.py`'s map. **The lav flat-tops at -0.49 dBFS on loud words**: listen to emphatic lines and prefer a clean take. Every roll has a sidecar beside it (`roll_sidecar.py show`): full transcript, takes, contact sheet.
Scripts: the editing copy with every cue is the shoot doc `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`; what Dan read is Teleprompter 3 - Outside By The Pool `1yc2xg1sG4lTncvcAmkA17SN-JZnQSsbB9Q-fpEbXotg`.

## This video
Rolls: **C1760, C1761 0:00 to 0:50**.
Set: Pool, **portrait roll** (rotation -90, decodes 2160x3840; do not add a transpose), shirtless, hard afternoon sun. **Outdoor video: round 1 shows Dan colour, audio and crop options** (VIDEO-RULES, 2026-10-14). The lav hangs on a cord in the centre of his chest in every take.
Deliverable: 1080x1920, 45 to 66 s, J2 captions, Soft Blue Light HyperFrames graphics. A dedicated short: nothing is derived from it. Cover images are a separate setup task.

- B-roll on this shoot: the pool demos and equipment (C1732 to C1754, listed in the report). Clip library first for anything else.
- B-roll not filmed yet: the vial, label out of focus (prop shot).

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-52-why-zepbound-is-actually-free.md`: cut "Why Zepbound Is Actually Free" from 10/15 roll C1760-C1761 with /shorts. Best take of every line, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-52-why-zepbound-is-actually-free.md` with `$long-form-content-edit` for take selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Deliver, send Dan the review copy, update `00-MASTER.md`.


## Execution checkpoint, 2026-11-01, Codex, R2

[Watch the 59.49-second timing cut](http://127.0.0.1:9290/). Dan approved the three transcript removals and pitch-preserving acceleration under 60 seconds. Clean edit 61.49 seconds; final 59.49 seconds at 1.03365x. Independent timing review found no confirmed cut/speed defect. Browser playback, seeking, pace comparisons and paused/sound-ready owner handoff verified silently. Full-quality copy is in `Videos to Review/Zepbound Free SFC R2 - timing cut.mp4`.

[Colour, voice and crop choices remain open](http://127.0.0.1:9290/look-r1.html), recommend B/B/1. Those are provisional in the timing cut. Exact-file audio gate fails tone only; no full-master pass claimed. Graphics, B-roll, J2 burned captions, their contextual previews and final delivery gates remain pending. No upload or scheduling. Queue is draft_review; Drive update verified. Continue in this chat from `/Volumes/Expansion/_edit_work/DS-52/round2/RESUME.md`. Recipes, review copies and notes are also in `Short-form video content/Zepbound Free - DS-52/R2 Timing Review/`.

## R3 approved finishing, 2026-11-01

Dan approved the 59.49-second pace, colour V, voice B, crop 1, then requested graphics and captions. These choices replace the pending-look checkpoint above. No approval or publishing inferred beyond that scope. Saved exact approval/hashes and next action in `/Volumes/Expansion/_edit_work/DS-52/round3/RESUME.md` and `records/`. Edit cap acquire returned waiting #1; production has not started. Auto-resume heartbeat `resume-zepbound-free-r3` is ACTIVE every 10 minutes in the same chat, pauses itself once a slot is acquired. Keep R2 review immutable.
