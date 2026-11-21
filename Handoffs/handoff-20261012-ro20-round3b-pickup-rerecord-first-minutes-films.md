# RO-20 / RO-20B / RO-20C "Invest In Your Health": round 3b, Dan's answers to the first minutes, then the three films

**CONTENT (LFC), organic long-form, 16:9, three videos cut from one roll, one task. Sidebar name: `Invest In Your Health LFC R3b`.**
Updated 2026-10-16 (later) by the round 3b session (Claude Opus 5.5). **Step 1 DONE, waiting on Dan:** the C1722 pickups are laid in and shown on
http://127.0.0.1:8868/ (generator `recipe/page5_20.py`) with two questions: (1) do the studio pickups sit (A: cuts-only tone match, recommended and used in the clips;
B: film chain only), (2) the sign-off sentence (Dan's starter prompt left the bracket unfilled, so it is asked again). Treatment, takes and lessons:
`.claude/skills/longform-edit/reference/ro20/README.md`, "Round 3b". Pickups in `round3/pickups/` are option A (`OPT=match pickup_audio20b.py`);
option B is in `round3b/opts/chain/`. Desk-mic outputs backed up in `round3/backup_desk_20261013/`. **Next: Dan's two answers, then steps 2 to 4.**

## Goal

When the studio pickups are uploaded: lay them in, show Dan the first minutes of videos 2 and 3 and video 1's ending again, get his answer on
the sign-off sentence, then, with nothing pending, build the three full films.

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

1. **Pickups from roll C1722** (`/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1722.MP4`; lav on the LEFT channel only, `-map 0:a:0 -af pan=mono|c0=c0`;
   take map in `Docs/PICKUPS_1017_SHOOT.md`, section "Recorded 2026-10-15: where every take is (roll C1722)"). Takes to use, set exactly on the lav envelope and confirmed by ear first:
   P1 35.9 to 47.7 s; **P2 53.0 to 66.6 s** (take 1: take 2 drops "makes you more money" and stumbles); P3 116.4 to 136.9 s; P4 166.1 to 183.2 s.
   - Extract the lav to a 48 k mono WAV, transcribe it with Whisper medium.en word times, and point `pickup_audio20.py` at it (`D`, the transcript
     file name, `TAKES`; drop the P3 two-take splice, take 2 is clean). The lav flat-tops at -0.49 dBFS on loud words on this shoot: check each take.
   - **Treatment: same mic as the film now, so start from the film's own chain**, not the desk-mic recipe: the pickup lav through
     `voice_chain.py` with `build.VOICE4` (dereverb only if the green screen room measures wet), then level matched to the film's speech. Compare
     blind against two others (the `pickup_audio20.py` match with BOOST 0, WET off, LOWCUT 0; and the raw lav level-matched) on the three join
     clips, rank, pick. Keep the film's room tone under the pickup only if the floor drops at the join.
   - Rerun `first_minutes_r3.sh` (it renders P1 to P4 and the joins), update `page4_20.py` (decision 1 becomes "do the studio pickups sit?"),
     copy to `Videos to Review/`, refresh port 8868, and stop for Dan. Ask the sign-off sentence again (page decision 2).
2. Rebuild `voice/film_voice.wav` (`build.py filmvoice`): it does not cover the appended sign-off yet.
3. Per video, assemble from `videos.json`: film ranges (set the two dropped sentences' exact frames on the voice envelope; v1 end 900.35, v2 film start 904.70,
   v2 open 3014.45 to 3026.62, v3 film start 1420.786 with a short lead-in handle from the roll before "All right."), pickup segments, video 1's sign-off.
4. The three films: quiet music bed from RO-06 / RO-07 at the audio gate's floor row (under the pickups too), SRT, chapters re-cut per video, edit sheet,
   delivery gate, watch pass, one independent `ra-reviewer` per film, `roll_sidecar.py mark-used`, queue `delivered`. Later-round delivery message lists
   what is new with timestamps (VIDEO-RULES 2026-10-10). Copies to `Videos to Review/`.

## Open risks

- The sign-off sentence cut was judged on measurements and Whisper only; Dan has not answered it.
- Gi03 is on screen 3.2 s. Pool clips B0427 and B0032 read more orange than the presenter inside the card window.
- B0275 (heart monitor strip) is graded inside `pickups20.py` only; video 1's item Cc04 uses it ungraded.
- P2's J1 window is 0.04 s shorter than its slot (the window closes early; nothing is held).
- The camera clipped the top of his hair for most of the roll (unfixable in the edit, reported in round 1).

## Recommended model and effort

Claude Opus 5.5, high: three long builds with joins judged by ear and measurement.

## Starter prompt

```
Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20261012-ro20-round3b-pickup-rerecord-first-minutes-films.md`: round 3b of the three "Invest In Your Health" videos (LFC, content; RO-20, RO-20B, RO-20C in one task). My four pickups are recorded on the shoot lav (10/15 shoot, roll C1722; the take map is in the handoff). Lay them in, show me the first minute of videos 2 and 3 and video 1's ending, then build the three full films only when nothing is pending. Sign-off sentence: [keep it ended on "filled with motivation." / put the words back]. Name this session "Invest In Your Health LFC R3b".
```
