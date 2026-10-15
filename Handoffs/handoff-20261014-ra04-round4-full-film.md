AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Top 3 Tips AD R4`.

# RA-04 "Top 3 Tips For Getting Abs": round 4, Dan's call on the motion, then the full film

**Written 2026-10-14 by the round 3 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-04-top-3-tips-for-getting-abs.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe and lessons: `.claude/skills/ad-edit/reference/ra04/README.md` (round 3 = lessons 17 to 21; scripts in `round3/`).
Work folder: `/Volumes/Extreme/_edit_work/ra04/`. Decisions and hashes: `round3-plan/decisions.json` key `round3_motion`.
**Round 3 page: http://127.0.0.1:8898/** (served from `round3/`; restart with `python3 -m http.server 8898 --bind 127.0.0.1` there).

## Where round 3 left it

* **Motion built and reviewed, waiting on Dan.** Clip `media/ai1.mp4` (129 frames, sha in decisions), card `cards_9x16/brokenarm.mp4`
  with the AI-GENERATED chip at (60,236). Shots 1+2 are ONE 6 s take, `round3/motion/AI1-12_c.mp4` frames 4-104 (S1 to F3b: walk in,
  reaction at the bar, phone out on "use Abs By AI", reading). Shot 3 is `AI1-3_b.mp4` frames 60-87 (one leg press push, phone flat on
  his chest). 1.249x, every output frame a distinct source frame.
* **Reviews:** review 1 FAILED the first build (two takes joined at F2 jumped; `round3/review/REVIEW.md`). Review 2 PASSED the rebuild
  (`round3/review2/REVIEW.md`); frame gate PASS + reviewer PASS on the leg press push (`round3/gate/AI1-3_b.spec.json`,
  `gate.py ... --verify` exits 0).
* **Open judgement for Dan:** at the barbell he purses his lips as if blowing out air for about 0.75 s (clip frames 28-50), then a
  closed-eye frown. No take did a clean head shake.
* **Plan already changed for slot A:** `beats.json` knee card is now `brokenarm` [39.1391, 43.4434] (129 f); `dan08` 37.07-39.139
  (62 f, cx 1078.3); LT3 ends 39.1391 and was re-rendered (`r3_lt3.py`); captions rebuilt (`s07_captions.py 9x16`). Backups of the
  round 2 versions: `round3/backup/`.
* **Spend:** $5.80 of the $20 generation budget (12 Veo takes, `round3/motion/ledger.json`). $14.20 left.

## Next actions, in order

1. **Record Dan's answer** in `round3-plan/decisions.json` (`round3_motion.verdict`, his words).
   * **If he changes a shot:** regenerate with `round3/gen_motion04.py` (AI1-12 = shots 1+2 as one take; AI1-3 = leg press), check every
     take with `check_take04.py`, `strip04.py`, `platform04.py`, `selfchange04.py`, rebuild with `assemble04.py`, `s06_inserts04.py
     brokenarm`, `r3_context.py`, a FRESH `frame-reviewer` agent, then `page_r3.py`. Ask Dan before passing $20 total.
   * **If he approves:** go on.
2. **The full film** (handoff 10-13 step 3, unchanged): `s10_render04.py 9x16` (stage 1 must re-run: dan08 changed), mix locked to the
   picture (`r2_chain_a.sh` pattern, voice B), 16:9 from the same edit, land-then-hold check, `piccuts.py decide`, junk pass,
   `roll_sidecar.py mark-used`, edit sheet, `audio_gate.py` with the A/B, `deliver/gate.py --format ad9x16` and `ad16x9`, watch pass, one
   independent reviewer, negative-imagery scan, REVIEW 540p copies, delivery to `Claude Ad Videos/top 3 tips for getting abs - RA-04/`,
   a copy in `Videos to Review/`, `queue.py set RA-04 delivered` + artifact db, `clip_library.py add --used-in "RA-04"` for the AI clip.
   The 16:9 needs its own AI clip treatment (the clip is 9:16): decide fill vs plate with `clip_fit.py decide()`.
3. **Later-round revision list with timestamps** for Dan: 0:15 result card, the tip 3 clip (0:39.1 to 0:43.4), the voice.

## Known risks

* Two-build cap: `python3 .claude/skills/_shared/buildcap.py`; three other renders held slots during round 3. Run the chain in the
  background behind `capwait4.sh`.
* The round 3 preview reused the round 2 crop for dan08 (about 5 px off the final); check that hold's hair gate in the full render.

## Starter prompt

> Read `Handoffs/handoff-20261014-ra04-round4-full-film.md` and `.claude/skills/ad-edit/reference/ra04/README.md`, then run round 4 of
> RA-04 "Top 3 Tips For Getting Abs" (an AD) with /ad-edit. Name this task `Top 3 Tips AD R4`. My answer on the round 3 motion page:
> [approve / change shot N: ...]. Then build the full 9:16 and 16:9, every gate, independent review, and deliver.

**Recommended model and effort: Opus 5.5, high.**
