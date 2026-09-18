# Handoff — Roll sidecars: analyse every footage roll ONCE, keep the answer forever (2026-09-18)

**Source:** Edit Pipeline Watchlist, entry 05 (https://claude.ai/artifact/NEfYBTQPo2raMmfZnaoE9v). Dan asked for this
handoff on 2026-09-18. **Tooling only — no video is edited, rendered, uploaded or published by this task.**

## Goal, in plain language

Every edit session re-learns the same facts about the raw footage — what Dan says in each clip, which microphone track
is the good one, what is on screen, which way the camera was turned — and then throws that knowledge away when the
session's scratch folder is wiped. Known costs so far: a 17-minute Whisper re-transcribe because a drive was unplugged,
a whole pass to work out which video 84 unlabelled clips belonged to, contact sheets rebuilt every session, and a
`/findassets` skill whose whole job is hunting by hand for footage Dan described in words.

Build one small tool that analyses a roll **once** and writes a permanent notes file ("sidecar") beside it, plus a
search command. After this, "find me a clip of Dan doing a vacuum from the front" is a text search, not a hunt — which
is also the first step toward fixing B-roll selection, the one stage of our edit that is still fully manual.

## Decisions already made (do not re-litigate)

1. **One sidecar per source clip**, two files, written next to the clip on the shoot drive:
   `<clip-stem>.roll.md` (human/agent-readable) and `<clip-stem>.roll.json` (machine-readable, same facts).
   Heavy artefacts live in a sibling folder `<clip-stem>.roll/` (`words.json` word-timed transcript, `contact.jpg`).
2. **A text-only mirror on the internal disk**, so the facts survive the Extreme drive being unplugged:
   `Media/footage-index/<shoot-slug>/<clip-stem>.roll.md|json` + `words.json`. `Media/` is already gitignored
   (`.gitignore:71`) — **the repo is public; sidecars never get committed.** No JPGs in the mirror.
3. **Identity = content, not path.** Key each sidecar on `size + sha256(first 64 MB + last 64 MB)`. Folder names on the
   drive contain `|` and `:` and get renamed; a moved or renamed clip must still find its sidecar.
4. **Local and free by default.** ffprobe, `pick_lav.py`, local Whisper, ffmpeg contact sheet. The only paid step is the
   optional "what is on screen" description (decision 6).
5. **Never overwrite a human-corrected field.** Any field carrying `"locked": true` in the JSON is preserved on re-run.
6. **On-screen description:** one Gemini call per clip over the contact sheet (not the video) → setting, framing
   (near/far, front/45°/profile), shirt on/off, exercise or action, props, other people. Falls under the standing
   $25/session AI-generation authorization; **state the estimate before the backfill batch and record the actual.**
   If the estimate for the whole backfill exceeds $15, run the pilot shoot only and report.

## What goes in a sidecar

| field | how it is produced |
|---|---|
| identity: content key, file name, shoot, size, duration | ffprobe + hash |
| picture: resolution, fps, rotation/portrait flag, codec, colour tags present or ABSENT | ffprobe. ⚠ Untagged = decode as BT.709 (memory `untagged-video-bt601-trap`) — record the fact, don't fix the file |
| audio layout + **which track is the lav** | `.claude/skills/_shared/audio/pick_lav.py` — per file, always (memory `shoot-828-slog3-format`: three roll families in the 8/28 shoot alone) |
| roll family / grade fit | which LUT/grade family the roll belongs to, from the shoot memory + `_shared/reference/picture.json`; `unknown` is an allowed value |
| transcript, word-timed | the existing chunked Whisper path (`.claude/skills/ad-edit/reference/whisper_chunked.py`, `longform-edit/reference/whisper_run.py` + `_shared/whisper-to-scribe.py`). **Reuse one of these; do not write a fourth transcriber.** |
| take list | transcript split at silences ≥ 1.0 s: start, end, first 12 words, `retake_of` when it repeats an earlier take. If a script doc is known for the shoot, the matched script line |
| shot list / on screen | decision 6, keyed to contact-sheet timestamps |
| contact sheet | one frame every 5 s (every 2 s for clips < 60 s), timestamps burned in |
| `used_in` (append-only) | `{job, in, out, date}` rows — written by a helper when a job's EDL is final, so clip-variety checks can ask "has this range already aired?" |

## Build

* `.claude/skills/_shared/rolls/roll_sidecar.py` with subcommands:
  * `build <clip-or-folder> [--no-describe] [--force]` — idempotent; skips a clip whose content key already has a
    sidecar unless `--force`.
  * `find "<words>" [--shoot …] [--framing front|45|profile] [--unused]` — searches transcript, take list and
    descriptions across the mirror (works with the drive unplugged); prints clip, in/out, the matching line, and the
    full path if the drive is mounted.
  * `show <clip>` · `mark-used <clip> --job DS-04 --in 123.0 --out 127.6` · `verify` (mirror ↔ drive agreement, orphans).
* `.claude/skills/_shared/rolls/README.md` — one page, plain language first.
* Tests beside it (`tests/test_roll_sidecar.py`): a 10-second synthetic clip; identity survives a rename; `locked`
  fields survive `--force`; `find` works from the mirror alone. Tests spend nothing (`--no-describe`).
* **Harvest before transcribing.** `/Volumes/Extreme/_edit_work/*/` already holds word-timed transcripts and lav picks
  for many rolls (ra01, ds04, ds-17, ro01, ad3-vert, …). Match them to source clips by file name + duration and import
  them instead of re-running Whisper. Record `transcript_source: harvested:<path>` vs `whisper:<model>`.
* **Respect the two-build cap.** Backfill is background work: before each Whisper run check the
  `Handoffs/video-editing/00-RULES.md` §1.3 process pattern and wait if two builds are running; run `nice`d. It must
  never take an edit-queue slot or make the dispatcher think a slot is busy — confirm with `dispatcher.py status`.

## Order of work

1. Build tool + tests. 2. **Pilot: the 8/28 shoot `main camera` folder** (every current RA/RO/DS job cuts from it):
`/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/`.
3. Prove it (below). 4. Backfill the other shoots on the Extreme drive (8/14, 8/3, 7/8, welcome-video, the GoPro
folders, `screen recordings`) and `03 B-Roll - Real Footage` + `04 AI-Generated Clips` in the asset library
(`/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/`; read its `00 START HERE - asset index.txt`).
5. Wire it in (below).

## Wire it into the pipeline (small text edits, no rule changes)

* `.claude/skills/_shared/EDITOR-CARD.md` and `Handoffs/video-editing/00-RULES.md`: one short rule — *"Before you
  transcribe, pick a lav or build a contact sheet for a source clip, run `roll_sidecar.py show`; if there is no sidecar,
  run `build` and use its output. When your EDL is final, run `mark-used`."*
* `scripts/edit-queue/preamble.md`: the same sentence, one line.
* `.claude/skills/findassets/SKILL.md`: make `roll_sidecar.py find` step 1 of the search, ahead of the manual hunt.
* Do **not** edit the per-skill transcription scripts in this task beyond calling them.

## Proof required before calling it done

* Pilot numbers: clips indexed, minutes of footage, transcripts harvested vs freshly run, wall-clock, Gemini spend.
* Three real look-ups answered by `find` alone, checked by opening the frames: (a) a front or 45° **dramatic vacuum**
  (DS-04's open revision — hand the candidates to that job's owner, do not edit DS-04); (b) every take of one RA script
  line; (c) a B-roll exercise clip not yet in any `used_in`.
* Unplug-proof: `find` returns the same hits reading only `Media/footage-index/`.
* `roll_sidecar.py verify` clean; tests pass.

## Out of scope / guardrails

No edits to any master, recipe, gate, threshold or corpus. No renames or moves of footage. No uploads. Nothing
committed from `Media/`. Commit and push only the tool, tests, README and the four text edits; nothing here deploys to
absbyai.com, so "live verification" is the proof list above. Re-read `AI_COORDINATION.md` from disk before finishing;
when done, delete this handoff's line there and its row in `Handoffs/README.md`, and report in chat.

## Recommended executor

* **Codex GPT-5.6 Sol / High** (recommended — tooling is Codex's lane per `codex-owns-non-core-work`, and Claude video
  work is frozen until 2026-09-24 11:00 CT).
* If Codex usage is tight: Claude **Sonnet 5 / High** after the 09-24 reset. Fable is not needed; this is careful
  plumbing, not judgment.

## Starter prompt

> Read `Handoffs/handoff-20260918-roll-sidecars-footage-index.md` and execute it end to end. Build
> `.claude/skills/_shared/rolls/roll_sidecar.py` with tests, harvest existing transcripts from
> `/Volumes/Extreme/_edit_work/` before running Whisper, pilot on the 8/28 shoot's `main camera` folder, produce the
> proof list in the doc, then backfill the remaining shoots in the background without ever taking an edit-queue slot.
> State the Gemini cost estimate before the description batch. Sidecars mirror to `Media/footage-index/` and are never
> committed (public repo). Commit and push only the tool, tests, README and the four small text edits. Do not touch any
> master, gate, threshold or footage file name.
