# AV-06 — Ad 7 "In 2010 I Photoshopped My Face On A Fitness Model. AI Just Did It For Real.": 9:16 vertical full + ≤0:59 cutdown

**List 3 · ad variant · READY · replaces J10.** Read `00-RULES.md` first. Dan's approval of this job unblocks AS-05 (Ad 7 square).

## What exists
* 16:9 (Muhammad): `… | muhammad | 16x9 | ad 7.mp4` in the Ad 7 folder, 1920×1080, 29.97, **6,358 frames, 3:32.1**, Drive `1mTizfbX4Uk97EwJOF_uO3KBp1P3PToh1`.
  Dan in Upwork 09-12: *"Both HD videos at 7 and 10 are looking good, and those are finalized."* On YouTube + Demand Gen since 09-15.
* ⚠ **Muhammad still owes a corrected HD** (round 5, 09-15): the chip reads "AI-GENERATEd" at 2:48–2:51. Check the ad folder and
  `.claude/skills/editor-deliveries/state.json`. If the corrected HD has been filed, build from it. If not, build from the current
  file; our vertical re-renders that chip anyway, so spell it right and note it in `notes-vertical.md`.

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
* Real pictures of Dan: 0:48.5–0:50.6 and 2:20.5–2:24.
* **3:25.5–3:29, the closing demo:** Muhammad's cut plays Dan's own generation under "So generate your future self image".
  Rebuild that beat as the app-recording man's upload ending on **his** AI after picture (`1gFwcbYiRvoGQz1WJ7oKj-T7dRAM2zRPp`).
  That was Dan's 09-12 note, and it matches the same-person rule.
* The other app demos already show Dan's before → Dan's goal image. Keep them.
* Last notes: `revision docs/ad7-revisions-muhammad-round4-9-12-26.md`.

## Deliver
`in 2010 i photoshopped my face on a fitness model ai just did it for real | claude | 9x16 | ad 7.mp4` + `in 2010 i photoshopped my face on a fitness model ai just did it for real | claude | 9x16 59s | ad 7.mp4`, REVIEW 540p copies, audio A/B, stamps,
`notes-vertical.md`, `recipe-vertical/` into `Muhammad Ad Videos/in 2010 i photoshopped my face on a fitness model ai just did it for real - ad 7/`. Send Dan the review copies.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AV-06-ad7-vertical.md`: build the 9:16 vertical and ≤0:59 cutdown of Muhammad's finalized Ad 7 with /shortad-from-longform, decoding his master as BT.709 from the start, his audio untouched, the real-picture chip off my face and abs, before and after the same person. Every gate, independent audit, deliver, send me the review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/AV-06-ad7-vertical.md` using `.claude/skills/shortad-from-longform/SKILL.md` as the method and `Handoffs/handoff-20260914-ad3-square-codex.md` as the model of a Codex variant build. Deliver, send Dan the review copies, update `00-MASTER.md`.
