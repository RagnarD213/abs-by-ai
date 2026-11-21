AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Never Pay Nutritionist AD R4` (revisions) or
`Never Pay Nutritionist AD Setup` (approved).

# RA-15 "Never Pay A Nutritionist Again": after Dan's review of round 3

**Written 2026-10-15 by the round 3 session (Claude, Opus 5.5).** Round 3 delivered the finished 9:16 and 16:9.
Delivery folder: `Claude Ad Videos/never pay a nutritionist again - RA-15/` (`notes.md` there: files, hashes, gates, changes, for Dan).
Review page: http://127.0.0.1:8839/ (service `review_server.py 8839`). VLC copies in `Videos to Review/`.
Recipe and lessons 13-27: `.claude/skills/ad-edit/reference/ra15/README.md`; work folder `/Volumes/Extreme/_edit_work/ra15/`.

| file | sha256 (16) | gate 2.6.0 |
|---|---|---|
| `... \| claude \| 9x16 \| RA-15.mp4` | 2c964e7ab3c9940c | 38/39, only `audio:stamp` (tone row, the bass lift) |
| `... \| claude \| 16x9 \| RA-15.mp4` | a8cc2c68c5a398a8 | 38/39, same |

## If Dan approves
Record his words in `APPROVAL.md` in the delivery folder (RA-14's is the model), `queue.py set RA-15 finalized` + the artifact db,
delete both `Videos to Review/Never Pay Nutritionist AD R3 - *` copies, `review_server.py 8839 --remove`, re-run
`round3/s_sheet15.py <16x9> --approved "<his words>"`, then fire `/ad-setup` for both shapes (one Claude setup handoff, five
thumbnails by Codex per AGENTS.md). Verticals/squares/cutdowns of this ad are AV/AS jobs (`/shortad-from-longform`), only if he asks.

## If Dan sends notes
Rebuild from the work folder in this order (each script's docstring says what it reads): `s05_plan15.py` (plan; settings `TRACK`,
`TRACK_HOLD`, `LEVELS`), `round3/s_analysis.py`, `gfx15.py`, `gfx16.py`, `s06_inserts15.py` / `s06_inserts16.py` (named cards),
`s07_captions.py 9x16|16x9`, `s10_render05.py 9x16|16x9`, mux with `mix_bass_r3c.wav` (re-run the voice chain with `--frame-lock`
only if the length changes), then `round3/r3_deliver.sh KEY`, `s20_neg.py`, `round3/s_gateplan15.py`, `watch.py` + a fresh judge,
`gate.py`, `round3/s_sheet15.py`, one fresh `ra-reviewer` per shape, `round3/page15r3.py --media`. Send the change list with timestamps.

## Open, for Dan's eye (from the reviews; nothing blocking)
Lower thirds and the 9:16 button cross his abs (RA-14 placement); 9:16 shoulder/hand touches an edge for under 0.4 s at 0:10.9,
0:42.7, 0:50.3; "twice." is a 0.64 s close shot (a longer cutout shot needs a new Veo take); 16:9 framing is tighter than RA-01's
(the no-wide-level gate row); the opening line is his on-set wording.

**Recommended model and effort: Opus 5.5, high.**

## Starter prompt
> AD. Rename this task `Never Pay Nutritionist AD R4` (or `... AD Setup` if I approved). Read
> `Handoffs/handoff-20261015-ra15-after-dan-review-round3.md` and act on my round 3 answer: <paste>.
