# Ad 10 square (AS-06), round 2: build both squares (look locked by Dan 2026-10-03)

Created 2026-10-02. Recommended: **Claude Opus 5.5, High.** Session name: `My Dad Bod At 38 S/Sh Ad R2`.
Supersedes `handoff-20261002-ad10-square.md` (round 1 executed in the session of that name).

## State: look LOCKED by Dan 2026-10-03

- Dan's answer, recorded verbatim in `~/abs-review/as06-ad10/decisions.json`: *"The first minute looks good. That is
  approved. One change I want to make, though: I want to use the less aggressive centering that we recently developed
  ... where we reduced it by two-thirds, and apply that to that ... Everything else is approved."*
  So: graphics A (Soft Blue Light) with the Ad 10 wording as shown, every fill and card, labels and the caption
  recolour are approved. Nothing is pending. Build both files.
- **Centering (his one change), already applied:** the standard "land on him, then hold" track
  (`_shared/framing-motion.md`, policy `vertical-land-then-hold-20261003`): `kit_track.py --build build --tolerance 20`.
  `build/facetrack.json` is the new track; the vertical's own is `orig/facetrack_vertical.json`. On this ad's
  talking-head frames: travel 3,319 to 2,044 px (38 % less; the approved vertical's track was already a gentle one, the
  68 % figure was RO-10 against the old chase-everything track), crop moving 41 % of talk frames instead of 59 %, he
  sits 13.8 px off centre at the median. A 5 s square sample (10.9 to 15.9 s) rendered with it and looks right.
  **Do not rerun kit_track with another tolerance and do not copy the vertical's track back.** The first minute on the
  look page was rendered with the OLD track; the full build uses the new one. Say that in notes-square.md.
- The square's window is 1080 px wide around a 608 px track centre, so the gate's centring row and the hair check must
  be read on the delivered square, not assumed from the vertical.
- Look page (for reference): `http://127.0.0.1:8820/` (serve `~/abs-review/as06-ad10/sq/look/` with
  `_shared/review_server.py 8820` if it is down).
- Work dir (internal disk): `~/abs-review/as06-ad10/`. `build/` is a copy of the approved vertical build
  (`/Volumes/Extreme/_edit_work/kit9x16/ad10-master/`, which reproduces the delivered vertical SHA-256s b25b6e50 / 36ae2f6d).
  `orig/` keeps the vertical's untouched files. `sq/` is the square (sq_fit.json, plates.json, manifest.json, hf renders).

## What round 1 changed in the build copy (do not redo, do not undo)

1. `sbl_copy.json` -> `master_to_sbl.py` (content.json + sbl_sheet.json). Then **beats.json was patched by hand**, not
   rebuilt: re-running `build_kit.py` moved approved cuts, flashes and pushes (`orig/beats_regenerated_rejected.json`).
   Windows became `insets` (hfov W01..W04), titles became `hf` beats (T01, T02); pushes, flashes, words, seams and
   picture_cuts are byte-identical to the vertical's. `hf/manifest.json` only carries graphic times.
2. `assets_sq/`: daughter photos cropped out of his olive card, phone clips masked to the phone, phone_goal cropped above
   his italic tag. `assets.py` points at them (vertical's copy in `orig/assets_vertical.py`).
3. `label_kind: ai` added on phone_goal, ai_beach, ai_beach_end, gym_respect, wife_notices.
4. `captions.mov`: the vertical's layer padded with 268 empty frames (it ended at frame 5175 of 5443) and the lit word
   recoloured olive -> (104,197,255). First 5175 frames proven identical before the recolour (framemd5).
5. Stale local `kit_labels.py` moved to `orig/` (it shadowed the kit's and broke ffmpeg paths).
6. `sq/sq_copy.json`: 17 fills, 8 cards with reasons; gym chip moved by hand to (46,64) in sq_fit.json.
7. `facetrack.json` rebuilt at tolerance 20 on 2026-10-03 (Dan's centering change; see State).

## Next actions

1. No notes to apply: the look is locked. Read `decisions.json` and confirm `build/facetrack.json` carries
   `"policy": "vertical-land-then-hold-20261003"` before rendering.
2. Check two build slots with `~/abs-review/as06-ad10/slots.sh` (counts real workers only).
3. `sq_render.py picture --build build --out sq` (full 5,443 frames), then
   `sq_render.py mux --build build --out sq --vertical "<ad folder>/... | claude | 9x16 | ad 10.mp4" --name "my dad bod at 38 my dad bod at 40 | claude | 1x1 | ad 10"`
   (asserts the vertical's AAC stream md5).
4. Cutdown: cut the square picture at `recipe-vertical/cut-plan.json` frames (0-901, 2704-3242, 5170-5443) and mux the
   **vertical 59s file's** audio stream copied. Prove each seam against the square full.
5. Every gate at the current GATE_VERSION on both files (format for 1:1: check `_shared/deliver/formats.py`; RA-01's
   AS-13 recipe shows the square plan), `audio_gate.py --reference-mix <his> --verbatim`, label clearance on the delivered
   file, then three fresh judges per file and an independent `ra-reviewer` on both.
6. Deliver to `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/` (1x1 and 1x1 59s, REVIEW 540p copies,
   stamps, audio A/B, `notes-square.md`, `recipe-square/`), queue AS-06 to delivered, board line, send Dan the review
   copies with a numbered action list. **No upload.**

## Starter prompt

> Read `Handoffs/handoff-20261002-ad10-square-round2-full-builds.md`. Name this session "My Dad Bod At 38 S/Sh Ad R2".
> I locked the square look on 10-03 with one change, the calmer centering, which is already applied. Build the 1:1 full
> and 1:1 59 second squares of Ad 10 from the round 1 work on the internal disk, through every gate, three fresh judges
> and an independent review. Send me the review copies with a numbered action list. Do NOT upload anything. No em dashes.

Model and effort: Claude Opus 5.5, High.
