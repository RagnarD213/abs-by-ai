# RA-07 "Fire Your Trainer!": round 3 (motion for the three fix clips, then the whole ad, gated and delivered)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R3`.
Written 2026-10-14 by the round 2 session (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Round 2 page: http://127.0.0.1:8827/ (served from `/Volumes/Extreme/_edit_work/ra07/round2/`). Round 1 page: http://127.0.0.1:8807/.

Read first: `.claude/skills/_shared/VIDEO-RULES.md` (first sections: AI clip sense check, whole short in one round),
`/ad-edit` (sections "RA-07 lessons", "RA-14 round 3 lessons", "RA-14 round 4 lessons"), `_shared/PRE-RENDER-APPROVAL.md`,
`_shared/IMAGE-GENERATION.md`, `_shared/CUT-CONTINUITY-QC.md`. Round 2 recipe: `.claude/skills/ad-edit/reference/ra07/round2/`
(live copies in the work dir `/Volumes/Extreme/_edit_work/ra07/`).

## Step 0: record Dan's answers

Dan's reply to the round 2 page arrives with the starter prompt. Write it verbatim, per item, into
`/Volumes/Extreme/_edit_work/ra07/round3-plan/decisions.json` (same shape as `round2-plan/decisions.json`), with hashes. The
page asked three things:

1. New frames: I3b Shoulder fix (phone on the bench, then the seated side lateral raise machine), I4a Out of order (now a Smith
   machine squat rack, standing in for his "leg squat machine"), I4b Hack squat instead. Recommended: approve all three.
2. The three clips moving: I2 Same sheet for everyone, I3a Tweaked shoulder, I5 Back next week. Recommended: approve.
3. The finished first 30 seconds. Recommended: approve.

Nothing is approved that he has not said. If he changes a frame pair, remake only that pair (Codex, `codex-image.sh`, END from START)
and put it on a small page before any motion. If he rejects a clip, Dan plays on camera there (the plan's hold list needs a size
change on every pause splice it exposes: re-run `s70_plan.py` and check `splices left inside holds: []`).

## Round 3 work, in order (if he approves)

1. **Re-hash** the round 2 files below into `round3/HASHES.json`.
2. **Motion for the approved new frames** (`round2/motion/gen_motion.py`: add jobs, Kling v3 standard, start + end image, no audio,
   about $1 a take, ledger includes failures):
   * **I4a** (40.44 to 42.11, 1.67 s, "or when the equipment you need is broken."): one take START to END, 4 s. Trim to walk-up, stop,
     palms up. The OUT OF ORDER sign must keep its letters in every frame.
   * **I3b** (42.11 to 43.38, 1.27 s, "AI adjusts your plan in"): he changes place, so TWO takes joined by a cut (VIDEO-RULES: a change
     of time or place is a cut, never asked of one take): START-only take (he looks at the phone, a small nod) and END-only take
     (one easy lateral raise). About 0.5 + 0.77 s. If the 0.5 s phone shot reads as a flash, show only the machine rep and say so.
   * **I4b** (43.38 to 44.91, 1.53 s, "seconds, while human trainers"): one take START to END, 5 s, trimmed to him settling in and the rep.
   * Each take: the three sense questions at playback speed + the measured self-change check (frame vs frame + 10, person masked),
     then a FRESH independent subagent with the three questions (the round 2 brief worked; it found the loose sheet in I2's tail).
     Expect retakes: in round 2, I2 needed three takes (stack turned into a binder; a second trainer appeared). Do not ship a fault.
   * Conform with `s75_clips.py` (add the three to `SRC`; I3b needs a two-piece concat). Chips placed by looking at each clip.
3. **The whole 9:16.** Re-run `s86_assemble.py work` with `PENDING = set()`; nothing pending, so the full film is shown, not a
   placeholder film. Then RA-14 round 4's lessons, on this ad: print his mouth frame by frame after "step." and end on the last
   frame of the held pose (end hold 0.80 s, measured in round 1); smooth the music tail on the mix after the last word if it is
   abrupt (`ad-edit/reference/ra14/round4/s91_tail.py`); frame-lock the mix: re-run the voice chain with `--frame-lock` on the
   finished picture (same EQ as `mix_bass.wav.voice_chain.json`), then `audio_gate.py` on it.
4. **Gates on the exact file**: delivery gate `_shared/deliver/gate.py --format` for the 9:16 with a gate plan built like
   `ad-edit/reference/ra14/round4/s93_gateplan.py` (`talking_head_windows`, full-screen cards in `punch` with `punch_covered: true`,
   measured phone box like `s94_phonebox.py`); `watch.py` + its fresh judge; the independent `ra-reviewer` with the three AI clip
   questions in its brief. The edit sheet is written with the 16:9 (RA-14 round 4 lesson 5).
5. **Deliver** to `Claude Ad Videos/fire your trainer - RA-07/` (naming per `/editor-deliveries` and memory `ad2-vertical-approved`),
   copy the review copy to `Videos to Review/` (the ad is 52.7 s), send Dan the round 3 page with "What I decided" and a revision
   list with timestamps if anything he already saw changed.
6. **Then the 16:9** from the same cut and sound (ad-edit Step 8 in reverse: same EDL and mix, 16:9 crops and layouts), with its
   edit sheet, gate, watch pass and review. It can be its own round if the 9:16 comes back with notes.
7. At the end of the job: register every keeper AI clip in the clip library (`_shared/cliplib/clip_library.py add ... --used-in RA-07`),
   set the edit queue (`delivered` on the review copy; `finalized` only on Dan's words).

## Locks and files (work dir `/Volumes/Extreme/_edit_work/ra07/`, sha256 first 16)

| file | hash |
|---|---|
| `round2-plan/decisions.json` (Dan's round 1 answers) | 36041c71dc38958c |
| `cut.json` (unchanged since round 1) | d548aa837fe38410 |
| `words_aligned.json` | 0f3b808eed7bbedb |
| `beats_r2.json` | 663853c259e2e08c |
| `mix_bass.wav` (bass lift, -14.2 LUFS, not frame-locked) | da442876928fbe70 |
| `grade.json` (RA-14's C2 LUT as is) | 7389f3c50d3a1a93 |
| `ra01lib.py` (levels 738x1312 / 918x1632, LUT grade, BT.709 encode) | 913e0634604deb2a |
| `framing_holdstart.json` | 1f513b4848297e87 |
| `cap_9x16/captions.mov` (round 1's, unchanged) | 36424daa67c85054 |
| `round2/gfx/manifest.json` (L1-L3 headlines on the number words, C1) | e06a414deade1ef6 |
| `round2/clips/H1.mp4` / `M1.mp4` / `I2.mp4` / `I3a.mp4` / `I5.mp4` | a9f6b38df3fc3070 / c243a0dc9dd2b7d8 / 20dadeb68e47dbd4 / f493f219ad092d05 / 15fc554c63a1ab94 |
| `round2/cards/P1.mp4` / `K1.mp4` / `W1.mp4` | 4d99a7cd43ac3b0f / ece7d02b823512f5 / 1cc1152f15185f60 |
| `round2/motion/I2_v3.mp4` / `I3a_v1.mp4` / `I5_v1.mp4` (the takes used) | 61685a24b9c3e494 / 36356bfd6d8f4658 / 4659563719dabb74 |
| `round2/frames/I3b-start.png` / `-end.png` | f9227f183e00e437 / 6eda933bd5131e57 |
| `round2/frames/I4a-start.png` / `-end.png` | a72b4fe94af6afe8 / ac3c207363cde564 |
| `round2/frames/I4b-start.png` / `-end.png` | 40d295b292c8baa4 / 99acd5ac5fe2ac36 |
| `round2/DRAFT - RA-07 round 2 - first 30 seconds.mp4` | 122c28bf3f6c3aa4 |

The plan (`beats_r2.json`, from `s70_plan.py`): H1 0.00-3.44 | Dan NEAR / FAR | "One," NEAR 0.43 s, FAR | P1 14.95-17.05 | K1
17.05-18.85 | paper line NEAR, FAR | "Two," NEAR 0.43 s, FAR | W1 27.53-30.13 | Dan FAR | I2 31.63-34.30 | "And three," NEAR, FAR |
I3a 36.47-38.54 | M1 38.54-40.44 | I4a 40.44-42.11 | I3b 42.11-43.38 | I4b 43.38-44.91 | I5 44.91-47.01 | Dan FAR then NEAR with
C1 to 52.69 (1579 frames). Every one of the 16 pause splices measured visible (`round2/splices/splices.json`, 2.4-11x); none is left
inside a hold.

## Gate status (honest)

* Audio gate on `mix_bass.wav`: 11 of 12 PASS; `tone` FAIL on max (2.86 against 2.5 dB), mean 1.14 passes. This is the bass lift
  (VIDEO-RULES: the tone row fails on any fixed tone shape); RA-14's approved bass mix fails the same row. Not yet frame-locked.
* `s88_checks.py` on the round 2 working composite: faces clear every graphic by 373 px or more; 0 caption collisions.
* Junk pass (`round2/junk_report.json`): 0 confirmed; the two high PAUSEJUMP flags (3.3 s, about 42 s) sit on card cuts.
* Delivery gate, watch pass, edit sheet, independent full review: NOT RUN (round 3).
* Known soft spots to look at again: the "One," and "Two," close shots are 0.43 s each; the library clips H1 and M1 are Lanczos
  upscales (Real-ESRGAN is not installed on this Mac; Ad 13's 1080 copy of A0147 is slowed to 4.54 s and unusable); the 24 fps AI
  clips are conformed to 29.97 by duplicating every 5th frame (the reviewer called it a faint stutter; same as H1 in round 1).

## Cost ledger

Motion: $5.00 spent of the $10 cap (`round2/motion/ledger.json`: I2 v1, v2, v3; I3a v1; I5 v1; estimate $1 a take, the Replicate
invoice is the record). Frames: 7 Codex images on the subscription ($0). Gemini watch of the first 30 s: under 5 cents.
Round 3 estimate: I4a $1, I3b $2, I4b $1 = $4, plus retakes. A single retake keeps it at $10; past that, ask Dan for the number
before generating (VIDEO-RULES: never ship a bad clip to save budget; ask first, alone, with the number).

## Recommended model

Claude Opus 5.5, high effort (model-routing-plan: editorial build and first cuts). Escalate to Fable 5.1 only if a clip fails Opus's
check twice.

## Starter prompt

> AD. Rename this task `Fire Your Trainer AD R3`. Read `Handoffs/handoff-20261014-ra07-fire-your-trainer-round3-after-dan-review.md` and run round 3 of RA-07 "Fire Your Trainer!" with /ad-edit. Record my round 2 answers (below) in `round3-plan/decisions.json`, make the motion for the approved fix clips (Use the Codex subscription to generate any new images), then build the whole 9:16, run every gate, the watch pass and the independent review, deliver it to the ad folder and send me the page. Then the 16:9. My round 2 answers: [paste]
