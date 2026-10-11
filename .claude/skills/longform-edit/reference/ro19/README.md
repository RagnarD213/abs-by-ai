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
- **A wet room does not mean the dereverb wins.** This roll measures 72 to 85 ms early decay, the same kitchen as RO-20, and
  nine blind trials still put the untreated lav first (6.8) and both light-dereverb versions last (3.5, 3.4). Run the
  trials per roll; do not carry another roll's voice pick over. The audio gate then fails the room and tone rows on the
  untreated voice: report it, give Dan both by ear.
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
