# Handoff — Ad 5 vertical (Muhammad V3) — Dan's round-1 revisions

**Written 2026-09-11 by the session that built the vertical. Dan approved the build overall ("excellent job… audio sounds good,
cropping is good, all the graphics look good") with three revisions. This handoff executes them.** Delete this doc's entries
(here, `Handoffs/README.md`, the board) when the re-delivery is in the folder.

## What exists

| | |
|---|---|
| build dir | `/Volumes/Extreme/_edit_work/ad5-vert/` — the Python compositor pipeline (`beats.py` → `render5.py` → `zmux.py`), every gate, the recipe |
| delivered | `Muhammad Ad Videos/every diet you've tried failed for the same reason - ad 5/… \| claude \| 9x16 \| ad 5.mp4` (7,036 frames = his) and `… \| claude \| 9x16 59s \| ad 5.mp4` (54.99 s), review copies, A/B audio, stamps, `notes-vertical.md`, `recipe-vertical/` |
| skill | `/shortad-from-longform` — read it in full first, especially Step 4 (the editor's audio, untouched), Step 7 (the watch pass is the gate), and the **[A6]** and **[A7]** lessons; the a7 scripts are `reference/a7/` |
| audio | **Muhammad's, untouched** — the full length carries his AAC stream bit for bit (`zmux.py` asserts the md5), the cutdown his mix cut at the seams (`cut/his_mix.wav`). **Nothing in these revisions touches audio. Do not re-mux with anything else.** |

## Dan's three revisions (his words, 2026-09-11)

> "When the pictures come out at 15 seconds, I want all of them to be vertical and full screen. The landscape pictures, replace them
> with other pictures that are vertical and will fit easily into this full screen. You can also use the studio pictures that are
> edited and finalized, but make all the after pictures throughout this video vertical and full screen. Avoid the landscapes."

> "Throughout this video, whenever you're showing the after pictures, I want to start adding a label where we say, 'Real pictures
> of me, not AI-generated.' … Obviously, the one that is AI-generated, the one of me with the pool behind me, was my AI after
> picture. Keep that AI-generated label on all AI-generated content, but for my real after pictures, always apply that label."

> "Modify all video editing skills to always have that label on my real pictures." — **DONE 2026-09-11** by the writing session:
> the rule is in `AGENTS.md` ("Label Dan's real pictures"), `/shortad-from-longform` (standing content rules), `/ad-edit`,
> `/longform-edit`, `/shorts`, `/website-video`, `/make-ad`, `/editor-brief`, `/revisions`, `/imagesandclips`,
> `/scriptwriting`, and the editors' asset index. Nothing to do here except follow it.

## The beats to change (frames on his 29.97 grid; `beats.py` `T`)

Every REAL after picture of Dan in the cut, and what it becomes:

| frames | now | change to |
|---|---|---|
| 439–449 | `bleed` `07_SHOT4_photoshoot-standing.jpg` (portrait, red shorts) — already full-bleed | keep; **add the real-picture label** |
| 449–459 | `bleed` `06_SHOT3_photoshoot-towel-smile.jpg` (portrait) — already full-bleed | keep; **add the label** |
| 459–469 | `card` `04_SHOT1_photoshoot-smiling-trees.png` — **landscape in a card** | **replace with a portrait photo, full-bleed** (`bleed`, slow push), label |
| 469–500 | `card` `05_SHOT2_photoshoot-flag.jpg` — **landscape in a card** (his flash rides over 497–506) | **replace with a portrait photo, full-bleed**, label; the flash stays on its frames |
| 3549–3616 | `window` body `panels` — Dan above, two after photos in small cards below | Dan's rule is "all the after pictures … vertical and full screen": **two full-bleed portrait photos in sequence** (3549–3582, 3582–3616), each labelled, slow push. This drops Dan's window for 2.2 s — log it as a deviation from Muhammad's layout, on Dan's instruction |
| 6360–6425 | `card` `07_SHOT4…standing.jpg` (portrait in a card, blur-in) | **full-bleed** (`bleed`, keep the blur-in via a `blur=True` branch in `r_bleed` or drop it), label |

**Not real pictures — leave them alone, AI-GENERATED label stays:** the goal image card (3122–3220), the lock-screen phone
(2882–3020), the fat-Dan card (2605–2763), the app demo's result screen (6905–6954), every AI clip. The deckchair before
picture (138–211, 1035–1194) and the two fat-dad photos are real but they are BEFORE pictures — Dan's rule is about the after
pictures; leave them unlabelled.

### Picking the replacement portraits

* `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/06 Dan Photo Shoot Stills/` — 46 portrait
  `photo-NNN_FINAL_PRIMARY.jpg` at 2747×4096 (the pool shoot; SHOT3/SHOT4 are from here). The landscape ones are
  `Dan-flag-FINAL.jpg`, `photo-103/111/113/117/118…` — **do not use those**.
* `photos/finalized social media photos/` — 383 finals, 357 portrait: the pool-shoot picks AND the **studio** picks Dan named
  (`studio-white-*`, `studio-gray-*`, `studio-blue-*_FINAL_PRIMARY.jpg`; the `-IG-4x5` variants are 4:5 crops — prefer the
  full-height `_FINAL_PRIMARY.jpg`).
* Rules that decide the pick (memory `cover-photo-selection`, `thumbnail-design-system`): **abs visible and defined, never a
  soft or undefined shot**; the crop must keep hairline-to-shorts inside the tightest push (skill rule 12 — verify by drawing
  both push windows on the asset before rendering); the subject centred (`ox`) and the stomach in frame (`oy`, skill A5.22).
  Four distinct shots for 439–500 (his cut used four different pictures), two more for the 3549 pair. Contact-sheet the
  rendered 9:16 frames before committing (skill: "Contact-sheet the RENDERED 9:16 crop").

### The label

Add to `g5.py` beside `ai_chip_bleed`: `real_chip_bleed(im, y=None, size=54)` drawing **"Real picture of me — not AI-generated"**
in the same chip style (black rounded box, white Manrope SemiBold). Placement follows the AI-label rules already in the skill:
**low on the frame at the shorts/waist line, above the caption band (top of chip ≈ 1180–1230), never over his face**, wide
enough to read (the AI chip is ~54 px; this string is longer — wrap to two lines or drop to 44 px so it stays inside the
1080 width with 44 px margins). `r_bleed` takes `label='real'` / `label='ai'`; the AI chip keeps its current look.

### Then

1. `python3 render5.py --out picture.mp4` → `python3 zmux.py picture.mp4 ad5_vertical_9x16.mp4` (asserts his audio md5).
2. Gates, all of them, on the exact file: `audio_gate.py … --reference-mix his_mix.wav --verbatim --ab …`, `watch.py` +
   `zwatch_sheets.py` (look at every strip whose frames changed — diff against the previous `picture.mp4` with the gray-trace
   snippet in `chain10.sh`/`chain11.sh`, and state exactly which strips were re-looked at in `zwatch_mark.py`'s note),
   `caption_sync_check.py`, `zhairgate2.py`, `landing_check.py`, then the skill's `reference/qc.py … --build-dir .` (20/20).
3. The cutdown contains 439–500 (range 2) → `python3 zcutdown.py && python3 zcut_build.py`, render with
   `render5.py --cutplan cut_plan.json --out cut/picture.mp4`, mux with `cut/his_mix.wav`, the same gates from inside `cut/`.
4. **An independent Fable subagent audit on the delivered file is part of the skill (Step 7b) — run it, and expect a
   "does not ship" the first time; on this build the first two audits found eleven real defects the gates had passed.**
   Give it the changed spans and ask it to verify: every after picture full-bleed and portrait, the label on every real
   after picture and on no AI picture, no label over a face, nothing below y 1660, no frozen/black/sheared frame.
5. `python3 deliver5.py` (re-copies both masters + review copies + A/B + stamps + notes + recipe into the Ad 5 folder),
   update `notes-vertical.md` (a "Round 1 (2026-09-11)" section: what changed, the six pictures chosen and why), send Dan
   the 540p review copies, update the board entry, delete this handoff from `Handoffs/README.md` and the board.

## Traps specific to this build (read `[A7]` for the rest)

* **Odd-width raw frames shear** — keep every media size even (`g5.card_hole` does; a new `bleed` path is 1080×1920, fine).
* **`-ss` time seeks land on the wrong frame on these masters** — extract by index (`select='eq(n,N)'`).
* **The plate/overlay caches settle on their last element** — a new label is drawn per frame in `r_bleed`, not cached.
* The watch scan's one "unexplained jump" at 225.19 s is the app recording's own screen change — expected.
* `zcrop.py`'s punch demotion and `FORCE_VISIBLE` joins are build-specific measurements; do not re-run `zcrop.py` unless the EDL
  changes (it will not for these revisions — the talk frames are untouched).

## Starter prompt (Opus, high)

> Execute `Handoffs/handoff-20260911-ad5-vertical-revisions.md`: Dan's three revisions on the Ad 5 vertical
> (`/Volumes/Extreme/_edit_work/ad5-vert/`) — every real after picture full-bleed portrait (replace the two landscape shots and
> the photo-panels pair with portrait pool-shoot or finalized studio pictures), the new "Real picture of me — not AI-generated"
> label on every real after picture (AI-GENERATED stays on the AI ones), Muhammad's audio untouched. Load
> `/shortad-from-longform` first. Render, run every gate on the exact files (master and cutdown), the independent audit, then
> `deliver5.py`, notes, board. Model: Opus, effort high.
