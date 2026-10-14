AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Top 3 Tips AD R2`.

# RA-04 "Top 3 Tips For Getting Abs": round 2 (Dan answered round 1 on 2026-10-14)

**Written 2026-10-13 by the round 1 session, rewritten 2026-10-14 with Dan's answers (Claude, Opus 5.5).**
Job doc: `Handoffs/video-editing/RA-04-top-3-tips-for-getting-abs.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`. Recipe and lessons:
`.claude/skills/ad-edit/reference/ra04/README.md`. Work folder: `/Volumes/Extreme/_edit_work/ra04/`.
Decisions with hashes and Dan's words: `/Volumes/Extreme/_edit_work/ra04/round2-plan/decisions.json`.

## Dan's answers (2026-10-14), recorded

| item | verdict | his words |
|---|---|---|
| First 30 seconds | **approved** | "First 30 seconds look good." |
| "Completely free" at 0:17 | not answered: **keep as filmed** | |
| Analysis card | **Soft Blue** (`cards_9x16/analysis.mp4`) | "Let's go with the blue graphic. Let's always go with the blue graphics going forward. Let's make that our standardized graphic set." |
| Voice | **B, extra bass** (`mixB.wav`) | "Let's go with the voice with the extra bass." |
| Tip 3 | **new AI clip**, frames first | below |

The standing rule ("blue graphics going forward") is already recorded: VIDEO-RULES second section and memory
`analysis-card-reusable-graphic` (the RA-14 session made a Soft Blue HyperFrames analysis card the standard on 10-14,
`_shared/hyperframes/analysis-card/`). RA-04 keeps the Soft Blue card Dan approved on this page; switch to the template
only if it has a 9:16 layout and draws the same thing.

## ⚠ Fix first: the banned before/after screen is in the round 1 draft for 0.3 s

Found by the RA-05 session: the result card `flow_b` started B0049 at 27.3 s, and the app's "Meet the new you" before/after
screen runs to about 27.6 s, so it shows at 0:15.3 for the card's first frames. Dan approved the first 30 seconds without
seeing it called out. Fix: start at 28.0 s (`FLOW_B_T0`, already in both copies of `s06_inserts04.py`), rebuild `flow_b`,
and look at its first five frames and the last five of every app card. Proof still: `/Volumes/Extreme/_edit_work/ra05/look/ra04_flowb_check.jpg`.
Tell Dan in one line that it was fixed.

## Round 2 work, in order

1. **Rebuild with the approved changes:** `flow_b` from 28.0 s; the mix with voice B (`s08_audio.py` must pass
   `--eq "<fitted EQ>,equalizer=f=120:t=q:w=0.8:g=+3.0"`, the line in README lesson 9; `LOCK=picture_9x16.mp4`).
2. **The tip 3 AI clip: frames only, then stop for Dan.** His request: *"a man with a broken arm walks into a gym and sees
   the squat rack. He walks up to the squat rack with a broken arm and shakes his head. Then he goes to the leg press machine
   and does the leg presses instead, after looking at his phone... You may need to generate more than two frames."*
   * **Where it plays (recommended):** from "when life gets in the way" (about 0:38.9) to the end of "adjust your plan"
     (0:43.4), about 4.5 s, replacing the knee-brace stock clip (B0126). The TIP 3 lower third ends on the first AI frame.
     "When you get injured..." alone is only 3.1 s, too short for three actions; say so on the page and offer it as option B.
   * **Three shots, five frames** (9:16, subject in the centre third, made with `.claude/skills/_shared/codex-image.sh`; make F1
     first and pass it as `--image` to every other frame so it is the same man):
     * F1 (shot 1 start): an ordinary man around 40, average build, plain grey T-shirt and shorts, left forearm in a white
       cast and a navy sling, walking across a commercial gym floor; a squat rack with a loaded barbell ahead of him.
     * F2 (shot 1 end): the same man stopped in front of the squat rack, looking at the barbell, mid head-shake.
     * F3 (shot 2 end, shot 2 starts on F2): same spot, he holds his phone in his good hand and looks down at it (screen glow only, no legible UI).
     * F4 (shot 3 start): seated in a leg press machine, feet on the platform, knees bent, cast arm resting in its sling.
     * F5 (shot 3 end): legs extended, pushing the sled, same position of the cast arm.
   * Prompt rules: ad-edit Step 4.5 (no camera or film words, ordinary unretouched person, flat light, no logos or text on
     clothes or the gym), no belly framing, no hands on his body. Check every frame for six fingers, cast on the wrong arm,
     scrambled signage.
   * Put the pairs on a round 2 page (PRE-RENDER-APPROVAL layout): each pair with its name ("Broken arm at the squat rack"),
     when it plays, the words before, under and after it, what you see, and what plays if he says no (B0126). Then stop.
   * After Dan approves the frames: three image-to-video clips (start and end frame), checked at playback speed with the three
     sense questions (VIDEO-RULES 2026-10-13: cause and effect, readable with sound off, shows the line). A clip that fails is
     cut down or regenerated, never shipped with the fault described. Budget: **$10 total for this ad**; spend so far $0.
     Estimate the three clips before running. AI-GENERATED chip on the clip.
3. **When nothing is pending, the full film:** 9:16 master (58.9 s), then the 16:9 from the same edit, then everything
   round 1 did not do: land-then-hold centring check, `piccuts.py decide`, the junk pass, `roll_sidecar.py mark-used`, the edit
   sheet, `audio_gate.py` with the A/B, `deliver/gate.py --format ad9x16` and `ad16x9`, the watch pass, one fresh independent
   reviewer, the negative-imagery scan, REVIEW 540p copies, notes, recipe, delivery to
   `Claude Ad Videos/top 3 tips for getting abs - RA-04/`, a copy in `Videos to Review/`, `queue.py set RA-04 delivered` +
   artifact db, `clip_library.py add --used-in "RA-04"` for the new AI clip. Give Dan the later-round revision list with
   timestamps (only the changed parts: 0:15 result card, the tip 3 clip, the voice).

## Files (work folder)

| file | sha256 (first 16) | state |
|---|---|---|
| `round1/DRAFT - RA-04 round 1 - first 30 seconds.mp4` | a7b8880b81e3f623 | approved by Dan, except the 0.3 s banned screen to fix |
| `cards_9x16/analysis.mp4` | see decisions.json | approved (Soft Blue) |
| `mixB.wav` | 95491901462e7fdb | approved voice (rebuild it locked to the new picture) |
| `cut.json` / `beats.json` | 1f5635247ad23960 / da9c6face242662a | 58.06 s talk + 0.85 s end hold; 18 pause cuts already applied, do not apply again |

Review page for round 1 stays up at http://127.0.0.1:8894/ until the video is finalized. Use a new port for round 2.

## Known risks

* Length has 0.09 s of room under 0:59; the AI clip must fit its slot, never stretch the film.
* Lower thirds and the CTA button cross Dan's chest (approved in the first 30 seconds).
* Keep the build inside the two-build cap; `capwait4.sh` waited 30 to 40 minutes on 10-13. Run chains in the background.

## Starter prompt (paste into a fresh Claude Code session)

> Read `Handoffs/handoff-20261013-ra04-round2-after-dan-review.md` and `.claude/skills/ad-edit/reference/ra04/README.md`,
> then run round 2 of RA-04 "Top 3 Tips For Getting Abs" (an AD) with /ad-edit. Name this task `Top 3 Tips AD R2`. My answers
> are recorded in the handoff. Fix the result card first, rebuild with the bass voice, then make the start and end frames for
> the broken-arm squat rack AI clip with the Codex subscription, put them on a review page and stop for my approval.

**Recommended model and effort: Opus 5.5, high.**
