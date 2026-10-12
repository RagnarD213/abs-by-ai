# RO-20 / RO-20B / RO-20C "Invest In Your Health": round 3b, re-record the pickups, first minutes of videos 2 and 3, then the three films

**CONTENT (LFC), organic long-form, 16:9, three videos cut from one roll, one task. Sidebar name: `Invest In Your Health LFC R3b`.**
Written 2026-10-12 by the round 3 session (Claude Opus 5.5). Replaces `handoff-20261011-ro20-round3-pickups-and-first-minutes.md` (executed as far as the pickups allowed).

## Goal

Record Dan's four pickups again (the 10-12 recording is unusable), lay them in, show him the first minute of videos 2 and 3, record his
answers to the round 3 page, then, with nothing pending, build the three full films.

## Read first

1. `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (the pickup procedure dated 2026-10-11 and the bass rule dated 2026-10-12), `PRE-RENDER-APPROVAL.md`, `CUT-CONTINUITY-QC.md`.
2. `.claude/skills/longform-edit/reference/ro20/README.md`, all of it; the last section is this round. Working recipe: `/Volumes/Extreme/_edit_work/ro20/recipe/`.
3. `/Volumes/Extreme/_edit_work/ro20/round3-plan/decisions.json` (Dan's words), `round2-plan/videos.json` (the three videos as ranges; video 1's sign-off range is now in it), `round3/round3-hashes.sha256`.
4. Round 3 page: http://127.0.0.1:8868/ (`round3/`, generator `recipe/page4_20.py`). Dan has NOT answered it yet: three decisions (re-record; the sign-off sentence ended on "filled with motivation."; the receipts clip in place of scissors cutting a card).

## Done in round 3 (do not redo)

- **Video 1 AI cap: $12** (Dan). Spent: video 1 $7.39, video 2 $0.60, video 3 $0.60. Ledgers `round2/motion/ledger.json`, `round3/motion/ledger.json`.
- **Motion made and wired into `plan_parts/p00_halo.py`:** intro T3 (`round3/motion/T3-t1.x112.mp4`, the take from 0.25 s at 1.12x, plan item `T3`, 0:00 to 0:06.74),
  job interview `J1-t3.mp4` (item Ca02), partnership `J2-t3.mp4` (item Ca03, made from the approved END frame). Read frame by frame; not yet seen by Dan or an independent reviewer.
- **Video 1 sign-off:** pieces `v1so1` to `v1so4` appended after `cta`, timeline 3184.314 to 3244.808 s, plan part `p08_signoff_v1.py` (Gi01 to Gi05, P03). Proof `round3/signoff_v1/proof.json`, notes in `take_map_notes.md`.
- **Pickup screens:** `recipe/pickups20.py P# WORDS.json OUT.mp4 --audio VOICE.wav`; P2 with `--j1 /Volumes/Extreme/_edit_work/ro20/round3/motion/J1-t3.mp4 --j1-in 6.3`. Placeholders in `round3/pickups/`.
- **Voice:** voice 4 unchanged (its lowest tone band already reads above the reference, so the bass rule adds nothing). Told to Dan on the page.
- **Shown on the page:** video 1's first 77 s (audio gate 12 of 13, tone 1.52 against 1.2, the known fixed-EQ result), J2 in context, the sign-off, four silent pickup screens.

## Order of work

1. **Record.** Tell Dan the mic is starting, then: `~/.cache/absbyai/rec_mic "<repo>/Media/longform-raw/ro20-pickups/rerecord_20261012" 900 30` with
   `recipe/pickup_watch.py DIR PID` beside it (PATH must include `Media/video_edit/bin`). The lines are on the round 3 page and in `page4_20.py` (`LINES`); P2 starts at
   "In the last video". Check the recorder's last line (samples against wall time), then test the samples for block breaks (README, this round). Delete segments with no pickup.
2. **Pick takes** (last clean take per line; his wording wins), Whisper word times per pickup into `round3/pickups/words_P#.json` (`{"duration", "words"}`; give P3 at least 5 s after its last word for the end screen).
3. **Match the pickup voice to the film voice:** Yeti to mono, 70 Hz high-pass, a smoothed long-term spectrum match to `voice/film_voice.wav` speech (third octave, capped at about 6 dB),
   level matched to the sentences either side. Judge the joins with a blind listener (film sentence, pickup, film sentence) and the audio gate rows on the built first minutes. If a pickup still stands out, tell Dan.
4. **Rebuild `voice/film_voice.wav`** (`build.py filmvoice`): it does not cover the appended sign-off yet.
5. **First minutes:** video 2 = film 3014.45 to 3026.9 (on camera, `--bare` style check for stray graphics) + P2 segment + film from 904.74; video 3 = P4 segment + film from 1420.786.
   Video 1's ending in context = film to 900.25 + P1 + the sign-off. Copies of 45 s or more go to `Videos to Review/`. Update the page, record Dan's answers, re-hash. Stop for Dan.
6. **With nothing pending, the three films** exactly as the old handoff's step 6: quiet music bed from RO-06 / RO-07 at the audio gate's floor row, SRT, chapters per video, edit sheet,
   delivery gate, watch pass, one independent `ra-reviewer` per film, `roll_sidecar.py mark-used`, queue `delivered`. Set the two dropped sentences' exact frames on the voice envelope.

## Open risks

- The sign-off sentence cut ("filled with motivation.") was judged on measurements and Whisper only; nobody has listened to it.
- Gi03 is on screen 3.2 s, the shortest lower third in the film.
- Pool clips B0427 and B0032 read more orange than the presenter inside the card window, with their approved grades.
- Library clip B0275 (heart monitor strip) is graded inside `pickups20.py` only; video 1's item Cc04 uses it ungraded.
- The camera clipped the top of his hair for most of the roll (unfixable in the edit, reported in round 1).

## Recommended model and effort

Claude Opus 5.5, high: joins judged by ear and measurement, then three long builds.

## Starter prompt

```
Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20261012-ro20-round3b-pickup-rerecord-first-minutes-films.md`: round 3b of the three "Invest In Your Health" videos (LFC, content; RO-20, RO-20B, RO-20C in one task). Start the mic now for my pickup re-record and show me the four pickups to read. My answers to the round 3 page: [sign-off sentence: keep / put the words back] [receipts clip: keep / make an AI clip] [any other notes]. Then lay the pickups in, show me the first minute of videos 2 and 3 and video 1's ending, and build the three full films only when nothing is pending. Name this session "Invest In Your Health LFC R3b".
```
