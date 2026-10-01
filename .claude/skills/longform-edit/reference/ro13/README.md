# RO-13 "Can You Drink Alcohol And Still Have Abs?" (9/23 C1707): round 1 recipe (Claude Opus 5.5, 2026-10-01)

Third film on the approved HyperFrames templates. Starts from `../ro11/` (which starts from `../ro10/`); only the files
that differ are kept here. Work dir and media: `/Volumes/Extreme/_edit_work/ro13/`.

What changed from RO-11:
- `plan.py`: two `ai` slots, each with its own placeholder pair (`ph="A"` / `ph="B"` -> `aiframes/<ph>-start.png`, `-end.png`).
  `build.ai_placeholder` reads `it["ph"]`.
- `gfx.py`: section titles read `RULE n OF 6`. `scene: "portraits_codex"` reuses RO-16's approved three-photo panels
  (copy `ro16/assets/g03/` into the job's `assets/g03/`).
- `resolve.py`: a last pass keeps template overlays (lt, l3, cycle) off every full-screen item: a side card that starts
  inside one ends it on the card's cut; a lower third that starts inside one waits for it; either ends where the next begins.
- `stills.py`: the "after the last part lands" time looked for the words fades / gone / sweep / pulse anywhere in the beat
  text, so a fact card whose COPY contained "gone" was caught before its detail line. It now reads only the motion words
  after the quoted copy.
- `page.py` / `page_extra.py`: two AI clips in the frames section, five decisions, generic "flagged" line fed by
  `round1/flag_notes.json`.

Traps this build paid for:
- **A title phrase can match an earlier sentence.** "Rule number six" resolved to "keeps rule number 6 from falling apart"
  eleven seconds early. Anchor a title on enough words to be unique ("Rule number six. The next morning run").
- **A lower third whose first part lands late shows an empty strip.** "Number four ... (6 s) ... treats alcohol as a poison"
  put a topic-only strip on screen for six seconds. Start the lower third within about 3 s of its first part.
- **`pgrep -f <script>` in a wait loop matches the loop's own shell** (skill lesson 29, hit again). Wait on a marker in the
  job's output file instead.
- **Look at the stock frame the slot actually uses.** A "depressed man on bed" clip had a bottle and a blister pack of pills
  beside him; the wine pour opened on four seconds of white. Both were only visible on the stills.
- Dan re-read several lines differently from the prompter (30 restarts on a 14:29 roll). The Gemini verbatim listen is
  what found them; medium.en merged most into long words.
