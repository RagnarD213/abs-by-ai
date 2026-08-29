# Handoff — cover images for the 5 ab-wheel Shorts

- **Handing off from:** Claude Code (2026-08-28, the session that cut and finalized the shorts)
- **Handing off to:** Claude Code, fresh session
- **Reason:** The five shorts are approved and final. Covers were never built and are the last
  thing between them and being scheduled.
- **Skill:** invoke **`/coverimage`** — it is self-contained and holds the locked type system,
  the geometry, the asserts and the two platform layouts. **Do not redesign anything.**
- **Model/effort:** Sonnet 5, or Opus if the photo search turns out to need judgement. This is
  execution against a settled spec, not design.
- **Spend:** $0 if a photo is used. ~25c per retouched video frame (`nano-banana-pro`,
  standing-authorised). Expect **$0.00–$1.25** total.
- **Not a native-retest trigger.** No production code, no deploy.

---

## What exists already

**The five finished shorts** (1080x1920, 29.97 fps), in `Short-form video content/`:

| # | file | pre-title (eyebrow) | headline | runtime |
|---|---|---|---|---|
| 1 | `abwheel-short1_ab-wheel-beats-crunches.mp4` | THE BEST HOME AB EXERCISE | WHY I LOVE THE AB WHEEL | 0:33.7 |
| 2 | `abwheel-short2_biggest-ab-wheel-mistake.mp4` | FIX THIS FIRST | THE BIGGEST AB WHEEL MISTAKE | 0:48.0 |
| 3 | `abwheel-short3_beginner-to-advanced.mp4` | MY FAVORITE HOME AB EXERCISE | HOW TO DO AB WHEEL ROLLOUTS | 0:54.0 |
| 4 | `abwheel-short4_youre-rolling-too-fast.mp4` | INTENSE HOME AB EXERCISE | HOW FAST TO ROLL OUT WITH THE AB WHEEL | 0:32.3 |
| 5 | `abwheel-short5_hits-every-ab-muscle.mp4` | ULTIMATE HOME AB EXERCISE | WHY THE AB WHEEL BEATS CRUNCHES | 0:31.9 |

**Full context:** `YouTube Long Form Video Content/abwheel-17-dollar-ab-wheel/SHORTS.md`.
**Source longform:** `/Volumes/Extreme/_edit_work/abwheel/mrepro/ref_hd.mp4` (6:58, 1920x1080).
**Word timings for locating a topic in it:**
`/Volumes/Extreme/_edit_work/abwheel/shorts-r2/work/words.json` (`chunks[].timestamp`).
⚠ **Mount the Extreme SSD first** — it has detached mid-task twice this week.

---

## The job

Ten files: an **Instagram** and a **YouTube** cover for each of the five, per `/coverimage` §7.
Copy `posted covers/_build-covers-batch2-final.py` and adapt its config; the YouTube builder
**imports** that config rather than copying it, and it must stay that way.

Output to `Short-form video content/covers/posted covers/` (and `.../youtube/`) as
`abwheel-short<N>_<slug>_cover-<X>.png`, with the build script saved beside them.

**Two variants per short**, same photo and crop, differing only in copy. No approval gate before
building — Dan judges the finished covers.

---

## Copy: start from what is already burned into each short

`/coverimage` says cover copy comes from the short's own on-screen graphic first. **That copy is
in the table above and it is Dan's own wording** — shorts 3, 4 and 5 verbatim, 1 and 2 his
approved rewrites. It maps straight onto the locked hierarchy:

- **eyebrow** (Copperplate, olive) ← the pre-title
- **headline** (Impact, white, the specific line) ← the title
- **subtitle** (Impact, olive) — optional; drop it where the headline needs the room

⚠ **Short 4's headline is long** ("HOW FAST TO ROLL OUT WITH THE AB WHEEL"). The rule is **two
lines, never three** — raise `head_size` and let `fit()` shrink to the column, or shorten to
something like `ROLL OUT THIS SLOW` and keep the full phrase as the subtitle. Do not let it run
to three lines.

---

## Photo search — the part that needs eyes

Order: `photos/finalized social media photos/` (228 images) → the ab-wheel longform itself.
**Never** `photos/finalized dating photos/`.

⚠ **There is probably no ab-wheel photograph.** The finalized library is pool/studio portrait
work; nobody has shot the ab wheel as stills. The skill's own rule handles this: **prefer a photo
generally, not only on an exact topic match** — abs first, topic second. A strong upright physique
photo beats a mediocre on-topic video frame every time.

⚠ **CHECK THE 8/28 STUDIO SHOOT BEFORE DEFAULTING TO THE OLD LIBRARY.**
`photos/studio shoot | 8-28-26 | dan | mindi/` was shot **today** and another session
("Studio photo shoot editing") is selecting from it right now. If finished picks have landed
there, they are the freshest and best-lit sources available. Coordinate rather than duplicate —
read `AI_COORDINATION.md` before starting.

**Look, don't grep.** Colour-signature searches have already failed once on this task family.
Build the contact sheet in `/coverimage` §2 and read it.

### If you fall back to a video frame

Pull from **`ref_hd.mp4`, never the finished short** — the shorts have burned word captions
across the abs. Then two traps specific to THIS source, both measured while cutting the shorts:

- ⚠ **The rollout itself crops terribly.** Measured over every frame: during a rollout Dan spans
  **0.03 → 0.97 of the 16:9 width**, lying flat. There is no vertical crop of that pose. Use the
  **kneeling and standing talking beats** instead — upright, abs lit, and there are plenty.
- ⚠ **Muhammad's burned graphics are wide.** Top pills run x 0.037–0.956, the lower thirds
  x 0.097–0.969, and the left muscle panel to x 0.39. Pick a frame with **no** graphic rather
  than trying to crop around one. Clean windows: roughly 0:00–0:22, 1:04–1:07, 2:12–2:44,
  2:57–3:18, 4:00–4:12. Verify before committing —
  `/Volumes/Extreme/_edit_work/abwheel/shorts-r2/shots/geom.json` has a per-shot graphic box.

Retouch any video frame per `posted covers/_retouch-prompt.txt`.

---

## The five rules that get covers rejected

All are enforced in the build script, not by eye. Read `/coverimage` §4–6 in full; these are the
ones Dan has personally rejected work over:

1. **Abs decide it.** On-topic and technically clean is still a FAIL if the abs don't read.
2. **Never hunched, folded or soft.**
3. **Never crop the top of his head** — add a `HEAD_TOP` row for any new photo or the assert
   cannot protect you.
4. **Headline on two lines, never three.**
5. **The type block is CENTRED in the black band and never touches the photo.** Parking it at the
   bottom of a tall band is the single thing he has rejected most.

Plus: abs must stay **above y=1680** (Instagram crops the tile to 3:4), wordmark bottom-**right**,
and `git check-ignore` the output path before staging anything — the repo is public and these are
Dan's personal photos.

---

## Exact next action

1. Mount the Extreme SSD; read `AI_COORDINATION.md`; invoke `/coverimage`.
2. Check the 8/28 studio shoot for finished picks, then contact-sheet
   `photos/finalized social media photos/` and choose five sources on abs first.
3. Build 2 Instagram variants x 5 shorts, then port to the YouTube layout.
4. Send all of them to Dan in chat and let him pick.

**Do NOT install on YouTube** — §8 is explicit that it happens only when Dan asks.

## Risks

- The Extreme SSD detaching mid-run. A byte-identical copy of the longform is **not** guaranteed
  to be on the internal drive any more; the duplicate in `Muhammad Organic Videos/` was flagged
  for deletion.
- Another session is working the same photo library today. Don't move or rename anything in it.
- ⚠ Something on this Mac creates ` 2.png` / ` 2.mp4` conflict copies in these folders. **Check
  the covers folder for duplicates before telling Dan a batch is done** — five superseded shorts
  masters reappeared beside the finals during the last task.
