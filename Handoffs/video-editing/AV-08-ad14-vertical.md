# AV-08 — Ad 14 "I Watched 400 Workout Videos And Gained Weight": 9:16 vertical full + ≤0:59 cutdown

**List 3 · ad variant · READY (file the 09-16 HD first) · replaces J17.** Read `00-RULES.md` first. Dan's approval of this job unblocks AS-07 (Ad 14 square).

## What exists
* **Build from Muhammad's real HD, delivered in Upwork on 2026-09-16.** The file currently in the Ad 14 folder is the 3.0 Mbps
  "V3" (5,924 frames, 3:17.7, Drive `1VQuOxzfbmXv_TgO5GgURXrLkkwusU6_k`), a review-grade encode that went to YouTube/Demand Gen on 09-15.
* **Step 0:** if the 09-16 HD isn't filed yet, run `/editor-deliveries` for it (Muhammad's room; resolve his message links,
  because Drive search can't see his files), move the V3 into `old versions/`, and confirm the HD is the approved round-3 cut
  (`hd_vs_draft.py`, VERDICT IDENTICAL, or list the differences). Replacing the live YouTube/Ads copy is a separate
  `/ad-setup` step (already on the board), not part of this job.
* ℹ️ Codex's private "Ad14 R1" in `Media/codex-video-trial/06-ad-r1/` is a **trial re-edit** of the same script. It isn't this
  ad and it doesn't block this job. Don't touch its directory.

## Build (same method for every new Muhammad vertical)
`/shortad-from-longform` end to end. Step 0b's "approved draft" is the editor's HD itself, since Dan approved the delivered cut.
* **Colour: decode as BT.709 from the start.** Copy the Ad 3 render-10/12 compositor out of `/Volumes/Extreme/_edit_work/ad3-vert/`
  into your own `_edit_work/<job>/`. Never start from `ad4-vert/` or `ad5-vert/`, whose grades carry the BT.601 fault.
* **Audio: Muhammad's, untouched** (`--verbatim`); the cutdown is his mix cut at the seams only.
* **Labels:** our real-picture chip is the same solid black rounded pill as AI-GENERATED, upright, inside the picture, **never over
  face or abs**. Muhammad's own version (italic, square brackets, see-through band) is not to be copied. Re-verify every
  timestamp below against the delivered master before placing anything.
* **Same person:** wherever the ad uses the app recording (it uploads a man who is not Dan), his upload must end on his own AI after
  picture (`1gFwcbYiRvoGQz1WJ7oKj-T7dRAM2zRPp`, AI-GENERATED chip), never Dan's, never the email screen.
* **Cutdown ≤0:59:** hook, problem, AI demo, payoff, CTA. Seams snap to silence and to HIS picture cuts, never inside a light leak.
  Prove every seam against the master. Check the CTA-pill trailing-caption overprint on both files.
* `compliance:banned_screen` over every frame, a full-resolution watch pass, all gates at the current version, independent audit.
* The square (AS job) is a re-layout of THIS build after Dan approves it, so keep the build dir intact.

## This ad's specifics
* Real pictures of Dan: 0:56 (Age: 40, label beside the tag), 0:57.5, 0:58.5, 0:59.5. Re-measure these on the HD; round 3 may have shifted them.
* The closing flow was fixed in round 2 to end on the recording man's own AI after picture. Confirm it in the HD.
* Last notes: `revision docs/ad14-revisions-muhammad-round2-9-12-26.md` + round 3 (09-15, *"APPROVED - FINALIZED - READY FOR HIGH QUALITY EXPORT"*).

## Deliver
`i watched 400 workout videos and gained weight | claude | 9x16 | ad 14.mp4` + `i watched 400 workout videos and gained weight | claude | 9x16 59s | ad 14.mp4`, REVIEW 540p copies, audio A/B, stamps,
`notes-vertical.md`, `recipe-vertical/` into `Muhammad Ad Videos/i watched 400 workout videos and gained weight - ad 14/`. Send Dan the review copies.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AV-08-ad14-vertical.md`: build the 9:16 vertical and ≤0:59 cutdown of Muhammad's finalized Ad 14 with /shortad-from-longform, decoding his master as BT.709 from the start, his audio untouched, the real-picture chip off my face and abs, before and after the same person. Every gate, independent audit, deliver, send me the review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/AV-08-ad14-vertical.md` using `.claude/skills/shortad-from-longform/SKILL.md` as the method and `Handoffs/handoff-20260914-ad3-square-codex.md` as the model of a Codex variant build. Deliver, send Dan the review copies, update `00-MASTER.md`.
