# Handoff: Cut Shorts from "The Supplements I Actually Take"

**Date:** 2026-08-28
**Project:** Abs By AI
**Handing off from:** Claude Code
**Handing off to:** Claude Code (invoke `/shorts`)
**Business goal this serves:** Five finished long-forms have never been mined for short-form —
~2h12m of talking head sitting idle. This is the first of them. It also fills a measured paid-side
gap: the 2026-08-26 ad audit found **AI Trainer, Nutritionist and Supplement Audit appear in zero
ads and zero keywords**, so supplement-topic organic Shorts reach an audience the ads currently
cannot.

⚠ **DAN HAS NOT PICKED YET, AND THAT IS DELIBERATE — HIS INSTRUCTION IS THAT HE PICKS IN THIS
SESSION, NOT THE ONE THAT WROTE THE HANDOFF. YOUR FIRST ACTION IS STEP 0.5: PUT THE SHORTLIST IN
FRONT OF HIM AND WAIT.** The 14 candidates are already researched, timecoded and written up — the
work is done, it just needs his letters. Segment selection has been his call since 2026-08-04.
**Do not cut anything before he answers, and do not substitute your own judgement for his.**

---

## Objective

Cut N vertical 1080×1920 Shorts from `03 - The Supplements I Actually Take`, to the locked J2
design system, QC'd and delivered to `Short-form video content/` with a `SHORTS.md`.

---

## Why this video was chosen first

It is structurally the closest thing we have to **V3 (My Top 10 Tips)**, which is the highest-
yielding source ever cut — 11 shorts. Both are a sequence of discrete, self-contained items rather
than one continuous argument. 26 chapters, most of them a single supplement with its own reason to
exist.

| | |
|---|---|
| Runtime | **23:29** (1409.49 s) |
| Chapters | 26 |
| SRT | 820 cues, rebuilt 2026-08-27, spans 0.12 → 1408.47 s |
| Style-gate state | rebuilt to the new standard 2026-08-27 (11/1, 18.1 cuts/min, 43 % insert coverage) |
| Published on YouTube | **Believed NO** — ⚠ verify, see Step 0 |

---

## Step 0 — three things to confirm before cutting

1. **Is the long-form published?** The coordination record says Dan has not yet watched the review
   copies and `/youtube-packaging` was never run on it, so it is almost certainly unpublished. The
   standing rule is **post Shorts every 2–3 days AFTER the long-form goes up** — so the Shorts can
   be built now, but the posting schedule waits on the parent video. Say so in `SHORTS.md`; do not
   queue anything in Blotato without asking Dan.
2. **Check concurrent builds** (`ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'`).
   Cap is **two** across all sessions. Measured 2026-08-27: four concurrent builds cost a 9.3×
   latency penalty and bought zero throughput.
3. **Dashboard** — this handoff's Key task is `money::Execute handoff: cut Shorts from the
   supplements long-form (03)`. Check it off only when the files are delivered AND Dan has watched
   the review copies. Ad 1 attempt 1 had a check-off reverted for exactly this.

---

## ⚠ CUT FROM THE CLEAN MASTER, NOT THE DELIVERED ONE. This is the decision that shapes the batch.

The folder holds five MP4s. **Use `CUT_v1_graded_NO-GRAPHICS.mp4`.**

| file | duration | what it is |
|---|---|---|
| `FINAL_supplements.mp4` | 1409.493 s | delivered master — ~150 burned graphics, 43 % insert coverage |
| **`CUT_v1_graded_NO-GRAPHICS.mp4`** | **1409.523 s** | **same picture edit, graded, NO graphics and NO stock inserts** |
| `FINAL_supplements_PRE_REBUILD.mp4` | 1409.508 s | the 8/20 cut, superseded |
| `FINAL_supplements_PRE_AUDIOFIX.mp4` | 1409.523 s | pre two-mic fix — **do not use, the voice is comb-filtered** |

**Proven frame-aligned, not assumed.** All four are within **0.03 s** of each other, and matched
frame grabs at 200 s / 400 s / 620 s / 900 s / 1150 s confirm the clean master carries the same
picture with graphics absent. At t=200 s `FINAL` shows the "ATHLETIC GREENS" J2 card while the
clean master shows Dan on camera. **So every timecode in this document is valid against either
file**, and the SRT lines up with both.

Why this matters: at 43 % insert coverage, cutting from the delivered master would make nearly half
of every short a full-frame graphic that has to be treated as a `card` under the skill's rules —
producing shorts that are mostly not-Dan. The clean master gives full-bleed talking head, and we
add our own J2 graphics designed for the vertical frame.

⚠ **Audio comes from the clean master too, and it is already correct** — the two-mic comb filter
was fixed on 2026-08-23 (right channel only, per-roll EQ fit, band error 2.37 → 0.39 dB,
−14.02 LUFS / −1.21 dBTP). Do not re-process it. Do not touch `*_PRE_AUDIOFIX.mp4`.

---

## ⚠ THE LAYOUT PROBLEM: the counter is the payload, and a 9:16 crop deletes it

This is the one genuinely new thing about this video and it needs a decision per short.

The whole video is **one locked camera**. Dan stands behind a granite counter with **the entire
supplement stack laid out across the full width of the frame** — Anthony's collagen, Isopure, the
Thorne bottles and the white tubs on the left and centre, AG1 and Cure on the right. Measured from
the frame grabs, Dan's torso sits at roughly **x ≈ 0.60–0.63** of frame width, not 0.478.

A 9:16 window is **0.317 of the frame**. Centred on Dan that spans ~0.46–0.78 — it keeps the tubs,
Cure and part of the AG1 bag, and **deletes the entire left half of the stack**.

So:

- **A short whose payload is a specific product** (fish oil, AG1, vitamin D, creatine, the Thorne
  bottles) → **band layout**, `reference/band/`. The whole 16:9 frame sits uncropped in the lower
  ~74 % and the graphics band takes the top ~430 px. The stack stays visible, and this is the same
  layout the five V4 shorts use.
- **A short whose payload is an idea with no product on screen** (A, D, E) → **full-bleed 9:16**,
  which is sharper (1.78× upscale vs the band's ~1.32× on a narrower window) and more intimate.

**Do not decide this from the plan — measure it per Step 6 of the skill.** Sample frames across
each chosen segment and measure how often the candidate overlay regions are clear.

⚠ **And measure `TALK_X` PER SHOT with the Vision torso-block method (`recentre/`).** Do not reuse
one constant. That is exactly what shipped 10 off-centre Shorts and got caught by Dan on
`v2-short3` on 2026-08-27. His measured centre here (~0.60) is already far from the 0.478 that V2
and V3 hard-coded. On a single locked camera a per-shot constant is enough — no pan.

---

## Step 0.5 — PUT THE SHORTLIST TO DAN AND STOP

**This is the first real action of the session. Everything after it is blocked until he answers.**

1. Read `Handoffs/assets/shorts-supplements-20260828/shortlist.md`. It holds all 14 candidates with
   working titles, real timecodes, verbatim spoken text, estimated finished runtime at his measured
   200 wpm, and the reason each one is ranked where it is. Full untrimmed text for every candidate
   is in `verbatim-candidates.txt` in the same folder.
2. **Present it to him in chat** — do not just link the file. He picks by letter, and he picks
   faster when the text is in front of him. Lead with the four strongest (B, A, D, E), then the
   solid six, then the weak four with their reasons for being weak.
3. **Surface these three flags in the same message**, because they change which letters he wants:
   - **[F]** ends on "I would recommend going on Zepbound instead." Organic Shorts *can* name the
     drug — the no-drug-names rule is ad-compliance only (proven 2026-08-25). His call. Offer the
     clean alternative: end at "…it doesn't make any sense" (~19:58), a complete thought that loses
     nothing.
   - **[I]** contains "I just uncontrollably shit myself" *and* a sentence that does not parse as
     transcribed (see the [I] note below).
   - **[N]** is the closest to failing the reason-to-watch test.
4. **Then stop and wait.** Do not start Step 1, do not transcribe, do not render a test.

A reasonable default to offer if he asks for a recommendation rather than choosing: **B, A, E, C,
J, M** — the two strongest standalone beats, the most relatable one, and three product shorts that
would use the band layout. F and I are excluded from that default only because of the flags above,
not on quality.

Once he answers, record his picks here before building:

| pick | working title | in → out | source dur | words | est. finished |
|---|---|---|---|---|---|
| | | | | | |

Candidate letters throughout this document refer to the shortlist file.

---

## Per-candidate build notes (apply to whichever Dan picked)

**[A] Let AI read the research — 0:58.76 → 2:16.03, 202 words**
The video's thesis and its strongest hook. ⚠ Opens mid-word: the SRT's first token is `-based`
(the tail of "science-based"). **Move the in-point to the start of "You are not smart enough"** and
verify against measured silence. Contains "Don't even get your supplement recommendations from me
only" — keep it, it is the line that makes the short honest rather than an ad. Full-bleed layout.
⚠ Dan flagged this line for review on 2026-08-20 and chose to keep it; it is still spicy for
anything paid.

**[B] The big three — 17:32.18 → 18:07.65, 119 words**
The most self-contained beat in the video and the strongest single Short. Also opens mid-sentence
(`is with what I call the big three`) — the natural in-point is ~17:30, "the best way to get
started is with what I call the big three". Band layout so the three products can be shown. This
should be **posting order #1** regardless of what else gets cut.

**[C] If you only take one supplement — 6:57.15 → 7:31.20, 117 words**
Trim the leading `recommended by AI for those reasons` fragment. Starts cleanly at "Fish oil is one
of the most important supplements." Band layout — hold on the fish oil bottle.

**[D] Supplements are only 5 % — 20:42.66 → 21:49.73, 254 words**
Needs the heaviest trim (254 → ~180). The ironing-your-clothes-before-a-date analogy is the
payload; the first ~40 words are wrap-up throat-clearing. ⚠ Contains "if you're fat and broken. You
say stupid things" — that is the joke landing, and it is on-register per the BE CONTROVERSIAL rule,
but flag it to Dan before anything paid. Full-bleed.

**[E] The biggest mistake I made — 16:35.58 → 17:25.03, 182 words**
Already almost exactly the right length. Highly relatable, fully actionable (basics → 30 days →
one new supplement per month). Full-bleed, though "I bought a huge stack like this" gestures at the
counter, so consider band.

**[F] Pre-workouts are over-priced caffeine — 19:17.10 → 20:09.65, 171 words**
⚠ **Contains "I would recommend going on Zep bound instead."** Per the 2026-08-25 research the
no-drug-names rule is **ad-compliance only, not organic** — Renaissance Periodization did 502K on
a Tirzepatide title with no suppression. So it is postable organically, but **Dan decides**, and it
must never appear in a graphic (standing rule). The clean fix if he wants it out: end the short at
"...it doesn't make any sense" (~19:58), which is a complete thought and loses nothing.
Also note Whisper renders it "Zep bound" — never print that in a caption.

**[H] The one I don't take that you should — creatine — 15:28.78 → 16:13.29, 132 words**
Trim the leading `and more sleep overall`. Strong angle: recommending something he doesn't take.
⚠ Whisper garbles one phrase — "not just for ...building" — the audio needs re-checking there;
that ellipsis is a transcription artifact, not a pause. Contains "diarrhea and gas".

**[I] Why I can't take whey — 12:27.40 → 13:14.45, 144 words** ⚠ **READ THIS BEFORE PICKING**
Two problems.
1. **Profanity:** "I just uncontrollably shit myself." On-register per the BE CONTROVERSIAL rule
   and it is the funniest line in the video, but it is Dan's call and it is unusable in anything
   paid.
2. ⚠ **A sentence in it is self-contradictory as transcribed:** *"Most people, you can't take whey
   protein, so you should be doing that instead of the Aminos"* (13:00.96). The following clause
   only makes sense if he said **"can"**. Both the rebuilt and the pre-rebuild SRT read "can't" —
   but those are two Whisper runs on the same audio and agreeing does not settle it, since "can"
   vs "can't" is a known-hard acoustic call. **Resolve it by ear/energy at 13:00.9–13:03 during
   Step 1.** If it really is "can't", that sentence must be cut from the short — burning a caption
   that reads "you can't take whey protein, so you should be doing that" would ship visible
   nonsense. The short still works without it.

**[J] 70 % of people are deficient — vitamin D — 4:41.35 → 5:39.68, 187 words**
Strong stat hook, concrete dose (5 drops / 5,000 IU), and a contrarian beat ("I think the USDA is
wrong"). ⚠ Whisper writes the numbers as `5 ,000` and `1 ,000` — the skill's punctuation-merge rule
must run BEFORE chunking or a caption will read `5 ,000`. Band layout.

**[K] Eat before you take the pills — 5:50.29 → 6:32.40, 139 words**
Solid but the least distinctive of the set. Only cut it if Dan wants volume.

**[L] The three supplements for my skin — 9:54.80 → 11:06.91, 248 words**
Needs trimming to ~180. ⚠ Names **"clavicular"** (a looksmaxing influencer) — that is on-register
and aligned with the attraction philosophy per `/scriptfromoutline`, but it is a named third party;
flag it. Concrete payload: B6, zinc, DIM for cystic acne. Trim the leading `what I take for my
joint health` fragment.

**[M] The one that probably does nothing — 11:13.98 → 12:03.53, 164 words**
The honesty IS the hook. Payload: zinc is the part that works, and it works for acne too. Right
length as-is. Band layout — the Thorne bottle should be visible.

**[N] Joint health in your 40s — 9:08.66 → 9:56.31, 175 words**
⚠ **Closest to failing the reason-to-watch test.** "Seven days a week of hard weightlifting, two to
three days a week of jiu-jitsu" drifts toward the bragging failure mode that killed
`v6-short1_gained-muscle-in-quarantine`. It survives only because it ends on a real instruction
(take glucosamine/collagen if you want training sustainable into your 60s). **If Dan picks it, cut
the training-volume boast and keep the instruction.**

**[P] Curcumin, not turmeric — 8:07.46 → 8:34.29, 97 words**
Only ~29 s at Dan's pace, under the 45–60 s band the organic research found. Genuinely useful
distinction (2 caps vs 4–6). Either accept it short or extend the in-point back to 7:49 to pick up
the setup.

---

## Build steps

Follow `/shorts` end to end. What is specific to this video:

**Step 1 — word timestamps.** No `*-words.json` exists for this video. Generate one from the clean
master's audio. Local Whisper or Replicate `vaibhavs10/incredibly-fast-whisper` with
`timestamp: "word"` (token in `bakeoff/.env`, costs cents). **The 820-cue SRT is cue-level and is
NOT a substitute** — captions come only from word timestamps.

**Step 3 — snap every cut to measured silence.** `silencedetect=noise=-26dB:d=0.05`.
⚠ **This video has NO music bed** (the rebuild added inserts, not a bed — the gate's bed check
reads 0.8–1.1× on the videos that carry none), so `silencedetect` is the right tool here, unlike
the ab-wheel batch where the scored source made it useless. Bound the snap to the neighbouring
word, assert every cut lands inside a measured silence, and report all failures in one pass.

**Step 4 — shot classification.** On the clean master there is only ONE camera setup for the whole
23 minutes, so there is effectively one `talk` treatment and no cards to preserve. That makes shot
detection almost trivial — but **run `work/boundcheck.py` anyway** on any boundary you do find:
the detector runs on a 320×180 downscale and put a cut 0.60 s early on the ab-wheel batch, which
presented as a framing bug.

**Step 5 — crop offsets via the Vision torso block**, per shot, 5 frames sampled across each.
`recentre/`. Then look at the A/B sheets; the metric over-fires.

**Step 7 — title placement.** ⚠ Standing rule (Dan, 2026-08-28): **the title may never sit on his
face or his abs.** On full-bleed shorts use the `dropTop 310` geometry from
`scored-source/layout.json` — picture rendered into 1080×1610 at the BOTTOM, J2 field carries the
title. Assert it on the delivered file with `work/titleclear.py`, six samples across the title
window. Band-layout shorts do not need the drop.

**Step 8 — captions.** ⚠ Standing rule (Dan, 2026-08-28): captions print **`abs` in lower case**.
`AI` stays upper case. Also, on this transcript specifically: merge punctuation-leading tokens
before chunking (`5 ,000`, `1 ,000`, `-based`, `Zep bound`).

**Step 9 — one audio pull per segment**, shots rendered `-an`. Do not cut audio per shot.

**Step 10 — QC.** `qc.js`, then a contact sheet of every card moment from the finished file.
Normalise loudness across the batch afterwards — the source is a single continuous take at
−14.02 LUFS, so the spread should be small, but check it.

---

## Delivery

- Work folder: create `YouTube Long Form Video Content/supplements-i-actually-take/` (the source
  video lives in `claude edited long form content/`, but the shorts pipeline's working files belong
  with the other shorts work).
- Output naming: **`supp-short1_<slug>.mp4` … `supp-shortN_<slug>.mp4`** in
  `Short-form video content/`. Existing prefixes in use: `short` (V4), `v2-`, `v3-`, `v6-`,
  `abwheel-`. Do not collide.
- `SHORTS.md` in the work folder: posting order, per-short title, description with
  `utm_source=youtube&utm_medium=short&utm_campaign=supplements&utm_content=<id>`, editorial notes,
  and how graphics were handled.
- 540p review copies sent to Dan in chat. Scan every review copy for silent seconds before sending
  (standing rule).
- Both media folders are git-ignored — verify with `git check-ignore` before staging anything.

---

## Compliance and flags to carry into `SHORTS.md`

| item | where | call |
|---|---|---|
| **Zepbound named** | F, 19:58 | organic OK per the 8/25 research; never in a graphic; Dan decides |
| **"I just uncontrollably shit myself"** | I, 12:51 | on-register, unusable paid |
| **"if you're fat and broken. You say stupid things"** | D, 21:20 | the joke landing; flag before paid |
| **"You are not smart enough…"** | A, 0:58 | Dan reviewed and kept it on 8/20 |
| **"clavicular"** named | L, 10:00 | named third party, on-register |
| **Brand names** (Thorne, Athletic Greens/AG1, Anthony's, Cure, Isopure) | throughout | **correct and allowed** — he names them on camera and the delivered chips already print them |
| **No before/after side-by-side** | — | none exists in this video; keep it that way in any end card |

---

## Cost and risk

**AI spend: ~$0.05** (one Whisper transcription) or **$0.00** if run locally. No production code,
no deploy, no native-retest trigger. Everything else is local ffmpeg/PIL.

**Risks:** none destructive. The source masters are read-only inputs; never write into
`claude edited long form content/`. If a re-cut is needed, keep the shipped values in a
`.pre-*` backup and recompute from that, never from a previous edit.

---

## Exact next action

**Do Step 0's three checks, then Step 0.5: present the 14-candidate shortlist to Dan in chat, with
the three flags, and wait for his letters.** Nothing gets transcribed, cut or rendered until he
answers. When he does, fill in the picks table above and run `/shorts` from Step 1.
