# Ad 13 "The Cost Of Getting Abs", round 3: opener motion, P03 redo, then the full videos

Written 2026-10-02 after Dan answered the round 2 page. Recommended: **Claude Opus 5.5, High**.
Sidebar name: `The Cost Of Getting Abs AD R3`. Previous: `handoff-20261001-ad13-round2-full-build-after-lock.md`
(read its bottom section "Round 2 delivered" for where every file is).

## What Dan decided (verbatim: `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/review2/decisions.json`)

- Opener START and END frames approved, vertical and horizontal. **Motion is authorized** for both.
- Colour approved. Centering approved (`kit_track.py --tolerance 12`).
- P06, P09 to P11, P20, P22 approved. The horizontal's first-minute graphics approved. P03 on the horizontal approved.
- **P03 on the vertical rejected.** "It doesn't really look like YouTube on the phone. I want this to look like a screen
  capture... you didn't show the full video; you just showed me cropped out of the video... Just cut off the bottom of
  the screen capture and put the captions beneath that."
- "Everything else is approved and good to go, so go ahead and build out the videos."

## Work, in order

1. Read `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `kit9x16/README.md` (section "A later round on
   a master build"), memories `ai-clip-artifact-giveaways`, `untagged-video-bt601-trap`.
2. **Opener motion (two clips, about 4 s each, start + end frame).** Frames: `round2/opener/{start,end}_{9x16,16x9}.png`
   (hashes in decisions.json). Action: one bench press rep with the robot spotting, the trainer walks toward camera with
   his box and looks back; camera locked off. Budget $5 for this video including retries; spend so far under one cent.
   Check every frame at full size, all of the last 2 seconds (hands, fingers, the bar, faces, the box). Upscale locally
   if the clip is under 1080 wide. Replace the two placeholder `img` beats in `sbl_copy.json` `add_pictures` with one
   `vid` beat 0.0 to 3.7 (new file name; keep `label_kind: ai`), and the two placeholder rows in `h16x9.py` `PICS`.
   The square uses the top square of the vertical clip. Register the clips in the clip library when the ad is approved.
3. **P03 vertical redo.** A real phone screen capture of the YouTube app playing "Crazy 3 Min Home Abs Workout - With Six
   Pack Shortcuts CEO Dan Rose" (id `GJHDRlepMTM`), portrait, the whole 16:9 video visible at the top, title, channel and
   4.47M subscribers under it. Same moment as now (about 8 to 15 s in: before the workout, Dan centred, Mike Chang at the
   side). First choice: record Dan's iPhone through iPhone Mirroring (standing authorization; memories
   `iphone-mirroring-control`, `iphone-mirroring-standing-authorization`). Fallback: screen-record Chrome's phone
   emulation of m.youtube.com. Then cut the capture off above the caption line (y 1400 of 1920) so captions sit on a
   plain dark area beneath it. No cropping of the video itself. yt-dlp does not work on this Mac.
4. **Full vertical + 59 s cut:** `kit_run.py --master ... --sbl sbl_copy.json --from restyle`, re-running the track by hand
   with `--tolerance 12` (the run's track stage uses 6), through picture, captions, mux, prewatch, three fresh judges,
   fold, pick, cutdown and its gate. Not proven yet on this path: `kit_plan.py`, the gate pre-check, `kit_cutdown.py`.
   52 % of the words sit under graphics: if caption rows object, shorten graphic times in the copy file, never a bound.
5. **Square:** `_shared/hyperframes/square.py` exists but Dan has not approved a square in the blue set. Standing rule:
   the first square gets its own short look page before square files are built. Build that page, then stop on it.
6. **Full horizontal:** extend `shortad-from-longform/reference/ad13-r2/h16x9.py` past the first minute: every later
   lower third, list card, price card (T02 to T05), tally values, CTA, picture, phone demo (P20 uses the approved
   workout demo) and flash, from `sbl_copy.json` and `beats.json`. His audio stream-copied whole. Then the `ad16x9`
   gate, judges and an independent `ra-reviewer`. It is a new deliverable: never replace the live video
   (`-SuKGXGcbIg` / `hrQf1240kQA`).
7. **One round 3 page:** finished vertical, 59 s cut, horizontal, the opener motion in context, the new P03, the square
   look. Serve it with `.claude/skills/_shared/review_server.py PORT DIR` (seeking works; never `python3 -m
   http.server`). Keep Dan's decisions to a handful. Nothing is uploaded: this is an ad, Unlisted via `/ad-setup` only.

## Traps

- `kit9x16/master_to_sbl.py` holds uncommitted edits from this job AND another session's Ad 6 work. Do not revert it.
- At most two builds at once on this machine; it was at load 70+ on 10-02. Run gates detached. No em dashes.
- Round 2's page stays at http://127.0.0.1:8814/ (`review2/`). Build round 3 in `review3/` on a new port.

## Starter prompt

> Read `Handoffs/handoff-20261002-ad13-round3-full-builds.md` and the files it lists. Name this session "The Cost Of
> Getting Abs AD R3". Generate the two approved opener clips, redo P03 on the vertical as a real phone screen capture of
> YouTube with the captions beneath it, then build the full vertical, its 59 second cut and the full horizontal, and the
> square look page. Show me one round 3 page. Do not upload anything.

Model and effort: Claude Opus 5.5, High.
