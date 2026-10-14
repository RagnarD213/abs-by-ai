# RA-14 "The Cheat Code For Six Pack Abs": round 4 (record Dan's round 3 picks, then the full 9:16)

**AD (short-form, filmed).** Sidebar name for the next task: `Cheat Code Six Pack AD R4`.
Written 2026-10-14 at the end of round 3 (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-14-cheat-code-for-six-pack-abs.md`.
Read first: `.claude/skills/_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, the `/ad-edit` skill (sections "RA-14 round 2
lessons" and "RA-14 round 3 lessons"), `_shared/hyperframes/README.md`. Round 3 brief: `handoff-20261014-ra14-cheat-code-round3-after-dan-picks.md`.

## Round 3 page: http://127.0.0.1:8819/ (folder `/Volumes/Extreme/_edit_work/ra14/round3/`)

Rounds 1 (8814) and 2 (8815) stay up. Dan's three questions on the page:
1. **Opener O2, moving:** A approve (recommended) / B changes / C one video-model take from the frame pair (about $1).
2. **A1, the Soft Blue analysis card** (the new standard for every video): A approve (recommended) / B changes.
3. **R1, the recap list** (asked in rounds 1, 2 and 3): A keep (recommended) / B no card. Never treat A as his answer.

## What round 3 built (all on the page; nothing below is approved yet)

- **O2 opener** `round3/opener/O2.mp4` (109 frames, 0 to 3.64 s), built in code ($0) by `s81_opener.py`: frame 0 is the approved start
  frame, the flex is lifted from the approved end frame, one Codex sheet (`raw/o2_runsheet.png`) gave run pose 2. Two side-on run poses,
  hip-aligned by measured upper-body overlap, 2.3 px per frame; he runs INTO the tile at 1.23 s (no hop: the hop put the tile over his
  face), the tile pops 24 px, a 3-frame flash, an 8-frame small/big flicker, then the flex with a whole-body squeeze every 12 frames;
  the counter (top right, clear sky) reaches x6 at frame 89. Four independent reviews; their findings fixed; the fourth review's one
  fault (elbow gap in the squeeze) fixed and checked by eye at native size. No fresh review of that last change.
- **A1** is the shared template `_shared/hyperframes/analysis-card/` (pushed, commit 48bb0ab plus the start-state fix below): 16:9
  `build.py`, 9:16 `vertical.py`, 1:1 `square.py`, `from_plan.py` kind `analysis`. RA-14 config in `round3/gfx_sheet_r3.json`: rows land on
  "fat" 24.06, "lose" 24.66, "where" 25.40, band on "need" 25.82; chip under the picture; card ends at y 1376, captions run under it.
- **Shot plan** `beats_r3.json` (`s84_plan.py`): every in-hold pause splice (11.38, 19.72, 31.13, 41.38, 42.64 s) measured visible on the
  rendered picture (head moved 15 to 40 px) and given a size change; a one-frame flash of the other take at 10.54 s removed; the step one
  hold slips its first 5 frames into the removed pause (`picture_slip`), so the 10.68 s join is gone. 17 holds, all cuts change size.
- **Holds** `round3/seg/danNN.mp4` (`s82_holds.py`, F2 framing, C2 LUT). **Phone cards** `round3/cards/P1.mp4`, `T1.mp4` (`s83_phone.py`,
  1.0x, crop screen skipped, real-picture chip only while his photo is on the phone). **Captions** `round3/cap_9x16` (`s85_captions.py`):
  lifted whole lines to y 1049 over R1; hand-overs clipped. **Graphics** `round3/gfx` (vertical.py renders of L1 L2 A1 L3 R1 C1).
- **Composite** `round3/work/picture_9x16.mp4` (`s86_assemble.py work`, all 1512 frames, picture only, never shown whole) and the cuts:
  `DRAFT - RA-14 round 3 - first 30 seconds.mp4` (0 to 30.30 s, + REVIEW 540p), `context/<ID>-context - REVIEW 540p.mp4`.
- **Checks** (`s88_checks.py`, `round3/checks_raw.json`): face at least 374 px above every lower third, the button and R1; zero caption
  collisions with any graphic; A1 card above the captions. Strips of every cut in the first 30 s: `round3/checks/cuts_*.jpg` (all cuts
  change size).
- **Voice** `mix_bass_r3.wav` = Dan's `mix_bass.wav` trimmed to 1512 frames, 24-bit. Not gated yet.

### Bugs found and fixed this round (carry the lessons)
- `ra01lib.encode_h264` wrote BT.601 YUV under a BT.709 tag (frame 0 of O2 was 26 levels off). Fixed in this job's `ra01lib.py`. The shared
  `_shared/adkit/cardlib.py` and other jobs' copies have the same bug: separate task chip offered to Dan, not fixed here.
- The analysis card's bars showed filled on the first frame: a later GSAP `fromTo` wrote its start value at time 0. Fixed with
  `immediateRender: false` in the template.
- A hung RA-05 `voice_chain.py` (orphaned, 16 h at 0 % CPU, cwd `/Volumes/Extreme/_edit_work/ra05`) held a build slot; killed. Its
  `mix.wav` from 10-13 18:04 was already on disk.

## Locked (re-hash before touching; sha256 first 16)

| file (under `/Volumes/Extreme/_edit_work/ra14/`) | hash |
|---|---|
| `cut.json` | 394e9127a580ce5c |
| `mix_bass.wav` (approved voice) | a969e60b871ecd8d |
| `words_aligned.json` | b01781a5203792fb |
| `framing.json` | d798e48e215d593a |
| `round2/frames/O2-start.png`, `O2-end.png` | 44323801cacdf80d, da3f482f899b023c |
| `round2/colour/luts/ra14_C2_brighter_gold.cube` | 4e222c22be62cdfd |

Round 3 files on the page (not approved): `beats_r3.json` 5ccd71cb0aad3d14, `mix_bass_r3.wav` 84d5c8831b57c2c3, `round3/opener/O2.mp4`
fb479022004e9c07, `round3/opener/raw/o2_runsheet.png` 188f184a1535b220, `round3/cards/P1.mp4` 04b715ab683b7b00, `round3/cards/T1.mp4`
39a2f9bdf5b5f2ee, `round3/gfx/renders/A1.mov` 7cfa16597c98b7bd, `round3/cap_9x16/captions.mov` f3116b522e4ab7ce,
`round3/DRAFT - RA-14 round 3 - first 30 seconds.mp4` c7b1188389096ead.

## Round 4: exact next actions

1. Record Dan's reply verbatim in `/Volumes/Extreme/_edit_work/ra14/round4-plan/decisions.json` (per item: id, path, sha256, verdict, his
   words, scope, next), with `motion_authorized` / `new_frames_before_motion`. If he asks for changes to O2 or A1, make them, show only
   those, and stop again. If R1 is answered "no card", drop it from `gfx_sheet_r3.json`, rebuild captions at the normal height for that
   window (`s85_captions.py`), and re-check the 41.38 / 42.64 s size changes still read without the card.
2. If all three are settled: the full 9:16 from the locked parts (`s86_assemble.py work` already composes all 1512 frames; mux
   `mix_bass_r3.wav`), then the music tail: two rests at 49.2 and 49.6 s dip 6 to 7 dB inside the final fade (RA-01's step was 15 dB).
   Listen; smooth with `s42_bed.py` only if audible, then re-make the mix and null-test it against `mix_bass.wav` up to 47 s.
3. Gates on the exact delivered file: `audio_gate.py` (outdoor `artifacts` row is Dan's known exception for these rolls, ad-edit RA-01
   lesson 2), the edit sheet (`sheet_from_claude_build.py`, then `validate.py --hash`), `watch.py` + a fresh judge, `gate.py --format
   ad9x16` (check the format name with `gate.py --formats`), then one independent reviewer on the delivered file (ra-reviewer agent),
   including the three sense questions for O2.
4. Deliver to `Claude Ad Videos/the cheat code for six pack abs - RA-14/` (`... | claude | 9x16 | RA-14.mp4` + REVIEW copy + stamps),
   copy to `Videos to Review/` (the ad is 50.5 s), send the page, set the queue to `delivered`.
5. After Dan approves the 9:16: the 16:9 (the A1 card's 16:9 layout exists; lower thirds and R1 use the 3A card at 16:9).

Budget: $10 for this ad; spent $0 (the Codex sheet was on the subscription). Recommended model: Claude Opus 5.5, high effort.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Cheat Code Six Pack AD R4`. Read `Handoffs/handoff-20261014-ra14-cheat-code-round4-after-dan-picks.md` and run round 4 of RA-14 "The Cheat Code For Six Pack Abs" with /ad-edit. My round 3 picks: [paste the reply box from http://127.0.0.1:8819/]. Record my answers, make any change I asked for, and if nothing is pending build the full 9:16 with every gate and an independent review, then deliver it and stop for my review.
