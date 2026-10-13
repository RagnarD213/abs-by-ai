# Delivery gate 2.6.0: evidence for the click row and the build wait (2026-10-13)

Two faults in the shared delivery gate, both seen on RO-19 round 4. This file is the before and after.
Code: `.claude/skills/_shared/deliver/checks/audio.py` (`click_at_joins`), `.claude/skills/_shared/deliver/formats.py`
(`control_quantile`), `.claude/skills/_shared/buildcap.py`.

## 1. `audio:click_at_joins`

**What was wrong.** The row compares each join with a bar read off the same file. The bar was the largest of 150
random points. The largest of 150 is a lottery: for one unchanged file, 400 different draws gave bars 1.6 to 8.2
times apart (4.1 on a median file). A film 2.1 s shorter draws 150 different points, so RO-19 round 3 got a bar of
0.4244 and passed, and round 4, with the same voice at the flagged places, got 0.1802 and failed.

**What changed.** The bar is now measured from every 8 ms window in the file (about 140,000 on RO-19) and read at a
fixed point, the 99.54th percentile. That point is the middle of the old lottery (0.5 to the power 1/150), so the bar
is not raised or lowered on average. On the 54 files below the new bar is 0.95 to 1.04 times the median of the 400
old draws (median 1.00). The 1.25 multiplier is unchanged. Windows that hold a join are left out of the bar, so a
click cannot help set it.

**The two RO-19 films.**

| film | old bar | old verdict | new bar | new verdict |
|---|---|---|---|---|
| RO-19 round 3 | 0.4244 | PASS, 0 of 219 | 0.2573 | PASS, 0 of 219 |
| RO-19 round 4 | 0.1802 | FAIL, 2 of 219 (119.15 s, 929.03 s) | 0.2569 | PASS, 0 of 219 |

The two flagged joins measure 0.92 and 0.97 times the new bar; the limit is 1.25. Neither is a click by shape: the
largest sample step is 1.6 to 1.8 times the twentieth largest in the same 8 ms, which is a consonant. A splice is one
isolated step. With `audio_joins` declared (the 44 places the voice was really joined, from the build record) the
worst join is 0.04 times the bar under either rule: every real voice splice sits in a pause.

**Does it still catch a click.** 600 unfaded cuts of 5 to 40 ms made in the loudest 30% of each film:

| film | old rule, seed 7 | old rule, other 400 draws | new rule |
|---|---|---|---|
| RO-19 round 3 | 22% | 2% to 60% | 43% |
| RO-19 round 4 | 64% | 2% to 66% | 48% |
| ad6 vertical | 45% | 2% to 54% | 45% |
| RO-13 master | 16% | 1% to 52% | 18% |
| kit Ad 1 master 9:16 | 9% | 6% to 52% | 23% |
| Fired Them All R6 | 52% | 0% to 58% | 35% |

The new rule catches what the old one caught on a median draw, every time. It is not a strong detector (see "Known
gaps" in `_shared/deliver/README.md`); that is unchanged and stated there.

**Every file with a gate stamp, its video and its plan still on disk (54).** Old verdicts re-computed here agree
with all 54 stamps. "Draws that pass" is the share of 400 seeds of the old rule that pass the same file.

| file | format | joins | old bar (seed 7) | old draws min / median / max | draws that pass | old | new bar | new |
|---|---|---|---|---|---|---|---|---|
| SSD: ro19/round4/film/RO-19 round 4 - full film.mp4 | longform | 219 | 0.1802 | 0.176 / 0.266 / 0.982 | 94% | FAIL (2) | 0.2569 | PASS |
| SSD: wv01-edit/version-b/speed-1p2/Fired Them All AD R6 - Version B 1.2x 1080p.mp4 | website | 180 | 0.2023 | 0.173 / 0.317 / 1.144 | 92% | FAIL (1) | 0.3132 | PASS |
| Media/codex-video-trial/04-ad1/AD1_FIRST_CUT_16x9.mp4 | ad16x9 | 41 | 0.3005 | 0.182 / 0.331 / 0.883 | 100% | PASS | 0.3366 | PASS |
| Media/codex-video-trial/04-ad1/internal-v2/AD1_FIRST_CUT_16x9.mp4 | ad16x9 | 41 | 0.3005 | 0.182 / 0.331 / 0.883 | 100% | PASS | 0.3366 | PASS |
| Media/codex-video-trial/04-ad1/rebuild-muhammad/REVISED_CODEX_PROOF.mp4 | ad16x9 | 25 | 0.2215 | 0.191 / 0.380 / 0.879 | 100% | PASS | 0.3624 | PASS |
| Media/codex-video-trial/04-ad1/rebuild-muhammad/audio-retry/AD1_AUDIO_RETRY_PROOF.mp4 | ad16x9 | 25 | 0.2311 | 0.181 / 0.365 / 0.855 | 100% | PASS | 0.3570 | PASS |
| Media/codex-video-trial/04-ad1/rebuild-muhammad/full-ad-approved/AD1_FULL_16x9.mp4 | ad16x9 | 92 | 0.4923 | 0.188 / 0.325 / 0.838 | 100% | PASS | 0.3285 | PASS |
| Media/codex-video-trial/04-ad1/rebuild-muhammad/full-ad-approved/internal-v2/AD1_FULL_16x9.mp4 | ad16x9 | 92 | 0.4923 | 0.188 / 0.325 / 0.838 | 100% | PASS | 0.3285 | PASS |
| Media/codex-video-trial/04-ad1/rebuild-muhammad/internal-proof-v1/REVISED_CODEX_PROOF.mp4 | ad16x9 | 26 | 0.3717 | 0.180 / 0.365 / 0.812 | 100% | PASS | 0.3585 | PASS |
| Media/codex-video-trial/06-ad-r1/AD14_REVISION_R1.mp4 | ad16x9 | 6 | 0.2581 | 0.180 / 0.301 / 0.594 | 100% | PASS | 0.3026 | PASS |
| Media/codex-video-trial/06-ad-r2/AD14_REVISION_R2.mp4 | ad16x9 | 6 | 0.2581 | 0.180 / 0.301 / 0.594 | 100% | PASS | 0.3026 | PASS |
| Media/codex-video-trial/06-ad-r3/AD14_REVISION_R3.mp4 | ad16x9 | 6 | 0.2581 | 0.180 / 0.301 / 0.594 | 100% | PASS | 0.3026 | PASS |
| Media/codex-video-trial/06-ad-r4/AD14_REVISION_R4.mp4 | ad16x9 | 6 | 0.2581 | 0.180 / 0.301 / 0.594 | 100% | PASS | 0.3026 | PASS |
| Media/codex-video-trial/06-ad/FIRST_CUT_INTERNAL.mp4 | ad16x9 | 6 | 0.2579 | 0.181 / 0.305 / 0.579 | 100% | PASS | 0.3056 | PASS |
| Media/video_edit/_scratch/ad13-round4-judged-v1/h16x9/i added up what getting abs was supposed to cost | codex | 16x9 | ad 13.mp4 | ad16x9 | 23 | 0.6612 | 0.185 / 0.363 / 0.735 | 100% | PASS | 0.3577 | PASS |
| SSD: ra01/round1/master_16x9.mp4 | ad16x9 | 21 | 0.3298 | 0.179 / 0.335 / 0.758 | 100% | PASS | 0.3363 | PASS |
| SSD: ra01/round2/master_16x9.mp4 | ad16x9 | 20 | 0.2622 | 0.169 / 0.331 / 0.738 | 100% | PASS | 0.3308 | PASS |
| SSD: ad3-vert/ad3_vertical_9x16.mp4 | ad9x16 | 47 | 0.3942 | 0.202 / 0.371 / 0.782 | 100% | PASS | 0.3656 | PASS |
| SSD: ad5-vert/ad5_vertical_9x16.mp4 | ad9x16 | 58 | 0.2420 | 0.225 / 0.390 / 1.079 | 100% | PASS | 0.3901 | PASS |
| SSD: ad5-vert/cut/ad5_vertical_9x16_59s.mp4 | ad9x16 | 14 | 0.4167 | 0.208 / 0.422 / 1.080 | 100% | PASS | 0.4300 | PASS |
| SSD: av05-ad6-vert/ad6_vertical_9x16.mp4 | ad9x16 | 55 | 0.2415 | 0.187 / 0.251 / 0.836 | 49% | FAIL (3) | 0.2481 | FAIL (1) |
| SSD: av05-ad6-vert/cut/ad6_vertical_9x16_59s.mp4 | ad9x16 | 55 | 0.3976 | 0.175 / 0.253 / 0.809 | 70% | PASS | 0.2600 | PASS |
| SSD: kit9x16/ad1-master/kit_ad1_master_9x16.mp4 | ad9x16 | 97 | 0.6002 | 0.218 / 0.401 / 0.699 | 100% | PASS | 0.3996 | PASS |
| SSD: kit9x16/ad1-raw/kit_ad1_raw_9x16.mp4 | ad9x16 | 41 | 0.4049 | 0.183 / 0.329 / 0.870 | 100% | PASS | 0.3355 | PASS |
| SSD: kit9x16/auto-ad10-run2/my dad bod at 38 my dad bod at 40 | claude | 9x16 59s | ad 10.mp4 | ad9x16 | 72 | 0.5392 | 0.248 / 0.438 / 0.822 | 100% | PASS | 0.4323 | PASS |
| SSD: kit9x16/auto-ad10-run2/my dad bod at 38 my dad bod at 40 | claude | 9x16 | ad 10.mp4 | ad9x16 | 72 | 0.3475 | 0.267 / 0.491 / 0.829 | 99% | PASS | 0.4963 | PASS |
| SSD: ra01/round1/master_9x16.mp4 | ad9x16 | 21 | 0.3298 | 0.179 / 0.335 / 0.758 | 100% | PASS | 0.3363 | PASS |
| SSD: ra01/round2/master_9x16.mp4 | ad9x16 | 20 | 0.2622 | 0.169 / 0.331 / 0.738 | 100% | PASS | 0.3308 | PASS |
| Media/codex-video-trial/02-organic-sample/HUMAN_reference.mp4 | longform | 2 | 0.3529 | 0.219 / 0.462 / 0.704 | 100% | PASS | 0.4575 | PASS |
| Media/codex-video-trial/02-organic-sample/SAMPLE_v1.mp4 | longform | 2 | 0.2809 | 0.190 / 0.369 / 0.485 | 100% | PASS | 0.3602 | PASS |
| Media/codex-video-trial/02-organic-sample/rev2b/SAMPLE_REV2.mp4 | longform | 2 | 0.3044 | 0.181 / 0.292 / 0.486 | 100% | PASS | 0.2917 | PASS |
| Media/codex-video-trial/03-organic-abwheel/FULL_AB_WHEEL_v1.mp4 | longform | 28 | 0.3119 | 0.179 / 0.289 / 0.704 | 100% | PASS | 0.2899 | PASS |
| Media/codex-video-trial/03-organic-abwheel/FULL_AB_WHEEL_v2.mp4 | longform | 28 | 0.2713 | 0.184 / 0.293 / 0.616 | 100% | PASS | 0.2884 | PASS |
| Media/codex-video-trial/03-organic-abwheel/FULL_AB_WHEEL_v3.mp4 | longform | 28 | 0.2713 | 0.184 / 0.293 / 0.616 | 100% | PASS | 0.2884 | PASS |
| Media/codex-video-trial/03-organic-abwheel/FULL_AB_WHEEL_v4.mp4 | longform | 28 | 0.4963 | 0.174 / 0.291 / 0.639 | 100% | PASS | 0.2937 | PASS |
| Media/codex-video-trial/03-organic-abwheel/FULL_AB_WHEEL_v4b.mp4 | longform | 28 | 0.4963 | 0.174 / 0.291 / 0.639 | 100% | PASS | 0.2937 | PASS |
| Media/codex-video-trial/03a-organic-color-sample-v2/COLOR_SAMPLE_v2_30s.mp4 | longform | 1 | 0.2504 | 0.185 / 0.246 / 0.293 | 100% | PASS | 0.2442 | PASS |
| Media/codex-video-trial/03a-organic-color-sample/COLOR_SAMPLE_30s.mp4 | longform | 1 | 0.2504 | 0.185 / 0.246 / 0.293 | 100% | PASS | 0.2442 | PASS |
| Media/codex-video-trial/06-organic-r1/FIRST_CUT_INTERNAL.mp4 | longform | 25 | 0.2048 | 0.188 / 0.292 / 1.053 | 100% | PASS | 0.2972 | PASS |
| Media/codex-video-trial/06-organic-r3/C1652_R3_PRIVATE_REVIEW.mp4 | longform | 25 | 0.1833 | 0.138 / 0.200 / 0.382 | 100% | PASS | 0.1971 | PASS |
| Media/codex-video-trial/06-organic/FIRST_CUT_INTERNAL.mp4 | longform | 23 | 0.2409 | 0.160 / 0.307 / 1.049 | 100% | PASS | 0.2916 | PASS |
| SSD: ro01/revision10/full/RO01_MASTER_R10_REVIEW_1080p.mp4 | longform | 97 | 0.4187 | 0.192 / 0.403 / 1.207 | 98% | PASS | 0.3967 | PASS |
| SSD: ro01/revision9/full/RO01_MASTER_R9_1080p.mp4 | longform | 75 | 0.5172 | 0.209 / 0.404 / 1.193 | 97% | PASS | 0.4006 | PASS |
| SSD: ro01/revision9/full/RO01_MASTER_R9_FINAL_REVIEW_1080p.mp4 | longform | 74 | 0.3248 | 0.204 / 0.415 / 1.028 | 97% | PASS | 0.3995 | PASS |
| SSD: ro08/round2/render1/RO-08 round 2 - full film.mp4 | longform | 149 | 0.3098 | 0.167 / 0.248 / 1.363 | 100% | PASS | 0.2571 | PASS |
| SSD: ro13/round2/RO13_MASTER.mp4 | longform | 69 | 0.4818 | 0.221 / 0.440 / 1.113 | 100% | PASS | 0.4477 | PASS |
| SSD: ro19/round3/film/RO-19 round 3 - full film.mp4 | longform | 219 | 0.4244 | 0.171 / 0.265 / 0.924 | 95% | PASS | 0.2573 | PASS |
| SSD: kit9x16/sbl-ro10/calories the reason youre not losing weight | claude | 9x16 | RO-10.mp4 | organic9x16 | 24 | 0.3041 | 0.182 / 0.349 / 0.882 | 100% | PASS | 0.3455 | PASS |
| SSD: ds-17/ds-17_how-to-jump-rope.mp4 | short | 10 | 0.3730 | 0.210 / 0.479 / 0.665 | 100% | PASS | 0.4647 | PASS |
| SSD: ds-17/revisions/r1/ds-17_how-to-jump-rope.mp4 | short | 10 | 0.3730 | 0.210 / 0.479 / 0.665 | 100% | PASS | 0.4647 | PASS |
| SSD: ds-17/revisions/r2/ds-17_how-to-jump-rope.mp4 | short | 10 | 0.3730 | 0.210 / 0.479 / 0.665 | 100% | PASS | 0.4647 | PASS |
| SSD: ds28/round1/opening-and-G02.mp4 | short | 5 | 0.1767 | 0.161 / 0.242 / 0.459 | 100% | PASS | 0.2363 | PASS |
| SSD: kit9x16/sbl-ro10/calories the reason youre not losing weight | claude | 9x16 59s | RO-10.mp4 | short | 24 | 0.3666 | 0.184 / 0.307 / 0.520 | 100% | PASS | 0.3078 | PASS |
| SSD: wv01-edit/speed-1p2/WV-01 Website VSL A 1.2x 1080p.mp4 | website | 149 | 0.2424 | 0.176 / 0.276 / 0.593 | 90% | PASS | 0.2769 | PASS |

Totals: 51 PASS stay PASS. 1 FAIL stays FAIL (`ad6_vertical_9x16.mp4`, three joins down to one, at 1.27 times the
bar; its shape is also speech, not tuned away). 2 go FAIL to PASS (RO-19 round 4 and Fired Them All R6): each had
drawn a bar in the lowest tenth of its own lottery (0.180 against a median 0.266; 0.202 against 0.317). No PASS
became a FAIL.

`RO05_r6.mp4` carries a 2.2.0 stamp that failed this row (15 of 123) but its plan is no longer beside it, so it could
not be graded again.

**Long-form plans should declare `audio_joins`.** A long-form's `joins` are picture cuts. About 1 window in 540 of
ordinary speech beats the bar, so 200 picture cuts falling at random would fail the row about one film in three with
nothing wrong. The formula is in `longform-edit/SKILL.md` (delivery gate section).

**Regression corpus.** No corpus entry was rejected or approved on this row, so `qc_corpus/run.py` now runs a fixture
for it (`_shared/deliver/tests/test_click_at_joins.py`, step 0d): a click cut in at a join fails, clean joins pass, and
the bar may not move more than 3% when 2.1 s is removed from the file. The old rule moves 24% on that fixture.

**Corpus run on the changed gate (2026-10-13, 68 minutes):** `CORPUS PASS`. 178 entries: 173 agree with Dan's
verdict, 5 are gaps already on record, no rejected file passes and no approved file fails. All five fixtures pass,
the new one included.

**Found on the way.** The audio selftest that starts every corpus run used one fixed scratch folder,
`/tmp/audio_selftest`. Another session ran it at the same time and the two overwrote each other: the same code passed
16 of 16, then failed three rows ten minutes later. Each run now gets its own folder
(`_shared/audio/selftest.sh`).

## 2. The gate waiting on itself

**What was wrong.** Before its Whisper step the gate waits until fewer than two other builds are running. The counter
matched text in command lines, one process at a time. It counted the shell that launched the gate (the shell's own
command line contains "python ... gate.py"), so with one other match the gate waited for itself: 74 minutes on RO-19
round 4, 22 on SL-07. It counted each ffmpeg process, so one render (decoder and encoder) filled both slots. And
waiting tools counted each other, so three of them could wait forever with nothing running.

**What changed.** `_shared/buildcap.py` counts builds. A worker is told by its executable (ffmpeg, Whisper, Python
running a build script), never by text in a command line. One build is one process group: one launched command and
everything it started. The caller's own build is left out. A waiting tool marks itself, and waiters go first come,
first served. The cap is still two.

**Same machine, same moment, gate typed inline (2026-10-13 16:20):**

| counter | what it saw |
|---|---|
| old | 7 "builds": the launching shell, one render counted three times, three other ffmpeg processes |
| new | 4 builds, none of them the launching shell; the render counted once |

`python3 .claude/skills/_shared/buildcap.py --selftest` passes 20 of 20 cases (the RO-19 launch, a render with three
ffmpeg children, a watcher that greps for gate.py, three waiters, a newcomer). A live run with two real waiters showed
the second listing the first as ahead of it, the first not counting the second, and no marker left after both were
killed. `python3 .claude/skills/_shared/buildcap.py` prints what a tool would wait behind right now.
