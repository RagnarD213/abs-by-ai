# RA-14 "The Cheat Code For Six Pack Abs": round 2 (opener frames, wider framing, colour options)

**AD (short-form, filmed).** Sidebar name for the next task: `Cheat Code Six Pack AD R2`.
Rewritten 2026-10-13 after Dan reviewed round 1 (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-14-cheat-code-for-six-pack-abs.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, the `/ad-edit` skill,
`_shared/PRE-RENDER-APPROVAL.md`, `_shared/IMAGE-GENERATION.md`.
Dan's words, verbatim, with every item: `/Volumes/Extreme/_edit_work/ra14/round2-plan/decisions.json`.

## What Dan said about round 1 (page http://127.0.0.1:8814/)

1. **Framing:** "I want both the tight and the wide shot a little bit wider. Both are a little bit too tight."
2. **Colour:** "I want to see some color correction options here. I feel like we can do better with the color corrections."
3. **The AI picture at 5 seconds (G1): out.** "That's kind of the opposite of the point we're trying to get across here,
   and just use the camera scene. That'll be right after the AI-generated clip we're about to make in the beginning."
4. **A new AI opener.** From ten ideas he picked three for START and END frames: **Character creator, 8-bit power-up,
   Arcade combo.**

He has NOT answered round 1's three questions (analysis card look, voice, recap list). They stay open: ask again on the
round 2 page, never treat a recommendation as his answer.

## Round 2 deliverable: one review page, then stop

Build in `/Volumes/Extreme/_edit_work/ra14/round2/`, serve with `review_server.py` on a free port (8814 is round 1; keep it).

### A. Opener frames (top of the page)

START and END frame for each of the three ideas, 1080x1920. **Use the Codex subscription to generate the images**
(`.claude/skills/_shared/codex-image.sh`, GPT-6.1 Sol high). No motion is generated this round. The clip fills 0.00 to
3.64 s under "Guys have figured out the cheat code for getting six pack abs.", then hard cut to Dan, close size, on
"It's AI." If he approves none, the opening stays the camera scene.

| id | name | what you see |
|---|---|---|
| O1 | Character creator | A video game character screen: an ordinary guy shown head to knees. A slider drags from one end to the other and his body goes from soft to ripped as it moves. START = slider at the low end, soft build. END = slider at the top, ripped. |
| O2 | 8-bit power-up | An old pixel side-scroller. A little pixel dude runs, grabs a glowing six-pack icon like a power-up, instantly has pixel abs and flexes. START = running toward the icon. END = flexing with pixel abs. |
| O3 | Arcade combo | A guy at an arcade machine slams in a button combo, the machine lights up like a jackpot, he steps back, lifts his shirt and finds abs, the guys behind him lose it. START = hands on the buttons, machine dim. END = shirt lifted, abs, machine lit, friends reacting. |

Rules that bind the frames: men shown whole, never a shot built around a stomach, no hands grabbing a belly; ordinary
non-model faces (ad-edit Step 4.5 prompt rules); the subject in the centre third; no generated lettering (any slider
label, score or "cheat" text is drawn by us in code afterwards); a cut, not a morph, where the idea is a time jump (O3
may be two shots); the AI-GENERATED chip on the delivered clip, clear of faces. For each pair on the page, as labelled
rows: when it appears, the line it plays under (bold, word for word), what comes right after, what you see, the
intended action and length, the cost to animate, and what plays if he says no. Under the frames answer the three sense
questions (cause and effect, readable with the sound off, shows the line).
Budget: $10 for this ad in total across all rounds, retries included. Spent so far: $0. Frames cost nothing.
Before the page: run `.claude/skills/_shared/framecheck/gate.py` on each pair, then a fresh `frame-reviewer` agent per pair
(and per retry). Review pages refuse AI frames without both (added 2026-10-16).

### B. Framing options

Round 1 sizes on this roll: close 504x896, wide 612x1088 (source px, exact 9:16 lattice w=18m h=32m; y0 = the hold's
minimum hair top minus 4 % of the crop height). Show two or three wider PAIRS as numbered stills on the same two
moments (one close, one wide) with their crop values, for example close 540x960 / wide 666x1184, close 576x1024 / wide
720x1280, close 612x1088 / wide 756x1344. Keep the wide at least 1.10x the close and the hair rule unchanged. Wider is
also sharper (round 1's close was a 2.14x enlargement). Recommend one pair; he picks. This is his call for this roll
and is wider than the written framing standard; record his pick with his words.

### C. Colour options (the bake-off in PRE-RENDER-APPROVAL, steps 2 and 4)

At least three candidates on the same two moments (wide and close), LOOKED AT at full size beside frames from two
approved videos (RA-01's master, the approved Ad 1 vertical; the website video for a third reference), with what is
wrong with each written down. Then the best two as moving 10 to 15 s samples of the opening. What I saw in round 1's
grade (`grade.json`, RA-01's LUT at 1.15 exposure + saturation 1.25): skin reads orange-brown, shadows and the trees
are heavy, the picture is flat for an outdoor pool. RA-01's "no white balance change" was a planner's ruling, not
Dan's; a candidate with a daylight white-balance correction is allowed and expected (ad-edit RA-01 lesson 3: build a
daylight LUT rather than lifting saturation). Tools: `/Volumes/Extreme/_edit_work/ra01/s32_grade.py` (face luma and
chroma against references), `/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e*.cube`. Decode as BT.709.

### D. The opening without the AI picture

Remove card G1 from `s60_plan.py` (`CARDS`) and re-plan the holds so a size change still lands every few seconds:
opener clip 0 to 3.64, close on "It's AI. I'm not talking about an AI picture.", wide on "I'm talking about getting
real abs in real life with AI.", close on "Here's how it works." Re-render the opening sample with the recommended
framing and colour; where the opener clip will go, show the recommended START and END frames as a labelled
placeholder (VIDEO-RULES "Future contextual previews"). The goal picture still appears later as the result of the
step one demo; say so in "What I decided" so he can overrule it.

### E. Ask again (unanswered from round 1)

Analysis card: redraw in Soft Blue Light (recommended) or keep the RA-01 card. Voice: `mix.wav` (recommended) or
`mix_bass.wav`. Recap list card R1: keep (recommended) or none.

Then record his answers, write the round 3 handoff (opener motion from approved frames, moving previews of every
graphic and clip, the finished first 30 seconds) and stop.

## Locked from round 1 (work dir `/Volumes/Extreme/_edit_work/ra14/`, sha256 first 16; re-hash before touching)

| file | what | hash |
|---|---|---|
| `cut.json` | take map and airtight cut: 48.81 s of talk, 4 take seams (10.57, 30.30, 33.43, 46.46 s) | 394e9127a580ce5c |
| `mix.wav` | voice chain (fitted tone, no dereverb) + Realizer bed at -32; audio gate PASS 12 of 12 | fe821bf0b0c5c108 |
| `mix_bass.wav` | the same with +3 dB at 120 Hz | a969e60b871ecd8d |
| `words_aligned.json` | 168 words, CTC aligned to `mix.wav` | b01781a5203792fb |
| `framing.json` | head and hair track, 241 samples | d798e48e215d593a |

Dan did not object to the cut, the takes, the captions, the graphics family or the other eight items; none of those is
approved in words either, so they stay as shown, not locked. `beats.json` and `grade.json` change this round.
Total length 50.45 s, no line cut. Roll `C1667.MP4`, native portrait, dual-mono lav.

## Carried work (decided, not questions)

- Add one head measurement on the exact first frame of each hold (`s04_track.py`), then `s60_plan.py`; the crop
  landed 5 to 20 source px off in round 1 because the head is sampled 5 times a second.
- Five pause splices sit inside a hold (11.38, 19.72, 31.13, 41.38, 42.64 s): measure on rendered picture and give each
  visible one a size change or cover.
- Captions lift above the recap card; `s07_captions.py` needs a per-state y.
- The phone demos need a renderer (`s63_stills.py` `phone_card` has the shell and placement).
- Music tail fix (`s42_bed.py`) and frame-lock of the mix once the length is final.
- 16:9 not started. At delivery: edit sheet, delivery gate, watch pass, one independent review, review copies, audio
  A/B, `Videos to Review/`, `roll_sidecar.py mark-used`, clip library `used-in`, queue to `delivered`.

## Recipe and machine

Scripts: `/Volumes/Extreme/_edit_work/ra14/` and `.claude/skills/ad-edit/reference/ra14/` (`s60_plan.py`, `s62_sample.py`,
`s63_stills.py`, `s64_page.py`, `s07_captions.py`). `s62_sample.py` decodes the roll from frame 0 (about 6.5 minutes per
run): render all colour and framing candidates' strips in ONE decode. The Mac was saturated on 10-13; use
`./capwait.sh`, and note it also counts idle gate processes.

## Gate status

Audio gate on `mix.wav`: PASS. Nothing else has run; there is no finished file.

## ROUND 2 BUILT 2026-10-13: waiting for Dan's six picks (page http://127.0.0.1:8815/)

Everything above this line is the brief round 2 was built from. State now:

- **Page:** `/Volumes/Extreme/_edit_work/ra14/round2/index.html` (generator `s74_page.py`, text in `round2/notes_r2.json`). Six
  decisions: opener idea, framing pair, colour, and the three round 1 questions asked again. None is answered.
- **Opener frames (Codex subscription, 6 images, $0):** clean frames for a motion model in `round2/frames/O1..O3-start/end.png`;
  as-played stills (our slider, counter, AI-GENERATED chip, caption) in `round2/stills/`. Prompts: `round2/opener/prompts/`.
  All lettering is drawn in code (`s71_opener_frames.py`). Recommended: O1 Character creator. **No motion is authorized.**
- **Framing:** pairs F1 540x960 / 666x1184, F2 576x1024 / 720x1280 (recommended, written to `framing_choice.json` so the
  sample could be built; NOT his pick yet), F3 612x1088 / 756x1344. `ra01lib.Aspect` reads `framing_choice.json`.
- **Colour:** three baked 65-point LUTs in `round2/colour/luts/` (`bake.py`, numbers in `looks.json`): C1 RA-01 level, C2
  brighter with golden skin (recommended), C3 brighter with a cooler background. `grade.json` is still round 1's; write the
  pick into it. The head track was measured on round 1's grade and does not need re-measuring for a new grade.
- **Opening re-planned (`s60_plan.py`, `beats.json`; round 1's are `round1/beats_r1.json`, `round1/s60_plan_r1.py`):** G1 is
  out. O0 is the pending opener slot 0 to 3.64 s. The 4.44 s pause splice is a visible jump once G1 is gone, so the holds
  are close "It's AI." / wide "I'm not talking about an AI picture." / close "real abs in real life" / wide "Here's how it
  works." / close from the R1|R2 seam (10.58 s) with L1. This differs from section D above on purpose. After the P1 card the
  levels are round 1's. `beats_camopen.json` is the same plan with the camera scene as the opening (`OPENER=0`).
- **Head track:** `framing_holdstart.json` adds a measurement on the first and last frame of every hold (`s04b_holdstart.py`);
  landing error is now 0 px. `framing.json` (locked) is untouched.
- **Samples (10.58 s, under 45 s, so not copied to `Videos to Review/`):** four files in `round2/`, built by `s72_sample.py`
  with an input seek instead of a decode from frame 0.
- **Not done, still carried:** measure the other inside-hold splices (11.38, 19.72, 31.13, 41.38, 42.64 s); L1 on the close
  shot needs its still re-checked for face clearance; captions above the recap card; the phone demo renderer; music tail;
  16:9. Captions (`cap_9x16`) were not rebuilt: the opening's word timing did not change.
- **Spend:** $0 of $10.

### Round 2 files (sha256, first 16; none is approved yet)

| file (under `/Volumes/Extreme/_edit_work/ra14/`) | hash |
|---|---|
| `round2/frames/O1-end.png` | 30cf35f7ea6426a4 |
| `round2/frames/O1-start.png` | 10d42e5204184026 |
| `round2/frames/O2-end.png` | da3f482f899b023c |
| `round2/frames/O2-start.png` | 44323801cacdf80d |
| `round2/frames/O3-end.png` | d79b372b206cacc3 |
| `round2/frames/O3-start.png` | 81c3cffaa87ff159 |
| `round2/colour/luts/ra14_C1_approved_level.cube` | 29c01696a71e84b8 |
| `round2/colour/luts/ra14_C2_brighter_gold.cube` | 4e222c22be62cdfd |
| `round2/colour/luts/ra14_C3_brighter_cool.cube` | c03902f7a2da83f5 |
| `round2/RA-14 round 2 - opening - RA-01 level colour - opener placeholder.mp4` | 6172af0faa1a704a |
| `round2/RA-14 round 2 - opening - brighter gold colour - camera opening.mp4` | f47417c60749d242 |
| `round2/RA-14 round 2 - opening - brighter gold colour - opener placeholder - more bass.mp4` | dc6a32c2f5914e67 |
| `round2/RA-14 round 2 - opening - brighter gold colour - opener placeholder.mp4` | 39b2d1ceb974232d |
| `beats.json` | a837a254683b5992 |
| `beats_camopen.json` | 025e117b265aa3f9 |
| `framing_holdstart.json` | 0e526c3efea8af97 |
| `framing_choice.json` | fbea024afe893fc8 |

### Next action (round 3)

Record Dan's reply in `/Volumes/Extreme/_edit_work/ra14/round3-plan/decisions.json` (his words, per item, with hashes of the
approved frames), write his framing and colour picks into `framing_choice.json` and `grade.json`, re-run `s04b_holdstart.py`
and `s60_plan.py`, then: opener motion from the approved frames only, moving previews of every graphic and clip, the
finished first 30 seconds. Stop for his review.

### Starter prompt for round 3 (Claude Opus 5.5, high effort)

> AD. Rename this task `Cheat Code Six Pack AD R3`. Read `Handoffs/handoff-20261013-ra14-cheat-code-round2-after-dan-review.md` (the ROUND 2 BUILT section) and run round 3 of RA-14 "The Cheat Code For Six Pack Abs" with /ad-edit. My round 2 picks: [paste the reply box from http://127.0.0.1:8815/]. Make the opener motion from the frames I approved, show me every graphic and clip moving in context, then the finished first 30 seconds. One review page, then stop.

## Original round 2 starter prompt (already run)

> AD. Rename this task `Cheat Code Six Pack AD R2`. Read `Handoffs/handoff-20261013-ra14-cheat-code-round2-after-dan-review.md` and run round 2 of RA-14 "The Cheat Code For Six Pack Abs" with /ad-edit. Use the Codex subscription to generate the images. Make start and end frames for the three opener ideas I picked (Character creator, 8-bit power-up, Arcade combo), show me two or three wider framing pairs and at least three colour correction options beside approved videos, take the AI picture at 5 seconds out, and re-ask the three round 1 questions I have not answered. One review page, then stop for my picks. No motion until I approve frames.
