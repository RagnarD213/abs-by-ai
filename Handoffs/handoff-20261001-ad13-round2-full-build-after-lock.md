# Ad 13 "The Cost Of Getting Abs", round 2: full vertical + 59s after Dan locks the look, then the square

Written 2026-10-01 by the round 1 session. Recommended: **Claude Opus 5.5, High**. Sidebar name: `The Cost Of Getting Abs AD R2`.
Fire only AFTER Dan has answered the round 1 page. Parent: `handoff-20261001-ad13-other-formats.md` (AV-11 + AS-10).

## Where round 1 stopped

Review page (graphic lock, nothing is a full film): `http://127.0.0.1:8813/` served from
`/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review/` (restart: `cd` there, `python3 -m http.server 8813`).
Dan owes three answers (the reply box): 1 look and words of the graphics (notes by ID), 2 the Thai shorts photo at 0:41
(keep or swap), 3 order of work (full vertical + 59s then a square look page, or the square look first).

## Read first

1. `.claude/skills/shortad-from-longform/reference/kit9x16/README.md`, section "An editor's master in Soft Blue Light".
2. `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `Handoffs/video-editing/00-RULES.md`.
3. `Handoffs/video-editing/AV-11-ad13-vertical.md`, `AS-10-ad13-square.md`.

## State (verified 2026-10-01)

- Build dir `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/`. Master: Muhammad's round 4 HD (already filed in the Ad 13
  folder; 7,339 frames, 4:04.878). Raw roll: 8/14 shoot `C1602.MP4` (99.4 % of his words).
- Done: recover, measure, content (no escalations), restyle (`sbl_copy.json` is the editorial copy file), setup, audio
  (his mix untouched), kit, base, track, graphics (20 HyperFrames graphics + card plates in `hf/`), labels, words,
  captions; first minute and one context clip per item in `review/`.
- NOT done: the full picture, mux, prewatch gate, three fresh judges, fold, labelcheck, cutdown, deliver, the square.
- Caption spellings were fixed in `ref.whisper.json` (the automatic one is `ref.whisper.auto.json`): do not regenerate it.
- Queue: AV-11 and AS-10 are `in_progress` (Claude). Spend so far: under one cent. No AI clips were generated.

## Work

1. Record Dan's answers verbatim in `review/decisions.json` (id, verdict, his words, scope). Apply copy or picture notes
   in `sbl_copy.json` only, then rerun from `restyle`:
   `kit_run.py --master "<master>" --build <B> --name "i added up what getting abs was supposed to cost | claude | 9x16 | ad 13" --sbl <B>/sbl_copy.json --from restyle --deliver "<Ad 13 folder>"`
   (stops for the judged watch pass; three fresh `ra-reviewer` judges; resume `--from fold`; then the cutdown chain).
2. Not yet proven on a Soft Blue Light master build: `kit_plan.py` (graphic regions and chips now come from
   `hf/manifest.json` and `hf/plates.json`), the gate pre-check, `kit_cutdown.py`. Expect to fix the kit, never a bound.
   Run `gate.py` detached. At most two builds at once on this machine.
3. Independent `ra-reviewer` on both delivered files before Dan sees them. Review copies + numbered action list.
4. Square (AS-10): the HyperFrames templates have no 1:1 layout yet (`vertical.py` is 9:16 only). Add the 1:1 layouts
   (3A card at the bottom, type 1.0x: locked 2026-09-28), show Dan one short square look page (his 10-01 rule), then
   build 1:1 full + 59s from the locked vertical per `a11_sq_ad1/` and the shared square rules.
5. Queue rows to `delivered`, mirror to the artifact, close the board line, delete this handoff's README row.

## Traps

- Do not upload anything. This is an ad (ends "Tap the button below"): Unlisted via `/ad-setup` only after approval.
- 52 % of the words are under graphics that pause captions; if the gate's caption rows object, shorten graphic times
  in the copy file (a `t1` phrase on a lower third), never the bound.
- `photo-137` (Thai shorts) is on the frowning list; it is in Muhammad's approved cut. Dan's answer 2 decides.

## Starter prompt

> Read `Handoffs/handoff-20261001-ad13-round2-full-build-after-lock.md` and the files it lists. Name this session
> "The Cost Of Getting Abs AD R2". Dan's answers to the Ad 13 round 1 page are: [paste the reply box]. Record them,
> apply them, build the full 9:16 and its 59 second cut through the gate, three fresh judges and an independent review,
> then the square look page and the two square files, and send me the review copies with a numbered action list.

Model and effort: Claude Opus 5.5, High.
