# Handoff: HyperFrames pilot, one graphic rebuilt in Soft Blue Light (2026-09-30)

**Goal.** Prove HyperFrames as our motion-graphics layer by rebuilding ONE approved graphic, the C1652 R4
"downward spiral" cycle diagram (4:32 to 4:46 in the approved film), as a Soft Blue Light transparent overlay, composited
on the real footage, shown to Dan beside the current version. Nothing is published; no existing master is touched.

**Background.** `Docs/HYPERFRAMES_RESEARCH.md` (read section 1, 5, 6 first). Dan wants motion graphics at Nate
Herk's level in sales videos, ads, content videos and Shorts. Decision: HyperFrames as the graphics layer only; cut,
audio chain, gates and delivery unchanged; Soft Blue Light stays the locked style
(`.claude/skills/_shared/GRAPHICS-STANDARDS.md`, `SOFTBLUE.md`, `softblue.py`).

**Facts the session needs.**
- Node 24 is installed (`node --version`). ffmpeg/ffprobe live at `Media/video_edit/bin/`; put that directory on
  PATH for the session or symlink into `/usr/local/bin` (HyperFrames looks for `ffmpeg` on PATH). Chrome downloads itself.
- Install: `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes`.
  Pin the npm version in the test project's package.json (whatever is current that day; record it in the README).
- Docs: https://hyperframes.heygen.com (quickstart, rendering, CLI, motion-graphics guide, performance,
  troubleshooting). Transparent export: leave the background unpainted, `npx hyperframes render --format mov`
  (ProRes 4444). Checks before every render: `npx hyperframes lint`, `npx hyperframes check`,
  `npx hyperframes snapshot --at ...`.
- Source film and timing: `Media/codex-video-trial/06-organic-r4/C1652_FINAL_APPROVED.mp4`; graphic entries g26
  (`cycle`, 272.04 to 286.09 s, "The downward spiral") and g27 (289.39 to 297.20 s, "Turn the spiral around") in
  that folder's `graphics.json`; word timings in `mapped-words.json`. Frames of the current version:
  session scratchpad; regenerate with ffmpeg at 272 to 286 s.
- Nate's design rules to fold in (his MOTION_PHILOSOPHY.md, https://github.com/nateherkai/hyperframes-student-kit):
  light over colour, something always drifting, arrows draw themselves, cards settle with `back.out(1.2 to 1.5)`,
  enter `power2.out` 0.2 to 0.5 s, exit `power2.in`, word reveals `expo.out` with 0.35 s stagger, one hue per
  meaning (red = the spiral down, teal/blue = the turn around), a one-second rest beat. Motion quiet, per Soft Blue Light.

**Steps.**
1. Install the plugin, create `Media/hyperframes/pilot-c1652-spiral/` with `npx hyperframes init`, render the
   built-in demo to prove the chain (draft quality). Write `Media/hyperframes/README.md`: version pinned, PATH note,
   the commands, what worked.
2. Plan before code: a beat sheet for g26 and g27 anchored to the words in `mapped-words.json` (which word triggers
   each box, each arrow, the loop close, the reversal). Keep the approved copy and the four items exactly.
3. Build the two scenes in one HTML file each, 1920x1080, Soft Blue Light geometry and colours ported from
   `softblue.py` (field, glass, type, GOOD/BAD colours). Arrows draw along their path; boxes spring-settle; the loop
   pulses once when closed; the second scene reverses direction and flips red to teal. `lint` and `check` clean.
4. Render both as ProRes 4444 MOV, composite onto the caption-free base for 272 to 297 s with ffmpeg (same overlay
   pattern as motionlib), and build a review page in the RO-16 format (`Docs` pointer: memory
   `review-page-what-i-decided`): current version and new version side by side, moving, plus stills, plus a
   "What I decided" list. Render time and token use recorded.
5. Stop and show Dan. Do not touch the C1652 master, do not publish, do not build more graphics until he approves.
6. On approval: save the graphic as a reusable template under `.claude/skills/_shared/hyperframes/` with a README
   (how to call it, which words drive it, the easing values), and add a short "HyperFrames" section to
   `SOFTBLUE.md` pointing there. Then write the next handoff: lower third and before card as templates.

**Spend.** No dollars. Tokens only; keep effort at high, never above.

**Board.** Add an ACTIVE entry when starting; delete this handoff's rows in `Handoffs/README.md` and
`AI_COORDINATION.md` when done; no dashboard row unless Dan asks.

---

**Starter prompt (paste into a new Claude Code session, Opus 5.5, effort high):**

Read and execute `Handoffs/handoff-20260930-hyperframes-pilot.md`. Install the HyperFrames Claude Code plugin,
pin the version, prove the render chain with the built-in demo, then rebuild the C1652 "downward spiral" and "turn the
spiral around" graphics as Soft Blue Light transparent overlays with real motion (arrows drawing, cards settling,
loop pulsing, reversal), composited on the real footage, and show me old and new side by side on a review page with
a "What I decided" list. Graphics layer only; do not touch the C1652 master or publish anything. Stop for my review
before building anything else.
