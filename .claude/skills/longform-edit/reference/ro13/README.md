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

## Round 2 (full film, 2026-10-04, Claude Opus 5.5 session on Sonnet 5.5): delivered, independent review SHIP on candidate 2

Order: Veo first/last frame (`ai-clip-ideas/reference/gen-veo-keyframes.js`, A 4 s, B 8 s, no audio, ~$1.80) -> A01/A02 become
`kind="clip"` with `label="AI-GENERATED"` -> `resolve.py` -> `from_plan.py --render` -> `dupscan.py` -> `build.render_range(0, 430.63)`
-> `finish_chain.sh` -> reviewer -> `watch.py --judge` -> delivery gate (24 min) -> deliver.

Traps this round paid for:
- **Shared HyperFrames code moved under the locked renders.** Template commits (10-01) and a working-tree change (10-04, side-list
  default `drift` -6 to 0, edited by another session) made `from_plan.py` re-render G01 to G25. The 16:9 output of the committed
  templates is unchanged (G01 identical to the approved first minute), but the side lists would have lost their approved -6 px drift.
  Pin `drift=-6` on every `l3` item in `plan.py`; `hf/manifest.json` stays byte-identical to the approved hash.
- **The first-minute EQ fit fails the tone row on the whole film** (max 3.01 dB, limit 2.5). Refit with the chain's own fitter on
  the whole film's untreated voice (`round2/fitfull/eq_full.txt`, + 0.9 dB at 150 Hz): mean 0.88, max 1.79. `build.py` uses it by default.
- **The belly rule (VIDEO-RULES 10-04, written minutes after Dan approved the frames):** clip B's first 3 s are a bare belly under a
  lifted shirt in the first 30 s. Review 1 said DOES NOT SHIP. The fix was in the plan only: the clip starts at 3.5 s of its take
  ("standing in the mirror", clothed, hands to the sink) and the presenter covers 16.6 to 20.4.
- **Generated clips carry 4 black rows top and bottom** (Veo 1080p output). Crop 1920x1072 from y=4 and scale before a rebuild.
- The pair images in `watch/strips` need verdicts too, or `watch:pass` reads `inspected` false.
- `build.py` now seeks 0.4 frame early (RO-10 repeated-frame fix) and the segment cache key carries `seek04`; `dupscan.py` lists none.
- Delivery gate needs `banned_source` (the RO-10 line) and a `negative_events_scan.json` beside the master (the editor's own
  scan of the sheets, re-hashed to the final file).
