# RO-16 round 2: opener motion, then the full film

**Job:** RO-16 "If I Had Belly Fat, Here's How I'd Lose It In 90 Days", organic long-form from 9/23 roll C1710.
**Written:** 2026-09-30 by Claude (Opus 5.5) at the end of round 1. Method: `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`
(organic decision budget), `.claude/skills/longform-edit/SKILL.md`.

## Read first
- `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `GRAPHICS-STANDARDS.md`, `CUT-CONTINUITY-QC.md`.
- Round 1 packet: `/Volumes/Extreme/_edit_work/ro16/round1/index.html` (serve with
  `cd /Volumes/Extreme/_edit_work/ro16/round1 && python3 -m http.server 8794 --bind 127.0.0.1`).
- Round 1 review: `/Volumes/Extreme/_edit_work/ro16/round1/REVIEW-round1.md` (two passes) and `round1/EDITOR-DISPOSITION.md`.
  Hashes: `round1/HASHES.json` (re-hash before touching anything). Phone copy + sheets on Drive (anyone with link):
  https://drive.google.com/open?id=1u6PAxdIKmNs2louFzWyp92GJFqwIPz6c
- Recipe copy in git: `.claude/skills/longform-edit/reference/ro16/` (the SSD copy is the working one).

## Recipe (all in `/Volumes/Extreme/_edit_work/ro16/recipe/`)
`edl.py` (38 pieces, take choices + why) -> `shots.py` (43 shots, pauses >= 0.70 s tightened, W2/T2 alternating) ->
`assemble_audio.py` + medium.en ASR -> `words_out.py` -> `plan.py` (every graphic/clip anchored to heard words) ->
`resolve.py` (times; snapping: full-screen items start on a cut up to 0.45 s before them, gaps < 0.8 s between full-screen
items close, side cards end on a join < 0.35 s before their end) -> `stills.py` / `build.py range <a> <b> <out>` (graded picture, paint, audio B chain,
frame-locked mux). `gfx.py` renders Soft Blue (pinned `softblue.py`), `frames.py` holds the locked look.

## Locked (reused, Dan-approved on WV-01, same set)
Colour C `wv01-edit/round2/recipe/grade-C.cube` (sha256 7c226895...), crops W2 3552x1998@144,162 and T2 2608x1466@616,184
(W3 3120x1755@360,172 only under side cards), audio B = voice_chain `--no-dereverb` + WV-01 EQ + 0.9 dB @150 Hz (the
-0.9 dB audition trim is NOT applied; chain targets -14 LUFS). No music (approved C1652 had none).

## Dan's decisions pending (round 1 asked 3)
1. Opener A (mirror, recommended; frames regenerated after review) / C (no AI opener). Concept B was dropped (identity drift).
2. First minute (0:00-1:15): approve or notes.
3. Step title cards: full-screen 2.4 s (as built) or lower-third headers.
Record his words in `round2-plan/decisions.json` with hashes before building.

## Next actions (round 2)
1. If A: generate motion with Veo 3.1 fast, start `aiframes/A-start.png`, end `A-end.png`, 6-8 s, locked camera, action in the
   packet. Check every frame (hands, mirror reflection, fog). Place it at A01 (0:00-7.05) with the AI-GENERATED chip. Update the
   ledger. Show the finished first minute with the real clip only if the motion is uncertain; otherwise go to step 2.
2. Apply Dan's first-minute notes and title-card choice.
3. Full render: `build.py range 0 729.46 <master>`; then subtitles (.srt from medium.en words, proofread), chapters (8 steps),
   `_shared/deliver/gate.py --format longform`, the watch pass, CUT-CONTINUITY-QC on every join, dense hair check, one
   independent ra-reviewer on the complete file, then deliver to `claude edited long form content/NN - If I Had Belly Fat.../`
   with REVIEW 540p, A/B, stamps, notes, recipe. Set queue `delivered`, send Dan the review copy.
4. On approval: register new clips in the clip library (`clip_library.py add ... --used-in RO-16`), roll `mark-used` for every source range.

## Cost ledger
Known (estimated): $1.50 = 10 nano-banana-pro 2K frame calls at about $0.15 (2 kept: A-start, A-end from the post-review pass;
8 rejected or superseded). Ledger: `/Volumes/Extreme/_edit_work/ro16/BUDGET.json`. Cap $5 per video.
Unknown: none. Pexels stock: $0.

## Model
Claude Opus 5.5, high (the round is mostly mechanical build plus judgment on the AI motion).

## Starter prompt
> Read `Handoffs/handoff-20260930-ro16-round2-opener-motion-then-full-film.md` and execute RO-16 round 2 with Dan's
> round-1 answers: <paste Dan's reply>. Re-hash round 1 first, generate the approved opener motion, then build, gate,
> independently review and deliver the full film, and send me the review copy.
