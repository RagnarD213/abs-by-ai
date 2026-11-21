---
name: muhammad-trial-edit-analysis
description: "Why Muhammad A's Upwork trial edit beat our pipeline's cut, and the 2026-08-21 rebuild that closed the gap — feeds the editing-stack decision"
metadata: 
  node_type: memory
  type: project
  originSessionId: deff5058-6825-4c67-8076-fed760cea4ba
  modified: 2026-08-21T21:51:54.371Z
---

Dan sent 4 Upwork editors a paid trial (ad-1 footage, 8/14 shoot) on 2026-08-20. Muhammad A
(Pakistan) delivered a 61s edit Dan rated clearly above our /ad-edit rev-4: "sounds better, looks
better, graphics are better." Measured on 2026-08-21, the gap is FIVE specific things, all
replicable in our PIL/ffmpeg pipeline:

1. **Airtight pacing** — zero pauses ≥0.25s in the whole video (206 wpm density at true 1.0x —
   word-level timing matches the raw roll exactly, no speed-up). Our cuts keep Dan's natural pauses.
2. **Music bed** — upbeat track at ~-20dB RMS under the voice, full length. Our ads/videos have none.
3. **Transition SFX** — whoosh/pop on every graphic entrance.
4. **Animated graphics** (Premiere MOGRT-template look): pastel-cyan explainer theme, navy
   geometric sans, rounded cards + soft shadows, progressive bullet builds, lower-third label chips
   ("The Problem" + red strip), full-screen title cards, dashed-arrow connectors, and an animated
   highlight box drawn around the physical door photo synced to "THIS picture got me abs."
   Our graphics are static PNG overlays.
5. **Brighter grade** — lifted shadows (talking-head luma 67 vs our 55).

Tooling: encoder tag = Mainconcept → Adobe Premiere Pro; speed almost certainly from Premiere
text-based editing (auto pause delete) + a template pack + stock music. No burned captions at all.

His flaws: stray backtick typo in a bullet, a black "Broll assets folder" placeholder card left in,
and side-by-side before/after cards — banned in our PAID ads (fine for organic YouTube; the trial
was cut as a YouTube episode).

Feeds the dashboard task "Decide the video-editing stack" ([[muhammad-a-hired]] if Dan hires him).
Related: [[bias-toward-action]].

**PARTLY CLOSED 2026-08-21 (same day) — the five points below were, the real gap was not. See the 2026-09-09 addendum.** All five were rebuilt into the pipeline and delivered as a 60s
head-to-head sample (`EDITED ADS 8-20-26/ad1-how-ai-got-me-abs/SAMPLE_modern-edit-60s_*`, plus a
side-by-side). $0.00 spend. The reusable output is `.claude/skills/ad-edit/reference/motionlib.py`
(animated graphics) and `sfxlib.py` (synthesised whooshes/pops — chosen over downloads so there is
no per-asset licence to track), worked example in `reference/modern60/`. Two honest gaps remain: he
is 4.3s shorter on the same words (his extra cuts are inside words; ours only in measured silence)
and his grade is ~6 luma brighter. **Music is the open question, not the technique** — the sample
uses a CC BY 4.0 track needing a description credit; a paid library is the fix if this becomes house
style. Dan's verdict on the sample decides the stack; nothing is locked until he watches it.

**ADDENDUM 2026-09-09 — the five points above were NOT the whole gap, and one of them was wrong.**
Measured on the Ad 2 vertical (`Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/notes-vertical-v2.md`,
independent audit 2026-09-03): **he cuts the PICTURE 1–15 frames away from the audio splice, on a
pose-matched frame (a J/L cut), so his joins read as continuity and ours as jump cuts.** `piccuts.py`
in that recipe folder recovers his picture-cut frame at every talk splice (22 of 33 moved by −15…+10
frames) — built once, never promoted out of that folder.

The superseded belief: that he hides every trim under a framing change across the splice. He does not —
**43 of his 72 talk-to-talk splices exceed 4× his own median frame diff; ours 32.** The real defect was
that 100 % of our attempt-1 talk ran at ONE fixed crop, which is what makes a tripod shot read as a
webcam recording. Target: ≥25–39 % of talk inside a push.

Dan rejected the whole pipeline's output on 2026-09-09 ("far below the quality the human editors have
made"). The audit behind the fix plan — 33 QC scripts with one shared, the style gate in 1 of 6 skills,
the watch pass mandatory in 1 of 6 — is in
`Handoffs/handoff-20260909-video-quality-to-muhammad-standard.md`.
Related: [[audio-never-over-strip]], [[framing-standard-hair-anchored]].

**ADDENDUM 2026-09-24: Dan's eye overruled the pose-match theory.** VQC-C built the shared head-matched
picture cut (`_shared/cut/piccuts.py`) and showed Dan one Ad 1 join, cut on the audio vs on the frame where
his head matches (48 px vs 6 px head jump). His verdict on both: *"They both look bad. I wouldn't use either
of these cuts. They both look like jump cuts."* A matched frame does not hide a same-framing cut. What passed
his eye is the kit's framing STEP (instant punch-in/pull-out) on every bare talk cut, or an insert over it
(blind tie with Muhammad, 2026-09-18). Never pitch frame choice alone as the jump-cut fix again, and never
drop the step because a frame matched. Test a cut technique on Dan with the step in place, not bare.
