# HANDOFF: "Why You Should Invest More In Your Health" — v3 revisions

**From:** Claude Code (Fable 5 session, 2026-08-20) · **To:** fresh session (Opus 5 recommended)
**Skill:** `/longform-edit` — READ ITS SKILL.MD FIRST, especially the new
"Junk-footage detection" section (all lessons from v1/v2 of this exact video).

## State

- Deliverable under revision: `Media/longform-raw/absbyai-0803-shoot/invest-health/roughcuts/INVEST_HEALTH_v2.mp4` (53:30) + `INVEST_HEALTH_v2.srt`. Dan reviewed this file; his v3 timestamps refer to it.
- Working dir: `Media/longform-raw/absbyai-0803-shoot/invest-health/` — `C1511.MP4` (local copy of the 69-min source roll), `C1511.whisper.json` (word timestamps), `silences.json`, `edit/` (all scripts), `edit/gfx/` (chips, watermark, soup column, placeholders).
- Pipeline (all in `edit/`, run with `export PATH="$HOME/bin-ff:$PATH"`; ffmpeg 6.0 static symlinked there):
  1. `python3 build_edl.py` → writes `edl.json` (word-snapped ranges + pause capper + zoom alternation). **Run bare, never piped through grep** (a swallowed traceback previously let a stale EDL ride through a full render). After it, re-apply grade+fps keys to edl.json (3-line python at top of the chain command in git history, or copy from below).
  2. `python3 ~/Developer/video-use/helpers/render.py edl.json -o ../roughcuts/CUT_v2_graded.mp4 --no-subtitles` — segment cache: only changed ranges re-extract, BUT zoom state is index-parity, so inserting/removing a range flips `vf` for all later ranges → near-full re-render (~35 min). Batch ALL EDL changes, render once.
  3. `python3 build_gfx.py` then trim title chip end to start+5.2 in `chip_timings.json`.
  4. `python3 make_srt.py ../roughcuts/CUT_v2_graded.mp4` → renames to v-file; **apply subtitle word fixes (below) inside make_srt.py's `join_tokens`/flush path or as a post-pass before writing**.
  5. `python3 composite.py CUT_v2_graded.mp4 INVEST_HEALTH_v3.mp4` — chips + watermark + soup split-screen + 2 placeholders, all SOURCE-time-keyed (survive re-cuts automatically). Add the new overlays (below) to its overlay table the same way.
  6. `python3 qc_v2.py ../roughcuts/INVEST_HEALTH_v3.mp4` — update its SPOTS list to the v3 revision points; **every changed joint must be verified by the transcription section**, plus phrase-level repeat scan + 1fps contact sheets around new joints (skill section, items 3-4).
- Grade (bake into edl.json every rebuild): `curves=all='0/0 0.085/0.012 0.27/0.42 0.55/0.70 0.82/0.94 1/1',eq=saturation=1.08` ; `"fps": "30000/1001"`.

## Dan's v3 revisions (timestamps = v2 file; convert to SOURCE time via edl.json before editing — `build_gfx.py` has the src_to_out mapper, invert it)

1. **Subtitles: "GOPs"→"GLPs" everywhere; the string "GOP" must not appear** (political-restriction risk). Also fix Whisper drug spellings while in there: tersepityde/Terzepetide→Tirzepatide, reditrutide→Retatrutide, osepic→Ozempic, "set down"→Zepbound (check ~2825 src context), "Aura ring"→"Oura Ring", "vitamin Z"→leave (it's a joke? check audio at src 2416 area — actually that's the Zepbound video, ignore). Grep the final SRT for `GOP` and assert zero hits in QC.
2. **6:42 — remove repeated "all kinds of problems" footage.** Source region ~src 513–533: he says "multiple different problems, all kinds of prescription medications, arthritis, joint problems resulting from being overweight." then "There's all kinds of problems that you have to deal with if you don't take care of your health." Cut the second sentence entirely (range `doctor-time.0` ends ~526.85; adjust so the kept audio goes "...resulting from being overweight. So a lot of people think..." — i.e. also drop the retake fragment at 529.28–533.4 that carries "deal with if you don't take care of your health"; re-check words around 529–536 from SOURCE audio first, per skill item 2).
3. **Zoom cuts: raise punch-in from 6% to 10%** — `ZOOM_VF` in build_edl.py → `crop=1728:972:96:0,scale=1920:1080:flags=lanczos`. Dan flagged 8:18 and 32:17 as jump cuts; both joins already alternate zoom (verified) — 6% was just too subtle. After render, frame-compare BOTH sides of those two joins and 3 random others to confirm the punch reads.
4. **Sleep-tracker section (~34:45–35:50 of v2; src 2664–2779):**
   a. **Remove the doubled Oura introduction** ("32:52" note — Dan confirmed it's this section). Transcribe src 2664–2740, find the redundancy (likely "the Aura ring, my preferred option" re-introducing after "the Aura ring is the best and most accurate sleep tracker"), cut the smaller redundant span, verify joint by re-transcription.
   b. **Insert Oura Ring + Whoop product graphics at his side as he mentions each** ("32:55" note). Dan chose **official product/press photos from the web** (standard for review content). Get a clean Oura Ring 4 press render + Whoop 4.0/5.0 band press image, cut out/pad onto transparent PNG, show each ~4–6 s beside him (viewer-left, over the door area, ~500 px tall, subtle 0.35 s fades — reuse composite.py's img_fade overlay type). Oura when he says "Aura ring" (~src 2668), Whoop at "the whoop" (~src 2716).
5. **39:54 supplements joint (src ~3056–3063): recut + graphic (Dan chose both).**
   Recut: drop "if you're middle class." → keep "...final thing you need to be investing in." + "Supplements." (end range at word "in" ~3058.21+pad, resume at "Supplements." ~3062.49−0.12; the existing `supp-intro` ranges and stretched-word "you're" residue are replaced by this). Verify by re-transcription. Graphic: supplement-bottles visual (use `Media/ad-assets/` supplement imagery if suitable, else a J2-framed photo card) overlaying ~2 s across the joint.
6. **49:59 — insert a short Bryan Johnson clip** (src ~3798+, where he introduces the channel). Dan chose: my pick — a few seconds of Blueprint daily-routine montage b-roll. `yt-dlp` a Bryan Johnson (channel: @BryanJohnson) video, pick ≤8 s of visually-distinct routine b-roll, insert as a **video overlay window** (like the soup insert in composite.py — full-frame or large PiP over Dan while his audio continues), with a persistent small attribution "Bryan Johnson / YouTube" (Manrope, matching watermark style). Keep it ≤8 s, transformative-commentary context = fair use posture. `yt-dlp` may need `pip3 install --user yt-dlp`.

## QC gate for v3 (all must pass before delivery)

- Duration ≈ plan; loudness −14±1 LUFS; every CHANGED joint re-transcribed clean; `grep -c GOP` on SRT = 0; phrase-repeat shingle scan over final transcript (skill item 3) with each hit inspected; contact sheets at new joints; chips/watermark/inserts frame checks (mid-window + gaps); zoom-contrast frame pairs at 8:18/32:17 equivalents.
- Deliver: `INVEST_HEALTH_v3.mp4` + `INVEST_HEALTH_v3.srt`, SendUserFile the SRT + evidence frames, update `AI_COORDINATION.md`, commit+push skill/reference script changes (media stays out of git — `git check-ignore` first).

## Open decisions (do NOT execute without Dan)

- Cut-down variants: conservative ~40 min + aggressive <30 min EDLs — recommended sequence is variants BEFORE b-roll/AI-clip dressing; aggressive as primary upload. Dan has not yet said go.
- No baked-in speed-up (recommended against; offer 1.0/1.1/1.2 sample if he asks again).
- Soup insert sits viewer-left; flip if Dan says he meant screen-right.

## Risks

- Zoom parity: any range-count change re-renders ~everything (~35 min) — batch all cuts, render once.
- Whisper traps: read the skill's junk-detection + Whisper-timestamp sections before touching any cut point. Never cut inside zero-length word clusters; re-transcribe stretched words from source.
- Do not touch `C1511M01.XML`/source media; Seagate drive not needed (local copy exists).
- AI spend: $0 expected (all local; yt-dlp free).
