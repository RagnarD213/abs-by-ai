# RO-19 "My First Spray Tan" (8/3 kitchen doorway roll C1512): round 1 recipe (Claude Opus 5.5, 2026-10-11)

One 30:42 talk roll, re-edited from scratch on the round method. Starts from the RO-20 recipe (same shoot, same kitchen:
copy `/Volumes/Extreme/_edit_work/ro20/recipe/` or the ro06 + ro07 references in that order, then this folder). Only the files
that differ are kept here. Work dir and media: `/Volumes/Extreme/_edit_work/ro19/` (never commit media; the repo is public).
Round 1 page: `round1/index.html`, port 8863.

Order: `pick_lav.py` -> `asr_rolls.py` (medium.en) -> `mkglobal.py` (+ `word_patches.json`) -> `edl.py` -> `shots.py` ->
`words_src_out.py` (read the WHOLE repeat list) -> `framing.py` -> `grade20.py masks | stats` -> `lookstills20.py` ->
`audio_options20.py` + `listen_trials.py` -> plan parts (`PLAN_BRIEF.md`, one writer per part) -> `resolve.py` ->
`dupscan20.py` -> `pairs.py` -> `hyperframes/from_plan.py --render` -> `build.py filmvoice` -> `round1.py first` ->
`stills20.py` -> `pagecopy19.py` -> `page20.py` -> `review_server.py 8863 round1` -> `round1.py context` (`chain19c.sh`).

What is new here:
- `pairs.py`: Dan's real before / after photos as a Soft Blue scene (two 4:5 cards, a caption tab under each, one plural
  disclosure under both), three portraits, or one photo. A plan clip carries `pair=[before, after]` (+ `reveal="phrase"`,
  the after card comes up on that phrase), `portraits=[...]` or `photo=...`; its `src` is `gfx/<id>.mp4`. Photo crops are made
  once with the person mask: head to 85 % of the visible body, 4:5, centred on the body. `softblue.unit(1920, 1080)` is 2.0:
  lay scenes out in fractions of w and h, not in "units".
- `resolve.py`: an item with `anywhere=True` is found by its own words anywhere in the film and does not move the search
  cursor, so the lead editor's reserved items (AI clips, photo scenes, the close) live in one file (`p90_lead.py`) while
  the part writers work in film order.
- `shots.py`: a wordless sliver under 1 s between two long pauses (a breath, a rustle) is dropped, not kept as a shot.
- `words_src_out.py`: a piece's first word whose Whisper start sits in the pause before it is kept when it is still
  spoken after the in point (11 pieces lost their first word to the midpoint rule).

Traps this build paid for:
- **The round 1 voice bake-off was VOID: the audition window was 27 s of silence.** `audio_options20.py` took a typed
  roll time (166 s) that sat in the gap between two takes; nine blind trials ranked room tone, the untreated lav "won",
  and the first minute was built on it. Dan caught it by ear. Take the window from a kept piece's own start, measure it
  (speech in the first 0.5 s, no pause over 1.5 s) and listen to it before any trial. Nothing about this roll's voice was
  learned in round 1. VIDEO-RULES, "Audio comparison clips start on speech".
- **`offset()` can swallow the next word's onset** when Whisper butts two words together (the hi clamp is next start +
  0.25 s). Two cut-outs caught "if" and "from". Print the 20 ms envelope past every out point whose next word starts
  within 0.1 s and set the out by hand (8th field).
- **`onset()` trusts a word time that can be seconds early.** "Alright," was placed 3.6 s before it is spoken and the in
  point landed in silence. After `edl.py`, print the envelope around every in point; force with `"ONSET:a:b"`.
- **The 4-word repeat scan found a whole retake the take map missed** ("from what my tanning specialist told me...", said
  twice). Read every line of the scan, not its head and tail. A plan writer caught it, not the lead.
- **Two photos from one pose on one day read as the same photo.** The single "pale" photo at 0:48 was a second double
  biceps from the same shoot as the opening pair. Give each photo scene a different pose.
- **Codex refuses a man in briefs** (moderation: sexual). Swim shorts pass. Same scene otherwise.
- **Pexels has no footage of a spray tan being applied** (every hit is sunscreen or sunbathing). It needs an AI clip.
- **The Pexels index cannot be POSTed from pexels.com to localhost** (blocked). Put the text in `window.name`, navigate
  the tab to the receiver (`px_recv.py`, port 8871) and POST from there.
- **The outside reviewer invented jump cuts and a repeated phrase** in the first minute (nine "same size" jumps that are
  one continuous take, and "but the, but the"). Check each claim against `build.py segs` and a `verify_asr.py` window
  before acting on it.
- **Hair:** the camera frames his hair at the top edge all roll and cuts it slightly in the opening take. Both sizes keep
  row 0. Reported to Dan, not fixable by a crop.
- The machine was shared with the RO-20 chain (two workers). This build ran one worker at `nice -n 10` and said so.

## Round 2 (2026-10-11, Dan's round 1 notes): what was added

Page: `round2/index.html`, port 8865. Order: `audio_options19r2.py warm`, then `bass <best warm key>` -> `listen_trials19r2.py check`, then `5` ->
`photocrop.py` -> `PAIRS_OUT=gfx/r2 pairs.py P02 P03 P04 P05` -> `gen_motion.py <ID> <ID>-t1` (prompts in `motion-prompts/`) ->
`build.py filmvoice` -> `round2.py first`, `context IDS`, `stills` -> `headroom.py` -> `page19r2.py` -> `review_server.py 8865 round2`.

- **The pale shoot is 1 April 2026 in Dan's Photos library: 96 pictures of him, not four.** Round 1 took the four the old edit had and could not
  match poses. Query the library copy for that date (`ZASSET`, 14:49 to 15:00), read the 1024 px derivatives for a contact sheet, export the
  originals with `sips`, then `ImageOps.exif_transpose` (sips keeps the rotation tag, so the pixels come out sideways without it).
- **A pair is the same pose at the same body size.** `photocrop.py`: head top from the person mask, one landmark row read off a ruled close-up
  (the navel on front poses, the waistband on a side pose), and both cards are cropped so head-to-landmark is the same fraction of the card.
  The automatic waistband search (first non-skin run down the torso) was fooled by his forearms on the side pose: read the row by eye.
- **No hands-on-hips picture exists in the pale shoot.** A third pair would not have been the same pose, so it was not offered.
- **Pin the framing solve before any plan change** (`round2-plan/segs.round1.json`, `build._PIN`): removing one clip and moving one clip's start
  changed nothing else because every shot kept its round 1 size and crop. The only named change is `intro.0r0` to W.
- **Never render into a reviewed file.** Round 2 photo scenes go to `gfx/r2/` (`PAIRS_OUT`), the film voice to `voice/film_voice_r2.wav`.
- **Veo with a start and end frame that differ a lot fades the difference in.** A3's body print faded in on a bare sheet half a second after the
  duvet came back. Fix without a new take: play the start (asleep), hard cut on a word ("sheets") to the part where the print is already there.
  A1's change of pose came as a half second dissolve inside the mist, which reads as part of the gag.
- **Voice options, measured on the audition window:** alpha 0.40 / floor -12 measured flux 1.11x the reference (limit 1.10), so W3 is
  alpha 0.35 / floor -11. A deeper 450 Hz dip (W4) measured the driest inside the limits. On the first minute itself W4 still fails the gate's
  tone row (any fixed warm EQ does) and the damage row by a hair (0.083 against 0.080; untreated 0.079 there). Five blind trials did not
  separate eight options (five different winners). Dan picks by ear.
- **`gemini_listen.py` defaults to a retired model**: set `GM=gemini-3.1-pro-preview`.
- **Library clip B0437 was in the round 1 plan** (Cb02) and Dan banned it the same day on RO-20. Check a plan against VIDEO-RULES' never-use
  clips before every page, not only when the plan is written.
- **Headroom proof flaws seen in look F:** the wide shot's hair cap is flat on some frames, and a thin dark line runs from his hair to the top
  edge on a few frames. Both need fixing before it could run on the film.

## Round 3 (2026-10-12, Dan's round 2 notes, then the full film): what was added

Page: `round3/index.html`, port 8866. Order: re-hash rounds 1 and 2 -> `build.VOICE4` + `FILM_VOICE` (voice B2, new file) -> `gen_motion19r3.py A5|G1|G3 <ID>-t1` ->
Photos export + `photocrop19r3.py` -> `PAIRS_OUT=gfx/r3 pairs.py P02 P04` -> `phone_side19.py` -> `plan_patch_r3.py` (never `resolve.py`: the plan is hand-patched) ->
B-roll stills beside presenter frames (`round3/broll/`) -> `round3_19.py bed | first | film` -> `finish_chain19r3.sh` -> `scene_check19.py` -> `ra-reviewer` ->
edit sheet -> delivery gate -> `page19r3.py` -> `review_server.py 8866 round3`.

- **A phrase anchor that is said twice cut a sentence in half, and two rounds did not catch it.** edl piece `pros` ended on "goes out in the sun.", which Dan says
  twice in one sentence; the first match ended the piece 7.2 s early ("he only goes out in the sun" / "sun exposure is ..."). Found only while proofreading the full
  film's captions. Check after `edl.py`: every piece's `heard` must END on the last words of its own `text` line (a ten line script; it flags ASR spellings too, read
  them). The fix moved everything after 10:23 later by 215 frames: `round3-plan/timeline_shift.json`, applied to shots, words, the plan and the lower third manifest
  by `plan_patch_r3.py` (rendered lower thirds are timed from their own start, so only their start and end move).
- **Whisper can end a word half a second late.** "sun." ended at 960.82 in the word list and at 960.33 on the lav. Read the envelope at a piece's out, set it by hand
  (8th field) when the gap is over 0.3 s.
- **The full-size original of a Photos picture may be in iCloud only.** `originals/` had 9 of 18 driveway frames; the others had a 1536 px or only a 768 px
  derivative. `osascript`: `tell application "Photos" to export {media item id "<UUID>/L0/001"} to <folder> with using originals` downloads and writes the HEIC
  (then `sips` to JPEG and `exif_transpose`). No window comes to the front.
- **A filtered copy in Photos is a 1:1 crop of the frame taken the same second.** Template-match the copy inside the full frame (0.998 at one offset), then reuse the
  approved crop box shifted by that offset: the new card is the same framing with the tint gone, so the pair needs no new body-scale work.
- **Veo with a morning start frame and an evening end frame jumps the light in one frame** (G1, frame 49 of 144), with the clock hands blurred through it. Prompted as
  a time-lapse it reads as one. Veo also moved a held object to the other hand when the start and end frames disagree about which hand holds it (G3's mitt, six
  frames). Look at which hand holds what in BOTH frames before asking for frames.
- **The app tour follows the words of the film it is in.** RO-06 said calorie tracking, then workouts; this film says trainer, then nutritionist, so the screens run
  workouts first. `phone_side19.py` measures his widest reach over the whole span with the person mask (x 300 to 1620) and picks the shift (270 px) from it. The
  calorie recording B0038 sits still from frame 102 to 260: show a tap on Log Meal and jump to frame 262 instead of holding a still screen for four seconds.
- **B-roll against the presenter: measure his skin, not the frame.** Frame median luma flagged dark backgrounds that are fine (money on black, a spray can) and
  missed nothing, but the number to match is his skin (0.43 in the presenter picture; five of his own clips read 0.27 to 0.35). `build.lift()` raises luma by a gamma
  with the colour ratios held. Look at the before and after sheet.
- **The first minute's audio gate is not the film's.** On the first minute B2 fails tone and the processing row by a hair (0.082 against 0.079); on the whole film
  only tone fails. Gate the film, report both.
- **Never move a build folder while a chain is still writing into it.** The hair and graphics checks of the first render were lost that way.
- **Three renders, three independent reviews (2026-10-12).** Final master sha256 `2031c3e3...880d`, 18:48.56, `round3/film/`. Order that worked: render ->
  `finish_chain19r3.sh` -> `ra-reviewer` on the whole film (666 images) -> fix everything in ONE render -> `carry19r3.py` (frame PSNR against the judged render;
  only changed frames go to a fresh judge: 80, then 13) -> a fresh `ra-reviewer` on the changed parts -> merge findings -> `watch.py --judge` -> edit sheet -> gate.
- **What the first review caught that the editor had not:** a stock clip whose own glitch effect (vertical roll, tearing) sat inside the chosen window (Cd10 from
  7.0 s; clean from 1.0 to 4.2 s), and lower thirds across stock faces. Contact-sheet every stock clip over the EXACT window used, and run
  `hyperframes/checks.py` on a render BEFORE the review: it flags any face under a strip, stock people included (`min_face_gap`).
- **A size change can put his chin under a lower third.** Breaking a 54 s wide hold, the first two shots tried at the closer size both failed the face check: he
  bends down in them. Test a size change on a 30 s `render_range(..., audio=False)` plus `checks.py --film-t0` before the full render (2 minutes, not 90).
- **The sheet writer reads `hf/manifest.json`, `hf/beats.json` and the lower third configs as they are.** After a timeline shift, hand it a shadow build folder
  (`round3/sheetbuild/`: symlinks plus the shifted manifest, beats and configs) or the sheet carries the old times.
- **The bed at the chain's -30 dB is close to inaudible on this roll** (the side channel reads -54 dB in the pauses) and the audio gate's floor row has only about
  1 dB to spare at one band. Say so on the page. Louder is Dan's call and fails that row.
- **Gate on the delivered file: 32 pass, 7 fail** (tone stamp, hair x2 by Dan's call, the burned-caption false alarm from lower thirds, coverage 32 %, three take
  joins a hair over the splice ceiling, one false start at 2:53 left in). Reported on the page, nothing tuned.
- Do not edit `plan_resolved.json` on disk while a reviewer is reading it for an older render; write the next plan to a side file until the render starts.
