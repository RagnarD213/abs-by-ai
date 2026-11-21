# RO-18 "How To Make Time For Exercise & Nutrition" (9/23 C1714 + C1715): round 1 recipe (Claude Opus 5.5, 2026-10-15)

Two talk rolls on the 9/23 studio set (7:36 + 10:41 raw), cut to 10:45. Starts from RO-14's round 1 recipe (`../ro14/`, which sits on
`../ro17/`); only the files that differ or are new are kept here. Work dir: `/Volumes/Extreme/_edit_work/RO-18/round1/`. Review page
port: see the round's handoff. Never commit media.

## What is new here
- **Two rolls on ONE virtual source timeline.** `lav.wav` is C1714's lav, digital silence up to frame 13800 (460.46 s, a whole
  number of frames and of samples: 13800 x 1601.6), then C1715's lav. Every recipe script keeps working in virtual time;
  `frames.roll_of(f)` / `frames.roll_t(t)` map a virtual frame or second to (roll path, local time) for `frame_src`,
  `build.render_seg` and `hair_pre`. A piece never spans the gap. One medium.en pass and one Gemini listen cover both rolls.
- **Room tone per roll** in `build.py` (C1714 286.75-289.0, C1715 virtual 944.3-947.3, both measured steady and click-free); the
  RO-14 timestamp landed on speech here.
- **gfx scenes:** `tiles` (six pictures, 3 x 2, each rising on its word via `reveal_items`), `dictate` (what you say, the fillers
  struck out, what it types; rows on `reveal` words), `split` (one bar in two parts). `resolve.py` resolves a plain `reveal` list
  to `reveal_t` too.

## Traps this round paid for
1. **The job doc said the camera was nudged left at the start of C1715. It was not:** the light tube and bulb measure 0 px apart
   (phase correlation on background strips); "move it a little to the left" was the prompter. Measure before matching framing.
2. **The Extreme drive was full (5 GB free).** `stock/`, `cache/`, `review/`, `hf/` and `assets/*` are links to the same paths on
   `/Volumes/Expansion/_edit_work/RO-18/round1/` (21 TB free). Make the links before the first download or render.
3. **`px_recv.py` writes one fixed file:** a second gather (photos after videos) overwrote the video index. Rename the file
   between gathers. Run Pexels `fetch` loops with `Promise.all` in batches of about 15 terms; a sequential loop of 30 timed out.
4. **Word map after `patch_words.py`:** besides the dropped first word of every region (RO-14), three more faults: a region edge
   that duplicates a word ("phone phone"), and words of the ABANDONED take kept at a piece's tail because Whisper started them
   early and they overlap the piece by 0.08 s ("For For", "Think Think", "A A car"). Check the level strip, then drop those
   words by hand. Print the film-time sentences (`out_sentences.txt`) and read them once before planning.
5. **Do not split one continuous read into two pieces for the notes:** w1f/w1g were contiguous and the split's snapped in-point
   clipped "It gets". Merge contiguous reads; check every snapped in-point against the strip (the "Number three" start was
   0.24 s late on a low-confidence Whisper word).
6. **`gfx.scene` had an RO-11 special case keyed on the item id "G16"** (fat vs lean bars). A new G16 card rendered those bars.
   Removed. Never key a drawing branch on an item id.
7. **AI frames: 9 ideas, 6 passed, 3 dropped after three tries each.** What failed review, so it can be designed out next time:
   - Walking toward the camera (legs grow, the background behind him gets redrawn: a door became glass). Prefer actions that
     keep the person in place: a head turn, a lean, sitting up.
   - Codex edits redraw hair, headbands and gloves: curly hair and a patterned sweatband on all three tries of one pair, a
     six-fingered then a three-fingered glove. Say "keep his hair exactly as it is" and count fingers yourself before review.
   - `lockstill.py` boxes that cut across a surface the person touches leave a hard-edged block (a dark rectangle on the yoga
     mat at the box edge). Use a mask instead: the body (pose segmentation grown about 30 px, which keeps the contact shadow)
     plus the moving object's own outline (here the white bedding by brightness and saturation), everything else from START.
   - `lockstill.py` also restores START props that should have gone: the tip of a pen she had been holding, left floating. Inspect
     the whole area a hand or prop vacated.
   - Gate `still` boxes on a plain surface slide (a laptop lid, a desk top): the gate then reports a 120 px "move" that is not real.
     Put still boxes on corners or texture, and declare what the person's feet or arms hid in START as revealed.
   - A box that is too tight for the person's own movement (a head that drops forward past it) flags the uncovered background;
     size the person's box for both poses.
8. **Headless Chrome screenshots of a page anchor (`#all`) with lazy images come out blank.** The top of the page works.

9. **`build.render_range` wrote one shared `tmp_base.mp4`.** Two renders at once (a first-minute render started by hand during
   `context_all`) truncated each other ("AssertionError: 899" in the decoder loop). The base is now `out + ".base.mp4"`.
10. **A full disk fails silently:** the Extreme drive reached 0 bytes mid-chain; the first-minute step left an EMPTY log (it could
    not even write the traceback) and the chain echoed "FIRST done". If a step's log is empty, run `df -h` first. The whole work
    folder now lives on Expansion with `/Volumes/Extreme/_edit_work/RO-18` a link to it.
11. **`/private/tmp/claude-501` is shared by every session:** a contact sheet written as `fm_sheet.jpg` there picked up another
    session's frames with the same names. Scratch files go in the session's own scratchpad.
12. **A vertical library clip in a 16:9 slot is centre-cropped:** A0089 (the dating-app clip) became a shirtless man's belly. Check
    the aspect of every library clip before planning it into a full-frame slot.

13. **Room tone that starts on a click ticks at every join.** The first C1714 window (285.5) began on a small click; the reviewer heard
    it at every C1714 piece edge. Listen to the chosen window on its own (and look at its peak) before using it.
14. **A full-screen clip and a phone card that overlap wrap the picture.** `build.py` took one "current clip" for both; the app-tour
    phone card at the close overlapped the last full-screen clip and the frame came out the wrong size. `resolve.py` now starts the
    second one where the first ends, and `build.py` keeps one reader per item and asserts every frame is 1920 x 1080 RGB.
15. **An independent check before Dan sees the page pays for itself:** 17 fix-level findings in round 1 (wording meant for Dan inside a
    graphic, rows that appeared before their word, lower thirds under 3 s, a stock clip that did not show the line, repeated stock
    scenes, two dark clips). Brief the reviewer on the plan and rules only; `review/REVIEWER-BRIEF.md` is the template.

16. **A screen recording that kept its own iPhone status bar shows two clocks and two islands in the phone card.** B0035 (660 x 1434)
    has the recording's bar and red dot over scrolling content; the shell draws its own 9:41 bar. Phone items now take
    `crop_top` (px in the source; B0035 needs 92) in `build.ClipReader` and `stills.py`. Look at the top 100 px of every library
    recording before planning it into a phone card; B0544 is already clean.
17. **A study-card value label can run past the card:** bars were scaled to a fixed width, so "about 150 words a minute" ended 33 px
    outside the border. `gfx.study_card` now shrinks the bars so the longest label fits, and shows the detail line on its own word
    (one more `reveal` than bars) or 0.6 s after the last row, never 1.6 s after the card opens.
18. **A second, narrower independent re-check after the fixes found two more fix-level problems** (17 and 18 above). Budget one.

## Files
`frames.py` (two rolls), `build.py` (roll_of, room tone per roll), `edl.py`, `plan.py`, `gfx.py` (tiles, dictate, split; the G16 case
removed), `resolve.py`, `page.py`, `page_extra.py`, `titles.py`, `hair_pre.py`, `patch_words.py`, `grid.py` (the 3 x 3 grid of this film's own graphics for P02), `chain_r1.sh`,
`chain_r1b.sh` (stills to page), `chain_r1d.sh` (re-render only the blocks holding changed items). AI frame prompts and
specs: `ai-frame-prompts/`, `frame-specs/`.

## Round 2 (2026-10-20): Flow motion, what the reviewers caught, and fixes that worked
19. **An END frame whose object looks different drags Veo into a morph.** A7's approved END showed the laptop closed and silver; the
    START lid was dark bronze. All four START+END takes turned the lid silver and grew an Apple logo as it closed (reviewers caught
    a faint logo-shaped square the clip gate cannot see). START-only takes (`veo.py add` without `--end`) kept the bronze lid; 1 of 6
    had no logo at all. When the END frame changes an object's look, try START-only before repairing pixels.
20. **Repairs that failed review:** a chroma-keyed tint hold (`lidtint.py`) also greyed her hands and face (skin and a copper lid
    share chroma); a geometric lid mask (`lidtint2.py`) left blocky patches. Inpainting a small mark (`lidpatch.py`, `dotfill2.py` with a
    hand-read track) was clean.
21. **Flow takes drift 10 to 21 px although the prompt says static.** `recipe/stablock2.py TAKE SPEC OUT N [zoom] homog` matches every
    frame to frame 0 (SIFT on the background outside `may_change`, RANSAC) and passes the gate; the chained LK version
    (`stablock.py`) drifted 36 px on an 8 s take. A real dolly-in (parallax between desk and blackboard) cannot be removed in 2D: retake.
22. **A pen set down by a Veo hand changed ends in all four takes** (twirl, the tip melts and regrows). The fix was editorial: a wide shot
    of the writing, a cut to a 1.33x closer shot that starts with the pen already down (A8, two takes).
23. **Give a slow AI action room instead of speeding it:** A7 needed 4.4 s; starting it on the previous line's last words ("do all of
    your homework") made the gasp a reaction to that line and cost C36 1.2 s.
24. **Approved assets on Extreme get cleaned:** `ro06/round5/phone/P01-softblue.mp4` (the self-generation demo) was gone; its exact frames
    came back from round 1's 1080p render block. Copy every borrowed asset into the job's own `assets/` when a round first uses it.
25. **zsh: `rm -f x*` with no match aborts an `&&` chain** (the first master render never started). Use `setopt null_glob` or no glob.

## Round 4 lessons (2026-10-25)

26. **A demo's wait never plays as silence.** The longform gate bounds inner silence at 2.0 s (`junk:dead_air`) and fails any second
    under -50 dBFS (`audio:stream_integrity`); the voice chain's expander pulls room tone down about 9 dB, so even a room bed reads silent.
    A screen recording's processing wait (Wispr Flow: 2.5 s after the voice) goes UNDER the next line: cut the phone to its result as the
    speaker finishes and hold the picture over the next line (`hold_over` in resolve.py, an L-cut of picture). Round 4 v1 failed both rows.
27. **Inserting new speech into a finished film:** add the roll to the virtual timeline (frames.ROLLS + lav.wav at an offset), splice ONE
    shot after the anchor shot and shift every later out_f (r4_insert.py), shift words_out and the HyperFrames manifest by the same frames
    (r4_hf_shift.py asserts each graphic keeps its old offset from its item), then prove it with a shifted frame diff (framediff_r4.py).
    Approved framings stay put because shot ids, CROP_Y and the DP's covered joins are unchanged; compare against the last approved build.json.
28. **A portrait roll in a 16:9 film:** give it its own framing (P: a 3:4 window of the autorotated frame placed in a panel) and paint the
    scene from a per-item reader (build.SplitReader), not from the base frame, so the panel can run past its shot.
29. **Sync a screen recording to the camera by the UI, not by ear:** the waveform bars' white-pixel activity (20 fps) against the lav level;
    match the longest dip to the longest voice gap and the bars' stop to the voice's end (RO-18: recording = C1719 - 94.8 s).
30. **The shared ffmpeg in Media/video_edit/bin queues in renderq:** a light measurement can wait 20+ minutes on a loaded machine; start it
    in the background, never assume it hung.
