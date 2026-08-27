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

## Step 0.4 — check the microphones (see /longform-edit Step 0.4 for the full rule)

**The rolls are not stereo — they carry two different mics, and the right channel is the
close lav.** Take `-af "pan=mono|c0=c1"` at the very first audio stage. Carrying both put
a dry voice in one ear and a delayed, polarity-inverted room copy in the other; on the
8/14 ad roll the left channel is also clipped in 24,368 samples. Verify per roll with the
lag-search recipe in /longform-edit — the wiring can change between shoots.

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
   roll (Step 0.4).
33. **Check the stereo image of anything you deliver.** His voice measured +0.99 L/R
   correlation with the side channel 23 dB under the mid; ours measured −0.01 with side
   and mid EQUAL. That single number would have caught this on day one. A talking-head
   voice belongs dead centre — `pan=stereo|c0=c0|c1=c0` after the voice chain.
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
   3.6 kHz was making the room WORSE.
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
