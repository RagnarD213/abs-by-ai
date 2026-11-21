# Handoff: SL-05 Stop Deadlifting shorts, round 1 review packet (2026-09-30)

## Goal
Build ONE review page for Dan covering all five picked shorts: the look (first 10 seconds of Short 1: colour and audio)
and the intro title graphic for each short, plus a "What I decided" list. **Do not render any full short in this round.**
Dan's words (2026-09-30): *"Let's use the Codex method of extensive approvals in the first round for graphics and the
intro. Let's just approve the first 10 seconds for color correction and audio, and the intro graphic... just not make it
as extensive as a VSL. Just make it a little less time-consuming and more appropriate for less important organic content."*
Then he picked: *"I like all five."*

Read first, in this order: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`,
`Handoffs/video-editing/SL-05-stop-deadlifting-shorts.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md` (the review page
section and the organic decision budget), `.claude/skills/shorts/SKILL.md`, and
`.claude/skills/shorts/reference/zeeshan-master/README.md` (the SL-04 pipeline for Zeeshan masters, all three rounds).

## Source and work folder
- Source: `Zeeshan Content Videos/stop deadlifting - video 3/stop deadlifting | zeeshan | 16x9 | video 3.mp4`, Video 3
  Rev 5, MD5 `e98bbb9bace1085df31950e9e51fd326` (re-check before starting), 1920x1080, **29.97 fps**, AAC stereo 48 kHz,
  556.5 s. Parent goes public Sun Oct 11; nothing uploads or queues in this job.
- Work folder: `/Volumes/Extreme/_edit_work/sl05/`. Already there: `words.json` (Replicate incredibly-fast-whisper, word
  timestamps, 1,962 words), `transcript.txt` (sentence view), `master16k.mp3`, `PROPOSAL.md`, `sheet1.jpg`/`sheet2.jpg`
  (6 s contact sheets), `tops.png` (hair-headroom evidence). Build in `sl05/build/`, copied fresh from
  `.claude/skills/shorts/reference/zeeshan-master/`. **Never run anything inside `/Volumes/Extreme/_edit_work/sl04/`**:
  another session is re-cutting SL-04 short 1 there.
- Queue: SL-05 is `in_progress` (Claude). Board: one line inside the "Stop Deadlifting - QUEUED" entry.

## Dan's picks (locked 2026-09-30: all five)
Approximate source times from Whisper; snap every cut to measured silence (VAD under his music bed, `work/vad.py`) and
confirm on the picture. No source second may appear in two shorts (assert it).

| # | Working title | Source pieces | ~Length |
|---|---|---|---|
| 1 | Deadlifts Cause More Injuries Than Every Other Lift | 1:56.6-2:19.7, 3:13.1-3:47.5 | 58 s |
| 2 | Safer Lifts Build MORE Muscle Long Term | 0:00.0-0:02.6 ("Stop doing deadlifts."), 4:00.7-4:48.8 | 51 s |
| 3 | Wide Grip vs Narrow Grip: Build Width, Not A Powerlifter Body | 4:55.4-5:15.9, 5:24.9-5:38.4, 5:49.8-6:03.5 | 48 s |
| 4 | 2 Back Exercises To Do Instead Of Deadlifts | 6:03.5-6:09.3, 6:14.0-7:07.3 | 59 s |
| 5 | Train Legs Without Deadlifts | 7:07.3-7:46.5 | 39 s |

- Short 5 opener: Dan did not answer whether it opens on "Stop doing deadlifts." Default: **no hook** (that line is
  already Short 2's opener, and "Deadlifts are also powerful for building leg muscle, but..." opens well on its own).
  Put it in "What I decided" so he can overrule. Drop the leading "Now," at 7:07.3 if the cut is clean.
- Short 3 and Short 4 share the 6:03.5 boundary: Short 3 ends on "...better for making you look better." (words end
  ~6:03.5); Short 4 starts on "So if I've convinced you..." Pick one silence point and give each side its own frames.
- Watch for junk: Short 5 has "building more muscle to begin with but, but then" (~7:40); Short 1's join from "It's
  really a high risk of injury exercise." to "But what you don't realize..." must read as one thought.
- "On screen right now" lines (5:08 in Short 3, 6:57 in Short 4, 7:23 area in Short 5) need the visual they point to
  inside that short.

## What the page must contain (standard review page, generator `.claude/skills/longform-edit/reference/ro16/page.py`)
Decision budget for this round: **at most 5 questions.** Everything else goes in "What I decided".

1. **Header:** what this is, what is reused from SL-04, then "Your decisions (N)".
2. **Look sample at the top (player):** the first 10 seconds of Short 1 finished in the vertical crop, title band and
   captions on, in two grades:
   - A: SL-04's approved Zeeshan-short grade approach (per-shot `GRADE_SAT` in the SL-04 `render.js`; Short 1's final was
     `curves 0.25/0.155 0.5/0.335 0.75/0.56 1/0.84, eq sat 1.08`). Re-measure on THIS source, which is a different room.
   - B: Zeeshan's grade untouched (decoded as BT.709, `scale=in_color_matrix=bt709:in_range=tv`).
   Show median luma / saturation under each, next to Muhammad's reference numbers from VIDEO-RULES (Ad 1 0.22/0.23,
   Ad 6 0.27/0.39). Re-measure the rendered file, not stills (SL-04 round 2 trap).
   **Audio:** Zeeshan's mix untouched (map `0:a:0` stereo, cut only, 15 ms de-click fades, AAC **320k**), gated with
   `audio_gate.py --reference-mix <his same cut> --verbatim`. The question is only "sounds right?"; link the A/B clip.
3. **Intro title graphic, all five shorts:** one still per short on its real graded opening frame, exact eyebrow +
   headline copy, three per row. Short 1 also shows the two style options side by side:
   - A (recommended): the SL-04 J2 title band Dan finalized on 09-30 (black band, olive letter-spaced eyebrow, white
     Impact headline, frame flush with the video edge, no scrim). Matches Zeeshan's olive key-point chips.
   - B: Soft Blue Light title (`_shared/softblue.py`, 9:16 layout per `SOFTBLUE.md`).
   Draft copy (Dan edits on the page; measure that it fits in 2 lines):
   1. STOP DOING DEADLIFTS / MORE INJURIES THAN EVERY OTHER LIFT
   2. BUILD MORE MUSCLE / SAFER LIFTS WIN LONG TERM
   3. BACK WIDTH / WIDE GRIP VS NARROW GRIP
   4. SKIP THE DEADLIFT / 2 BACK EXERCISES TO DO INSTEAD
   5. SKIP THE DEADLIFT / TRAIN LEGS WITHOUT DEADLIFTS
   Titles hold for the whole short, on the band, never on his face (Step 7 of `/shorts`). AbsByAI.com on every short.
   Never "over 40" in a title (memory `shorts-organic-research`).
4. **Hair at the top edge (one decision, with evidence):** `tops.png` shows Zeeshan's talking shots with the hair at or
   within a few px of source row 0 (1:24, 3:30, 5:24, 6:40 worst). No 9:16 window can add rows. Measure it properly
   with `hair/measure.py` (Vision mask every 0.25 s over every talking shot in the five pieces) and show one evidence
   image like `Short-form video content/arms-shoulders REVIEW/R2_hair_camera-framing.jpg`. Precedent: on 2026-09-30 Dan
   accepted the same camera framing for SL-04 and finalized it. Recommend accepting; the title band sits directly above
   his head, so the edge reads as the band's edge.
5. **"What I decided" (one line each):** cut points per short with the first and last words; Short 5 no hook; how
   Zeeshan's burned KEY POINT chips are handled (SL-04 round 2 method: `cardCrop` above his pill rows and our re-set
   pill on the black field, or a zoom window that excludes the band; re-measure his pill rows on this video); which shots
   become cards (AI clips at 0:00, 0:44, 3:42, 5:00, 5:12, 6:18 keep their "AI Generated" label whole; the exercise
   B-roll with "Exercise #1: T-Bar Row" / "Barbell Row" / "Exercise #4" pills keeps each pill whole); his zoom-blur
   transitions at section starts (hold a sharp frame, max 7 frames, or cut around them); caption style (Arial 86 bold,
   lower-case "abs", CTC-retimed onsets per `work/ctc_source.py`); spend so far ($0 new; Whisper already paid).
6. **One reply box** with the decision lines pre-filled and a Copy button.

Serve the page from a local server and check every `src`/`href` returns 200 before sending the link; Dan reviews in
Chrome. Send the link plus a plain-language summary and a numbered action list at the bottom.

## Internal work to do now so round 2 is fast (no full renders)
- `segments.js` for all five with measured `inAt`/`outAt`; the full-rate cut finder (`work/cuts.py`); shot plan with
  window/card per shot and its reason (`plan_shots.py`); graphic scan (`work/gfxscan.py`) for his chips and labels;
  CTC caption timing; junk pass (`_shared/cut/junk.py`) and the cut-continuity pass (`_shared/CUT-CONTINUITY-QC.md`) on
  the selected pieces. Record anything that needs Dan in the page, not in chat.
- Machine cap: at most two video builds at once across sessions; check `ps` first (RO-12, RO-16 and SL-04 may be running).

## Close the round
When Dan's reply arrives (this session if he answers while it is open, otherwise the next): record every decision in `sl05/round2-plan/decisions.json` (item, path, sha256, verdict, his exact
words, scope). Then write `Handoffs/handoff-YYYYMMDD-sl05-round2-build-five-shorts.md` (build all five from the locks,
`deliver_all.sh`, watch pass, fresh-subagent judge, `gate.py --format short`, independent Opus reviewer, deliver to
`Short-form video content/stop-deadlifting-short<N>_<slug>.mp4` + REVIEW 540p copies + `stop-deadlifting-SHORTS.md`,
queue `delivered`, send Dan the review copies). Stop. No session waits for his answer.

## Constraints
- No covers (Codex does covers). No upload or Blotato. Don't duplicate DS-18 (kettlebell deadlift) or DS-24 (rear delt fly).
- Zeeshan's audio: cut only, never processed. No em dashes anywhere: grep the page and notes for the em-dash character before sending; the count must be 0.
- Cost ledger: $0 so far this job beyond the ~2 cent Whisper run. No AI generation planned.

## Recommended model
**Opus 5.5, high effort** (SL jobs are Claude secondary cuts under the 2026-09-30 routing).

## Starter prompt
> Read `Handoffs/handoff-20260930-sl05-round1-look-and-intro-packet.md` and everything it lists, then build the SL-05
> round 1 review page: the first 10 seconds of Short 1 in two grades with Zeeshan's audio untouched, the intro title
> still for all five shorts (Short 1 in both title styles), the hair evidence, and a "What I decided" list. No full
> renders. Send me the page link, then write the round 2 handoff once I reply.
