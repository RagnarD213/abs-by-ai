CONTENT (SFC, reaction). Task name: `Hormozi Not Hungry Bored SFC R1`.

# DS-109: Alex Hormozi Says You're Not Hungry, You're Bored. He's Right.

**R1 first-review packet delivered 2026-11-15.** [Review page](http://127.0.0.1:9810/). The full film has not been rendered or approved. No upload or scheduling. Original filmed source registered 2026-11-14 from the 11/13 shoot.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `Docs/SHOOT_1113_FOOTAGE_REPORT.md` (format, orientation, camera clock, full roll map).
Script: script C01 in Next Shoot Filming Scripts, Google Doc `1y9hR6wV0Sj7PEVZbfL6bsV_WTD48W8N8RjUfW6bwcI4`. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`. Never modify the originals.
Times are minutes:seconds into each roll from an audio pass: close, not frame-accurate. Read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting; run `pick_lav.py` if a sidecar is missing.

| roll | range | notes |
|---|---|---|
| `C1909` | 3:26-4:27 | Dan watches the Alex Hormozi clip |
| `C1909` | 4:27-6:06 | scripted reaction |
| `C1909` | 6:06-7:48 | off-the-cuff reaction |

Orientation: **portrait (stored 3840x2160 with rotation -90; decode to 2160x3840, add no transpose)**. Sony FX30, 29.97p, S-Cinetone / Rec.709 (grade as Rec.709, no log LUT). One stereo LPCM audio stream.

## Build

- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.
- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common on these rolls.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.

## Deliver

One reaction Short. Scripted and off-the-cuff were both filmed: build the scripted one, and show the off-the-cuff one for comparison only if it is clearly stronger. Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Starter prompts

**Claude: Opus 5.5, high effort.**
> CONTENT (SFC, reaction). Name this chat "Hormozi Not Hungry Bored SFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/DS-109-alex-hormozi-says-youre-not-hungry-youre-bored-hes-right.md`: cut "Alex Hormozi Says You're Not Hungry, You're Bored. He's Right." from the 11/13 green-screen shoot, rolls C1909. Use /shorts with the reaction Short standard (`.claude/skills/shorts/reference/ds40-codex-r5-reaction-format/README.md`). Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.

**Codex: GPT-6.1 Sol, high effort.**
> CONTENT (SFC, reaction). Name this chat "Hormozi Not Hungry Bored SFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/DS-109-alex-hormozi-says-youre-not-hungry-youre-bored-hes-right.md`: cut "Alex Hormozi Says You're Not Hungry, You're Bored. He's Right." from the 11/13 green-screen shoot, rolls C1909. Use the reaction Short standard (`.claude/skills/shorts/reference/ds40-codex-r5-reaction-format/README.md`) and `.claude/skills/shorts/SKILL.md`. Key with the approved house chroma key (`.claude/skills/_shared/chroma-key/README.md`). Follow the first-review approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.

## R1 work state, 2026-11-15

First review is ready for Dan in the original Codex chat `01a1dc87-ce93-75c1-b1c7-9aac9dc8317a`. [Open the checked review page](http://127.0.0.1:9810/). It contains the28-second opening, matching three color choices, four level-matched voice auditions, house-key proof and narrated food-card context. Recommendations: ColorB Neutral White; VoiceB Bass Default. Dan has not reviewed or approved this packet yet.

The actual final opening passes independent picture review, and the M6-served bytes match its SHA256 `0687c6c688ea00eaeb63ba71f801c6378398dbf5dc7df9d9bb19cea8e8504913`. All11 unique previews/auditions passed silent playback/seeking checks. Final player state is paused and sound ready; volume-zero preservation was checked. The managed review is cached on both Macs.

Await Dan’s opening/key, color, voice and food-card choices before the full render. Covers/setup remain separate. Production and rebuildable assets stay on M2 at `/Volumes/Extreme/_edit_work/DS-109`; use the task-local LAN peer config there for editcap/review commands if the saved peer connection fails. One production owner; reuse verified keys and all approved choices.

Exact scope, checks and recovery history: [R1 first-review receipt](../../Docs/DS109_R1_FIRST_REVIEW_20261115.md). Original preparation: [November14 checkpoint](../../Docs/DS109_R1_PREP_20261114.md).
