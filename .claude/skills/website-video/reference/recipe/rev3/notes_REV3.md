# Website conversion video — 16:9 master, REVISION 3

**Rev 2 was reviewed 2026-09-02 (4:13 PM): audio approved, rejected on headroom, one repeated line, and
captions colliding with the lower thirds.** Rev 3 changes exactly those three things, from measurements,
and touches nothing else: same EDL, grade, 4K base, graphics set, card designs, and the **same audio
chain, unchanged**. **$0.00 AI generation spend.** No production code, no deploy, no native-retest trigger.

| | |
|---|---|
| master | `website_video_16x9.mp4` — **3:50.23** (rev 2: 3:51.56), 1920×1080, 29.97 fps, AAC 256k |
| review copy | `REVIEW_540p_website_video.mp4` |
| audio A/B | `AB_his-vs-ours.mp4` — 12 s of Muhammad's ad, then the same window of ours (audio unchanged from rev 2) |
| loudness | −14.5 LUFS · true peak −2.6 dBTP · LRA 2.8 LU · voice centred (L/R +0.9999) · 0 silent seconds |
| script fidelity | 99.0 % re-transcribed off the finished render |
| QC | **all checks PASSED** — the rev-2 suite (14) plus caption clearance in pixels and headroom on the delivered frames; watch pass on the delivered file; contact sheet from exact grabs checked for the light / wide shot / black field / head cut / caption touching a graphic; audio gate PASSED (see §5) |

## 1 — Framing: every crop anchored to his measured head (Dan's main note)

Rev 2's three levels were top-anchored at a fixed y=40 read off one grid frame where his head top sat
at y≈100. Measured across the whole cut (`headtrack.py`, 982 samples at 4/s on the 4K base), his head
top sits at **296–340 px** (median 340) — that frame was not in the video — so every shot carried
**159–261 px of headroom at 1080p** (median 201), worst on TIGHT: "very, very bad crop."

Rev 3: per punch segment, `y0 = (that segment's minimum head top) − 3 % of the crop height`, so the head
top lands ~33 px below the top edge at his tallest instant in every level, and the bottom edge goes as
low as the zoom allows. Widths and zooms are unchanged (WIDE 1.256× / MID 1.45× / TIGHT 1.66×), x stays
centred on him, the light guard and the no-wide-shot assertions still hold.

| | rev 2 (delivered, measured) | rev 3 (delivered, measured) |
|---|---|---|
| head top below the top edge, median | 201 px | 53 px |
| range over every valid frame | 159–261 px | 21–95 px |
| bottom edge of the WIDE level (4K) | 1760 | ≈1960 — shorts and the counter in shot |

The spread above the minimum is his own posture inside a fixed hold (he moves up to ~50 px of 4K in a
10–15 s take); a crop that followed the slouch would cut his head when he stands up. Two passes were
needed: the first put his hair on the edge (7–11 px) in three TIGHT holds because the base-sampled
track under-read his tallest instant; the delivered frames were then measured with the QC's own
detector and merged into the track (`headtrack_refine.py`), moving those anchors up 29–34 px.

## 2 — The repeated line at 0:32

Whisper had stitched *"Now, I've been out of shape, — I've been out of shape, and now at 40"* into one
2.8 s token, which is why the orphan scan passed. An isolated medium.en pass timed both attempts; the
transcript was patched (`tx_patch.py`), the first attempt cut on the base timeline (33.03 → 35.44 s,
both edges in measured pauses, `tight.py MANUAL_CUTS`), and the fluent restart kept. Result: *"Now,
I've been out of shape, and now at 40, I have the most defined abs of my life."* The rest of the cut was
scanned the same way (`repeat_scan.py`): four slow single words and two scripted parallelisms, each
re-transcribed in isolation — no other restart.

**One judgment call to flag:** cutting the repeat shrinks the before card's line to 1.3 s of speech. The
before photo now fades in on the pause after "finally lost.", holds through "I've been out of shape,"
and is out by "and" (never runs into "and now at 40"); Dan is on camera for "and now at 40," (1.1 s);
the four shoot photos start on **"I have the most defined abs"** instead of "now at 40". Before → Dan →
after, never a shared frame (asserted). Say the word if you want the photos back on "now at 40".

## 3 — Captions clear of every graphic (standing rule)

Measured on rev 2: all six lower thirds sat at y 738–924 and the lifted captions inked at 727–806 —
**47–49 px of overlap on every lower-third beat**, and QC only compared captions against full-frame
cards. Rev 3: the lower thirds sit at the bottom (plate 878–1000; with its shadow 858–1044) and lifted
captions ink to 795 (two-line cues grow upward to 668) — **62–73 px of clearance, measured on all 21
cue/graphic pairs**. No caption ink inside or within 20 px of the phone box. Suppression over full-frame
cards unchanged.

## 4 — The two new QC checks (both fail rev 2's file, both pass this one)

- **Caption clearance in pixels** — every cue that overlaps a lower third is rendered alone over green,
  its ink bbox is measured against the lower third's alpha bbox from the graphic's own MOV, and a ≥20 px
  gap is asserted. Rev 2: −47 px. Rev 3: 62 px minimum.
- **Headroom on the delivered frames** — the head detector runs on the finished master every 0.25 s
  wherever Dan is on camera: ≥15 px on every valid frame, within 45 px of the edge in every punch
  segment, median ≤60 px, sanity ceiling 100 px (an anchor that failed reads 150+). Rev 2: 159–261. Rev 3: 21–95, median 53 — the 95 is one slouch inside a 14 s tight hold, the anchor of that hold measured 33.

## 5 — Audio: unchanged, and a note about the gate

`audio3.py` (EQ fitted to Muhammad's ad, expander, no compressor, bed −44 dB, gain + limiter) ran
unchanged on the new picture. **The shared audio gate was replaced by another session this evening**
(`_shared/audio/audio_gate.py`) and gained two rows — early decay of the room and speech spread. On its
first thresholds (≤55 ms, ≥ his −1.5 dB) rev 3 failed both rows at 77 ms / 5.6 dB — and **so did rev 2's
approved file, identically (75 ms / 5.5 dB), because it is the same chain**. The thresholds were revised
the same evening (≤80 ms, ≥ his −3 dB) and the final master **PASSES all eleven rows** (tone 0.88 dB
mean, floor within +0.2–2.5 dB of his, L/R +0.9999, −14.5 LUFS, −2.6 dBTP) and carries the gate's stamp.
For the record: his room decays in 40 ms and ours in 77 — the kitchen doorway. If you ever want this
video drier than what you approved, that is the shoot-audio-standard handoff's dereverb stage, a
separate decision not made here.

## Recipe

`tx_patch.py` → `tight.py` (manual cut) → `hard_splices.py` → `headtrack.py` → `layout.py plan|pip|punch`
→ `headtrack_refine.py` → `layout.py punch|mix` → `audio3.py` (bed −44) → `captions.py` → `deliver.sh`
(`sheet.py`, `qc.py` + `qc_frame.py`, `watch.py`, review copy). `rev3.sh` + `rev3b.sh` are the two
passes as run. Working dir `/Volumes/Extreme/_edit_work/website-video-828/`; rev 2's intermediates and
scripts are in `rev2/`, rev 1's in `rev1/`.
