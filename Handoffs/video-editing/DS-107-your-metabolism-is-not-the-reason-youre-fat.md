CONTENT (SFC). Task name: `Metabolism Not The Reason SFC R1`.

# DS-107: Your Metabolism Is Not The Reason You're Fat

**Filmed source ready for editing.** Registered 2026-11-14 from the 11/13 shoot. Not edited, rendered, approved, uploaded or scheduled.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `Docs/SHOOT_1113_FOOTAGE_REPORT.md` (format, orientation, camera clock, full roll map).
Script: script B08 in Next Shoot Filming Scripts, Google Doc `1y9hR6wV0Sj7PEVZbfL6bsV_WTD48W8N8RjUfW6bwcI4`. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`. Never modify the originals.
Times are minutes:seconds into each roll from an audio pass: close, not frame-accurate. Read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting; run `pick_lav.py` if a sidecar is missing.

| roll | range | notes |
|---|---|---|
| `C1908` | 1:21-4:12 |  |

Orientation: **portrait (stored 3840x2160 with rotation -90; decode to 2160x3840, add no transpose)**. Sony FX30, 29.97p, S-Cinetone / Rec.709 (grade as Rec.709, no log LUT). One stereo LPCM audio stream.

## Build

- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.
- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common on these rolls.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.

## Deliver

One dedicated vertical Short. Nothing derived from it. Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Starter prompts

**Claude: Opus 5.5, high effort.**
> CONTENT (SFC). Name this chat "Metabolism Not The Reason SFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/DS-107-your-metabolism-is-not-the-reason-youre-fat.md`: cut "Your Metabolism Is Not The Reason You're Fat" from the 11/13 green-screen shoot, rolls C1908. Use /shorts. Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.

**Codex: GPT-6.1 Sol, high effort.**
> CONTENT (SFC). Name this chat "Metabolism Not The Reason SFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/DS-107-your-metabolism-is-not-the-reason-youre-fat.md`: cut "Your Metabolism Is Not The Reason You're Fat" from the 11/13 green-screen shoot, rolls C1908. Use `$long-form-content-edit` for take selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Key with the approved house chroma key (`.claude/skills/_shared/chroma-key/README.md`). Follow the first-review approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.
