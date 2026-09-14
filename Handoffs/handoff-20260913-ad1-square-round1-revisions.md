# Handoff — Ad 1 square (1:1) — Dan's round-1 revisions

> ✅ **EXECUTED AND RE-DELIVERED 2026-09-14.** Record: `notes-square.md` "Round 1" beside the files and `/shortad-from-longform` [S1].25. Bottom line chosen 1030 (Google's square template finding recorded in the shared rules). Remaining: Dan's approval → the "When Dan approves" list below.

**Written 2026-09-13 by the session that built and delivered the square.** Dan reviewed the delivered
`… | claude | 1x1 | ad 1.mp4` and called it *"pretty solid"* with two revisions. Nothing about the edit, the
grade or the audio changes. This is a geometry pass on four graphics and a label pass on six pictures, then a
re-render, the gates, an audit, and a re-delivery.

Read first: `/shortad-from-longform` **[S1]** (all of it, especially 22–24) and
`.claude/skills/shortad-from-longform/reference/a11_sq_ad1/README.md`. The shared square rules are
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md`.

## Dan's words (2026-09-13, verbatim; dictated, so "apps" = abs)

> "With the label of me that's correct on the real pictures, put that above my head or somewhere it doesn't
> block my face or abs. It's important not to block my face or abs because this is supposed to be proof, and
> this is kind of blocking the proof. Make that revision for all of the real pictures of me throughout the
> video that aren't AI-generated."

> "At 25 seconds, the graphic is a little bit too high. I want you to lower the graphic a little bit so more of
> my body is visible. Make the text a little smaller or make it extend a little bit longer to accommodate this.
> For this graphic at 135, I want you to move it down a little bit more so more of my body is visible. There's
> some unnecessary blank space at the bottom of the graphic. Same revision for the graphic at 2:46. Too much
> unnecessary space at the bottom. My body is blocked. Move the graphic downwards and eliminate space at the
> bottom to accommodate that. Same thing for the graphic at 3:46. Move it down and eliminate the blank space at
> the bottom."

> "Overall, I think this was pretty good. Color correction looked good, and audio looked good. For the graphics,
> for the most part, they looked good, except for the feedback for moving them downwards."

⚠ **The label rule is not new — the square missed it.** Dan gave the identical placement rule on the Ad 2 square
on 2026-09-12 and it is already in `AGENTS.md` ("LABEL PLACEMENT — NEVER OVER HIS FACE AND NEVER OVER HIS ABS")
and 8 video skills. This build placed its chips with `sqlib.bleed_chip()` at `CAP_Y − 26`, the old waistline
position, because its labels were laid out before that rule landed ([A8].2: re-read `git log` for standing rules
before the first render — this is that, again).

## What exists

| | |
|---|---|
| build dir | `/Volumes/Extreme/_edit_work/ad1-sq/` — `sqlib.py` (layout), `sqassets.py` (per-media treatment + label), `render.py` (compositor → `picture.mp4`), `captions.py`, `sqmux.py` (asserts 6,976 frames + the approved vertical's audio md5), `sqcutdown.py` → `sqcut_build.py` → `cut_edl.py`, `plan_sq.py`, `deliver_sq.py` |
| delivered (to be replaced) | `Muhammad Ad Videos/this picture got me abs - ad 1/… \| claude \| 1x1 \| ad 1.mp4` (6,976 f) and `… \| 1x1 59s \| ad 1.mp4` (1,493 f / 49.82 s), both **DELIVERY GATE PASS at 1.2.0** |
| audio | the approved 9:16 vertical's AAC stream, md5-asserted in `sqmux.py`. **Dan approved it. Do not touch it.** |
| captions | `words_ctc.json` (CTC), 100.0 % on both files. Window beats mute captions, so the layout change below does not move them |

## Revision A — the four window graphics: lower them, remove the bottom dead space

**Why there is dead space (measured).** `sqlib._bullet_layout()` / `window_rect()` stop the text block at
`BOT_SAFE = 980` (a number this build chose — `notes-square.md` records it as "a round number we chose, not a
platform boundary"), and every bullet adds `+30` px AFTER itself, **including the last one**, so the ink ends
~940 and the bottom ~140 px (13 % of the frame) is empty field. Dan's window cannot grow into it, and on two beats
the `MAX_WIN_H = 700` cap would stop it anyway.

| Dan's timestamp | beat (`beats.py`) | now | window h now |
|---|---|---|---|
| **0:25** | `window` 14.30–26.95, header + 3 bullets | 46 px, 6 lines | **422** |
| **1:35** | `window` 91.85–97.05, 2 bullets | 46 px, 3 lines | **680** |
| **2:46** | `window` 162.40–171.80, 2 bullets | 46 px, 6 lines | **524** |
| **3:46** | `window` 220.75–228.50, 2 bullets | 46 px, 4 lines | **628** |
| (2:52, not named) | `stmt` 171.80–177.25, same split | 62/50 px | 640 |

**Measured options** (window height after removing the trailing 30 px; right safe strip kept at 100 px):

| beat | bottom line 980 | **bottom line 1030 (50 px margin)** | bottom line 1040 |
|---|---|---|---|
| 0:25 | 46px 462 · 42px 496 · 38px 524 | **46px 512 · 42px 546 · 38px 574** | 46px 522 · 42px 556 |
| 1:35 | 720 · 735 · 747 | **770 · 785 · 797** | 780 · 795 |
| 2:46 | 564 · 641 (5 lines) · 661 | **614 · 691 (5 lines) · 711** | 624 · 701 |
| 3:46 | 668 · 688 · 704 | **718 · 738 · 754** | 728 · 748 |

**Recommended default (make it, don't ask):**
1. Drop the `+30` after the LAST bullet (both `_bullet_layout` and `plate_window`'s body loop). Free, no trade-off.
2. **One type rung smaller on every window beat, 46/42 → 42/38**, so the ad keeps one bullet size throughout
   (Dan offered "a little smaller" and it buys the most on 2:46, where 42 px saves a whole wrapped line).
3. **Bottom line 980 → ~1030** — BUT first spend five minutes confirming the real bottom overlay for the square's
   placements (Google Demand Gen / YouTube in-feed / Discover / Gmail, and Meta feed 1:1). If a platform draws UI
   over the bottom of a 1:1 video, stop above it and say what it is; if not, 1030. **Record the number and its
   source in the shared square rules doc**, because Ads 5, 4, 3 and Zeeshan's Ad 1 squares inherit this layout.
4. Raise `MAX_WIN_H` from 700 to ~820 (1:35 wants 785, 3:46 wants 738).
5. Apply the same bottom line to the 2:52 `stmt` beat so the four screens and the statement match.

Result at the default: 0:25 **422 → 546**, 1:35 **680 → 785**, 2:46 **524 → 691**, 3:46 **628 → 738**.

**Check that a taller window shows more BODY, not more room.** `window_crop()` sizes the crop by magnification
(`MAG`, `CROP_W_MAX = 1400`) and anchors it at the source top (`y = 0`), so a taller window extends the crop
DOWN into his torso — which is what Dan asked for. At 1080×785 the crop is 1400×1018 (fits the 1080-tall source);
past ~1080×840 the crop hits the source height and the magnification rises instead. Verify on rendered frames,
and run `sqhairgate.py` — the hair-anchored top must not move.

⚠ The layout signature (`LAYOUT_SIG` in `render.py`) and the plate cache key must change, or `render.py` serves the
old plates ([A4].2, [A5].15). Re-render the whole master ([A9].12) and diff the gray trace — the change set must
be exactly these five beats plus the label beats below.

## Revision B — the labels: off his face and off his abs, on every picture of Dan

Every beat carrying a chip over Dan's body, with the clear space MEASURED on the delivered frames (Apple Vision
person mask, `rc/personmask`; first and last frame of each beat because the stills push). Safe area: y ≥ 80,
right 100 px reserved. Chip sizes from `sqlib.chip_layer`: one-line real chip **644×56 @34 px, 573×53 @30, 540×51
@28**; two-line ("Real picture of me —" / "not AI-generated") **360×98 @34, 321×92 @30**; AI chip **276×48 @34**.

| beat | picture | now | clear space measured | recommended placement |
|---|---|---|---|---|
| 11.45–12.40 `today_towel` (cover) | real | waistline | **62–70 px above his head** (head top y 154–162); beside head L 460 / R 293 px | **one line @28–30 centred above his head** (Dan's first choice) |
| 12.40–13.35 `today_trees` (cover) | real | waistline | **0 px above** (hair 14 px from the top); beside head+shoulders L 412 / R 290 px | **two-line @34, top-left**, beside his head |
| 13.35–14.30 `today_flag` (cover) | real | waistline | **89–94 px above his head**; the flag fills both sides | **one line @34 centred above his head** |
| 47.95–50.45 `bodybuilder` (fith, photo on the field) | real | waistline | 0–45 px above; beside head L 452 / R 330 px, **but the photo is only ~720 wide and centred** | two-line, top-left **inside the photo** — do not straddle the photo's edge and the field; shrink to @30 if needed |
| 0.00–2.95 `ai_goal_plain` (fith) | AI | over his abs, and **covering a chip burned into the source video** | 0 px above in the video; beside head L 434 / R 252 px | see below |
| 61.45–66.30 `photoshop_gag` (fith) | AI | low, on his legs | 0 px above; beside head L 392 / R 320 px | AI chip @34 beside his head |

Dan's words name the REAL pictures. The two AI-picture rows follow the standing rule in `AGENTS.md` ("Applies to
BOTH labels on any picture of Dan"); the stranger in the app screens and the AI stock men are not Dan and keep
their card chips.

⚠ **The hook's goal video has AI-GENERATED burned into it over his abs**, which is why our chip was drawn on top
of it (`cover_chip` in `sqassets.py`). Moving our chip would expose the burned one. **Use the clean still
instead**: `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/01 Before and After Images/dan by
pool - AI GOAL IMAGE.png` (864×1184, checked 2026-09-13: no label on it, and it has real headroom above his head).
Render the hook as a still with the same slow push as the approved vertical, chip placed by measurement, and
confirm frame 0 and the push's last frame both keep his hair ([A10].4, `sqstill_end.py`). This replaces the
`cover_chip` code path — delete it rather than leaving two ways to label the hook.

**Placement mechanics.** `render.chip_png()` and `sqlib.bleed_chip()` take one fixed y; give each labelled media
an explicit chip spec in `sqassets.py` (position + one-/two-line + size), chosen from the table above and then
re-measured on the RENDERED frame with the mask. The chip must clear the head+torso box on EVERY frame of the
beat, not just frame 0. Add the new real-picture chip images to `plan_sq.py`'s per-insert `chip`/`pos` so
`compliance:labels` keeps reading them (it did at 0.986–0.987 on the old positions).

## The cutdown

The cutdown is a selection out of the master, so it inherits every change: re-run `sqcutdown.py --build`
(`assert_range_lands()` re-proves every range's first and last frame against the new master), `sqcut_build.py`,
`cut_edl.py`, then the cut gates. Its window beats at 0:25-equivalent and 3:46-equivalent change with the master;
`today_towel` and `today_trees` are in it too.

## Gates, audit, delivery — all mandatory

1. Two-build cap: `ps -Ao command | grep -E 'ffmpeg|render\.py|whisper'` before rendering.
2. `render.py` → `sqmux.py` (asserts 6,976 frames + audio md5) → gates on the master: `audio_gate.py --verbatim`,
   `watch.py` + a written `watch_mark.py` note naming every strip re-looked at, `sqhairgate.py`, `centering.py`,
   `sqlanding.py`, `caption_sync_check.py` (100 % expected — captions did not move), then
   `plan_sq.py --transcribe` and **`_shared/deliver/gate.py --format ad1x1 --plan plan.json`** at whatever
   `GATE_VERSION` is current (it was 1.2.0; Phase 3 may have taken it to 1.3.0 — re-check).
3. Cutdown: the same chain from inside `cut/` (`chain_cut3.sh`), then its own delivery gate. ⚠ Copy the build
   root's `ad1_square_59s.mp4` into `cut/` before any cut-side extraction — three extractions in round 0 read a
   stale copy ([S1].24).
4. **An independent Fable subagent audit on the delivered bytes** (Step 7b). Tell it exactly what changed and ask it
   to verify: every label clears his face AND abs on every frame of its beat; every window screen shows more of his
   body and has no dead band at the bottom; nothing readable crosses the bottom line you chose; the hook still
   reads as the approved hook. Round 0 needed three audits.
5. `python3 deliver_sq.py` (it now refuses to deliver without a PASS delivery stamp and carries the stamp to the
   folder), update `notes-square.md` with a "Round 1 (2026-09-13)" section, send Dan the 540p review copies.

## When Dan approves

* Add the approval to `.claude/skills/_shared/qc_corpus/` with his words above — he approved the colour and the
  audio outright, which is a corpus-worthy anchor for a square.
* Upload unlisted and add to the Ad 1 Demand Gen ad groups per the shared square rules' "After the build".
* Check off the dashboard row for the square only then. Delete this handoff's lines from `Handoffs/README.md` and
  `AI_COORDINATION.md`.

## Traps from round 0 that will bite a re-render

* `render.py` loads `cx_track.json` at import — import it from the build root only.
* A time-based `-ss` lands on the wrong frame on these masters; extract by index.
* `qc.py` in the build root was the 9:16 attempt-3 fork (checks for 1080×1920); use the skill's
  `reference/qc.py … --build-dir .` if you run it at all — the shared delivery gate is the authority.
* `compliance:negative_events` wants `findings` as a LIST (a prose string is read as 870 findings) and a scan
  record whose sha256 matches the delivered bytes — re-scan after the re-render.
* `captions:graphic_clearance` and `captions:sync` are declared not-applicable in both plans with written reasons;
  keep them unless the build changes.

## Starter prompt (Fable 5.1, effort high)

> Execute `Handoffs/handoff-20260913-ad1-square-round1-revisions.md`: Dan's round-1 revisions on the Ad 1 1:1
> square in `/Volumes/Extreme/_edit_work/ad1-sq/`. (A) Lower the four window screens at 0:25, 1:35, 2:46 and 3:46
> so more of his body shows and the dead space at the bottom is gone — drop the trailing bullet gap, one type rung
> smaller, bottom line ~1030 after checking the square placements' real bottom overlay, raise MAX_WIN_H. (B) Move
> the "Real picture of me — not AI-generated" label off his face and abs on every real picture (above his head or
> beside it, measured with the person mask on the rendered frame), and do the same for the AI chips on pictures of
> Dan — the hook from the clean goal still, not the video with the burned chip. Audio and colour are approved; do
> not touch them. Load `/shortad-from-longform` first. Re-render, run every gate on both delivered files including
> `_shared/deliver/gate.py`, an independent audit, then `deliver_sq.py` and send Dan the review copies.
> Model: Fable 5.1, effort high.
