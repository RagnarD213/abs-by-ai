# `softblue-sl06/`: Soft Blue shorts from a 4K long-form, with recorded pickups (SL-06 Top 5 Zepbound Tips, 2026-10-12)

The SL-03 batch renderer (`../softblue-sl03/`) extended for three things it did not have: a recorded pickup at the head of
a short, stock / library / AI clips as covers (SL-03's covers were raw-roll B-roll), and film graphics rebuilt for the
vertical picture area. Work folder: `/Volumes/Extreme/_edit_work/sl06/` (run from there; these are copies kept in git).
Start from this folder for the next batch cut from one of our own long-forms that has a `timeline.json` with `blocks`.

```
snap.py T..               silences around a film time on the film's dry voice (cut points)
pickup.py asr RAW.wav     Whisper word times of Dan's recording
pickup.py fit RAW.wav '[[t0,t1],..]' _tag     tone EQ fitted toward the FILM's voice (voice_chain.fit_eq), per mic distance
pickup.py make X RAW.wav T0 T1 _tag           one take -> pickups/X.wav (EQ, level matched to the next film line, film bed under it)
batch.py audio|words|plan|track|plan|gfx|proof|render S..     as SL-03; plan runs twice (track needs the first shot table)
export_stills.py S..      one still per crop level, clip, rebuilt graphic and bar -> round1/stills + items_S.json
page_r1.py                the round-1 page from items_S.json + notes_r1.py (review_server.py PORT round1)
```

What is new in `batch.py` and `plans.py`:
- `PICKUP[S]`: the short's timeline starts `head(S)` seconds late; the pickup is piece 0 of `TEXT` and is CTC-aligned like any
  piece; `joins` includes the pickup join; a cover with `b="head"` ends exactly on it. A frame inside the head with no cover
  fails the plan.
- `COVERS[S]` are dicts. A clip: `src, t` (in-point), `fx / fy` (where the fill crop sits, 0..1), `fit` (`fill` default,
  `square`, `whole`, `stack2` = a side-by-side split clip rebuilt one half over the other), `rot=180`, `eq` (colour correction),
  `ai=(x, y)` (AI-GENERATED chip, drawn with `softblue.disclosure`). A graphic: `scene=<name in scenes.py>`. The phone demo:
  `phone=True` (the approved phone-beside-Dan layout; the camera keeps running beside it).
- Talking windows are cut from the 4K roll (`cam()` grades only the strip of columns the short uses), so a 724 window is a
  downscale, not a 1.49x upscale. Window maths stays in 1920-space.
- A shot break at every true audio join, even inside one film block (SL-03 keyed shots on raw minus film offset only, which
  hides a jump between two pieces of the same block). Talking shots default to alternating full / mid at every adjacent join.
- `bar_times` ends a bar 0.25 s before the next one starts; a one-line bar is allowed.
- `scenes.py`: the film's chart and ramp redrawn inside canvas y 310..1380, so captions (from y 1412) never sit on a graphic.
  Narrow glass columns use `_bar`, not `softblue.glass` (its specular line overhangs a column).

What round 1 learned:
- **Never record with `ffmpeg -f avfoundation`. Use `~/.cache/absbyai/rec_mic OUT_DIR MAX_SECONDS 30`** (source
  `_shared/audio/rec_mic.swift`). The ffmpeg capture dropped 11.7 % of the audio on SL-06's pickups (105.95 s of samples in a
  120 s window, a 512-sample block gone about every 90 ms). Whisper transcribed it, the EQ fit converged and the audio gate
  passed, so a finished short went to Dan with a faulty opening. **Check every take before using it:** samples against wall
  time within 2 %, and second-difference spikes whose spacings are multiples of 512 samples (more than two in a take = dropped
  blocks). All five SL-06 takes from 10-12 failed that check after the fact and were re-recorded.
- **Never open a recording window blind.** The first 4-minute window caught Dan dictating notes on another video. Show the
  lines, wait for his "go", then record 2 minutes. `pgrep -f` on the ffmpeg command line matches the waiting shell itself:
  wait on the background task, not on a pgrep loop.
- **Dan rewrites a pickup while he records it.** B went through four wordings; the last complete take is the line. Read the
  whole transcript before choosing, and update `PICKUP` and `TEXT` to what he said.
- **He moves relative to the mic between lines.** SL-06: the first half 8 dB quieter and roomier than the second. Fit the EQ
  per distance group (`fit ... _far`, `_close`), and tell him which pickups are the roomier ones.
- **A take that hits 0 dBFS is out** even when it is the last one (D take 3, 137 clipped samples).
- The audio gate has no key for a head span. The verbatim reference (`his_mix.wav`) is the pickup plus the film's cut, so the
  film seconds are proven untouched and the pickup seconds are reported from `pickups/X.report.json` (tone error, level, room).
- **The film's 3A list card does not fit under the title band.** With five items its top reaches y 994 and the lifted captions
  land on his mouth. Steps go one at a time in the key-point bar (`STEP 1 OF 5`); the card still was shown as option B.
- **Check the film's own stock against rules newer than the film** (the phone-gazing clip, a belly-framed pen injection, a dark
  syringe close-up). Each got a replacement or a stay-on-camera.
- Whisper (small and medium) on the cut audio, diffed against `TEXT`, catches clipped edge words and subtitle mis-hearings
  (the film's "Again," that he never says).
- `review_server.py PORT DIR` run twice within seconds can fail at `launchctl bootstrap` and leave the page down. Run it once
  after the last page build, then curl the page and a byte range.

Not done yet (round 2 of SL-06 does it): `deliver.py` for this batch (gate plan, watch pass, 540p, stamps), AI clip motion
covers, and a `declare.json` for the gate rows that measure Dan's approved layout.
