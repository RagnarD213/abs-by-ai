CONTENT | SL-06 | Top 5 Zepbound Tips SFL R4

# SL-06: shirtless gym flex intros (all six, regenerate), better thigh-injection clips for C, then motion and rebuild

Written 2026-10-18 by Claude (Opus 5.5), from the "Top 5 Zepbound Tips SFL R3" task after Dan's reply to the stage 1 page.
**Recommended: Claude Opus 5.5, high effort.** (Twelve new AI frames with a fresh reviewer each, a new YouTube search,
then Flow motion, six re-renders and the full gate chain.)

## Dan's reply (2026-10-18, verbatim)

`/Volumes/Extreme/_edit_work/sl06/round3/DAN_R3_STAGE1_NOTES.md`. Recorded in `/Volumes/Extreme/_edit_work/sl06/decisions.json`
(`R3_stage1`). Summary:
- **All six pairs regenerate:** Dan **shirtless**, a **real gym setting** behind him (not a blank wall), and the poster **looks
  like a real poster** (designed, less plain). Poster texts, poses, the tiny vial, the pointing hand and the timing stay.
- **All three C clips rejected** (Nurse Scott, Clinical Skills Training, Karli Sine). Find better ones: **a doctor injecting
  into the thigh, or someone injecting into the FRONT of the thigh.** He says better thigh videos exist.

## What stays from R3 stage 1 (reuse, do not redo)

- Folder `/Volumes/Extreme/_edit_work/sl06/round3/` (never overwrite `round2/`). Stage 1 page: http://127.0.0.1:8821/ (refresh
  it in place with the new frames and clips: `python3 page_r3a.py`, then `review_server.py 8821 .../round3/page`).
- Scripts (copies in the main folder at `.claude/skills/shorts/reference/softblue-sl06/round3/`, local commit 2ba01bb):
  `preview_intros.py` (stills in place, AI chip placement per short), `preview_c_open.py` (C's opening with montage, card crops,
  credits, captions), `page_r3a.py`, `yt/dl_low.sh` and `yt/dl_hd.sh`. Lessons: `softblue-sl06/README.md`, "Round 3 stage 1".
- Frame specs `aiframes/{A..F}.spec.json` (poster still boxes, vial boxes, `person.reach: false`). **New frames need new boxes:**
  mark them on a gridded zoom of the new START (the poster lines and the vial), and add gym equipment that must stay still
  (a rack upright, a plate rim) as `still` boxes. Old frames and reviews: move them to `aiframes/rejected/R3a/`.
- Poster texts (exact, Dan's case): D "Inject Zepbound Thursday evening" (plus the calendar with every Thursday circled, a real
  30-day month); A "Start at 1 mg, not 2.5 mg"; B "Use a needle, not a KwikPen"; C "How to inject Zepbound"; E "Come off
  Zepbound without regaining fat"; F "How much protein do you need on a GLP-1?". Heads: A 4.14, B 4.61, C 2.84, D 3.28,
  E 3.15, F 2.50 s.
- Prompts in `aiframes/prompts/` (`_common2.txt` + `{S}_start2.txt`, B adds the clean-skin lines; END: `_end_common.txt` +
  per-short changes). What made the likeness work: `refs/face_sheet.jpg` (four real faces) as ref1 plus the "LIKENESS IS THE
  MOST IMPORTANT THING" paragraph, and "natural skin, no dark specks, no crackle texture".

## The work

### 1. Regenerate all six pairs (Codex subscription: `_shared/codex-image.sh --model gpt-6.1-sol --effort high`)

- Rewrite `_common2.txt`: **shirtless**. The face sheet still leads; physique refs from real shirtless studio photos
  (`refs/physique.jpg` = studio-blue-110; add studio-blue-127 and studio-white-23), "lean and shredded, not bulky, the same
  size as the references". Glasses: keep them only if the face reads as him (the film he cuts into has them). Black gym shorts;
  the framing is waist up.
- **A real gym behind him:** racks, a cable machine, dumbbells on a rack, rubber floor, warm gym light, slightly soft so the
  poster reads. The same gym on all six, with the middle band clear for poster, face and vial.
- **A real poster:** a printed gym-style poster on the wall (bold headline with Dan's exact words, a colour band or border, a
  simple icon at most), not a white sheet. Exact spelling, and nothing else on it may read as words (no fake small print).
  Image models misspell: check every letter, regenerate rather than patch.
- Every pair: spec, `gate.py`, a **fresh `frame-reviewer`** per pair and per retry; brief it on poster spelling and no other
  text, vial, fingers, likeness against the face sheet, skin, lean build, gym equipment not warping START to END. No pinching or
  belly framing. Then rebuild the in-place previews (`preview_intros.py`; re-check the chip spots on the new frames) and the page.

### 2. New thigh-injection clips for C

- Search for a doctor or nurse giving an injection into the **front of the thigh** (subcutaneous, insulin syringe preferred),
  and people self-injecting into the **front of the thigh** (GLP-1, insulin, peptide and testosterone SC tutorials, "front thigh
  injection", "anterior thigh subcutaneous injection", Shorts). Rejected by Dan: `HcAsUbiFJyw`, `Pz49hyOla6s`, `4v3kQNFLID8`.
  Seen and not usable: belly only (`LRKzLdwhw2o`, `d1aG2dvI6NU`, `wXjQHAxopzk`, `e9NGueNM03I`, `dSO_761NbzQ`, `xXBDpo1MuK8`),
  pens (`gOxy_K3ifNE`, `GncFgoqRmwo`), unclear site (`Ynv8qapLCmk`).
- Tools: `python3 .claude/skills/reaction-clips/reference/yt.py s "query" 10` and `t ID "thigh" 0` (captions via the android
  client). Downloads: **`~/.cache/absbyai/ytdlp/yt-dlp_macos --js-runtimes node`** (`python3 -m yt_dlp` only gets 360p now).
  Scan at 360p with a timestamped contact sheet, pull only the used seconds in HD (`dl_hd.sh`). Run downloads with `nohup`.
- Placement (Dan's R2 note): a montage of several different thigh injections over "This takes about 10 seconds once you know
  what you are doing" (2.84 to 5.77), then a pinch-and-inject clip over "Inject into your thigh on the outer front part, right
  around the middle" (5.77 to 9.56). Credit each "Video: <channel> / YouTube", small chip lower right (y 1716), the whole clip.
  Colour match to Dan (measure luma). Fill the frame unless there is a reason; write the reason on the page.
- Update `clips/youtube_sources.json`, rebuild `preview_c_open.py`, refresh the page.

### 3. Stop for Dan's approval of frames and clips (page 8821), then

- Motion on the Flow subscription: `veo.py add` per intro (9:16), spawn `flow-veo` in the background, then `clipcheck.py` and a
  fresh `frame-reviewer` per take (`_shared/veo/README.md`). Flow makes 8 s takes: trim to each head.
- Rebuild the six in `round3/` with `batch.py`: a full-frame cover fit for the intro so the **title band is off during the
  intro** and back on the first film frame, the AI chip, the credit chip for C's clips.
- Each short: render, `deliver_watch.sh`, a fresh Sonnet watch judge, `gate.py --format short` (39 rows; every short now has an
  AI clip), then one fresh `ra-reviewer` on all six. One page, each change with timestamps and watch ranges. Copies to
  `Videos to Review/` as `Top 5 Zepbound Tips SFL R4 - short <S> - <title>.mp4`; delete that short's R2 copies. No covers, no upload.

## State at handoff

- Stage 1 frames (tank, grey wall) all passed gate and reviewer, but Dan rejected the look; C clips rejected.
- Spend: $0 this round (Codex subscription images, no paid API).
- **Git:** the main folder could not push (104 ahead / 59 behind, a 9-file hand merge in other sessions' files). Commit 2ba01bb
  (round 3 tooling and lessons) and the earlier b1e35a1, 2a22a47, 016500c, 014d467 are local in the main folder only; the
  separate task "Unstick the main folder so saved work reaches GitHub" is doing that merge. This handoff was pushed from the
  R3 task's worktree. Board entry `SL-06:R3-FRAMES` carries the block note; update it when this round starts.

## Open risks

- Shirtless AI Dan: Codex adds bulk and redraws faces. Check the build against the real shirtless photos and the face sheet.
- Busy gym backgrounds give Veo more to warp in motion: keep equipment soft and declare it as `still` in the spec.
- Poster design invites extra words: forbid small print in the prompt; the reviewer checks there is no other text.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFL R4". This is CONTENT. Read `Handoffs/handoff-20261018-sl06-round4-shirtless-gym-intros-and-better-thigh-clips.md` and `/Volumes/Extreme/_edit_work/sl06/round3/DAN_R3_STAGE1_NOTES.md`, then execute it: regenerate all six AI flex intro frame pairs with me shirtless in a real gym and a real-looking poster (Codex subscription for the images), gate and review them, find better thigh-injection clips for short C (a doctor, or someone injecting the front of the thigh), credit them, and refresh the review page at http://127.0.0.1:8821/ for my approval. After I approve, make the motion on my Google Flow subscription, rebuild the six shorts with the title band off during the intro, run the gates and an independent review, and give me one page. No covers, no upload.
