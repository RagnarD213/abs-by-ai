# Invest In Your Health, round 4: build the three full films (RO-20, RO-20B, RO-20C)

**CONTENT (LFC), organic long-form, 16:9, three videos cut from one roll, one task. Sidebar name: `Invest In Your Health LFC R4`.**
Written 2026-10-17 by the round 3b session (Claude Opus 5.5) after Dan approved everything. Nothing is pending from Dan.

| video | title | job |
|---|---|---|
| 1 | Why You Should Invest More In Your Health | RO-20 |
| 2 | What To Cut To Afford Getting In Shape | RO-20B |
| 3 | What To Buy For Your Health At Every Income Level | RO-20C |

Always name them to Dan by title (AGENTS.md, 2026-10-17); the code may follow the title.

## Dan's words (2026-10-17, on the round 3b page http://127.0.0.1:8868/)

*"Okay, everything is approved. Go ahead and edit the videos."* Recorded item by item in
`/Volumes/Extreme/_edit_work/ro20/round3b/decisions.json`. That approves: pickup treatment **A** (cuts-only tone match), the video 1
sign-off sentence **kept ended on "filled with motivation."**, the partnership clip J2-t3 in video 1, video 2's ending screens (P3) with
the studio pickup, and the round 3b first minutes and video 1 ending as shown.

## Read first

1. `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (in full), `PRE-RENDER-APPROVAL.md`, `CUT-CONTINUITY-QC.md`.
2. `.claude/skills/longform-edit/reference/ro20/README.md`, all of it; the last three sections are rounds 3 and 3b. Working recipe:
   `/Volumes/Extreme/_edit_work/ro20/recipe/` (never run another session's build directory).
3. Previous handoff, for the full build steps 2 to 4 and the open risks: `Handoffs/handoff-20261012-ro20-round3b-pickup-rerecord-first-minutes-films.md`.
4. `round3-plan/decisions.json`, `round3b/decisions.json`, `round2-plan/videos.json` (the three videos as ranges of the one timeline).

## Locks (re-hash before building; a mismatch stops the build)

- `round3b/round3b-hashes.sha256`: the four pickup voices `round3/pickups/P1-P4.voice.wav` (option A, `OPT=match recipe/pickup_audio20b.py`),
  the four pickup segments `round3/pickups/P1-P4.mp4`, and the three approved review clips in `round3/first-minute-3b/`.
- `round3/round3-hashes.sha256`: everything locked in round 3 (video 1's first 77 s, AI clips, cards, sign-off).
- Voice 4 (`build.VOICE4`) for the film voice, look D, all graphics as approved. **The 2026-10-17 HyperFrames motion rule is prospective:
  do not restyle these approved graphics.**

## Already applied (do not apply twice)

- Takes from roll C1722 (10/15 shoot): P1 35.90 to 48.10 s, P2 53.00 to 66.80 (take 1), P3 116.30 to 137.10, P4 166.05 to 183.45.
- Pickup treatment A: 70 Hz high-pass, third-octave match to the film voice with boosts capped at 0 dB, no synthetic room, level matched to
  the film's active speech (-15.8 dB), peaks under -2 dBFS. No room tone added (the pickup floor sits above the film's, so it never drops).
- P3 already carries its 5.4 s tail for YouTube's end screen.
- Video 1's sign-off is appended after the last piece (round 3); the sentence ends on "filled with motivation." (film 3212.175 s).

## Build (steps 2 to 4 of the previous handoff, with these round 3b notes)

1. Re-hash the locks. Check the build cap (`python3 .claude/skills/_shared/buildcap.py`; two builds at a time across all sessions).
2. `build.py filmvoice`: rebuild `voice/film_voice.wav` so it covers the appended sign-off.
3. Per video, assemble from `videos.json`: film ranges (set the two dropped sentences' frames on the voice envelope; v1 end 900.35, v2 film
   start 904.70, v2 open 3014.45 to 3026.62, v3 film start 1420.786 **with a short lead-in handle from the roll before "All right."**, which
   starts 4 ms after its range today), the pickup segments, video 1's sign-off.
4. **Pickup audio in the films:** the pickup voices are already treated. Lay them in as they are; never send them through `voice_chain.py` a
   second time. Give the audio gate an untreated baseline that covers the pickup ranges (the raw C1722 lav, same ranges) so its "do no harm"
   row is measured, not missing.
5. Quiet music bed from RO-06 / RO-07 at the audio gate's floor row, under the pickups too. SRT, chapters re-cut per video, edit sheet.
6. Gates on each delivered file (`_shared/deliver/gate.py --format longform`), watch pass, the cut-continuity pass on every join (pickup entry
   and exit with moving context), then one independent `ra-reviewer` per film. Fix what they find before Dan sees anything.
7. Deliver per 00-RULES section 4 to `claude edited long form content/NN - <Title>/` (master, SRT, chapters, stamps, notes, recipe, REVIEW 540p),
   copies to `Videos to Review/` named `Invest In Your Health LFC R4 - video N full film.mp4` (remove the R3/R3b copies of these videos then),
   review page on port 8868, `roll_sidecar.py mark-used` for every source range, queue `delivered` for all three (`queue.py` + artifact db mirror).
8. Delivery message: later-round format (VIDEO-RULES 2026-10-10), with the new parts by timestamp in each film (the pickups, the sign-off,
   the video 3 lead-in) and the end-of-task wrap-up boxes.

## Gate status, honestly

The round 3b review clips were checked with the audio gate only, without stamps. Video 1's ending passed every row a clip can measure. Video 2's first
minute missed the processing row by 0.002 (flux 0.081 against 0.079) and video 3's tone peak by 0.06 dB (2.56 against 2.5). "Do no harm" was
not measured on any of them (no untreated baseline). The film-only context clips fail the same rows by more (tone peaks 2.7 to 4.1 dB,
v2film flux 0.082), so those rows on short clips say nothing about the joins. The full films are what get gated. Never raise a bound.

## Cost ledger

AI: video 1 $7.39 of its $12 cap; videos 2 and 3 $0.60 each of $15. No new AI clip is planned. Any retake goes through the Google Flow
subscription (`flow-veo` agent), never Replicate unless Dan says rush. Round 3b Gemini listening: under $1.

## Open risks (carried)

- Gi03 is on screen 3.2 s. Pool clips B0427 and B0032 read more orange than the presenter inside the card window.
- B0275 (heart monitor strip) is graded inside `pickups20.py` only; video 1's item Cc04 uses it ungraded. Grade it there too (all B-roll is graded).
- P2's J1 window is 0.04 s shorter than its slot (the window closes early; nothing is held).
- The camera clipped the top of his hair for most of the roll (unfixable in the edit, reported in round 1).
- Release: the long-form calendar has RO-20/B/C off the schedule until Dan says otherwise. No setup or upload in this task.

## Recommended model and effort

Claude Opus 5.5, high: three long builds, joins judged by ear and measurement, three independent reviews.

## Starter prompt

```
Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20261017-ro20-round4-three-films.md`: round 4 of the three "Invest In Your Health" videos (LFC, content; Why You Should Invest More In Your Health RO-20, What To Cut To Afford Getting In Shape RO-20B, What To Buy For Your Health At Every Income Level RO-20C, in one task). I approved everything on the round 3b page, including pickup treatment A and keeping the sign-off ended on "filled with motivation." Build the three full films, run every gate and an independent review of each, and deliver them for my review. Name this session "Invest In Your Health LFC R4".
```
