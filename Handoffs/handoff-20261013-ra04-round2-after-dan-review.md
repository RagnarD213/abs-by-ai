AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Top 3 Tips AD R2`.

# RA-04 "Top 3 Tips For Getting Abs": round 2, after Dan reviews the round 1 page

**Written 2026-10-13 by the round 1 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-04-top-3-tips-for-getting-abs.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.

## Where it stands

Round 1 is with Dan: **http://127.0.0.1:8894/** (managed review service, folder `/Volumes/Extreme/_edit_work/ra04/round1/`).
The page shows the finished first 30 seconds, every graphic and clip as a still with a play-in-context button, two analysis
card colour options, two voice options, a "What I decided" list and four decisions. **Dan has not replied yet.**
No full film has been shown to him (the round method). A full 9:16 draft exists in the work folder for internal checks only.

Nothing is gated, stamped, audited, delivered or uploaded. Queue state: `in_progress`. Spend: $0.

## The four decisions waiting for Dan

1. "Completely free" at 0:17: keep as filmed (in the cut) or cut the two words (clean cut, 1.3 s shorter).
2. Analysis card colours: Soft Blue (in the cut) or the RA-01 olive.
3. Voice: the RA-01 sound (in the cut, `mix.wav`) or with the +3 dB bass lift at 120 Hz (`mixB.wav`).
4. Tip 3 pictures: the real clips (in the cut) or AI frames for "Gym is closed" and "Tweaked back".

When he replies, write `round2-plan/decisions.json` first (ID, path, sha256, verdict, his exact words), per PRE-RENDER-APPROVAL.

## What exists (work folder `/Volumes/Extreme/_edit_work/ra04/`)

| file | sha256 (first 16) | what |
|---|---|---|
| `round1/DRAFT - RA-04 round 1 - first 30 seconds.mp4` | a7b8880b81e3f623 | what Dan is reviewing (31.16 s, ends with the analysis card) |
| `draft_9x16.mp4` | 247eaaba3b415ec5 | internal full 9:16 draft, 58.89 s, not shown to Dan |
| `picture_9x16.mp4` | e566988a6a6314a4 | its picture |
| `mix.wav` / `mixB.wav` | aa2c78a9a78d1954 / 95491901462e7fdb | voice A (RA-01 chain) / voice B (bass lift) |
| `cut.json` | 1f5635247ad23960 | the airtight cut: 58.06 s of talk + 0.85 s end hold |
| `beats.json` | da9c6face242662a | cards, Dan holds, lower thirds, CTA |
| `hf9/` | manifest 03a84b747f9f9d9c | Soft Blue overlays and phone plates (HyperFrames) |
| `cards_9x16/` | | the seven insert cards (+ `analysis_olive.mp4`) |

Recipe and lessons: `.claude/skills/ad-edit/reference/ra04/` (README has the stage order and what this ad taught).

## The cut, for the record

* Roll `C1664.MP4` (8/28 portrait outdoor roll, dual-mono lav; `pick_lav.py` JSON beside the roll).
* Takes: R1 77.34-90.72 (L1 to "like this"), R2 108.24-123.02 ("Just go to..." take 2, tip 2 opener), R3 129.41-135.94
  ("The Abs By AI app can tell exactly..." take 2), R4 152.94-175.67 ("And you can use it..." take 2, all of tip 3),
  R5 183.02-190.35 (call to action, take 2). 18 pause cuts are already applied in `cut.json`: do not apply them again.
* Colour: RA-01's `grade.json` (1.15x LUT, saturation 1.25), checked side by side on this roll.
* Graphics: three TIP lower thirds, a glass CTA button, three phone plates (`gfx04.py`). Captions: RA-01 style with a cyan highlight.
* Clips (clip library): A0074 lock screen (AI, chip), B0049 app flow (same man before and after; crop screen, "Meet the new
  you" and the email form are left out), B0544 app tour, B0126 knee brace (stock), B0464 Dan's squats. Analysis card
  subject = the app man's result picture.

## Next action (round 2)

1. Read Dan's reply. Record decisions. Re-hash the files above (expected vs actual) before touching anything; build in `round2/`.
2. Apply his changes. If he cuts "completely free": add the span to the cut (the pause before "completely" is 0.28 s),
   rerun stages 3 to 12 of the recipe; card and graphic times follow from phrases.
3. If he wants AI frames: make START and END frames with `.claude/skills/_shared/codex-image.sh` (9:16, subject in the
   centre third, no belly framing), show them, stop. No motion before he approves frames. Ad budget: $10 total.
4. When nothing is pending, build the full film: 9:16 master, then the 16:9 from the same edit (`ra01lib.Aspect("16x9")`;
   the phone plates and lower thirds need their 16:9 layout: `from_plan.py` / `ad13-r2/h16x9_full.py` are the models).
5. Final-round work this round did NOT do: land-then-hold centring check (`cut/landing.py motion_stats`; crops are fixed per
   hold now), `piccuts.py decide`, the junk pass on the final cut, `roll_sidecar.py mark-used`, the edit sheet for the 16:9,
   `audio_gate.py` with the A/B clip, `deliver/gate.py --format ad9x16|ad16x9`, the watch pass, one fresh independent
   reviewer (give it the three AI-clip sense questions for A0074), the negative-imagery scan, REVIEW 540p copies, notes,
   recipe folder, the delivery folder `Claude Ad Videos/top 3 tips for getting abs - RA-04/`, a copy in `Videos to Review/`
   (the full ad is over 45 s), `queue.py set RA-04 delivered` + artifact db, clip library `add --used-in "RA-04"`.

## Known risks, stated plainly

* The lower thirds and the CTA button sit across Dan's chest (the kit's 68 % position). He is shirtless in every shot,
  so there is no clear band. It follows the approved vertical kit; Dan sees it in round 1.
* The three "Number one / two / three," shots are 0.6 s punch-ins. They exist because a pause was cut there and a
  same-size splice is a jump cut. If Dan dislikes them, the alternative is to keep those three pauses (0.53 s) and cut a line.
* Length has 0.09 s of room under 0:59. Any added pause needs time taken somewhere else.
* The fitted voice EQ already lifts the lows to the reference; voice B may read boomy on his loudest lines.
* Face sharpness: these rolls upscale 1.5x to 1.8x in 9:16 (same as RA-01, which Dan approved).

## Starter prompt (paste into a fresh Claude Code session)

> Read `Handoffs/handoff-20261013-ra04-round2-after-dan-review.md` and `.claude/skills/ad-edit/reference/ra04/README.md`, then
> continue RA-04 "Top 3 Tips For Getting Abs" (an AD) with /ad-edit. Name this task `Top 3 Tips AD R2`. My answers to the
> round 1 page (http://127.0.0.1:8894/) are: [paste the reply box]. Record them, apply them, and if nothing is pending
> build the full 9:16 and the 16:9 from the same edit, run every gate and the independent review, deliver, and send me
> the review copy.

**Recommended model and effort: Opus 5.5, high.** A bounded revision plus a recipe-backed full build with gates.
