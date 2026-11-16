CONTENT (LFC). Task name: `I Ranked 15 "Healthy" LFC R1`.

# RO-41: I Ranked 15 "Healthy" Foods From Actually Healthy To Basically Candy

**Filmed source ready for editing.** Registered 2026-11-14 from the 11/13 shoot. Not edited, rendered, approved, uploaded or scheduled.

## Read first

`00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, and the shoot report `Docs/SHOOT_1113_FOOTAGE_REPORT.md` (format, orientation, camera clock, full roll map).
Script: script A16 in Next Shoot Filming Scripts, Google Doc `1y9hR6wV0Sj7PEVZbfL6bsV_WTD48W8N8RjUfW6bwcI4`. The filmed wording wins where Dan departed from the script.

## Sources

Working copies: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/`. Verified second copy: `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`. Never modify the originals.
Times are minutes:seconds into each roll from an audio pass: close, not frame-accurate. Read each roll's `.roll.json` sidecar (word timings, mic pick) before cutting; run `pick_lav.py` if a sidecar is missing.

| roll | range | notes |
|---|---|---|
| `C1915` | 4:37-15:55 | several hook takes; acai pronunciation chat about 7:15-8:12 |

Orientation: **landscape 3840x2160**. Sony FX30, 29.97p, S-Cinetone / Rec.709 (grade as Rec.709, no log LUT). One stereo LPCM audio stream.

## Build

- Green screen: key with the approved house key (`.claude/skills/_shared/chroma-key/README.md`), calibrated to these rolls.
- Pick the best take of every line across all takes listed above. Watch the whole range; hook restarts and retakes are common on these rolls.
- Graphics follow the Soft Blue Light HyperFrames standard. AI clip frames, if any, go to Dan as START and END pairs first.
- First review before any full render, per `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.

## Deliver

One 16:9 long-form. Shorts are cut from it later (List 2), nothing else. Covers and upload/setup are separate tasks after Dan approves the film (Codex owns setup).

## Pre-made AI clips (Dan selected 2026-11-15, Flow-credits batch 4: existing library clips)

- **A0143**: plays under "Granola is 480 calories a cup". An overweight man eats granola at a table loaded with "healthy" food (4.0 s, 16:9). Also used in RO-10. `clip_library.py show A0143`. Label it AI-generated on the picture.
- **A0181**: plays under "One cup of trail mix is about 700 calories. That's more than a Big Mac". A balance scale: trail mix poured onto one pan outweighs a double cheeseburger (16:9). Also used in RO-17. `clip_library.py show A0181`. Label it AI-generated on the picture.
- **A0183**: plays under "Trail mix and dried fruit sound healthy, but they're loaded with calories". A packing worker pours candy-coated chocolates into a jar of nuts and raisins and winks (5.0 s, 16:9). Also used in RO-17. `clip_library.py show A0183`. Label it AI-generated on the picture.
- **A0185**: plays under "A cup of raisins is 493 calories. A cup of grapes is 106". Raisins poured into a palm beside a bunch of grapes (4.3 s, 16:9). Also used in RO-17. `clip_library.py show A0185`. Label it AI-generated on the picture.

## Pre-made AI clips (Dan approved 2026-11-15, Flow-credits batch 4: new clips)

- **A0275** (The Health Food Aisle): plays under "I ranked 15 "healthy" foods, and nine of them belong in the candy aisle.". The health food aisle is all candy. (5.3 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0275`. Label it AI-generated on the picture.
- **A0276** (Just A Quarter Cup): plays under "And nobody pours a quarter cup. You pour a bowl, you eat a bowl.". The measuring cup sits there while he fills the whole bowl. (7.7 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0276`. Label it AI-generated on the picture.
- **A0277** (Cola For Breakfast): plays under "If you wouldn't drink a Coke with breakfast every morning, you shouldn't be drinking orange juice every morning either.". Cola in the juice glass with breakfast. (5.3 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0277`. Label it AI-generated on the picture.
- **A0278** (Two Tablespoons): plays under "But nobody is scooping out exactly two tablespoons. You're digging a spoon into the jar.". Two tablespoons, he says: a giant spoonful. (7.8 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0278`. Label it AI-generated on the picture.
- **A0279** (Three Cans): plays under "That's 530 calories and 119 grams of sugar. That's the sugar in three cans of Coke.". His healthy smoothie next to the three cans of soda it equals. (5.3 s, 16:9, silent; full usable length, trim in context). `clip_library.py show A0279`. Label it AI-generated on the picture.

## Starter prompts

**Claude: Opus 5.5, high effort.**
> CONTENT (LFC). Name this chat "I Ranked 15 "Healthy" LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-41-i-ranked-15-healthy-foods-from-actually-healthy-to-basically.md`: cut "I Ranked 15 "Healthy" Foods From Actually Healthy To Basically Candy" from the 11/13 green-screen shoot, rolls C1915. Use /longform-edit (long-form green-screen standard: `.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue.

**Codex: GPT-6.1 Sol, high effort.**
> CONTENT (LFC). Name this chat "I Ranked 15 "Healthy" LFC R1". Read `Handoffs/video-editing/00-RULES.md` and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`, then execute `Handoffs/video-editing/RO-41-i-ranked-15-healthy-foods-from-actually-healthy-to-basically.md`: cut "I Ranked 15 "Healthy" Foods From Actually Healthy To Basically Candy" from the 11/13 green-screen shoot, rolls C1915. Use `$long-form-content-edit` with the long-form green-screen standard (`.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`). Key with the approved house chroma key (`.claude/skills/_shared/chroma-key/README.md`). Follow the first-review approvals before the full render. Deliver, send Dan the review copy, update `00-MASTER.md`.
