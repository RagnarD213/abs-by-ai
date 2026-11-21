# Handoff: cut the filmed B-roll into the clip library (2026-09-29)

## Goal
Turn the 68 ranked B-roll moments in Dan's raw shoot rolls into short, graded, ready-to-drop clips and register each
one in the clip library, so human and AI editors can pull them by ID instead of scrubbing raw footage.

## Decided already (do not re-ask Dan)
- Library, catalog and tool exist: read `.claude/skills/_shared/cliplib/README.md` first.
- Filmed B-roll lands in `03 B-Roll - Real Footage/dan-filmed/` via `clip_library.py add ... --kind real --category dan-filmed`.
  `add` copies the file in, makes previews, uploads to Drive (anyone-with-link inherited) and assigns the B#### ID.
- Raw rolls are never modified, moved or renamed.
- Default audio: MUTED (B-roll sits under a voiceover). Keep audio only where the cut list says `audio: keep`, and then
  follow the `/findassets` audio standard (`pick_lav.py`, lav mono to centred stereo, `audio_gate.py --synthetic`).

## Input
`Media/clip-library/broll-cut-list.json` (68 moments: source roll, in/out, slug, description, tags, framing,
orientation) and the readable table `broll-cut-list.md`. Categories: exercise 39, food/meal prep 11, physique 7,
lifestyle 7, supplements 4. Shoots: 8:28 (23), 8:3 (21), 7:8 (11), welcome-video (8), 8:14 (5).

## Recipe per moment
1. `python3 .claude/skills/_shared/rolls/roll_sidecar.py show <roll>` for the roll facts (rotation, grade family, lav).
2. Nudge in/out to a clean start (rep start, hand entering frame). The list's times sit on 5-second contact-sheet
   spacing. Target 4-10 s. Skip a moment that turns out unusable (crew in frame, exposure pumping) and note it.
3. Picture: **8:28 rolls C1673-C1685 are S-Log3** and must be graded; use the approved 8/28 grade in
   `.claude/skills/longform-edit/SKILL.md` / `ad-edit/SKILL.md` (search "S-Log3"). Every other shoot is S-Cinetone
   (8:3, 8:14, 7:8, welcome) and needs at most the family grade those skills record. Decode untagged video as
   BT.709 (memory `untagged-video-bt601-trap`). Dan is small in frame on the 8:28 poolside rolls: crop in, keeping
   the whole head and hair in frame (`VIDEO-RULES.md` "Hair never leaves the frame").
4. Keep native orientation (portrait rolls C1654-C1672 stay 9:16; landscape stays 16:9). 1080p (1080x1920 or
   1920x1080), H.264 CRF 16, 29.97, `-an` unless keeping audio.
5. Look at a 6-frame contact sheet of the cut before registering it.
6. Register: `clip_library.py add CUT.mp4 --kind real --category dan-filmed --slug <slug> --description "<desc>"
   --people dan --tags ... --notes "source <roll> <in>-<out>, graded <recipe>"`.
7. `roll_sidecar.py mark-used <roll> --job CLIPLIB --in <in> --out <out>` so the raw index knows it was cut.
8. After the batch: `clip_library.py sheet` and `clip_library.py verify` (0 problems).

Work folder for intermediates: `/Volumes/Extreme/_edit_work/broll-cuts-20260929/`. Max two ffmpeg builds at once
(`VIDEO-RULES.md`). No AI spend is needed.

## Done means
Every usable moment is a B#### clip in the catalog and on Drive, the Sheet shows them with thumbnails, `verify`
passes, the skipped moments are listed in `broll-cut-list.md` with a reason, and the HANDOFFS line in
`AI_COORDINATION.md` plus the `Handoffs/README.md` row are deleted. Commit the cut-list update and nothing from
`Media/` (gitignored, repo is public).

## Known gaps to report to Dan (not to fill)
No gym establishing shots, weigh-ins or scenery-only footage exist in any shoot; the 9/23 shoot has no usable B-roll.
A future shoot could add them.

## Starter prompt
> Execute `Handoffs/handoff-20260929-cut-broll-into-clip-library.md`: cut the 68 B-roll moments from
> `Media/clip-library/broll-cut-list.json` into graded clips and register each with `clip_library.py add`.

Recommended model: Opus 5.5, medium effort.
