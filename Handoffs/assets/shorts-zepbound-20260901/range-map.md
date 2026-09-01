# Zepbound long-form (02) — EDL range map with approximate master timecodes

Generated 2026-09-01 from `.claude/skills/longform-edit/reference/ranges_zepbound.py` (the cut's own EDL,
raw roll `C1513.MP4`, grade `curves=all='0/0 0.069/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'`).

⚠ **Master timecodes are APPROXIMATE.** They are cumulative range durations; `render.py` rounds every
range to whole frames and the error accumulates monotonically (measured +1.137 s over 62 ranges on 03).
This EDL also sums to **30:46** against a delivered master recorded as **30:28**, so the shipped cut was
trimmed after this file was written. **Use the labels to find beats, then re-derive every timecode
against the actual master's SRT (1009 cues) and Whisper word timestamps.** Raw in/out are exact.

| # | master ≈ | dur s | raw in | raw out | label |
|---|---|---|---|---|---|
| 1 | 00:00.00 | 19.7 | 72.40 | 92.10 | `intro` |
| 2 | 00:19.70 | 19.1 | 121.00 | 140.05 | `why-i-started` |
| 3 | 00:38.75 | 45.2 | 146.60 | 191.85 | `heard-about-it` |
| 4 | 01:24.00 | 20.6 | 192.25 | 212.85 | `my-old-thinking` |
| 5 | 01:44.60 | 88.7 | 221.55 | 310.25 | `the-data-changed-my-mind` |
| 6 | 03:13.30 | 9.5 | 315.15 | 324.65 | `anecdotes` |
| 7 | 03:22.80 | 30.1 | 331.25 | 361.30 | `started-recommending-it` |
| 8 | 03:52.85 | 35.8 | 364.15 | 399.90 | `30-pounds-math` |
| 9 | 04:28.60 | 44.4 | 408.70 | 453.10 | `even-ripped-people` |
| 10 | 05:13.00 | 34.8 | 455.90 | 490.70 | `my-diet-was-good` |
| 11 | 05:47.80 | 79.3 | 494.30 | 573.60 | `good-isnt-perfect` |
| 12 | 07:07.10 | 40.9 | 576.05 | 616.90 | `not-medical-advice` |
| 13 | 07:47.95 | 32.2 | 621.15 | 653.35 | `old-vs-new-thinking` |
| 14 | 08:20.15 | 99.0 | 676.00 | 775.00 | `the-transformation` |
| 15 | 09:59.15 | 15.6 | 775.00 | 790.60 | `alcohol-knockout` |
| 16 | 10:14.75 | 12.9 | 791.05 | 803.95 | `how-much-i-drank` |
| 17 | 10:27.65 | 22.4 | 804.50 | 826.85 | `blowouts-gone` |
| 18 | 10:50.00 | 66.2 | 838.80 | 904.95 | `sugar-carbs-productivity` |
| 19 | 11:56.15 | 19.8 | 916.60 | 936.40 | `if-youre-obese` |
| 20 | 12:15.95 | 37.4 | 938.65 | 976.00 | `if-youre-ripped` |
| 21 | 12:53.30 | 15.6 | 976.00 | 991.65 | `how-to-do-it` |
| 22 | 13:08.95 | 31.6 | 992.15 | 1023.70 | `where-to-get-it` |
| 23 | 13:40.50 | 55.5 | 1032.40 | 1087.90 | `compounded-vs-brand` |
| 24 | 14:36.00 | 29.9 | 1093.80 | 1123.70 | `no-added-ingredients` |
| 25 | 15:05.90 | 11.1 | 1129.30 | 1140.40 | `lily-direct` |
| 26 | 15:17.00 | 43.0 | 1145.10 | 1188.10 | `how-to-get-a-script` |
| 27 | 16:00.00 | 16.1 | 1191.90 | 1208.05 | `skip-the-membership-fees` |
| 28 | 16:16.15 | 102.0 | 1213.90 | 1315.95 | `oral-pen-or-needle` |
| 29 | 17:58.20 | 126.9 | 1329.30 | 1456.20 | `where-to-inject` |
| 30 | 20:05.10 | 16.1 | 1461.50 | 1477.60 | `which-day` |
| 31 | 20:21.20 | 21.4 | 1484.60 | 1506.00 | `why-thursday` |
| 32 | 20:42.60 | 10.1 | 1509.40 | 1519.50 | `inject-thursday-7pm` |
| 33 | 20:52.70 | 45.7 | 1529.05 | 1574.75 | `my-side-effects` |
| 34 | 21:38.40 | 26.7 | 1586.90 | 1613.60 | `escalate-gradually` |
| 35 | 22:05.10 | 6.3 | 1616.10 | 1622.40 | `context-max-dose` |
| 36 | 22:11.40 | 15.8 | 1626.70 | 1642.55 | `tiny-dose` |
| 37 | 22:27.25 | 17.5 | 1645.40 | 1662.95 | `dose-ladder` |
| 38 | 22:44.80 | 33.3 | 1665.90 | 1699.25 | `where-i-sit-now` |
| 39 | 23:18.15 | 25.1 | 1703.25 | 1728.35 | `digestion-improved` |
| 40 | 23:43.25 | 24.4 | 1733.35 | 1757.70 | `biggest-mistake` |
| 41 | 24:07.60 | 52.1 | 1777.10 | 1829.20 | `wont-damage-your-skin` |
| 42 | 24:59.70 | 51.8 | 1836.20 | 1888.05 | `it-doesnt-hurt` |
| 43 | 25:51.55 | 51.7 | 1895.15 | 1946.85 | `dont-go-above-2.5` |
| 44 | 26:43.25 | 9.9 | 1952.30 | 1962.15 | `unless-youre-obese` |
| 45 | 26:53.10 | 25.1 | 1981.90 | 2007.00 | `ice-if-youre-scared` |
| 46 | 27:18.20 | 43.8 | 2007.00 | 2050.85 | `muscle-loss-is-the-risk` |
| 47 | 28:02.05 | 35.8 | 2060.60 | 2096.35 | `protein-target` |
| 48 | 28:37.80 | 14.6 | 2115.30 | 2129.90 | `wrap-obese-diabetes` |
| 49 | 28:52.40 | 35.2 | 2142.40 | 2177.65 | `wrap-20-30-lbs` |
| 50 | 29:27.65 | 78.6 | 2200.40 | 2279.00 | `outro` |

EDL total ≈ 30:46.25 (1846.2 s).
