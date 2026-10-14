AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Top 3 Tips AD R3`.

# RA-04 "Top 3 Tips For Getting Abs": round 3 (after Dan answers the round 2 frames page)

**Written 2026-10-14 by the round 2 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-04-top-3-tips-for-getting-abs.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe and lessons: `.claude/skills/ad-edit/reference/ra04/README.md` (lessons 13 and 14 are new). Work folder: `/Volumes/Extreme/_edit_work/ra04/`.
Round 2 page: http://127.0.0.1:8895/; round 2b page (new shot 3 only): http://127.0.0.1:8896/. Frame hashes: `round2/frames_manifest.json`.

## Dan's answers so far (2026-10-14), recorded in `round3-plan/decisions.json`

* **Shots 1 and 2 frames approved** (S1 0fb43996d74b3b4f, F2 157edd1096409c06, F3b 802a4c9e7014614c): "All of the frames are looking good except for shot 3."
* **Shot 3 rejected** (F4b/F5b): "that's not how a leg press machine is loaded... he's putting his foot on the plates rather than the platform."
  He asked for a realistically loaded machine, feet on the platform, start smiling at the phone, end smiling while exerting, and
  **"If this physics is off, you have to regenerate."** New pair on the 2b page, pending his OK: **F4c_a** 75170719eae9b0a2 (start) and
  **F5c_b** 4051998b79f4fdb2 (end, an edit of F4c_a; plates and platform move up the rails as one piece).
* **Budget raised to $20 for this ad** ("Your budget is approved up to $20 for generations"). $0 spent.
* Slot not answered: **A** (0:39.139 to 0:43.443) is the default, said on the 2b page.

## Step 0: record Dan's answer on the 2b page

Add his words on shot 3 (F4c_a / F5c_b) to `round3-plan/decisions.json`. If he asks for changes: regenerate only shot 3, END derived
from START (lesson 13), check the leg press physics (one platform on the sled, plates only on side horns, feet on the platform, sled
and plates moving as one piece), back on a page, stop again.
If he says no to the clip: B0126 stays (as in round 1) and go straight to step 2.

## Done in round 2 (do not redo)

| item | state | sha256 (first 16) |
|---|---|---|
| `cards_9x16/flow_b.mp4` | B0049 from 28.0 s. Round 1 had the banned "Meet the new you" screen for 8 frames; every frame of flow_a, flow_b, tour scanned: 0 left | 25071b27d5c22e0d |
| `mix_r2.wav` | voice B (fitted EQ + `equalizer=f=120:t=q:w=0.8:g=+3.0`), locked to the picture; sample-identical to approved `mixB.wav` (corr 1.0000) | 62dea6861a358d46 |
| `round2/draft_r2_9x16.mp4` | full 9:16 with the knee clip still in tip 3. Internal only, never shown to Dan | cdcd88337698319c |
| Locks re-hashed at round 2 start | analysis.mp4 f12f181b2c26cdd2, mixB 95491901462e7fdb, first-30 a7b8880b81e3f623, cut.json 1f5635247ad23960, beats.json da9c6face242662a | all matched |

`cut.json` already carries the 18 pause cuts: never apply them again. Picture length 58.88 s (0.09 s under 0:59).

## Round 3 work, in order

1. **Motion (after frame approval):** three takes on Replicate `google/veo-3.1-fast`, `image` + `last_frame`, 9:16, 4 s, no audio,
   $0.40 each. Template: `.claude/skills/longform-edit/reference/ro06/gen_motion.py` (assert each frame's sha256 against the decisions
   file; ledger every call). Pairs: AI1-1 S1 to F2 (walks to the rack, stops, shakes his head); AI1-2 F2 to F3b (finishes the shake,
   takes out the phone, reads it); AI1-3 F4c_a to F5c_b (glances up from the phone, still smiling, one push of the leg press). Prompts: plain actions, Step 4.5 vocabulary (no camera
   or film words), "camera stays still".
   Slots (slot A): AI1-1 39.139 to 41.374 under "when life gets in the way. When you get injured,"; AI1-2 41.374 to 42.509 under
   "use Abs By AI to"; AI1-3 42.509 to 43.443 under "adjust your plan." Trim each take to its best-flowing part; a slight speed-up is
   allowed, slowing or holding is not. Slot B: same three shots squeezed into 3.1 s (about 1.0 s each), or ask.
2. **Before Dan sees motion:** every take gets the three sense questions (cause and effect, reads with the sound off, shows the line),
   the self-change map (`longform-edit/reference/ro08/a5_cut.py`), first and last second strips, then a fresh independent reviewer
   with the three questions in its brief. Fix failures by retake or trim. Budget **$20 for this ad, $0 spent so far** (frames were
   Codex). Ask Dan first, alone, before passing $20. **Shot 3 physics is Dan's named check:** the platform, horns and plates move up
   the rails together, both feet stay on the platform, the phone stays in his hand. Any take that breaks it is regenerated, never trimmed around.
3. **Build the card:** replace the `knee` card (`s05_plan04.py` beat, `s06_inserts04.py fill_card`) with the AI clip, AI-GENERATED chip
   placed by looking at the man (top corner clear of him; RA-07 lesson 7). Slot A also shortens LT3 to end at 39.139 (check the copy
   "Let AI Fix What Gets In Your Way" still has 1.9 s on screen from 37.205). Captions run over the clip; check them against the man.
   Show the finished motion in context on a round 3 page (only what changed), then stop, unless Dan approved motion in advance.
4. **Then the full film** (handoff 10-13, step 3, unchanged): 9:16 master, 16:9 from the same edit, land-then-hold check,
   `piccuts.py decide`, junk pass, `roll_sidecar.py mark-used`, edit sheet, `audio_gate.py` with the A/B, `deliver/gate.py --format
   ad9x16` and `ad16x9`, watch pass, one independent reviewer, negative-imagery scan, REVIEW 540p copies, delivery to
   `Claude Ad Videos/top 3 tips for getting abs - RA-04/`, a copy in `Videos to Review/`, `queue.py set RA-04 delivered` + artifact db,
   `clip_library.py add --used-in "RA-04"` for the AI clip. Later-round revision list with timestamps: 0:15 result card, the tip 3
   clip, the voice.

## Known risks

* Shot 3 is 0.9 s: one push of the sled. If the take's push is slow, use its fastest stretch, or ask to move a word boundary.
* Veo has flagged generated faces as "celebrity likeness" before (ad-edit lesson 110): a three-quarter retake usually passes; filtered
  attempts are free.
* Two-build cap: `python3 .claude/skills/_shared/buildcap.py`; run long chains in the background behind `capwait4.sh`.

## Starter prompt

> Read `Handoffs/handoff-20261014-ra04-round3-after-frames.md` and `.claude/skills/ad-edit/reference/ra04/README.md`, then run round 3
> of RA-04 "Top 3 Tips For Getting Abs" (an AD) with /ad-edit. Name this task `Top 3 Tips AD R3`. My answers to the round 2 page:
> [paste your reply to the 2b page]. Generate the motion for the approved frames, check every take before I see it, and put it in context on a review page.

**Recommended model and effort: Opus 5.5, high.**
