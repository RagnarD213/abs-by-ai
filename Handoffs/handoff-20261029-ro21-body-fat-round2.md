**LFC.** Task name: `Body Fat % LFC R2`. Model: Claude Opus 5.5, high effort (the video started on Claude).

# RO-21 "What Every Body Fat Percentage Looks Like (On Me)", round 2

Round 1 (Claude, task `Body Fat % LFC R1`, 2026-10-28/29) is reviewed. Dan approved the first minute and every item on the round 1
page except the four changes below, and said "Proceed with the edit." Release: Wed Dec 30, 2026 (January blitz).

## Read first
1. `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/longform-edit/SKILL.md` (top
   sections), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.
2. **`.claude/skills/longform-edit/reference/ro21/README.md`**: the whole recipe, order and every trap round 1 hit. Then
   `reference/ro24/README.md` (the 16:9 key port) and `.claude/skills/_shared/greenscreen-bg/README.md` (locked template).
3. Decisions with hashes: `/Volumes/Expansion/_edit_work/RO-21/round2-plan/decisions.json` (Dan's exact words inside).
   Re-hash the locked files listed there before touching anything; record expected vs actual.

## Where everything is
Work dir `/Volumes/Expansion/_edit_work/RO-21/` (Extreme is 98% full). Recipe scripts: `recipe/` (same files as the skill
reference). Key: `key/K*.mkv` + `.done` stamps, the WHOLE film's presenter frames are keyed (22 ranges): never re-key; if a shot
moves outside the ranges, key only the missing frames with `recipe/key/key_all.sh` (keyonce skips the rest). Round 1 page:
`round1/review/` served at http://127.0.0.1:9521/ (managed `review_server.py`). AI pictures `ai_images/L35..L08.png`, B-roll
`broll/B*.mp4` (padded +2 frames, `recipe/broll_r1.py` rebuilds), stock `stock/INDEX.md`, voice `audio/film/film_voice_B.wav`.

## Locked (do not re-ask)
- First minute (cut, opening ladder, graphics): approved. Colour: **B Rich** (`assemble_r1.py --grade rich`; round 1 drafts
  were warm, so everything renders again in rich). Voice: **A** = `film_voice_B.wav` (RO-24 Bill Maher voice + bass lift).
- The eight AI pictures, the "me today" photo (studio-white-57), every graphic, picture card, side card, lower third, B-roll
  and background on the round 1 page, except below. Takes, word fix ("show"), unpatched recap "calorie", dropped scale
  graphic: all approved by "Everything else looks good."

## The four changes (Dan, 2026-10-29)
1. **B01** (15.86-19.66, "The scale can't tell fat from muscle. It just tells you how heavy you are."): replace stock B0502
   with our library AI clip **A0207** (man steps off his bathroom scale, frowns, taps it as if broken; 16:9, 5.4 s), full
   screen, AI-GENERATED chip for its whole time. Dan: "our AI clips of someone weighing themselves are better than stock
   now" (memory `ai-weighing-clips-over-stock`). Grade it to sit with the film; crop out any burned label.
2. **P12** (302.44-304.74, "You look like that picture right there."): change the card headline "That Picture" to a
   descriptive line; Dan's example "You start to see the upper four abs". Use e.g. eyebrow "180 LB AT 12%", headline
   "Upper Four Abs Show" (fit check: 766 px at 84 px in `from_plan.py`). Re-render P12 only.
3. **B10** (319.73-323.99, "I sleep best at 63 degrees so I keep my room as cold as I can get it."): a NEW AI clip of Dan
   sleeping, looking ripped (shirtless, lean like L08 / his real photos), in a dark cool bedroom with a **Nest thermostat on
   the wall visibly reading 63**. Codex START/END frames (`_shared/codex-image.sh`, real identity reference, Dan relaxed,
   no hands on body), the readout must say 63 (set the digits in code over the frame if Codex misdraws them), then
   `_shared/framecheck/gate.py START END --verify` + a fresh `frame-reviewer`. **Dan approves the frames before any
   motion.** Motion afterwards on Google Flow via the background `flow-veo` agent (subscription, no paid API), then
   `clipcheck.py --verify`. Read memory `ai-clips-natural-or-regenerate` (calm, real-looking, regenerate slop).
4. **G10** (323.99-334.13, the University of Chicago sleep study lower third, Dan on screen): keep the lower third; the
   background behind Dan during it shows **a sleep-deprived overweight man** (a new Codex AI still: tired, heavy man awake
   in bed at night or groggy in the morning, not belly-focused). Put it on the studio set's TV (`set` type, the set's own
   AI chip) or as a clear background panel; not blurred. Background segment today: `BG22` in `round1/bg_plan.json`
   (override in `recipe/facts_r1.py`).

## Next actions, in order
1. `python3 .claude/skills/_shared/editcap/editcap.py acquire RO-21 --title "Body Fat % LFC R2" --type LFC --release 2026-12-30`
   (exit 3: `wait` in the background, tell Dan, stop). Rename the chat `Body Fat % LFC R2`. Work in `round2/` (copy the
   round 1 recipe outputs you change; never overwrite a reviewed round's files).
2. Build B10 frames (Codex) + the G10 sleep-deprived man still; gate + frame-reviewer on the B10 pair.
3. A SMALL round 2 page (same layout): B10 START/END frames with the line they play under, the G10 background in context
   (one context clip), B01 with A0207 in context, P12 in context. Give the first minute its own inline player at the top
   of every page from now on (Dan, R1: "The first minute isn't showing on the review page": the docked player stays empty
   until a button is pressed). Silent checks, then Finish checks for owner. `editcap.py release RO-21 --review`. Stop.
4. After Dan approves the frames: B10 motion (flow-veo), clipcheck, then the FULL film in rich: `assemble_r1.py` whole
   range, voice mux, a music bed (none yet; pick one and transcribe it: zero words), captions/subtitle file (Whisper on
   the delivered audio), chapters, every gate (`_shared/deliver/gate.py`, `audio_gate.py`, watch pass), an independent
   `ra-reviewer` (Opus 5.5) on the exact file, then deliver per `00-RULES.md` section 4 and the round method (full-film page
   with a revision list and timestamps). Copy review videos of 45 s+ to `Videos to Review/`.
5. Queue: `python3 scripts/edit-queue/queue.py set RO-21 delivered` when Dan gets the full film; mirror to the Edit Queue
   artifact db (project `tmp/edit-queue-export/RO-21.json`, ArtifactData set on https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs).

## Cost ledger
Round 1: $0 paid generation (21 Codex images on the subscription), a few cents of Gemini listening/watch checks. Round 2
expected: about 6-12 Codex images (frames + one still), Flow credits for one 4-5 s clip, cents of Gemini.

## Open risks
- The AI chip placement rule in `assemble_r1.py`: top-left on AI backgrounds, inside the first photo on panels.
- `ffmpeg` in `Media/video_edit/bin` is the render-queue wrapper; use `ffmpeg.real` for few-frame grabs only.
- The coordination board is at its 2,500-word cap; the job is claimed on the edit queue instead (no board entry).

## Starter prompt
> Body Fat % LFC R2. Read `Handoffs/handoff-20261029-ro21-body-fat-round2.md` and do it: RO-21 "What Every Body Fat
> Percentage Looks Like (On Me)" round 2 with /longform-edit, Opus 5.5 high. Acquire the edit slot first, re-hash the locks,
> build the B10 sleeping-Dan frames (Nest thermostat at 63) and the G10 sleep-deprived man background, swap B01 to AI clip
> A0207, fix the P12 headline, then send me the small round 2 page and stop for my frame approval.

## Round 2 status (2026-10-29, Claude Opus 5.5)
Delivered the small page http://127.0.0.1:9522/ (`round2/review/`), handed over paused with sound ready; edit slot released
(--review); queue `draft_review`. Locks re-hashed: 77/77 match (`round2/rehash_r2.json`). Built: B01 = A0207 with chip
(`round2/broll/B01.mp4`), P12 "Upper Four Abs" (`round2/hf/tpl/renders/P12.mov`), G10 tired man on the set TV
(`round2/ai/G10_man.png` -> `round2/bgclips/G10_man.mp4`), B10 START/END `round2/ai/B10_start.png` / `B10_end.png` (gate PASS +
fresh reviewer PASS; first END failed for a head swing). Hashes `round2/hashes_r2.txt`. **Next:** Dan's frame approval, then
step 4 above (B10 motion on Flow via flow-veo from these frames, prompt: one slow breath, camera locked; then the full film).

## Round 3 status (2026-10-29, Claude Opus 5.5): full film delivered
Dan's R2 reply (B10/P12/G10 approved, "Proceed with the edit"; other man's pictures at 0:06, 0:28 single, 0:57 and through the
film): `/Volumes/Expansion/_edit_work/RO-21/round3/decisions_r2.json`. Full film 7:27 (13,410 frames) at
`round3/final/RO21_MASTER.mp4`, page http://127.0.0.1:9523/, delivered to `claude edited long form content/24 - What Every Body Fat
Percentage Looks Like (On Me)/`, queue `delivered`, slot released. Independent review: SHIP on the third pass (first two caught a
40 ms-per-join lip-sync drift from round 1, side-by-side pairs, a click and a recap restart; all fixed). Gate 38/39, the fail is
the approved voice A tone row. Open question to Dan: switch the three remaining round-1 TV pairs of him to singles?
**Next:** Dan's notes or approval; on approval `/video-setup` (Wed Dec 30) with `RO21.srt` and the chapters.

## Round 4 status (2026-10-30)
Dan's R3 notes done: third picture set (Hispanic man, 30s), three sets rotate, gym B-roll regraded, AI label off every face and abs. Picture-only patches; audio and SRT unchanged. Delivered in round4/final. Next: Dan's review, then /video-setup for Wed Dec 30.
