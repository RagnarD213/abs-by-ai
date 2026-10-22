# `softblue-sl18/`: SL-18 I'm 41. I Wasted My Life. shorts (R1, 2026-10-20/21)

The SL-15 batch renderer (`softblue-sl15/`, read its README and `softblue-sl07/README.md` first) adapted to cutting Shorts from an
APPROVED 1080p long-form MASTER instead of the raw roll (the handoff said: never the raw roll, never a review candidate). Work
folder: `/Volumes/Expansion/_edit_work/SL-18/` (copies kept in git; run from there; `sl18batch.py` is a symlink to `batch.py` so
other sessions' `pkill -f "batch.py track"` cannot kill it). Order: `snap.py` -> `batch.py audio` -> `patch_audio.py` -> `words, plan,
track, plan, words` -> `gfx, proof, render` -> `deliver.py copy` -> `runwatch.sh` -> judge + `ra-reviewer` -> `rungate.sh`.

## What is different from SL-15

- **The picture and audio are the master itself.** `lib.SRC` is the approved master; `batch.cam` decodes it BT.709 tv range with no
  grade. `A_pieces` is the master's own shot list: every edit-map entry start, its excluded false-start joins (`snap.py` writes them
  into `silence.json`) and the master's internal wide/close cuts found by scene detection (`plans.MASTER_CUTS`). Each shot gets a
  roll tag `M###` so a talking run that crosses a film cut becomes two shots (a size step); all tags read one decoder.
- **One-frame flash at a film cut:** frame rounding could show one frame of the next master shot in this shot's window. `picture()`
  clamps the source frame to the shot's own master range (`self.rng`).
- **Wide vs close master shots:** the film alternates a wide and a close camera. Wide shots (face about 218 px) take the 604 x 900
  window and close shots (about 290 px) the 724 x 1080 window, so his face is a similar size in every shot; where two shots of the
  same size meet, the master's own wide/close change is the size step. Measure `fw` in `track.json` per shot before choosing.
- **`plans.PATCH` repairs the film's own joins** in `audio.wav` AND `his_mix.wav` (the verbatim gate's reference): the RO-25 cut at
  film 386.786 had removed about 120 ms of the "ch" of "rich" (every Whisper run heard "ripped and ripped"); the film's processed
  full-roll mix (`round7/audio/baseline/full-Bass-2.wav`, on the round-1 cut-map clock, r 0.9998 after an offset fit) still has it,
  laid over the next take's silence. A `mute` patch fades a one-sample step or a stray exhale; never fade to digital zero for more
  than a few ms (a reviewer measured 121 ms of true silence): crossfade into the film's own room tone instead.
- **New HyperFrames template `_shared/hyperframes/line-graph/`** (not yet approved by Dan): the film's Pillow graph rebuilt in
  motion at 1080 x 1610; each segment draws on its words. Start the scene about 0.45 s before its cut (`cover t`) so the header is
  already drawing on the first frame (8 blank frames otherwise). Hide each segment until it starts: a round cap on a zero-length
  dash draws a stray dot.
- **New `clip_seq` options:** `pre` (an ffmpeg crop before scaling: black edge rows, a phone mock's white margin), `fit="tall"` with
  `ar` (a phone-screen clip shown whole above the captions), `round` (corners onto the field), `push` (a slow centred zoom), and
  `stack2` with `h` (two halves of a two-person 16:9 clip stacked, sized to end above the captions).

## What the reviews caught (four to five DOES NOT SHIP verdicts per short before SHIP)

- **The film's own approved AI clips failed today's checks.** DESK (pill and water): the glass returns as full as it started after a
  long drink, so the Short ends at frame 111. A0061 (pool couple): smears from frame 124 and its people stand 785-860 px apart, so a
  fill crop cuts both heads; a wider span card fixed it. A0085 (meal prep) dissolves into a second take at frame 63 and cuts the
  man's hair at the source top: dropped. Run `clipcheck.py` and a fresh `frame-reviewer` on every library or film AI clip.
- **A screen mock's hard screen switches fail `clipcheck` as "vanish"**: check each screen as its own range.
- **Pauses at every join:** a Short's joins must keep his natural 0.4-0.6 s between sentences; start the next piece in the silence
  before its first word (plus his breath) rather than at the word.
- **Overlapping film ranges break `film2out`:** two pieces must never share film time (a piece end at 370.55 and the next piece start
  at 370.30 sent a cover to the wrong piece).
- **Captions:** a cue never splits a phrase that closes within two words; never ends on a small connector (`SMALL` in batch.py);
  breaks at every picture cut including clip-to-clip; the lone-word merge never crosses a cut; check with the cue-vs-cut scan in
  the build log before rendering.
- **Key points:** distill, never echo the title or the words he says; land line 1 on the matching words, give line 2 at least 1.5 s.
- **Eyebrows are CAPITALS** (Dan, 2026-10-20, GRAPHICS-STANDARDS): the title band topic, the graph eyebrow, KEY POINT.
- **A cutaway shows what the line says:** a "No new matches" screen under "once I'd made more money" said the opposite.
- **Whisper on the whole delivered file hallucinates after a sentence-final word** ("productivity. activity."); confirm on a clean
  window with two models before treating it as a stumble.
- **`haircheck_v.py`** is the vertical headroom check the 2026-10-20 hair rule needs: every 0.25 s of each talking shot plus both
  native frames at every join, mask top measured from the picture area's top (canvas y 310).
- **A blended lead-in word has no clean cut.** The film's "So if you're on Adderall" is one run: from 149.32 the file opened inside the
  vowel of "So", and the "if" was a fragment 10-20 dB down. Whisper with a leading-silence pad prints "If" on any of those starts (a
  guess), so judge the first 150 ms on its own and the levels. The Short opens on "you're" (149.475); a pickup is the clean fix.
- **The gate's `style:static_run` (30 s) counts a long full-screen graph as one static scene** even though it animates: a 1.4x zoom
  CUT inside the graph (`zoom`, `fx`, `fy` on a second cover of the same mov) breaks it and emphasises the beat. Keep the zoom window
  clear of the header text (fy so the crop starts below the footnote).
- **`deliver.face_out` must use only the shot's own track samples:** the track runs 0.1-0.15 s past each end, across a film cut into
  the other camera, and blended a 1.37x size change into 1.14x, so the gate called a real size step a jump cut.
- **An audio-only fix is a remux** (`remux.sh`, frame count asserted): the picture's watch-pass verdicts carry over to the new file.
