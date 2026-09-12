---
name: website-video
description: Build a WEBSITE conversion video for absbyai.com — the trust video a visitor watches on the post-lock-in analysis page or the /start landing page right before they buy — from Dan's teleprompter shoot footage into a finished, gated 16:9 master, in ONE shot. Use this whenever Dan asks for a website video, a conversion video, a "video for the analysis page", a VSL / landing-page video, the "post-generation video", a re-cut or revision of the website video, or any video whose home is a page on absbyai.com rather than YouTube or an ad platform — even if he doesn't say "/website-video". It locks in the audio that sounds like Muhammad's, the hair-anchored framing, the slow trustworthy pacing, real app screens beside Dan, and AI clips re-rendered until perfect, and it QCs harder than any other video skill. For paid ads use /ad-edit; for YouTube content use /longform-edit; for Shorts use /shorts.
---

# Website video: the last thing a visitor watches before they pay

## Standing rule — label Dan's REAL pictures (Dan, 2026-09-11)

- **A before and after picture are the SAME PERSON** (Dan, 2026-09-12: *"don't mix before-and-after pictures… That doesn't really make sense if you change the person."*). Never pair one person's before with another's after — in an app recording, a result screen, a card or a thumbnail. If that person's after does not exist, generate it for THEM through the live product (a real generation, never a composite) or change the before so the pair matches. ⚠ The only real app recording in the asset library uploads a man who is NOT Dan, so every phone demo cut from it inherits this.
- **Dan's REAL after pictures carry a burned label: "Real picture of me — not AI-generated"** (Dan, 2026-09-11: viewers were taking his real photos for AI). Every real photo-shoot or studio picture of Dan shown as a result gets it for its full duration, in the same chip style as the AI label. AI images of Dan keep "AI-GENERATED". The two labels are mutually exclusive: every picture of Dan's physique carries exactly one of them.
- ⚠ **LABEL PLACEMENT — NEVER OVER HIS FACE AND NEVER OVER HIS ABS** (Dan, 2026-09-12, on the Ad 2 square: *"the label will not block my face or my abs… put it above my head, to the side, or somewhere that it doesn't block my face and my abs in all of these after pictures"*). This REPLACES the old "low on the frame, at the shorts/waistline" rule, which is what put the chip across his lower abs. Put it **above his head, off to one side, or anywhere in the frame his body does not occupy** — still inside the safe area, still large enough to read, still clear of the caption band. **The picture exists to show the physique; a label over the abs defeats the picture.** Choose the position by MEASURING him on the RENDERED frame (person mask → the bounding box of head + torso, then place the chip in the largest clear band), never at a fixed y — every photo frames him differently. If nothing is clear enough, shrink the chip or move it to a corner before you put it on him. Applies to BOTH labels on any picture of Dan.
  This applies in every aspect ratio and in every skill that puts a picture of Dan on screen (ads, longforms, shorts, website video, verticals). First applied on the Ad 5 vertical revisions (`Handoffs/handoff-20260911-ad5-vertical-revisions.md`).

**Built 2026-09-09 from six revisions of the first website conversion video** (rev 1 rejected on audio, framing and
graphics; rev 2 on headroom, a repeated line and caption collisions; rev 3 on hair cut off in every hold; rev 4 on
two AI-clip tails and a card; rev 5 on audio room, a skin patch, an unnatural clip, a lower third and chicken; rev 6
approved: *"you nailed it, this is perfect"*). Every rule here is one of those rejections turned into a measurement
or a gate. The goal of this skill is that the **first** delivery is the rev-6 one.

Why this video is different from an ad or a content cut: it plays to someone who has already uploaded their photo
and seen their goal image, and is deciding whether to trust us with $19.99. **Trust is the brief.** Nothing flashy,
no fast cuts, no hype graphics, no whooshes — a calm, well-lit, honest three-and-a-half minutes where Dan looks and
sounds like the most credible person they have met today. That is why the audio must sound like Muhammad's ad,
why the crops must never touch his hair, why every app screen must be real, and why an AI clip that reads as AI is
worse than no clip.

**Effort profile (Dan, 2026-09-09):** slower cuts than content or ads; **more** money and attempts on AI clips than
any other skill — regenerate until the clip is perfect, don't trim around a flaw; and the most thorough QC we run on
anything. Budget: the $25/session standing cap applies; a website video that needs $15 of clips is normal.

## Read first, in this order

1. `reference/REVIEW_HISTORY.md` — what Dan rejected in each of the six rounds and the exact words. Ten minutes that
   save six revisions.
2. `reference/AUDIO_STANDARD.md` — the chain, the numbers, and the two things that are NOT levers.
3. `reference/AI_CLIPS.md` — prompting, the acceptance checklist per clip, and the regenerate-not-trim policy.
4. `reference/RUNBOOK.md` — every stage with the exact command, in order, with what to look at before moving on.
5. `reference/LESSONS.md` — lessons 73–122 verbatim (shared numbering with /ad-edit), when a stage needs the why.

The pipeline itself is `reference/recipe/` (one copy, owned here; /ad-edit points at it). Shared modules:
`.claude/skills/_shared/audio/` (lav pick, chain, gate, stamp), `.claude/skills/_shared/motionlib.py` (graphics).
Everything not covered here — cut placement, Whisper, ffmpeg traps, the external drive — is /longform-edit, and the
ad graphics/caption vocabulary is /ad-edit; do not re-derive either.

## Inputs

- **Script:** the teleprompter script Dan read (a Google Doc). Ground truth for the cut; his spoken corrections win.
- **Footage:** the shoot rolls on `/Volumes/Extreme/` — 4K, and on the 8/28 kitchen set S-Log3/S-Gamut3.Cine with four
  mono audio tracks (lav measured per file by `pick_lav.py`, never a channel number). A new set needs `make_lut.py`
  re-fitted and the two framing levels re-measured (rule kept, numbers re-derived — see Framing).
- **Reference audio:** Muhammad's `this picture got me abs | muhammad | 16x9.mp4`, pinned by fingerprint in
  `_shared/audio/reference/`. The gate measures every delivery against it.
- **Product screens:** captured from the REAL app on a local fixture server, never a real login (Runbook stage 5).
- **Dan's real photos** for "how I look today" (Muhammad's four shoot photos), his before photo, his goal image.

## The five locks

### 1. Audio — sounds like Muhammad's, measured, every time

`_shared/audio` is the standard; this skill adds the one thing rev 5 was missing and forbids the thing rev 1 did.

- Lav only, mono, centred (`pick_lav.py` → `audio_source.json`). Never `-ac 1`, never a stacked `pan`.
- **Dereverb with the parameters Dan approved by ear on 2026-09-09** (alpha 0.30, d1 22, d2 70 ms, floor −10 dB,
  smooth 0.45 — the `_shared/audio` defaults). The strong setting (alpha .62 / floor −24) is what he called
  "underwater"; it is not a dial to turn when the room reads high. Room target: ≤ 50 ms (his 40; rev 6 measured 45).
- The rev-2 fitted EQ (`reference/recipe/audio3_rev2chain.py`, the curve he approved: "you got it nailed"), the
  downward expander as approved, **no compressor**, bed at −44 dB (= 34 dB under the voice) or none, measured gain +
  `alimiter` to −14 LUFS / −2.5 dBTP. **Never `loudnorm`** (it went dynamic on rev 1 and swung 8 dB second to second).
- **Two things are NOT levers, measured:** the expander does not change speech spread (default / soft / off all read
  6.0 dB — the spread is set by the gain the limiter needs to reach −14 from a −23 LUFS premix); and EQ does not move
  voice-over-floor (it scales voice and floor together). Don't spend a revision on either.
- Gate on the **delivered file** with `audio_gate.py`, all rows including the damage row (flux / HF swirl ≤ his
  ×1.10); stamp; A/B clip with every review copy; **re-transcribe the finished mix** (fidelity ≥ 99 %, an eaten
  fricative shows there, not in a spot check). Entry point: `audio4.py` (Runbook stage 7).

### 2. Framing — anchored to the measured top of his hair, never the frame

The standard Dan locked on rev 4 ("lock that in and crop all the videos like this going forward"):

- Two levels only, **NEAR** (hair → belly button) and **FAR** (hair → shorts line, counter barely visible), plus
  **PIP** (FAR geometry with Dan pushed right so a phone sits beside him). No wide level exists; the studio light
  never enters a crop. On the 8/28 set: NEAR 2076×1168, FAR/PIP 2630×1480 of the 4K frame; re-measure for a new set.
- Per hold, `y0 = (that hold's minimum hair top over BOTH tracks) − 4 % of the crop height` → hair ~43 px below the
  edge at his tallest instant. The hair top comes from `hairdet.py` (climbs from the skin through the dark hair band
  to the door's per-column luma; short climbs are misses and are discarded because they read LOW). Hairline is not
  hair — rev 3 cut the hair in 23 of 26 holds with a detector that "looked right" on small tiles.
- The loop is **plan → render → refine on the delivered frames → re-render once** (`hairtrack_refine.py`); anchors
  can only move up, so it converges in one pass. Rev 6 moved two holds (14 px and 2 px in 4K) on that pass.
- `hairgate.py` on the delivered file: hair ≥ 20 px on every valid frame, per hold 30–70 px, median ≤ 75, AND the
  detector-free test (no hair-coloured pixels in the top 12 rows of the head band on ANY frame). Prove any new gate on
  the known-bad rev-3 file first.
- **Validate by eye at native scale before rendering**: `pv/hairtrack_proof.jpg` (tallest + median frames, 4K crops,
  grid). A proof sheet of 480-px tiles is how rev 3 shipped.
- Any pass that re-encodes the picture stays in the video's own colour space: an RGB round trip darkened every pixel
  by 1.4 levels on rev 6 and tipped the hair gate's border rows (`tanpass.py` shows the YUV pattern).

### 3. Pacing and graphics — calm, sparse, real

- Trust cut: holds ≥ 9 s, pauses shortened to ~0.30 s (not 0.16), punch boundaries land on splices, NEAR/FAR alternate
  across every visible join, the hook opens on FAR, hardest splices covered first inside a 3.5 s floor. Nothing sits
  unchanged > 25 s. No SFX, no whooshes, cards fade 0.5 s. Median hold on rev 6: 3.75 s; longest 9.9 s.
- **Graphics sparingly** (Dan: "much more sparingly"). What is allowed: lower thirds at the bottom of the frame
  (`lower_third_bar(bottom=1000)`), full-frame photo cards that fill the frame (before → Dan → after, never together),
  the trial / price / CTA cards, and **phone PiPs beside Dan** (433×820 in `PIP_BOX`, Dan at 65 %) for every app
  screen. Never a graphic on a near-black field with one small element; never a screen that looks lame (stick-figure
  exercise icons got the trainer screen called "awful" — today every exercise in shot has a real AI demo).
- Every app screen is the REAL app: captured on a local fixture server (`DATABASE_URL=pgmem://local`, fixture admin +
  comp member, token in `localStorage`), viewport 390×738 at DPR 3, seeded through the app's own storage keys
  (`hub/hub_capture.py`, `macro2/`, `trainer/trainer_capture.py`). Never the before/after hero, never the email form.
- Captions: burned, word-timed from the TIGHT word list, lifted ≥ 20 px above every lower third (measured in pixels
  on the delivered frame), shifted right over PiPs, suppressed over full-frame cards, "abs" lowercase.
- Before → Dan → after needs ≥ 0.5 s of Dan between the cards (asserted in `beats.py`).

### 4. AI inserts — invest until each one is perfect

Read `reference/AI_CLIPS.md`. The short version: stills first (nano-banana from the character reference
`ai/prompts/MAN.txt`, in-place edits of an approved still when only one thing changes), Step 4.5 vocabulary from
/ad-edit (no camera/rig/grandeur words, fight the default person, frame it slightly wrong), whole figure inside the
frame, then Veo 3.1 Fast 8 s 1080p. **Every clip passes the acceptance checklist on frame strips of its first
second, last second and whole length before it goes in — and a clip that fails is regenerated, not trimmed around,
up to three attempts.** Trimming is for a clean clip that is too long, not for hiding a flaw (rev 4 shipped two
tails that way). Same man, same ambience density, tagged AI-GENERATED upper-left at 1.5×, captions stay on.

### 5. QC and delivery — more thorough than any other video

`deliver.sh <master>` runs, on the exact file that ships: the audio gate + stamp + A/B, the exact-grab contact sheet,
`qc.py` (splices, jump cuts, levels, pacing, loudness, script fidelity, drug names, tags, banned screens on EVERY
frame, caption/card and caption/lower-third/PiP clearance in pixels, hair on the delivered frames), `watch.py` (every
frame for frozen runs and black; consecutive-frame strips at every boundary), the 540p review copy, and the silence
check. **Then the human pass, which no metric replaces**: open `watch/strip/*.png` and `pv/final_sheet_5s.jpg` and
look, with `reference/REVIEW_HISTORY.md` open beside them — that list is exactly what Dan looks for. A subjective
retouch (a skin patch, a colour choice) ships as **two masters** (`_A` / `_B`) plus a region A/B clip so he can judge
in twenty seconds instead of watching twice.

## The one-shot pre-flight (run through this before you send anything)

Each line is a revision that happened. If any line is not a measured yes, it is not ready.

- [ ] Audio gate PASS on the delivered file, room ≤ 50 ms, damage row PASS, fidelity ≥ 99 %, A/B built. (rev 1, rev 5)
- [ ] No `loudnorm` anywhere; bed ≤ −44 dB or absent; compressor off. (rev 1)
- [ ] Hair: proof sheet at native scale looked at; hairgate PASS incl. the detector-free test; no wide level, no light. (rev 2, rev 3)
- [ ] `repeat_scan.py` + `orphan_scan.py` clean on the transcript — no stitched restart, no abandoned take. (rev 2)
- [ ] Captions clear every lower third and PiP by ≥ 20 px, measured; none on a card. (rev 2)
- [ ] Every AI clip: first/last-second strips looked at; no smoke/breath, no drifting objects, no baked dissolve, no
      static hold at the end, no look-to-camera grin, whole figure in frame, movement reads as the named exercise. (rev 4, rev 5)
- [ ] Every app screen real, no stick figures, no before/after, no email form; screens sit beside Dan, not on a plate. (rev 1, rev 5)
- [ ] Food and props match Dan's preferences stated in review (steak, not chicken; no weights at home). (rev 5)
- [ ] Skin: any patch Dan has mentioned handled by a landmark-anchored gain, under-corrected, delivered as A/B. (rev 5)
- [ ] Nothing sits static > 25 s; no jump cut; no card the video ends on fades out. (rev 1–3)
- [ ] Watch pass 0 frozen / 0 black; every flagged jump explained by an insert or a photo swap. (rev 4)
- [ ] `notes.md` written for a non-technical reader: what changed, what did not, the gate table, what to look at.
- [ ] Both review copies + audio A/B (+ region A/B) sent in chat; rev N−1 preserved as `*_REV<N-1>`.
- [ ] The build never ran more than two encodes at once; nothing ran inside another session's build dir.

## THE DELIVERY GATE — `_shared/deliver/gate.py` **(REQUIRED on the delivered file, 2026-09-11)**

```bash
python3 .claude/skills/_shared/deliver/gate.py <delivered file> --format website --plan plan.json
```

**One gate, all six video skills, run on the file that is actually going out.** It carries the
union of the rows that used to live in seventeen per-video QC forks, with every bound in
`_shared/deliver/formats.py` beside the file and the date it was measured on. It writes
`<file>.deliver_gate.json`; `gate.require_stamp(<file>)` refuses anything without a PASS stamp at
the current `GATE_VERSION`.

- **A missing input is `NOT MEASURED`, which FAILS** — never a silent skip. `--plan-keys` lists what
  `plan.json` may carry; a row whose key is absent says so and fails.
- **A row this format has not answered for FAILS as `UNCONFIGURED`.** If a check genuinely does not
  apply here, add it to that format's `not_applicable` in `formats.py` with a written reason.
- **Never raise a bound to make a build pass.** `python3 .claude/skills/_shared/qc_corpus/run.py`
  must stay green, and it is what proves a bound change did not resurrect a rejected cut.

⚠ The older per-video QC script in `reference/` still runs and still has rows this gate has not
absorbed yet (the watch pass is Phase 3 of `Handoffs/handoff-20260911-video-quality-engine.md`).
**Framing landed in the shared gate 2026-09-12**: the five `framing:` rows in
`_shared/deliver/checks/framing.py` grade the delivered file with mediapipe FaceMesh + Apple Vision
person segmentation, so they need no `hairtrack.json` door-panel profile and run on any set.
`hairgate.py` stays as this recipe's plan-side check (it still drives the anchors); the shared rows
are what the stamp is judged on. **Run both until Phase 3 lands.**

## Delivery layout

```
claude edited long form content/<NN> - <Video name>/      working delivery (every revision, ALT masters, rollbacks, pv/, recipe/)
  website_video_16x9.mp4 (+ .audio_gate.json)              the master, gated and stamped
  website_video_16x9_ALT.mp4                                the losing version of an A/B, if any
  REVIEW_540p_website_video.mp4   AB_his-vs-ours.mp4   AB_<region>.mp4   notes.md   pv/   recipe/
  *_REV<n>.mp4 / notes_REV<n>.md                            superseded revisions, never deleted
Website Videos/<Video name>/                                Dan's finished-video folder (git-ignored): final master,
  website_video_16x9.mp4  REVIEW_540p…  notes.md  README.md   stamp, review copy, notes, pointer back
```

On "finalized": export from the pre-caption master at CRF 14 / preset slow / AAC 320k, run `deliver.sh` on that file,
file it in both folders, and write the YouTube-unlisted + `public/site-video.js` install handoff (the Chrome extension
cannot upload > 10 MB and the stored Google token is calendar-only — say so in the handoff).

## Decisions locked (Dan)

| decision | status |
|---|---|
| Audio = the rev-2 chain + the 2026-09-09 approved dereverb, gated against Muhammad incl. the damage row; A/B every delivery | LOCKED 2026-09-02 / 09-09 |
| Framing = hair-anchored NEAR/FAR/PIP, 4 % headroom, hairgate + detector-free test on delivered frames, never wide, never the light | LOCKED 2026-09-08 |
| Trust pacing: ≥ 9 s holds, ~0.30 s pauses, no SFX, cards fade 0.5 s | LOCKED 2026-09-01 |
| Graphics sparingly; app screens as phone PiPs beside Dan; never a plate on black; never a lame screen | LOCKED 2026-09-02 |
| Before → Dan → after, never side by side; no email form; no goal-image card at the close (emphasis on the prospect) | LOCKED 2026-08-20 / 09-08 |
| AI inserts to break up the talking head, tagged, captions on; regenerate until perfect | LOCKED 2026-09-08 / 09-09 |
| Steak, not chicken, in meal clips; home exercise clips without weights | Dan, 2026-09-09 |
| Subjective retouches ship as two masters + a region A/B | Dan, 2026-09-09 |
| Two builds max at once, machine-wide | AGENTS.md |

## When something is new

A new set, a new script, a new product feature to show: keep the rule, re-derive the number, and write the number
down here with the date. The runbook tells you which script holds each number. If a review adds a rule, it goes into
`reference/REVIEW_HISTORY.md` AND into the pre-flight list above — the list is the contract.
