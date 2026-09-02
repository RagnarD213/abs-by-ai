---
name: ad-edit
description: >
  Edit a FILMED ad — Dan on camera reading a teleprompter script — from raw shoot
  footage into finished 16:9 + 9:16 ad creatives: script-driven rough cut, zoom cuts
  (never jump cuts), product-demo inserts, ad graphics, burned captions, color and
  audio per /longform-edit. Use whenever Dan asks to edit an ad, cut ad footage,
  build the ad from a shoot, or REVISE an ad edit — even if he doesn't say
  "/ad-edit". For fully AI-generated ads use /make-ad; for content videos use
  /longform-edit; for writing the script itself use /scriptwriting.
---

# Ad-Edit: raw teleprompter footage → finished ad creative

**STATUS: v1 — written 2026-08-20, before the first ad was cut.** Built from a
measured study of 11 winning direct-response ads (7 of Dan's own green-marked
winners + V Shred's #1 all-time and 2026 winner + MadMuscles' current top ad) —
see `reference/AD_STUDY.md` for the evidence. Several decisions are deliberately
PENDING until ad #1 ships (marked ⏳ below). **Update this file after every ad**
— especially the two LEARNING sections at the bottom. This skill is supposed to
graduate from "Dan directs the details" to "Claude places them unprompted."

## Why this is not /longform-edit

The stakes are inverted. A longform video costs its production; an ad's edit sits
in front of **thousands of dollars of paid testing**, so the end product must be
as polished as we can make it, and the parts that carry the marketing message —
the product-demo segments, the graphics, the CTA treatment — matter more than
anything else on screen. Concretely:

1. **The teleprompter script is ground truth (99%).** The cut is built TO the
   script, not inferred from an outline. Deviations in delivery are almost always
   Dan correcting a script mistake — keep his spoken version, flag the drift.
2. **Zero jump cuts.** Every take join is disguised by a zoom cut or covered by
   an insert. A visible jump cut fails QC.
3. **Burned captions** (longform deliberately uses SRT; ads never do).
4. **Two deliverables per ad: 16:9 primary AND 9:16 secondary** — this batch is
   horizontal-first; other batches may flip, and both must be strong regardless
   (responsive Google ads use every format; MadMuscles ships every winner in both).
5. **Cut the entire script, no length ceiling.** Dan's own winners run 4–7 min.
6. Graphics/motion graphics start **minimal** and grow via Dan's revisions —
   that's the learning loop, not a lower bar.

**Everything not listed here is /longform-edit, verbatim — do not re-derive it:**
footage download + Step 0.5 clip identification, Whisper word-timestamp
transcription, all six cut-placement rules (word boundaries PLACE, silence
VALIDATES), the video-use render chain + segment cache, per-roll color grading
(camera side only, never a WB correction on a skin-tone-subject video), two-pass
loudnorm to −14 LUFS, the QC assertion suite, all ffmpeg traps, `git
check-ignore` before staging, and working on the external drive `/Volumes/Extreme/`. Read that SKILL.md
first if you haven't this session.

## Step 0 — inputs

- **Script:** the ad's section of **"Abs by AI finalized scripts batch 1 -
  TELEPROMPTER"** (`1bpEndCcM-imeOWS0tp86l7Ud0bGyxLQ-MWZVAwcacgA`) — pure spoken
  words, THE ground truth for the cut.
- **Cues + assets + per-ad notes:** the same ad in **"abs-by-ai ads batch 1
  finalized scripts for teleprompter"** (`1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg`)
  — bracketed visual cues, placed images, compliance notes. Every cue is a
  graphics/insert obligation for the edit.
- **Footage:** same shoot setup as longform (Sony rolls via Drive / `/Volumes/Extreme/`). One
  teleprompter roll per ad plus b-roll clips.
- **Shoot requirement to flag BEFORE filming: ads must be shot 4K.** Both pillars
  of this skill — punch-in zoom cuts and the 9:16 export — need crop headroom. A
  1080p source leaves ~1.15x of zoom before softening and makes the vertical crop
  a 608→1080 px upscale. (Longform's 4K recommendation is a nice-to-have; here it
  is load-bearing.)

## Step 0.4 — AUDIO: `_shared/audio` is the standard. One lav pick, one chain, one gate, one stamp.

**Every video this skill renders takes the LAV TRACK ONLY, as mono, duplicated to centred stereo,
through ONE shared voice chain and ONE shared gate measured against Muhammad's `this picture got me
abs | muhammad | 16x9.mp4` — and `qc.py`/`qc5.py` and `deliver.sh` refuse a file that does not carry
that gate's stamp.** Module: `.claude/skills/_shared/audio/` (README there). Run `selftest.sh` before
a batch.

1. **`pick_lav.py <roll>`** on every roll, first. It probes every stream and channel (the 8/3 and 8/14
   rolls are two hard-panned mics; the 8/28 rolls are FOUR mono tracks with the lav on `a:1`), cross-
   correlates the live candidates, and writes `<roll>.audio_source.json` with the exact `-map` and
   filter. `base.py` reads that JSON. **No script writes `pan=mono|c0=c1` again** — on an 8/28 roll
   that takes the far mic or renders silence. It exits non-zero on ambiguity; do not guess.
2. **`voice_chain.py --in <tight cut> --out <out.mov> [--bed music --bed-db -30] [--extra sfx.wav]`** —
   the approved rev-2 chain (`audio3.py` is now a shim to it): dereverb only if the room measures
   > 55 ms, EQ FITTED to his file per roll (never a pasted curve), expander, compressor OFF (his LRA
   is 3.5), centred, bed ≤ −30 dB ducked, measured gain + `alimiter` (never `loudnorm`, which went
   dynamic on rev 1) to −14 LUFS / −2.5 dBTP in PCM. It refuses silent input (a stacked `pan`).
3. **`audio_gate.py <delivered file> --ab AB.mp4`** on the EXACT delivered file: L/R image, comb
   ripple, early decay ≤ 80 ms (the chain dereverbs above 55), 10-band tone (mean ≤ 1.2 / max ≤ 2.5 dB), floor between words within
   3 dB of his, dryness, −14 ±1 LUFS, speech spread, true peak ≤ −1.0 dBTP, zero silent seconds,
   length. It writes `<file>.audio_gate.json` with the file's sha256. **A FAIL is not deliverable**,
   and a re-render without a re-gate fails `require_stamp` on its sha256. Send the A/B (his three
   sentences, then ours) with every review copy.

History: rev 1 of the website video read L/R +0.998 and still failed by 9.5 dB on floor (bed −23 dB,
3:1 compressor with makeup, two air shelves); the spray-tan shorts passed every check and were
rejected on ROOM (85 ms vs his 40). Both are rows of the gate now. Lessons 28, 32, 33, 74, 76 below
are the measurements behind it.

## Step 1 — script-driven rough cut

Transcribe the roll (longform Step 1), then align the transcript against the
teleprompter script line by line:

- The script defines the **beats and their order** — nothing missing, nothing
  reordered. Grep for retake markers first (longform Step 2), then map every
  script sentence to its take(s).
- **When delivery deviates from the script,** default to Dan's spoken words (he
  fixes script mistakes live). If the drift changes meaning, drops a compliance
  phrase, or loses a scripted callback, flag it in the delivery notes.
- Build `ranges.py` + the EDL exactly as longform does, one range per kept take
  span. **Never split a range to hang a graphic** (chips map by source time).

## Step 2 — take selection (LEARNING MODE — currently hybrid)

Dan's protocol, set 2026-08-20:

1. **First minute: Dan picks.** Build a **take reel** — one MP4 containing every
   usable take of every line in roughly the first minute, each take preceded by a
   2s slate frame (`L3 T2` = line 3, take 2) and listed in chat with timestamps.
   Send it; he replies with picks. Do not assemble the first minute before this.
2. **Rest of the ad: Claude picks**, using the criteria below, and lists the
   choices (line → take, one-line reason) in the delivery notes so Dan can
   overrule cheaply.
3. **Record every pick of Dan's that differs from what Claude would have chosen**
   in "Take-selection lessons" below, with why (ask him if it isn't obvious).
   When the lessons converge, propose graduating: Claude picks everything and
   flags only genuine coin-flips. **Tell Dan when you're confident enough to take
   it over — that's his stated plan.**

Claude's starting criteria (to be corrected by his picks): complete and fluent
first; then energy/punch over smoothness, especially in the first 30 seconds; no
mid-word teleprompter cadence (audible reading rhythm); later takes of a line
usually beat earlier ones (he retakes because something bothered him); a take
whose ending flows into the next line's chosen take beats one that doesn't.

## Step 3 — no jump cuts: the zoom-cut system

Adjacent takes from one locked camera = a jump cut unless disguised. Two tools,
in preference order:

1. **Punch-in alternation** (what every studied winner does): alternate framings
   between consecutive takes — full frame ↔ ~1.15–1.3x digital punch-in (4K
   source: up to 2x). Keep the eyeline anchored (crop centered on his face, not
   the frame center) and alternate strictly — never two identical framings across
   a join. This doubles as visual pacing: in long uninterrupted speech, add a
   punch level change on a sentence boundary every ~10–15s even where there's no
   join to hide.
2. **Cover the join with an insert** — b-roll, a demo clip, or a graphic card
   spanning the cut. Prefer this when the join is mid-thought or the takes'
   framing/posture mismatch survives a punch.

QC assertion: no two adjacent segments from the same camera setup at the same
punch level. A dissolve/whip is NOT the default fix — the studied ads cut, they
don't dissolve (the only dissolves seen were the deliberate rewind-replay motif).

## Step 4 — product-demo segments (the paramount part)

These carry the marketing message; be pickiest here. Dan's rule set (2026-08-20):

- **Reuse an existing clip if one fits and isn't worn out.** Track every use in
  `reference/demo-clip-log.md` (create on first use: clip → source path → which
  ads/videos used it). **Once a clip has appeared in ~3–4 ads/content videos,
  generate a fresh one instead.**
- **No fitting clip → capture a new one:** run the REAL app and screen-record it
  — web at absbyai.com in a clean browser profile, or the iOS Simulator via the
  /make-ad product-capture recipe (`simctl addmedia` → real picker → real
  generation → `simctl io screenshot`/recording). **The make-ad warnings apply
  verbatim: real generations cost real money (state the spend), and a generation
  on the Apple-review demo account steals its home-screen hero — delete the stray
  transformation and verify the beach-man hero is restored.**
- Capture demos for whatever the script's cue sells — generation flow, Macro
  Tracker analysis, the Trainer program, Daily Brief — when a live demo
  communicates the value better than a still. When in doubt whether a segment
  wants a demo, it probably does — the cue list is the contract.
- **Treatment in frame (16:9):** a phone recording is 9:16 — use the longform
  split-screen geometry (phone at native scale, Dan filling the rest) when he
  talks over it, or a full-height phone panel on the locked graphics background
  for standalone demo beats. Punch into the phone column briefly on the key
  number/moment (longform rule). In the 9:16 export, demo recordings go
  full-frame — they're native vertical.
- **Compliance on every demo/AI asset:** the AI-GENERATED label on every AI
  goal/after image; never a drug name on screen. **NEVER a side-by-side
  before/after ANYWHERE — the in-app-UI exception is REVOKED (Dan, 2026-08-20,
  after ad #1 shipped the app's "Meet the new you" screen and he called it the
  most serious mistake in the video — account-suspension class).** The pattern is
  always: before → something else → after, with the after clearly tagged
  AI-GENERATED. An app screen that renders before+after together (e.g. "Meet the
  new you") is unusable; use the flow's before-alone / generating / after-alone
  screens instead.

## Step 4.5 — prompting AI inserts (stills and clips)

Applies to every AI asset that goes INSIDE a filmed ad — the b-roll clips, the
future-self demos, the pastiche shots, the opener treatments. Sourcing protocol
is unchanged (stock first, AI only when no great clip exists — see the
graphics-placement lessons); this is about what goes in the prompt once you've
decided to generate.

The failure these rules prevent is not "a bad clip". It's a clip that reads as
AI to a viewer who couldn't say why. Two things cause it: the prompt asks for a
film crew, or the model returns its default human being.

**Never let these words into a prompt.** Each one leaks a production the ad
isn't supposed to have:

- *Hardware* — any camera or lens brand, `anamorphic`, `large sensor`
- *Optics* — `bokeh`, `shallow focus`, `lens flare`, bare `depth of field`
- *Rig and move* — `dolly`, `crane`, `gimbal`, `steadicam`, `tripod`, `push in`,
  `whip pan`
- *Post* — `color grade`, `LUT`, `film grain`, `speed ramp`, `slow motion`
- *Grandeur* — `cinematic`, `dramatic lighting`, `epic`, `stunning`, `moody`
- *Crew* — anything implying a second camera, a boom, a light, or another pair
  of hands

Lean on the opposite instead: `handheld`, `overcast daylight`, `flat light`,
`slight camera shake`, `small reframe mid-shot`, `amateur photograph realism`.

**Fight the model's default person.** Image models return a symmetrical,
poreless, evenly-lit human, and that is the tell. State the texture outright:
open pores, uneven skin tone, a smile that sits slightly crooked, shadow under
the eyes, hair that's escaped. Proportions of a person, not a model. Dull flat
light, never low sun or anything shaped. Describe clothing down to its wear —
"washed-out olive hoodie, collar gone slack", not "casual clothes". A settled,
unremarkable expression: anything theatrical bakes in and then overrides your
direction for the whole clip. This is the same correction lesson 49 arrives at
from the other direction — write it in from the start rather than after a
"celebrity likeness" rejection.

**Rule out explicitly in the prompt:** lettering, logos or graphics on any
garment (generated type comes out as mush and the video model faithfully
rebuilds the mush); retouching; makeup; flawless teeth; sunglasses; hair across
the face.

**Frame it slightly wrong.** Subject off-centre, one small correction mid-shot.
Clean, centred composition is the clearest signal that somebody was paid to
stand there. (This does NOT relax the crop rules — never cut the top of the head
or the shorts line.)

**Check every still before it becomes a start frame:** six fingers, scrambled
signage, anything in the background that shouldn't be there. Whatever is in the
reference gets rebuilt as a solid object in the footage.

**If the clip has dialogue or a voice**, write it caught rather than performed:
contractions, hedges, stalls, sentences that stop and restart. Fragments are
correct. Keep any endorsement smaller than the product deserves — "okay, that's
actually good?" lands; "it's completely transformed my daily routine" kills it.

**Hold ambience density constant across every AI clip in one ad.** Background
that thickens or thins between clips gives the edit away faster than any visual
mismatch does.

## Step 5 — graphics

**LOCKED (ad #1 verdict, 2026-08-20): the J2 tactical system for graphics —
panels, tags, green/olive outlines, and the J2 CTA bar — with MadMuscles-style
captions (see Step 6).** Dan explicitly kept the olive-outlined J2 panel frames
and the J2 lower-third CTA bar and rejected the MadMuscles red-pill/blur-panel
look for everything except captions.

**Minimal-first policy (Dan's instruction):** for the first few ads, place only
the graphics that are *clearly* called for — the script doc's bracketed cues,
the CTA treatment, and compliance labels. **When unsure whether to add a motion
graphic or AI clip, DON'T** — Dan will direct placements in revisions, and every
directed placement gets recorded in "Graphics-placement lessons" below until
Claude can place them unprompted.

The proven ad-graphics vocabulary to draw from as the skill matures (all from
winners — details and examples in `reference/AD_STUDY.md`):

- **Persistent CTA lower-third from the first CTA to the end of the ad** (pill or
  bar: "Tap below or go to AbsByAI.com"). This is the single most consistent
  device across every winner studied. First CTA lands ~20s–1:30 in.
- **Side-panel inserts** beside the talking head every ~10–15s of pitch: b-roll
  in a rounded rect, text cards (white + red emphasis words), physique photos,
  red ✗ overs, simple graphs.
- **Numbered-step chips** pinned through listicle sections; numbered list cards.
- **Player-UI motifs** for hook-replay commentary: pause, rewind ⏪, red circle,
  yellow arrows, the animated pointing-hand at the CTA.
- **Metaphor visuals** for the mechanism, and the **AI-reveal shimmer** (exists
  in ad-factory, pure ffmpeg) on generated images.
- **End card:** goal-physique imagery (labeled) + "Tap below — or go to
  AbsByAI.com" + the persistent bar still running.

**Animated graphics live in `.claude/skills/_shared/motionlib.py`** (added 2026-08-21).

⚠ **2026-08-24: there were TWO copies and only one was in git.** `_shared/motionlib.py`
was the tracked one; `reference/motionlib.py` was an untracked duplicate sitting beside
it on disk. That is the drift this repo has already lost a pipeline to. Both per-skill
copies are now **shims that import from `_shared/`**, and `/longform-edit` imports the
same file — which it never did before, which is why its edits shipped static PNG chips
while the ad edits had animation, and why an outside editor beat it. It renders PIL
frame sequences to alpha MOVs that ffmpeg overlays: `card_in`, `bullets_build`,
`lower_third`, `title_card`, `callout_box`, `number_pop`/`pop_text`, `photo_swap`, plus
primitives (`panel_plate`, `stroke_box`, `dashed_arrow`, `chip`, `rounded_photo`) and
easing helpers. Its palette is the CONTENT style (bright paper, near-black ink, brand
red, Manrope) — for PAID ads keep the locked dark J2 look and use the components with a
J2 palette. `.claude/skills/_shared/sfxlib.py` generates the matching transition one-shots.
`reference/modern60/` is a complete worked example (tight cut → graphics → audio → QC).

Graphics are one overlay pass over the finished cut at CRF 18 (longform Step 7),
chips/graphics burned per the same PIL-not-drawtext rule, previewed composited
on a REAL frame before rendering — both longform traps (Copperplate small-caps,
eyebrow-over-bright-footage) apply.

## Step 6 — captions

Burned, word-timed from Whisper on the **final mixed audio** — never estimated
windows (the /make-ad rule Dan enforced; `captions-from-words.js` is the model).
Never `" ".join()` Whisper tokens (longform Step 8 token rules).

**LOCKED (ad #1 verdict, 2026-08-20): MadMuscles-style captions — Arial Bold
~64px at 1080p 16:9, white with black outline, centered, low third, above the
CTA bar — on top of J2 graphics.** Dan's caption rules, non-negotiable:
- **"abs" is ALWAYS lowercase in captions** (never ABS), every occurrence — it is
  the central recurring word of every ad. "AI" stays uppercase. (J2 Impact
  headlines on cards/end-cards are all-caps by design and are exempt.)
- **The first 30 seconds must be word-for-word accurate** — proof them manually
  against the audio (Whisper misheard "goal picture" as "gold picture" on ad #1).
  Outside the first 30s, small mishears are tolerable.
- Keep a per-ad corrections dict for recurring Whisper mishears.

Layout rule regardless of variant: captions sit ABOVE the persistent CTA bar and
never collide with it, with side-inserts, or with the AI-GENERATED labels; no
captions over the end card.
**Standing rule (Dan, 2026-09-02): captions never overlap ANY graphic — lower thirds, phone
insets, cards. Lower thirds sit at the bottom of the frame, captions lift above them, and QC
measures the clearance in pixels (lesson 99). A collision is a FAIL, not a note.**

## Step 7 — pacing targets (measured from the winners)

- **First 30 seconds are cut noticeably faster than the body** — the money zone.
  A montage/skit hook runs 0.7–2s per shot; even talking-head hooks alternate
  framing quickly. Match the hook's edit energy to its copy.
- **Body settles to a 4–7s median shot length**, with a visual change (punch
  level, insert on/off, demo cutaway) at least every ~15s.
- **Nothing sits visually unchanged longer than ~25s.**
- **No speed-up pass for now** — Dan explicitly deferred the /make-ad 1.2x rule
  for filmed ads; revisit only after he's watched a finished ad at 1.0x.
- **No music bed by default** (audio = longform: clean dialogue, −14 LUFS).
  Dan's old company A/B-tested WITH/NO-music variants — treat music as a future
  variant axis he triggers, not a default.
- Hook variants (swap the first 5–10s, MadMuscles-style) are **out of scope for
  v1** — deliberately deferred to keep this skill buildable; add when Dan asks.

## Step 8 — the 9:16 secondary export

Not a center crop. Rebuild the frame:

- Talking head: crop tracked/centered on Dan (4K source makes this clean).
- Demo screen recordings: full-frame native vertical.
- Graphics + captions: re-laid-out for vertical (captions per the /make-ad
  1080×1920 spec numbers; CTA bar lower; side-inserts become full-width cards
  above/below him).
- Same EDL, same audio — only the visual layout pass differs. Keep both builds
  in one script so a revision re-renders both.

## Step 9 — compliance scan (before delivery, every ad)

1. AI-GENERATED label on every AI image/clip, in both aspect ratios.
2. No side-by-side before/after ANYWHERE, including inside real app UI (rule
   hardened 2026-08-20 — scan every insert frame for it explicitly).
3. No drug names spoken or on screen ("weight loss medication" only).
4. **Negative-imagery scan (Dan's rule, 2026-08-20):** sample frames across the
   finished cut and check for Google's "Negative Events and Imagery" triggers —
   above all **zoomed-in close-ups of overweight/out-of-shape body parts framed
   with disgust or shame** (the fat-belly close-up + disapproving reaction is the
   classic strike; it already limited one of our Demand Gen creatives). Close-ups
   of fit bodies (abs, biceps) are fine. **Certain violation → replace the shot
   yourself and say so. Unsure → leave it in and flag it for Dan's call.**
5. The /make-ad micro-disclaimer applies to AI-actor content only; a filmed ad of
   Dan needs no actor disclaimer, but keep "Results are not guaranteed" if the ad
   shows transformation claims and Dan hasn't said otherwise. ⏳ confirm on ad #1.

## Step 10 — QC, review loop, delivery

**QC = the full longform Step 9 suite** (splice discontinuity vs control
distribution, loudness, no sub-0.20s adjacent ranges, graphics-window
assertions, re-transcribe flagged joints from the FINISHED render) **plus:**

- Script-fidelity check: re-transcribe the finished ad and diff against the
  teleprompter script — every script beat present, in order; deviations listed.
- No same-framing adjacent segments (the jump-cut assertion).
- Caption timing spot-checks against the final mix; caption/CTA/label collision
  check at both ratios.
- The compliance scan above.

**Review loop (the polish bar for ad #1, per Dan):** the fundamentals — clean
script-true rough cut, zoom cuts everywhere, demo inserts and clearly-called-for
graphics — done right in v1, then **expect significant revision rounds** where
Dan specifies graphics/AI-clip placements. That's the design, not a failure.
Sequence per ad:

1. Take reel for the first minute → Dan's picks.
2. Full v1 (ad #1: both style variants) → Dan's notes.
3. Revisions off the segment cache — a one-beat change re-renders in minutes.
   Deliver both ratios only once the 16:9 is approved (don't double every
   revision render).

**Delivery layout** (on `/Volumes/Extreme/`, per longform; media stays out of git):

```
<shoot>/EDITED ADS <date>/<ad-slug>/
  <slug>_v1_16x9.mp4          the deliverable
  <slug>_v1_9x16.mp4          after 16:9 approval
  take-reel_first-minute.mp4
  CUT_v1_graded.mp4           pre-graphics rollback point
  edl.json, ranges.py, chips.py, notes.md   the recipe
```

Copy any new generic script into this skill's `reference/` (the longform lesson:
scratchpads get cleaned, git-ignored media folders lose code).

No human editor is in this loop — this skill is the entire pipeline.

---

## Take-selection lessons (LEARNING — append every divergence)

Ad #1: Dan did not overrule any pick. The take reel offered the prompter-test
pass vs the slated master; v1 shipped the master (Claude's default) and his
revision notes accepted it silently. One correction that IS take-selection
signal: the kept 2nd instance of a repeated sentence contained a 2s-pause
faltering re-attempt (he heard it at 1:33 as "junk footage") — **when Whisper
shows a stretched word inside a candidate take, LISTEN to the isolated span
before keeping it; a later take with internal silences loses to a clean earlier
take.** Rule updated: later-take-wins only when the later take is fluent.

## Graphics-placement lessons (LEARNING — append every Dan-directed placement)

Ad #1 rev-1 (2026-08-20), Dan's directed placements and the patterns behind them:
1. **Static photos are never left static** — he asked for motion on the shoot-photo
   run ("add motion effect so they're not static"). Default: Ken Burns (zoompan
   ~1.0↔1.09 over the window, alternate in/out per consecutive image) on EVERY
   still insert.
2. **A benefit enumeration gets one insert PER benefit** — "more attractive to
   women / men respect you / feel better-energy-health-live longer" got three
   clips, cut on the phrase boundaries. Pattern: when the script lists concrete
   life benefits, cover each with its own literal clip.
3. **A pain/struggle line gets a literal struggle clip** — "finding motivation is
   really hard" got an overweight-man-straining insert. Match the demographic
   (overweight, male) or it doesn't land.
4. **Stock-first sourcing works**: Pexels (free, no key needed —
   `https://www.pexels.com/download/video/<ID>/` curls straight to the CDN;
   search HTML greps for `/video/slug-ID/`). Dan's bar: stock if a GREAT clip
   exists, AI-generate only otherwise. Ad #1 filled all four slots from Pexels, $0.
5. **"Made it my phone lockscreen" beats want the goal image ON A PHONE** — he
   replaced a reused AI b-roll clip with a phone-mockup of the goal image
   (bezel + lockscreen clock + AI-GENERATED tag, slow push-in). Reusing the same
   AI clip twice in one ad was rejected the second time.
6. **Crop discipline on photo inserts: never cut the top of the head or the
   shorts line** — fit the whole figure on the J2 panel instead of cover-cropping
   (same rule as /coverimage).

Ad #1 rev-2 (2026-08-21), second round of directed placements:
7. **Ken Burns must be SUPERSAMPLED or it shakes.** zoompan on a ~2K input
   jitters (integer x/y rounding) and Dan called it out immediately. Recipe:
   `scale=7680:4320` before zoompan, output s=1920x1080 — verified smooth
   (consistent inter-frame diffs). Applies to every still insert and the opener.
8. **Benefit-clip casting matters as much as content**: the person must look like
   the PROSPECT'S GOAL (his future-self demo: ripped six-pack, late 30s/40s,
   matched ethnicity) — a generic fit person isn't enough, and an unclear
   emotional read ("she's just running away") fails. Each clip must legibly act
   out its sentence.
9. **AI-clip protocol when stock fails: start/end frames first for Dan's approval
   (nano-banana via `_shared/gemini-image.js`, ~$0.13/frame), then image-to-video.**
   Write both prompts to Step 4.5 (banned vocabulary, anti-default-person, frame
   slightly wrong) — it is cheaper than a regeneration.
   Replicate Kling drained mid-session (again); **Veo 3.1 Fast via the same
   GEMINI_API_KEY is the working fallback** (`:predictLongRunning`, image + prompt,
   6s/720p/16:9 ≈ $0.90/clip). Veo traps: `lastFrame` is NOT supported on the
   Gemini API (400 "use case not supported"); bikini/flirtation content trips the
   RAI filter — restyle the scene (sundress) and neutralize the prompt ("talk and
   laugh together"), retry; safety-filtered attempts are not charged.
10. **Never show an email-capture form in an ad** — Dan had the after-screen's
   email field hidden under an oversized black AI-GENERATED box (dual purpose:
   disclosure + hiding the ask). Cover the WHOLE form incl. its explainer text.
11. **The "AI reads your pictures" idea gets a custom animation, not a real app
   screen**: scan line sweeping the (tagged) after image once, then invented-but-
   coherent stats appearing (Current/Goal weight + BF%, fat loss, muscle gain),
   ending in "Recommended Workout Plan" as the bottom line, plan NOT revealed.
   Built as PIL frame-sequence → mp4 (`reference/ad1/prep_assets3.py`).
12. **End card → live product flow.** Dan replaced the static end card with the
   sample person's real flow: photo-in-generation-screen → generating → after
   alone (covered email box). Show prospects what they'll actually experience.
13. **Captions must clear graphics text**: per-event ASS MarginV override (field 8)
   lifts cues over an insert's on-screen text windows.

Ad #1 rev-3 (2026-08-21):
14. **A module that builds assets at import time WILL silently regress fixes.**
   prep_assets.py rebuilt ALL panels on every `exec_module` import from later
   asset scripts, restoring cover-cropped photos Dan had already rejected —
   the same defect shipped twice. Asset builders must guard their build loop
   under `if __name__ == "__main__":`; per-revision fix scripts write the final
   files LAST. Also: Ken Burns headroom — compose stills within the max-zoom-safe
   window (image ≤1650x900 on the 1920x1080 panel at 1.09x zoom).
15. **Never show the app's photo-crop screen in a demo** — start flows at the
   generation screen with the photo already in place (Dan, twice: mid-video and
   end flow). Demo-flow slices: appflow si=3.2.
16. **The stats screen pattern locked**: tag directly BELOW the after image
   (never covering it), stats, "Recommended Workout Plan" immediately after,
   then app-style teaser body text that describes where they're at and what
   it takes, without revealing the plan.

Modern-edit 60s sample (2026-08-21) — built to close the gap against the Upwork trial
edit; the reusable output is `_shared/motionlib.py` + `_shared/sfxlib.py`, and the
whole sample is reproducible from `reference/modern60/`:
19. **Graphics must MOVE.** Static PNG overlays are the single biggest reason our cuts
   read as cheaper than a Premiere-template edit. Every element now animates:
   `card_in` (scale 0.90→1.0 with a spring, ~0.42s), `bullets_build` (bullets appear on
   the word that introduces them), `lower_third` (chip slides, red strip grows out of
   it, statement wipes in), `title_card`, `callout_box` (stroke draws itself clockwise
   then breathes), `pop_text` (letter-by-letter snap). Alpha is carried by **QTRLE MOV**
   — libx264 has no alpha channel, and pre-multiplying against a guessed background is
   how graphics get grey fringes.
20. **Pause removal is a MEASUREMENT job, not a Whisper job.** Cut placement comes from
   a 5 ms RMS envelope of the real audio. Whisper timestamps a word up to 0.4s before
   any audio exists, and starts fricatives ("Fitness") before the /f/ — clamping cuts to
   its word bounds either eats onsets or blocks two thirds of the valid cuts. Whisper's
   only role is the re-transcription QC afterwards.
21. **Every pause cut needs cover, and a punch change is the cheapest cover.** Assign
   punch levels so their boundaries land ON the splices; the layout change masks the
   jump and doubles as pacing. Protect the hook completely (no splice in the opening
   line) — a micro-jump under a static overlay reads as a glitch, not an edit.
22. **A video panel gets rounded corners from a PLATE, not a mask.** Composite order:
   base → clip (square corners, filling the window) → `panel_plate` (opaque brand paper
   with a rounded hole punched in it, shadow baked around the hole). One static PNG per
   panel, no per-frame masking.
23. **Synthesise the transition SFX.** `sfxlib.py` generates whooshes/pops/risers from
   filtered noise and decaying sines — no account wall, no per-asset licence to track,
   and the timbre is tunable. Two cascaded band-pass stages, not one: a single 6 dB/oct
   skirt leaks enough broadband noise that a whoosh reads as hiss (centroid 7 kHz vs
   3 kHz). Mix them ~10 dB under the speech RMS; normalised one-shots summed raw land AT
   dialogue level and are jarring.
24. **PIL's 'lt' anchor is the ascender top, not the ink top.** A rule placed at
   `y + text_height` lands inside the glyphs — that shipped a strikethrough headline
   once. Position from `textbbox()[3]`. And scale a glyph in its OWN small tile:
   `scale_about` on a canvas-sized layer with an off-centre anchor translates the whole
   frame instead of scaling in place.

Modern-edit sample rev-2 (2026-08-22) — Dan: "the audio is still much worse than his":
32. **When a fix keeps not working, stop tuning and go measure the SOURCE.** Two rounds
   of EQ went onto a signal that was two microphones fighting each other. The tell was
   available the whole time and took one command: cross-correlate the two channels with a
   lag search. Strong peak at a non-zero lag = two mics, not stereo. Run it on every new
   roll (Step 0.4). → `_shared/audio/pick_lav.py` does this per file now.
33. **Check the stereo image of anything you deliver.** His voice measured +0.99 L/R
   correlation with the side channel 23 dB under the mid; ours measured −0.01 with side
   and mid EQUAL. That single number would have caught this on day one. A talking-head
   voice belongs dead centre — `pan=stereo|c0=c0|c1=c0` after the voice chain. → row 1 of `audio_gate.py`.
34. **An EQ match is only valid against the source you will actually ship.** Refitting
   after the channel fix reversed almost every band: the comb-filtered mix wanted +4.5 dB
   at 530 Hz and −3.2 at 4 kHz; the clean lav wants −4.6 at 320 and +4.6 dB of shelf
   above 3.5 kHz. A lav correction is always roughly "cut the chest bump, add the air".
35. **Fit across several windows of both videos, not one.** A single 4 s window put the
   mean error at 1.25 dB; the same chain measured over five windows each was 3.02 dB. The
   five-window fit is in `reference/modern60/fitvoice.py`.
36. **Locate a matching span in a reference edit by TRANSCRIPT, not by envelope
   correlation.** His cut removed different pauses so the offset drifts through the video,
   and a 2 s envelope window false-matched "the knowledge isn't the problem" 17 s out of
   place with a confident-looking 0.78 correlation. Whisper both tracks and search the
   word list (`reference/modern60/ab_audio.py`).
37. **Ship an A/B when the note is subjective.** "Sounds worse" is not measurable by
   argument — three sentences, his then ours, back to back, lets Dan settle it in 20
   seconds.

Modern-edit sample rev-1 (2026-08-22) — Dan compared our screens against the trial
edit's directly and picked HIS. These are the rules that difference came down to:
25. **A full-screen graphic is a solid brand FIELD, not a white page with a card on it.**
   Photographs sit straight on the field; the field IS the card. Type is bigger and
   heavier than feels right, leading is TIGHT (~0.95 body, 0.88 display), blocks are
   TOP-aligned not vertically centred, headings carry a solid accent rule at their own
   width, list markers are small filled SQUARES, and title-card headlines sit in an
   accent BAND in oblique caps. `motionlib.GREEN` is that system in J2 dark green with
   an olive accent; the brand red stays reserved for attention devices (callout stroke,
   lower-third strip) that sit over FOOTAGE rather than on a field.
26. **Measure the reference's design, don't eyeball it.** Cap heights, line advances,
   rule thickness and padding all came off his frames with a pixel scan, then got solved
   back into Manrope point sizes. Eyeballing had the title headline at 118 px when his
   was 145, and the panel bullets at 0.95 leading only because it was measured at 63 px
   advance. Half an hour of measuring beats three revision rounds.
27. **Grade-matching is a per-channel PERCENTILE fit, not a luma lift.** Rev-0 matched
   his average brightness and still looked worse, because it crushed blacks to
   `[0,5,0]` against his `[10,10,12]` and ran the blue midtone 22 levels under his.
   Sample p10/p50/p90 per channel on a face-sized crop of both, fit `curves=r:g:b`
   through those three points, and add NOTHING else — `eq=contrast` re-crushes the very
   black lift the curve just added, and `eq=saturation` is what made the mids too warm.
28. **"It sounds like there's echo" is a SPECTRUM problem before it is a reverb
   problem.** Ours measured 3 dB hot at 3.2–8 kHz (where room reverb lives) and 5.5 dB
   thin at 400–700 Hz (which makes a voice read as distant). Fix the tilt first, then
   add a gentle downward expander for the tails, then light compression if the reference
   is "flatter" (LRA 3.8 → 1.9 LU here). Note the presence lift we had been adding at
   3.6 kHz was making the room WORSE. → the gate's tone, dryness and EDT rows; `voice_chain.py` dereverbs when EDT > 55 ms.
29. **Re-transcription is the audio QC, and it earns its keep.** An expander at
   threshold 0.030 / ratio 2.4 ate the /f/ in "for free" and the "n't" in "isn't" —
   inaudible in a spot check, obvious as 97.9 % → 96.0 % fidelity. After fixing that,
   the same test caught the music bed masking "isn't" until the sidechain release went
   to 420 ms. Never ship an audio-chain change without re-transcribing the finished mix.
30. **PIL: measure with the anchor you draw with.** `textbbox()` defaults to `la`
   (ascender); every draw call here uses `lt` (top of ink). At a 145 px headline that is
   a 48 px error, and it put a title headline straight through the top edge of its own
   accent band. Related: `oblique()` must shear about the TEXT's centre — shearing a
   canvas-sized layer about the canvas centre translates the line sideways by
   `k * (centre - y)` and pushed the headline off the right edge of the band.
31. **"Where I'm at today" wants the SHOOT PHOTOGRAPHY, not workout b-roll** (Dan,
   2026-08-22). The finalised social photos are the proof; a plank clip is just motion.

Ad #1 rev-4 (2026-08-21):
17. **AI-GENERATED tag placement differs by insert type.** On a FULL-FRAME AI
   clip (no panel background, the clip fills 1920x1080) a centered tag sits mid-
   frame and blocks the subject — Dan called this out at ~2:00. Fix: upper-left
   corner (overlay 40:40) at 1.5x size for full-frame AI inserts. PANEL-style
   inserts (phone mock, crude-photoshop clip — a clip scaled to <1920 width on a
   background panel) keep the original centered small tag; nothing is blocked
   there since the clip doesn't fill the frame. Decide by insert type (`wid==0`
   in layout2.py's VID list = full-frame), not by clip content.
18. **A stock clip that isn't a literal match to the script line gets replaced,
   not kept as "good enough."** The tire-flip clip at 0:46 illustrated a fit
   goal, not the "finding motivation is hard" pain point on screen at that
   moment — Dan wanted the demographic-matched struggle clip (lesson 3) instead,
   even though a fit-guy tire flip is visually strong on its own.

Ad #1 rev-5 (2026-08-23) — Dan: *"still not as good as the one Muhammad made"*, with the
editor's new 2:33 cut and **the revision doc Dan had sent that editor** as the brief. The
whole build is reproducible from `reference/rev5/` (beats → gfx → layout → audio → captions
→ qc). What it added to the system:

38. **Anchor every beat to a PHRASE, never to a second, and search AFTER a time.** The tight
   cut's timeline moves the moment a pause parameter changes, so hardcoded anchors drift off
   the words they were placed on. Two traps in the lookup itself: Whisper tokens carry a
   **leading space** (`" this" != "this"`, so `.strip()` in the normaliser), and an ad script
   repeats whole phrases — "tap the button below", "phone lock screen", "stressful life" —
   so a naive search matches the FIRST occurrence and yields beats with negative duration.
   `reference/rev5/beats5.py` asserts every beat has positive duration for exactly this reason.
39. **Grade-match on SKIN PIXELS, not on a fixed crop.** Rule 27's percentile fit assumes the
   two videos frame the subject alike. The reference edit is already punched in, so its centre
   crop is nearly all face while ours still contains the dark doorway — fitting that way lifted
   our shadows into haze chasing his skin values. Select skin pixels in both (r>g>b, bounded
   r−b) for the mid/high control points and take the black point from each video's own global
   p1: skin error 23.2 → **5.1 levels**, and the black point landed on his exactly (4/4/2).
40. **PIL ignores EXIF rotation and iPhone photos rely on it.** A sideways portrait reached a
   finished graphic before `ImageOps.exif_transpose` went into `motionlib.fit_cover/fit_contain`.
   Any photo that came off a phone must be opened through that path.
41. **Count the beat's seconds before choosing how many stills go in it.** Four photos in a
   1.8 s beat is 0.44 s each — a flicker, not a montage. Two landed there and the other two
   moved to the line that was literally about how he looks now, which also filled a bare stretch.
42. **A retimed insert needs its own source length.** `-t` defaulted to the beat length while
   `setpts=PTS/3` demanded three times that, so a third of the intended footage played and
   nobody would have seen it in a QC that only checks the beat is covered.
43. **Panels need an edge on a near-black field.** `panel_plate` bakes a drop shadow, which is
   invisible on (13,14,11) — a white app screenshot read as a floating rectangle with hard
   corners until an olive hairline was drawn round the hole.
44. **Whisper shells out to a bare `ffmpeg`.** Put the static build on `PATH` inside the script;
   inheriting it from the calling shell fails the moment the script is backgrounded.
45. **Read the whole of any clip Dan links before trusting his in/out points.** The app
   recording for the 1:09 revision ends on the "Meet the new you" BEFORE/AFTER screen (from
   25.25 s) and an email-capture screen after it — both banned. His stated 0:03–0:26 would have
   shipped the violation; the usable window is 3.0–24.9 s.
46. **Suppress captions over full-screen cards and app screens rather than dodging them.** A
   card already carries a headline, and the product demo's UI text is the part of an ad that
   matters most. 56 of 164 cues dropped; the remaining ones shift right over the bullet panels
   and lift above the lower thirds.
47. **The QC blind spot repeats: check what "covered" means before believing a FAIL.** Two
   splices reported bare were under a Ken Burns card and an app-flow card that the covered-list
   simply omitted. Third time this class of error has been the metric, not the media.
48. **Music picked by measurement.** Score candidates on spectral distance to the bed under the
   reference edit (sampled in its quietest window) plus energy flatness over the needed length —
   `reference/rev5/pick_bed.py`. Pixabay's licence needs no attribution, which a CC-BY track
   would have forced into a paid ad.
49. **Veo rejects generated faces as "celebrity likeness".** Reprompt the still for an
   explicitly ordinary, non-model face ("deliberately NOT a model, NOT anyone famous", amateur-
   photograph realism). Filtered attempts are not charged.

Measured against the reference edit: **3:55.3 from 4:31** (112 pause cuts, 30.1 s removed,
**198 wpm** against his 203), −14.10 LUFS, −1.30 dBTP, L/R correlation **+0.9986** with the
side channel 31.5 dB under the mid (his: +0.99 / 23.0 dB), script fidelity **98.6 %**.

Ad 3 (2026-08-27) — "Stop wasting money on personal trainers", the first ad cut to the rev-5
standard from a roll the reference editor never touched. Reproducible from
`/Volumes/Extreme/_edit_work/ads234-8-14/c1593/`. **QC 12/12, then the watch pass found three
real defects the metric gate had passed** — which is the whole argument for the watch pass:

50. **A looped image input defaults to 25 fps. Pass `-framerate 30000/1001` on EVERY
   `-loop 1` input.** Against a 29.97 fps timeline the two frame grids drift, and at the
   output frames where they diverge the overlay drops the still for ONE frame: the plate
   vanishes and whatever it was covering is exposed. That is how the app's **email-capture
   form reached the delivered picture** with the disclosure correctly built, correctly
   sized and correctly enabled. Proven by A/B on the exact failing parameters — 25 fps
   exposes one frame, `30000/1001` exposes none; plate padding and overlay lead changed
   nothing. This affects every plate, tag and Ken Burns still in `layout*.py`.
51. **A compliance gate that SAMPLES cannot see a single-frame violation.** The
   banned-screen scan ran at 2 fps and reported a clean 0.647; the same scan at full frame
   rate reported **1.000 at 179.41 s**. Any check for a banned pattern runs on every frame.
52. **`card_in` animates its entrance and then HOLDS.** The photo and CTA cards sat
   dead-frozen 2.4–8.7 s, which is Dan's rev-1 note 1 verbatim. Every card now carries a
   continuing Ken Burns drift (`scale_about` on the finished layer, alternating in/out on
   consecutive stills); frozen runs went 16 → 7 and all survivors are the real app
   recording's own holds. Verify on the alpha MOV itself and check the **longest identical
   run**, not just runs ≥8 frames — a 3.8 % drift over 9.7 s changes the integer layer size
   only every ~4 frames, which passes an 8-frame freeze test and is still imperceptible.
53. **Caption from the TIGHT word list, not from a fresh pass on the finished mix**, whenever
   the audio stage does no retiming (a `-c:v copy` mux). Measured here: the two agree to
   **+22 ms median with no systematic offset**, but `small.en` over the mix DROPS PUNCTUATION
   and mishears ("personal trainer" for "trainers", "gonna" for "going to"). Punctuation is
   what tells the chunker where a sentence ends, so captioning off the mix split cues
   straight across sentence boundaries ("...personal trainer AI has"). Keep the mix
   transcription for QC — that is what it is actually good for.
54. **Clip a caption at a card boundary; never drop it.** Dropping every cue that merely
   touches a suppression window deleted real words and made the next caption open
   mid-sentence ("of dollars on personal...").
55. **`bullets_build` draws its heading on ONE line with no wrap**, and its accent rule is
   drawn at the heading's own width — an over-long heading runs across the video column onto
   Dan's face. Measure every heading against `panel_w - 2*PAD` (794 px at panel_w=980,
   head_size=76) before building. Three of five failed on first write.
56. **Whisper silently drops an abandoned re-attempt** and stitches the surviving halves into
   one clean-looking sentence — the transcript reads fine while the audio stutters. Scan for
   speech energy that no word interval covers (`orphan_scan.py`). One hit in this roll: a
   whole abandoned sentence that would have shipped.
57. **A roll's noise floor identifies the bad take.** Dan's own "did that plane pick up?" is
   measurable — the flagged take's floor is −41.6 dBFS with the 20–200 Hz floor at −13.3 dB,
   against −45.3 / −20.2 on the retake and ≈−48 dB everywhere else on the roll.
58. **A grade fitted for one roll of a shoot transfers to its siblings — but fit the GAIN
   first.** Raw C1593 measures within 3.8 levels of raw C1591 on skin percentiles, yet the
   same chain landed 15.3 levels off, because the curve is steepest exactly where they
   differ. A **1.13 linear pre-gain** (`colorlevels`) into Ad 1's approved chain lands **2.4
   levels** from the shipped look. Refitting a fresh 6-point spline instead reached only
   16.7 levels — a large correction overshoots through sparse control points. Prefer
   gain-then-approved-curve over a fresh fit.
59. **Parallelise the graphics build.** 22 alpha MOVs at ~3 min each serially; four workers
   over an explicit partition finished all of them in 90 s. `_skip()` makes the partition safe.
60. **Preview composited on a real frame at NATIVE resolution.** A 420 px preview made the
   app-screenshot panel look illegible and nearly bought a needless re-render; at 1080p the
   body copy reads cleanly. Fourth time the metric has been wrong rather than the media.
61. **Native-vertical assets go in a PLATE, never cropped to 16:9.** A 16:9 crop of a
   1080×1920 clip keeps 32 % of the height and cuts heads off. Size the plate hole to the
   clip's own aspect (574×1020 for 9:16, 1264×1000 for the 4:3-ish archive clip) and let the
   olive hairline give it an edge on the near-black field.

Ad 2 (2026-08-27) — "Stop paying human nutritionists", cut from C1592 straight after Ad 3:

62. **WHISPER SILENTLY DROPS WHOLE TAKES AND THE TRANSCRIPT LOOKS CLEAN.** On C1592 the
   default pass (`condition_on_previous_text=True`) fed the previous window back as a
   prompt and the decoder skipped a **complete second hook take** (32.2–46.9 s) as
   "already said", emitting one word in its place. Setting it False fixed that and then
   dropped the **third take of the close** instead. Neither pass alone is complete.
   **Transcribe every ad roll with `reference/whisper_chunked.py`** — overlapping 70 s
   windows stepped 60 s, each decoded with fresh short context, words kept only inside
   their own span, plus a seam de-dup (the same word can be timed 119.9 in one window and
   120.1 in the next). Result on C1592: 0 orphan speech runs, against 17 and 15.
63. **`reference/orphan_scan.py` is the completeness proof, and it is not optional.** It
   flags any run of speech-level energy that no word interval covers. It is what exposed
   the missing hook take, and on C1593 it found the one real defect in that roll — an
   abandoned re-attempt Whisper had stitched over, which would have shipped as a stutter.
   Run it after transcribing and before building the EDL. Zero orphans = complete.
64. **Force punch boundaries on the splices that are MEASURABLY visible, before rendering.**
   `reference/hard_splices.py` measures the frame difference across every pause-removal
   splice on the tight cut and reports the ones above the file's own p99 control. Intersect
   that with "not under a graphic and not already a punch boundary" and force those. On
   Ad 2: 135 splices, 76 measurably hard, 37 uncovered, and only **22** were both — 15
   after a 1.6 s floor. Covering all 37 would shred the pacing; covering none shipped four
   naked jump cuts that QC caught only after a full render. This is the cheap version of a
   failure that otherwise costs 35 minutes.
65. **The retime field is a source OUT-POINT, not a duration.** Passing the wanted length
   where the code expects "usable until" gives `avail = 10 − 30 = −20` and ffmpeg dies on
   `setpts=PTS/-2.36`. And clamp the rate to ~[0.85, 1.60]: a 5 s AI clip stretched over a
   10.6 s beat is 2.1× slow motion and reads as a glitch. Play it near real time and hand
   the rest of the beat back to Dan — which is the better edit anyway.
66. **Two QC checks were wrong for a second ad, not the media** (this keeps happening —
   count it). The AI-label check asserted "≥3 tagged inserts", which is an Ad-3 fact, not a
   rule; the requirement is that every clip from the AI library carries a tag, so assert
   that instead. And the caption/card collision check failed on a 4 ms overlap that is
   pure ASS centisecond quantisation — a tenth of a frame. Give it 0.02 s of slack.
67. **Launch a background render in ONE Bash call and wait in a SEPARATE one.** Combining
   them means the harness's timeout kills the whole process group, and a caption burn died
   mid-write leaving a 208 MB file with no moov atom.

Ad 4 (2026-08-27) — "Stop wasting money on supplements", C1594, third of the batch:

68. **The forced-punch set must be computed WITHOUT reference to the punch plan**, because
   the plan is built from it. Testing "is this splice already near a boundary" against the
   previous iteration's plan makes the result oscillate: a splice that was covered becomes
   bare once the plan shifts, and QC finds it after a 35-minute render. Compute
   hard ∩ uncovered, apply a spacing floor, done — one pass, converges.
69. **The spacing floor is a real trade-off, so measure the result.** 1.6 s left two visible
   splices bare on this ad; 0.8 s caught everything at the cost of one 0.36 s framing
   segment. Check the resulting median hold (2.97–4.04 s across these three ads) against the
   reference's 4–7 s and look at the short segment in the watch strips before accepting it.
70. **A splice within ~4 frames of an insert boundary is masked BY that boundary.** QC's
   0.05 s tolerance reported a splice 53 ms after an insert ended as "bare", when the
   insert's own exit is the biggest visual event on that frame. 0.15 s is the honest number.
71. **`plate=None` means FULL FRAME.** Native-16:9 stock is a downscale and should fill the
   frame; only native-vertical assets need a plate. Keep both paths in `layout*.py`.
72. **Do not fake a cue the doc says is missing.** Ad 4's own cue notes the Supplement Audit
   RESULT screen needs a real photo of Dan's shelf run through the feature and that "nothing
   here is faked". The ad ships without that beat and `notes.md` says so, which is the
   correct outcome — an invented result screen would be a fabricated product claim.


Website conversion video (2026-09-01/02) — the post-generation video on absbyai.com, cut from
the 8/28 shoot (C1650+C1651) to a TRUST brief: no fast cuts, nothing flashy, the last thing a
visitor watches before they buy. Reproducible from `reference/website-video/`. What it added:

73. **A trust cut is the same pipeline with the dials turned down, not a different pipeline.**
   Three punch levels, 9 s minimum hold, pauses shortened to ~0.30 s instead of 0.16 s, cards
   that fade over 0.5 s and drift slowly, no SFX bed at all, music at −23 dB. Every insert is
   REAL: the actual macro-tracker recording, the real trainer/meal-plan/brief screens, Dan's
   real photos, one AI image (his own goal image) tagged. Dan stays on screen beside every
   phone panel (panel LEFT, Dan in the right column) — the product and the person together is
   the trust device. Coverage 54 %, Dan fully replaced only 16 %.
74. **The 8/28 shoot is S-Log3 / S-Gamut3.Cine 4K with FOUR mono audio tracks.** No prior
   grade transfers. `make_lut.py` builds a 33³ .cube in numpy (Sony's S-Log3 transfer →
   linear, the S-Gamut3.Cine→Rec709 matrix in linear, a soft shoulder, the 709 OETF) and
   `lut3d=...:interp=tetrahedral` applies it; exposure 1.45× and `eq=saturation=0.88` were
   picked against the approved Ad 3 skin. **The lav is a:1** (SNR 40 dB); a:0 is the far mic,
   7.2 ms late, polarity inverted; a:2/a:3 silent. `-map 0:a:1`, never `-ac 1`. → measured per file by `pick_lav.py`; `base.py` reads its JSON.
75. **Render the base at 2560×1440 when the source is 4K.** The 1.30 punch of 1440p is
   1969 px wide, so no framing level ever upscales; the cost is ~1.8× the base encode.
76. **`loudnorm` fell back to DYNAMIC on this mix and the JSON said so.** −19.3 LUFS in with
   TP −1.8 cannot reach −14 / −1.5 linearly. `audio2.py` is the replacement: measured gain +
   `alimiter`, the limiter's delay MEASURED by cross-correlation (239 samples here, not the
   remembered 219) and trimmed, then ebur128 on the result. Set the limiter low enough for
   the AAC overshoot (0.71 → −2.2 dBTP on the delivered file). → the finish stage of `_shared/audio/voice_chain.py`.
77. **Previewing a QTRLE alpha .mov with `-ss` + `overlay` onto a single PNG shows NOTHING and
   looks like a broken graphic.** The still base has one frame at t=0 and the seeked overlay
   never lines up. Extract the graphic frame to RGBA PNG and composite in PIL instead —
   `pv/preview_sheet2.jpg` is the pattern. Cost 20 minutes and nearly a needless rebuild.
78. **Assert panel-heading width before building** (`ml.text_size(heading.upper(), font(68,
   'ExtraBold'))[0] <= panel_w − 2·PAD`). "A plan you can actually follow" measured 1215 px
   against a 794 px limit and ran straight across Dan's chest in the preview; even "A plan you
   can follow" (851) failed. Lesson 55 as a one-line assert, so it cannot recur.
79. **A card the video ENDS on must not fade out.** `card_in`'s default out-fade exposed the
   talking head for the last 0.36 s — visible only on the watch pass's final frames. `hold=True`
   in `_card` sets `out_dur=0`; the website's button sits under the player, so ending on the
   CTA card is the design.
80. **Thin hard splices HARDEST-FIRST inside the spacing floor.** With a 3.5 s floor, first-come
   ordering covered a 1.2-diff splice at 50.35 s and left the 2.62 one at 51.08 s bare. Sort
   the candidates by measured difference, accept greedily against the floor.
81. **Two-roll EDLs: `edl.py` anchors spans by phrase per roll and validates every edge against
   a −40 dB envelope**; `base.py` takes N sources. The price line was re-read on the second
   roll after Dan caught the script's `$[X.XX]` on camera (`"$20 … I forgot to put that in the
   script"` → `$19.99` on C1651) — take the correction, cut the slip.


Website conversion video rev 1 — REJECTED 2026-09-02 (audio, framing, graphics, in that order).
Handoff for rev 2: `Handoffs/handoff-20260902-website-video-rev2.md`. Standing rules that came out
of it, all three of which now fail a build rather than living in prose:

82. **NEVER SHIP THE FULL WIDE FRAME FROM THE KITCHEN SET, AND NEVER A LEVEL THAT SHOWS THE LIGHT.**
   Dan: "I don't want to use this wide shot ever… this was shot in 4K intentionally from far away so
   we have room to punch in." The widest allowed level is top-of-head → shorts with the counter
   barely visible (1.256× on the 8/28 set: 3058×1720 @ (451,40)); the tight level is head → navel
   (1.66×). The studio light sits at x>3560 in the 4K frame — any crop reaching it is a defect.
   Render the base at full 4K so the tight level never upscales. `layout.py` asserts the crop
   never exceeds the widest level and never crosses the light.
83. **GRAPHICS SPARINGLY, AND NEVER ON A BLACK FIELD WITH ONE SMALL ELEMENT.** Dan on the J2AD
   phone panels and bullet panels: "a graphic on the left and a huge amount of black space… just a
   bunch of text, generic… horrible." Rule: no graphic with more than ~40 % empty field; an app
   screen goes NEXT TO DAN over the footage (a phone-shaped inset in a slightly wider crop), not on a
   plate; when a full-frame card is used it fills the frame the way Muhammad's title cards do. His
   panel field is the mid-olive gradient (`orglib.py` / `motionlib.MIL`), not near-black.
84. **IF A FEATURE LOOKS LAME ON SCREEN, DON'T SHOW IT.** The trainer workout screen with stick-figure
   exercise icons was called "awful". The choice is not "which screen" but "screen or Dan"; Dan wins
   unless the screen is genuinely good. Before/after and body-fat stats live on the viewer's own
   screen for the website video — the script says "look near your image".
85. **"How I look today" = Muhammad's four photos**, `00 ASSETS USED IN THE REFERENCE AD/04–07`, in
   sequence, never side by side with the before picture. The before picture goes ON "I've been out
   of shape" and nowhere near a line about being lean.
86. **The audio complaint will be described as "the two-channel issue" whether or not it is one.**
   Measure first (Step 0.5). Comb filter = L/R correlation near 0 with a 7–8 ms lag peak; floor =
   voice-over-floor per band; tone = the 10-band fit. Three different fixes, one word from Dan.


Website conversion video rev 2 — delivered 2026-09-02, the same day rev 1 was rejected. Audio gate
PASSED on the delivered file (tone 0.80 dB mean / 2.10 max vs his ad; floor +2.6 / +0.3 / +0.6 dB vs
his), QC 14/14, watch pass clean, $0.00 spend. Reproducible from `reference/website-video/` (rev-2
scripts; rev 1's are in its `rev1/`). What it added:

87. **Fit the EQ against the GATE'S OWN metric, iterate, and stop at the smooth iteration.**
   `voicefit.py` copies `voice_ref_check.py`'s analysis and iterates 10 parametric bands (they
   interact — one pass leaves 2.9 dB at the top band). Iteration 2 passed (0.76 mean / 1.06 max);
   iteration 6 reached 0.30 only by alternating +4 / −3.4 / +1.5 / −7.4 / +1.7 / −5.2 on neighbouring
   bands — an over-fit comb, not a voice EQ. A hand "+1.2 at 950 Hz" on top made the max error worse
   (1.06 → 1.69). Ship the first smooth passing curve.
88. **The bed is a floor problem, and every 4 dB of bed is ~2.5 dB of floor.** The bed file is
   −9.5 LUFS against a −22 LUFS voice, so rev 1's "−23 dB" sat 10 dB under the voice and 9.5 dB over
   his floor. Measured: −30 fails by 8 dB, −34 by 5.6, −40 passes 1.9 dB dirtier than his, **−44 lands
   on his floor**. State the bed as dB below the VOICE's integrated level (34 dB here), never as a
   volume on the file, and let the gate pick it.
89. **The loudness finish costs floor too.** +9 dB of gain into the limiter took 0.5–2.6 dB off
   voice-over-floor (premix +8.8 / +5.4 / +3.8 → finished +8.3 / +3.8 / +1.2, no bed). EQ alone does
   not move the ratio (it scales voice and floor together in-band); makeup, limiting and the bed do.
   Run the gate on the FINISHED file — the premix passes things the master does not.
90. **Measure the reference's cards; do not inherit a description of them.** The handoff said his
   photo cards put Dan in the other half of the frame. A pixel scan of his native frames showed
   FULL-FRAME plates — 1476×924 on 1920×1080, photo inset 28 px, plate (66,76,37)→(80,89,49) on a
   (10,11,5) grid field, title plate 1497×764 with ~142 px oblique caps at 0.88 leading — and his
   phone splits at ~475×922 with Dan filling the right half. That is why his cards never read as
   "one small element on black": the plate IS the frame. `gfx2.py` is that system.
91. **Framing levels are code.** `layout.py` asserts every crop is no wider than the widest allowed
   level and ends before the light (first bright pixel measured at x=3672 on two frames; guard 3530),
   and `qc.py` re-asserts it on the plan. Two traps on the way: crop widths must be even (2311
   failed), and the alternation counter must advance exactly once per segment — the rev-1 pattern
   double-stepped into MID/WIDE/MID/WIDE with no TIGHT for the first minute.
92. **Before → Dan → after needs an explicit gap.** Dan's note put the before photo on "out of
   shape" and the after photos on the very next clause; the beat sheet's 0.35 s merge rule would have
   crossfaded the two cards into a superimposed before/after for 0.4 s. End the before card 0.5 s
   before the after card, so Dan is on camera between them.
93. **A phone beside Dan in the footage is one alpha MOV**: the recording through a rounded-rect
   mask (`alphamerge`), onto a transparent `color` source with `overlay=format=rgb`, then a
   hairline+shadow plate PNG, `fade=…:alpha=1` at both ends, QTRLE argb. `layout.py pip` builds it
   and `mix()` overlays it like any card. Size it like his (433×820 at 1080p), Dan pushed to 65 %.
94. **A contact sheet made with `fps=1/N` and `%{pts}` labels lags the content by ~N/2 s.** Tile
   "0:40" showed a card's fade-out that happens at 42.5–42.9 s, "3:35" showed a card that starts at
   216.45 — three false alarms in one review. Grab suspect frames with exact `-ss` before calling
   anything a defect; `deliver.sh` now builds the sheet from exact grabs.
95. **Reusing a rev-1 graphic requires its beat to be unchanged — ffprobe it.** Five of the six
   lower thirds matched; `num2.mov` was 0.15 s short of its rev-2 beat (rev 1's beat sheet had
   trimmed it against a neighbour that no longer exists), which would have repeated a transparent
   last frame for four frames. Assert `|mov − beat| < 0.1 s` for every reused MOV before the mix.
96. **Concurrency held at two builds all session** by putting the long chain in the background with
   a process waiter (`wait_stage2.sh`: `kill -0 PID` loop, hard timeout, grep for the wrapper's
   RENDER COMPLETE line, then launch the next stage) — the audio fit, card previews and script work
   ran in the foreground while the 4K base (29 min) and the 4K tight (~25 min) encoded.


Website conversion video rev 2 — REVIEWED 2026-09-02: **audio approved** ("you got it nailed. This is
the audio that we want"), rejected on headroom (every shot), one repeated line, and captions colliding
with every lower third. Handoff for rev 3: `Handoffs/handoff-20260902-website-video-rev3.md`. Standing
rules from it, each of which must be a measurement or an assertion, not prose:

97. **ANCHOR EVERY CROP TO THE MEASURED HEAD, NEVER TO THE FRAME.** Rev 2's levels were top-anchored
   at y=40 from a grid frame that read the head top at y≈100; `reference/website-video/headtrack.py`
   measured the real head top every 0.5 s across the cut at **296–340 px** (median 336) — that frame
   was not in the video. Result: 168–232 px of headroom at 1080p, worst on the tight level, which is
   Dan's "very, very bad crop." Rule: per punch segment, `y0 = segment_min_head_top − 0.03 × crop_h`;
   the head top lands ~30 px from the top edge in every level; the bottom edge goes as low as the
   zoom allows (shorts and counter visible on the wide level). **QC asserts the headroom on the
   DELIVERED frames** (head top within 15–60 px of the top, never cut). One reference frame is not
   the video; measure the whole cut. Detector caveat: when he looks down the skin test misses and the
   value jumps — use the per-segment minimum, misses only go down.
98. **A STRETCHED WORD IS A HIDDEN RESTART UNTIL PROVEN OTHERWISE.** Whisper stitched "Now, I've been
   out of shape, — I've been out of shape, and now at 40" into one 1.75 s `and`, and `orphan_scan.py`
   passed because the stretched interval covered the energy. Dan heard the repeat at 0:32. Run
   `reference/repeat_scan.py` (words > 0.7 s, repeated 4-grams within 25 s) after every transcription
   and before the EDL, and re-transcribe every flagged span IN ISOLATION (4 s window, medium.en,
   `condition_on_previous_text=False`). Cut the first attempt, keep the fluent restart.
99. **CAPTIONS NEVER OVERLAP A GRAPHIC — measured in pixels, asserted in QC.** All six lower thirds
   sat at y 757–905 and the "lifted" captions (MarginV 300) inked at 727–806: 49 px of overlap on
   every lower-third beat, and QC only checked captions against full cards. Dan: "move the graphics
   down so they don't overlap with the captions. Let's make this a standing rule." Lower thirds sit
   at the bottom (box ≈852–1000), captions lift above them (`MV_LIFT` from the measured ink bottom:
   ink bottom ≈ 1080 − MarginV + 26 → 290 for ≥30 px clearance), and QC renders the ASS over black at
   each lifted cue and asserts a ≥20 px gap to the lower third's alpha bbox, plus no ink inside the
   phone box. Geometry you assumed is not geometry you measured.
100. **When a revision passes every gate and still gets rejected, the gate was measuring the wrong
   thing.** Rev 2 passed 14/14 and a clean watch pass; none of them measured headroom, caption
   clearance to lower thirds, or restarts hidden inside a token. Each review adds the check that
   would have caught it — that is how this skill scales out of Dan's eye.


Website conversion video rev 3 (2026-09-02, same day) — the three rejected items rebuilt from the
handoff's measurements; audio chain untouched. Reproducible from `reference/website-video/`
(`rev3.sh` is the whole chain). Both new checks were run on rev 2's delivered file FIRST and failed it
(caption gap −47 px on 21 cue/graphic pairs; headroom 159–261 px, median 201) — that is the proof a
new gate is measuring the right thing before it is trusted on the new render.

101. **Fix a stitched restart in the TRANSCRIPT first, then cut — and DROP every word inside a removed
   span.** `to_tight()` collapses a word that sits inside a removed span onto the splice, so the first
   attempt's five words would have captioned the cut line twice; the dry run showed it before any
   render. `tx_patch.py` splices the isolated medium.en pass's words into the roll JSON (the first
   word keeps the envelope onset; the restart's first word takes the measured −40 dB rise, 0.15 s
   after Whisper's start), `tight.py` `MANUAL_CUTS` takes a BASE-time span with both edges asserted
   against the envelope, absorbs the pause cuts inside it, and drops the words. Set the patch window's
   edges BETWEEN the last token to replace and the first to keep — a window ending at 51.95 removed the
   "I" at 51.90 and the isolated pass's "I" at 52.14 fell outside it. A dry run (`RENDER=0`) that
   prints the words around the cut costs seconds; a render that captions a ghost word costs an hour.
102. **Track the head on the BASE, not on the tight cut, and key the track to the keeps.**
   `headtrack.py` samples `base.mov` at 4/s and maps each sample through `tight_cuts.json`; a re-cut
   needs no re-extract, and `layout.py` asserts the track's keeps signature at import so a stale
   track fails the build instead of framing the video. 982 samples, 0 without a detection, head top
   min 296 / median 340 (4K px). Validate the detector on the TALLEST frames, not just a random
   sheet — `pv/headtrack_tallest.jpg` is what proves the per-segment minimum is a head and not wood.
103. **A fixed crop can hold the headroom at his TALLEST instant, not on every frame — assert what the
   crop controls.** Anchored to each segment's minimum head top, the head sits ~33 px below the edge
   at his tallest and the rest of the spread is his own posture inside the hold (up to ~50 px of 4K in
   10–15 s). A crop that followed the slouch would cut his head when he stands up. So the gate is:
   ≥15 px on every valid frame (never cut), per-segment minimum ≤45 px (the crop IS anchored), median
   ≤60 px, ceiling 90 px — not "60 px on every frame". Look-down misses only ever read LOW, so a
   sample is valid when it is within 40 px of the ±1.5 s minimum; print the rejected count.
104. **Measure caption clearance by rendering the cue ALONE, retimed to t=0, over GREEN.** Rendering
   the whole ASS over lavfi black at the cue's real time decodes minutes of frames per cue, and over
   black the outline and shadow are invisible to a bbox — the ink measures ~6 px smaller than what the
   viewer sees. Green frame, bbox of everything not green, against the graphic's own alpha bbox at
   three points across the cue (the lower third is still growing in at its first frames); assert
   ≥20 px wherever they overlap horizontally. The fix itself: `motionlib.lower_third_bar(bottom=1000)`
   (plate 878–1000, alpha incl. its shadow 858–1044) and `MV_LIFT=290` (ink bottom 795, two-line cues
   grow up to 668): 63 px clear.
105. **A cut shrinks the card that sits on the cut line — re-plan the beat, don't just rebuild the
   MOV.** BEFORE went 2.6 → 1.8 s. Fades 0.30/0.30, card out by "and" (Dan: never let the before
   picture run into "and now at 40"), Dan on camera for "and now at 40," (1.1 s), and TODAY moved
   from "now at 40" to "I have the most defined abs" — the claim the four photos prove. `beats.py`
   asserts ≥0.5 s of Dan between the before and after cards, so the merge rule can never crossfade
   them. This was a judgment call and is flagged as such in the delivery.
106. **The head track must be measured at the DELIVERED scale too, and the crop takes the minimum over
   both.** The first rev-3 render passed 17 of 18 checks and failed its own headroom floor: 7–11 px in
   three TIGHT holds, hair on the edge, although the base-sampled track had placed the head 33 px down.
   Two causes, both structural: the delivered check samples at a different phase, and its narrower
   band (the same physical width the QC uses) reads the crown a few rows higher than the 90-px band on
   the 4K did. `headtrack_refine.py` runs the QC detector on `punched.mov`, maps every head top back
   into 4K through that segment's crop, and stores them under `refine`; `layout.py` merges both tracks
   before the per-segment minimum. Segment anchors moved 3–34 px (4K); the two near-cut holds by 34
   and 29. The plan → render → measure → refine → render loop can only move a crop UP, so it converges
   in one pass. Rule: the sampler that gates the delivery is the sampler that anchors the crop.

## Decisions locked vs pending

| decision | status |
|---|---|
| Script = ground truth; spoken corrections win; flag drift | LOCKED (2026-08-20) |
| Take selection: Dan first minute, Claude rest, learn toward full handoff | LOCKED |
| 16:9 primary + 9:16 secondary this batch; both must be strong | LOCKED |
| Cut whole script, no ceiling | LOCKED |
| No 1.2x pass, no hook variants (for now) | LOCKED |
| Music bed ON for filmed ads, CC0/Pixabay (no attribution), chosen by measurement | LOCKED 2026-08-23 (Dan) |
| Persistent CTA bar DROPPED for ad 1 rev-5; burned captions KEPT | Dan, 2026-08-23 |
| Paid-ad graphics palette = `motionlib.J2AD`: black field, olive/dark-green headers, white body | LOCKED 2026-08-23 (Dan's revision doc) |
| Minimal graphics first; Dan directs placements; learn | LOCKED |
| Negative-imagery scan; remove certain violations, flag unsure ones | LOCKED |
| NO before/after anywhere, incl. in-app UI; before → other → tagged after | LOCKED (2026-08-20, Dan's #1) |
| Style: J2 graphics + CTA bar, MadMuscles captions, "abs" lowercase | LOCKED (2026-08-20) |
| "Results are not guaranteed" micro-disclaimer (photo run + end card) | shipped on ad #1, not vetoed |
| CTA bar exact copy/geometry per style | ⏳ ad #1 |
| CONTENT style (YouTube episodes): see `/longform-edit` Step 7 and `reference/HOUSE_STYLE.md` there — the palette is `motionlib.MIL` (military green, Dan's 2026-08-24 revision), NOT `GREEN` | LOCKED 2026-08-24 |
| (superseded) CONTENT style: the trial edit's screen system — solid brand FIELD, big heavy type, tight leading, top-aligned, accent rules/bands — in J2 dark green with an olive accent (`motionlib.GREEN`); no captions | Dan chose his structure over our bright-paper version, 2026-08-22 |
| Airtight pause removal + music bed + transition SFX for CONTENT cuts | proposed 2026-08-21, not queried in rev-1 notes |
| Grade CONTENT cuts by per-channel percentile fit to a reference, not a luma lift | LOCKED 2026-08-22 |
| Voice chain: EQ-match to the reference, gentle expander for room tails, light compression | LOCKED 2026-08-22 |
| Music: track choice is a measured decision (least mid-band energy, flattest energy over the needed window); CC-BY needs a description credit — budget a paid library if it becomes house style | ⏳ Dan |

## Long renders: never poll for a filename, always signal DONE

A backgrounded render watcher once ran **20 hours after its render had finished** because it
polled for a filename the render never wrote (2026-08-22) — Dan saw a blinking dot and left a
finished video unreviewed for a day. Wait on the **process** (`wait $PID`), never on
`[ -f "$OUT" ]`; give every wait a hard timeout; make it print why it exited; and end the
session with the file path, size and *ready to review*. Helper that does all of this:
`.claude/skills/longform-edit/reference/render_wait.sh`. Full rule: the Delivery section of
`/longform-edit`.
