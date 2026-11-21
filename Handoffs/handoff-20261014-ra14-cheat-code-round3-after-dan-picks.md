# RA-14 "The Cheat Code For Six Pack Abs": round 3 (opener motion, Soft Blue analysis card, moving previews, first 30 s)

**AD (short-form, filmed).** Sidebar name for the next task: `Cheat Code Six Pack AD R3`.
Written 2026-10-14 after Dan's round 2 picks (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-14-cheat-code-for-six-pack-abs.md`.
Read first: `.claude/skills/_shared/VIDEO-RULES.md` (the first two sections are new on 10-14), `_shared/PRE-RENDER-APPROVAL.md`,
the `/ad-edit` skill (its "RA-14 round 2 lessons"), `_shared/IMAGE-GENERATION.md`, `_shared/hyperframes/README.md`.
Round 2 brief and state: `Handoffs/handoff-20261013-ra14-cheat-code-round2-after-dan-review.md` ("ROUND 2 BUILT").
Dan's words, verbatim, per item, with hashes: `/Volumes/Extreme/_edit_work/ra14/round3-plan/decisions.json`.

## What Dan picked (2026-10-14, page http://127.0.0.1:8815/)

| item | pick | his words |
|---|---|---|
| Opener | **O2 8-bit power-up** (motion authorized for O2 only) | "let's go with opener O2: the 8-bit power-up" |
| Framing | **F2 Wider**: close 576x1024, wide 720x1280 (`framing_choice.json`) | "a wider crop, the recommended crop" |
| Colour | **C2 Brighter, golden skin** (`grade.json` now holds the one LUT) | "the brighter golden skin, the recommended color" |
| Analysis card A1 | **redraw in Soft Blue Light with HyperFrames, as the standard for every video** | "Redo the analysis card in our graphics in soft blue light with our hyperframes. Make that standardized with the rest of our videos." |
| Voice | **`mix_bass.wav`** (+3 dB at 120 Hz) | "Let's do the voice with a bass lift." |
| Recap list R1 | **not answered** (asked in rounds 1 and 2) | none. Show R1 moving in context and ask once more. Never treat "keep" (the recommendation) as his answer. |

New standing rules from the same reply, already written: outdoor videos show colour, audio and crop options in round 1
(studio uses the standard), and the Soft Blue HyperFrames analysis card is the standard everywhere. VIDEO-RULES.md, first
two sections; memory `outdoor-look-options-round-one`, `analysis-card-reusable-graphic`.

## Round 3 deliverable: one review page, then stop

Build in `/Volumes/Extreme/_edit_work/ra14/round3/` and serve it with `review_server.py` on a free port (check `lsof`;
8814 and 8815 are rounds 1 and 2, keep them).

1. **O2 opener motion, 0.00 to 3.64 s** under "Guys have figured out the cheat code for getting six pack abs.", hard cut to
   Dan close on "It's AI." From the approved frames only: `round2/frames/O2-start.png`, `O2-end.png` (raw Codex originals
   in `round2/opener/raw/`). Plan from round 2: he runs right about 1.2 s, touches the power-up, a white flash of 3 frames,
   then he flexes with pixel abs while the counter flips ABS X0 to ABS X6 (counter drawn in code, `s71_opener_frames.pixel_text`).
   **Try code first ($0):** ask Codex (subscription, `codex-image.sh --model gpt-6.1-sol --effort high`, the start frame as
   reference) for a small set of matching sprite poses (2 to 4 run frames, 1 transition, the flex), composite them on the
   start frame's background in code with NEAREST scaling, step the run cycle on 2s or 3s like an 8-bit game, scroll nothing
   or scroll the ground in whole pixels. If it looks stiff, one video model take from the frame pair (about $1; budget $10,
   spent $0). Check it against the three sense questions and the AI clip rules before Dan sees it; the AI-GENERATED chip
   stays low left, clear of the sprite.
2. **The Soft Blue analysis card (A1), built as the SHARED standard**, not a per-video recipe: a HyperFrames template beside
   `_shared/hyperframes/side-list`, `media-card` etc., wired into `vertical.py` (and the 16:9 path) so `from_plan.py` can
   draw it. Content as approved on RA-01 (`_shared/adkit/analysis_card.py`, README): the subject picture, a scan line,
   BODY FAT / FAT TO LOSE / MUSCLE TO GAIN bars, the plan band, no printed numbers, one AI-GENERATED chip placed by person
   mask. Use it on "It measures exactly how much fat you have to lose and where you need to gain muscle." (22.42 to 26.59 s).
   Update `_shared/adkit/README.md` and the HyperFrames README to point at it.
3. **Every graphic and clip moving in context** (round method step 3 and 4): L1, P1, L2, A1, L3, T1, R1, C1 on the new framing
   and colour, each with a "Play it moving, in context" button (about 3 s of speech either side). L1 now sits on the close
   shot: confirm it clears his face over the whole hold with the person mask.
4. **The finished first 30 seconds** (the ad is 50.5 s, so 30 s is the first-minute step): O2 opener, approved framing, C2,
   captions, L1, P1, L2, A1 and whatever is ready, `mix_bass.wav`. Any item not yet approved is a labelled placeholder.
5. **Carried work (decided, not questions):** measure the inside-hold pause splices at 11.38, 19.72, 31.13, 41.38 and 42.64 s on
   rendered picture (the 4.44 s one was a visible jump; round 2 lesson 5) and give each visible one a size change or cover;
   captions lift above the recap card (`s07_captions.py` per-state y); the phone demo renderer (`s63_stills.py phone_card` has
   the shell); music tail fix (`s42_bed.py`) and frame-lock `mix_bass.wav` once the length is final; re-run the audio gate on
   the final mix. 16:9 after the 9:16 is approved.
6. Page in the standard layout (first 30 s on top, then the O2 motion, then "What I decided", then every item in order three
   per row). Decisions: O2 motion (approve or redo), A1 Soft Blue card, R1 recap list (third ask), anything genuinely new.

Then record his answers, write the round 4 handoff (full 9:16, gates, watch pass, independent review, delivery, then 16:9)
and stop.

## Locked (re-hash before touching; sha256 first 16)

| file (under `/Volumes/Extreme/_edit_work/ra14/`) | what | hash |
|---|---|---|
| `cut.json` | take map and cut, 48.81 s of talk | 394e9127a580ce5c |
| `mix_bass.wav` | the approved voice (+3 dB at 120 Hz) and bed | a969e60b871ecd8d |
| `words_aligned.json` | 168 words aligned to the mix | b01781a5203792fb |
| `framing.json` | head track, 241 samples (round 2 adds `framing_holdstart.json`) | d798e48e215d593a |
| `round2/frames/O2-start.png`, `O2-end.png` | approved opener frames | in `round3-plan/decisions.json` |
| `round2/colour/luts/ra14_C2_brighter_gold.cube` | approved grade | in `round3-plan/decisions.json` |

`beats.json` (round 2 plan with the O0 opener slot) and `beats_camopen.json` are the current plan; the shot order of the
opening was changed in round 2 because of the 4.44 s jump (close / wide / close / wide / close from the 10.58 s seam).

## Recipe and machine

Scripts in `/Volumes/Extreme/_edit_work/ra14/` and `.claude/skills/ad-edit/reference/ra14/round2/`: `s60_plan.py`,
`s04b_holdstart.py`, `s71_opener_frames.py`, `s72_sample.py` (input seek, one decode for all candidates), `s73_r2_stills.py`,
`s74_page.py`, `colour/lab.py`, `colour/bake.py`. `ra01lib.grade()` now returns the LUT in `grade.json`; `ra01lib.Aspect`
reads `framing_choice.json`. The Mac runs other sessions' renders: wait through `_shared/buildcap.py` (`buildcap.wait()`).

## Gate status

Audio gate PASS on `mix_bass.wav` from round 1 (re-gate the final mix). Nothing else has run; there is no finished file.
Spend $0 of $10.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Cheat Code Six Pack AD R3`. Read `Handoffs/handoff-20261014-ra14-cheat-code-round3-after-dan-picks.md` and run round 3 of RA-14 "The Cheat Code For Six Pack Abs" with /ad-edit. Use the Codex subscription to generate the images. Make the 8-bit power-up opener move from my approved frames (code first, a video model only if that looks stiff), build the Soft Blue Light analysis card as the shared HyperFrames standard for every video, show me every graphic and clip moving in context, ask me about the recap list again, and give me the finished first 30 seconds. One review page, then stop for my picks.
