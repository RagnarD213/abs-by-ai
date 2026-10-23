**SFC.** Task name: `Surgeon Fake Abs SFC R1`.

# DS-34: "Surgeons Now Carve Fake Abs Into Belly Fat. Don't Do It.", first cut from raw footage

**Dedicated short · 10/15 shoot · READY.** Added 2026-10-16 at Dan's request. Read `00-RULES.md` first.

## Source (10/15 shoot, called the 10/17 shoot in the planning docs)
Folder: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/`
Read `Docs/SHOOT_1015_FOOTAGE_REPORT.md` first (roll map, measurements, editor warnings). Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709). The lav is on the **left channel only**; use `pick_lav.py`'s map. **The lav flat-tops at -0.49 dBFS on loud words**: listen to emphatic lines and prefer a clean take. Every roll has a sidecar beside it (`roll_sidecar.py show`): full transcript, takes, contact sheet.
Scripts: the editing copy with every cue is the shoot doc `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`; what Dan read is Teleprompter 2 - Green Screen `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ`.

## This video
Rolls: **C1729 1:48 to 3:16 (scripted); reaction C1730 3:13 to about 6:30**.
Set: Green screen, **portrait roll** (rotation -90, decodes 2160x3840; do not add a transpose). A laptop edge sits at the bottom of the frame: crop above it. Dan's eyes drop to the laptop while he watches the clip.
Deliverable: 1080x1920, 45 to 66 s, J2 captions, Soft Blue Light HyperFrames graphics. A dedicated short: nothing is derived from it. Cover images are a separate setup task.

- B-roll on this shoot: the pool demos and equipment (C1732 to C1754, listed in the report). Clip library first for anything else.
- B-roll not filmed yet: none on the list.
- Only the scripted take exists (checked 2026-10-23: C1729/C1730 have no off-the-cuff take for this video; the off-the-cuff run starts later on C1730, at 7:28 with the dad bod video). Build from the scripted take. The clip plays first, with nothing before it (memory `reaction-shorts-clip-first`); clip and times: `10-17 Shoot - Reaction Clips` doc `1BcRpzDQYNCssROEvg10Z9cOL2AtdvBdyqHwvxxwHtQA`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-34-surgeons-now-carve-fake-abs-into-belly-fat-dont-do-it.md`: cut "Surgeons Now Carve Fake Abs Into Belly Fat. Don't Do It." from 10/15 roll C1729-C1730 with /shorts. Best take of every line, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-34-surgeons-now-carve-fake-abs-into-belly-fat-dont-do-it.md` with `$long-form-content-edit` for take selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Deliver, send Dan the review copy, update `00-MASTER.md`.
