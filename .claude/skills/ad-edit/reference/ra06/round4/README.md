# RA-06 round 4 (2026-10-15): the 16:9 from an approved 9:16, gates on both, delivery

Work dir `/Volumes/Extreme/_edit_work/ra06/`. The copies here are the round 4 versions; `s10_render06.py`, `s06_split.py`,
`s06_inserts06.py` and `ra01lib.py` were edited in place in the work dir (round 3 copies are in `../round3/` and `..`).

## Order

| # | command | makes |
|---|---|---|
| 1 | re-hash the locked files into `round4/HASHES.json`; copy the approved 9:16 | the 9:16 master |
| 2 | `python3 s06_split16.py` | the 16:9 opener: vacuum tall left, plank and toe touches as two 16:9 panels right, ending at y 900 |
| 3 | `python3 gfx16.py` (loads `hv16.py`, RA-15's 1920x1080 copy of `vertical.py`) | LT2 (narrow bottom-left strip), CTA upper left, plates |
| 4 | `python3 s06_inserts16.py` then `python3 s06_beside16.py` | AI clips whole in plates; the four app cards as Dan beside a phone panel |
| 5 | `python3 s07_captions16.py 16x9` | captions; lifts only over strips that reach the centred caption |
| 6 | `r4_chain16.sh` (outputs on `/Volumes/Expansion/_edit_work/ra06_r4/`) | picture + mux with the approved `mix.wav` |
| 7 | per file: `audio_gate.py`, `s20_neg.py` after looking, `r4_measure.sh`, `s_chips06.py`, `s_gateplan06.py`, `watch.py` + fresh judge, `gate.py` | stamps |
| 8 | `s_sheet06.py <16:9 master>` then `validate.py --hash` | the edit sheet |

## What this round taught

1. **Run the delivery gate on an approved 9:16 before calling it final.** Round 3 ran only the audio gate; the full gate found two
   caption collisions in the file Dan approved (the I4 chip 13 px INTO the caption ink, the vacuum label 1 px short). `cardiff.py`
   proves a re-composite changed only the moved labels (outside them: mean 0.1-0.4 levels, encoder noise).
2. **Refresh the chip references after moving a chip.** `compliance:labels` and `captions:graphic_clearance` both read
   `round4/chips/chips.json`; a stale one failed both rows on a correct file.
3. **9:16 clips as small plates on the field fail in 16:9 for app screens.** Two independent checks called a 478x852 phone on a
   1920x1080 field "80 % empty" (ad-edit lesson 83). The approved fix is Dan on camera beside the phone (VIDEO-RULES 2026-10-10):
   `s06_beside16.py` takes his own footage under the card (asserting no source join inside it), shifts him right with
   `softblue.shift_presenter` by a DX measured from his person mask, and caps the panel at 520 px wide (a 702 px flow panel pushed
   his reach off the frame). The AI story clips stay as plates.
4. **Showing Dan under a former card exposes the joins at its edges.** flow_b | tour2 was a source join hidden by the card change;
   with Dan on both sides at one size it is a jump cut. Give the beside cards a size per card so every source join changes size.
5. **A 1.136x zoom step reads as a near-jump** (the 16:9 judge measured 237 px to 210 px head width). On a 2160-wide portrait roll
   FAR is capped at 2144; NEAR 1792x1008 gives 1.196x and still ends at the belly button.
6. **The full-width 16:9 lower third covers his abs in a FAR shot.** A narrow strip in the corner his body leaves clear (person mask
   over the strip's span) keeps the template and copy; captions then need no lift.
7. **The first talking frame after a card can catch a head turn** (2.302 s). Hold the card a few frames (`r4_16x9_overrides.json`,
   read by the split builder, the render and the gate plan) rather than trimming the speech.
8. **The Extreme drive filled to 0 bytes mid-build** (another job's 3.6 GB temp file); the render died with an empty log and Python
   exit 120. `df` first when a stage dies silently; render outputs went to the Expansion drive through symlinks.
10. **A phone beside Dan on two cards with him alone between them is a sideways hop if the footage is continuous.** flow_a | dan06 |
    flow_b is one unbroken piece at FAR: the picture jumped 102 px left and 270 px right mid-sentence (the gate and the watch judge
    both passed it; the independent reviewer caught it, because the gate treats beside-Dan cards as cards). Keeping the phone up
    through dan06 would cut the sample man's before photo straight to his AI after, which Dan's before, something else, after rule
    forbids. What passed: one shared offset for flow_a and flow_b, and dan06 at NEAR with no phone (`level16` in the overrides), so
    both layout changes are size changes and Dan is the something else.
9. **The edit-sheet validator requires a real/AI label on any picture of Dan with physique.** The split opener is exercise footage,
   classified `physique: false` with the reason written in the sheet (as approved in the 9:16, no chip).
