# Review evidence receipts

Implementation support for the review workflow in `../SKILL.md`. That skill remains the editorial authority. This file adds no approval standard and does not change calibration, audio thresholds or later-round restraint.

`framing.py` decodes display orientation and sample aspect ratio before measurement. Its longest analysis dimension is 960 pixels. Portrait stays portrait. Proof thumbnails preserve the same shape. A decode failure or no assessable subjects raises an error instead of implying success. Its detections still need the source skill's visual adjudication.

## Coverage and benchmark freeze

Use `review_record.py` for capability tests and reviews where evidence coverage must be auditable. Keep the JSON and evidence in scratch space, outside Git. It checks declared coverage, existing nonempty evidence files, source hashes and unresolved judgments. It does not inspect those files or verify that a reviewer actually watched them. Never treat `bookkeeping_complete` as editorial approval.

State what each reviewer received. A model that receives still images has not heard audio or watched motion. External audiovisual analysis must name the model, supplied time range, sampling settings, prompt and saved response. Retain failures and usage. A player being open, an extracted frame directory, transcript or successful automatic scan does not establish completed viewing. Follow the source skill's required full-resolution checks even when external analysis is available.

Each `picture`, `motion` and `audio` coverage span has `start`, `end`, `reviewer`, `method`, `observations`, and `evidence`. The evidence path points to the actual review artifact, not merely the source media. Spans must cover the full duration without gaps. Keep incomplete spans and unresolved judgments visible; the validator should fail until they are resolved.

Record the following fields:

| Field | Required content |
|---|---|
| `source` | `path`, SHA256 in `sha256`, seconds in `duration`; also record editor, round and remote version identity |
| `benchmark_unseen` | True only if the current answer has never been exposed, including through calibration or earlier attempts |
| `coverage` | Separate `picture`, `motion`, `audio` arrays of spans |
| `joins` | `inventory_complete`, `items`: each has `time`, `observation`, `disposition`, `native_frames`, `motion_audio` |
| `ai_shots` | Same inventory wrapper; each item has `start`, `end`, `observation`, `disposition`, `consecutive_fullres`, `last_two_seconds`, `regions`, `motion` |
| `text_panels` | Same wrapper; each item has `start`, `end`, `observation`, `disposition`, verbatim `transcription`, `fullres`, `speech_timing` |
| `audio_measurements`, `framing_evidence`, `library_pass`, `calibration_selfcheck` | Paths to completed review evidence |
| `unresolved` | List of remaining judgments; must be empty for a freeze |

`disposition` is `editor_item`, `retained` or `private_summary`. An inventory with no items needs `none_reason`. Evidence paths can be absolute or relative to the record. For a multi-image proof, link a manifest that lists and hashes the images actually inspected, with observations. Do not record generated but unread frames as reviewed.

```sh
python3 .claude/skills/revisions/reference/review_record.py /scratch/review.json
python3 .claude/skills/revisions/reference/review_record.py /scratch/review.json --freeze /scratch/notes.md /scratch/summary.md --blind
```

Omit `--blind` for known-answer regression cases. Freeze writes a new `.freeze.json` once, hashing the source identity, record, notes, summary and evidence. It refuses missing coverage, missing evidence, unresolved judgments, prohibited dashes, an exposed blind test or an existing freeze file. Its `editorial_pass` is always null. Read the benchmark only after a successful blind freeze, then adjudicate differences against the footage and source rules. Retain the original frozen files.

## Focused tests

```sh
python3 -m unittest discover -s .claude/skills/revisions/reference -p 'test_framing_geometry.py'
python3 -m unittest discover -s .claude/skills/revisions/reference -p 'test_review_record.py'
```

Geometry tests cover portrait, landscape, square, anamorphic pixels, rotation metadata and missing input. Record tests cover missing runtime, gaps, changed source, missing AI endings, unresolved judgments, absent proof, exposed benchmarks and immutable freezes. Existing audio and watch self-tests remain separate requirements when applicable.
