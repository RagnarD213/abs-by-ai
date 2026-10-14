AD (paid ad: it ends on "Tap the button below now to get started"). Sidebar name for the next task: `Best Ab Exercise AD R2`.

# RA-06 "What's The Best Ab Exercise?": round 2, after Dan reviews the round 1 page

**Written 2026-10-14 by the round 1 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-06-whats-the-best-ab-exercise.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe: `.claude/skills/ad-edit/reference/ra06/` (README: stage order and seven lessons).

**Do not fire this until Dan has replied to the round 1 page.** His reply goes, word for word, into
`/Volumes/Extreme/_edit_work/ra06/round2-plan/decisions.json` before anything is built.

## Where it stands

Round 1 is with Dan: **http://127.0.0.1:8806/** (managed review service, folder `/Volumes/Extreme/_edit_work/ra06/round1/`),
and a VLC copy in `Videos to Review/Best Ab Exercise AD R1 - full ad draft.mp4` (delete it when the ad is finalized).
The ad is 45.7 s, so the round 1 sample is the WHOLE 9:16 ad, built with Dan's RA-14 picks. Audio gate PASS on the draft
(12 of 12, -14.2 LUFS). An independent reviewer said DOES NOT SHIP on the first build (`review_r1/ROUND-1-REVIEW.md`, 12 items); ten were fixed and a second reviewer confirmed nine (`review_r1b/ROUND-1B-REVIEW.md`); the tenth ("make your abs real" ~5 dB low) and its new note (captions on the toe-touch rep) were fixed after it and checked by the editor only: the phrase now measures -15.6 LUFS against -14.6 and -12.7 either side, and the split order is spiderman / toe touches / vacuum with the captions on his chest. Not yet: the delivery
gate, the watch pass, the edit sheet, the 16:9, the delivery folder. Queue state: `in_progress`. Spend: $0 of the $10 ad cap.

## The three decisions waiting for Dan

1. **Look:** A (in the ad) his RA-14 picks: colour C2 brighter gold, shot pair 2 (close 648x1152, wide 810x1440), voice
   with the bass lift. B: he names another from the sheets (`look/sheet_close.jpg`, `sheet_wide.jpg`, `sheet_crops.jpg`,
   `voice_A_bass.m4a` / `voice_B_no_bass.m4a`).
2. **Claim lines as spoken** (captions only): "thousands of guys have FIRED their trainer" (0:20.0), "the generic plans
   that human personal trainers give you always fail" (0:11.3), "you'll get far better results" (0:31.2). A keep all.
   Cutting the first takes the A0147 robot card with it (about 3.5 s shorter); re-plan from `edl_spec.json`.
3. **Five AI clip ideas, yes or no each** (frames next round on the Codex subscription, no motion before he approves
   frames): 1 the copier (0:11.3-0:15.6), 2 one-size tracksuit (0:15.6-0:20.0), 3 body scan (0:06.0-0:11.3), 4 robot
   waves goodbye (0:41.5-0:43.6), 5 exercise wheel opener (0:00-0:02.3, alternative to the split screen). Full scene text
   in `page_notes.json`. A yes replaces Dan on camera for that span: re-plan `s05_plan06.py` `CARDS` and re-render.

## Next action (round 2)

1. Record his reply. Re-hash the files below before touching anything; build in `round2/`.
2. Apply his picks (a different colour: `grade.json` `filter` from `colour/looks.json`; a different pair: `framing_choice.json`
   then `s04b_holdstart.py beats.json` again; no bass: `cp mix_nobass.wav mix.wav` after re-running stage 3).
3. AI ideas he said yes to: START and END frames with `.claude/skills/_shared/codex-image.sh` (9:16, subject in the centre
   third, ordinary non-model faces, no stomach framing, no generated lettering, idea 4 reuses A0147's two characters).
   Show the frames and stop.
4. When nothing is pending: the 16:9 from the same edit (`ra01lib.Aspect("16x9")`, fixed crops per the horizontal rule;
   the split screen needs a 16:9 layout: three panels side by side cannot hold a lying man, so stack two over one or run
   them as a 3-up row of 16:9 thumbnails on the field), the edit sheet for the 16:9, `deliver/gate.py --format ad9x16` and
   `ad16x9`, the watch pass, a fresh independent review of both files, REVIEW 540p copies, notes, delivery folder
   `Claude Ad Videos/whats the best ab exercise - RA-06/` (`… | claude | 9x16 | RA-06.mp4`, `… | claude | 16x9 | RA-06.mp4`),
   `queue.py set RA-06 delivered` + the artifact db, `roll_sidecar.py mark-used` for C1664 313.36-335.01 and
   340.94-368.64 plus the three B-roll ranges, clip library `add --used-in "RA-06"` for the split-screen cuts.

## Known risks, stated plainly

- The two lower thirds and the button sit across his chest and upper abs (the vertical kit's 68 % position), same as
  RA-04 and RA-05 round 1. Dan has not ruled on it yet on those pages.
- Land-then-hold motion per hold (travel px / p90 px/s / share of time moving): dan02 207/103/76 %, dan05 91/108/100 %,
  the rest under 55 px of travel. Max head offset 58 px of a 648 px crop (9 %), median 10-32 px.
- The robot clip A0147 is a 720x1280 original sharpened to 1080x1920 (no local upscaler on this Mac).

## Files (work folder `/Volumes/Extreme/_edit_work/ra06/`, sha256 first 16; re-hash before touching)

| file | sha256 (first 16) | what |
|---|---|---|
| `round1/DRAFT - RA-06 round 1 - full ad.mp4` | ba0f647e2e175ee3 | what Dan is reviewing (45.71 s), a copy of `draft_9x16.mp4` |
| `draft_9x16.mp4` | ba0f647e2e175ee3 | the draft, audio gate stamp beside it |
| `picture_9x16.mp4` | f8e7ca39be8525cd | its picture, 1,370 frames |
| `mix.wav` | 0e7e79bb22df9815 | fitted tone + bass lift + Realizer bed at -32, rides (`RIDE`): +2 dB on "An AI trainer can design...", +2.5 dB on "Then get a personalized...", +7.5 dB in total on "make your abs real", -14.2 LUFS |
| `mix_nobass.wav` | 6b6afa423deabaab | option B voice |
| `cut.json` | d04eb8248c43b42a | 45.41 s of talk + 0.30 s end hold, 13 pause cuts, seam 19.95 s |
| `edl_spec.json` | a4ad68bb2859973a | take map: R1 313.36-335.0, R2 340.94-368.3 |
| `tx/c1664.whisper.json` | 25f98ea8b65740ff | Replicate large-v3 words 309-372 s, re-timed by `s02b_patch.py` |
| `words_aligned.json` | 81e037428419e01a | 156 words, CTC aligned to `mix.wav` |
| `framing.json` / `framing_holdstart.json` | 0f4b77eeeb288ad9 / ea07a3be1d72e0d7 | head track, hold-edge samples |
| `beats.json` | e21e5fe2d080afdf | 7 cards (44.0 % coverage), 10 Dan holds, 2 lower thirds, button |
| `grade.json` / `framing_choice.json` | 3842c625c2b4fb45 / 6bd9c52cf20a95e5 | C2 look, pair 2 |
| `cards_9x16/split.mp4` | f5a82cc5f722575a | the three-exercise opener |
| `round1/index.html` | 76b2d9e35c3d0407 | the review page |

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Best Ab Exercise AD R2`. Read `Handoffs/handoff-20261014-ra06-round2-after-dan-review.md` and
> `.claude/skills/ad-edit/reference/ra06/README.md`, then continue RA-06 "What's The Best Ab Exercise?" with /ad-edit. My
> answers to the round 1 page are: [paste the reply box]. Record them word for word first and apply them. Make frames for
> any AI clip I said yes to and stop for my approval; if nothing is pending, build the 16:9 from the same edit, run every
> gate and the independent review, deliver both files, and send me the review copy. Use the Codex subscription to
> generate the images.

**Recommended model and effort: Opus 5.5, high.** A recipe-backed build with one new 16:9 layout and the full gate set.
