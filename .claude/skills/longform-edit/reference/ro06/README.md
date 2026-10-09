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

Round 2 (2026-10-08, Dan's first-minute notes: open tight, tight as the default, wide to establish and now and then):
- **Three sizes, solved for the whole film** (`build.all_segments`): X tight (hair to just below the shorts, about 2x on the
  1080p wide rolls), T medium (1.5x), W camera frame. A real join needs sizes at least 1.2x apart, so the medium is what sits
  between two tight shots. Run `build.py segs 80` to read the solution, the jumps and the longest holds.
- **A run of one take at one size must share ONE crop.** Each shot's crop is centred on its own median head position, so two
  adjoining shots at the same size differ by a few pixels and the picture shifts at a cut that is not meant to be a cut.
- **A picture-only split moves the audio by one sample** (each shot is placed at its own rounded sample position).
  `split_shot.py` marks the new shot `split_of`; `voice_shots()` merges it back, and the voice track stayed bit-identical to
  the approved round. Prove it: md5 of the two untreated WAVs, then of both delivered files' decoded audio.
- **The lower third and the wide shot cannot share the screen here**: the strip lands exactly on the equipment at his feet.
  The wide took the "$58" sentence with no graphic and the lower third moved one sentence later, onto the tight shot.
- **The per-shot `active` flag misses a one-second lean.** He bends and points at the equipment inside otherwise still shots
  (61 s, 70 s). In the tight size that reads as him falling out of frame. Found by eye on the camera frame; those sentences
  go medium or wide. Scan every tight segment for head drop and sideways travel before a full render.
- **A split where a full-screen clip starts inside a shot** (segment key `shot+c`) lets the picture come back at another size
  after the clip for free.
- The tight size is an enlargement: sharpening 0.9 (medium keeps 0.5). Show Dan same-size crops and say what he trades.
- The review page for a first-minute-only round: `page2.py` (stills pulled from the rendered file, "Play from here" buttons
  that seek the one docked player).

Round 3 (2026-10-08, Dan's notes on the round 2 first minute: jump rope swap, panning equipment shot, frames for four AI clips):
- **Judge "fast" by measuring the roll, not by the clip's catalog line.** Head height per frame against a median plate of
  the locked-off roll gives jumps per second: C1674's both-feet stretch is 95 a minute with a pause on each landing, the
  alternating-feet stretch is the beginner demo Dan rejected, the high-knee stretch is 155 a minute and steady for 12 s.
  The driveway clip B0004 is fast but its picture is 640x720 inside a 1280x720 frame: unusable full screen.
- **A pan made by sliding a crop needs shutter blur.** At 560 px a second, 30 fps steps of 18 px strobe. `c02_pan.py`
  averages 8 sub-frame positions across half a frame, on a float x, with a steady middle and soft ends.
- **Topaz video upscale on Replicate** (`topazlabs/video-upscale`, 4k): send the clip inline as a `data:video/mp4;base64`
  input. A Replicate files-API URL fails with "source.container is required". 3 s cost $0.24 and was clearly sharper than
  lanczos at 2.25x (comparison in `round3/c02/`). Its output is 30 fps: read the same number of frames, do not retime.
- **A piece wholly hidden under a full-screen clip must not move the crop of the pieces you see.** Adding clips inside a
  shot creates hidden `shot+c` pieces that join the neighbouring run and shifted its shared crop by 2 px. `all_segments()`
  now weights the run's crop by visible frames only. Prove an approved first minute is untouched: compare crop and source
  frame for every visible presenter frame against the previous round's `build.json` (expect 0 differences).
- **AI frame placeholders:** a `clip` item with `frames=[start, end]`, `pending=True`, `label="AI-GENERATED"` and no `src`.
  `build.ai_placeholder` shows START for the first half of the slot and END for the second, labelled.
- **Codex frame pairs:** make a character sheet and a room picture first, then every START frame from those, then each END
  frame as an edit of its own START ("keep everything identical, change only..."). Say which side of the picture a moving
  arm finishes on, and restate the haircut: both went wrong once. Prompts: `ai-frame-prompts/`.

Round 4 (2026-10-08, AI motion for the four approved frame pairs, lip sync on two, first minute rebuilt):
- **Motion:** `gen_motion.py <ID> <tag>` (Veo 3.1 Fast on Replicate, image + last_frame, 1080p, no audio, $0.10 a second). It hashes the
  frames against `round4-plan/decisions.json` and scales 1672x941 to 1920x1080 first. All four worked on the first take. Prompts:
  `ai-motion-prompts/`. Read a take with `clipsheet.py` (numbered frames, optional crop) before trimming.
- **An END frame drawn "a split second after the hit" puts the hit at the END of a plain take**, which leaves no aftermath for the
  slot. Veo answered the "almost at once" prompt with TWO slaps (contact at clip frames 23 and 45), then a recovery into the end
  pose. The second, harder one filled the slot: `late=0.312` on the plan item (new in `resolve.py`) starts the clip a beat after its
  phrase so it opens on the wind-up and the hit still lands on the word. The 9 extra presenter frames are the same shot and crop.
  For a hit that must land early in its slot, draw the END frame as the aftermath a second or two later, not the instant after.
- **sync/lipsync-2-pro with `active_speaker` on also moved the TRAINER's mouth** (A1, last 0.8 s). `lipsync.py` trims the take to the
  slot at 24 fps, cuts the slot's audio from the untreated voice track on the build's own output frames, and syncs. `syncfix.py` then
  keeps the synced picture inside a soft box round the client's face and the untouched take everywhere else. `syncdiff.py` proves
  it (trainer's face 0.2 levels from the take, client's face equal to the sync). Send the slot-length trim, not the whole take: it
  bills per second ($0.083).
- **Merge on the raw YUV planes.** A decode to RGB and back darkened the whole clip by 1.9 levels; ffmpeg 6.0's `maskedmerge` has no
  `shortest` and crashed on a looped mask.
- **Check lips on the closing sounds.** `qc/lipsync_closures.jpg` pulls the client's mouth from the FINISHED file at each m and b.
  Gemini cannot judge lip sync (it samples one frame a second; it called this sync unconvincing while every m closed on time), and
  `gemini-2.5-pro` is retired: `GM=gemini-3.1-pro-preview gemini_listen.py`.
- A Veo take is 24 fps and untagged BT.709; the builder's `fps=30000/1001` duplicates frames (no retime). A first-minute build with
  AI clips: `build.py range 0.0 62.9963`, both audio md5s unchanged, 1,204 presenter frames with 0 differences. Page: `page4.py`.
- **Dan approved all four clips and the first minute as built (2026-10-08):** "I really love the way that you did the lip-syncing and the slap. Both of those
  turned out significantly better than I expected." This method is now the standard for excuse-voice lines (VIDEO-RULES, top section).

Round 5 (2026-10-08, the full film: three length trims, a music bed, two phone demos, three full renders, two independent reviews):
- **A length trim needs no new ASR pass.** `words_out5.py`: a word in a shot whose source range did not change keeps its old output time plus that
  shot's shift, so every word before the first trim is identical to the approved round; words in changed shots are remapped from source time and kept
  only when their middle survives. Re-run `shots.py`, then put the picture-only splits back from the old `shots.json` (it rebuilds the list).
- **Pin the approved first minute twice: sizes AND crops.** The solve is global and a run of one take shares one crop, so setting a later shot to medium
  moved an approved shot's crop for 121 frames. `OVERRIDE` pins the sizes, `PINCROP` the crops (from the approved file's `build.json`). Proof: crop and source
  frame per presenter frame (0 differences), untreated voice sample for sample, and PSNR of every frame against the approved file (all above 40 dB).
- **After a reviewed render, pin EVERYTHING to it.** Adding eight cutaways and moving ten lower thirds re-ran the solve and flipped 17 shots (one back into
  a lean). `_R2` in `build.py` holds every shot at the reviewed render's size and crop; only the named changes move. Compare the solve with the last
  `build.json` before every render.
- **Pre-flight every clip against its slot before a full render** (the loop is in `render5.py`'s neighbours: duration minus start against slot frames). One
  B-roll clip 0.9 s shorter than its slot killed an 18 minute render at minute 11; the fault had sat in the plan since round 1 because only the first minute
  had ever been rendered.
- **`leanscan.py`** reads the 2-per-second masks framing.py already made and flags, per tight or medium shot, a head drop over 90 px, sideways travel over
  17 % or hair within 10 px of the top. Bends to the equipment go medium, never tight. Then check every lower third against the same flags: six of them
  came up exactly as he bent down, so the strip sat over his head (the graphics checker caught one of six, because a bent head has no face box). Start
  those on the word he says once he is standing, and re-check the solve (a lower third that covers under 45 % of a shot no longer counts in it).
- **Lower third timing rules that two reviews wanted:** the body fills within about 2 s of the strip appearing (start the item on a phrase about 1.3 s before
  its first part), and the last part stays up at least 1.5 s (`tail=`). Scan both from `hf/beats.json` before rendering.
- **The lower-third template sets a later part too close to the one before** (7 to 12 px where a word space is 15 to 19): "RecommendIs". Worked around here
  by making mid-sentence lower thirds single-part; the template fault is its own task. A leading no-break space is refused by the template.
- **The camera operator re-aims inside takes on this shoot** (a 166 px pan, a 134 px tilt). `stab.py` measures the background's travel per frame (LK on
  background corners, his column and the water masked) against where the camera settles; `build.render_seg_stab` slides the crop by it. The wide has no room
  to slide, so that shot goes medium. Residual after: under 20 px. Both reviewers found the moves; the build's own checks did not.
- **Phone demos (`phone_demo.py`):** the approved self-generation demo is lifted out of its olive card (display rect measured from the white UI frames, corners
  squared by extending each row) into the approved iPhone shell on the Soft Blue field; the status area takes the page's own top-corner colour. Labels drawn
  inside a clip get `label_in_picture=True` so the builder adds no second chip, and `finish5.py` takes the chip reference from the delivered pixels.
- **Price-card chips drawn by HyperFrames match the PIL chip at 0.83** (other font rendering), under the gate's 0.85. Their own rendered pixels are the reference.
- **Music bed outdoors:** the lav carries pool and insect noise about 40 dB under the voice, so a bed at RO-12's level cannot be heard. `--bed-db -15` on a
  bed with 10 dB of headroom lifts the pauses 3 to 4 dB over that noise and still passes the floor row (0.1, -1.0, 1.1 against -3.0).
- **The audio gate's fixed 20 to 140 s window fails tone on this film (5.5 kHz +6.1) with the chain Dan approved on the first minute.** Not the bed (same
  result without it). Measured per roll with the gate's own bands the 5.5 kHz reading runs from -5 to +6.8 and follows what he is doing in the stretch as much
  as the roll, so a per-roll correction would be fitting noise. Left as approved and reported; a 4 dB treble shelf passes the row and is offered as an A/B.
- **Edit sheet:** the writer now reads a multi-roll build. Plan items need `people` and `physique`; real MOVING footage of Dan is `physique=False` (no label
  applies to it), price cards and equipment shots are `people="none"`.
- **Chapters:** anchor on the section's first sentence, not where its lower third comes up, and keep them 10 s apart or more.
- **Watch pass after a re-render:** compare every frame with the judged render (downscaled, PSNR); a cut strip whose frames are unchanged keeps its verdict
  and only the changed ones go to a fresh judge. Keep the judged render's 540p copy and never delete `watch/` while a judge is still working in it.
