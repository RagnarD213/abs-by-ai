# RO-31 "How To Get Rid Of Man Boobs" (10/15 C1775): round 1 recipe (Claude Opus 5.5, 2026-10-31)

Same 10/15 studio set as RO-28 and RO-29. Start from `../ro29/` (round 2 recipe) and `../ro28/`; only what differs is kept here. Work dir
`/Volumes/Expansion/_edit_work/RO-31/round1/`. One roll, 5:56 raw, cut to 3:52, 15 pieces. Never commit media.

## Traps this round paid for
1. **The sidecar's `small` transcript hides restarts.** It printed one clean line where he stopped and started again: On Zepbound (a whole sentence),
   "Then track" (a third read), "So don't assume". Run medium.en on the roll before writing the EDL, then read medium.en on the ASSEMBLED voice:
   three more surfaced there ("If you want a diag-", "The second step is", "Push-up"). The tell on the assembled words is one word over 1.5 s.
2. **Confirm a restart with a Gemini listen on 4 s clips** (`GM=gemini-3.1-pro-preview gemini_listen.py`; gemini-2.5-pro now returns 404). Whisper base and
   small both print the clean sentence. Use `recipe/env.py` level strips for the edges.
3. **Codex refuses anatomy of a chest.** "The image tool rejected the medical illustration request." Do not reword around it: the diagram is SVG inside a
   HyperFrames scene (`chest/`), no AI label, and every part can animate.
4. **A side view of a chest alone reads as a woman's breast**, twice, even shallow. Draw the whole man in profile (head, neck, stomach running on past the
   chest with no fold under it). An independent reviewer caught the second version; the eye of the person who drew it did not.
5. **`stills.py` opens `aiframes/<id>-start.png` for kind "ai"** through `ai_placeholder`; a blind-test round has no such files. Point stills at `review/aiframes/<id>/X1.jpg`.
6. **Blind pairs, START only:** `blind.py build` refuses a set with one source. An idea whose other frame was refused or failed twice goes on the page as a plain
   X1 copy. End frames wait for the pick, so the frame gate cannot run in round 1: one fresh frame-reviewer over all the start frames instead.
7. **`review/options/` must exist** before `colour_options.py`; its failure is silent inside the chain and the page breaks later.
8. **Probe a library clip against its slot before the chain** (A0050 is 3.06 s; the assert killed the context pass at item 15). `chain_r1.sh` reported CONTEXT done with only 15 of 39.
9. **Library clips carry readable gym names:** the 10/23 gym's wall logo and a Jacob's Ladder show in the front and side chest-fly clips (B0665 to B0667), and the camera moves, so a crop will not hold. B0668 (low angle) is clean.
10. **B0546 reads neon orange in low sun.** `eq=saturation=0.72:brightness=0.015,colorbalance=rm=-0.07:gm=-0.01:bm=0.03`.
11. **A0077's T-shirt vanishes after about 2.2 s.** Use only `max_len=2.1`.
12. **Side card over a take join:** cover the part before the join with a clip and start the card on the join (C08 then P01).
13. **Lower third hold:** measure 1.5 s after the LAST part lands, not after the first. `over_full=True` lets one ride onto the next clip.
14. **The board can be full of other sessions' entries.** It stood at 2,498 of 2,500 words; a three-word entry is what fit.
