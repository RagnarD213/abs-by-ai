# `softblue-sl36/`: SL-36 Man Boobs shorts, R2 first vertical review (2026-11-18)

Three Shorts from RO-31 "How To Get Rid Of Man Boobs" (Claude film, roll C1775, 10/15 studio), built from `softblue-sl21/` (read its
README first). First batch under Dan's 2026-11-16 rule: no horizontal previews, the first review is the actual 1080x1920 drafts plus
colour and voice choices. Work folder `/Users/danrrose/Projects/_edit_work/SL-36/round2/` (M6 internal; sources fetched from the M2
with `editroute.py fetch`). Order: `snap.py` -> `batch.py audio, words, plan, track, plan, cues` -> `chain_r2a.sh` (gfx, colour stills,
proofs) -> look at the proofs -> `chain_r2b.sh` (renders) -> `checks_r2.py`, `haircheck_v.py S`, `joinsheet.py` -> `page_r2.py` ->
`_shared/review_server.py PORT round2/review`. Run chains as ONE queued step: `stallwatch.py run SL-36 -- renderq.py run --group SL-36 -- bash chain.sh`.

## What is different from SL-21
- **Picture source:** RO-31's graphics-free `round3/final/base.mp4` (the gate plan's `source_picture`, 6963 frames like master bce049d0).
  Picture cuts come from `RO31_MASTER.mp4.build.json` `segments[].o0` (output frames). `scan.py` reports them one frame early on some
  windows (its seek rounding); an exact `select` decode confirmed every listed cut frame.
- **Every talk-to-talk cut is the film's own W2/T2 camera change** (a native 1.3x step), so `plans.FULL_ALL` keeps every talking shot in
  the full window (no mid punch-ins).
- **Colour options:** `batch.look()` applies L2 (warmer, +18 % saturation) or L3 (gamma 0.86, S-curve) to the talking picture only, via
  `SL36_LOOK`; `colour_stills.py` renders matching frames. Drafts render L1 (the parent look).
- **Voice options:** one 14 s passage; V1 = the film mix verbatim, V2/V3 rebuilt from the untreated film voice with the film's EQ chain
  changed, level matched (the rebuild of V1 correlates 0.998 with the film mix, lag 239 samples = the film limiter's delay).
- **Diagram panels:** the film's two-panel chest diagram (HyperFrames render, 1920x1080) shows one panel at a time with `fit="box"` and
  an ffmpeg `pre` crop (`crop=880:875:50:140` left, `990:140` right), box (0, 330, 1080, 1074) above the captions.
- **Before/after:** the film's pair becomes two `photo1` scenes in sequence. Only the first photo of a run rises in (`t=0.45`); the next
  ones start at `t=1.0`, or every photo opens on dim fading frames.
- **Vertical key-point bars re-flow both parts as one paragraph** about 26 characters wide: a first line that is too wide pushes words
  of line 1 into line 2 ("Push-Ups And Chest / Flies Plus Fewer Calories"). Keep each part short and check the proof.
- **A bar with `a=-0.2` shows its glass on the previous shot** when the landing word is under 0.2 s after a cut (SL-36 C 0:14.95, B
  fixed with `a=0.05`). Check every bar's start against the shot cuts.
- **C opens on "diet"** after the film's "Now,": the in-point sits in a 10 ms dip (-38 dB) before the plosive; `plans.FADEIN` uses a
  4 ms fade there instead of 15 ms.
- `hfbuild` needs node: on the M6 it is `~/.local/node/bin` (not on the batch session's PATH by default); the chains export it.
- Headless page check: `chrome-headless-shell` from `~/.cache/hyperframes/chrome/` with puppeteer-core from the hyperframes npm
  package, `--mute-audio`, `?review_mode=automation`, then `AbsReviewAudio.handoff()`.
