# Roll sidecars

This tool remembers what is in every source clip so an editor does not have to inspect the same footage again. It records the transcript, mic choice, picture facts, take boundaries, on-screen action, contact sheet, grade family, and ranges already used in finished edits.

The source video is never renamed, moved, re-encoded, or changed. A build writes:

- `<clip-stem>.roll.md` and `<clip-stem>.roll.json` beside the source clip.
- `<clip-stem>.roll/words.json` and `<clip-stem>.roll/contact.jpg` beside the source clip.
- A text-only copy under `Media/footage-index/<shoot>/`, without the JPG, so search works while the Extreme drive is unplugged.

`Media/footage-index/` and all source-drive sidecars are private working data. Never commit them to Git because the repository is public.

## Normal use

Run every command from the project root:

```bash
python3 .claude/skills/_shared/rolls/roll_sidecar.py show "/path/to/C1656.MP4"
python3 .claude/skills/_shared/rolls/roll_sidecar.py build "/path/to/one clip or a folder"
python3 .claude/skills/_shared/rolls/roll_sidecar.py find "dramatic vacuum" --shoot "8:28" --framing front --unused
python3 .claude/skills/_shared/rolls/roll_sidecar.py mark-used "/path/to/C1677.MP4" --job DS-04 --in 8.0 --out 13.0
python3 .claude/skills/_shared/rolls/roll_sidecar.py verify
```

Always run `show` before starting a new transcript, mic analysis, or contact sheet. When an edit's EDL is final, run `mark-used` for every source range it uses.

`build` is idempotent. It hashes the first and last 64 MB plus file size, so a renamed or moved clip still finds the same record. Use `--force` to refresh generated facts. Any JSON object with `"locked": true` is treated as a human correction and survives a forced rebuild.

Use `--no-describe` when the paid Gemini picture description is not needed, including all tests. Before a real description batch, state the estimated Gemini cost. The tool records the returned token counts and estimated actual charge in each JSON sidecar.

## How a build works

1. Probe the clip with ffprobe and calculate its content identity.
2. Search `/Volumes/Extreme/_edit_work/` for an existing word-timed transcript and lav pick with the same source name and matching duration.
3. Run the shared `pick_lav.py` only when no valid lav result can be harvested.
4. Run the existing chunked local Whisper script only when no valid transcript can be harvested.
5. Build a timestamped contact sheet at 2-second spacing for clips under one minute, otherwise 5-second spacing.
6. Optionally send that JPG, never the video, to Gemini for searchable visual descriptions.
7. Write matching drive and local-mirror sidecars.

Before every ffmpeg or Whisper operation, the tool checks the shared two-build cap. If two other builds are active, it waits. The process is run at reduced priority and never claims an edit-queue job or slot.

## Human corrections

Lock only the field that was corrected. For example:

```json
"grade": {
  "value": "8/28 outdoor daylight family, approved 1.15x fit",
  "locked": true
}
```

The rest of the sidecar can still refresh. `used_in` is append-only through `mark-used`.

## Tests

```bash
python3 .claude/skills/_shared/rolls/tests/test_roll_sidecar.py
```

The tests create a private 10-second synthetic clip, use a harvested local transcript, make no Gemini calls, and prove rename identity, locked-field preservation, and mirror-only search.
