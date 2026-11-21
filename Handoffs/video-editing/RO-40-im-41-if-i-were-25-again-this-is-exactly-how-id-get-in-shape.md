CONTENT (LFC). Task name: `I'm 41. If I LFC R1`.

# RO-40: I'm 41. If I Were 25 Again, This Is Exactly How I'd Get In Shape.

**Filmed source ready for editing.** Registered 2026-11-14 from the 11/13 shoot. Not edited, rendered, approved, uploaded or scheduled.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `Docs/SHOOT_1113_FOOTAGE_REPORT.md` (format, orientation, camera clock, full roll map).
Script: script A15 in Next Shoot Filming Scripts, Google Doc `1y9hR6wV0Sj7PEVZbfL6bsV_WTD48W8N8RjUfW6bwcI4`. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`. Never modify the originals.
Times are minutes:seconds into each roll from an audio pass: close, not frame-accurate. Read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting; run `pick_lav.py` if a sidecar is missing.

| roll | range | notes |
|---|---|---|
| `C1914` | 7:10-12:28 | first half, hook restarts, cut off mid-take |
| `C1915` | 0:19-3:55 | pickup that finishes the video (second card) |

Orientation: **landscape 3840x2160**. Sony FX30, 29.97p, S-Cinetone / Rec.709 (grade as Rec.709, no log LUT). One stereo LPCM audio stream.

## Build

- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.
- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common on these rolls.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.

## Deliver

One 16:9 long-form. Shorts are cut from it later (List 2), nothing else. Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Pre-made AI clips (Dan selected 2026-11-15, Flow-credits batch 4: existing library clips)

- **A0243**: plays under "Train 15 minutes every morning, every day / do it in the morning". AI you in bed before dawn opens his eyes and taps the glowing 5:30 alarm, calm (4.9 s, 16:9). `clip_library.py show A0243`. Label it AI-generated on the picture.
- **A0173**: plays under "I eat less junk, and I do less late night eating". Night kitchen: a man pulls a pizza box loaded with ice cream and cake out of the fridge, spoon in mouth (16:9; use about 1.6 to 5.4 s of the take). Also used in RO-08. `clip_library.py show A0173`. Label it AI-generated on the picture.
- **A0144**: plays under "If you're not weighing yourself, you don't know if what you're doing is working". A shirtless man on a bathroom scale looks down and puts his hand to his forehead (4.0 s, 16:9). Also used in RO-10. `clip_library.py show A0144`. Label it AI-generated on the picture.

## Pre-made AI clips (Dan approved 2026-11-15, Flow-credits batch 4: new clips)

- **A0273** (Learning To Love It): plays under "After a few months I actually started to ENJOY eating like this.". Forcing down a huge plate turns into enjoying it. (7.8 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0273`. Label it AI-generated on the picture.
- **A0274** (Can't Look): plays under "Trying to get abs without weighing yourself daily is like trying to get rich while never looking at your bank account.". He can't bring himself to look at the scale, then peeks. (5.3 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0274`. Label it AI-generated on the picture.

## Starter prompts

**Claude: Opus 5.5, high effort.**
> CONTENT (LFC). Name this chat "I'm 41. If I LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-40-im-41-if-i-were-25-again-this-is-exactly-how-id-get-in-shape.md`: cut "I'm 41. If I Were 25 Again, This Is Exactly How I'd Get In Shape." from the 11/13 green-screen shoot, rolls C1914 + C1915. Use /longform-edit (long-form green-screen standard: `.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.

**Codex: GPT-6.1 Sol, high effort.**
> CONTENT (LFC). Name this chat "I'm 41. If I LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-40-im-41-if-i-were-25-again-this-is-exactly-how-id-get-in-shape.md`: cut "I'm 41. If I Were 25 Again, This Is Exactly How I'd Get In Shape." from the 11/13 green-screen shoot, rolls C1914 + C1915. Use `$long-form-content-edit` with the long-form green-screen standard (`.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key (`.claude/skills/_shared/chroma-key/README.md`). Follow the first-review approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.
