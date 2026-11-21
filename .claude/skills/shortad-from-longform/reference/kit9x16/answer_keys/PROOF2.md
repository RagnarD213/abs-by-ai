# Proof 2: Ad 10 rebuilt by `kit_run.py`, through the gate (2026-10-01)

Build: `/Volumes/Extreme/_edit_work/kit9x16/auto-ad10-run2` (recover, measure, content, kit, render, gate; no hand
edit of the content sheet; every fix went into the kit). The delivered AV-07 (Dan-approved 2026-09-25) stays in the
ad folder untouched; this is the proof build.

| | full 9:16 (3:01.6) | 59s cutdown (0:53.3) |
|---|---|---|
| `gate.py --format ad9x16` | PASS, 0 open defects | PASS, 0 open defects |
| audio (`--verbatim`, his mix) | PASS | PASS |
| judged watch pass | 298 entries, 0 defects | 100 entries, 0 defects |
| escalations | 0 | n/a |

## Frame differences against the delivered AV-07 (`compare_renders.py`, mean grey levels per beat)

Two encodes of one picture read 1 to 2. Median per beat kind: title cards 0.3, full-bleed photos 1.7, cards 2.3,
windows 5.3, lower thirds 9.5, CTA pills 11.3, talk 10.9. Every beat over 12, explained:

| beat | diff | why |
|---|---|---|
| 63.1 and 65.1 s dad photos | 40, 28 | Dan's approved Ad 1 crops (head and stomach in) instead of AV-07's lifted frames |
| 93.2 s phone clip | 25 | his moving clip instead of AV-07's single still frame |
| 106.2 s photo | 42 | the kit shows photo-74, which is what his master shows; AV-07 used photo-10 (a key error) |
| 121.8 to 125.7 s and 172.8 to 176.8 s app screens | 12 to 18 | the phone is cropped to the phone, and the real-picture chip shows only while the uploaded photo is on it |
| 127.2 to 138.6 s window | 20 | the window ends 0.2 s earlier so "30 minutes" is captioned; Dan sits a little differently in the window |
| 23.3 and 69.1 s lower thirds | 24, 14 | his measured times instead of AV-07's hand-rounded ones; faster type-on |
| talk (median 10.9) | | the picture cuts on his cut frame (AV-07 moved 22 cuts for pose), and the kit measures where Dan sits in the frame from the raw roll (862 px) instead of assuming centre |

## The model judge against the session judges (same renders, same images)

| render | session judges (3 fresh agents) | Gemini 2.5 Flash | Gemini 3.8 Flash | Gemini 3.1 Pro |
|---|---|---|---|---|
| first automatic build | 6 defect moments | caught 2 of 6 | 0 of 6 | 0 of 6 |
| second build | 13 defect moments | not run | 1 of 13 | 4 of 13 |
| cost per pass | (session tokens) | not recorded | $0.36 to $0.53 | $1.23 to $1.88 |

Both stronger models found one real defect the session judges missed (a doubled AI label), and missed most of
what the session judges caught (one-frame leaks at cuts, a look-away, caption errors). Verdict: the model judge is a
useful second opinion (`--judge both`), not a replacement. The watch pass stays with fresh session judges.

## What the judged rounds changed in the kit

Nine judged rounds on Ad 10 and Ad 8 produced about 40 kit fixes (README: round-4, round-6, gate-round and cutdown
lessons). The last full round on each ad returned 0 defects from all judges with no hand edit anywhere.
