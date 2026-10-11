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
