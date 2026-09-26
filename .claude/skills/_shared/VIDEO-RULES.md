## Never show stick-figure exercise demos (Dan, 2026-09-25)

- Never show the app's stick-figure exercise animations in any video. Use suitable, polished AI-generated exercise demonstration clips instead, matched to the displayed workout. Dan rejected the WV-01 workout preview and said: "Never ever show these stick figures in any video."

## Standing authorization for thumbnail replacement (Dan, 2026-09-16)

- When Dan requests a thumbnail replacement, install the approved new thumbnail without asking again about removing the old thumbnail or its completed A/B test. Preserve available test results in the installation notes first. This does not authorize deleting the video or post itself.

## Video clip generation budget and frame approval (Dan, 2026-09-15)

- **Reaffirmed by Dan, 2026-09-16:** Gemini and Replicate generation is standing-authorized up to **$5 total per video**. Use the project's Gemini/Replicate keys, including `bakeoff/.env`, for this authorized work without asking again. Ask for spend authorization only before exceeding $5 for that video; do not request separate approval for a batch within the remaining budget. Track costs and retries across revisions. Dan explicitly approved the pending C1652 three-clip batch (estimated $0.75) after being told the earlier built-in still costs were unreported; preserve those unknown costs honestly without repeating the same permission stop.
- Up to **$5 per video** is authorized for AI clip generation. Count supporting start/end-frame generation and paid retries in that video's total; a new task or revision does not reset it. This more specific limit applies within the existing session and batch limits above.
- Before exceeding $5, discuss the specific clips, why existing assets or suitable stock will not do, and the estimated new total. Dan is generally open to **up to $10 with a reason**, but that is not automatic authorization to exceed $5.
- Show Dan the **start and end frames plus the intended action** for approval before generating motion. Budget authorization does not replace frame approval. Materially different replacement frames require approval again.
- Current stock choice (Dan, 2026-09-15): **Pexels and existing assets with known usage rights only; no paid stock service or subscription.** Use AI where the intended scene needs it. Keep a per-video generation total, including paid unsuccessful attempts. Gemini quality-review spend remains governed by its separate standing authorization.

## Approve the opening, all graphics and clips before a full render (Dan, 2026-09-26)

- Read [PRE-RENDER-APPROVAL.md](PRE-RENDER-APPROVAL.md). Every video editing workflow uses the VSL round-4 approach: first 30 seconds to lock source-specific color/audio and opening treatment, all planned graphics with before/during/after speech, every clip in context, and proposed AI start/end frames. Finished AI clips are approved before full assembly unless their exact use was already explicitly authorized.
- Render the complete film only after the opening treatment, graphics and clips are locked. While waiting, prepare sources, edit maps and isolated/contextual previews, not a complete placeholder film. Reuse unchanged approvals and honor an explicit sample waiver. For RO-01 revision 4, color/audio are approved and no new opening calibration sample is needed.
- Use Soft Blue Light and the Motivation lower third. Single points normally use a compact `KEY POINT:` lower third with a useful sentence; no random-word chips or large empty cards. Larger layouts need substantive content such as a study, diagram, comparison or list. Review junk pauses and false starts before submitting the packet.
- [ASSET-APPROVAL.md](ASSET-APPROVAL.md) retains clip source/hash records. Queue frame approval alone does not authorize a full film. Keep the dispatcher paused when Dan has paused it, batch decisions and never keep a session polling for an answer.

## Cover work does not block an approved B-roll video build (Dan, 2026-09-20)

- Treat B-roll approval and cover approval as separate decisions. Once Dan approves the exact B-roll clips, trims and crops, insert them and regenerate the video promptly, even if the cover image is still being revised.
- An unfinished cover may still block packaging or upload when that workflow requires one, but it does not block the video render, exact-file quality checks or a review copy. Never imply pending B-roll is approved just because Dan asks for a final video.

## Short-form footage fills the vertical frame (Dan, 2026-09-18)

- **When the source can support a clean portrait crop, short-form footage occupies the complete 9:16 canvas.** Do not shrink it into a square/card stage or reserve black bands above and below. Black bars or an inset stage are only for footage whose essential action, body, equipment, text or graphics cannot survive a full-screen portrait crop.
- For a dedicated talking Short, default to a tight measured portrait composition: only a little space above the top of Dan's hair, with the lower edge around the middle of his thighs/shorts. Centre each shot and inspect the whole moving take so gestures are not needlessly clipped. A native-portrait recording must be treated as portrait even when its encoded width/height appear landscape because of rotation metadata.
- Titles and captions adapt to the full-frame picture; the picture is not reduced to make room for them. Place compact graphics in measured clear space and keep them off Dan's face and abs. If a full-screen crop is genuinely impossible, record the specific containment reason before using an inset or black field.

## RO-05 rejection: colour, transitions, graphics, hook, hair (Dan, 2026-09-23)

Dan on Claude's RO-05 "How I Make My Daily Salad" first cut (r10): *"this is not up to standard. This is not usable. This is not
something that we can publish."* Every point below is a standing rule for every video from now on.

- **No swipe sound effect, ever.** *"I really hate that swiping sound effect. We need to remember this going forward: never, ever use
  that swiping sound effect for anything."* `sfxlib.whoosh()` and `sfxlib.riser()` now raise an error; do not re-create them by hand,
  and do not use any whoosh/swish/swipe sample from anywhere else. Muhammad's own flash transitions are silent.
- **Transitions are Muhammad's.** *"We need to make the transitions like Muhammad's transitions in the AbWheel video."* Reference:
  `YouTube Long Form Video Content/The $17 Ab Wheel Beats Every Crunch - READY FOR UPLOAD/Muhammad edit/The $17 Ab Wheel Beats
  Every Crunch - Muhammad edit v2 HD - READY FOR UPLOAD.mp4` (his white/blue bloom flashes with a double-pulse envelope, whip-pans with
  real directional blur inside cards; measured in `/Volumes/Extreme/_edit_work/abwheel/mrepro/notes.md`). Dan has more examples of his
  transitions; ask for them before building transitions if the handoff does not already link them.
- **Colour must look like Muhammad's, not washed out.** *"It looks a little bit washed out. The colors aren't as saturated. I want this
  to look like Muhammad's video as much as possible."* Measured on 2026-09-23 (median luma / median saturation): Muhammad Ad 1
  0.22 / 0.23, Muhammad Ad 6 0.27 / 0.39, the approved Codex C1652 kitchen cut 0.23 / 0.32; the rejected RO-05 r10 0.38 / 0.27 (mids
  lifted, flat). Grade toward his numbers, then prove it with side-by-side stills against his frames BEFORE any full render.
- (Graphic style superseded 2026-09-26 by Soft Blue Light, see GRAPHICS-STANDARDS.md; the effort and style-board points still apply.) **Graphics are Muhammad's actual graphics.** *"The graphics also look very basic and very bad... We need to make the graphics the
  same as Muhammad's, not inventing graphics."* Rebuild his components from his frames (pills with the typewriter line-2 reveal, olive
  tab + white pill, gradient pills, numbered chips, frosted stack panels built one item at a time, grid/bracket title cards with the
  motion-blur wipe, glow cards). Generic white bars, "KEY POINT" tabs and home-made stat cards were rejected. Show a graphics style
  board side by side with his frames before placing any graphic.
- **Recipe / how-to videos open on the finished product.** *"For the intro, I want an attention-getting clip... I want to see the
  finished product right at the beginning of the video."*
- **Never crop hair that the camera captured.** *"Double-check that we're not unnecessarily cropping out my hair when it was in frame
  in the filming."* Where the operator already cut his hair, keep as much head as the source has; never crop further. Measure the hair
  top densely across the WHOLE shot (every 0.25 s), not from a few samples; a punch-in whose top edge would cut hair on any frame is
  not used.
- **Effort before tokens.** *"Putting effort into it, not doing the color correction, not getting the cropping right, not doing the
  graphics right, that's a big waste of tokens. We need to avoid making any videos like this in the future."* Style (grade, graphics,
  transitions) is proven on stills and one finished 60-90 s sample section against Muhammad side by side BEFORE the full video is
  built. Ten rounds of reactive defect-fixing on a cut whose style was never right is the waste he means.

## A before and after picture are the SAME PERSON (Dan, 2026-09-12)

- **Never mix people across a before/after pair.** Dan, on the Ad 5 vertical's app demo, which uploaded one man's photo and
  returned his own AI result: *"Generally, going forward, don't mix before-and-after pictures. It should be the same person
  in the before and after. That doesn't really make sense if you change the person."*
- This binds every place a pair appears: an app recording, a result screen, a card, a thumbnail, a landing page. If the
  "after" for a given "before" does not exist, **generate it for that person** (a real generation through the live product,
  never a composite — an overlaid photo was rejected within minutes) or change the before so the pair matches. Do not ship
  the mismatch and do not crop around it.
- **Scoped Ad14 R3 exception (Dan, 2026-09-17):** Dan explicitly authorized a simulated/composited app demonstration that
  presents his heavier shirtless sunglasses photo as generating the existing `dan by pool.png` goal. Keep the same person
  and the `AI-GENERATED` disclosure, and record the internal provenance as simulated. This exception does not repeal the
  normal live-generation rule for other before/after pairs.
- ⚠ The only real app recording in the asset library uploads a man who is **not Dan**, so every phone demo cut from it
  inherits this fault until it is re-recorded.

## Video editing feedback — organic C1652 (Dan, 2026-09-16)

- **No repeated stock clip within one video.** Use a different source clip for each stock placement; different trims of the same stock source still count as repetition. Audit source IDs/hashes across the full timeline.
- **Real videos are not still photos.** Do not put “Real picture of me — not AI-generated” on real moving footage of Dan. That disclosure applies to real physique photographs; AI-generated imagery retains the appropriate AI label. This clarifies the photo-label rule below.
- **Horizontal framing stays still.** In 16:9 videos, choose a fixed horizontal center per shot. Recenter only if Dan is actually approaching the frame edge; do not follow ordinary movement in ample horizontal space. Preserve deliberate wide/tight cuts and approved framing sizes.
- **Audio/graphics acceptance is specific to the delivered video.** C1652 R1 audio and graphic treatment were rejected despite a numeric audio PASS. Match Muhammad using actual listening/moving reference comparisons, and record the verified reusable method in the shared skill; earlier approval on another source is not proof of parity here.

## Reusing Dan's previously produced videos (Dan, 2026-09-17)

- **Old-channel proof: Dan is the main speaker, inside the full YouTube page.** Always select a native close-up of Dan talking, not a two-person shot where Mike Chang speaks and Dan looks like a sidekick. Keep the video playing inside the full screen capture with channel name, subscribers and views legible; never crop away the page. Use the diet clip for diet references and the M100s clip for exercise/SixPackAbs.com references. Dan reaffirmed this after rejecting Ad14 R3 at 0:24 (2026-09-17).
- **Use the finished edited export, never the raw camera source.** When an edit borrows footage from any of Dan's previously produced videos, source it from the final edited/color-corrected master. Never use raw, ungraded or unfinished footage merely because it is higher resolution or easier to locate. If the finished export cannot be found, keep the scene unresolved while searching rather than silently substituting raw footage.


- **Correct workout exports (Dan, 2026-09-17):** For the one-minute ab workout, use only `YouTube Long Form Video Content/V4 + V5 - The Ultimate 1 Minute Ab Workout - UPLOADED/V4 - 1 Minute Ab Workout That Hits All 4 Ab Muscle Groups (At Home) - UPLOADED.mp4` or `V5 - The Ultimate 1 Minute Ab Workout - Follow Along (No Talking) - UPLOADED.mp4` in that same directory, whichever gives the cleaner shot. Dan rejected Ad14 R3's use of `Media/video_edit/out/abs_workout_final_edited.mp4` as raw/uncorrected; never use that file or `Media/video_edit/work/main.mp4` as finished reference footage. A filename containing `final_edited` is not proof of approval.
- **Approved Dan self-generation demo (Dan, 2026-09-17):** R3's 2:17 sunglasses-before → pool-goal demonstration is approved for reuse every time Dan refers to generating a photo of himself with AbsByAI. Preserve the exact approved sequence and disclosure treatment from R3 g17. Reusable assets/provenance: `Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/`. This extends the R3 simulation exception to reuse of this exact demo; retain simulated/composited internal provenance and same-person identity, and do not generalize it to unrelated pairs.

## Hair never leaves the frame (Dan, 2026-09-25)

- On every video, Dan's hair never goes out of the top of the frame at any moment. Dan, on the SL-04 arms and shoulders shorts: *"My hair goes out of the frame a little bit. We have to eliminate this for all videos going forward. If you have room on the top, then crop a little bit higher so there's a little bit of extra space above my head."*
- Where the source has picture above his head, crop higher so there is a little space above his hair on every frame of the shot (measure the hair top densely across the whole shot, including when he moves or rises). Where the source itself has no room (the camera framed his hair at the edge), use a different shot or a wider window that does, rather than ship hair touching the edge.

## Cover text never covers Dan's face or hair (Dan, 2026-09-18)

- On every thumbnail or cover image, keep all text completely clear of Dan's face **and every part of his hair**. Measure the rendered placement against the actual portrait; move or resize the text into clear negative space rather than allowing even a partial overlap.

## Label Dan's real pictures (Dan, 2026-09-11)

- **Thumbnail exception (Dan, 2026-09-16):** Do not put “Real picture of me — not AI-generated” on thumbnail or cover images; it is too small to read on a phone. Keep that label on real physique photographs when they appear inside videos. Thumbnail/cover designs also omit `AbsByAI.com` unless Dan explicitly requests it. This overrides the broader real-photo label rule below for thumbnails and covers; it does not remove AI-image disclosures inside videos.
- **Dan's REAL after pictures carry a burned label: "Real picture of me — not AI-generated"** (Dan, 2026-09-11: viewers were taking his real photos for AI). Every real photo-shoot or studio picture of Dan shown as a result gets it for its full duration, in the same chip style as the AI label. AI images of Dan keep "AI-GENERATED". The two labels are mutually exclusive: every picture of Dan's physique carries exactly one of them.
- ⚠ **LABEL PLACEMENT — NEVER OVER HIS FACE AND NEVER OVER HIS ABS** (Dan, 2026-09-12, on the Ad 2 square: *"the label will not block my face or my abs… put it above my head, to the side, or somewhere that it doesn't block my face and my abs in all of these after pictures"*). This REPLACES the old "low on the frame, at the shorts/waistline" rule, which is what put the chip across his lower abs. Put it **above his head, off to one side, or anywhere in the frame his body does not occupy** — still inside the safe area, still large enough to read, still clear of the caption band. **The picture exists to show the physique; a label over the abs defeats the picture.** Choose the position by MEASURING him on the RENDERED frame (person mask → the bounding box of head + torso, then place the chip in the largest clear band), never at a fixed y — every photo frames him differently. If nothing is clear enough, shrink the chip or move it to a corner before you put it on him. Applies to BOTH labels on any picture of Dan.

## Don't default to frowning photos (Dan, 2026-09-13)

- **Don't use a photo where Dan is frowning/scowling/unhappy-looking as a thumbnail or cover
  image unless he specifically asks for one, or the video/post is itself about something sad,
  negative, or a failure/bad event** (e.g. "I made this mistake," a warning, a rant). Flagged
  when the live "The 17 Dollar Ab Wheel Beats Every Crunch" thumbnail used `studio-blue-271`
  (the red "THAI BOXING" shorts photo) with a visibly downturned, sullen mouth — wrong tone for
  an upbeat "do this" thumbnail.
- Every finalized photo with a genuine frown/scowl/sullen resting expression is sorted into
  `photos/finalized social media photos/Frowning Photos/` (both the `_FINAL_PRIMARY.jpg` and
  `-IG-4x5.jpg` files) so it doesn't get picked by default when browsing or building a new
  thumbnail. As of 2026-09-13 that's 11 photos: `studio-blue-271`, `photo-20`, `studio-blue-47`,
  `studio-white-2`, `studio-gray-63`, `photo-81`, `photo-84`, `photo-135`, `photo-137`,
  `photo-138`, `photo-158`. Their `_cutouts/*_CUTOUT.png` files were left in place (still usable
  on request); only the browsing copies moved.
- The bar is a real downturned/scowling mouth, not merely "not smiling" — plenty of good serious
  or intense-focus photos (flexed poses, martial-arts stances, side profiles) stay in the main
  folder because a stern/intense look is a normal fitness-brand vibe, not a frown.
- When adding new finalized photos to the folder in the future, sort any genuinely frowning ones
  into `Frowning Photos/` the same way, and don't route around this rule by pulling one back out
  for a normal thumbnail without Dan's say-so.
- A few already-delivered `reference/recipe/` build scripts (`ad-edit/reference/ad1/`,
  `website-video/reference/recipe/**`) hardcode paths to `photo-137`/`photo-158` in the old
  location — those masters are already shipped, so this wasn't fixed, but a future rebuild from
  one of those exact recipes needs the path corrected to `Frowning Photos/`.

## An AD is never published organically (Dan, 2026-09-17)

- **An ad video never goes out on an organic channel — not Facebook, not Instagram (either account), not
  TikTok, not Blotato, not YouTube Public — no matter how the request is phrased.** An ad lives as an
  UNLISTED YouTube upload that Google Ads points at (`/ad-setup`), and nowhere else. Organic distribution is
  for content videos (`/video-setup`).
- **"Set it up on all platforms" does NOT authorize organic posting of an ad.** Dan writes that sentence for
  content videos, and it is the sentence that published Ad 5. When it arrives attached to an ad, do not
  execute it: say plainly "this is an ad — ads don't go organic, do you want it posted anyway?" and wait.
  Dan's per-video "yes, I mean post the ad organically" is the ONLY override, and it goes in
  `ORGANIC_OVERRIDES` in `scripts/blotato/ad_guard.py` with the date and his words.
- **This is enforced in code, not on trust.** `scripts/blotato/ad_guard.py` blocks an ad payload three ways —
  a missing `"content_type": "organic"`, a source path under any `<Editor> Ad Videos/` folder, and a caption
  or slug matching a known ad title or ad YouTube id — and every Blotato queue script imports it. **Never
  hand-roll a queue script that skips it**, and never set `content_type` to "organic" on an ad to get past it.
- **The Blotato MCP tools are gated too.** A `PreToolUse` hook in `.claude/settings.json` runs
  `scripts/blotato/hook_ad_guard.py` on every `blotato_create_post` / `blotato_update_schedule` call and
  blocks it if the payload carries a known ad. That covers the path the queue scripts do not: calling the
  MCP directly. A hook that cannot read its input or load the registry BLOCKS rather than passes.
- **Audit the live queue with `python3 scripts/blotato/ad_guard.py --scan`** before and after any Blotato
  write, and whenever the queue is touched.
- ⚠ What it cost: Ad 5 "Every Diet You've Tried Failed for the Same Reason" ran free on FB, IG @danrosefit,
  the @abs.by.ai mirror and TikTok on 2026-09-16/17, and Public on YouTube, because on 2026-09-10 Dan wrote
  "upload it to YouTube and set it up on all other platforms in the Blotato queue" and the session did
  exactly that. `/ad-setup` positively permitted it at the time. Nothing malfunctioned — the rule did not exist.

## YouTube visibility — never upload Public (Dan, 2026-09-16)

- **Never upload any video to YouTube as Public, and never use YouTube's native scheduling/publish-at path.** This applies to API uploads, Studio uploads, scripts and manual work. The upload-time visibility must always be non-public.
- **Ad videos are always uploaded Unlisted.** No ad gets a separate Public YouTube copy, even if it will also be used on other platforms.
- **Organic videos are always uploaded Private.** Blotato queues and releases the organic video at the intended time, including YouTube; do not schedule the Private upload to become Public from YouTube Studio or the YouTube API.
- Before reporting an upload complete, read back the saved visibility. It must be `unlisted` for an ad or `private` for organic content. A missing or different value is a failure; correct it before continuing. If the video type is unclear, use Private while resolving it—never Public.

## Audio: one standard, enforced by a stamp (2026-09-02)

- Every rendered video's audio goes through `.claude/skills/_shared/audio/`: `pick_lav.py` decides which
  track is the lav **per file** (never a channel number — the 8/28 rolls have four mono tracks),
  `voice_chain.py` is the only voice chain, and `audio_gate.py` measures the **delivered** file against
  Muhammad's pinned reference and stamps it. Every QC and delivery script refuses a file without a matching
  PASS stamp. Do not write a new chain or a new gate in a skill; extend the module with a flag.
- Run `selftest.sh` before a batch. Send the gate's A/B clip with every review copy.
- **An editor's finished mix is delivered UNTOUCHED by default** (Dan, 2026-09-10: *"Zishan's audio sounds much
  better… This is an awful mistake which can't happen again… Use Zishan's audio."*). A vertical or cutdown rebuilt
  from Muhammad's, Zeeshan's or any editor's finished cut carries his audio exactly as he exported it — stream-copied,
  or only CUT for a cutdown — gated with `audio_gate.py --reference-mix <his> --verbatim`. Our loudness and L/R
  targets are for OUR mixes; never bend an editor's audio to pass them, and never sum it to mono. A small constant
  lift happens only when Dan asks for one, and the approved Muhammad verticals (+4.2 dB, loudness range 3.5 → 2.8 LU)
  are its ceiling; the rejected Zeeshan build (+9.9 dB into the limiter, range 5.9 → 4.1, mono) is what past it
  sounds like. If his export is too quiet for a feed, ask him for a louder one.

## One delivery gate, versioned, on the delivered file (2026-09-11)

- **Every delivered video goes through `.claude/skills/_shared/deliver/gate.py --format <fmt>` and
  carries its PASS stamp.** One gate for all seven video skills, run on the file that actually goes
  out. Every bound lives in `_shared/deliver/formats.py` beside the file and the date it was measured
  on — **never in a per-video script**, which is how a fix landed in one of six pipelines and the
  other five kept the bug.
- **A missing input is NOT MEASURED, which FAILS**, and **a row a format has not answered for FAILS
  as UNCONFIGURED.** If a check genuinely does not apply, it is an entry in that format's
  `not_applicable` with a written reason a reader can audit. Silence is not a pass.
- **`GATE_VERSION` invalidates every older stamp.** Change a check or a bound, bump it, and
  everything previously stamped has to be re-gated. `Docs/VQC_baseline_20260909.md` is why: 20
  delivered files carry a PASS stamp that would fail a re-gate today.
- Module README and the current known gaps: `.claude/skills/_shared/deliver/README.md`.

## No gate change ships without the regression corpus (2026-09-09)

- **`python3 .claude/skills/_shared/qc_corpus/run.py` must pass before any change to a quality gate,
  a threshold or a setting is committed.** It re-runs our gates over every file Dan **rejected** and
  every file he **approved**, with his words recorded, and it must **fail every rejected one and pass
  every approved one**.
- **Why:** every gate we own was built backwards from the last rejection, so each new failure shipped
  exactly once. Twice that produced a gate that scored a **rejected** build as *better* than an
  approved one — the "underwater" dereverb won every audio row it had, and rev 3's own headroom gate
  passed the cut Dan called *"basically not usable"*. Both files are in the corpus now.
- **Never raise a threshold to make a build pass** (memory: `audio-never-over-strip`). If a corpus
  entry fails a bound, that is the finding — report it, do not tune it away.
- **A new rejection becomes a corpus entry in the same session it happens**, with Dan's verbatim
  words, before the fix is built. So does a new approval: half the corpus's job is stopping a gate
  from blocking good work.
- **A check that did not run is a FAILURE, not a pass, and never a silent skip.** A missing flag, a
  missing baseline, a missing plan, a script that is not on disk — each one fails and says what is
  missing. If a check genuinely does not apply, declare it explicitly, with a reason a reader can
  audit. Full reasoning: `.claude/skills/_shared/qc_corpus/README.md`.

## Video builds: never run more than two at once

- **Cap concurrent video builds at two across all sessions.** Before starting a render, transcription, QC or watch pass, check whether other sessions are already building (`ps -Ao command | grep -E 'ffmpeg|qc_style|render\.py|whisper'`). If two builds are already running, wait — do not start a third.
- **Measured 2026-08-27, not assumed.** Four concurrent builds drove the Mac mini (10 cores) to a load average of **242 with 0% idle**, and made `finish_audio.py` take **126 seconds against 13.6 seconds on a quiet machine — a 9.3x latency penalty.**
- **It buys nothing.** x264 already threads across all 10 cores, so extra concurrent builds do not raise throughput; they only timeslice. The sole headroom is the ~19% of a build that is single-threaded Python (PIL graphics, Whisper), which is why **two** builds overlap usefully — one build's Python runs under another's encoding — and a third is pure loss.
- This is the largest available speedup in the video pipeline: worth more than the three candidate software optimizations and a new Mac combined, and it costs nothing. Full numbers: `.claude/skills/_shared/timing/REPORT_20260827_build_timings.md`.
- **Never run a pipeline script inside another session's live build directory** — it will overwrite intermediates that session is reading. Work in a scratch copy.

## Video review refinements — C1652 R3 (Dan, 2026-09-17)

- **Clip variety means different visible content, not merely different IDs or trims.** Do not reuse stock from essentially the same scene/shoot with the same actors or actresses, even from a different camera angle. Doctor inserts within one video need distinct casts and settings. Prefer suitable Pexels/known-rights footage; use authorized AI generation if no suitable distinct clip exists.
- **Exercise illustrations must vary the exercise.** For Dan demonstrating daily exercise, use ab wheel plus toe touches or kettlebell deadlifts, not repeated ab-wheel footage. This includes similar excerpts from one source video. Dan remains the same person; the exercise action must differ. Necessary repetitions inside an actual exercise teaching demonstration are a different purpose.
- **No added camera movement in horizontal16:9 presenter footage.** Do not pan, drift, track or recenter just because Dan shifts slightly. Keep a fixed composition within the shot; preserve approved framing sizes and deliberate cuts unless separately rejected. Check rendered footage, not just a fixed-center setting.
- **Requested AI narrative clips require actual motion.** A static frame, start/end montage, slow image pan or brief motion fragment followed by a held endpoint is not a completed clip. Generate and validate the intended motion from approved assets; do not ask again for unchanged approved frames. This does not prohibit real photo displays or specifically approved scientific still illustrations.
- **Three-photo screen template:** use three vertical real studio portraits with distinct poses and consistent presentation proportions; plural disclosure “Real pictures of me — not AI-generated,” clear of faces/abs. Save the tested layout for reuse.
- **Organic graphics:** imitate Muhammad’s actual moving graphics, including lower-thirds and full-screen treatments. Use self-contained titles that name the topic. Specific approvals with limited requested edits take precedence over a general redesign; for C1652's Zepbound/stakes lists, enlarge text as requested and preserve the otherwise approved panel design.

## Horizontal footage stays completely static — Dan, 2026-09-17

- **No added camera movement or recentering on Dan in horizontal/16:9 videos.** No tracking, pan, drift, animated crop or zoom to follow or center him. Choose a fixed composition for each shot and leave it fixed. This supersedes earlier horizontal exceptions for approaching the frame edge; tracking is only for square/vertical layouts when actually needed.
- Ordinary cuts between fixed compositions remain editing cuts, not camera motion. Graphics may animate without moving the presenter picture beneath them. Check actual rendered background landmarks: a fixed-X setting alone does not prove a static picture. If the camera source itself drifts, resolve that in source choice/stabilization rather than silently claiming the delivered picture is static.
- Dan approved C1652 R4 as good enough to ship despite a small remaining movement near1:09. Do not reopen that accepted film to enforce the future rule. Its approved master is SHA256 `eace1bdbb9f7a16fadff8bb2d2e80812ea4e777cf413a1e06575527f95d64f44`.
- C1652’s Zepbound text size is approved. Dan would prefer a third benefit, “Makes you serious about fat loss,” in a future relevant treatment; he accepted the existing two-row graphic in this final film. Do not expand its content without speech/timing context in future work.

## On-screen text graphics are KEY POINTS, not a second set of subtitles (Dan, 2026-09-18)

- **A text graphic exists to DISTILL the point, never to repeat the words being spoken under it.** Dan, on Zeeshan's
  deadlift video: *"I don't think there's much value if, let's say, I say 'lower risk' and repeat that 'lower risk.'
  The value of the graphic, I see, is distilling the key point for someone who may not have gotten it from a longer,
  more complex explanation."*
- **The format is his own, written into the doc by him:** `KEY POINT: <the distilled point>` — "KEY POINT:" in caps,
  the point in Title Capitalization, and the one or two words that carry the punch in FULL CAPS. His worked example:
  `KEY POINT: Deadlifts Cause More Injuries Than EVERY OTHER LIFT COMBINED`.
- **Where two or three chips currently stack up saying the same thing three ways, it becomes ONE key point.** A
  three-chip build that mirrors a three-item spoken list is the repetition he is rejecting, not a device.
- **What is still allowed as a plain chip:** labels and signposts that are not repeats — the name of the exercise on a
  demo clip, numbered section titles ("Exercise #2: Lat Pulldowns"), the URL chip, a product feature list in the CTA.
- This applies to every video from here on, not just the one it was written on. When reviewing a cut, the graphics pass
  is: transcribe every chip, then ask of each one "does this distill something, or does it just echo the audio?" —
  and write the replacement key point, not a typo fix, for every chip that only echoes.

## Approved graphics and layout standards (Dan, updated 2026-09-26)

Read [GRAPHICS-STANDARDS.md](GRAPHICS-STANDARDS.md) before designing or revising graphics. Soft Blue Light is now the standard graphic family for all videos, including website VSLs, ads, organic videos, Shorts and newly revised square/vertical graphics; the approved Motivation lower-third format is locked for lower thirds in all videos. This 2026-09-26 expansion supersedes older Muhammad graphic palettes and website-only scope. Preserve already approved exports unless their graphics are explicitly being revised. Muhammad sound, camera color and transition references retain their separate scopes. That reference also defines three-portrait screens, sequential horizontal photos, credible iPhone framing, single rounded blue cards behind side text lists, with no secondary full-height field and fixed presenter positioning with intact arms. These specific approvals supersede conflicting older graphic examples. Keep source-specific crop, color and audio settings scoped to their recordings.

## Exercise demonstration timing and visual cues (Dan, 2026-09-25)

- Match each demonstration to the words being spoken. Show correct form while Dan gives the positive instruction, then show the mistake when he warns against it. If he returns to a positive instruction, return to correct form or the presenter. Set picture cuts from the heard words and check moving action on both sides of every cut. Swapping clips at their old boundaries is not enough if the result still contradicts the narration. DS-18 R7 demonstrates this for weight placement, toe direction, back position and glute squeeze versus hip thrust.
- When a form detail is hard to see, point to the relevant body part or equipment with green arrows for correct form and red arrows for the mistake. The color, label and visible action must agree. Keep arrows on the target as it moves, clear of captions and the teaching action. Do not add arrows to a shot with no specific feature to point out.
- A recurring overlay needs a clear teaching purpose. Check it against the narration, captions and action; omit it when it repeats information without helping the viewer. When removing one element from a combined graphic layer, preserve unrelated approved elements in that layer.
