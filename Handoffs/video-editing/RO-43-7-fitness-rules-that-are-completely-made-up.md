CONTENT (LFC). Task name: `7 Fitness Rules That LFC R1`.

# RO-43: 7 Fitness Rules That Are Completely Made Up

**Filmed source ready for editing.** Registered 2026-11-14 from the 11/13 shoot. Not edited, rendered, approved, uploaded or scheduled.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `Docs/SHOOT_1113_FOOTAGE_REPORT.md` (format, orientation, camera clock, full roll map).
Script: script A18 in Next Shoot Filming Scripts, Google Doc `1y9hR6wV0Sj7PEVZbfL6bsV_WTD48W8N8RjUfW6bwcI4`. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`. Never modify the originals.
Times are minutes:seconds into each roll from an audio pass: close, not frame-accurate. Read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting; run `pick_lav.py` if a sidecar is missing.

| roll | range | notes |
|---|---|---|
| `C1915` | 25:26-34:29 | several hook takes and retakes across the seven points |

Orientation: **landscape 3840x2160**. Sony FX30, 29.97p, S-Cinetone / Rec.709 (grade as Rec.709, no log LUT). One stereo LPCM audio stream.

## Build

- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.
- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common on these rolls.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.

## Deliver

One 16:9 long-form. Shorts are cut from it later (List 2), nothing else. Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Pre-made AI clips (Dan approved 2026-11-15, Flow-credits batch 4: new clips)

- **A0283** (Eight Glasses): plays under "So for decades, people have been forcing down glass after glass of water because of half of a sentence in a government report.". Forcing down eight glasses of water at his desk. (7.8 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0283`. Label it AI-generated on the picture.
- **A0284** (Treadmill Milkshake): plays under "No amount of cardio is going to fix your drinks and your snacks.". Strolling in the fat-burning zone with a milkshake. (7.8 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0284`. Label it AI-generated on the picture.
- **A0285** (Kitchen Closed): plays under "Don't eat any food after 7 PM. So where did it come from? Nobody knows.". The fridge is locked: closed after 7 PM. (7.8 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0285`. Label it AI-generated on the picture.
- **A0286** (Meal Four Of Six): plays under "Rule number five. Eat six small meals a day to stoke your metabolism.". Six small meals a day: he opens the next one on schedule. (5.3 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0286`. Label it AI-generated on the picture.
- **A0287** (The Rule Book): plays under "Here are 7 bullshit fitness rules that are still incredibly popular.". Into the bin: the old fitness rule book. (2.5 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0287`. Label it AI-generated on the picture.

## Starter prompts

**Claude: Opus 5.5, high effort.**
> CONTENT (LFC). Name this chat "7 Fitness Rules That LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-43-7-fitness-rules-that-are-completely-made-up.md`: cut "7 Fitness Rules That Are Completely Made Up" from the 11/13 green-screen shoot, rolls C1915. Use /longform-edit (long-form green-screen standard: `.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.

**Codex: GPT-6.1 Sol, high effort.**
> CONTENT (LFC). Name this chat "7 Fitness Rules That LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-43-7-fitness-rules-that-are-completely-made-up.md`: cut "7 Fitness Rules That Are Completely Made Up" from the 11/13 green-screen shoot, rolls C1915. Use `$long-form-content-edit` with the long-form green-screen standard (`.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key (`.claude/skills/_shared/chroma-key/README.md`). Follow the first-review approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.
