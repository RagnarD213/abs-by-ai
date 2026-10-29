# `softblue-sl10/`: SL-10 Alcohol And Abs shorts (R1, 2026-10-29)

Four Shorts from RO-13 "Can You Drink Alcohol And Still Have Abs?" (Claude's 4K film, one roll C1707 on the 9/23 studio set). The
`softblue-sl17/` renderer (read its README and `softblue-sl15/`) with the film's map built from RO-13 `shots.json` (frame map ->
`ro13_cut_map.json`) and the master's own mix as audio. Work folder `/Volumes/Expansion/_edit_work/SL-10/` (run from there; copies here).
Order: `snap.py` -> `fitgrade.py` (once) -> `batch.py audio, words, plan, track, plan, gfx, proof, render` -> `post.sh S` (deliver,
hair, cut scan, fresh watch pass, junk) -> fresh `ra-reviewer` per Short (`REVIEWER_BRIEF.md`) -> `rungate.sh S` -> `page_r1.py`.

## What this batch learned
- **The film's own grade chain is not the delivered look.** grade-C.cube on raw C1707 read +5.6 levels over the master; `fitgrade.py`
  fits per-channel curves on aligned talking frames (held-out mae 5.45 -> 2.91). Always measure against the master.
- **Bars: the slot must hold every frame of the render.** The compositor showed `fr(b) - fr(a)` frames and cut the 0.33 s power2.in
  exit at ~45 % (reviewer B r1). `cmd_gfx` now sets `b` from the render's frame count.
- **A bar wraps the whole joined point by width, not line by line.** "Zepbound Killed The Urge, / Not Willpower" broke inside line 1
  twice; keep line 1 + line 2 short enough that the break falls between them (check `hf/proj/<id>/index.html` and a settled frame).
- **Reviewers flagged every echo bar.** Distil: "Bitter Beats Sweet / Less Sugar Per Glass", "Bad Taste Is / A Built-In Brake",
  "Mixers Are / Liquid Dessert", "It Was Zepbound, / Not Willpower". Line 2 needs 1.5 s fully up before the exit and the next cut.
- **A piece that starts at a film join can carry the previous line's tail** (B: 90 ms of "evening" at -32 dB): start inside the
  film's measured silence, not at the snap's first silent sample.
- **Library card B0348/B0349/B0351 ("insulin injector pen") are glucose test kits.** No real injection-pen clip exists.
- **Fill crops on panning stock:** pick the in-point where the subject is sharp and in the window for the whole used range (cocktail
  rack-focus at ~4.5 s; sleeper's face at fx 0.92, not 0.66; nightstand at fx 0.95 keeps the clock and glass that carry the idea).
- **Cut a cover on the next caption's start**, never between a word's end and its cue's minimum hold (D: "protection rule." ran 0.4 s
  into the insert).
- A line that names "the list" or "this one" of the film is a reference back: cut it, and tell Dan on the page.
