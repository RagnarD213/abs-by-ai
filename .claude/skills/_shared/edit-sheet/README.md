# The edit sheet: one file every finished 16:9 writes next to its master

**What it is.** `<master name>.edit-sheet.json`, written at delivery by whoever edited the 16:9 (Claude or Codex). It is
the answer sheet of the edit: which takes, which frames, which crop, which words, which graphics with what text, which
pictures and whether each is real or AI, which audio, and what Dan approved. Any later build of the same film in another
shape (9:16, 59 s cutdown, square, shorts) reads this file instead of reverse-engineering the finished video.

**Why (Dan, 2026-10-01).** "I plan to edit all videos with Claude and Codex going forward." The vertical kit
(`shortad-from-longform/reference/kit9x16/`) spent over an hour of every build recovering these facts from an editor's
master by measurement, and stopped whenever it was unsure. When we made the 16:9 ourselves, the facts already exist.

**Rule.** A missing field is caught when the 16:9 is DELIVERED, not when the vertical is built. `validate.py` runs in
the delivery step of `/longform-edit` and `/ad-edit` and of Codex's `$long-form-content-edit`; a failing sheet blocks
the delivery gate stamp.

```
python3 validate.py SHEET.json            # exit 0 = complete; exit 1 names every missing or wrong field
python3 validate.py SHEET.json --hash     # also re-hash the master and check every file path exists (slow on a big master)
python3 sheet_from_claude_build.py BUILD_DIR [--master FILE] [--out SHEET.json]     # Claude's builds
```

## Format (`schema: "abs-edit-sheet/1"`)

All times are seconds on the DELIVERED timeline unless a field says `src_` (seconds in the raw roll). Frame numbers are
on the 30000/1001 grid. Paths are absolute.

| key | what it holds | why the vertical needs it |
|---|---|---|
| `job`, `title`, `type`, `editor` | `RO-10`, the film title, `LFC` / `SFC` / `AD`, `claude` / `codex` | naming, format of the gate |
| `video` | `master`, `sha256`, `fps`, `frames`, `duration`, `width`, `height`; `rolls` {name: {`path`, `width`, `height`, `fps`}} | binds the sheet to one exact file; where the raw is |
| `grade` | `filter` (the ffmpeg chain applied to the raw, after any crop), `order` (`after_scale_1080` = the 16:9 scaled the crop to 1920x1080 first and graded that; `at_source_size` = graded at the raw's size), `lut` (path or null), `decode` (`bt709`), `note` | the vertical regrades the RAW the same way |
| `edl` | every picture segment in order: `roll`, `src_in`, `src_out`, `out_in`, `out_out`, `src_f0`, `out_f0`, `out_f1`, `shot`, `audio` (`sync` = the audio is the same source span; else {`src_in`, `src_out`}), `join` (`cut` = a take change, `reframe` = same take, picture only) | the exact frames; no pose matching, no take search |
| `framing` | per segment: `name` (`W2`, `T2`, ...), `crop` [w, h, x, y] in raw pixels, `head` {`hair_top`, `cx`, `chin`} in raw pixels (min hair top over the shot, median centre), `measured` (how) | the vertical re-frames from the RAW, hair-anchored; it needs where his head is, not the 16:9 pixels |
| `words` | `list` [{`w`, `t0`, `t1`}] on the delivered timeline, `timing` (`ctc` / `mapped-source` / `whisper`), `fixes` [[heard, shown]] | captions, graphic timing, cutdown picker |
| `graphics` | one entry per graphic: `id`, `template` (a `_shared/hyperframes/` folder name, or `softblue:<fn>`), `config` (the template's own config with FILM-time word starts, so it re-renders at any shape), `text` (every string on screen), `t0`, `t1`, `layer` (`overlay` over Dan, `side` moves Dan, `full` replaces the frame), `driven_by` [{`part`, `phrase`, `t`}] | text and timing are never retyped |
| `pictures` | every photo or clip: `id`, `t0`, `t1`, `kind` (`clip`, `photo`, `phone`), `sources` [{`path`, `src_in`, `frames`}], `label_kind` (`ai`, `real`, `none`), `label` (the chip text), `people` (`dan`, `other`, `none`), `physique` (true if a bare physique), `approved_crop` (null or {`path` or `box`}), `library_id`, `note` | labels are facts here, never a model's guess and never a library match |
| `audio` | `mix` (the delivered mix: the master itself), `untreated` (the untreated assembly the audio gate compares against), `gate_stamp`, `chain` (voice chain record), `music` (path or null) | the audio gate needs both |
| `approvals` | `status` (`approved`, `pending`), `round`, `decisions` [{`id`, `verdict`, `dan`, `scope`}], `source` | the vertical does not re-ask what Dan already decided |
| `provenance` | `written`, `by`, `build_dir`, `inputs` {file: sha256 of the build files it was made from} | audit |

### Rules the validator enforces

- `edl` covers 0 to `video.frames` with no gap or overlap; every segment names a roll that `video.rolls` has.
- Every `edl` segment has a `framing` row; every `framing.crop` lies inside its roll; `head.hair_top` is above `head.chin`.
- `words.list` is in time order, inside 0..duration, and not empty.
- Every graphic has a known `template`, a non-empty `config`, `t0 < t1`, and every string in `text` appears in the config.
- Every picture has `label_kind`. A picture with `people: "dan"` and `physique: true` must be `ai` or `real` (exactly one
  label, VIDEO-RULES). A picture never gets `label_kind` from a guess: the writer must cite `label_source`.
- `audio.untreated` and `approvals.status` exist. With `--hash`: every path exists and `video.sha256` matches the master.
- Unknown top-level keys are an error (a typo must not pass as an optional field).

### What is deliberately NOT in the sheet

The vertical's own design (which clip is a card, where a push goes, the cutdown ranges): the kit decides those from its
template and its measured rules. Gate verdicts: the vertical is gated as its own file.

## Writers

- **Claude builds** (`/longform-edit`, `/ad-edit` round-method builds: `edl.json`, `shots.json`, `plan_resolved.json`,
  `words_out.json`, `hf/`, `<master>.build.json`): `sheet_from_claude_build.py`. Proven 2026-10-01 on RO-10 (long-form, HyperFrames
  graphics: 53 segments, 1,673 words, 24 graphics, 21 pictures) and RA-01 (ad; older adkit graphics, so its
  `graphics[].template` are `adkit:*` and a vertical stops on them until they are re-authored from the templates).
  Both pass `validate.py --hash`. Who is in a picture comes from the plan item (`people`, `physique`), a `--facts`
  file, or the clip library; never a guess.
- **Codex builds**: see `CODEX.md` here (what Codex's builds record today, what is missing, and the instruction).

## Readers

- `kit9x16/kit_run.py --sheet SHEET.json --build B --name "..."` (the vertical and its 59 s cutdown).
