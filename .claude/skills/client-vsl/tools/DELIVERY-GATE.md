# Client video delivery gate (AD)

Use the final export with its actual sound. Keep the evidence in the private client job folder. Run the gate separately on every exported MP4 that will go on Dan's page or to the client, including any clean master or alternate pace. The review page builder and the delivery ledger both recheck the receipt before proceeding.

```sh
python3 .claude/skills/client-vsl/tools/delivery_gate.py FILE --job JOB --rows ROWS.json
python3 .claude/skills/client-vsl/tools/client_ledger.py gate JOB --stage deliver --file FILE --rows ROWS.json
```

The gate writes `FILE.delivery-gate.json` next to the movie, with the results and exact SHA-256. Keep the source files and evidence referenced by that receipt available to the page builder and delivery ledger. R5 builders accept `--video FILE --captions SRT --job JOB` after their existing `ROWS.json OUTDIR` arguments. R4's full-film builder requires `--rows ROWS.json`. Pass `--file` again for each additional client delivery variant.

## Export evidence

Under `JOB/delivery/<video-sha256>/`, save the following.

- **`inputs.json`** contains `sha256`, `editor`, `captions`, `captions_sha256`, `source_map`, and `source_map_sha256`. Use paths relative to that evidence folder or absolute paths. Supply the SRT from the final caption render at final playback speed. On a clean export use the matching delivery SRT. Save inputs from the actual export before changing any plans.
- **Source map** contains `kind: "source_ranges"`, `duration_s`, and ordered `segments` covering the complete rendered timeline. Each has `start_s`, `end_s` and `kind`. A `speaker` entry also has `source_fps` (a number or rational such as `"30000/1001"`) and `picture` and `audio` objects, each with `source` (the recording identifier) and `in_s` and `out_s` (times on that recording). Split entries at every cut, switch of source, or retime. Declare `cover` and `silent` entries with a `reason`. Include talking-head inserts and testimonials. Joint Vigor's prior exports can use `kind: "joint_vigor"` with the archived `plan`, `edl`, their `plan_sha256` and `edl_sha256`, `start_s`, `end_s`, `pace`, `duration_s`, and `exclude` (removed ranges in plan seconds). The legacy map interrogates the rendered camera plan and dialogue edit list. Precomposited inserts require their own audiovisual review.
- **`blind-review.json`** comes from an independent reviewer. Give the reviewer the export and the client's original instructions, without the editor's claimed fixes or timestamps. The report records `sha256`, `reviewer`, `reviewer_session`, `reviewed_at` (ISO-8601 with time zone), a specific `method`, `blind: true`, `moving_video: true`, `audio: true`, `whole_film: true`, `reviewed_duration_s`, `verdict: "PASS"`, `findings: []`, and `row_verifications` keyed by row ID. A PASS entry contains `result: "PASS"`, `client_words`, `fix` (the reviewer's confirmed description, shared with the page), `observed` (specific visible or audible evidence), `spoken_quote` and `t` (seconds into this export). The reviewer must be able to inspect movement and the audio together. A contact sheet, waveform measurement or picture-only model cannot sign this report. An API processing audio is silent on the Mac.
- **`ROWS.json`** is the page data. Its `asked` array holds `id`, `words` (the client's exact note), `fix`, `verdict`, and `t`. Use `"Done"` only with reviewer proof. Copy the client's quoted spoken phrase into `spoken_quote` if the client supplies one. For a note that gives no dialogue quote, the reviewer selects the words heard at the fix. Use enough consecutive words to identify a unique occurrence near the time. The gate finds the quote in the final-file Whisper transcript and checks both the reviewer's and page's timestamps. The builder uses the transcript time and displays **not yet** for every other row.

## What runs

1. Local Whisper decodes the final audio, checks the captions and supplies transcript timestamps.
2. The saved render plan and dialogue edit list check the picture and audio source times within one source frame on every declared speaking segment.
3. Gemini receives the moving video with audio in consecutive portions, and timecodes any lip-sync or picture-versus-speech problems. The subscription CLI is tried first. If it cannot inspect movement with sound, the authorized Gemini API fallback requests six video samples per second alongside its audio track. The gate reserves less than $5 before running paid checks and saves the responses. Gemini samples the picture, so the source-frame comparison and the separate blind review remain required.
4. The gate requires all of those checks, a passing blind review, and transcript proof for every Done row on the exact file. If one fails or evidence is missing, the receipt cannot be used to build a page or pass the client delivery ledger.
