# Soft Blue Shorts title band: clipped descenders audit (2026-10-22)

**Dan's ruling (2026-10-22): close enough, fix going forward only.** The 11 delivered Shorts below release as they are; do not re-render or swap them. The fix and the check apply to every new render.

**Problem.** `lib.band()` drew the two-line title at y 96 with a 100 px step and a font up to 88 px. With title-case
titles (rule of 2026-10-16/20), a second line with g, j, p, q or y at full size ran its descenders to row 312. The
band's glass line sits at 309 and the picture is pasted from 310, so the tails of those letters were sliced off flat.
The older all-caps titles had no descenders, so this never showed before. Found by the SL-17 reviewer on Short B
(`/Volumes/Extreme/_edit_work/SL-17/review/ROUND-1-REVIEW-B5.md`).

**Fix (in git).** Every `lib.band()` copy under `.claude/skills/shorts/reference/` (softblue-sl03, sl06, sl07, sl09,
sl15, sl18, sl19, calories-round3/4/5; sl17 already had it) now draws at y 86 with a 96 px step. Worst case at
88 px: lowest glyph row 298, 11 px above the line. `batch.py gfx|proof|render` runs
`.claude/skills/_shared/softblue_titlecheck.py` on every title first and stops if the lowest white row is 299 or
lower down. Tested: the old SL-15 geometry fails it (rows 311, 312); every title in every batch passes with the new
geometry. **The live work folders on Extreme (`/Volumes/Extreme/_edit_work/SL-xx/lib.py`) still have the old
geometry: a re-render must copy the fixed `band()` (two lines) in first.**

## Method

`python3 .claude/skills/_shared/softblue_titlecheck.py frame <file>` on all 152 finished Shorts in
`Short-form video content/` (review copies, A/B comparisons and `_pre*` folders skipped): frame 1, or 1.5 to 8 s in
for Shorts that open on a full-frame hook; band detected by the navy field and the glass line; white type measured
in rows 100 to 307. 43 Shorts carry the band. Every flagged file was checked by eye on a contact sheet, and its
SHA-256 matches the master in its setup receipt (so the clipped file is the one queued or uploaded).

## Clipped: 11 Shorts (letter tails visibly cut at the band edge)

| release | Short | clipped line | where it is now |
|---|---|---|---|
| **Mon Oct 26** | I'm 41 Wasted Life 1: Why ADHD Meds Backfire Long Term (SL-18) | "Backfire Long Term" (g) | not uploaded; setup handoff not yet run |
| Mon Nov 9 | Top 5 Zepbound Tips 1: Start At 1 mg, Not 2.5 mg (SL-06) | "Not 2.5 mg" (g, comma) | not uploaded; setup at cover picks |
| Fri Nov 13 | Oura 1: Train Harder After A Bad Night's Sleep (SL-09) | "A Bad Night's Sleep" (g, p) | **in Blotato**, schedules 5867678/79/80/82 (read live) |
| Fri Nov 27 | Oura 5: Oura Ring Or WHOOP? Which One To Buy (SL-09) | "Which One To Buy" (y) | **in Blotato**, schedules 5867711/13/15/16 (read live) |
| Tue Dec 1 | Top 5 Zepbound Tips 4: Inject On Thursday Evening (SL-06) | "Thursday Evening" (y, g) | not uploaded |
| Sat Dec 5 | Top 5 Zepbound Tips 5: How To Come Off Without Regaining It (SL-06) | "Without Regaining It" (g) | not uploaded |
| Mon Dec 14 | 3 Healthy Foods 1: Coconut Water Is Just Sugar Water (SL-19) | "Just Sugar Water" (g) | uploaded, on the waiting list |
| Tue Dec 22 | Belly Fat 2: Weigh Yourself Every Morning (SL-07) | "Every Morning" (y, g) | uploaded, on the waiting list |
| Fri Dec 25 | 3 Healthy Foods 3: My 4 Go-To High-Protein Snacks (SL-19) | "High-Protein Snacks" (g) | uploaded, on the waiting list |
| Fri Jan 1 2027 | My First Spray Tan 1: Why You Look Less Ripped In Photos (SL-15) | "Ripped In Photos" (p) | uploaded, waiting for RO-19 |
| Sat Jan 2 2027 | My First Spray Tan 2: Get A Tan Without Sun Damage (SL-15) | "Sun Damage" (g) | uploaded, waiting for RO-19 |

Files: `Short-form video content/` `wastedlife-short1_…`, `zepbound-tips-short1/4/5_…`, `oura-short1/5_…`,
`healthyfoods-short1/3_…`, `belly-fat-90-days-short2_…`, `spraytan-short1/2_…` (iCloud ` 2`/` 3` duplicates are
identical copies).

## Close but intact (no re-render needed)

- Belly Fat 4: The 3-Pound Rule That Keeps Belly Fat Off (SL-07): lowest row 300, 9 px clear, nothing cut.
- Top 5 Zepbound Tips 2: Use A Needle And Vial, Not The Pen (SL-06): lowest row 299, 10 px clear.

## Clean

All six Salad Shorts (SL-03), Belly Fat 1/3/5, Oura 2/3/4, Zepbound Tips 3/6, 3 Healthy Foods 2, Wasted Life 2 and
all three Top 1% Shorts (SL-17, already on the fixed geometry).

## Re-render path (not used: Dan ruled no; kept in case he changes his mind)

Per batch: copy the fixed `band()` into the Extreme work folder's `lib.py`, run `batch.py render <S>` (picture only
changes in rows 86 to 310; audio, captions and cut are untouched), re-run the delivery gate, then compare to the
approved master outside the band (should be identical). For uploaded Shorts the new master also needs a new
TikTok cover-first copy, re-upload, SHA match and the config / Blotato schedule media swapped. Nothing was
re-rendered or swapped in this audit.
