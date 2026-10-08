# RO-06 "How To Work Out At Home On A Budget": round 5, build the full film

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R5`.
Written 2026-10-08 by Claude (Opus 5.5) after Dan approved the round 4 first minute and the four moving AI clips.
This is the only RO-06 handoff: it replaces every earlier one (rounds 1 to 4, all executed or folded in here).
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md` (traps from rounds 1 to 4),
`/Volumes/Extreme/_edit_work/ro06/round5-plan/decisions.json` (Dan's words, hashes, my reading of the open decisions),
`/Volumes/Extreme/_edit_work/ro06/round4/round4-record.json` (takes, trims, costs, checks).

## Scope of this round
Build the complete film, run everything that needs the complete film, show it to Dan. Build in
`/Volumes/Extreme/_edit_work/ro06/round5/`. Never overwrite `round1/` to `round4/`.

## Dan's words (2026-10-08, on the round 4 page)
"All right, this is looking great. Everything is approved ... I really love the way that you did the lip-syncing and the
slap. Both of those turned out significantly better than I expected."

## Locked by Dan (do not reopen)
- Cropping, colour, audio, the tight open, the three-clip opening, jump rope `B0448@4.0`, the panning equipment shot.
- **The round 4 first minute**, `round4/first-minute/DRAFT - RO-06 round 4 - first minute.mp4`, sha256
  `8d0c592092943e7f0f2b97343021205e854ef55f201acb1cce82442193c12099`. Re-hash before building.
- **The four AI clips in motion, exactly as placed** (`recipe/plan.py`, items A1 to A4): `round4/motion/A1-final.mp4@0.0`,
  `A2-final.mp4@0.0`, `A3-t1.mp4@1.341` with `late=0.312` (the second slap; the hit lands on "destroy" at 39.40),
  `A4-t1.mp4@0.30`. Hashes in `decisions.json`. No new takes, no new lip sync.
- Soft Blue Light graphics and the HyperFrames templates. All graphics, stock and clips were shown on the round 1 page.

## The seven older decisions: built at the recommended option (my reading, Dan can overrule)
The round 4 page listed them with the recommendations filled in and said the full film is built once they are answered.
Dan replied "Everything is approved" and did not speak to them one by one. They are built as below. **If the starter
prompt carries a different answer for any line, that answer wins.** List all seven on the full-film page under "What I
decided (overrule anything)".
| decision | built as | what it means in the build |
|---|---|---|
| Hair at the top edge, 9 later rolls | leave as shot | No headroom extension. The hair rows fail on rolls C1567 to C1574 (5 to 15 px in the source); report it plainly as his choice. |
| Length | A: trim three pure repeats, about 16:30 | Cuts below. |
| Product pictures | keep the six AI-made pictures, labelled | Nothing to change (F01 to F06, `label="AI-GENERATED"`). |
| Jump rope price | keep as built | No price on screen in the jump rope section, $9 in the total list. |
| Music | a quiet bed under the voice | Steps below. |
| App demo | the approved demo in the Soft Blue phone card | P01 and P02 below. |
| Opening | on-camera open | No AI opener. |

## Build steps
1. **Length A cuts** (source times, roll-local): C1569 65.7 to 91.4 (keep the $58 total line before it), C1572 16.1 to 29.9,
   C1580 the restatements at 11.9 to 24.5 and 141.6 to 149.0. Check each edge on the envelope and with medium.en before
   cutting. Lower third G30 is anchored on "So I want you guys to get started": move its anchor if that line goes. Rerun
   `edl.py` through `resolve.py`, then `hyperframes/from_plan.py --render` (unchanged scenes are skipped). **None of these rolls
   is in the first minute** (C1559, C1560): after the cuts, prove the first minute's presenter frames still match round 4's
   `build.json` (crop and source frame, 0 differences) and its untreated voice md5 is still
   `fbf7798364cf1f0592144e03827a3b8a` over 0 to 62.9963 s.
2. **P01** (plan item, "upload your current picture"): the approved sunglasses-to-pool demo, same steps and the same
   AI-GENERATED disclosure, rebuilt in the Soft Blue phone card. **P02** (the workout list and an exercise sheet, `B0034`): in
   the approved upright-phone treatment (VIDEO-RULES, "Approved workout-app format"). Both are `pending=True` in `plan.py` today.
   Show both as stills and "play it in place" on the review page: they are new to Dan in this form.
3. **Music bed:** Pixabay, chosen with `reference/pick_bed.py` (flatness first), transcribe it and require zero words, duck it
   under the voice. The bed level is a ceiling: read the gate's "clean between words" row and drop the bed 6 dB if it fails.
   With a bed the delivered audio no longer matches the round 2 decoded md5; the untreated voice md5 above is the proof that
   the voice itself did not move.
4. **Before the full render, the leans scan.** The per-shot `active` flag misses a one-second lean inside a long shot (seen
   at 61 s and 70 s: he bends and points at the equipment). Scan every tight (X) segment for head drop or sideways travel
   (`hair_fm.py` rows carry top, left, right per quarter second), then `split_shot.py` and set those sentences to T or W.
   `exc3.0r3` (69.4 to 76.2, "With this stuff right here") is one. Also: one hold of 24.4 s at 12:22 exceeds the 22 s rule
   (`build.py segs 1100`), and check the closing section for cover ("my gym where there's bodybuilders", "get a gym
   membership"): clip library first, then Pexels.
5. **Full film:** `build.render_range(0, total)`, then the SRT (sidecar only, no burned captions), chapters, the edit sheet
   (`_shared/edit-sheet`, must validate before the gate), the audio gate, the watch pass (`_shared/deliver/watch.py`) with a
   fresh judge, the dense hair check, hyperframes `checks.py`, one independent review (`ra-reviewer`), and the delivery gate
   `--format longform`. A check that did not run is a failure: say so. Never raise a bound.
6. **Deliver:** review page (full film on top, What changed, What I decided with the seven lines above, P01 and P02, the
   music choice, one reply box) on a free port with `review_server.py`; VLC copy `Videos to Review/Work Out At Home LFC R5 -
   full film.mp4`; delete `Videos to Review/Work Out At Home LFC R4 - first minute.mp4`. Master, SRT, chapters, 540p copy,
   stamps, notes and recipe go in `claude edited long form content/13 - How To Work Out At Home On A Budget/`. Edit queue:
   `delivered`. Add the approval and any rejection to the QC corpus with Dan's words when he replies. Then stop.
7. When the EDL is final run `roll_sidecar.py mark-used` for every source range.

## Budget
$5 per video for AI clips, retries included. **Spent: $2.43.** Left: $2.57. Nothing in this round needs a new AI clip. Past
$5: stop and tell Dan the number and the reason first.

## Honest status
- Not run yet (they need the complete film): delivery gate, watch pass, independent review, edit sheet.
- Not heard by a person in full: the cross-take join in the kettlebell price section (clean on medium.en and on frame strips).
- An outside playback check (Gemini, one frame a second) called the lip sync unconvincing; Dan watched it and loved it. Closed.

## After Dan finalizes the film (not this round unless he says so)
Register the four AI clips in the clip library (`clip_library.py add ... --status used-final --used-in "RO-06"`), delete this
video's copies in `Videos to Review/`, stop the page services (`review_server.py PORT --remove` for 8846 to 8849 and the new
one), set the queue to `finalized`. At upload the AI flag is true (`/video-setup`): the film has realistic AI footage.

## Next action
Re-hash the locked files, apply the length cuts, then steps 2 to 6. Recommended: **Claude Opus 5.5, high.**

## Starter prompt
> Read `Handoffs/handoff-20261008-ro06-round5-full-film.md` and execute it with /longform-edit. This is RO-06 "How To Work Out
> At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R5`. I approved the round 4 first
> minute and all four AI clips. Build the full film with these answers to the older decisions (change any line before
> sending): hair, leave as shot; length, trim the three repeats to about 16:30; product pictures, keep the AI pictures;
> jump rope price, keep as built; music, add a quiet bed; app demo, the approved demo in the blue phone card; opening,
> keep the on-camera open. Run every check and the independent review, show me the full film, then stop.
