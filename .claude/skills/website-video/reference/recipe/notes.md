# Website conversion video — 16:9 master, REVISION 5

**You approved rev 4's framing and locked it as the standard** ("The framing and the cropping are all looking good. You
nailed it with this one. Let's lock that in and crop all the videos like this going forward"). **Nothing about the
framing changed here** — the same `punched.mov` file from rev 4 is reused, byte for byte, so every crop you approved is
literally the same picture. Rev 5 changes exactly the three things you asked for and nothing else.

| | |
|---|---|
| master | `website_video_16x9.mp4` — **3:50.23 (unchanged)**, 1920×1080, 29.97 fps, AAC 256k |
| review copy | `REVIEW_540p_website_video.mp4` |
| audio A/B | `AB_his-vs-ours.mp4` — Muhammad's ad, then the same window of ours (audio chain unchanged since rev 2) |
| rev 4 | `website_video_16x9_REV4.mp4` — kept beside it (superseded, not rejected) |
| AI spend | **$0.00** — both clip fixes are trims of clips we already have; nothing was regenerated |

## 1 — The grilling clip at 2:27 (the smoke)

You were right, and the cause was my prompt: I asked for a man who "leans in, breathes in the smell and smiles," and Veo
rendered the breath as smoke coming out of his mouth. Measured on the source clip at 0.1-second steps: he is upright and
stirring until **4.4 s**, leans in over the pans from 4.4 s, and the puff appears at his mouth **5.0–5.4 s** — which was
the last second of the insert.

The fix is a trim, not a regeneration: the clip run now starts **one word later**, on "customize," instead of on "Your AI
will also," so the beat is 3.68 s instead of 5.21 s and the clip is cut at 4.08 s of source — **0.3 s before he starts to
lean**. You are on camera for "Your AI will also" (1.5 s) and the clips fade in on "customize." The insert now ends with
him stirring the pan. Proof: `pv/rev5_insert_d1_last.jpg` (its last second at 0.1-s steps).

## 2 — The portioning clip at 2:33 (the containers sliding and vanishing)

Same thing, also confirmed: in the wide shot the row of containers starts to drift at about **7.0–7.1 s** of source and
is visibly displaced by 7.6–7.95 s. Veo drifts static objects when a shot ends on them.

The wide shot is now cut at **7.05 s** — the insert's last frame is source 6.99 s, before the drift starts. The 0.97 s
that came off it went to the next clip (the eating shot), which had spare footage: its tail was measured clean to the
last frame, so it now runs 7.58 s instead of 6.61 s. Nothing was slowed down to fill the gap. Proof:
`pv/rev5_insert_d2_last.jpg` and `pv/rev5_insert_d3_last.jpg`.

## 3 — The goal-image card at 3:36 — removed

Gone. You are on camera for "But now AI has solved that … a plan to get you there," with captions on, and **nothing
replaces it** — you asked for a removal, not a swap. The framing still changes twice inside that stretch (FAR at 3:25.7,
NEAR at 3:35.1, FAR at 3:42.0), so it does not sit static; the push-in now lands on the line itself rather than on a
picture of you.

**If you'd rather have a prospect-facing visual there** — their own goal image, or the "look near your image" cue — say
so and it is a one-beat rebuild. I did not build one, because that is a different ask.

## 4 — What did NOT change

The crops and the punch plan, `punched.mov` itself, the hair track, the grade, the EDL and tight cut, the audio chain
(bed −44 dB, no compressor — the one you approved by ear on rev 2), the caption style, the six lower thirds, the
before/after-photo cards, the two phone screens, the trial/price/CTA cards, and the other four AI clips.

Worth stating plainly, because a beat edge moved and that normally forces a 20-minute punch re-render: it was **proved
frame by frame** that it did not. Only 29 frames of the whole video get a different crop from the new beat edges, and
all 29 sit underneath the eating clip, which is a full-frame opaque insert — so no frame you can actually see changed.
The rev-4 punch file was reused unmodified.

## 5 — Gates

All green on the exact delivered file, same suite as rev 4 plus the two checks the goal-image removal changes:

| | |
|---|---|
| audio gate | **PASSED all 11 rows** and stamped the file — tone 0.88 dB mean / 2.02 max vs Muhammad's ad, floor +2.5 / +0.5 / +0.2 dB, early decay 77 ms, −14.50 LUFS, −2.60 dBTP, voice centred (L/R +0.9999, side 45.5 dB under mid), 0 silent seconds |
| QC | **all checks PASSED** — 0 bare splices above the p99 ceiling, no jump cuts, levels exactly NEAR/FAR/PIP with no wide crop and nothing reaching the light, median hold 4.46 s / longest 9.91 s, script fidelity **99.0 %**, no drug names, **no goal-image card**, all 7 AI inserts tagged, no banned app screen on any of 6900 frames (best 0.36 against a 0.90 limit) |
| captions | 145 cues, none on a card; every caption clears its lower third by **62–73 px** (tightest 62 px at 1:24), none inside either phone box or the AI tag |
| hair (delivered frames) | **43 px minimum, 57 median**, per-segment minimum 43–53 px in every hold, and the detector-free test found **0 of 4754 frames** with hair in the top 12 rows — identical to rev 4, as expected from reusing its punch |
| watch pass | 6900 frames, **0 frozen runs, 0 black frames**; the 30 flagged jumps are all inside AI clips (23 in the garage-gym curls, 6 in the beach jog, 1 photo swap) — none in the talking head |

## Recipe

`build_inserts.py ai_d1 ai_d2 ai_d3` → `layout.py mix` → `audio3.py` (bed −44) → `captions.py` → `deliver.sh`
(`sheet.py`, `qc.py` + `qc_frame.py` + `hairgate.py`, `watch.py`, review copy). `rev5.sh` is the whole chain;
`strip.py` builds the clip frame strips. Working dir `/Volumes/Extreme/_edit_work/website-video-828/`; rev 4's notes are
`notes_REV4.md`, its scripts are in git via the skill's `reference/website-video/`.
