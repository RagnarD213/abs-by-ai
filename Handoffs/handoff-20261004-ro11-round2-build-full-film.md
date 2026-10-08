# Handoff: RO-11 round 2, opener motion then the full film (everything is approved) (2026-10-04)

**CONTENT, long-form (LFC).** Task name: `Calories Don't Matter LFC R2`. Recommended: Claude Opus 5.5, effort high.
A long-form content video gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version here.

**Goal.** Generate the approved AI opener's motion, then build, gate, review and deliver the full RO-11 film, "When
Calories Don't Matter For Fat Loss" (9/23 roll C1705, 9:58). No creative decisions are pending.

**Dan's words (2026-10-04).** On round 1: *"Other than that, everything looks good."* (first minute, all 21 HyperFrames
graphics, titles, recap, clips, the cut). On the first opener: *"I like the idea of it, but I'm concerned this will be
disapproved for negative events and imagery... because of the fat pinch. I'd like you to replace this with a picture of an
overweight man with a tiny plate of bland-looking chicken breast and broccoli in front of him, looking like he's eating very
few calories and still not losing weight."* On the new frames: *"All right, that looks good."* Record with hashes:
`/Volumes/Extreme/_edit_work/ro11/round2-plan/decisions.json`.

**Read first.** `_shared/VIDEO-RULES.md` (new top section: no fat pinching or belly close-ups, above all in the first 30
seconds), `_shared/PRE-RENDER-APPROVAL.md`, `_shared/hyperframes/README.md`, `.claude/skills/longform-edit/reference/ro11/README.md`,
then `../ro10/README.md`, `finish.py`, `finish_chain.sh`, `clipscan.py`, `dupscan.py` (RO-10's full-film round is the model:
same set, same scripts; its work dir is `/Volumes/Extreme/_edit_work/ro10/round2/`).

**Locked (do not change).**
- Cut, takes, shots: `/Volumes/Extreme/_edit_work/ro11/edl.json`, `shots.json` (17 pieces, 53 shots, 17,928 frames =
  598.2 s), words `words_out.json`. Take choices and every restart: `recipe/edl.py`.
- Look and audio: colour C, W2/T2, framing solved by `recipe/build.py all_segments()` (zero same-size joins); audio = the
  fit in `FIT.mp4.voice_chain.json` + 0.9 dB at 150 Hz. First minute: audio gate PASS 13/13, -14.2 LUFS.
- All 21 HyperFrames graphics, copy and motion (`hf/manifest.json`, `hf/BEATS.md`): 11 lower thirds, 7 fact cards, 2 side
  lists (G03, G20), the cycle (G18). The 7 section titles (FACTOR n OF 7), recap G21, clips C01 to C12.
- Opener frames: `aiframes/C-start.png` (sha256 969fa7ab...552c5b) and `aiframes/C-end.png` (0edd9b75...a29d0), made with
  Codex; 1920x1080 copies `C-start-1080.jpg`, `C-end-1080.jpg`. Frames A and B are rejected; do not use them.

**The one new asset: the opener motion (authorized).**
- Slot A01: 0:00 to 0:04.56, under "You can still gain fat, even if you're not eating too many calories." Dan appears on
  camera at "I'll show you how to prevent this".
- Generate from C-start to C-end (first and last frame; Veo or Kling through the API, AI video is not a Codex job). Prompt:
  `aiframes/motion_C.txt`. Estimated $0.60 to $1.20 a take. Both frames show nearly the same pose, so there is little
  travel to invent (RO-12 trap 11). Guard the launch with `if __name__ == "__main__":` (RO-12 trap 12).
- Check every frame: no morphing fork, plate or food, no melting hands, no hand on his body, stomach stays hidden. A clip
  must cover the 4.56 s slot from real motion: never hold or stretch it. If two takes fail, say so and ask before a third.
- Place it: in `recipe/plan.py` change A01 from `kind="ai"` to `kind="clip"` with `src=[".../aiframes/C_motion_v1.mp4@<start>"]`
  and `label="AI-GENERATED"` (chip top right is clear of his head; check on a still).
- Dan approved the frames, not the motion. Show the finished motion at the top of the delivery note so he can overrule it.

**Next action (in order).**
1. Rename the task, board entry, `queue.py set RO-11 in_progress`. Generate and check the motion, edit `plan.py`.
2. `cd /Volumes/Extreme/_edit_work/ro11`; `python3 recipe/resolve.py`; `from_plan.py --plan plan_resolved.json --words
   words_out.json --shots shots.json --out hf --render` (every scene should report unchanged).
3. Full film: `build.render_range(0, 598.20, '/Volumes/Extreme/_edit_work/ro11/round2/RO11_MASTER.mp4')`. Two-build cap:
   check `ps` first.
4. `checks.py` on the master (round 1: G03 and G18 pass; **G20 reads -211 px at 555.25 s because both hands swing wide
   UNDER the card, not into it; Dan saw the flag and approved everything, so leave it and say so**). Hair check on the whole
   film (first minute: 30 px minimum). Jump-cut and junk pass on the exact file (`CUT-CONTINUITY-QC.md`). No stock clip or
   scene twice (`dupscan.py`); check each clip slot against its source length.
5. SRT from the delivered audio's own transcript, chapters (the 7 factors), `_shared/audio/audio_gate.py`,
   `_shared/deliver/gate.py --format longform --plan plan.json`, watch pass, one independent `ra-reviewer` on the exact file.
   Fix what it finds (3-round cap). Report gate rows honestly; RO-12's README lists the rows that read Soft Blue cards as
   burned captions.
6. Deliver to `claude edited long form content/11 - When Calories Don't Matter For Fat Loss/` (master, SRT, chapters,
   REVIEW 540p, audio A/B, stamps, notes, recipe). Send Dan the review copy, queue `delivered`, mirror to the Edit Queue page.
7. Description notes for setup: one realistic AI clip, so YouTube's altered/synthetic flag is TRUE; links to the glycine
   video, the alcohol video and the first calories video (RO-10, original upload Private; replacement Sunday date and public URL pending); study list in
   `Docs/SCRIPTS_CALORIES_PAIR_20260921.md` production notes. Ending is subscribe-only, no AbsByAI call to action.
8. After Dan approves the film: register the opener and the used stock in the clip library, delete this handoff's rows in
   `Handoffs/README.md` and the board.

**Not done yet (do not claim).** No full film, SRT, chapters, delivery gate, watch pass or independent review. The RGB
compositor proof was not re-run on this film (RO-10's used the same unchanged code).

**Spend.** About $1.70 of $5 (Gemini listening $1.10, rejected A and B frames $0.60). The C frames were Codex, no API cost.
With one or two motion takes the video lands near $2.30 to $4.10.

**Open risks.** Round 1 page (old opener placeholder): http://127.0.0.1:8802/. The shared folder's `VIDEO-RULES.md`,
`AI_COORDINATION.md` and `Handoffs/README.md` carry other sessions' uncommitted edits, so push with
`scripts/git/safe-push.sh` naming only your own files and report what it refuses.

## State on 2026-10-08 (read this first): the opener needs Dan's pick, the film is not built

- **Two motion takes failed the frame check; a third needs Dan's OK.** Take 1 (Veo 3.1 fast, `aiframes/C_motion_v1.REJECTED.mp4`)
  and take 2 (Veo 3.1, `aiframes/C_motion_v2.mp4`, prompt `motion_C_v2.txt` + `.neg.txt`) both turn the fork into a spoon in
  his mouth (take 2 frames 54 to 64), detach the fork head as it lowers (71 to 76) and reshape the food at the cut (24 to 36).
  The approved end frame shows food already eaten, so any take must change the plate. The 10:00 run was a provider error
  (E004): no clip, not a take.
- **Take 2's tail is clean:** frames 80 to 144 (3.29 s to 6.0 s): chews, lowers the fork, looks up at the camera 4.6 to 5.7 s, looks down.
- **Dan's choices, page http://127.0.0.1:8811/** (`round2/opener-page/`, served by `review_server.py 8811`):
  - **B (recommended):** film opens on Dan; A01 becomes `kind="clip"`, `src=[".../aiframes/C_motion_v2.mp4@3.29"]`,
    `label="AI-GENERATED"`, on from 1.82 s ("even") to 4.50 s. Preview: `round2/opener-preview/B_dan-first_then-clip.mp4`.
    In `plan.py` that is `start="even if you're not"`, `end="too many calories"`, `tail=0.24`; check `resolve.py` gives 1.82 to 4.50
    (the full-screen snap rules must not pull it to 0).
  - **A:** third take, no fork to mouth (nudges the chicken, sets the fork down, sighs, looks up), from `C-start.png` only.
    $0.60 to $1.20. If it fails, fall back to B.
  - **C:** take 2 as is at `@1.10` over the original 0 to 4.56 s slot (Dan overrules the frame check).
- **Done and reusable:** all locks re-hashed, match. `build.py` now has RO-10's repeated-first-frame fix; all 57 segments are
  cached and `dupscan.py` is clean (0). `junk_report.json` written (pre-render, `ranges.json`). `recipe/finish.py`,
  `finish_chain.sh`, `deliver.sh` are written for RO-11 (untested until a master exists). Jumps: 0.
- **Spend:** about $3.50 of $5 (`BUDGET.json`).
- **Next action:** record Dan's pick in `round2-plan/decisions.json`, edit `plan.py` A01, then step 2 onward above.

**Starter prompt (Claude Opus 5.5, effort high):**

Name this task `Calories Don't Matter LFC R2`. This is CONTENT (long-form). Read and execute
`Handoffs/handoff-20261004-ro11-round2-build-full-film.md`. Everything in RO-11 is approved, including the new opener frames:
generate the opener motion from the approved start and end frames, check it frame by frame, then build the full film, run
every gate and the independent review, deliver it and send me the review copy.
