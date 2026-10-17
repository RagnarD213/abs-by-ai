# RA-12 "The First Step To Getting Abs Isn't A Workout": round 2, prospect before/after, new opening clips, graphics under the captions

**AD (short-form, filmed).** Sidebar name: `First Step Abs AD R2`.
Written 2026-10-17 (Claude Opus 5.5) from Dan's round 1 answers. Replaces `handoff-20261015-ra12-round2-after-dan-review.md` (written
before his answers). Job doc: `Handoffs/video-editing/RA-12-first-step-to-getting-abs-isnt-a-workout.md`.
Read first: `.claude/skills/_shared/VIDEO-RULES.md` (the 2026-10-16/17 sections at the top), `_shared/PRE-RENDER-APPROVAL.md`, `/ad-edit`
(RA-12 and RA-04 sections), `.claude/skills/ad-edit/reference/ra12/README.md` (stage order, eleven lessons), and RA-04 round 5's
prospect assets in `.claude/skills/ad-edit/reference/ra04/round5/` (`decisions.json`, `before_white_man.prompt.txt`, `lock_src.spec.json`).

## Dan's words (2026-10-17, verbatim in `/Volumes/Expansion/_edit_work/ra12/round2-plan/decisions.json`)

> Throughout the ad, I want to switch this to using one of the AI-generated after pictures and generation clips that we've made of the
> prospect. Use one of the white guys that we made instead of me for the generation, for the after picture initially shown, and for the
> generation clip throughout the video. Use it for everything. I'm realizing now that using my own picture makes it seem like I don't
> really have abs and that my abs are AI-generated.
>
> I want you to move the bottom graphics to immediately below the subtitles on my shorts, just right below the subtitles, so they don't
> block my abs.
>
> For the initial clips, I want a clip of me working out, looking ripped, from our B-roll library. Use that ab wheel rollout, or whatever
> clip you can find with me looking the most ripped.
>
> For the second clip, use a B-roll clip of me eating the salad, or showing the salad, or holding the salad. If you can't find a good one
> that fits in this frame, then use an AI-generated clip that we've already made of me eating the salad.

## State

* Round 1: the whole 9:16, 46.25 s, page http://127.0.0.1:8842/, filed in `Claude Ad Videos/the first step to getting abs isnt a workout - RA-12/round 1 review/`
  (notes.md, three review files). Work dir `/Volumes/Expansion/_edit_work/ra12/` (Seagate; Extreme is full). Independent review 3: SHIP.
* Everything else in round 1 is untouched by his notes: the cut (`cut.json`), voice (`mix_fit_b1.5.wav` -> `mix_bass_r1.wav`), framing,
  captions, A1's design, T1, Q1 (A0172). Opener: he kept the montage idea (no AI opener).
* Spend: about $0.02; AI budget $0 of $10.

## Changes for round 2 (one new `round2/` folder; never overwrite `round1/`)

1. **The prospect replaces Dan's picture everywhere** (same person in every picture):
   * P1: B0550 `03 B-Roll - Real Footage/screen-recordings/B0550_app-generate-goal-image-heavier-white-man-lake-dock_1320x2868_42s.mp4`
     (real absbyai.com generation; loader about 0.6-35 s, crop x50 y715 1220x1432; result settled from 36.2 s, crop x0 y560 1320x1550),
     in the approved phone shell. His before photo is AI-generated: label AI-GENERATED, never "Real picture of me". Drop the
     `P1_real_photo` span from the gate plan.
   * G1 ("It's a picture."), K1 ("look at it every day") and A1 (analysis card photo): his AI goal picture (the result frame, or RA-04
     round 5's source still; find it in `ra04/round5/`). K1: library A0180 (`04 AI-Generated Clips/concepts-and-gags/A0180_phone-lockscreen-ai-goal-white-man-lake-dock_9x16_3s.mp4`,
     3.25 s, passed clipcheck and review) or the round 1 K1 code card with his picture; A0180 needs the motion check again only if trimmed oddly.
   * Words to watch: "you can generate a picture of yourself" now shows the prospect, which fits; nothing on screen may say it is Dan.
2. **Graphics under the captions.** C1, L1 and C2 move to sit immediately below the caption line (captions ink y about 1408-1495), over
   his shorts, never on his abs. Measure his waistband per hold with the person mask (FAR holds show shorts below about y 1430; NEAR holds
   end near his navel, so a hold carrying a graphic may need FAR). Keep 24 px clear of the caption ink. Check what YouTube's own
   Shorts overlay covers at the bottom before settling the y. These are revised graphics: full Soft Blue HyperFrames motion for their
   whole screen time (VIDEO-RULES 2026-10-17). `vertical.py` `cta_scenes`/`lt_scenes` place them at 68 % of the height; add a y option
   to the shared template rather than shifting renders by hand, and push that shared change at once.
3. **W1 ("isn't a workout"):** Dan's own ab wheel B-roll where he looks most ripped, starting on the rep: B0030, B0427, B0436 (library),
   or better takes on the pool rolls (`clip_library.py find "ab wheel" --rolls`). Colour-correct to the film. Fill the frame where the
   rep survives a 9:16 crop; else the widest card that keeps the full height.
4. **D1 ("and it's not a diet"):** Dan eating, showing or holding the salad. Library B0441, B0525, B0526 show containers and hands, not
   him eating; search the salad shoot rolls (RO-05 / SL-03 sources, `--rolls`) for him eating or holding the bowl. Only if none fits the
   frame: an existing AI clip of Dan eating the salad (none found in the library by "salad"; search wider before concluding).
   Never generate a new one without Dan's frame approval.
5. Plan text and page: update `beats.json` descriptions, the page items and "What I decided"; show only what changed (later-round rule)
   with exact new-film timestamps and short watch ranges for each change.

## Then

Rebuild from the plan step (`chain_c2.sh` pattern; `s08_audio.py` must stay the length-preserving version), `gate_seq.sh`, the watch pass
and a FRESH judge, `gate.py --format ad9x16`, a fresh `ra-reviewer`. Known gate items: the tone row (bass lift, by design); the label-row
sampling bug on spans under 0.9 s (a separate session is fixing the gate; re-run the gate if it lands). Update page 8842 or a new port,
the VLC copy (`Videos to Review/First Step Abs AD R2 - whole ad 9x16.mp4`; delete the R1 copy), the queue (`delivered`), the board entry.
If Dan approves the 9:16 next, build the 16:9 from the same edit (ra12 README lessons; RA-15 lesson 18).

## Model

Claude Opus 5.5, high effort.

## Starter prompt

> AD. Rename this task `First Step Abs AD R2`. Read `Handoffs/handoff-20261017-ra12-round2-prospect-and-graphics.md` and build round 2 of RA-12 "The First Step To Getting Abs Isn't A Workout" with /ad-edit: swap my picture for the AI prospect everywhere (generation demo, the after picture, lock screen, analysis card), move the buttons and the KEY POINT to just under the captions, use my ripped ab wheel B-roll and a clip of me with the salad for the two opening clips. Rebuild, run the watch judge, delivery gate and an independent review, fix what they find, and stop for my review with timestamps for each change.
