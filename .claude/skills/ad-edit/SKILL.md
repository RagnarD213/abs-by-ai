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
check-ignore` before staging, and working on the Seagate. Read that SKILL.md
first if you haven't this session.

## Step 0 — inputs

- **Script:** the ad's section of **"Abs by AI finalized scripts batch 1 -
  TELEPROMPTER"** (`1bpEndCcM-imeOWS0tp86l7Ud0bGyxLQ-MWZVAwcacgA`) — pure spoken
  words, THE ground truth for the cut.
- **Cues + assets + per-ad notes:** the same ad in **"abs-by-ai ads batch 1
  finalized scripts for teleprompter"** (`1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg`)
  — bracketed visual cues, placed images, compliance notes. Every cue is a
  graphics/insert obligation for the edit.
- **Footage:** same shoot setup as longform (Sony rolls via Drive/Seagate). One
  teleprompter roll per ad plus b-roll clips.
- **Shoot requirement to flag BEFORE filming: ads must be shot 4K.** Both pillars
  of this skill — punch-in zoom cuts and the 9:16 export — need crop headroom. A
  1080p source leaves ~1.15x of zoom before softening and makes the vertical crop
  a 608→1080 px upscale. (Longform's 4K recommendation is a nice-to-have; here it
  is load-bearing.)

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

**Delivery layout** (on the Seagate, per longform; media stays out of git):

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

## Decisions locked vs pending

| decision | status |
|---|---|
| Script = ground truth; spoken corrections win; flag drift | LOCKED (2026-08-20) |
| Take selection: Dan first minute, Claude rest, learn toward full handoff | LOCKED |
| 16:9 primary + 9:16 secondary this batch; both must be strong | LOCKED |
| Cut whole script, no ceiling | LOCKED |
| No 1.2x pass, no music bed, no hook variants (for now) | LOCKED |
| Minimal graphics first; Dan directs placements; learn | LOCKED |
| Negative-imagery scan; remove certain violations, flag unsure ones | LOCKED |
| NO before/after anywhere, incl. in-app UI; before → other → tagged after | LOCKED (2026-08-20, Dan's #1) |
| Style: J2 graphics + CTA bar, MadMuscles captions, "abs" lowercase | LOCKED (2026-08-20) |
| "Results are not guaranteed" micro-disclaimer (photo run + end card) | shipped on ad #1, not vetoed |
| CTA bar exact copy/geometry per style | ⏳ ad #1 |
