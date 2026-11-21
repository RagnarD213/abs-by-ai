# Calories Shorts R3 revision recipe

CONTENT (SFL), 2026-10-19. Work: `/Volumes/Extreme/_edit_work/sl08/round3/`. R2 remains immutable. This is the established R2 renderer plus the scoped R3 changes; do not rerun prepare.py or adapt.py from the historical baseline.

- All five selections, grade and approved source mix are retained. A removes exactly33frames/1.1011seconds, new parent start250.083166667. Its audio is the exact approved R2 PCM cut, with a15ms quiet-head fade only. The original aligned word map is shifted and captions regenerated. B-E openings remain unchanged.
- A01 replaces the rejected steak/salad opening with Dan working at a desk then eating the salad beside him. No verified matching existing Dan clip was found; A0169 is a different man and RO26 Nutrition B is a patio shot. The exact requested replacement frame pair passed the frame gate and fresh independent review.
- D01 uses stacked ripped-Dan sardines over heavy-Dan chips and crackers. The first END failed the independent arm-proportion review; its replacement keeps arms fixed while heads lean to food and passed fresh checks. Rejected evidence is retained.
- New frames still need Dan approval before Flow subscription motion. `pending_frame_approval` in plans.py blocks full A/D renders. Their independently assembled tails are assembly parts, not complete Shorts or final deliverables. A opening captions usey1640 and D opening captions usey1500 for scene clearance; other captions retain the established position.
- B/C/E complete candidates are assembled and receive exact MP4 audio stamps, ASR, native watch evidence, independent judgments and full delivery gates. Do not reuse R2 excerpt or WAV stamps. Status and final hashes belong in the R3 result receipt, not this recipe.
- `page_round3.py` verifies both frame gates and retains the repaired R2 player controls. R3 uses its separate review page onport9008. Never interact with Dan's active R2 page onport8998. Only copy complete Shorts into review/full after final checks pass. No covers, uploads, scheduling or publishing.

The grade, library clips, original title/graphic renders and source remain external read-only dependencies retained by R2 and its verified Drive archive. New images, approval specs, final candidates, proof and notes are retained in the R3 backup. API keys are read from the existing secret store and are never embedded in these scripts.

## Title band descender fix (2026-10-22)

`lib.band()` now draws the title at y 86 with a 96 px line step (was 96 / 100). With title-case titles, a second line with g, j, p, q or y at 88 px ran its descenders to row 312, cut by the glass line at 309 and the picture at 310 (SL-17 reviewer B5; 11 delivered Shorts were affected, `Docs/SHORTS_TITLE_BAND_AUDIT_20261022.md`). The lowest glyph row is now 298. `batch.py gfx|proof|render` runs `_shared/softblue_titlecheck.py` on every TITLE first and stops if any lowest white row is 299 or lower down. Check a batch by hand: `python3 .claude/skills/_shared/softblue_titlecheck.py titles <batch dir>`.
