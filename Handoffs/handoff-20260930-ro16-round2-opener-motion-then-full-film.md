# RO-16 round 2: finish the edit (full film, gates, review, delivery)

**Job:** RO-16 "If I Had Belly Fat, Here's How I'd Lose It In 90 Days", organic long-form from 9/23 roll C1710.
**Written:** 2026-09-30 by Claude (Opus 5.5) after Dan reviewed round 1. **Model:** Claude Opus 5.5, high (Dan asked for
Opus; the creative calls are locked, the work is a careful build plus checks).

Dan on round 1: *"Overall, I think you did an excellent job with this video. This, I think, is going to be the best video we've
ever edited. This is the process that we need."* Keep everything he approved exactly as it is.

## Read first
- `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md` (including the new
  "review page" standard), `GRAPHICS-STANDARDS.md`, `CUT-CONTINUITY-QC.md`, `.claude/skills/longform-edit/SKILL.md`.
- Dan's decisions with his words and hashes: `/Volumes/Extreme/_edit_work/ro16/round2-plan/decisions.json`.
- Round 1 page `/Volumes/Extreme/_edit_work/ro16/round1/index.html` (serve: `cd /Volumes/Extreme/_edit_work/ro16/round1 &&
  python3 -m http.server 8794 --bind 127.0.0.1`), reviews `round1/REVIEW-round1.md` + `round1/EDITOR-DISPOSITION.md`,
  hashes `round1/HASHES.json` (re-hash before touching anything; plan.py, gfx.py and the A01/G06/G16 stills changed in the
  round-2 prep below, which is expected).

## Recipe (working copy `/Volumes/Extreme/_edit_work/ro16/recipe/`, git copy `.claude/skills/longform-edit/reference/ro16/`)
`edl.py` (38 pieces) -> `shots.py` (43 shots) -> `assemble_audio.py` + medium.en ASR -> `words_out.py` -> `plan.py` ->
`resolve.py` (snapping rules) -> `stills.py` -> `build.py range <a> <b> <out>` (graded picture, Soft Blue paint, audio B chain,
level-matched room tone at joins, frame-locked mux). Film length 21,862 frames = 12:09.46. The SSD copy is the one to run;
copy changed scripts back into the git copy at the end.

## Locked (do not change)
- Look: colour C, crops W2/T2 (W3 only under side cards), audio B via voice_chain `--no-dereverb` + the WV-01 EQ + 0.9 dB @150 Hz,
  no music. Dan: *"Audio sounds good, color correction looks good, and placement of the graphics and clips looks good."*
- The first minute (0:00-1:13.7) as built in round 1, apart from the two items below that change inside it (A01, G03).
- Approved by name: G01, G04, T1, C02, G05, C03, G22, C01 (*"great use of that clip. Way to reuse a clip and not generate a new one"*).
  Every other item: Dan said *"almost all of these are looking good. I'm only going to tell you the ones that need revisions now."*

## Already done in round-2 prep (2026-09-30)
- **A01 opener motion generated** from the approved frames: `aiframes/A01_motion_v1.mp4` (Veo 3.1 fast, 8 s, 24 fps, used 0-7.05 s).
  Checked frame by frame (hands, face, reflection, no fog). In-context preview: `round2/RO-16 opener in context.mp4`. Plan item
  A01 now uses it with the AI-GENERATED chip top-right.
- **G06** topic is now "HOW ZEPBOUND HELPS" (Dan's explicit wording; his exception to the no-brand-name-in-graphics rule, this graphic only).
- **G16** bar: fat and its label green (`B.GOOD`), lean mass and its label red (`B.BAD`).
- **C16 removed** (Dan: a fit man photographing his food, or no clip; no suitable stock exists, so no clip).
- **C28 removed** (Dan: the photo made no sense over the microdose line). No replacement.

## Still open: G03 (the one decision)
Dan wants one of Codex's two VSL three-photo slates (the left and centre photos in round 1 had expressions he disliked).
- Option 1: studio-blue-11, studio-blue-127, studio-blue-247 (`round1/G03-option1.jpg`)
- Option 2, the VSL's final slate: studio-white-23, studio-blue-173, studio-blue-240 (`round1/G03-option2-VSL-final.jpg`)
`plan.py` currently holds option 2 as the default. **Use Dan's pick from the starter prompt**; if he has not picked, ask that one
question first and do nothing else until he answers. Panels use Codex's exact mechanics (`gfx.py` scene `portraits_codex`,
panels in `assets/g03/`).

## Do next
1. Re-hash; set G03 to Dan's pick; `python3 recipe/resolve.py`; re-render the changed stills and look at them (A01, G03, G06, G16).
2. Full render: `python3 recipe/build.py range 0 729.462 "/Volumes/Extreme/_edit_work/ro16/round2/RO16_MASTER.mp4"`. Two builds
   max on the machine.
3. Checks on the exact file: audio gate; `_shared/deliver/gate.py --format longform`; the watch pass; CUT-CONTINUITY-QC on every
   join (native frames); dense hair check (every 0.25 s, person mask); `_shared/cut/junk.py` on the delivered file. Specific watch
   points: the stretch around 11:18-11:52 lost its cutaway when C28 was removed (confirm the static-stretch row; framing cuts at
   the piece joins should keep it moving); G19's average line finishes its animation; G20's 3A reveal.
4. Subtitles `.srt` from the medium.en words (proofread: Zepbound, "Clean Eatz", "AbsByAI.com"), chapters (intro, the 8 steps,
   wrap). Not burned in.
5. One fresh independent reviewer (ra-reviewer) on the complete file; fix what it finds; re-review until SHIP.
6. Deliver to `claude edited long form content/09 - If I Had Belly Fat, Here's How I'd Lose It In 90 Days/`: master, REVIEW 540p,
   `.srt`, chapters, audio A/B, `.audio_gate.json` + `.deliver_gate.json`, `notes-RO16.md` (every deliberate choice), recipe copy.
   Upload the 540p copy to the Drive folder "RO-16 If I Had Belly Fat - review" (anyone with the link) and send Dan the review
   copy with a short "What I decided" list (the standard page if anything needs his eye).
7. Queue: `queue.py set RO-16 delivered`, mirror to the Edit Queue page (artifact db), update the board entry.
8. After Dan finalizes: register A01 and every new stock insert in the clip library (`clip_library.py add ... --used-in RO-16`,
   then `sheet`), and `roll_sidecar.py mark-used` for every C1710 range in `edl.json`.

## Cost ledger
$2.70 known (estimated): 10 nano-banana-pro frame calls ($1.50) + Veo 3.1 fast 8 s ($1.20). Cap $5 per video. Ledger:
`/Volumes/Extreme/_edit_work/ro16/BUDGET.json`. Pexels stock $0.

## Starter prompt
> Read `Handoffs/handoff-20260930-ro16-round2-opener-motion-then-full-film.md` and finish RO-16. My G03 pick: <option 1 or 2>.
> Re-hash, apply it, render the full film, run every gate and an independent review, deliver it, and send me the review copy.
