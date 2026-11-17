CONTENT (LFC). Task name: `I Crashed My Tesla LFC R1`.

# RO-39: I Crashed My Tesla Because I Didn't Trust FSD

**Filmed source ready for editing.** Registered 2026-11-14 from the 11/13 shoot. Not edited, rendered, approved, uploaded or scheduled.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `Docs/SHOOT_1113_FOOTAGE_REPORT.md` (format, orientation, camera clock, full roll map).
Script: script TESLA in Next Shoot Filming Scripts, Google Doc `1y9hR6wV0Sj7PEVZbfL6bsV_WTD48W8N8RjUfW6bwcI4`. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`. Never modify the originals.
Times are minutes:seconds into each roll from an audio pass: close, not frame-accurate. Read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting; run `pick_lav.py` if a sidecar is missing.

| roll | range | notes |
|---|---|---|
| `C1914` | 0:00-7:09 | complete |

Orientation: **landscape 3840x2160**. Sony FX30, 29.97p, S-Cinetone / Rec.709 (grade as Rec.709, no log LUT). One stereo LPCM audio stream.

## Build

- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.
- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common on these rolls.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.

## Deliver

One 16:9 long-form. Shorts are cut from it later (List 2), nothing else. Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Pre-made AI clips (Dan approved 2026-11-15, Flow-credits batch 4: new clips)

- **A0272** (Stuck In Traffic): plays under "That's 15 days every year sitting behind the wheel, stressed out, staring at the road.". Another hour stuck in traffic: he drops his head back on the headrest. (7.8 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0272`. Label it AI-generated on the picture.

## Source preparation verified November 17, 2026

Read-only resume check: batch `chat-RO-39-R1` remains enabled and queued with zero production attempts. Both Macs remain full. Preserve the immutable submitted brief and avoid a duplicate editor.

- The canonical M2 roll sidecar exists at `Media/footage-index/11-13-dan-rose-fitness-shoot-green-screen/C1914.roll.json`. Source key: `13690730089:ab5ef4692863fcbb1be494b15bb7343b0f3cf4c7e373345f3c9e23a7910e453c`. It reports 3840x2160, rotation 0, 29.97003 fps and 746.245 s. Transcript has 2,138 words across Tesla plus A15; exclude A15 from about 431 s onward. Verify picture/word cuts before locking any ranges.
- The measured existing lav pick is `-map 0:a:0 -af pan=mono|c0=c0`, single-live, measured over 120 s plus 45 s. Reuse the sidecar result; do not hard-code a channel from another roll.
- The actual crash clips are on the M2, **not** the M6: `~/Documents/Insurance Claims/2026-10-24/claim-attachments/2026-10-24_15-29-29-front.mp4` (79,650,931 bytes) and `2026-10-24_15-29-29-back.mp4` (40,104,657 bytes). Both files' existence and sizes were verified over SSH. The smaller front copy also exists, but prefer the original unless actual inspection gives a reason otherwise.
- Original footage context is recorded in `Handoffs/handoff-20261112-next-shoot-outlines.md`, the Tesla section: impact reported at about 43 s in the rear minute. This is a lookup hint, **not a verified edit point**. Inspect both native recordings silently, match the front/rear timeline, and build the narrated crash sequence from what they actually show. No frames or motion were inspected in this resume check.
- Keep private insurance data, other people's names, trucking-company identifiers, claim/police numbers and exact location out of public records and the film. Select/crop actual footage as needed without obscuring the incident. Do not copy the claims folder or its records into the repo.

No cut map, key calibration, rendered preview, media QC or review link exists yet. First-review approval stop remains required.

## Starter prompts

**Claude: Opus 5.5, high effort.**
> CONTENT (LFC). Name this chat "I Crashed My Tesla LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-39-i-crashed-my-tesla-because-i-didnt-trust-fsd.md`: cut "I Crashed My Tesla Because I Didn't Trust FSD" from the 11/13 green-screen shoot, rolls C1914. Use /longform-edit (long-form green-screen standard: `.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.

**Codex: GPT-6.1 Sol, high effort.**
> CONTENT (LFC). Name this chat "I Crashed My Tesla LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-39-i-crashed-my-tesla-because-i-didnt-trust-fsd.md`: cut "I Crashed My Tesla Because I Didn't Trust FSD" from the 11/13 green-screen shoot, rolls C1914. Use `$long-form-content-edit` with the long-form green-screen standard (`.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key (`.claude/skills/_shared/chroma-key/README.md`). Follow the first-review approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.
