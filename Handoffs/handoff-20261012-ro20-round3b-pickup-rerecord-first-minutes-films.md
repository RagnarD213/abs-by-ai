# RO-20 / RO-20B / RO-20C "Invest In Your Health": round 3b, Dan's answers to the first minutes, then the three films

**CONTENT (LFC), organic long-form, 16:9, three videos cut from one roll, one task. Sidebar name: `Invest In Your Health LFC R3b`.**
Updated 2026-10-13 by the round 3 session (Claude Opus 5.5). The pickups are re-recorded and laid in; the first minutes are on the page.

## Goal

Record Dan's answers to the round 3 page, re-record the pickups in the kitchen only if he says the voice does not sit, then, with nothing
pending, build the three full films.

## Read first

1. `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `CUT-CONTINUITY-QC.md`.
2. `.claude/skills/longform-edit/reference/ro20/README.md`, all of it; the last two sections are round 3. Working recipe: `/Volumes/Extreme/_edit_work/ro20/recipe/`.
3. `/Volumes/Extreme/_edit_work/ro20/round3-plan/decisions.json` (Dan's words), `round2-plan/videos.json` (the three videos as ranges), `round3/round3-hashes.sha256`.
4. Round 3 page: http://127.0.0.1:8868/ (`round3/`, generator `recipe/page4_20.py`). Open decisions: (1) does the pickup voice sit with the kitchen voice,
   (2) the sign-off sentence ended on "filled with motivation.". He has not yet seen the partnership clip (J2-t3) or the P3 screens with sound.

## State (do not redo)

- **Approved by Dan 10-13:** video 1's first 77 s (T3 intro, J1-t3), the pickup screens; P4 opens on the three-levels card (the B0429 shot is out).
- **Pickups:** `Media/longform-raw/ro20-pickups/rerecord_20261012/pickups_rerecord_48k_mono.wav` + transcript. Takes, treatment and its history in
  `recipe/pickup_audio20.py`. Outputs `round3/pickups/P#.voice.wav`, `words_P#.json`, `P#.mp4` (built by `recipe/first_minutes_r3.sh`).
  A blind listener still rates each join 8 of 10 noticeable ("closer, drier, fuller"); the gate rows pass. Dan decides by ear.
- **Built and shown:** video 2 first minute (film 3014.45 to 3026.62 bare + P2 + film 904.70 on), video 3 first minute (P4 + film 1420.786 on),
  video 1 ending (film to 900.35 + P1 + sign-off 3184.314 to 3244.808). Audio rows 12 of 13 on both first minutes (the 13th needs an untreated baseline).
- **Video 1 AI cap $12**, spent $7.39; videos 2 and 3 $0.60 each. Voice 4 unchanged (bass rule adds nothing on this roll).

## Order of work

1. Record Dan's reply word for word; re-hash. If he wants the kitchen re-record: he stands in the doorway with the shoot's lav; record with `rec_mic`
   or the camera, run the block test, rerun `pickup_audio20.py` (new `D`, `TAKES`; the match EQ should then come out near flat) and `first_minutes_r3.sh`, show the joins again.
2. Rebuild `voice/film_voice.wav` (`build.py filmvoice`): it does not cover the appended sign-off yet.
3. Per video, assemble from `videos.json`: film ranges (set the two dropped sentences' exact frames on the voice envelope; v1 end 900.35, v2 film start 904.70,
   v2 open 3014.45 to 3026.62, v3 film start 1420.786 with a short lead-in handle from the roll before "All right."), pickup segments, video 1's sign-off.
4. The three films: quiet music bed from RO-06 / RO-07 at the audio gate's floor row (under the pickups too), SRT, chapters re-cut per video, edit sheet,
   delivery gate, watch pass, one independent `ra-reviewer` per film, `roll_sidecar.py mark-used`, queue `delivered`. Later-round delivery message lists
   what is new with timestamps (VIDEO-RULES 2026-10-10). Copies to `Videos to Review/`.

## Open risks

- The pickup joins (above). The sign-off sentence cut was judged on measurements and Whisper only.
- Gi03 is on screen 3.2 s. Pool clips B0427 and B0032 read more orange than the presenter inside the card window.
- B0275 (heart monitor strip) is graded inside `pickups20.py` only; video 1's item Cc04 uses it ungraded.
- P2's J1 window is 0.04 s shorter than its slot (the window closes early; nothing is held).
- The camera clipped the top of his hair for most of the roll (unfixable in the edit, reported in round 1).

## Recommended model and effort

Claude Opus 5.5, high: three long builds with joins judged by ear and measurement.

## Starter prompt

```
Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20261012-ro20-round3b-pickup-rerecord-first-minutes-films.md`: round 3b of the three "Invest In Your Health" videos (LFC, content; RO-20, RO-20B, RO-20C in one task). My answers to the round 3 page: [pickup voice: good enough / I will re-record in the kitchen] [sign-off sentence: keep / put the words back] [any other notes]. With nothing pending, build the three full films. Name this session "Invest In Your Health LFC R3b".
```
