# RA-14 "The Cheat Code For Six Pack Abs": round 2, after Dan reviews round 1

**AD (short-form, filmed).** Sidebar name for the next task: `Cheat Code Six Pack AD R2`.
Written 2026-10-13 by the round 1 session (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-14-cheat-code-for-six-pack-abs.md`.
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, the `/ad-edit` skill, `_shared/PRE-RENDER-APPROVAL.md`.

## Scope of round 2

Dan has NOT replied yet. Round 1's page is http://127.0.0.1:8814/ (folder `/Volumes/Extreme/_edit_work/ra14/round1/`).
When he replies: record his words in `/Volumes/Extreme/_edit_work/ra14/round2-plan/decisions.json`, apply them, then build
the moving previews of every graphic and clip in context plus the finished first 30 seconds (9:16), and show those.
The full film, the 16:9, the gates, the watch pass and the independent review are round 3, only once nothing is pending.
Do not start round 2 before he answers the three decisions.

## What round 1 settled (work dir `/Volumes/Extreme/_edit_work/ra14/`, sha256 first 16)

| file | what | hash |
|---|---|---|
| `cut.json` | the take map and airtight cut: 48.81 s of talk, 23 source pieces, 4 take seams (10.57, 30.30, 33.43, 46.46 s) | 394e9127a580ce5c |
| `mix.wav` | voice through `voice_chain.py` (fitted tone, no dereverb) + Realizer bed at -32; audio gate PASS 12 of 12 | fe821bf0b0c5c108 |
| `mix_bass.wav` | the same with +3 dB at 120 Hz (Dan's option B; gate tone row fails at 2.55 against 2.5, the known fixed-shape mismatch) | a969e60b871ecd8d |
| `words_aligned.json` | 168 words, CTC aligned to `mix.wav` | b01781a5203792fb |
| `framing.json` | head and hair track, 241 of 241 samples, 5 per second | d798e48e215d593a |
| `beats.json` | the beat plan: 4 inserts, 5 overlays, 12 holds, each hold's land-then-hold crop track | f220cbe03847c48d |
| `grade.json` | RA-01's approved daylight grade, reused after a side-by-side check | 38c3929d700e32e6 |
| `round1/RA-14 round 1 - look sample (opening).mp4` | the first 10.68 s finished | 898f943a05fd2264 |

Total length 50.45 s (1.65 s end hold), 8.55 s under the 0:59 limit. No line cut. Spend on AI generation: $0.

Source facts: roll `C1667.MP4` (8/28 pool set, native portrait 2160x3840, dual-mono lav, `C1667.MP4.audio_source.json`
written by `pick_lav.py` on 340 s + 70 s). Takes used, source seconds: 340.09-351.63, 357.54-366.78, 366.78-379.23,
382.70-387.00, 394.01-408.92, 412.33-414.69 (the last edge is pinned past a 50 ms click at 411.95).
Framing sizes measured for THIS roll (he stands further back than on C1663): NEAR 504x896, FAR 612x1088, y0 = hold's
minimum hair top minus 4 % of the crop height. NEAR is a 2.14x enlargement.

## The plan Dan is looking at (tight seconds)

G1 AI goal picture 4.44-6.31 · L1 "STEP 1 / Generate Your Goal Picture" 10.68-14.18 · P1 self-generation demo 14.18-17.55
(phone to about 15.7, then the result) · L2 "STEP 2 / AI Builds Your Custom Plan" 18.99-22.42 · A1 analysis card
22.42-26.59 · L3 "STEP 3 / AI Coaches You Every Day" 30.30-33.43 · T1 app tour B0544 33.43-38.27 (play the source from
about 2.8 s so the Push-Up sheet at source 6.0 s lands on "A home workout") · R1 recap list 40.21-46.45 · C1 button
"Tap The Button Below / Get Started" 46.45-50.45. Holds alternate FAR and NEAR; every take seam sits on a size change
or under an insert.

## Dan's three decisions (page, "Your decisions")

1. Analysis card: redraw in Soft Blue Light (recommended) or keep the RA-01 dark olive card as approved.
2. Voice: `mix.wav` as approved on RA-01 (recommended) or `mix_bass.wav`.
3. Recap list card R1: keep (recommended) or no card.

## Known work for round 2 (already decided, not questions)

- The crop track lands 5 to 20 source px off at hold starts because the head is sampled 5 times a second. Add one head
  measurement on the exact first frame of each hold (`s04_track.py`), then re-run `s60_plan.py`. The standard asks for the
  actual cut-start measurement.
- Five pause splices sit inside a hold (11.38, 19.72, 31.13, 41.38, 42.64 s). Measure them on rendered picture
  (`s25_hard.py` or `_shared/cut/piccuts.py`) and give each visible one a size change or cover.
- Captions must lift above the recap card R1 (the still shows the lifted position); `s07_captions.py` needs a per-state y.
- The phone demos need a renderer: `s63_stills.py` has the shell and placement (`phone_card`); the demo display rect is
  `DISP` there. Keep the real-photo chip only while his photo is visible.
- The music bed's tail needs the RA-01 fix (`s42_bed.py`) once the length is final, and the mix must be frame-locked
  to the picture (`LOCK=`).
- 16:9: levels and centres are not chosen yet (RA-01's rule: both levels share the FAR window's centre).
- At delivery: edit sheet + `validate.py`, delivery gate, watch pass, one independent review (`ra-reviewer`), 540p review
  copies, audio A/B, `Videos to Review/` copy, `roll_sidecar.py mark-used` for the six source ranges, clip library
  `used-in` for B0544, queue to `delivered`.

## Recipe

Scripts are in `/Volumes/Extreme/_edit_work/ra14/` and copied to `.claude/skills/ad-edit/reference/ra14/`. Order:
`s00_source.sh` (lav pick, pull, transcript) · `s03_edl.py` (reads `edl_spec.json`) · `s08_audio.py` · `s09_align.py` ·
`s04_track.py` · `s60_plan.py` · `s07_captions.py 9x16` · `s63_stills.py cards analysis overlays` · `s62_sample.py` ·
`s64_page.py` · `review_server.py 8814 round1`. The machine was saturated all afternoon: use `./capwait.sh` and expect
long waits.

## Gate status, stated plainly

Only the audio gate has run (on `mix.wav`, PASS). No delivery gate, no watch pass and no independent review yet: there
is no finished file. Junk scan: `junk_report.json`; its one high row (a visible jump at source 374.85) is covered by the
A1 card's exit.

## Starter prompt (Claude Opus 5.5, high effort)

> AD. Rename this task `Cheat Code Six Pack AD R2`. Read `Handoffs/handoff-20261013-ra14-cheat-code-round2-after-dan-review.md` and continue RA-14 "The Cheat Code For Six Pack Abs" with /ad-edit: record my round 1 answers below, apply them, then build the moving previews of every graphic and clip in context and the finished first 30 seconds, and show me. My answers: [paste the reply box from http://127.0.0.1:8814/]
