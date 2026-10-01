# Answer keys for auto_content.py (the regression test)

Two hand-written content sheets the automatic one is scored against, and the scores it must not drop below.

| key | from | what it is |
|---|---|---|
| `ad10/` | AV-07, `/Volumes/Extreme/_edit_work/kit9x16/ad10-master/` | written fresh by a Codex session from Muhammad's Ad 10 master (delivered 09-24) |
| `ad1/` | Ad 1's approved vertical (`content_from_beats.py` over the approved `beats.py`) | carries Dan's own revisions (stock swaps, held photos, the after-reveal card), so it can never be matched fully by measuring the master |

Run (after `kit_recover.py` / `auto_measure.py` / `auto_content.py` on the ad's master in a build dir `B`):

```
python3 test_answer_keys.py --ad10 B10 --ad1 B1
```

It runs `compare_content.py` for each key with `--baseline answer_keys/<ad>/baseline.json` and exits non-zero if
any score drops or a real/AI label is swapped on the same picture. A deliberate improvement updates the baseline
with `--accept` (and the commit says why).
