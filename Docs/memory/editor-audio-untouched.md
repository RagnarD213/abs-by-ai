---
name: editor-audio-untouched
description: "Dan 2026-09-10 — a vertical/cutdown rebuilt from an editor's finished video carries the editor's audio UNTOUCHED by default (no limiter, no mono-sum, no -14 target); our \"+9.9 dB into a limiter\" Zeeshan version was rejected"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: abcaa32a-9420-4f02-8ed3-b5b041b09a14
  modified: 2026-09-10T19:39:47.084Z
---

When a video is rebuilt from an editor's finished cut (Zeeshan, Muhammad, Waleed — `/shortad-from-longform`), the
deliverable carries **the editor's own audio exactly as he exported it** by default: stream-copied into the full
length, and only CUT (4 ms joins) for a cutdown. No limiter, no mono-sum, no loudnorm, no -14 LUFS target. A small
constant lift only when Dan asks for one — the Muhammad Ad 1/Ad 2 verticals he approved (+4.2 dB, loudness range
3.5 -> 2.8 LU, no mono) are its ceiling.

Dan, 2026-09-10, on the Zeeshan Ad 1 vertical (his -23.5 LUFS mix lifted +9.9 dB into a 4x-oversampled limiter,
mono-summed, AAC 320k): *"What the fuck happened to the audio? Zishan's audio sounds much better. This is an awful
mistake which can't happen again. Why do these audio problems keep happening? Use Zishan's audio. This is the audio you
made. There are serious issues with your quality control on the audio. Over and over again, you produce bad audio. We
have to fix this."* ("Zishan" is Wispr for Zeeshan.) The same day he approved the Muhammad Ad 1 vertical (the small lift).

**Why:** every provenance check we had was level-normalised, so it proved the audio came FROM his mix while being blind
to what the lift and limiter did to it (loudness range 5.9 -> 4.1 LU, 21 % of seconds shaved > 1 dB). Our -14 LUFS and
L/R >= 0.98 rows would have FAILED Zeeshan's own mix, so the build bent his audio until it passed them; the damage was
measured, called a "trade-off", and shipped anyway — the exact inversion of [[audio-never-over-strip]].

**How to apply:** `audio_gate.py --reference-mix <his> --verbatim` and `"audio_mode": "verbatim"` in the build's qc.json
— the verbatim rows fail any change to his level, dynamics or stereo image. If an editor's file is too quiet for a feed,
ask the editor for a louder export. Rejected files and his export are corpus entries (`ad1zee-*`, `zeeshan-ad1-16x9`).
See [[gate-the-harm-not-just-the-fix]].
