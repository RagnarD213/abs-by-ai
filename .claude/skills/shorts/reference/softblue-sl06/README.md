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
- **Pickups now come from the studio lav, not the desk mic (Dan, 2026-10-13; VIDEO-RULES, "Pickups are recorded on the studio
  set").** The desk recording is a timing placeholder: build pictures, captions and timing against it, label it on the page,
  then swap in the lav take. `pickup.py` works the same on a lav WAV: `pick_lav.py` on the shoot clip, pull the lav to a mono
  48 kHz WAV, `asr`, pick the last clean take, `fit ... _lav` (expect a small correction), `make`. Every head changes length,
  so re-run audio, words, plan, gfx and render for each pickup short. The notes below about the desk recorder apply to placeholders.
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

## Round 2 (2026-10-16): lav pickups laid in, all six built, gated, judged, reviewed twice

```
render_queue.sh S..      renders one at a time behind buildcap.wait (the 2-build cap counts other sessions; the machine sat at load 200+)
deliver_watch.sh S       deliver.py copy (copy, audio gate --verbatim, 540p, Whisper diff, gate plan) + watch.py into a CLEARED watch folder
gate_queue.sh S..        the delivery gate once the watch judge is recorded (watch_pass.json "inspected"), one gate at a time
make_joins.py            6 s "pickup into film" clips per short + D's two pickup treatments (fitted EQ vs the film's chain EQ) for the page
listen_joins.py          blind Gemini listen of the pickup joins with two film-internal joins as controls (about $0.05)
page_r2.py + notes_r2.py the review page: six finished shorts in one floating player, joins, voice A/B, AI frames, every item as a still
                         that plays inside the finished short from 3 s before it (media seek, no extra clips), checks, one reply box
```

What round 2 taught (every item was a reviewer or judge finding first):
- **Today's rule: graphic copy is title case, never uppercased in code** (VIDEO-RULES 2026-10-16). `_shared/hyperframes/vertical.py`
  takes `topic_case="preserve"`; scenes.py labels and the title band eyebrow are written in title case. Emphasis caps on about one bar in six.
- **Brand names stay out of on-screen graphics until Dan rules** (VIDEO-RULES 2026-09-30): the title band defaults to "GLP-1 Tips" with
  "Zepbound Tips" as the option on the page. A reviewer will block a Zepbound band otherwise.
- **Check the B-roll share at plan time** (SL-07 lesson): C and E were 16-17% and would have failed `style:coverage`.
- **Stock syringes: look at the needle.** Most Pexels "insulin" footage (the green-background series 8670928/8670930) uses long
  hypodermic needles; the blue-background / white-sweater series (6824057, 6824121, 6824226) is real insulin syringes. A clinician
  injecting someone's arm contradicts a self-injection how-to. B0329's ampoules read "COVID-19 vaccine" at full size: never use it
  for a drug short. B0352's barrel is a 1-4 ml scale, not insulin units (judges call it the weakest choice).
- **An old AI clip is checked like a new one:** the film's A0058 split screen changes both bodies inside one take, which fails the
  2026-10-13 time-jump rule; it was dropped (Dan on camera). A0137 passes but has a smeared hand in its last second: trim before it.
- **Captions end on picture cuts:** `cmd_cues` (ported from SL-07) breaks a cue at every picture cut that falls between two words
  (size steps included) and never carries a sentence's last word into the next cue; `Short.__init__` ends a cue on a cut inside its
  last 10 frames. A cut that lands mid-word still lets the caption hang: move the cut into the next gap instead (E 46.85, C 36.62).
- **A rollout needs a card as wide as the travel** (`fit="span"`, full source height); a square cut his head off at full extension.
- **A phone recording's camera-dismiss transition shows as a black block** sliding over the screen: start the window after it.
- **Watch folders keep stale strips from earlier renders**; a judge then skips or mixes images and the gate refuses the log.
  `deliver_watch.sh` clears the folder first. A judge once returned an empty findings.json: have it read the file back.
- **A gate process can be killed by another session's cleanup** (exit 143); re-run it.
- **The pickup's last word on D reads "Zep out" to Whisper on the raw lav too**: how it was said, not the cut. Report, do not chase.


## Round 3 stage 1 (2026-10-18): AI flex intros as frames, credited YouTube clips (`round3/`)

```
preview_intros.py S..    START then END still (AI-GENERATED chip) over the short's real opening line, then the round-2 film (band returns)
preview_c_open.py        C's new opening: intro stills, two-clip thigh-injection montage, Karli Sine card, credits lower right, C's own captions
page_r3a.py              the stage-1 page (frame pairs + C clips); refuses pairs without gate + reviewer PASS (served on 8821)
dl_low.sh / dl_hd.sh     YouTube: scan at 360p first, then download only the seconds used in HD
```

- **YouTube HD needs the standalone yt-dlp (2026-10-18).** `python3 -m yt_dlp` on this Mac is stuck at 2025.10.14 (Python 3.9) and
  YouTube now answers "The page needs to be reloaded" on the web clients; the android client still gives captions and 360p only.
  Use the official build `~/.cache/absbyai/ytdlp/yt-dlp_macos --js-runtimes node` (checksum-verified from the GitHub release):
  1080p and 4K, `--download-sections "*m:ss-m:ss"` works. Scan candidates at 360p with a timestamped contact sheet, then pull only the
  used seconds in HD.
- **AI Dan likeness:** one real face reference gave a generic man with glasses. A four-face sheet (two film stills in his glasses,
  two smiling studio close-ups) plus the line "LIKENESS IS THE MOST IMPORTANT THING ... broad face, high cheekbones, wide jaw" read as
  him. Add "natural skin, no dark specks, no crackle texture": a reviewer failed one pair on invented freckles at 2 to 3x his density.
- **Frame specs for a waist-up subject:** set `person.reach: false` (no limb straightens; the legs are off-frame and MediaPipe guesses
  them). Mark prop boxes on a gridded zoom of the prop itself: two reviewers found the vial boxes sat on the knuckles.
- **Real thigh injections with a needle are rare on YouTube**: Zepbound vial tutorials inject the belly, thigh videos use the pen.
  Usable: Karli Sine `HcAsUbiFJyw` 2:28.6 (pinch and insulin syringe, vertical, her captions on her chest: card on the thigh),
  Nurse Scott `Pz49hyOla6s` 6:20, Clinical Skills Training `4v3kQNFLID8` 0:42.6 (square: a fill crop shows only the gown).

## Round 4 stage 1 (2026-10-18): shirtless gym intros, front-thigh clips (`round4/`)

```
prompts/gym_plate.txt   an empty-gym plate, generated once and given to every START as ref3 (same gym on all six)
prompts/_common3.txt    shirtless, physique sheet as ref2, printed navy/yellow poster, "lit brighter than the room"
deskin.py, finalize.py  raw Codex PNG -> remove the wormy skin texture (1-4 px band, colour skin mask) -> 1080x1920 JPEG
lock_tight.py           lockstill variant: inside --tight boxes keep END only on a skin mask (yellow-safe), so a poster
                        border is not dragged by the grown person mask; --keep boxes for a moved fist
page_r4a.py, preview_c_open.py, dl_hd4.sh   the R4 page, C's opening with three fill-frame credited clips, the HD pulls
```

- **Codex skin texture:** shirtless frames came back with a wormy, crackled pattern on chest and face at 1:1. A reviewer had failed
  R3 B on specks. Smoothing only the 1-4 px band on a colour skin mask (`deskin.py`) fixed it; apply the same to START and END.
- **Codex END edits barely move a hand.** Three prompt wordings ("touch the poster", "rise a hand's length", "up by 8 %") moved the
  pointing hand 30 to 110 px. When the move is too small, keep the good frame as END and ask for a START with the hand LOWERED
  (an easier edit), then lock END's background to the new START (`lock_tight.py`). A reviewer failed F until that was done.
- **Real gym depth:** the poster sits on a wall behind him, so "fingertip touches the poster" is not physical; reviewers accept
  the finger in front of the corner. Prompt the motion as "points at the poster".
- **lockstill traps:** a grown person mask keeps END's drifted poster border (a 2-3 px step); a START fingertip outside the
  segmentation is copied back as a floating blob. Both were caught only by the fresh reviewer.
- **Thigh clips that exist:** University of Iowa Health Care `e0wDPZ0D9Wk` 6:00.9 (gloved nurse, front thigh), Seattle Children's
  `7TP0rTlQVao` 6:59.5 (self, pinch, front thigh, logo bug bottom right), SynergenX `FeweDb3Xfxg` 1:39.5 (pinch and inject,
  front thigh, 4K). All three fill a 9:16 frame on the needle. Search notes and rejects: `round3/yt/sheets4/`.

## Round 5 (2026-10-20): A shorts, leaner D, Seattle-only C opening, Flow audio failures (`round5/`)

- **"Slightly less muscular" needs strong words.** A plain "slightly leaner" edit changed nothing measurable; "15 to 20 % less muscle,
  narrower lats, no V-taper wings" cut chest width 23 %. Measure with a person mask (width at chest and waist rows) against the
  approved bodies before review. The END edit then has to say "arms must NOT get bigger": a "squeeze harder" END re-added 8 %.
- **Shorts height:** "pull the shorts up" overshoots to the navel; ask for "two to three finger-widths below the navel" and compare
  the navel-to-band gap / nipple-to-navel ratio with the approved frames (B to F: 0.21 to 0.56).
- **Gate phantom legs:** on waist-up frames MediaPipe guesses the legs, and one START's guess (thigh 313, shin 518 px) failed every
  END on `person:bones`. A different START candidate guessed sanely. Where the lower body does not move, building END as the
  passed END above the ribs plus START below (feathered) is physically right; tell the reviewer exactly how it was made.
- **Flow "Audio generation failed":** 8 of 8 Veo 3.1 Fast frames-mode takes failed on 2026-10-20 (two prompt styles, credits refunded).
  Flow's fix is its "Return silent videos" project setting; the agent's permission guard blocks changing it, so it needs Dan.

### Round 5 motion (2026-10-20): Veo intros, what it took (`round5/`)

```
fix_take.py    repair a locked-camera Veo take: static boxes (D's calendar) copied from the approved frame where no person
               covers them; vial labels found by template match each frame and replaced by the approved frame's label
mouth_hold.py  hold one smile: from frame N the mouth of a clean frame is pasted, tracked by nose (+ chin with --anchor2) and
               clipped to the face outline (--skinclip); kills Veo's talking mouth under the voiceover
batch.py       COVERS fit="full" (intro over the title band), ai=(x, y, u, anchor), credit="Video: ... / YouTube" chip lower right
```

- **Veo frames mode stretches the move over 8 s** and wanders between: with START and END, Veo pointed the hand at his own
  chest for 7 s and reached END in the last 0.5 s. We use 2.5 to 4.6 s, so START+END takes were useless for these intros.
- **A hand pointing up near the body reads to Veo as "pointing at himself"** in every wording (6 tries). Starting from the END
  frame (fingertip already on the poster) holds it. The arm reaching back (E) worked from START too.
- **Veo moves the lips as if talking**, even with "does not talk" (mentioning speech may trigger it). Positive wording ("lips
  pressed together, same closed-mouth smile") helped once (F); mouth_hold.py fixes the rest. The paid API's negative prompt
  ("talking, lip movement, pointing at his own chest, looking down") gave clean A and B takes first time ($0.60 each, 6 s).
- **Veo garbles small text** (vial labels every take, a backwards R in "FRI"): repair from the approved frame, never ship.
- **Flow traps:** the aspect selector resets to 16:9 after a page reload (100 credits lost); "Return silent videos" is a project
  setting only Dan can switch (audio-step failures 8/8 without it); Flow refused one B take as "prominent people".
- **The shared render queue gates every ffmpeg call** (the bin/ffmpeg shim): even a reviewer's stamp write waited 69 min at
  load 150. Budget hours, not minutes, on a busy day.
