# AV-07 — Ad 10 "My Dad Bod At 38, My Dad Bod At 40": 9:16 vertical full + ≤0:59 cutdown

**List 3 · ad variant · READY · replaces J12.** Read `00-RULES.md` first. Dan's approval of this job unblocks AS-06 (Ad 10 square).

## What exists
* 16:9 (Muhammad): `… | muhammad | 16x9 | ad 10.mp4` in the Ad 10 folder, 1920×1080, 29.97, **5,443 frames, 3:01.6**, Drive `1582XKVpH-6LYq8fEJlFQksMZE0HL1Ct5`.
  Finalized 09-12 (same Upwork message as Ad 7). On YouTube + Demand Gen since 09-15.
* No vertical, square or cutdown exists.

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
* Real pictures of Dan: 0:08–0:11, 0:27.5–0:30, 1:46–1:48.
* Ad 10's demos were fixed in round 3 to show Dan's own before → Dan's goal image. Keep them as they are.
* Last notes: `revision docs/ad10-revisions-muhammad-round3-9-12-26.md`.

## Deliver
`my dad bod at 38 my dad bod at 40 | claude | 9x16 | ad 10.mp4` + `my dad bod at 38 my dad bod at 40 | claude | 9x16 59s | ad 10.mp4`, REVIEW 540p copies, audio A/B, stamps,
`notes-vertical.md`, `recipe-vertical/` into `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/`. Send Dan the review copies.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AV-07-ad10-vertical.md`: build the 9:16 vertical and ≤0:59 cutdown of Muhammad's finalized Ad 10 with /shortad-from-longform, decoding his master as BT.709 from the start, his audio untouched, the real-picture chip off my face and abs, before and after the same person. Every gate, independent audit, deliver, send me the review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/AV-07-ad10-vertical.md` using `.claude/skills/shortad-from-longform/SKILL.md` as the method and `Handoffs/handoff-20260914-ad3-square-codex.md` as the model of a Codex variant build. Deliver, send Dan the review copies, update `00-MASTER.md`.
