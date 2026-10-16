CONTENT | SL-06 | Top 5 Zepbound Tips SFC R2

# SL-06 round 2: lay in the lav pickups, build all six Zepbound shorts, gate, audit, one full review page

Rewritten 2026-10-16 by Claude (Opus 5.5). **Ready to fire now. Nothing is waiting on Dan.**

**Recommended: Claude Opus 5.5, high effort.** (Shorts from a long-form are a Claude secondary cut; six renders, gates and an audit.)

## What changed since round 1 (read this first)

- **Dan recorded the pickups on the shoot lav at the 10/15 shoot** (roll C1722, green screen set). The takes are chosen,
  matched to the film and saved as finished WAVs (section "Pickups" below). Do not record anything and do not use the
  desk-mic takes.
- **Dan did NOT review round 1, and will not.** His words, 2026-10-16: *"I'm not going to review this round because,
  without the pickups, I don't have context. I'll review all the other changes once you integrate the pickups in the next
  round."* So this round builds all six shorts on the round-1 recommendations (section "Build on these defaults"), and the
  round-2 page is his FIRST review of everything: the finished shorts, every graphic and clip, the AI frames and every
  open decision. Treat it as a round 1 under VIDEO-RULES ("Round 1 always reviews every graphic, stock item and clip").
- The round-1 page at http://127.0.0.1:8817/ is superseded. Remove its service once the round-2 page is up
  (`review_server.py 8817 --remove`).

## Goal

Six finished vertical Shorts (1080x1920) from RO-12 "Top 5 Zepbound Tips", A to E opening on Dan's lav pickup (F opens on
a film line), delivered as review copies with gate stamps and an independent audit, on one review page. No covers, no
upload, no queue. The parent goes public Sun Oct 25 2026; no short posts before it is verified public.

## Read first

1. `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/video-editing/00-RULES.md` in full.
2. `.claude/skills/shorts/SKILL.md`, then `.claude/skills/shorts/reference/softblue-sl06/README.md` (this batch's tooling
   and lessons), then `../softblue-sl03/README.md` for the gate plumbing (`deliver.py`, `rungate.sh`, `declare.json`).
3. `Handoffs/handoff-20261011-sl06-zepbound-shorts-pickups-and-build.md`: Dan's segment picks and his words. Still the spec.
4. `/Volumes/Extreme/_edit_work/sl06/notes_r1.py`: round 1's "What I decided" list and decisions, to carry onto the new page.

## State (2026-10-16)

- Work folder `/Volumes/Extreme/_edit_work/sl06/`: `plans.py` (all six as data), `build/<S>/` (audio, words, cues, shots,
  track, bars, ALL built against the desk placeholders, so every short is rebuilt), `clips/` (copies of every stock and
  library clip used), `pickups/` (the finished lav pickups, below), `aiframes/` (C and E start and end frames + REPORT.md),
  `round1/` (the unreviewed round-1 page, stills and `items_<S>.json`; reuse `export_stills.py` and `page_r1.py`).
- `Videos to Review/Top 5 Zepbound Tips SFC R1 - short D - Inject On Thursday Evening.mp4` is the round-1 test of D with a
  desk placeholder opening. Delete it when the round-2 D lands there.
- Desk-mic takes and their outputs: `pickups/raw_take2.wav`, `pickups/desk_placeholders/`. Never ship them.

## Pickups (done 2026-10-16: lay them in, do not redo)

Source: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1722.MP4`
(roll sidecar `C1722.roll/`; lav = `-map 0:a:0 -af pan=mono|c0=c0`, left channel only on this shoot). The Zepbound block is
roll 188.9 to 264.4 s; pulled to `pickups/lav_C1722_185-270.wav` (mono 48 kHz, its 0.0 s = roll 185.0 s). Each line was
read twice. The take used is his last clean take of each (take-selection rule); a Gemini listen also judged each of these
the smoother of the two. No take reaches the lav's -0.49 dBFS ceiling (peaks -3.8 to -7.8 dBFS). Edges are set on the lav
envelope, not on Whisper's times.

| | Line | Take used (roll C1722 s) | Finished pickup | Length | Speech level vs next film line | Room (film 67 ms) |
|---|---|---|---|---|---|---|
| A | Here's why you should start Zepbound at 1 milligram to avoid the side effects. | take 2, 203.59 - 207.47 | `pickups/A.wav` | 4.14 s | -13.7 vs -13.5 dB | 59 ms |
| B | Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead. | long take 2, 217.51 - 221.86 | `pickups/B.wav` | 4.61 s | -13.5 vs -13.0 dB | 53 ms |
| C | Here's how to inject Zepbound with a needle, step by step. | take 2, 237.84 - 240.42 | `pickups/C.wav` | 2.84 s | -15.1 vs -14.9 dB | 40 ms |
| D | Here's why Thursday evening is the best time to inject Zepbound. | take 2, 250.04 - 253.06 | `pickups/D.wav` | 3.28 s | -14.5 vs -14.4 dB | 64 ms |
| E | Here's how to come off Zepbound without gaining the fat back. | take 2, 261.48 - 264.37 | `pickups/E.wav` | 3.15 s | -13.5 vs -13.2 dB | 75 ms |

- **Short C, measured twice:** Whisper medium and the lav envelope show TWO complete takes, 233.98 - 236.60 and
  237.84 - 240.42, each ending "...with a needle, step by step." with nothing spoken after 240.42. (A note added earlier
  from Whisper small read take 1 as stopping at "with a needle" and take 2 as "step by step by... step"; small merged the
  two takes. The times above supersede it.)
- Alternates on the roll: A take 1 198.81 - 202.50; B long take 1 212.24 - 216.62; **B short wording** ("Here's why you
  should stop using the pen to inject Zepbound.") take 1 225.06 - 227.75, take 2 228.80 - 231.83; C take 1 233.98 - 236.60;
  D take 1 245.42 - 248.74; E take 1 257.66 - 260.17. Subtract 185.0 for the WAV.
- Treatment (`pickup.py`, tag `_lav`, `pickups/fit_lav.json`): one tone EQ fitted on all twelve lav takes toward the film's
  finished voice (same mic as the film, so the correction is small: 0.81 dB mean error, 1.62 max; largest band +3.4 dB at
  490 Hz), level matched to the next film line, the film's `bed.wav` under it at -26.8 dB on the film's clock, 15 ms
  de-click. No dereverb, no noise reduction, no gate. Per-take numbers: `pickups/<S>.report.json`. If a join sounds wrong
  by ear, the alternative is the film's own chain EQ (`/Volumes/Extreme/_edit_work/ro12/out/FIT.mp4.voice_chain.json` plus
  `bass=g=0.9:f=150`); compare the two on that join and keep the one that disappears.
- To use the B short wording: `pickup.py make B pickups/lav_C1722_185-270.wav 43.80 46.83 _lav`, then change
  `plans.PICKUP["B"]` and the first piece of `plans.TEXT["B"]`.
- **Listen to every join yourself before the page goes out.** Whisper hears "Zepbound" clearly on A, D and E and "zap bound"
  on B and C; the Gemini listen said "zap bound" on all twelve takes (the same boilerplate for every take, so weigh it
  lightly). The film has the same spread (RO-12 notes: intro takes 1 and 2 sounded like "zap bound"). Do not re-record or
  swap takes over it; one line on the page lets Dan judge it by ear.
- **Code still to update:** `plans.PICKUP` and `plans.TEXT` carry the five lines (B in the long wording) and point at
  `pickups/<S>.wav`, so no change is needed there; `batch.py head()` reads each WAV's real length.

## Build on these defaults (Dan has not seen any of them; every one goes on the round-2 page, overrulable)

1. **Title band:** ZEPBOUND TIPS (built). Show the GLP-1 TIPS still beside it (`round1/stills/D_title_glp1.jpg`) as the one
   alternative. With GLP-1, F's headline becomes "How Much Protein / You Need On A GLP-1".
2. **Title copy:** as in `plans.TITLE`, title case, two lines each.
3. **Steps in C and E:** one step at a time in the key-point bar with a counter (built). The film's list card does not fit
   under the title band (captions land on his mouth): show `round1/stills/C_optB_listcard.jpg` as the option not taken, one line.
4. **C's opening:** the fallback built (B0352 syringe close-up, lifted) until Dan approves the AI frames. Put the C frame pair
   (`aiframes/C_start.jpg`, `C_end.jpg`) on the page for approval. Motion only after he approves: 9:16, about 4 s, prompt says
   "fingers stay off the leg, no pinch"; about $1 to $2.
5. **E's last line:** the staircase stock (px9154824) built until Dan approves the roof gag. Put the E frame pair on the page;
   on approval it is TWO clips with a hard cut (he is drawn larger in the end frame); about $2 to $3.
6. **B's wording:** the long one he wrote while recording (built). The short wording is on the roll as an alternate.
7. **Key-point copy:** as in `plans.BARS`; list every bar's copy in the reply box.

Generation budget: $5 for this video, $0 spent (frames were on the subscription; the Gemini listen, about $0.05, is quality
review). Motion method and checks: `.claude/skills/longform-edit/reference/ro06/README.md`. Before AI frames reach the page,
run them through `_shared/framecheck/gate.py` and a fresh `frame-reviewer` agent (review pages refuse AI frames without both).

## Order of work

1. Rename the task "Top 5 Zepbound Tips SFC R2". Queue stays `in_progress`. Update the one-line board entry.
2. Check the five `pickups/<S>.wav` exist and match the table (length, report). Do not regenerate them unless a check fails.
3. For all six: `batch.py audio, words, plan, track (new shots only), plan`, then delete each `build/<S>/hf/manifest.json`
   and run `batch.py gfx A B C D E F` (every head changed; the A, B, C, E manifests were only time-shifted for round-1 stills).
4. `batch.py proof S`, look at every sheet, then `batch.py render S` for all six (about 4 minutes each; two builds at most).
5. Ear-check: transcribe each rendered short (Whisper small and medium) against `plans.TEXT`; listen to each
   pickup-into-film join; the level step at the join stays under 0.5 dB.
6. Write `deliver.py` for this batch from `softblue-sl03/deliver.py`: delivery copy to
   `Short-form video content/zepbound-tips-<plans.NAME>.mp4`, `audio_gate.py --reference-mix his_mix.wav --verbatim --ab`,
   REVIEW 540p, Whisper of the delivered file against the captions, gate `plan.json` (declare every join and size step),
   then `_shared/deliver/watch.py`, the judge, and `gate.py --format short`. Report any row that measures Dan's approved
   layout through `declare.json` with his words; never raise a bound.
7. A fresh `ra-reviewer` on the six delivered files, not shown your notes. Expect "does not ship" once; fix and re-run.
8. The round-2 page on a new port and folder (`round2/`), PRE-RENDER-APPROVAL layout: header with the seven defaults above
   as numbered decisions; all six finished shorts (each also copied to `Videos to Review/` as
   `Top 5 Zepbound Tips SFC R2 - short <S> - <title>.mp4`); a 6 second "pickup into film" clip per pickup short; the AI frame
   pairs; "What I decided" (carry round 1's list from `notes_r1.py`, updated for the lav pickups); every title, crop, clip,
   graphic and key point as stills (`export_stills.py`), three per row; one reply box.
9. Deliver: `notes-SL06.md`, `recipe-SL06/`, update `Short-form video content/zepbound-tips-SHORTS.md`,
   `queue.py set SL-06 delivered` with the artifact mirror, remove the 8817 service, delete the round-1 D copy from
   `Videos to Review/`. List the six shorts that need covers (a separate task). Posting order to suggest at setup:
   D, A, F, C, B, E; A and B at least a week apart; each Blotato config needs a `pinned_comment`.
10. When Dan finalizes: register new clips in the clip library, delete this video's copies from `Videos to Review/`, remove
    the round-2 page service, delete the board entry.

## Open risks the reviewer will look at

- Every same-camera join is a full to mid step (1.2x on screen). SL-03 reviewers wanted about 1.25x or a cutaway. B has two
  adjacent talk joins, C has seven in-take steps, E has six. If a join reads as a jump, cover it with a clip.
- C has two clips only (the opener and the needle close-up): `style:coverage` may fail. Add a steady cutaway, do not tune.
- C ends 40 ms before the film's own audio join at 216.12; the last word is whole on the envelope. Listen on the render.
- E runs about 58 s with the lav pickup; check it stays under 60 s.
- A caption can hang 0.3 s into the next shot at a clip cut (D near 0:21). Trim the cue to the cut if the reviewer flags it.
- The audio gate cannot declare a head span: its reference includes the pickup. Report the pickup numbers from
  `pickups/<S>.report.json` in the notes.
- B0458 (Dan's curls, F) and B0030 (ab wheel, F) are his real footage: no "real picture" chip on moving footage.
- The board is at its word limit; keep the entry to one line.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFC R2". This is CONTENT. Read `Handoffs/handoff-20261012-sl06-round2-build-after-dan-review.md` and execute it: lay my lav pickups from the 10/15 shoot into the six Zepbound shorts (they are already chosen and matched; do not record anything), build all six with /shorts in Soft Blue Light on the round-1 defaults, run the gates and an independent audit, and give me one review page with the finished shorts, every graphic and clip, the AI frames and the open decisions. No covers, no upload.
