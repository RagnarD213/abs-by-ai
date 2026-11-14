AD (Great Again T long ad). Task name: `GAT L02 AD R1`.

# RA-18: Great Again T L02: 3 "Healthy" Foods That Are Killing Your Testosterone

**Filmed source ready for editing.** Registered 2026-11-14 from the 11/13 shoot. Not edited, rendered, approved, uploaded or scheduled.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `Docs/SHOOT_1113_FOOTAGE_REPORT.md` (format, orientation, camera clock, full roll map).
Script: script L02 in Great Again T Ad Outlines (23 ads), Google Doc `1i_8S6ZkMDMdh17jSYe7K4JJmPNaXwnR-tGXhXhkZYU0`. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`. Never modify the originals.
Times are minutes:seconds into each roll from an audio pass: close, not frame-accurate. Read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting; run `pick_lav.py` if a sidecar is missing.

| roll | range | notes |
|---|---|---|
| `C1913` | 12:40-17:48 | landscape take |
| `C1905` | 8:38-13:07 | portrait take, alternates only |

Orientation: **landscape 3840x2160**. Sony FX30, 29.97p, S-Cinetone / Rec.709 (grade as Rec.709, no log LUT). One stereo LPCM audio stream.

## Build

- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.
- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common on these rolls.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.

## Deliver

One 16:9 long ad (3 to 5 minutes, YouTube ads). Vertical, square and 1-minute versions come later as List 3 jobs after you approve this cut. Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Starter prompts

**Claude: Opus 5.5, high effort.**
> AD (Great Again T long ad). Name this chat "GAT L02 AD R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RA-18-great-again-t-l02-3-healthy-foods-that-are-killing-your-test.md`: cut "Great Again T L02: 3 "Healthy" Foods That Are Killing Your Testosterone" from the 11/13 green-screen shoot, rolls C1913 + C1905. Use /ad-edit. Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.

**Codex: GPT-6.1 Sol, high effort.**
> AD (Great Again T long ad). Name this chat "GAT L02 AD R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RA-18-great-again-t-l02-3-healthy-foods-that-are-killing-your-test.md`: cut "Great Again T L02: 3 "Healthy" Foods That Are Killing Your Testosterone" from the 11/13 green-screen shoot, rolls C1913 + C1905. Use `.claude/skills/ad-edit/SKILL.md`. Key with the approved house chroma key (`.claude/skills/_shared/chroma-key/README.md`). Follow the first-review approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.
