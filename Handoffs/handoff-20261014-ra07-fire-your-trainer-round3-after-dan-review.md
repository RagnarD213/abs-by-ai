# RA-07 "Fire Your Trainer!": round 3 (the full film: fix clips in Dan's order, gated and delivered)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R3`.
Rewritten 2026-10-14 after Dan answered the round 2 page (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Dan's words, verbatim, per item with hashes: `/Volumes/Extreme/_edit_work/ra07/round3-plan/decisions.json` (sha 81dcfc21907abf58).
Round 2 page: http://127.0.0.1:8827/ (served from `/Volumes/Extreme/_edit_work/ra07/round2/`).

Read first: `.claude/skills/_shared/VIDEO-RULES.md` (first sections: AI clip sense check, whole short in one round),
`/ad-edit` ("RA-07 round 2 lessons", "RA-14 round 3 lessons", "RA-14 round 4 lessons"), `_shared/PRE-RENDER-APPROVAL.md`,
`_shared/IMAGE-GENERATION.md`, `_shared/CUT-CONTINUITY-QC.md`. Recipe: `.claude/skills/ad-edit/reference/ra07/round2/` (live copies in the
work dir `/Volumes/Extreme/_edit_work/ra07/`). RA-14 round 4 (`ad-edit/reference/ra14/round4/`) is the newest full-film recipe on this set.

## What Dan said (2026-10-14, about the round 2 page)

| item | his words | what it means |
|---|---|---|
| I4a Out of order | "I4A looks good to generate." | Motion authorized from `round2/frames/I4a-start.png`, `-end.png`. |
| I3b Shoulder fix | "The start frame is good, but the end frame is not what a side lateral machine is... He'd be putting his hands underneath the pads, then the pads go on his arms... grabbing the handles with his hands, with the pads on his arm, and then doing the side lateral motion" | START approved. END remade the same day as `round2/frames/I3b-end.png` (d1337212b72bc3d9; rejected one kept as `I3b-end_v2_rejected.png`): hands on the handles, the round pads on the outside of his upper arms, arms out to shoulder height. **Not yet approved: see Step 1.** |
| I4b Hack squat | "(the hack squat instead). That looks good." | Motion authorized from `round2/frames/I4b-start.png`, `-end.png`. |
| Order | "The hack squat goes right after the squat out of order. The side lateral goes right after the tweaked shoulder." | Each fix plays straight after its own problem (round 2 had both fixes together after the three problems). Re-lay below. |
| First 30 s | "The first 30 seconds look good." | 0.00-30.13 approved as built (`round2/DRAFT - RA-07 round 2 - first 30 seconds.mp4`, 122c28bf3f6c3aa4). Do not change anything in it. |
| Round 3 | "Build a full film in the next round." | The whole 9:16, gated, is this round's deliverable. |

Dictation reading (say it in "What I decided"): "For I5, certain frames look good, but this clip is in the wrong place" is read as I4b,
because the rest of the sentence is about the hack squat clip. I2, I3a and I5 moving drew no change; they are carried as shown, not approved in words.

## Round 3, in order

1. **I3b END approval.** If the starter prompt carries Dan's yes to the new END frame, it is approved: go on. If it does not, put the
   START/END pair on a one-item page first thing, keep building everything else, and make I3b's motion only after his yes. If he never
   answers inside the session, the full film plays Dan on camera in I3b's slot, labelled on the page, and nothing else waits.
2. **Re-hash** round 2's files (table below) into `round3/HASHES.json`.
3. **Re-lay the problem-then-fix run** in `s70_plan.py` (only 36.47 to 47.01 changes; the first 30 s must come out frame-identical).
   The words: "when life gets in the way," 36.54-37.46 / "When you get injured" 37.74-38.40 / "or you can't make it to the gym one
   day," 38.58-40.00 / "or when the equipment you need is broken." 40.50-41.95 / "AI adjusts your plan in seconds," 42.22-43.80 /
   "while human trainers leave you confused until next week." 44.00-46.90. Recommended layout (every clip at least 1.2 s; the clips run
   a beat ahead of the words, which is how a montage reads):
   * I3a Tweaked shoulder 36.47-37.90 (press, wince, grip; take 1 from about 0.25 s so the grip lands inside the slot)
   * I3b Shoulder fix 37.90-39.20 (two takes joined by a cut, he changes place: the phone about 0.5 s, the lateral raise about 0.8 s)
   * M1 Working out at home 39.20-40.44 ("to the gym one day,")
   * I4a Out of order 40.44-42.11 ("or when the equipment you need is broken.")
   * I4b Hack squat 42.11-44.00 ("AI adjusts your plan in seconds,")
   * I5 Back next week 44.00-47.01 ("while human trainers leave you confused until next week."), 3.0 s: take 1 from about 1.0 s, or a retake
     if the 1 s of him standing at the door drags. Never slow or hold a clip.
   Then `splices left inside holds: []` and every clip >= 1.2 s, or the plan asserts.
4. **Motion** (`round2/motion/gen_motion.py`, Kling v3 standard, start + end image, no audio, about $1 a take, ledger includes failures):
   I4a one take (4 s); I4b one take (5 s), trimmed to him settling in and the rep; I3b two takes (START-only: he looks at the phone, small
   nod; END-only: one easy side lateral raise, hands on the handles, pads on the arms). Every take: the three sense questions at playback
   speed, the measured self-change check, then a FRESH independent subagent with the three questions (round 2's brief, in this skill's
   round 2 recipe notes). I2 needed three takes in round 2: plan on a retake. The OUT OF ORDER sign keeps its letters; the hack squat sled
   and plates stay solid; the lateral raise pads stay on his arms. Conform with `s75_clips.py` (add the new clips; I3b is a two-piece
   concat); chips placed by looking at each clip.
5. **The whole 9:16.** `s86_assemble.py work` with `PENDING = set()`. RA-14 round 4 lessons on this ad: print his mouth frame by frame
   after "step." and end on the last frame of the held pose (end hold 0.80 s); smooth the music tail on the mix if it is abrupt
   (`ra14/round4/s91_tail.py`); frame-lock the mix (voice chain `--frame-lock` on the picture, same EQ as `mix_bass.wav.voice_chain.json`),
   then `audio_gate.py` (expect the known `tone` max miss from the bass lift; everything else must pass).
6. **Gates on the exact file:** delivery gate (`_shared/deliver/gate.py`, plan built like `ra14/round4/s93_gateplan.py`:
   `talking_head_windows`, full-screen cards in `punch` with `punch_covered: true`, the phone box measured like `s94_phonebox.py`),
   `watch.py` + its fresh judge, the independent `ra-reviewer` with the three AI clip questions in its brief. Fix, re-render, re-gate.
7. **Deliver** to `Claude Ad Videos/fire your trainer - RA-07/` (naming per memory `ad2-vertical-approved`), copy the review copy to
   `Videos to Review/` (52.7 s), page with "What I decided" and a revision list with timestamps (the first 30 s unchanged; the new run
   36.5-47.0 s; the end). Edit queue `delivered`.
8. **Then the 16:9** from the same cut and sound, with its edit sheet, gate, watch pass and review (own round if the 9:16 comes back
   with notes). At the end of the job: register every keeper AI clip in the clip library (`_shared/cliplib/clip_library.py add ... --used-in RA-07`).

## Files (work dir `/Volumes/Extreme/_edit_work/ra07/`, sha256 first 16)

| file | hash |
|---|---|
| `round3-plan/decisions.json` (Dan's round 2 answers) | 81dcfc21907abf58 |
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
| `round2/motion/I2_v3.mp4` / `I3a_v1.mp4` / `I5_v1.mp4` | 61685a24b9c3e494 / 36356bfd6d8f4658 / 4659563719dabb74 |
| `round2/frames/I3b-start.png` (approved) / `I3b-end.png` (new, pending) | f9227f183e00e437 / d1337212b72bc3d9 |
| `round2/frames/I4a-start.png` / `-end.png` (approved) | a72b4fe94af6afe8 / ac3c207363cde564 |
| `round2/frames/I4b-start.png` / `-end.png` (approved) | 40d295b292c8baa4 / 99acd5ac5fe2ac36 |
| `round2/DRAFT - RA-07 round 2 - first 30 seconds.mp4` (approved) | 122c28bf3f6c3aa4 |

I3a and I5 change length in the new layout: re-conform them from their takes (`round2/motion/I3a_v1.mp4`, `I5_v1.mp4`), never stretch.

## Gate status (honest)

Audio gate on `mix_bass.wav`: 11 of 12; `tone` max 2.86 dB against 2.5 (the bass lift; RA-14's approved mix misses the same row). Not
frame-locked. Round 2 composite: faces clear every graphic by 373 px or more, 0 caption collisions, every cut in the first 30 s a clean
size or card change. Junk pass: 0 confirmed. Delivery gate, watch pass, edit sheet and full independent review: NOT RUN.
Soft spots: the "One," / "Two," close shots are 0.43 s; H1 and M1 are Lanczos upscales (Real-ESRGAN is not installed); 24 fps AI clips
conformed to 29.97 by frame duplication.

## Cost ledger

Motion $5.00 of the $10 cap (`round2/motion/ledger.json`, five takes, estimate). Frames: 8 Codex images ($0). Round 3 estimate: I4a $1,
I4b $1, I3b $2, maybe an I5 retake $1 = $4-5, plus retakes. At $10, ask Dan for the number first (alone, at the top of the message);
never ship a faulty clip to stay under it.

## Recommended model

Claude Opus 5.5, high effort. Escalate to Fable 5.1 only for a clip Opus fails twice.

## Starter prompt

> AD. Rename this task `Fire Your Trainer AD R3`. Read `Handoffs/handoff-20261014-ra07-fire-your-trainer-round3-after-dan-review.md` and run round 3 of RA-07 "Fire Your Trainer!" with /ad-edit: put each fix right after its problem, make the motion for I4a, I4b and the shoulder fix, build the full film, run every gate, the watch pass and the independent review, deliver it and send me the page. Then the 16:9. The new shoulder-fix end frame: [approved / changes]. Use the Codex subscription to generate any new images.
