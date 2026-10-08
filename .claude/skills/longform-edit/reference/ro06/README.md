# RO-06 "How To Work Out At Home On A Budget" (8/3 pool rolls C1557 to C1581): recipe (Claude Opus 5.5, 2026-10-08)

The first long-form cut from MANY short rolls (25 clips, 20 used) with the round method. Starts from RO-10's recipe.
Work dir and media: `/Volumes/Extreme/_edit_work/ro06/` (never commit media; the repo is public).

Order: `mkglobal.py` (all rolls on one global source timeline, one lav.wav, sidecar words) -> `edl.py` (pieces with
roll-local word times; writes `take_map.json`) -> `shots.py` -> `assemble_audio.py` + medium.en on the assembled cut ->
`words_out.py` -> `framing.py` (person mask per shot: hair top, head centre, T crop) -> `grade.py` (per-roll skin-anchored
curve, three strengths) -> `plan.py` -> `resolve.py` -> `hyperframes/from_plan.py --render` -> `build.py range a b out`
-> `stills.py` -> `context.py IDS` -> `page.py`.

Traps this build paid for:
- **One global timeline makes a multi-roll film look single-roll to every downstream script.** Rolls laid end to end in
  frames (`rolls.json`), lav concatenated sample-exact, word times offset. `frames.roll_of()` maps a global frame back.
- **The roll sidecars' Whisper small words hide false starts.** A 5.6 s "sentence" in C1580 held a whole abandoned copy.
  It only showed on a medium.en pass over the ASSEMBLED cut as a doubled phrase. Run that pass and a 4-word repeat scan
  before placing anything; then map medium words back to source time and split shots from those, not the sidecar words.
- **Outdoor lav: the studio -50 dB silence threshold walks edges up to 0.6 s into neighbouring words.** Room here is
  -58 to -48 dB; -42 dB for edge snapping, -43 dB for pause detection. A soft tail ("house") still sits under it: the out
  point is never earlier than the word end + 0.18 s, never past the next word.
- **Dan runs sentences together outdoors**: almost no pauses over 0.7 s. Reframe cuts (nothing removed) every 6 to 10 s on
  sentence ends carry the framing changes; a comma or any word boundary is the fallback.
- **The sun dropped during the shoot.** Whole-frame brightness fell 0.24 to 0.10 while sunlit skin held 0.37 to 0.50.
  Grade per roll on the skin highlight (Y90 of mask AND skin-colour pixels), never on the frame median.
- **1080p wide rolls: T is 1.5x (bottom edge mid-thigh), not 1.32x (cut at the ankles).** Closer rolls 1.3x.
- **Hair at the frame edge is in the SOURCE on 9 rolls** (5 to 15 px). Reported to Dan; no crop can fix it.
- **Side cards do not clear on medium or close rolls shot centred at 1080p** (no pixels to slide the crop into, no wall to
  stretch). Only the wide roll took the 3A card; the rest became lower thirds whose parts land on the words.
- **Framing solved for the whole film** (`build.all_segments`, W or T per shot): jump at a real join 10, lower third on a
  W shot 1 (the strip sits on the equipment at his feet), no change at a reframe cut 0.6, side list forces W.
- **The fact card cannot count a dollar figure** ("the counted number must start headline part 0"): no `count` on prices.
  Eyebrow fits about 19 characters. Its photo box is near square: crop the product to about 0.89 w/h first.
- **Library clip A0139 (powerlifter deadlift) has another video's caption and "*AI Generated" burned in.** Not reusable.
- A case-insensitive volume: a file named `LOOK` collides with the `look/` folder.
