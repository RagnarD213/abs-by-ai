**SFC.** Task name: `Fat 90 Year Old SFC R6`. Recommended: Claude Opus 5.5, high effort (this video started on Claude).

# DS-40 R6: "Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right." Graphics round, then the full Short

Written 2026-10-22 by the R1-R5 task (Claude). Read `.claude/skills/_shared/VIDEO-RULES.md` (in full, as AGENTS.md requires),
`Handoffs/video-editing/00-RULES.md`, and `.claude/skills/shorts/reference/ds40-greenscreen/README.md` (the whole recipe and
every lesson so far) before starting.

## Locked by Dan (do not reopen)
- **Key:** the house chroma key standard (R2), `.claude/skills/_shared/chroma-key/README.md`. Dan 10-21: "Let's make all our
  future chroma keys this clean and make this a standard."
- **Colour B Warm Vivid** (`grade.py LOOKS['B_warmvivid']`). **Voice E:** house fitted chain plus `equalizer=f=120:t=q:w=0.8:g=+1.5`
  (`/Volumes/Extreme/_edit_work/ds40/r1/audio/a30/E_bass15.wav.voice_chain.json`).
- **Opening = R4 version B, now the format for ALL green screen reactions** (Dan 10-22: "Let's go with B. Let's lock this as our
  format, this size, and the laptop visible"; rule in VIDEO-RULES "Green screen reaction opening"). The Maher clip full screen
  (fixed vertical crop, centre x 620 of the 1280x720 source), Dan keyed small lower left at 0.40, flush left and bottom, laptop
  visible, his real reaction (roll C1730 1354.70 s + 3 frames = clip 4.40 s). Code: `ds40-greenscreen/comp_r4.py` (version B)
  on top of `comp_opening_r3.py`. Reviewed SHIP: `/Volumes/Expansion/_edit_work/ds40/r4/audit/R4-REVIEW.md`. Known minor item to
  fix when re-rendering B: the watch face is faintly see-through on some frames (run the watch hold-out boxes on this segment).
- **Clip:** `/Volumes/Extreme/_edit_work/ds40/r1/src/maher_yfiWjnStE3w_210-238.mp4`, in 4.40 s, out 23.78 s ("Let me ask you
  this" ... "an unchallenged lie"; "that" starts 24.36). Clip audio prep in `/Volumes/Expansion/_edit_work/ds40/r3/audio/`
  (+8.3 dB, limiter 0.80, 8 ms in / 50 ms out fades); the whole opening sat at -14.0 LUFS, -1.8 dBTP.
- **After the clip:** Dan grows to full size (R3's 0.5 s move: the clip shrinks into the card at the top, `CARD = (60,36,1020,576)`,
  Dan grows; 3-frame dissolve from the watching take to the scripted take while still small; 25 ms fade-in on his voice) into the
  R2 layout (moving Soft Blue field, clip card at the top, large Dan, OY 175, crop at source row 3490). Adapt the move's start to
  B (0.40, flush left/bottom). **Dan 10-22: "I want it to keep playing behind me silently, like other random clips from that Bill
  Maher interview."** The card keeps playing SILENT footage from other moments of the same episode (YouTube `yfiWjnStE3w`,
  "New Rule: Fat Acceptance"); never 2:15 to 2:33 again (a reaction never repeats its clip). Download more of the episode
  (standing download authorization; yt-dlp: `~/.cache/absbyai/ytdlp/yt-dlp_macos --js-runtimes node`, 720p max).

## The rest of the Short (from the shoot doc `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`, section "SCRIPT: Bill Maher Asks...")
Scripted take: ONE continuous take on roll C1730, 1400.25 to 1448.62 s (word times in the roll's `C1730.roll/words.json`), no
retakes. 48.4 s + 19.4 s clip + move = about 68 s, over the 66 s ceiling. **Plan:** cut two ad-libs that fall under the
full-screen BMI graphic (no visible cut): "So look at your weight, look at your height and then see if you're overweight or
obese." and "Most people in America are in the overweight category." -> about 62 s (the script's own estimate). Smooth the
audio joins (memory `audio-joins-smooth-before-ship`). Only the first 9.3 s (1400.25 to 1409.55) are keyed so far (R2 cache
`/Volumes/Expansion/_edit_work/ds40/r2/cache_r2`, crop row 3490); key the rest of the take with the same method.

Graphics (all Soft Blue Light, real HyperFrames motion for their whole time on screen; `_shared/hyperframes/`):
1. Lower third during the clip: "BILL MAHER, REAL TIME (HBO)" (check it never covers Maher's face or small Dan).
2. On-screen text at "That's why you need to treat your belly fat as an emergency": "TREAT YOUR BELLY FAT AS AN EMERGENCY".
3. Full-screen BMI table: height down the side, weight across the top, Normal / Overweight / Obese bands in different colours;
   held for "Here's a BMI table..." through "...the most important thing you can do." No table template exists: build one in
   `_shared/hyperframes/` (moving field, rows or bands landing on the words that name them). Use correct BMI maths (show the
   band boundaries 25 and 30; label the units). Believable-claims rule applies to on-screen text only.
4. "SUBSCRIBE" at "Subscribe to my channel...".
Plus J2 burned captions (shorts rules), no AbsByAI.com end mark.

## Round method
Round 1 for graphics on this video: show every graphic moving, in its real context, plus the edit plan (what is cut, timings,
which silent Maher moments play in the card) on the review page BEFORE the full render. Then the full Short: delivery gate,
independent reviewer (fresh agent, files only, every frame, light lane), review page on port 8940 (replace the R4 page with
`review_server.py 8940 --remove` then serve the new folder). Work in `/Volumes/Expansion/_edit_work/ds40/r6/` (Extreme is nearly
full). Run `python3 .claude/skills/_shared/editcap/editcap.py acquire DS-40` before any render; `release DS-40 --review` when
waiting on Dan. Codex's separate DS-40 build (`/Volumes/Extreme/_edit_work/DS-40-codex/`) is not yours: do not touch it.

## Traps already paid for (details in the recipe README)
- A seek's first decoded frame repeats the next one: never trust frame 0 of a resumed decode; seek a few frames early.
- Rawvideo decodes for measurement are filed as heavy by the render queue: run analysis with `renderq.py run --light`.
- Background jobs of a sub-agent die when it goes idle: tell reviewers to run in the foreground.
- `place()` in `comp_opening_r3.py` now clips to the canvas it draws on (a box or the full screen).

## Starter prompt
> Fat 90 Year Old SFC R6. Read `Handoffs/handoff-20261022-ds40-r6-graphics-and-full-short.md` and execute it: build the four
> graphics (lower third, "treat your belly fat as an emergency", the full-screen BMI table, subscribe) in Soft Blue HyperFrames
> motion, the edit plan for the rest of the Short with the silent Maher footage in the card, show them for approval on port 8940,
> then build the full Short in the locked B format with captions, independent review, delivery.
