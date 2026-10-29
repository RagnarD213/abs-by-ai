## Shorts shortlists show each Short's full transcript under its title (Dan, 2026-10-22)

- **Every proposed Short on a shortlist (extracted from a long-form, or a recut) is shown with its title and the complete
  word-for-word transcript of what it will say, pickup line included, in cut order.** Dan, on SL-16: *"Show me the full
  transcripts for all your proposed shorts with the title. Let's always do this as a standard process for making shorts going
  forward. Doing things this way is too confusing for me to tell what short is going to have which content."*
- A table of timecodes with an opening and closing quote is not enough. Use the film's corrected subtitles trimmed to the
  planned cut points; mark skipped passages. Claude and Codex, every Shorts batch. Detail: `/shorts` Step 2.

## AI clips of Dan look natural, or they never reach review; regenerate slop on the subscription (Dan, 2026-10-21, SL-06)

Dan rejected all six SL-06 AI flex intros, every one gate- and reviewer-passed: *"the smile is weird. We need just a regular,
relaxed, closed-mouth smile. He's also shaking and flexing too hard... Make it look natural and not like I'm shaking and flexing
and artificially smiling. This looks like AI slop. This is not something which should make it to my review in the future.
Especially given that we can now generate these on subscriptions, I want you to be a little more picky about what you bring to
me for review and regenerate if you get some slop like this."*

- **The bar for any AI clip of Dan: would it pass as a real camera clip of a calm man?** A relaxed, closed-mouth smile (no held
  toothy grin, no grin that grows, no mouth that moves); no trembling, shaking or jitter in arms, hands or head; no straining
  "flex harder" action; small natural motion only (breathing, a slight weight shift). If the frames themselves carry a big
  grin or a straining pose, fix the frames first.
- **Repairs do not rescue slop.** A pasted "held smile", a frozen mouth or other patching that keeps a bad take alive reads as
  artificial at speed: regenerate instead. Label and text restores (a vial label, a calendar) remain fine.
- **Be picky; the subscription makes retakes cheap.** Expect several takes per clip and keep only the most natural one. A
  take that merely "passes" (no vanishing objects, no talking) is not enough: the editor and the reviewer each answer one more
  question, *"does this look like real footage of a relaxed person, or like AI?"*, at playback speed, and any "AI" answer is a
  FAIL. Put that question in every frame-reviewer brief for motion.

## Reaction videos with an off-the-cuff take: edit both versions in one task (Dan, 2026-10-23)

- Dan: *"We'll do both the off-the-cuff and the scripted video at the same time for everything that we have scripted and
  off-the-cuff."* Where a reaction has both a scripted and an off-the-cuff take, the edit task builds both finished Shorts,
  shares the opening, card, key, colour, voice and graphics family, gates and independently reviews each, and shows them side
  by side so Dan picks which ships. Takes and ranges are in each job doc (DS-35 to DS-45, 10/15 roll C1730). DS-33, DS-34 and
  RO-22 have no off-the-cuff take.

## Reaction videos: the locked format, start to finish (Dan, 2026-10-25, Bill Maher Codex R5)

**The standard for all reaction Shorts is Bill Maher Fat 90-Year-Old Codex R5.** (Routing: no AI owns green-screen editing since 2026-10-27; see the end of this section.)
Dan chose it after comparing the finalized Claude and Codex films: "overall I like the Codex version better";
"Codex now has the green screen jobs" (routing withdrawn 2026-10-27, below); "lock this format as our reaction format: the Codex R5".
He preferred the full-screen vertical → horizontal speaking clip → silent clip behind Dan sequence, the smooth
handover into his response, the title ABOVE the silent video, and the colour on both Dan and the clip.

1. **Open on the clip, fixed portrait crop**, with its own sound and nothing before it. Dan's real synced reaction
   is keyed lower left at 0.40 of full size, flush left/bottom, laptop visible, mic silent.
2. **Move to the titled horizontal panel WHILE THE CLIP IS STILL SPEAKING**, with Dan large watching in front.
   R5 changes at 4.004 s. Preserve full 16:9 height; title/source label ABOVE the panel. Do not wait until the quote
   ends to introduce this layout. The reference uses clean cuts, not a mandatory half-second shrink/grow animation.
3. **Hand over smoothly to Dan's response in that same layout**, with the interview still moving but now SILENT
   behind his real foreground hair. R5 changes speaker at 19.6196 s and keeps the panel through 30.2302 s total film
   time. No restarted quote, held frame, doubled head or dead gap. Fit times to the source, keeping the sequence.
4. **Then Dan on the moving Soft Blue Light field**, purposeful fixed wide/tight cuts, relevant HyperFrames graphics
   and cutaways. Match the approved R5 look on BOTH Dan and the source clip, calibrating for different footage.

Exact master/hash, Dan's words, timing/geometry, title config, colour recipe, actual key/compositor code and evidence:
[Codex R5 reaction reference](../shorts/reference/ds40-codex-r5-reaction-format/README.md).
This supersedes the earlier Hormozi Fat Guy Claude R2 and Bill Maher Claude opening/full-format references. R5 already uses the house Claude R2 key algorithm; this changes the
finished format/editor reference, not the algorithm or numeric QA gates. Other videos' audio stays source-specific.
The separate both-takes rule above still applies. The older multi-background commentary reference does not replace
this reaction layout. Existing approved exports and the existing setup handoff remain as they are.
Do not interrupt another active editor or launch a new job merely to install this standard.

**Routing (Dan, 2026-10-27, replaces "Codex owns green-screen editing" of 10-25): no AI owns green-screen editing.**
*"I've changed my mind about that rule of doing green screen on Codex because this edit was so good. I haven't tested
Codex yet, but let's not have any rule for which one. Codex is untested, but I think Claude is our likely champion for
long-form green screen, probably Codex for the short form."* A video stays with the AI it started on (2026-10-20 rule).
For a new green-screen job, recommend Claude Opus 5.5 high for long-form and Codex newest Sol high for reaction Shorts: a
lean, not a rule. The R5 reaction format and the long-form background template stay locked whichever AI edits.

## Long-form green-screen backgrounds: the locked template (Dan, 2026-10-27, RO-24 R3)

Every long-form green-screen commentary video uses the shared background template `_shared/greenscreen-bg/` (README: the
seven types, placements, planner rules, plan format), Claude and Codex alike. Dan, on the RO-24 round 3 page: *"Let's lock
this in as our standard background template for all these kinds of long-form green screen videos... I want to lock this as
our permanent format."* The background is never plain and changes on cuts with what he is saying. Do not reopen the style;
a new film supplies only its facts, photos and clip windows. Reaction SHORTS keep the Codex R5 format above.

## Head and hair clearance blocks review delivery (Dan, 2026-10-20, RO-27)

Dan rejected the RO-27 opening's clipped hair, including at about 0:22 and 0:29: "we need to always make sure that we don't cut off my head or my hair in these shots." Both the wider and tighter presenter shots must leave slight visible headroom. This applies before any review preview, not only final delivery.

- Measure the actual top of the hair across every presenter hold, including the tallest posture and the frames at every cut. Do not use forehead/face boxes as a substitute. Anchor a fixed crop above the minimum hair row with approximately 4% of crop height as headroom; adjust to the actual source and verify the rendered result. Keep horizontal shots static.
- Use the maintained Claude methods: `longform-edit/reference/ro10/hair_first.py` and `haircheck.py` for dense rendered-picture sampling, and `website-video/reference/recipe/hairdet.py` / `hairgate.py` for the hair-top proof and independent every-frame top-edge check. The older `ad-edit/reference/website-video/` path in historical prose is stale. Do not copy the website video's door-background thresholds or coordinates to a different set.
- Calibrate against native-resolution raw and rendered proof frames on this set. Check the exact review export, including its lower-resolution copy: at least every 0.25 seconds of presenter picture, every join's adjacent native frames, and an independently calibrated every-frame edge check. Inspect native-scale proof images of the tightest margins and watch the affected shots in motion.
- Require at least 20 pixels of verified clearance at 1080p scale on every valid measurement, with slight visible room in both sizes. A missed/invalid detection is unresolved, never an automatic pass. If the source itself lacks hair, flag it and choose a complete alternative; moving a crop cannot restore missing hair.
- **Defective source (Dan, 2026-10-20, evening):** where the camera already framed his hair at or past the top edge and no complete alternative take exists, crop as high as the source allows (window from row 0, the SL-03 shorts note), say so on the review page, and do not block the preview on the 20 px figure. The 20 px rule binds whenever the footage gives the option.
- A clipped head/hair frame or unresolved check blocks presenting the candidate. Record the exact export hash, measurements, coverage, worst timestamps and visual verdict. Link/media checks, graphic face-clearance checks and sparse contact sheets do not establish safe presenter framing.

RO-27 R1 used fixed `3440:1935:200:112` and `3000:1688:420:236` source crops without a verified rendered hair-clearance report. Its earlier join/graphic checks did not establish headroom. Preserve R1 as rejected framing evidence and fix all affected previews in R2.

## Approved chroma key for all green-screen videos (Dan, 2026-10-21, replaces 2026-10-20)

Every green-screen video is keyed with Claude's Bill Maher Fat 90-Year-Old R2 key, Claude and Codex alike. Dan: "let's lock this chroma key as our default way to chroma key things. I want all green screen videos keyed out like this" and "Let's make all our future chroma keys this clean and make this a standard." It replaces the Codex R3 key locked the day before. The bar: edges steadier than the camera's own picture with motion removed, dark rim no worse than the source, nothing see-through over saturated pink (watch, glasses), no specks, strands and motion blur kept, measured with the shared scripts before Dan sees it. Method, exact code and hashes: `.claude/skills/_shared/chroma-key/README.md`. Calibrate plate, crop and hold-out boxes to each source on 2-3 s excerpts with `chroma-key/calibrate.py` (quick lane, minutes; it picks the motion peaks and the tracked hold-out and makes a contact sheet), never by re-keying a full clip; then key each piece exactly once through `chroma-key/keyonce.py`, whose `.done` stamp makes every later round skip an approved piece (every recipe, Claude and Codex), gate that one full run, and re-key only a failing piece. Why: on 10-21 re-keying whole clips to try settings was about 6 of the day's 8.5 key hours. Never average across a cut. Do not reopen the accepted style. This locks keying only; grade and audio stay per video, and already approved exports stay as they are.

## Green screen reaction opening: the locked format (current reference: Codex R5, 2026-10-25)

Use the complete "Reaction videos: the locked format, start to finish" rule above. The inherited corner geometry
is Dan at 0.40, lower left, flush left/bottom, full camera height with laptop, real synced reaction and mic silent.
Keep the camera-edge fade narrow except on frames where a hand exits. The speaking clip becomes horizontal early,
before Dan speaks, then stays silent behind him. The old Claude R4 B / Hormozi shrink-and-grow recipes are history;
[Bill Maher Codex R5](../shorts/reference/ds40-codex-r5-reaction-format/README.md) is the authoritative format.

## AI video clips: Google Flow subscription first, paid API only on "rush" (Dan, 2026-10-17)

Dan: *"Default to the subscription; switch to the paid API only when I say rush, accelerate, or as fast as possible. If the subscription credits run out, ask me before paying."* Binds Claude and Codex, every skill that makes Veo motion.

- **Default:** every Veo clip is generated in Google Flow on Dan's Google AI Pro credits (Veo 3.1 Fast, 20 credits a clip), by a background sub-agent driving his Chrome while the main agent keeps editing. Claude spawns the `flow-veo` agent with `run_in_background`; Codex runs `_shared/veo/FLOW-RUNBOOK.md` in its own browser. Queue clips with `_shared/veo/veo.py add`; procedure and measurements: `_shared/veo/README.md`.
- **Every AI clip in an editing task, any model (Kling jobs included), goes through the Google Veo subscription (Dan, 2026-10-17, RA-07 R6):** *"I want to use subscription for all editing tasks for AI clips going forward, unless I specifically tell you not to... I mean my Google VO AI subscription."* A per-job Kling or Replicate script is not a default path any more; a take already submitted when he said it may finish.
- **Paid Replicate API only with Dan's authorization, asked for every time (Dan, 2026-10-20):** his own words saying rush, accelerate or as fast as possible for that video count as the authorization (`veo.py route --said` checks); otherwise ask, with the clip count and the dollar estimate, and wait. A per-job `gen_motion*.py` that calls Replicate directly is the paid path and falls under this rule.
- **Credits run out:** stop and ask Dan once, with the clip count and the dollar estimate ($0.80 per 8 s Veo 3.1 Fast take). Never pay without his yes. Never buy credits or upgrade the plan.
- **Watermark:** Flow's "Visible watermarking" switch (avatar menu) stays OFF; the 2026-10-17 test downloads carry no visible mark. Downloads are the 1080p upscale.
- Unchanged: frames approved and gated before motion, the motion gate and frame-reviewer on every take, the per-video budget for any paid take, the AI label.

## Video rounds start automatically; editor chooses same task or fresh handoff (Dan, 2026-10-20)

Dan: "The system that I want is one where I give my revisions and then the new task automatically starts, is pinned, and the old task is unpinned." The editor chooses whether a fresh task is useful. Dan does not manage handoffs, fire suggested cards or transfer pins. This replaces the 2026-10-18 manual-card/pin rule for authorized video continuations. It does not authorize starting an unrelated film or interrupting a different active editor.

**Model default for every video edit and new round (Dan, 2026-10-20, evening; replaces the Sol-for-everything default of that morning):** a video stays with the AI it started on. A video started on Claude: Opus 5.5, high effort, every round. A video started on Codex: the newest available stable Sol, high effort, currently `gpt-6.1-sol`, resolved through the supported model catalog on the destination/client when available (never guess a future ID, never inherit Astra because the previous round used it; if no catalog is accessible, disclose the known baseline; if the catalog has no compatible Sol, report that blocker). Only Dan's explicit request for this round or all future rounds moves a video to the other AI; older recipe/handoff defaults and general routing do not. Dan: *"default to Opus High for things that we started on Claude and Sol High for things that we started on Codex, unless I explicitly request different... My limit was almost burned up."* An active turn cannot change model mid-inference: use an actually supported next-turn override and end the current turn before production resumes, or choose a fresh task if that control is unavailable.

**Choose and explain in one line.** Quality outranks token savings. Continue here for small contained notes, a recent reply (about an hour) and task context below about 40%. Prefer a fresh task for a substantial new round, a heavy remaining stage (new motion/retakes, full rebuild, gate/reviewer chain), context pressure, stale conversation or repeated wrong turns. Never hand off simply by habit. Use actual context telemetry if exposed; otherwise record a conservative estimate and its basis. Account-wide usage limits are not context usage. No exact percentage should be invented.

**Same task:** save Dan's exact words and scope, advance to `<Title> <Type> R<n+1>` for a new round, create a new round folder, preserve reviewed outputs and locked media/approval hashes, retain the pin. Resume on the video's own default (Opus high if it started on Claude, Sol high if it started on Codex) unless Dan explicitly overrides. A simple status answer is not a new editing round. A model/effort continuation queued in the same task is one next turn, never a duplicate child.

**Fresh task, in the same turn:** use the controller and runbook at [video-rounds/README.md](video-rounds/README.md).
1. Save the decisions and self-contained handoff, expected hashes, applied edits, costs, gate status and exact next action. Reserve the stable per-video next-round journal once, with revision/submission ID and old task identity. Suspend old production and release its queue claim if any; the edit slot moves with the video (the child runs `editcap.py acquire <JOB>` before production; see "Active edit cap"). A child begins read-only until the journal names it production owner; the existing queue claim and build cap still apply.
2. Call the actually available supported task creation tool with the existing project's verified ID/path, local environment, next-round title, complete starter prompt and explicit resolved Sol/high (or Dan's override). Record the exact returned task ID/host before further action. Never retry an uncertain create. A pending client ID is not a ready task ID.
3. Pin the new task using supported sidebar controls. Read its exact task and verify a started turn, then verify it appears in the supported pinned-task listing. Recheck approval hashes. Only then unpin the recorded predecessor, and read back that new is pinned and old is unpinned. Never toggle by guess, reorder other pins, archive or delete.
4. Record the new sole production owner and superseded pointers, then wake that same child once to perform the handoff. Stop the old editor. Report the next round, model/effort and verified result. Keep a starter prompt as recovery information; it is not a chore Dan must perform after successful automatic transfer.

**Unavailable or uncertain:** retain the old pin until the child start and pin are proven. Save exact IDs/outcomes and report the exact missing capability or pending operation. Reconcile through supported read APIs before a retry; never create a second child or blindly resend a continuation. The native Codex create/send, rename, pin/unpin and read tools were exposed on this Mac on 2026-10-20; read-only inventory succeeded. This does not establish Claude start-session availability or prove live pin mutations. The controller has dry-run/unit coverage; installation must not create production edits or test tasks without separate test authorization. No private database writes, new credentials, access-control changes or publishing are part of round transfer.

## Video editing task names (Dan, 2026-10-16)

- Rename every video editing chat at the start to `<Recognizable Video Title> <Type> R<round>`. Put a brief, recognizable video title first, in a few plain words. Use `R1`, `R2`, etc., not `Round 1` or `Round 2`. Examples: `Top 1% LFC R2`, `I'm 41 Wasted Life LFC R2`, `Stop Deadlifting SFC R1`, `Top 1% SFL R1`.
- Content types: `LFC` = long-form content; `SFC` = a dedicated short-form content video; `SFL` = shorts extracted from a long-form content video. Use SFL for those extraction/editing tasks, including batches. Existing AD and ad-format type labels continue for paid ads, in the same title-first, type, R-number order.
- Never put queue/job codes such as RO-25, ORO-25, RO-617, DS- or SL- numbers in the sidebar title, or lead with generic instructions such as `Prepare`, `Edit` or `Continue`. Keep internal IDs in job records, handoffs and filenames where needed. This changes task naming, not internal categories, IDs or schemas.
- Apply the same title to proposed editing tasks and ready-to-paste handoff prompts. Preserve the actual round when resuming the same task; advance it for a new editing/review round, and always when work moves to a new task through a handoff (Dan, 2026-10-17: two tasks must never share a name). Use the available chat-title tool to apply the name. This supersedes older editor-first names such as `Muhammad revisions` and inconsistent SFC labels for shorts extracted from long-form.

## Review-panel testing stays silent; owner handoff enables sound (Dan, 2026-10-28)

- Automated video/audio checks stay muted during playback, auditions, seeking, source/format changes, reloads and recovery. They must not interrupt Dan or feed Wispr Flow. On managed pages, click **Start silent checks** before testing; `?review_mode=automation` also starts in check mode. Verify actual `muted` state before playing. Task-generated trusted input is indistinguishable from owner input, so entering check mode is required.
- After checks, click **Finish checks for owner**. The shared helper cancels stale callbacks, pauses every media element, verifies all are paused and no recovery failure remains, THEN enables normal audio without calling `play()`. Never unmute playing media and never autoplay audible media. Preserve each player's chosen volume, including zero. Failed/incomplete handoffs stay muted and are reported, not called owner-ready.
- Dan receives a paused, sound-ready player. His next deliberate native Play or context/audition Play includes sound, with no extra unmute click. Owner mode must survive play/source hooks; late background play calls are suppressed instead of playing or re-muting his player. Owner recovery returns to paused/sound-ready without autoplay. Any later task checks must start silent mode again. Native owner controls remain available, including his deliberate mute choice.
- `_shared/review_player.js` supplies the two workflow buttons and `window.AbsReviewAudio.beginChecks()`, `.handoff()` and `.state()`. Templates keep initial `muted` attributes and load the helper early for safe startup, not permanent owner mute. Normal owner URLs perform a pause-verified startup handoff; automation URLs remain muted until explicit handoff, which removes the automation query. These states describe playback, never QA completion or content approval.
- Inspect audio without sending it to speakers: offline decoding, waveform/loudness/true-peak/clipping/silence/sync analysis and supported non-speaker file/model inspection. Record methods/limits and leave unavailable perceptual checks incomplete. Silent functional playback or a numeric PASS is not an audible listening pass. Keep the actual narration in the delivered previews for Dan.
- This supersedes the permanently muted owner default, not silent automation. Do not change Mac volume, Wispr Flow, microphone permissions, audio routing, exported audio or approved/scheduled assets. No verified system-wide app switch controls independent tasks. External/native players require explicit task mute, pause verification and sound-ready owner handoff where supported; otherwise report the limitation. Already-open managed pages must reload, and already-running tasks must read/apply this instruction. No new permission step is introduced.

## All new or revised video graphics move in Soft Blue Light HyperFrames (Dan, 2026-10-17)

- Every new or revised video graphic uses the Soft Blue Light theme and HyperFrames motion. Animate the graphic for its actual on-screen duration, not only its entrance, exit or word reveals. For a full-screen card, keep the Soft Blue Light field moving and give a suitable accent, edge light or bar continuing motion. A still PNG over a frozen field does not satisfy this rule.
- Preserve the exact approved words, layout, design and color when Dan requests motion only. Build the motion from the shared HyperFrames templates and method in `_shared/hyperframes/`; if the graphic kind lacks a suitable template, add or adapt a shared HyperFrames template and show its moving context for the required graphic approval. Do not fall back to a static `softblue.py` card for a new or revised graphic.
- This applies prospectively. Do not retrofit an already approved graphic in another film unless Dan requests it. RO-26 round 5 is an explicit revision: turn its approved “Four Things I Did Right” recap into a continuous motion graphic while preserving its copy and composition. Use the approved RO-16 G04 moving counter-bar sample at `/Volumes/Extreme/_edit_work/hyperframes-r2/review/media/g04_new.mp4` as a motion reference, not as permission to change the recap into a math graphic. Its shared config is `_shared/hyperframes/lower-third/example-ro16-g04.json`.

## Long-form round 1: first-minute draft and playable context (Dan, 2026-10-16, RO-26)

- Every new long-form first round includes a playable first-minute draft, colour-correction options and level-matched audio options, including studio videos, alongside all graphics, photos and clips. Do not make Dan approve an isolated asset catalogue before he can see the first minute.
- Every graphic and existing clip must play in its intended edit with actual narration and about 3–5 seconds before and after. Include entrance/exit and return to presenter. Isolated silent animation or B-roll is supplemental, never the only review evidence. Use the shared floating, scrubbable context player and test its sound and seeking.
- The limited first-minute draft uses recommended provisional choices; identify pending inserts and retain presenter footage until AI motion is approved. New AI motion still requires approved start/end frames. The complete film still waits for required choices and assets to be locked. This supersedes older instructions to show the first minute only in a later round.
- Photo correction: RO-26 O01 is AI-generated, confirmed by Dan. Never label it a real picture. See `Docs/memory/ro26-ai-pool-photo-correction.md` for exact asset identity; verify provenance before any real-picture label.

## First-round options and AI ideas: Claude and Codex use the same standard (Dan, 2026-10-16)

- Match AI clip concepts to the film's emotional tone. Entertaining means visually engaging and clear, not automatically comic: a somber personal-regret story may need restrained, credible scenes. Preserve Dan's explicitly chosen actions when developing frames, and do not add slapstick to a serious selection. This qualifies the funny-ideas defaults below; RO-25 uses the serious treatment Dan requested on 2026-10-16.
- Every new video's first review round includes visible colour-correction choices and playable, level-matched voice choices, including studio videos. Start from the approved source-specific look/sound, but show meaningful alternatives and recommend one. This replaces the 2026-10-14 studio exemption from options; an internal blind comparison does not replace Dan's audition controls. Preserve choices already approved for that exact film unless Dan reopens them. **A Short cut from an approved film reuses that film's look and voice with no options (Dan, 2026-10-20: "let's reuse that film's look").**
- Offer a broad range of funny, entertaining AI clip ideas tied to the actual spoken lines, following the 2026-10-11 ideation rule below. Literal illustrations are still useful where they fit. Give each idea a clear visual setup and payoff, with a short name and the surrounding speech; keep the action understandable in one viewing. Read the current Claude longform reference before adapting an older Codex recipe. Codex must not silently reduce the selection to one cautious idea.
- If Dan asks to choose text concepts first, deliver the ideas before generating their start/end frames. Frame selection and motion approval remain separate. A requested count applies to that job: RO-25 asks for ten ideas per each of six points and one selected AI clip per point; that does not impose sixty ideas on every video. His explicit six-point plan overrides the older approximate five-clip preference for RO-25 only. Generation spending limits still apply.
- All new or revised graphic copy uses title capitalization, including lower-third main points, headings, cards, and recap rows. **Eyebrow exception (Dan, 2026-10-20, from a side-by-side sample): the small label line above a graphic's main point (the eyebrow: "KEY POINT", "MOTIVATION", "REASON 2 OF 3", "THE LESSON") stays in CAPITALS; that is the standard.** The main point, headings, cards and list items stay in title capitalization. Do not uppercase text automatically in code or CSS. Preserve genuine acronyms and proper names; ALL CAPS emphasis is rare and deliberate, never a default on every card. This reaffirms the 2026-10-09 rule and replaces older uppercase topic/KEY POINT defaults.
- Offer colour options that vary a useful property on matching frames, and voice options on the same continuous spoken passage with matched loudness. If Dan asks for more saturation at the existing brightness or more bass, vary that requested property rather than substituting an unrelated adjustment. Keep source-specific quality checks and report actual gate outcomes.

## Scripted claim lines are already approved; never ask about them (Dan, 2026-10-14)

- **A claim line that is in the script Dan filmed is approved. Do not flag it, list it or ask him to approve it again.** Dan,
  on RA-06: *"Claim lines are okay, and going forward, you don't need to ask me to approve claim lines anymore. If they're
  in the script, then they're already approved."*
- How to apply: spoken lines and the captions that print them stay as filmed, with no "claim lines" decision on a review page,
  in a handoff or in a delivery report. This replaces the job docs' "claim lines flagged to me" step and the master list's open
  claim question (RA-06, RA-07, RA-15, RA-08, RA-16). Unchanged: on-screen GRAPHICS (cards, lower thirds, headlines) still
  never print a number, user count or comparison he cannot back (memory `ad-copy-no-unbelievable-claims`), and a line he
  ad-libbed that is NOT in the script can still be raised in one line.

## Junk footage between takes is never a cutaway (Dan, 2026-10-16)

- **A shot of Dan between takes (drinking water, looking away or down, resetting, waiting) is junk footage. Never use it as
  B-roll or a cutaway in any video, and never direct an editor to it.** Dan, on Muhammad's DS-11 Weigh Daily V3, where the
  clip of him drinking from his green bottle covered "your weight swings three pounds on water alone": *"I want to remove
  this clip of me drinking water at 43 seconds and just use the camera scene. Generally, I don't think this is a good clip
  to use. If we need something to illustrate water, we'll film new B-roll of me actually looking at the camera. This wasn't
  intended to be used as footage. This is just junk footage... make a note to not use these kinds of clips where I'm looking
  away and drinking water. That's junk footage between takes."*
- How to apply: a cutaway of Dan must be footage he filmed AS B-roll, acting the line out (the never-standing-around rule
  above). Raw-roll moments between takes are not B-roll even when they show the thing he names. If a line needs a picture
  that only exists as between-takes footage, leave him on camera and put the shot on the next shoot's B-roll list. Library
  clip `B0479` (the green bottle) is rejected; reviewers flag any clip of this kind in an editor's cut as a removal item.

## Stumbles inside a kept take get fixed (Dan, 2026-10-20, RO-20)

- **A stumbled, drawn-out or half-restarted word inside an otherwise kept take is junk footage: cut to a clean take of the line or trim
  the stumble out.** Dan, finalizing "Why You Should Invest More In Your Health" (RO-20) R4, about 0:33 ("if money is your most
  important priority", where "priority" ran 0.66 s with a half start): *"there was a small amount of junk footage included around 32
  seconds, where I said 'priority' and kind of started a little bit. In future videos, I'd like things like that to be fixed."* He
  shipped that one as is; the rule binds every edit from now on.
- How to apply: the delivery gate's `junk:repeated_take` row did not flag it (its stretch threshold is longer), and Whisper prints the
  word clean. Listen-check, or measure, every word over about 0.5 s inside a kept phrase and every intra-phrase gap over about 0.4 s
  in the first minute and at each take join; transcribe those windows with a disfluency prompt (for example `initial_prompt="Um, uh,
  pri- priority"`, `condition_on_previous_text=False`). Fix what is a stumble; leave his deliberate emphasis.

## Vacuum clips show the stomach and abs (Dan, 2026-10-28)

- For every stomach-vacuum demonstration, prioritize footage where Dan’s stomach and abs are visible during the actual draw-in. Use the full useful visible duration whenever possible; hands, arms, graphics and crops must not hide the teaching action.
- An initially blocked lead-in is acceptable only when needed and when the edit then includes all of the useful visible duration. For a short insert, or when only limited room is available, use the stomach-visible portion alone. Prefer removing blocked footage; do not spend the available insert time on it while omitting visible action.
- Inspect the actual source and delivered crop across the whole chosen span, record the visible/blocked ranges, and preserve natural speed and complete exercise action. This applies to all vacuum clips, real or AI, and future editor briefs. Dan set this rule while revising RO-30 B05.

## Never a shot of Dan just standing around (Dan, 2026-10-14)

- **A cutaway of Dan standing, posing or waiting, doing nothing that illustrates the line, is never used.** Dan, removing
  RA-06's physique-poses clip (library B0435) from "your goals, your body, and your injuries": *"Remove B1. That doesn't make
  any sense or add any value to the video. A shot of me just standing around. Generally, there isn't really any reason to put
  in the shot of me just standing around in the video. It doesn't really illustrate anything."*
- Same review, the exercise version: an exercise clip shows him actively DOING it (*"make sure I'm actively doing the vacuum
  when you show, not just standing around"*): for the stomach vacuum, the draw-in itself, not the hold before or after.
- How to apply: every cutaway of Dan must show an action the line is about (an exercise rep, cooking, using the app). Posing
  and standing B-roll (B0435, B0438, B0459 and the like) is not a cutaway; leave him on camera instead, or use a clip that acts
  the line out. It joins the phone-scrolling rule (B0437) below. Reviewers check every Dan cutaway for it.

## Short-form and ads: build the whole video instead of only the first 30 seconds when it is nearly approved (Dan, 2026-10-14)

- **For a Short or an ad, when most assets are already approved and nothing left in the rest of the video is likely to be turned
  down, the round that would deliver the finished first 30 seconds delivers the whole video instead.** Dan, approving RA-14 round 3
  (the first 30 s of a 50 s ad): *"I think it would have been better in this round to build out the full video because it would be only another 30 seconds.
  Everything else was pretty close to approval, and if we had to regenerate or re-render the video, then it wouldn't take that many
  resources. In situations like this where we have short-form content or an ad, I think it'd be better to just generate the whole
  video. In situations like this where most assets are approved and it's unlikely that anything in the last 30 seconds would be
  disapproved."*
- How to apply (editor's reading): it is the round that would otherwise be "the first minute / first 30 seconds" (PRE-RENDER-APPROVAL
  step 5). If the remaining part only adds a few seconds of render and holds no new or unapproved kind of item (no AI clip whose frames
  or motion he has not seen, no new graphic family), build and show the whole video in that round, with the moving previews of the
  remaining items still on the page. If something in the rest is genuinely uncertain (an unseen AI clip, a new graphic type, a look he
  has not picked), keep the first-30-seconds step. Long-form content is unchanged: first minute, then the full film.
- The approval gates before it are unchanged (look options, every graphic and clip shown, AI frames before motion). Delivery to the ad
  folder still needs the exact-file gates and the independent review; a whole-video review copy shown in a round is a review copy.
- Why: on RA-14 the first 30 s round came back fully approved and the remaining 20 s held only items Dan had already seen moving, so
  stopping at 30 s cost him a whole extra round for a render of a few minutes.

## Historical outdoor/studio distinction (2026-10-14; first-round colour/audio exemption superseded 2026-10-16)

- **Every video shot OUTDOORS, ad or content, shows Dan colour correction options, audio options and cropping options in
  its first round, and he picks.** Dan, choosing RA-14's round 2 options: *"Let's make this standardized for first-round
  edits of outdoor videos going forward... Outdoors, we need to look at color correction, audio, and cropping options every
  first round for every outdoor video going forward. Ad or content: always show those options first round."*
- **Studio videos use the standard look and sound without options:** *"In the studio, when we have everything
  standardized, I think that we can basically make the color correction and the audio standard. Just do it the way we've
  always done it."* Still run the source check in PRE-RENDER-APPROVAL step 1 (a studio roll that measures differently is
  the exception, and says so).
- How to apply (editor's reading): outdoor round 1 page carries three colour candidates beside frames of approved videos
  (with round 1's or the reused look shown for comparison), two or three wider/tighter framing pairs as stills on the same
  two moments with their crop values, and the voice options on the player. Recommend one of each; Dan picks. Run the
  bake-off yourself first (PRE-RENDER-APPROVAL, "Before Dan sees anything") so the options are worth his time. The
  RA-14 round 2 page (`ad-edit/reference/ra14/round2/`, lessons in the ad-edit skill) is the worked example.
- Why: RA-14 reused RA-01's pool look and framing in round 1 without options and Dan sent both back ("a little bit too
  tight", "we can do better with the color corrections"). The light outdoors changes from roll to roll.

## The analysis card is Soft Blue Light, built with HyperFrames, in every video (Dan, 2026-10-14)

- **The body-fat / fat-to-lose / muscle-to-gain analysis card (the RA-01 card he asked to reuse) is redrawn in Soft Blue
  Light with the HyperFrames templates, and that version is the standard for every video from now on.** Dan, on RA-14:
  *"Redo the analysis card in our graphics in soft blue light with our hyperframes. Make that standardized with the rest
  of our videos."*
- Keep what he approved on RA-01 (subject picture, scan line, the three bars, the plan band, no printed numbers, one
  label chip placed by person mask); change only the look. Build it once as a shared template beside the other
  HyperFrames templates and point `_shared/adkit/analysis_card.py` users at it. The J2 version stays only for re-exports
  of films already approved with it (RA-01).

## A revised thumbnail or cover is shown to Dan before it is installed (Dan, 2026-10-22, SL-18)

- **When Dan asks for changes to a picked thumbnail or cover, build the revision, show him the finished file (every layout), and
  install, upload or schedule it only after he approves that exact file.** Dan, after his Short 2 cover D revision was installed
  straight into Blotato: *"I want you to have me approve the final short before you install in the future."* (Editor's reading:
  "short" means the short's cover, the thing that was installed without his look.)
- An unrevised pick from the review sheet still goes straight to setup. Already scheduled posts keep their current cover until he
  approves the replacement; then swap it everywhere it is used (Instagram, YouTube, the TikTok cover-first copy, the Facebook cover
  registry and the live installer) and read each back.

## Revised covers and thumbnails: show Dan before installing (Dan, 2026-10-22)

- **When Dan asks for any change to a cover or thumbnail he picked (new text, new image, any revision), build it, show him the
  finished file in every layout, and stop. Install, upload or schedule it only after he approves that exact file.** Dan, on the
  SL-06 Top 5 Zepbound Tips covers (text changes on five picks, queued without his look): *"Show me the covers that I gave
  revisions to review. I didn't approve them yet... Let's make this a standard rule going forward. If there are revisions, you
  show them to me to review before we install."* The same day, on SL-18: *"I want you to have me approve the final short before
  you install in the future."*
- A pick from the review sheet with no change still goes straight to setup. A pick with a revision is a stop point: everything
  else in the setup (media backups, TikTok copies, captions, configs) may be prepared meanwhile, but nothing carrying the revised
  cover is queued or installed until his OK. If he named no letter for a short, that is a question, not a default.
- Binds Claude and Codex, `/video-setup`, `/ad-setup`, `/coverimage`, `/youtube-packaging`, and any cover swap on a live queue.

## YouTube thumbnail text: capitalize the first letter of every word (Dan, 2026-10-28)

Dan: "Let's make this a rule going forward that we always use title capitalization with the first letter of each word capitalized in our YouTube thumbnails."

- Every new or revised YouTube thumbnail uses the first letter of **every** word capitalized, including short words such as "At", "In", "To", "Me" and "And". Preserve proper names and genuine acronyms such as "YouTube" and "AI".
- Example: **This Boring Daily Routine Got Me Abs At 41.** Sentence case and automatic ALL CAPS are no longer the default for thumbnail copy. This supersedes older thumbnail recipes that force uppercase text.
- Apply prospectively; preserve existing approved thumbnails unless Dan asks to revise them. This thumbnail text rule does not change words or capitalization inside an approved film.

## Thumbnails: the five, each its own design, always made by Codex (Dan, 2026-10-25)

Dan changed the standard after choosing C for all five Calories Shorts: he chooses AI images of himself most often and rarely picks covers without him. This replaces the 2026-10-13 pool + studio + one AI Dan + two discretionary mix for new cover and thumbnail sets. Existing approved files and picks stay locked.

- **The initial five, every video:**
  1. An AI-generated or AI-enhanced image of Dan acting out the video's topic.
  2. A second AI-generated or AI-enhanced image of Dan in a different topic-relevant scene, action or composition. These are two distinct concepts, not crops of one picture.
  3. One real photograph of Dan from EITHER the pool OR studio shoot, chosen for the strongest image. A separate photo from each shoot is no longer required.
  4. and 5. Two concepts at Codex's discretion, chosen for how likely Dan is to pick them based on his actual approved-cover history. They may show Dan, including more AI Dan, or omit him when there is a strong visual reason. Do not fill these slots automatically with object-only or no-Dan designs just for variety.
- **Learn from the picks before planning:** inspect recent `covers/approved-*/picks.json` and the corresponding selected images, not only proposed sheets. Use `Docs/memory/cover-picks-ai-dan-acting-topic.md` as a guide to earlier evidence. Calories Shorts (SL-08, 2026-10-25) adds five more C picks: recognisable lean Dan, naturally acting out the exact topic, clear abs and readable type. Record the new pick with its actual final asset hashes. Carry forward winning qualities while keeping five genuinely different designs; do not force every design into the yellow-band layout.
- **Five unique designs:** vary layout, typography, colour and composition, and write one design line per option before building. Same approved copy across the five unless Dan asks for copy options.
- **Codex always makes them on Dan's subscription:** `_shared/codex-image.sh` with the newest supported stable GPT at high effort, currently `gpt-6.1-sol`. No outside image model or paid still-image API by default. Claude setup tasks call that helper; Codex tasks use it directly.
- **The real-photo choice stays real:** preserve the original face and body pixels, generate only its background, then composite the real cutout and type locally. Any AI Dan choice gets a real identity reference, the prompt "lean and shredded, not bulky, same size as the reference", and an actual face check before review. This explicit permission covers the two required AI Dan choices and any additional discretionary AI Dan choices.
- **Review and installation:** show all five, then stop for Dan's actual picks before uploading or scheduling. Shorts still get separate Instagram and YouTube layouts per choice. Keep text off face/hair; no frowning default, visible standing swim-brief shape, website mark or real-photo label. A requested revision to a picked cover needs approval of the exact revised files before installation. The full quality and disclosure rules keep their existing scopes.

## Pickups are recorded on the studio set at a shoot, not on the desk mic (Dan, 2026-10-13)

- **A pickup line for any video goes on the next shoot's list and is recorded on the studio set with the shoot's clip-on mic.** Dan,
  after hearing desk-mic pickups laid into the RO-20 first minutes: *"Yeah, that audio doesn't work. What I'm going to do is I'm just
  going to record these pickups on my studio set instead... get all of the pickups that we need for this task and every other
  outstanding video edit that we have... For pickups, I'll just do those first to make sure we get them, and then I'll just upload
  the pickups."*
- What was tried first: the desk Yeti, tone, level and room matched to the film voice over three passes. A blind listener still called
  every join "closer, drier, fuller", and Dan rejected it on first listen. Do not spend a round on matching a desk recording again.
- How to apply (editor's reading): when a video needs a pickup, write the line, add it to the shoot's pickups list (a PICKUPS section
  at the top of the shoot doc and a pickups-only teleprompter document loaded into PromptSmart; for the next shoot:
  `Docs/PICKUPS_1017_SHOOT.md`), tell Dan the job waits for the shoot, and build the rest. A desk recording is fine as a timing
  placeholder so the pictures can be built and approved, labelled as a placeholder. Each pickup is printed twice in the teleprompter
  document so he reads it twice.
- This replaces step 3 of "A Short opens like a dedicated video" below (record into the desk mic in the editing session). The rest of
  that section stands: the pickup line, the cover clip, one point per Short.

## AI clips that make no physical sense, or do not show the line, never reach Dan (Dan, 2026-10-13)

- **An AI clip is checked for sense before Dan sees it, and a clip that fails is regenerated, cut down to the part that works, or
  dropped. It is never sent to review with the oddity described as "a gag".** Dan, on the RO-08 round 2 film, about three clips the
  editor and two independent reviews had passed: *"when he grabs the muffin out at the end, all the donuts just disappear, vaporize,
  and go nowhere. It doesn't make sense. We need better quality control on these clips, so things that look like AI slop like this get
  caught in quality control and don't make it to my review."* And: *"The water jumps up in the air for no reason. Not clear how that
  water jumping in the air is connected to the guy or that it is hungry... It makes no physics sense what's happening in this video.
  It doesn't support what I'm saying. These types of clips should be caught in QC going forward."* And of a third: *"I don't think
  that illustrates the idea well, or the joke really lands here."*
- **The three questions, asked of every take at playback speed, by the editor and again by the independent reviewer (put them in
  the reviewer's brief, one answer per clip):**
  1. **Does everything obey cause and effect?** Nothing vanishes, appears, melts or changes by itself. Food that leaves the plate is
     eaten or carried; an object that moves is moved by something the viewer sees.
  2. **With the sound off, would a stranger say what the clip is showing?** If the answer needs the prompt to explain it (the water
     ripples because his stomach rumbled), it fails.
  3. **Does it show the line he is saying, and if it is a joke, does the joke land in one viewing?**
- A time jump (a clock moving an hour, a full box becoming an empty one) is shown with a CUT between two natural shots, never by
  asking the model to fast-forward inside one take.
- **Standard on every video, before Dan's FIRST look at any AI clip (Dan, 2026-10-14, approving RO-08 round 3).** *"I like how you
  cleaned up those AI clips... I'd like you to do these kinds of checks as a standardized thing going forward, so ideally, this is caught
  before I review it for the first time. You can spend a little bit more aggressively on regeneration to facilitate that, but I want you
  to catch these kinds of mistakes before I see them."* How to apply, Claude and Codex, every skill that puts an AI clip in front of him:
  1. Every take gets the measured check below and the three questions from the editor, then from a fresh independent reviewer with the
     three questions in its brief, before the first page or review copy that shows it moving. Not only after he has rejected something.
  2. A take that fails is fixed before he sees it: regenerate it (a retake from the approved frames, or two short takes joined by a cut),
     or cut it down to the part that passes. Do not send it with the fault described, and do not hand him the choice of fixes.
  3. Spend on retakes more readily than before: retakes of approved frames inside the video's AI budget need no question. At the cap,
     ask for more first (the budget rule below), never ship the fault.
  4. Plan for it: expect a retake or two per clip, and say so in the round 1 cost estimate.
- His order of repair, said about the donut clip: *"regenerate this so it looks natural. Use a part of the clip only. If you can't
  make it look natural, eliminate all the food just vaporizing into the air and disappearing. If you can't make it look natural, then
  just use the camera scene here."* The camera scene is always an acceptable result; a bad clip is not.
- **At the budget cap with clips that still have obvious problems, ask for more budget. Never ship them.** *"If we hit budget but
  the clips are still having obvious problems, then I would rather you ask for authorization for more budget than ship something
  with shitty clips like this."* Put the ask first in the message, alone, with the number.
- **About five AI clips per video at most, chosen by Dan from many ideas.** *"I like the approach that you took of generating many
  ideas and certain end frames for AI clips... I'm just going to be a little bit more selective in what we generate. Maybe a max of 5
  clips per video, but keep coming up with lots of ideas. I'm just going to reject more of them."* Nothing changes in what is offered
  (2026-10-11 rule below); expect about five approvals, and spend the rest of the budget on retakes of those.
- This narrows "AI clip faults: judge at playback speed; small faults pass" (2026-10-08, below): that rule covers a fault of a few
  frames inside an action that makes sense. It never covered what the clip shows happening.
- **How to check question 1 (added 2026-10-13, after RO-08 round 3 needed three renders): measure it, do not only look.** For each shot of
  an AI clip, compare its first frame with its tenth over the whole picture (tolerant of a pixel or two of drift), mask out the person, and
  look at every region left, enlarged, frame by frame. Two independent reviewers each found a leftover of the rejected effect that the
  editor's eye had passed on a contact sheet: a wisp on the desk, then an orange smear in the box. A cut out of a rejected take starts where
  the whole picture has settled, not where the subject has. Tool: the self-change map in `longform-edit/reference/ro08/a5_cut.py`.
- **A body cut off unnaturally never reaches Dan (Dan, 2026-10-21, RO-28 barbecue frames):** four men stood behind a grill with their lower
  bodies cut off and it passed two checks. Dan: *"the lower bodies are cut off. This looks very unnatural. That never should have made it
  to my review."* Every frame reviewer brief asks whether each person is whole where the shot implies it (feet in a standing group shot,
  nobody sliced by the frame edge or hidden behind a prop placed to crop them); a frame that fails is redrawn before any page.
- **START/END frames get the same treatment before motion is even generated (2026-10-14, after RA-04's leg press):** a frame spec, the
  frame gate and a fresh `frame-reviewer` agent; no page shows the pair until `.claude/skills/_shared/framecheck/gate.py START END
  --verify` exits 0. Routine and proof: `_shared/framecheck/README.md`.
- **Every motion take gets the motion gate before any page shows it (2026-10-14, after RO-08's donut take):** the same spec, then
  `.claude/skills/_shared/framecheck/clipcheck.py TAKE --spec spec.json [--frames A:B]` (point tracking: anything that vanishes in
  place or comes from nowhere, parts off their guide, slipping contacts), then a fresh `frame-reviewer` on the take; no page shows it
  until `clipcheck.py TAKE [--frames A:B] --verify` exits 0. It caught the donuts on the take Dan rejected and passed the parts that
  shipped. It does not judge cause and effect (A3's water): the reviewer's three questions still do. `_shared/framecheck/README.md`.
- Why it was missed: the editor wrote both faults on the review page ("around its fifth second the junk clears in one sweep", "the
  rumble reads as water splashing up out of three glasses") and shipped them anyway, and the reviewers were asked about frame faults,
  labels and lip sync, not whether the scene made sense.

## A lip sync that fails its check once goes in without lip sync (Dan, 2026-10-12)

- **If a lip-synced AI clip does not pass the quality check on the first try, use the clip with no lip sync: the character keeps his
  mouth shut and reacts while Dan's voice does the line.** Dan, approving RO-20's silent "fat guy who has money" after three failed
  sync attempts: *"I think generally this is a good way to handle it: if our lip sync fails the first time and doesn't pass the
  quality check, just do it without the lip sync if it's too challenging."*
- The check comes before he sees it: measure the mouth against the audio (`longform-edit/reference/ro20/lipmeasure20.py`) and look at
  a close-up strip of the mouth on the words. The round 2 clip went out unmeasured and he rejected it on sight ("doesn't match up at
  all").
- How to make the fallback: one take from the approved START frame with the mouth closed in the prompt, the way the approved
  non-speaking "brokie" clip works. Do not spend on a second or third sync attempt. This narrows the excuse-voice rule below: lip
  sync is still the first try for an excuse-voice line.

## A subtle bass lift on his voice is the standard (Dan, 2026-10-12)

- **Every video we mix ourselves gives Dan's voice a subtle addition of bass.** Dan, picking the RO-19 voice from seven options
  (four warm with less room echo, three of those with more bass): *"For the voice, let's go with B2 with more bass. Let's make
  a subtle addition of bass to my voice the standard for all Claude and Codex video editing skills. I like that better than
  the default, just the echo removed."*
- What B2 is (measured, 2026-10-11): the warm fixed tone shape (`highpass=f=70`, +1.5 dB at 140 Hz, a dip at 450 Hz, -1 dB at
  3.2 kHz), the chain's light dereverb on a wet room (alpha 0.30, floor -10 dB), no expander, plus **a wide +3 dB lift at
  120 Hz** (`equalizer=f=120:t=q:w=0.8:g=+3.0`). Its lowest speech band then measures the same as the reference voice (5.4 dB).
  +1.5 dB was too little to be his pick and +4.5 dB measured close to boomy.
- How to apply (editor's reading of "subtle"): start every new voice from the +3 dB lift at 120 Hz on top of that film's approved
  tone, pass it through `voice_chain.py --eq` until the chain has a named option, keep the 70 Hz high-pass so the lav's handling
  rumble does not come up with it, and listen for boom on his loudest lines. A room or microphone that already reads full
  (lowest band at or above the reference) gets less. Still show voice options on a new set; the bass version is now the
  default candidate, not an extra.
- Unchanged: an editor's finished mix is delivered untouched; never process past the reference; the audio gate's tone row
  fails on any fixed tone shape, which is the known mismatch, not a reason to drop the lift.
- Same review, photos: a "pale before" picture has to read as PALE, not as out of shape. He turned down a soft-looking one
  (*"I'm just looking more fat and not just pale"*) and asked for one with defined abs. And check a personal photo for a
  filter before using it as a before picture: the pale half of an approved pair was a tan-filtered copy (*"The original was
  significantly more pale. Find the original"*). In his Photos library, smaller same-second copies are edits of the full-size frame.

## More AI clip ideas, funny ones, on every video (Dan, 2026-10-11)

- **Offer more AI clip ideas per video than feel safe, and make most of them funny and entertaining.** Dan, approving all four
  RO-19 frame pairs (a vampire under an umbrella on a beach who ends up tanned, a man sprayed traffic cone orange, a brown
  body print left on white sheets, and one straight clip of the appointment itself): *"All of these are funny and
  entertaining, and I think they will make people accept the AI clips... Going forward, I want more of these funny,
  entertaining AI clip ideas, and I want you to come up with more ideas for AI clips. I am accepting nearly all of them, and
  I should be rejecting maybe a third of them. Basically, it's not too big of a deal if I reject the clip."*
- How to apply: if he approves every idea, too few were offered. Aim for a set where about a third could be turned down:
  on a long-form, bring roughly six to nine frame pairs to round 1, not three or four. Frames are made on the Codex
  subscription, so extra ideas cost no generation budget; motion is generated only for the ones he approves, inside the
  per-video cap (say so if the approved set would pass it, and let him pick).
- A straight, literal clip is still right when it shows the thing the video is about and no real footage exists (his words on
  the appointment clip: *"not funny... but that just illustrates our concept perfectly. Highly relevant."*).
- Same review: a stock "doctor" clip used many times was called weak. He asked for a reusable AI clip of **a man who looks
  like the prospect talking to a male doctor**, for every "talk to your doctor" line. Once approved it goes in the clip
  library and is the default for those lines. **It is library clip `A0166`** (approved in RO-19, 2026-10-13).

## Audio comparison clips start on speech (Dan, 2026-10-11)

- **Every audio comparison or audition clip starts with him speaking in its first second and is speech throughout.** Dan, on
  the RO-19 voice options: *"you didn't choose a good clip for that because the first 28 seconds were nothing... going
  forward, just always make sure it starts with speech immediately."*
- What happened: the audition window was typed as a roll time (166 to 197 s) that fell in the gap between two takes: 27 s
  of room tone and 4 s of speech. Nine blind listening trials were run on it and a voice was chosen from them. All of it
  was void, and nobody had listened to the clip.
- How to apply: take the window from the CUT (a kept piece's own start), never from a typed roll time. Before any trial,
  measure it: speech in the first 0.5 s and no pause over 1.5 s (print the level in 1 s steps). Then listen to one option
  yourself or have the listener confirm it hears continuous speech. `audio_options` scripts must refuse a window that fails.
- When he asks for voice options, build what he names (here: four warm, less-room-echo versions and a few with slightly
  more bass), level matched, on one clean window.

## A Short opens like a dedicated video: record a pickup, never "Number two" (Dan, 2026-10-11)

- **A Short cut from a long-form must not sound like a piece lifted out of a longer video.** It never opens on a list
  number or any line that points back at the long-form ("Number two", "Number three", "next", "also", "this one", "as I
  said"). Dan, on the SL-06 Zepbound shortlist: *"I want to make this a rule for our shorts going forward: avoid making it
  very obviously seem like something cut from a long-form video out of context, like starting with number 2 or number 3.
  Instead, we'll just record a short pickup into my mic right here in Claude, and then cover it with a graphic or AI clip
  or something."*
- **The fix is a pickup: one new sentence Dan records that states the Short's point as its own video.** His examples:
  *"Here's why you should inject Zepbound every Thursday evening"* or *"Here's why Thursday evening is the best time to
  inject Zepbound."* The pickup replaces the list opening; the film's footage starts on the next sentence.
- How to apply, every Shorts batch (Claude and Codex):
  1. At segment selection, mark each candidate whose first line points at the long-form. Trimming the number off is only
     enough when what is left reads as a dedicated opening.
  2. Write the pickup lines (three options each, through `dan-voice-writer`) and **put them in the shortlist message
     itself**, with the line that follows each, so Dan can record them when he picks.
  3. **Superseded 2026-10-13 (section "Pickups are recorded on the studio set"):** the pickup is recorded on the studio set at the next shoot; a desk recording is only a labelled timing placeholder. The desk method, kept for placeholders: Dan records into his mic in the editing session. Take every line two or three times and keep the best take.
     **Record with `_shared/audio/rec_mic.swift`, never `ffmpeg -f avfoundation`** (2026-10-12): ffmpeg dropped 11 % of the
     Yeti's audio on a busy Mac (a 512-sample block missing about every 90 ms; 26.6 s of samples per 30 s) in three takes
     out of three, and Whisper still transcribed them. Build once: `swiftc -O rec_mic.swift -o ~/.cache/absbyai/rec_mic`.
     `rec_mic OUT_DIR MAX_SECONDS [SEGMENT_SECONDS]` writes 30 s WAV segments and stops when `OUT_DIR/STOP` exists. Check
     every take: samples recorded against wall time (its last line prints both). Dan often has several sessions open and
     reads the lines when he gets to that one, so leave the recorder running in the background with a watcher that
     transcribes each finished segment and stops it once every line was heard twice; say so in chat, with the time limit.
  4. The pickup has no picture of him saying it, so **cover all of it with a clip, a graphic or an AI clip** (clip library
     first; a new AI clip goes through frame approval), then cut to him on camera on the first film word.
  5. Match the pickup to the film's voice (level, tone, the film's music bed under it) so the join is not heard. The
     film's approved mix stays untouched after the join. Say in the build report how the pickup was treated.
- **One point per Short.** Same review: *"It's a little confusing to have two points in a video like that."* A candidate
  that argues two things (pen versus needle, and which dose) is split, and each half goes where it belongs.

## All B-roll is colour corrected before it goes in a video (Dan, 2026-10-11)

- **Every piece of B-roll is colour corrected to sit with the film's approved look before Dan sees it, in every video.** Dan,
  on the RO-20 round 1 page (three of his own pool clips looked far darker than the kitchen footage around them): *"I like
  these clips, but I want you to use the color-corrected versions. This looks very dark... make sure to use color-corrected
  footage, not this dark raw footage. Let's make that a rule going forward for all the B-roll you're using... Color correct
  all B-roll used in this video and all videos going forward."*
- How to apply: grade each B-roll clip (library `B####` cuts of Dan, raw rolls, and stock that reads dark or off) against
  the presenter frames it will cut next to: measure his skin, then LOOK at the clip's still beside a talking-head still. A
  library note that says "graded" is not proof: B0455, B0456 and B0434 carried the S-Log3 LUT and still read very dark
  (low sun, shade). Where a grade cannot rescue a clip, pick one that is already bright ("or just use the ab wheel or
  something already color-corrected"). A B-roll still visibly darker than the presenter frames around it is a defect the
  editor fixes before the review page goes out.
- **Never raw footage, ever (Dan, 2026-10-23, RO-28 round 3).** Dan on the jump-rope pool clip at 2:22: *"This is raw footage.
  I want you to color correct this footage. Let's make this a standing rule: never, ever use raw footage. B-roll only:
  color-corrected footage in these videos."* That clip had a grade: a gamma lift that brightened the shade but greyed the
  blacks and flattened it, so it still read as raw. The first fix overshot the other way (25% of the frame crushed to black,
  twice the saturation, neon greens) and the independent review failed it. **Match by measurement:** grade the clip until its
  black share (luma < 16), median saturation and median brightness sit inside the range of the film's approved B-roll from the
  same shoot, then look at the stills side by side. RO-28: references 10-17% black, saturation .27-.38, median 54-70; the shade
  clip passed with a midtone curve and saturation 0.90 (`POOL_SHADE`), never a gamma lift alone and never crushed blacks.
  A flat, grey, washed-out, crushed or neon clip is a defect before any page goes out.
- This binds Claude and Codex, every video skill, and every editor brief and revision doc.

## A person looking at a phone is not a picture; never use the clip of Dan on his phone (Dan, 2026-10-11)

- **Library clip `B0437` (Dan checking his phone by the pool) is never used in any video.** Dan: *"I don't want you to ever use
  this clip again. This is just me looking at a phone. It's not appropriate, really, to ever use. Make a note to never use
  that in any video."* It is marked rejected in the clip library.
- The same day he cut a stock clip of a man scrolling his phone: *"It just shows a guy looking at his phone and doesn't add
  any value."* How to apply: a cutaway of someone looking at a phone illustrates nothing. Show what is ON the phone (the
  approved dating-app AI clip `A0089`, an app screen in the phone shell), the scene the line describes, or a graphic that
  makes the point (he supplied a diagram for "winner take all" and asked for a full-screen graphic with text beside it).

## A hard-to-picture idea gets a funny AI clip, not a forced literal one (Dan, 2026-10-10)

- **When a line has no straightforward literal picture (a saying, a metaphor, an abstract point), make the AI clip funny on
  purpose: an obviously unreal, cartoonish gag that acts the line out.** Dan, approving RO-07's A3 frames ("life is going to
  punch you in the face": a giant cartoon boxing glove on a spring comes through the front door and knocks the man off his
  feet): *"I think a lot of times, when we have a hard-to-illustrate AI concept like this (where there isn't a
  straightforward literal clip to generate), doing something funny like this is good. It's obviously not real, but making it
  funny, I think, is going to make it more accepted by the viewer. This looks like it'll be real funny and entertaining. I
  really like this one."*
- How to apply: when writing AI clip concepts, sort each line first. A line with a real literal picture (sore after a
  workout: a man easing down the stairs) gets that picture, played straight. A line without one gets a slapstick or cartoon
  idea, offered as start and end frames like any other new AI clip. Make the gag big and readable in one glance (his round 1
  note on the first version: the glove was too small and came from the wrong place). It joins the lip-synced "excuse" clips
  and the slap he liked on RO-06 (below).
- Unchanged: frames are approved before motion, the per-video generation budget, the AI label, no fat pinching or belly
  framing, and the first-30-seconds rules.
- Same review, two trims (they bind every exercise clip, real or AI): **a clip of an exercise shows the rep from its first
  second**, not the hold before it (his handstand push-up piece opened on a static handstand), and **a clip of a lift shows
  the lift itself**, not only the setup (the AI deadlift before A2 showed him gripping the bar and cut away before it moved).
  Never run a library clip into text or marks burned into its tail, or into the frozen frame that often sits under them: print the
  frame-to-frame change of the clip's last two seconds before trimming near its end (RO-07's deadlift clip was a still for 0.6 s before its
  red X, and a trim that only avoided the X ran into the freeze).

## Codex's-choice thumbnails: every image is its own design (Dan, 2026-10-10; widened to all five on 2026-10-13, top of this file)

- **When Dan asks for "three AI designs of Codex's choice" (or any set of options with the designer's choice), each image is a different DESIGN, not a different picture dropped into one layout.** Dan, on RO-06's sheet: *"These all essentially have the same design with different images... For Codex's choices going forward, I want a unique design on every image. We're not just putting the same image or different images in the same design five times."*
- How to apply: before building, write one line per option naming its layout, type treatment, colour and composition, and check that no two share them. Vary the headline placement (left stack, centred, bottom band, over-the-shoulder, split panel), the type style and colour, the subject scale, and the concept (object hero, before/after split, price tag, comparison, close-up detail). The same bar-plus-two-lines on the left over five backgrounds fails. Same copy is still fine; the design is what changes. The real pool and studio photos can keep the house layout; the three AI options may not.
- Applies to Claude and Codex, every thumbnail and cover task (`/video-setup`, `/ad-setup`, `/coverimage`, `/youtube-packaging`).

## A cutaway shows the thing he is naming (Dan, 2026-10-10)

- **When Dan names a piece of equipment, a food or a product in a line, the clip over that line shows him using that very thing.** Dan, finalizing
  RO-06: *"I referenced the medicine ball... but then you showed images or a clip of me doing toe touches without the medicine ball. That would
  have been a little better. Show me doing toe touches with the medicine ball... For the future, if I reference the medicine ball, it'd be better
  to show something where I'm using the medicine ball rather than something unrelated."*
- How to apply: for every cutaway, read the sentence it covers and write down the object he names. Search the clip library for that object plus
  the exercise (`clip_library.py find "medicine ball toe touches"`); the right exercise WITHOUT the named object is the wrong clip. If no clip
  shows it, prefer another real clip that does show the object, then leave him on camera, before using a look-alike. This also binds a cutaway
  that is moved or lengthened to cover something else: re-read the words it now sits over.
- He did not ask for a new round over it (RO-06 9:32, clip B0467 over "I prefer the medicine ball though"): a small miss, noted for next time.

## The app feature tour beside Dan is approved for reuse (Dan, 2026-10-10)

- **RO-06's closing scene (15:44) is approved and saved: Dan on camera, moved right, with the app in an upright phone on the left third, showing
  the home screen, a tap, calorie tracking from a meal photo, a tap, then AI workout demo videos.** Dan: *"I liked what you did with the clip at
  the end. That's something I think we want to reuse. Showing the calorie tracking and the workouts, I think, is a couple of our strongest
  features. I really love what you did at the end. Make sure to save that for future reuse."*
- Reuse it wherever a video says what the app does beyond the goal picture (the call to action of a content video, a website or ad line about
  features). Lead with calorie tracking and workouts. Clip library: `B0544` is the phone screen alone (432x920, 10 s, lay it in the approved
  shell beside the presenter); `B0543` is the finished RO-06 scene (his lips say that film's line, so it is a reference, not a drop-in).
- Rebuild or retime it with `longform-edit/reference/ro06/phone_side.py` (screens captured from a local copy of the app by `appcap6.py`):
  one fixed presenter position, the phone never on his face, both arms inside the frame, AI-GENERATED on the exercise videos, and none of the
  banned screens. It sits beside the two other approved app demos (the self-generation demo and the workout-app format, further down).

## Capital letters in graphics: emphasis now and then, not in every graphic (Dan, 2026-10-09)

- **Title capitalization is the default for every lower third, card and label. FULL CAPS on a word is for the rare graphic
  where that word truly carries the emphasis.** Dan, on RO-07 round 1 (he sent 16 of 45 lower thirds back to normal
  capitalization): *"With the graphics, a lot of the time you're just blindly capitalizing words in a very AI-slop
  deterministic way... Capitalizing these words in the graphics is good every now and then when we need to make emphasis
  on a word, but if you're just capitalizing random words in every graphic, then there is no emphasis. I need you to use
  more subtlety and judgment, not a deterministic rule."*
- How to apply: write every point in title case. Then pick, across the whole film, the few graphics with a real contrast
  or punch word (editor's reading: about one in six at most). Exercise names, round and section labels, times of day,
  app names and list items never take capitals. This narrows the 2026-09-18 KEY POINT format further down this file
  ("the one or two words that carry the punch in FULL CAPS"): that is allowed, not required.
- Same review, workout B-roll: choose the clip where Dan looks ripped and well lit, not the first that matches the
  exercise; start it on the first rep; prefer his real footage of an exercise over an AI demo (memory
  `broll-choose-where-dan-looks-best`).

## The first 5 seconds get the most effort (Dan, 2026-10-08)

- **On every content video, short or long, the first 5 seconds are planned and reviewed as their own piece.** Dan:
  *"For the shorts and for content generally, I want to pay more attention to the first 5 seconds. I want to get more
  ideas for AI-generated clips in the first 5 seconds where I feel like we need more attention and effort put in
  there. I want you to request AI clips, put in something we already made, or put in something attention-getting in
  the beginning more often... Sometimes we just start with a camera scene, but I feel like you should look for more
  opportunities to make the first 5 seconds more attention-getting... putting more effort into the first 5 seconds."*
- How to apply, in every edit, plan, handoff and editor revision doc: write down what is on screen from 0:00 to 0:05,
  then try to beat it with, in order, (1) a clip we already made (clip library, AI or real), (2) the most
  attention-getting picture from later in the same video moved to the front (the exercise done correctly, the finished
  dish or result, the before picture), (3) a new AI clip concept, offered as two or three ideas with start and end
  frames for approval. An exercise how-to opens on about 3 seconds of the exercise done correctly, then cuts to Dan.
- A plain camera open is still allowed when it is truly the strongest option. Say why in one line (the "What I
  decided" list, the build report, or the revision summary). A script cue that says "cold open on Dan" does not settle
  it.
- This strengthens "Frequently, not always, a video opens on an AI-generated clip" (2026-09-27, below): the default
  now leans toward an opener, and the camera open is the exception that needs the reason. The first-30-seconds rules
  still bind (no belly-fat framing, frames approved before AI motion, the applicable per-video generation budget below).

## Jump rope footage: the fast skip is correct, the both-feet clip is a mistake demo (Dan, 2026-10-09)

- **Whenever a video shows Dan jumping rope, use the footage of him skipping quickly over the rope, foot to foot, like a
  boxer.** Library clip `B0448` (roll C1674, the high-knee stretch, about 155 steps a minute).
- **The clip of him jumping over the rope with BOTH feet (`B0430`) shows a mistake. Never use it unless Dan is saying, in
  that moment, that jumping with both feet is a mistake.** Dan: *"I want to make a standing rule that this clip of me
  jumping over with both feet is meant to show a mistake. This clip ... should never be used in videos unless I'm saying
  it's a mistake to jump over with both feet. Basically, this clip is a mistake. Don't use it unless I'm illustrating a
  mistake. Always use the correct jump rope footage of me quickly skipping over the rope, not the beginner footage of me
  going very slowly foot by foot, but the footage of me skipping quickly like a boxer would."*
- **The slow foot-by-foot clip (`B0447`) is the beginner demo.** It is not the correct-form clip either: use it only where
  he is teaching how a beginner starts.
- This binds every video, every editor brief and every revision doc. The clip library descriptions of all three carry
  the rule. When a film needs jump rope twice, take a different part of the fast stretch of roll C1674, not the same frames.
- Why: RO-06's jump rope section (3:51) used the both-feet clip as plain "Dan jumping rope".
- **Repeated 2026-10-27 (RO-28): the 10/15 shoot's pool roll `C1742` is also a both-feet jump** and went out as plain jump rope
  at 2:22. Dan: *"Save that to memory because this issue has happened a few times. Don't use that clip of me jumping with both
  feet. Use only the clip of me one foot at a time, unless we're specifically showing that mistake."* Before using any jump rope
  footage of Dan, from the library or a raw roll, watch it at speed and confirm the feet alternate fast; a raw roll is unverified
  until you have looked. Default to `B0448` / `B0542`, colour matched to the film.

## The "excuse" voice gets a lip-synced AI clip, frames first (Dan, 2026-10-08)

- **When Dan does his "excuse" voice (an impression of someone whining an excuse, such as "Dan, I don't have time to go to
  the gym"), plan an AI clip of a character saying the line, with the character's lips synced to Dan's own recording, and
  bring its start and end frames in the first approval round.** Do it without being asked.
- Dan, approving the RO-06 first minute: *"I really love the way that you did the lip-syncing and the slap. Both of those
  turned out significantly better than I expected. I think in future ones where I'm doing the 'excuse' voice, like making
  fun of losers making excuses, let's get started in frames for those in the future because this turned out real good."*
- How to apply (editor's reading of "get started in frames"): on every script, outline and edit, mark each excuse-voice
  line. For each one, write the scene (who is whining, what he does with his hands, how trainer Dan reacts) and make the
  start and end frames with Codex. A slapstick payoff on the next line (the slap on "destroy") is welcome where the words
  invite it. The frame approval gate, the applicable per-video clip budget below and the no-belly-framing rule are unchanged. No new voice
  is ever made: the lips follow Dan's recorded impression.
- Reaffirmed on RO-20 (2026-10-11), approving the lip-synced "fat guy who has money" and the non-speaking "brokie": *"If I'm
  imitating some kind of loser to illustrate that with AI, both of those turned out funny and good."* The same day he turned
  down two AI gag OPENERS for that film ("Just use a camera scene for the intro"): the excuse-voice clip is the proven use.
- Method that Dan approved (motion from the frame pair, lip sync on the speaking character only, the checks):
  `longform-edit/reference/ro06/README.md`, round 4. Scripts: `gen_motion.py`, `lipsync.py`, `syncfix.py` beside it.

## Review videos also go in `Videos to Review/`, for VLC (Dan, 2026-10-08)

- **Every video shown to Dan for review that is 45 seconds or longer is also copied to the project folder
  `Videos to Review/`, in addition to the review page.** That means the finished first minute, a finished film, a
  finished short or ad, and any other review clip of 45 s or more (graphics shown in motion included). Shorter clips stay
  on the page only.
- Dan: *"With the review panel, I can only watch it at 2x speed, and I want to watch it at a higher speed in VLC. Also, I
  find that the review panel frequently has issues with the timeline of the video, like going backwards and forwards when
  you click. I want everything in VLC media player that's longer than 45 seconds for this task and going forward."* He
  first said Downloads, then the same day: *"Make a new folder within the AbsByAI project folder called 'Videos to
  Review'. Add the files into that folder. Once the video is finalized, though, delete the files from that folder to
  stop wasting hard drive space. Do that for this and every video going forward."*
- How to apply: copy the full-quality delivered file (not the 540p review copy), named so he can tell which video and
  round it is from the name alone, starting with the task name: `<task name> - <what it is>.mp4`, for example
  `Daily Salad SFL R3 - short 4 - Stop Buying Salad Dressing.mp4`. After a re-render he will review, replace the copy.
  Then open the folder for him (`open "Videos to Review"`) and list the file names in the chat message beside the page
  link. The review page is still built every time.
- **When Dan finalizes a video, delete its copies from `Videos to Review/` in that same session.** They are copies for
  watching; the delivery folder stays the record. Delete only that video's files, never another task's.
- The folder is git-ignored (the repo is public). Claude and Codex both do this, in every video skill.
- **Review pages must survive the editing session and Mac restarts (Dan, 2026-10-08).** Start them with
  `python3 .claude/skills/_shared/review_server.py PORT DIR`. On this Mac the command installs a per-port login service,
  verifies it is running, and returns. Since 2026-10-21 the service starts ON DEMAND: launchd holds the port and starts
  the server when the page is opened (also after a crash or a restart), and the server exits after 24 h with no
  request, so old reviews cost nothing while nobody looks and the link keeps working. Do not use a temporary
  terminal server, `nohup`, or `python3 -m http.server` for a delivered review. `--serve` is for the managed worker/tests.
- Reuse the same port and review folder when repairing an existing link. Never replace another review on that port.
  The service code and web-linked review assets are copied to local Application Support. Published pages therefore
  work even when the editing drive is disconnected. This also avoids macOS background access failures on removable
  drives. Only files linked from the page are cached; raw footage and build intermediates are excluded. Run the same
  command after updating a review page or export to refresh its cache before giving Dan the link. The command checks
  the served page before reporting success. VLC copies are actual files, not shortcuts to the external drive.
- **Enforced by a hook (Dan, 2026-10-16).** On RA-15 round 4 a review page was served with `python3 -m http.server` and Dan could not drag the video
  timeline ("I can't move the slider back and forth on the timeline"). The rule above already forbade it; the project hook
  `scripts/review/hook_no_plain_http_server.py` (PreToolUse, Bash, in `.claude/settings.json`) now blocks any command that starts an
  `http.server`. Serve with `review_server.py PORT DIR`, check `curl -r 0-99` says 206, and seek a video in the browser before sending the link.
- Before sending a page link, load the page and request a byte range of one video (expect 200 and 206), then verify
  browser seeking. When changing server lifecycle code, also terminate its managed worker and prove the same URL
  recovers automatically. Never claim a reboot test unless the Mac was actually restarted.
- After Dan has reviewed and finalized a video, remove only its review copies and stop its now-unused page service
  with `python3 .claude/skills/_shared/review_server.py PORT --remove`. This also removes that page's local cache.
  Retain original delivery files and approvals.
- **Housekeeping (2026-10-21):** `python3 .claude/skills/_shared/renderq/renderq.py prune` switches review services
  that still run all the time (made before 10-21) to start on demand, same link, and stops hand-started servers
  (`--serve`, `http.server`) running over 48 h, printing the command that brings each back. `--dry-run` lists first.
  On 10-21 there were 59 review servers, some 19 days old.
  Time passing or watching a preview alone is not finalization.

## Round 1 always reviews every graphic, stock item and clip; later rounds are lighter (Dan, 2026-10-08)

- **In the first round of every video, content videos included, Dan is shown all the graphics, all the stock and all the
  clips for review.** Dan: *"I want to go back to doing graphics review for content in the first round, like we used to
  do with graphics review in the first round. I want to keep that in the first round, but just make that less extensive
  than the Codex original VSL process for subsequent rounds. Let's always do graphics review for all videos in the first
  round, graphics stock and clips review."*
- How to apply (editor's reading of his words): round 1's review page shows every graphic as a still on its real frame,
  every stock clip or photo, and every other clip (AI, B-roll, app demo) in timeline order, three per row, with the
  "Play it moving, in context" button where a graphic moves. Nothing is locked on the editor's say-so alone before Dan
  has seen it there. That includes full-screen title and section cards.
- **Later rounds show only what changed or is new**, on the same page layout. Do not run the VSL's deeper cadence (still,
  then moving preview, then context, item by item across several rounds) on a content video.
- The numbered "Your decisions" list stays short and holds only real questions. Showing everything is a review, not a
  form: one reply box, and his notes name what to change.
- This replaces the part of the 2026-09-29 approval budget below that let routine graphics, stock and clips be chosen and
  locked without being shown. The AI start and end frame gate, the first minute and the full film are unchanged.
- Context: said the day RO-11's finished film came back with one note, that its seven full-screen section cards looked
  empty and each needed a picture on the right.

## Later-round delivery always includes revisions and review timestamps (Dan, 2026-10-10)

- When most of a video is finished and a later round makes only a few revisions, every delivery message lists each change and the exact timestamps to review in the newly delivered full film. This applies to Claude and Codex, content and ads, and every video editing workflow.
- For each revision, give a short before/after description, its location in the final master, and a practical watch range with a few seconds of surrounding context so Dan can judge the transition. Verify timestamps from the actual delivered timeline, never an earlier round or raw source.
- Link the full film and any already available short repair-context clips. Clearly separate new revisions from unchanged existing flags. State that the other approved scenes were preserved when that is true.
- Do this automatically in the chat, not only inside a report or handoff. Dan should be able to inspect the few changed sections without watching the whole long film again. Required internal full-film QC remains unchanged.

## Sound effects on transitions: judgment, not a blanket ban (Dan, 2026-10-08)

- **A sound effect on a transition is allowed when it works. The ban is on the sounds that failed, not on sound effects.**
  Dan, keeping the sound Zeeshan put on his zoom transitions in Video 5 (Getting Abs At 40 vs 25, round 2) after a
  review asked for it to come off: *"I thought the sound effect to use on transition actually worked, and in fact, this
  is something that I want to try on Claude and Codex edits in the future... Not all sound effects are bad, just the
  ones that we used previously that didn't work. These, I feel like, work, so use a little bit more judgment and
  subtlety with sound effects rather than just saying no sound effects on transitions as a blanket rule."*
- **What the approved one is (measured, 2026-10-08):** a low, soft swoosh about 0.5 s long, centred near 230 Hz with 95%
  of its energy under 800 Hz, sitting about 9 dB under his voice (about -27 dBFS RMS against a voice at -17 to -18),
  and it plays only when the picture itself moves (a zoom between two shots). Reference file, for character and level
  only, never to publish: `Media/sfx/transition-swoosh-reference-zeeshan-video5.wav`.
- **What failed, and still fails:** the old `sfxlib` whoosh and riser (a bright hiss sweep centred near 4,100 Hz, almost
  all of it between 2 and 6 kHz), fired on graphics coming in, 83 times in one ad. That is the "swiping sound" Dan
  rejected on RO-05 on 2026-09-23. Those two functions stay blocked.
- **How to judge one:** it is low and soft, not bright or hissy; it sits well under the voice and never over a word's
  consonants; it goes with a picture move the viewer can see, never with a lower third, a chip or a label appearing;
  it is the same sound every time and there are not many of them. When it calls attention to itself, it is wrong.
- **In a review of an editor's cut:** do not write an item asking for a transition sound to come off because a rule says
  so. Listen for whether it works. If it is harsh, loud, mistimed or on every graphic, write that. If unsure, put it in
  the summary under "For Dan's call" with one timecode, not in the doc.
- **In our own edits (Claude and Codex):** Dan wants to try this. Use a sound of the same character as the reference
  (licensed, or made by us), on picture transitions only, and show it to him in the first-minute review the first time
  a format uses it. Calm formats that set their own rule (the website VSL: no sound effects) keep it.
- A sound on a cut still does not fix a jump cut: a same-size cut needs the framing change or a clip
  (`CUT-CONTINUITY-QC.md`). Dan kept every jump cut item in that same review.

## AI clip faults: judge at playback speed; small faults pass (Dan, 2026-10-08)

- **A small fault that only shows frame by frame does not reject an AI clip.** On the RO-11 opener, two takes were rejected
  by the editor because the fork read as a spoon in the man's mouth for about 10 frames, its head came off the handle for
  about 6 frames, and the food reshaped at the cut. Dan, after watching both in VLC: *"I think the clip was actually
  acceptable. Those small faults that you notice, I don't think they would be noticed by humans... I think normally clips
  like that would be okay."*
- **A slight speed-up is an allowed way to cover such a fault:** *"For future clips, if we did want to use the whole thing,
  I think small faults like that could be covered by slightly accelerating the clip."* Holding or slowing a clip to fill a
  slot is still forbidden.
- How to apply: still read every AI shot frame by frame to find candidates, then decide by watching it at normal speed. A
  fault well under half a second that a viewer does not catch at speed goes in the report as a note. It is not a reason
  to buy another take or to stop for approval. Faults a viewer does see at speed, or that grow over a second or more
  (breath smoke, a fogging mirror, melting hands: Dan, 2026-09-14), still reject the clip.
- Choosing the best-flowing part of a take over the whole take is a normal editing call (Dan picked the clean 2.7 s tail
  on RO-11 because "it flows better").

## No fat pinching or belly close-ups, above all in the first 30 seconds (Dan, 2026-10-04)

- **Never build a shot around belly fat: no hands pinching or grabbing it, no push-in or crop that centres on it, no
  framing whose subject is the belly.** This binds AI clips, stock clips, photos and graphics, in ads and in organic
  videos (organic videos get promoted in engagement campaigns, so they face the same ad review).
- **It matters most in the first 30 seconds**, which is what gets reviewed and what plays as the ad.
- Dan, rejecting the RO-11 opener (a heavy shirtless man on a scale grabbing his belly): *"I'm concerned this will be
  disapproved for negative events and imagery, and we won't be able to advertise this in engagement campaigns because of
  the fat pinch... Focusing in on the belly fat like this with pinching or emphasis tends to get that disapproval."*
- What to show instead: the situation, not the body part. His replacement was an overweight man at a table with a tiny
  plate of bland chicken and broccoli, looking like he eats very little and still is not losing weight. A heavier person
  shown whole, clothed, doing something (eating, cooking, walking, stepping on a scale) is fine.
- How to apply: when writing an AI frame prompt or picking stock, say "do not show his stomach, no hands touching his
  body" and frame from the chest up or with the table hiding the midsection. The reviewer checks every clip and photo in
  the first 30 seconds for it.

## Squares and verticals: fill the frame, no boxes without a reason (Dan, 2026-10-02)

- **A clip or photo in a square or vertical fills the frame. Put it in a box (a card on the field) only when there is a
  real reason.** Dan, on the Ad 6 look page, about a centred man shown in a card in the square: *"I'd like to see that
  full screen in the square. I don't feel like there's any reason to crop that into the box. Let's make that a rule for
  squaring verticals going forward: we should avoid cropping things into boxes unless there's a reason to do that."*
- Reasons that count: filling the frame would cut something that matters (a face, a second person, the action, the flag
  in a wide photo), it is a phone screen, or a required label truly has no clear spot. Write the reason beside each boxed
  item on the review page. "The label was easier to place" is not a reason: try a smaller chip or a corner first.
- This extends the 2026-10-01 rule below (a horizontal clip in a vertical) to squares and to photos.

## Superseded mix (2026-10-13, section at the top of this file); who and how still hold: five choices, made by Codex inside the Claude setup task (Dan, 2026-10-02)

Dan, finalizing RO-16: *"the standardized way is we do the upload and setup with Claude. Claude calls Codex within the
command-line interface and uses my subscription to make the images. We don't use external models like Gemini to make any
images. We make five variations: one from the pool shoot, one from the studio shoot, three AI-generated images of Codex's
choice, unless I request something different."*

- **The five:** (1) one real pool-shoot photo, (2) one real studio-shoot photo, (3 to 5) three AI-generated images, each a
  unique design of Codex's choice that sells the video's topic. Five different images and designs; same copy unless Dan asks
  for copy alternatives.
- **Who and how:** the Claude upload and setup task (`/video-setup`, `/ad-setup`) makes them itself with
  `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No separate Codex task or handoff. **GPT-6.1 Sol
  at high effort is the default for every thumbnail and cover task** unless Dan names another model.
- **No outside image models** (Gemini, Nano Banana, Seedream, FLUX). [IMAGE-GENERATION.md](IMAGE-GENERATION.md) still binds:
  a real photo of Dan is never redrawn (Codex makes the background, his real cutout and the type are layered in code).
- Show the five on one review sheet and **stop for Dan's pick** before any upload or scheduling.
- This replaces the 2026-09-30 mix below (pool, two studio on Jelly Beans backgrounds, screenshot, designer choice). The rest
  of that section (consistent copy, separate Instagram and YouTube layouts for Shorts, locked covers stay locked) still holds.

## Superseded mix, kept for its other rules: five cover and thumbnail choices per video (Dan, 2026-09-30)

Every cover-image or thumbnail review, including its handoff, must request and deliver
five visual options for each video:

1. One pool-shoot photo.
2. Two different real studio photos, each composited into a bold, topic-specific
   photographic environment in the Jelly Beans cover family: crisp white cutout
   outline, large subject-related props, heavy type and one accent color.
3. One authentic screenshot from that video's approved finished master, enhanced
   for clarity as useful while preserving Dan's identity, physique and exercise.
4. One additional option chosen by the designer, using the image and design that
   best sells that video's topic.

Use a different image or design for each choice. Keep the copy consistent across
choices unless Dan requests copy alternatives. For Shorts, each choice includes
separate Instagram and YouTube layouts; they count as one visual option, not two.
Show the finished options and stop for Dan's picks. Export his selections, and
upload or schedule only within the separate authorized setup task. Preserve locked
covers and already approved selections. This replaces the old two-cover rule and
any older five-thumbnail mix with two pool photos. In future handoffs, link this
rule and spell out all five slots. Reference:
`Short-form video content/covers/review/jelly-bean-refresh/B3-jelly-beans-beat-soda-tight.png`.

## No AbsByAI.com mark at the end of a video (Dan, 2026-10-01)

- Do not put an "AbsByAI.com" mark graphic on screen at the end of a video, and do not ask an editor to add one. Dan:
  *"I want to stop putting AbsByAI.com at the end of each video like that."* Older scripts that cue
  "[AbsByAI.com mark on screen]" are overridden. The spoken call to action and description links are unchanged.

## New shorts batches: Soft Blue Light + HyperFrames; first vertical and square get a full pre-approval round (Dan, 2026-10-01)

- **SL-05 (Stop Deadlifting) was the last batch of shorts in the J2 / olive graphic set.** Dan, reviewing it: *"this is the
  last round of shorts I want to see with this graphic set going forward for new batches. I want to see everything made
  with the soft blue light and hyperframes graphics."* A batch already in revisions finishes in its current set.
- **Every new batch of shorts** (cut from a long-form, or dedicated) uses Soft Blue Light graphics built from the
  HyperFrames templates (`_shared/hyperframes/`, `GRAPHICS-STANDARDS.md`): title treatment, key-point bars, lower thirds,
  labels, cards.
- **The first time this is done in vertical, and the first time in square, Dan gets a thorough approval round with every
  asset reviewed before anything is built:** *"show me a thorough round of approval with all the assets pre-reviewed
  before you make it, and then we'll go ahead and make it."* That means each graphic as a still on its real frame, the
  title treatment, the key-point bar over an editor's burned pill, card layouts and caption placement, per
  [PRE-RENDER-APPROVAL.md](PRE-RENDER-APPROVAL.md). Later batches reuse what he approved.
- This supersedes "extracting shorts from an approved long-form keeps that film's approved graphics" for the shorts'
  OWN graphics (title band, bars, chips). An editor's graphics burned into the picture are still handled, not restyled.

## Verticals: the camera lands on Dan, then holds (the standard centering, Dan, 2026-10-03)

**Locked by Dan, 2026-10-05:** The right-hand `after.mp4` in the Codex before/after review is the approved framing reference for all future 9:16 videos. Use this land-then-hold method through shared `cut/landing.py`. Exact clip hash, measurements and Dan's approval are recorded in `Docs/VERTICAL_CENTERING_CODEX_20261003.json`. This locks the framing method; approved exports stay untouched.

- **In every vertical the crop that follows Dan lands centred on him after each cut, then stays still until he has moved
  3.3 % of the crop's width off centre, and only then follows.** Dan, choosing the calmer of two RO-10 first minutes:
  *"I like the calmest one, the two-thirds calmer. That looks the best to me... Let's make this our standard way of
  centering for verticals going forward. I feel like this is better than what we were doing."*
- It replaces the track that chased every small movement (his 2026-10-01 note: "excessive and distracting"). Never go
  back to a crop that does not move at all: he left the frame.
- Claude and Codex both build verticals this way. Method, numbers and code: `_shared/framing-motion.md`, "Vertical
  talking head: land on him, then hold". Use shared `cut/landing.py` via its scaled vertical preset; `kit_track.py` defaults to 20 px for a 608 px crop. Report travel, p90 pan speed, time moving and median/maximum head offset. Approved exports stay untouched.

## Verticals and squares: fill as much of the screen as the clip allows (Dan, 2026-10-02)

- **In a vertical or a square, every clip, photo and phone demo fills as much of the screen as its content allows. Crop
  the unneeded space off the sides as far as it goes, and avoid blank space.** Dan, on the RO-10 vertical: *"Usually,
  unless there's a strong reason not to, unless we have to preserve the content on the left and right sides and we can't
  crop, we want to fill as much of the screen area as possible and avoid having a lot of blank space. Let's lock that in
  as a standing rule for verticals and squares going forward."* And: *"be a little bit more aggressive... look a little
  bit more aggressively for opportunities to crop these clips."*
- **The crop is not three fixed shapes.** Full screen, square and whole clip (the rule below) are points on a line: pick
  the NARROWEST window that keeps what the clip is about, at any shape between the whole clip and full screen, placed
  on the subject and not on the middle of the frame. His notes: "crop out some of the unnecessary space on the left and
  make it more square, or as vertical as possible"; "crop out the space on the left and a little bit on the right";
  "nearly vertical".
- **Blank space is the exception and needs a reason:** the sides hold something the clip needs (his example: the overhead
  salad table, "we need the stuff on the sides there"). Say the reason in the build report.
- A card that is not full screen is as large as the frame allows and sits high enough to clear the captions; a phone
  demo is as large as fits. Height is still never cropped (rule further below).
- Applies to `/shortad-from-longform` (9:16 and 1:1), `/shorts`, `/ad-edit` verticals and every other vertical or square.

## A horizontal clip in a vertical: fill the frame, else centre square, else the whole clip (Dan, 2026-10-01)

- **Default: the clip fills the phone frame** (a vertical crop of it). Dan, on the RO-10 vertical page: *"Use B unless
  there's a strong reason not to... unless there's something critical in the sides where the clip wouldn't make sense,
  where there are body parts cut off."*
- **If filling the frame cuts off too much, show the centre square. If the square still cuts off too much, show the
  whole clip in a card.** *"I want it to depend on whether there's something in the sides that's critical."* His two
  worked examples: the AI man on the scale (one centred person, nothing at the sides) fills the frame; the overhead
  salad table (the subject spreads across the frame) is a centre square.
- Applies to our own AI clips and to stock, in every vertical (`/shortad-from-longform` sheet builds, `/shorts`,
  `/ad-edit` verticals). The whole-clip card still never crops height (rule below). Returns from a card are hard cuts.
- Going forward, AI clips made for a film that will get a vertical are framed with the subject in the centre third.

## A horizontal clip inside a vertical or square frame is never cropped shorter (Dan, 2026-10-01)

- **When a 16:9 clip sits as a card inside a 9:16 or 1:1 frame, show its full height. Never crop rows off the top or
  bottom, which only makes the card shorter and adds black space.** Dan, finalizing SL-05: *"There's not ever any reason for you to crop horizontal videos within a vertical frame and make them shorter than they already are. There's already too much black space, so avoid crops like you did on that first draft of the power lifter clip that unnecessarily make the video shorter when we have a horizontal within a vertical frame."*
- What it cost: SL-05 short 3's first build cropped Zeeshan's AI powerlifter clip to its top 69% (a 1080x419 strip) to
  remove his burned key-point pill. That cut the barbell out of a deadlift clip. Dan: *"it's a little bit cut off and
  unnecessarily cropped on the bottom... It looks like it's cropped shorter than it needs to be."* The approved fix was
  the whole frame, 1080x608.
- How to apply: a card's crop may only keep the full source height. Cropping the SIDES so the card gets taller (a
  1170 px wide window of a 1920 px frame, for example) is fine when nothing essential is lost, because it reduces black
  space. An editor's burned graphic inside the clip stays whole inside the card, and our own bar or chip that would
  duplicate it comes off for that shot. If the editor's graphic is unacceptable, pick a different part of the clip or a
  different clip; do not crop the height. This replaces the older "replace an editor's pill by cropping" recipe.
- Applies to `/shorts`, `/shortad-from-longform` (vertical and square), `/ad-edit` verticals and any other skill that
  places horizontal footage in a taller frame. Reviewers check it on the delivered file: any card shorter than its
  source's full height at that width is a defect.

## Shorts stand alone: show the whole exercise, not a detail of it (Dan, 2026-09-30)

- **A short must make complete sense to a viewer who never saw the long-form.** Leave out details that only work
  with the full video's context: a set-up step, a position check, a reference back to something said earlier.
- **When a short tells the viewer to do an exercise, show the whole exercise briefly:** a few complete reps (a demo or
  live-round clip from the same source), not an isolated detail of it. A detail cue (grip, thumbs, arm angle, elbow
  height) stays only when the complete movement is also on screen in the same short.
- Dan, approving SL-04 short 1 round 3: *"we want to avoid including details in it that won't be understood if the
  viewer didn't watch a full long form... if we say to do a certain exercise, rather than just showing individual
  details that don't make sense without full context, show the full exercise briefly."* Why: round 2 ended on the
  side-lateral arm-angle set-up with no exercise shown (*"It's not clear why I'm showing them the arm angle when I
  don't show the complete exercise"*); round 3 replaced it with his thumbs cue plus live-round reps and was approved.
- How to apply: at segment selection, for every exercise a candidate names, write down where its complete movement is
  (inside the segment, or another range of the same source to append, e.g. the live round). A candidate whose exercise
  never appears whole is either paired with a range that shows it or dropped. The reviewer checks it on the delivered file.

## Review page standard + "What I decided" (Dan, 2026-09-30)

- Every approval packet opens with the first minute, then the AI frames, then a **"What I decided (overrule anything)"** list,
  then every graphic and clip in order, three per row. Dan: *"I like this 'What I Decided' section. Let's make this the standard
  way to do things going forward."* Layout and details: [PRE-RENDER-APPROVAL.md](PRE-RENDER-APPROVAL.md#the-review-page-one-layout-and-a-what-i-decided-list-on-every-packet-dan-2026-09-30).

## Organic videos may name the drug (Dan, 2026-09-30)

- **Organic content videos may say and subtitle Zepbound, tirzepatide, GLP-1 and any other drug name.** Dan: *"I plan to make a lot of organic videos where the entire topic of the video is Zepbound. Organic videos can say Zepbound, Tirzepatide, GLP-1, or any of those."* The never-a-brand-name rule is an AD rule (ad-edit Step 9.3) and stays for ads only.
- The delivery gate still carries the ad rule on organic formats (`compliance:drug_names` and the `srt:shape` banned spelling "Zepbound"/"Ozempic" on `longform`); until that is changed with the regression corpus and a `GATE_VERSION` bump, those two rows failing on an organic video are the known mismatch, not a defect. Spoken and subtitled drug names are correct. **Drug names in on-screen graphics (Dan, 2026-10-28, RO-24 R4):** allowed in organic videos that are entirely about weight-loss drugs (graph labels, titles, cards: "Zepbound", "Ozempic", "Mounjaro"); in organic videos that are not entirely about them, keep drug names out of graphics. Dan: *"I want to eliminate the rule that we have to not mention weight loss drug names in graphics, because the whole video like this is about weight loss drugs. Let's just make that rule apply to videos that aren't entirely about weight loss drugs."* Ads keep their own rule.
- Related, same day: do not tell viewers to "empty the entire vial" (Dan cut that ad-lib from RO-12: people on non-standard doses do not).

## Organic content approval budget (Dan, 2026-09-29)

**Round 1 now always shows Dan every graphic, stock item and clip (Dan, 2026-10-08; section near the top of this file).** For organic content videos, the newer approval budget below replaces older requirements for Dan to approve every graphic and clip separately and the shared 10 to 15 decisions per video guidance. Keep the stepwise internal checks and the real approval gates. **Dan, 2026-10-20, settling the 20-versus-15 question: keep the current page as it is.** The major decisions go up top (first-minute draft, colour correction, audio, and the chroma key when it is a green-screen video); below them every graphic and every small thing, even fifty of them, laid out so he can scan through quickly. There is no cap on the scanned list; the numbers below were ceilings on QUESTIONS, not on what is shown. The **first approval round has at most 20 decisions**. In later rounds, **aim for 10 or fewer decisions per round**. These are ceilings, not targets. Ask Dan only about materially uncertain choices that require his judgment. Choose and check routine assets yourself, summarize what you chose, and let him overrule while reviewing the first minute and the finished film. Never reopen unchanged approved items or infer approval from silence. New AI motion still needs approved start/end frames first; show materially uncertain finished motion in context before locking it. The website VSL approval cadence remains separate and more detailed.

## Categorize every video before editing it: content gets Shorts, ads get formats (Dan, 2026-10-04)

Dan, 2026-10-04: *"From now on, we have to have everything categorized before we edit it. If it's a content video, if
it's long-form content, then we want to cut it into shorts. If it's an ad, that's when we need the vertical and square
version and the 1-minute version."* He asked for the rule in both directions: no ad-style edits of content videos, and
no content-style edits of ads ("such as making 5 shorts out of an ad").

| category | sidebar type | what is derived from the finished 16:9 | skill | never |
|---|---|---|---|---|
| long-form content | `LFC` | Shorts cut out of it, each standing alone | `/shorts` | a full-length vertical, a square, a 1-minute version of the whole video |
| ad | `AD` | the vertical (`V`), the square (`S`) and the 1-minute cut (`Sh`) of the ad | `/shortad-from-longform` | a batch of organic Shorts mined from the ad |
| dedicated Short | `SFC` | nothing: it is already the short | | any re-format |
| Shorts extracted from long-form content | `SFL` | already the derived Shorts | `/shorts` | ad-format adaptations of the source film |

- **Decide the category before any edit work**, the same way the upload rule below decides it (the video's own ending:
  a tap-the-button call to action is an ad; anything softer is content), and write it on the first line of the task
  and of every handoff. A handoff with no category is not ready to fire.
- **A request for the wrong kind stops before spending anything.** That covers a task prompt, a handoff, a queue job
  and a proof or test run of a pipeline. Tell Dan in one line what was asked and what the category allows. Do the
  read-only prep meanwhile.
- **Only Dan's own words naming that video and that format override this**, recorded with the build (`kit_run.py
  --dan-asked "<his words>"`). "Continue the edit" is not such words.
- **A pipeline proof uses a video of the right category.** The sheet path for verticals is proven on an ad, never on
  a long-form because it happened to be ready first.
- **Enforced:** `kit_run.py` refuses an edit sheet whose `type` is `LFC` or `SFC` without `--dan-asked`. The `/shorts`
  and `/shortad-from-longform` skills open with this rule.
- **Why:** on 2026-10-03 the vertical kit's proof run was pointed at RO-10 (the Calories long-form) because it was the
  first of our own edits with an edit sheet. It cost about seven hours of machine time and 1.6 million judge tokens for
  a full 9:16 and a 52 second cut that nobody needed: the long-form publishes as its 16:9 and its Shorts are their
  own job (SL-08). Queue jobs AV-13 and AS-12 (a vertical and a square of the organic Arms & Shoulders workout) are
  retired by this rule.

## Ad or organic? Classify every video from its own ending before any upload (Dan, 2026-09-28)

- **Before any upload or setup, decide from the finished video itself whether it is an AD or ORGANIC.** Read the
  last 15 seconds of the finished file's transcript (the `finished-asr*.json` beside the build, or transcribe the
  ending with `.claude/skills/ad-setup/transcribe.js`). Record the verdict and the exact closing words in the setup notes.
  - **AD:** a definite direct-response call to action telling the viewer to act on the ad itself, e.g. *"tap the
    button below"*, *"click the button below"*. Ads go through `/ad-setup` only: Unlisted YouTube + Google Ads.
  - **ORGANIC:** a softer end call to action (*"go to AbsByAI.com"*, *"leave me a comment"*, *"follow for more"*)
    with no "tap/click the button below". Organic goes through `/video-setup` only: Blotato releases it on every platform, YouTube included
    (no YouTube holding upload since 2026-10-01; see "YouTube visibility" below).
- **If the request, handoff or queue label disagrees with the video, STOP before uploading anything and ask Dan**,
  quoting the closing line: *"This handoff sets it up as an ad, but the video ends with 'leave me a comment' and has no
  tap-the-button CTA, so it reads as organic. Set it up as organic instead?"* The same applies in reverse. Do the
  read-only prep meanwhile; no YouTube, Google Ads or Blotato write until he answers.
- **Why:** on 2026-09-27 a handoff sent DS-18 "How To Kettlebell Deadlift" (a dedicated organic Short ending *"Leave
  me a comment"*) through the ad path: Unlisted upload plus two Google Ads groups that spent $0.62 before Dan caught
  it. Job prefixes are a hint, not proof: `DS-`/`RO-`/`SL-` are normally organic and `RA-`/`AV-`/`AS-`/Ad N normally
  ads, but the CTA in the video decides.

## Approved workout-app format, M100 excerpt and future clip placeholders (Dan, 2026-09-28)

- **Workout-functionality demonstrations:** WV-01 round8's upright phone, exercise list, visible tap, then natural-speed landscape exercise video above its description is the approved impressive presentation format. Reference: `/Volumes/Extreme/_edit_work/wv01-edit/round8/graphics/early-app-flow.mp4`, reviewed at about0:30. Preserve phone shell, side presenter, readable UI and intact exercise action. Its documented review composition is not a live interaction recording. For WV-01, replace leg press with an at-home, minimal-equipment exercise, preferably toe touches or another ab exercise; bodyweight squat is the fallback.
- **Old-channel exercise proof:** Dan approved the exact M100 original4:48-4:55 excerpt in WV-01 round8 for future exercise / Six Pack Shortcuts references outside diet context. Reuse `/Volumes/Extreme/_edit_work/wv01-edit/round8/graphics/m100-288-295.mp4`; full source `/Volumes/Extreme/_edit_work/wv01-edit/round7/assets/m100-complete.mp4`, original source288-295seconds, full YouTube-page treatment. This specific selection supersedes the older solo-Dan-only selection rule for this excerpt. Keep diet footage for diet references.
- **Future contextual previews:** When planned AI motion is not ready, show labelled START/END-frame placeholders at its intended location within the opening/context review so Dan can judge the scene with surrounding speech. This is a preview convention, not a finished clip or authorization for a complete placeholder film. Dan explicitly exempts WV-01 and its next round: do not retrofit placeholders into this video. Approved actual motion can still be inserted normally.

## Lock the graphic style before editing; AI clip frames first; AI openers (Dan, 2026-09-27)

- **Lock the graphic style before any full video is edited.** Dan: *"They render the whole video, then we change the graphic, then we render it again. I want to lock graphic styles before the videos go forward."* This binds human editors, Codex and Claude. If the format has a locked style (`GRAPHICS-STANDARDS.md`), every brief and revision doc links its moving references and the editor builds in it. If not, the first deliverable is graphic variations on one video's frames (the editor's own style, one imitating our locked style, two significantly different ones: masculine, bold, modern, trustworthy); Dan picks; only then are full videos cut or revised.
- **Every new AI clip is approved as start and end frames before the motion is generated, for human editors as well as our pipeline**, in the video's orientation (9:16 for shorts). This extends the frame-approval rule below to every editor.
- **Frequently, not always, a video opens on an AI-generated clip.** Look for the opportunity on every video; offer two or three opener concepts for frame approval. A strong on-camera cold open can stay.

## Speedo photos: always crop at the shorts line (Dan, 2026-09-27)

- **Any standing photo of Dan in the Speedo/briefs is cropped so it reads as regular shorts, never a Speedo.** Show as much of the waistband as possible: put the bottom edge at the waistband's lower seam, stopping just before the leg openings (where the brief shape starts) appear at either hip. Keep posting these photos; only the crop changes.
- **Leave seated and lying photos uncropped** (Dan: "It's not really possible to crop those"). The lying med-ball photo also stays as shot.
- Trim unnecessary space above his head, keeping a little headroom and never cutting hair. On the extended-arm (pointing) pose, cropping the outstretched arm past the elbow is fine.
- Applies to every surface: Instagram, Facebook, TikTok photo posts, covers, thumbnails, site images and in-video real-photo displays. Real shorts are untouched. Instagram needs aspect 0.8 to 1.91.
- Before queuing any photo post, check it for the Speedo. Crops, boxes and swap maps from 2026-09-27: `photos/finalized social media photos/_speedo-crops-20260927/`. Swap mechanics: `scripts/blotato/swap_media.py` (its "new schedule not found" line is read lag; re-fetch and MD5-check).

## AI label on uploads: only for real AI footage (Dan, 2026-09-27)

- YouTube's altered/synthetic flag (`--synthetic`, Blotato `containsSyntheticMedia`) and TikTok's `isAiGenerated` (Blotato config `ai_generated`) are set to **true ONLY when the video contains realistic AI-generated footage**: AI video clips or scenes, AI-Dan exercise demos, AI B-roll of people or places, AI-generated music, or an AI voice of someone other than Dan.
- **A still AI goal image that carries the on-screen AI-GENERATED label does NOT trigger the flag**, and neither does the absbyai.com CTA showing one. YouTube exempts AI-written scripts, titles, thumbnails, captions, infographics, color or upscaling, and cloning Dan's own voice. Keep the one-line AI-image sentence in the description.
- Before 2026-09-27 every video with an AI goal picture was flagged, so plain workout videos showed YouTube's "AI" badge. Decide per video from the actual edit; when unsure, check the edit recipe or contact sheet for AI clips.

## Never show stick-figure exercise demos (Dan, 2026-09-25)

- Never show the app's stick-figure exercise animations in any video. Use suitable, polished AI-generated exercise demonstration clips instead, matched to the displayed workout. Dan rejected the WV-01 workout preview and said: "Never ever show these stick figures in any video."

## Standing authorization for thumbnail replacement (Dan, 2026-09-16)

- When Dan requests a thumbnail replacement, install the approved new thumbnail without asking again about removing the old thumbnail or its completed A/B test. Preserve available test results in the installation notes first. This does not authorize deleting the video or post itself.

## Clip library first: reuse before you generate, register what you make (Dan, 2026-09-29)

- **Order of preference (Dan, 2026-10-01): our real B-roll, then an existing AI clip of ours, then stock, and a new AI
  clip last.** *"Always look for ways to use B-roll in our videos. Generally, it's better to use B-roll than stock or AI
  clips when we have the B-roll. I also want you to look through our existing AI clips library and look for
  opportunities to use those clips before requesting a new one."* This binds our own edits and every revision doc and
  brief written for an editor: scan the library against each line of the video, link the clip, and only then direct
  anything new.

- **Before generating any AI clip, searching stock, or hunting raw rolls for B-roll, search the clip library:**
  `python3 .claude/skills/_shared/cliplib/clip_library.py find "<what the beat needs>" [--aspect 9x16] [--rolls]`,
  then look at the top hits' `Media/clip-library/contact/<ID>.jpg` previews. If an existing clip fits, use it and cite
  its ID (A#### AI, B#### B-roll). Generate only when nothing fits, and say so in the job notes.
- **When a job finishes, register every new AI clip, stock clip or cut B-roll insert that made it into the approved
  video** (and any clean unused keeper) with `clip_library.py add ... --status used-final --used-in "<job>"`, then
  `clip_library.py sheet`. Rejected or defective takes never go in.
- Human editors browse the same catalog as a Google Sheet in the Drive library folder. Full rules: `_shared/cliplib/README.md`.

## Video clip generation budget and frame approval (Dan, 2026-09-15)

*Since 2026-10-17 every Veo clip is generated on the Google Flow subscription first (section near the top of this file). **Dan, 2026-10-20: every AI clip is generated on the subscription by default, and any generation outside the subscription is asked for first, every time**, with the clip count and the dollar estimate; when he says rush, that is his authorization to pay for that video. The dollar caps below bound a paid run he has authorized; they never pre-authorize one. Frame approval before motion is unchanged.*

- **Updated by Dan, 2026-10-09:** Replicate image and motion generation is standing-authorized up to **$50 total per website video**, **$15 total per long-form content video (Dan, 2026-10-13, raised from $5; he said "$15 per clip", recorded as per video until he confirms) and $5 total per other content video posted on YouTube or Instagram**, and **$10 total per ad uploaded unlisted and advertised**. Dan: "You're always authorized to generate whatever you need with Replicate" within those limits. Use existing project Replicate keys and send the necessary project image inputs to Replicate for that generation without asking again. This replaces the earlier $5 Replicate limit. The existing Gemini authorization is unchanged.
- Count supporting start/end-frame generation and paid retries in the video's total across all revisions; a new task or revision does not reset it. Preserve unknown charges honestly and track provider receipts. Ask for spend authorization only before exceeding the applicable cap, stating the specific clips and estimated new total.
- Show Dan the **start and end frames plus the intended action** for approval before generating motion. Budget authorization does not replace frame approval. Materially different replacement frames require approval again.
- Current stock choice (Dan, 2026-09-15): **Pexels and existing assets with known usage rights only; no paid stock service or subscription.** Use AI where the intended scene needs it. Keep a per-video generation total, including paid unsuccessful attempts. Gemini quality-review spend remains governed by its separate standing authorization.

## The round method: small approval rounds, full render last (Dan, 2026-09-28)

- *"The reason why Codex is making way better videos than you is that it's taking a way more stepwise approach. Rather than trying
  to one-shot it and edit the video all in one, there are many small rounds of approval. I want you to copy this approach going
  forward."* Every video skill follows [PRE-RENDER-APPROVAL.md](PRE-RENDER-APPROVAL.md): look options, then EVERY graphic as a still
  screenshot on its real frame (Dan edits the text and approves each), then moving previews, every clip (AI: concept, frames,
  motion), then the finished FIRST MINUTE, and only when nothing is pending the full video. One round per session, decisions
  recorded with hashes and Dan's words, a handoff at the end of each round. This supersedes the 30-second and 60-90 s sample rules below.

## Approve the opening, all graphics and clips before a full render (Dan, 2026-09-26)

*Read with the newer rules: the round order and the first-minute draft are set by [PRE-RENDER-APPROVAL.md](PRE-RENDER-APPROVAL.md) (long-form round 1 carries the first-minute draft, 2026-10-16; a nearly approved Short or ad shows the whole video, 2026-10-14); "first 30 seconds" below is the 2026-09-26 wording. Lower thirds use title capitalization (2026-10-09, 2026-10-16), so the `KEY POINT:` prefix is not a default any more, and every new graphic moves in HyperFrames (2026-10-17).*

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

- **Never that swiping sound effect.** *"I really hate that swiping sound effect. We need to remember this going forward: never, ever use
  that swiping sound effect for anything."* `sfxlib.whoosh()` and `sfxlib.riser()` raise an error; do not re-create them by hand.
  Muhammad's own flash transitions are silent. **Narrowed by Dan on 2026-10-08:** this bans that bright, hissy sound and
  sounds on graphics, not every transition sound. A low, soft swoosh on a picture transition can work. Read "Sound
  effects on transitions" near the top of this file before adding or rejecting one.
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
  transitions) is proven in small rounds (look options, each graphic as a screenshot, the finished first minute) BEFORE the full
  video is built (the round method above). Ten rounds of reactive defect-fixing on a cut whose style was never right is the waste he means.

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

## Real-photo labels include touched-up photographs (Dan, 2026-10-17)

- Label a real photograph as real, not AI-generated, even when it has been retouched or touched up. Use **“Real photo of me, not AI-generated”** for one photo and **“Real photos of me, not AI-generated”** for a group (title capitalization in the graphic). Do not substitute “Retouched photo(s) of me.” The distinction is a real photographic source versus a fundamentally AI-generated image; ordinary touch-ups do not change that classification.
- Dan's exact RO-26 revision: replace “Retouched Photos Of Me” on the opening trio at about 0:01 with **“Real Photos Of Me, Not AI-Generated.”** Preserve the photographs, composition and timing.
- Keep source provenance internally. A fundamentally AI-generated image remains AI-generated; this does not reclassify RO-26's rejected pool image. Keep the existing label-clearance rules and the thumbnail/real-moving-footage exceptions below.

## Label Dan's real pictures (Dan, 2026-09-11)

- **Thumbnail exception (Dan, 2026-09-16):** Do not put “Real picture of me — not AI-generated” on thumbnail or cover images; it is too small to read on a phone. Keep that label on real physique photographs when they appear inside videos. Thumbnail/cover designs also omit `AbsByAI.com` unless Dan explicitly requests it. This overrides the broader real-photo label rule below for thumbnails and covers; it does not remove AI-image disclosures inside videos.
- **Dan's REAL after pictures carry a burned label** (wording since 2026-10-17: "Real Photo Of Me, Not AI-Generated", plural "Real Photos Of Me, Not AI-Generated", no em dash; the section above). Original note, 2026-09-11, with the old wording "Real picture of me — not AI-generated": viewers were taking his real photos for AI). Every real photo-shoot or studio picture of Dan shown as a result gets it for its full duration, in the same chip style as the AI label. AI images of Dan keep "AI-GENERATED". The two labels are mutually exclusive: every picture of Dan's physique carries exactly one of them.
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

## Long-form release cadence (Dan, 2026-10-17; replaces the 2026-10-07 Sunday-only rule)

- Two long-forms a week: Sunday and Wednesday at 9 AM America/Chicago through Blotato, one per day, never another weekday. YouTube first; Facebook, Instagram and TikTok the next day at noon once YouTube reads public. Dated calendar: `Docs/LONGFORM_RELEASE_CALENDAR.md`; Shorts: `Docs/SHORTS_RELEASE_CALENDAR.md`. The full rule lives in `AGENTS.md`, "Long-form YouTube release cadence"; `scripts/blotato/longform_queue.py` and `video_topup.py` enforce it. The 2026-10-07 "one per week, Sundays only, socials Monday 9 AM" text that stood here is superseded.

## YouTube visibility — never upload Public (Dan, 2026-09-16)

- **Never upload any video to YouTube as Public, and never use YouTube's native scheduling/publish-at path.** This applies to API uploads, Studio uploads, scripts and manual work. The upload-time visibility must always be non-public.
- **Ad videos are always uploaded Unlisted.** No ad gets a separate Public YouTube copy, even if it will also be used on other platforms.
- **Organic videos: Blotato only (Dan, 2026-10-01).** No Private holding upload. Blotato creates and releases the public YouTube video at the scheduled time; we never upload organic content to YouTube ourselves and never use YouTube native scheduling or publishAt. Ads stay Unlisted via `/ad-setup`.
- Before reporting an upload complete, read back the saved visibility. It must be `unlisted` for an ad. Organic content is never uploaded by us (Blotato creates the public video at release), so an organic file sitting on YouTube as our own upload is itself the mistake: make it Private and report it. If the video type is unclear, nothing is uploaded until it is resolved; never Public.

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

## Active edit cap: at most 5 edits doing production at once (Dan, 2026-10-21)

- **At most 5 video edits do production work at once, Claude and Codex together.** Production = render-queue jobs,
  AI generation, builds. On 2026-10-21 about 12 edits ran at once, the render queue was overbooked (16-18 cores of work
  on 8, ~7.8 GB swap), heavy steps waited 3-5 hours and no video finished all day. The render queue caps steps; this
  caps edits. Tool and details: `.claude/skills/_shared/editcap/README.md`.
- **Every edit acquires a slot before its first production step and on every resume:**
  `python3 .claude/skills/_shared/editcap/editcap.py acquire <JOB> --title "<title>" --type <LFC|SFC|SFL|AD>`.
  Exit 0: go. Exit 3: waiting. Do no rendering, generation, building or spending; read-only prep is fine. Arm the
  auto-start (Claude: `editcap.py wait <JOB>` with `run_in_background`; Codex: a 10-minute heartbeat automation on
  the thread that runs `acquire` and continues on exit 0), tell Dan the place in line in one line, end the turn.
- **Waiting on Dan holds no slot.** Review page up, awaiting picks, NEEDS-DAN: `editcap.py release <JOB> --review`.
  When his notes arrive, `acquire` again. Finished: `editcap.py release <JOB>`. The next waiting edit starts by itself.
  If `release` prints `WAKE claude ...`, send that session the message.
- **Waiters start in release-date order, not firing order** (both release calendars; a Shorts batch takes the day after
  its long-form; ads rank with the nearest release; 2027 and undated work last). A returning edit goes to the front
  only if its release is soonest. Dan can reorder with `--release YYYY-MM-DD`.
- **Exempt:** setup/upload tasks, thumbnail and cover picks, scripts and docs. They never call it.
- Anything already running in the render queue counts toward the 5 even if it never registered, and is never
  stopped. An edit silent for 3 hours loses its slot. The tool fails open: if it breaks, it warns and allows.
- **See it:** `python3 .claude/skills/_shared/editcap/editcap.py status` (read-only, covered by the standing
  render-queue authorization in AGENTS.md).

## Video builds: the render queue (formerly "never run more than two at once")

- **Since 2026-10-20 the cap is enforced in code by the render queue, `.claude/skills/_shared/renderq/`.** Dan can start
  10, 20 or 30 editing jobs at once; every heavy step waits its turn in a real first-come line and starts when a slot
  frees. Do not count builds with `ps`, do not write a wait loop, do not hold a job back "because two are running":
  **just start it.** Claude and Codex alike. README: `.claude/skills/_shared/renderq/README.md`.
- **See the line:** `python3 .claude/skills/_shared/renderq/renderq.py status` (who holds each slot, every waiter in
  order, estimated start times, builds running outside the queue). Reading it is covered by the standing render-queue
  authorization (AGENTS.md, 2026-10-20).
- **What is gated, with no change to any script:** the wrapper at `Media/video_edit/bin/ffmpeg` (real binary
  `ffmpeg.real`) queues every heavy ffmpeg call; Whisper (`whisper_chunked.py`, `cut/speech.py`), HyperFrames renders
  (`hfbuild.render`), `deliver/gate.py`, `watch.py`, `framecheck/gate.py` and `clipcheck.py` take their own slot.
  `buildcap.wait()` now gets in line in the queue. Never waits: ffprobe, frame grabs, stills, audio-only ffmpeg,
  stream copies, anything 5 s or shorter, review servers. Audit of what still gets past it (2026-10-20 evening):
  `Handoffs/results-20261020-renderq-drives.md`.
- **Budgets, not slot counts (v3, 2026-10-21).** Every step gets a core allowance: heavy 4, light 2, quick 2. Past the
  floor (2 heavy, 1 light and 2 quick always run, so the line never stalls) a step starts only while (a) the cores in
  use plus its own fit in the Mac's 10 minus 2 kept for sessions and the UI, and (b) memory has had room for 30 s: at
  least 8 GB free or inactive, swap not growing, no macOS memory-pressure warning. `renderq.py status` shows cores and
  GB per holder and why the line is closed; `renderq.py why [VIDEO]` explains one waiter. Why: on 10-21 two "slots"
  held two chroma keys with 11 one-GB workers, swap filled and 27% of all CPU went to paging, so every job ran slower
  than two alone. Results: `Handoffs/results-20261021-renderq-v3.md`. Work inside a slot runs at nice 10.
- **Size every worker pool from the allowance:** `Pool(int(os.environ.get("RENDERQ_CORES", 4)))` (also
  `ProcessPoolExecutor`). Every slot holder exports `RENDERQ_CORES` to what it runs. Never `cpu_count()` or a fixed 6
  in a pipeline step. The ffmpeg wrapper can also add `-threads <allowance>` to calls that set none, but that is OFF
  (measured 10-21: a capped encode loses its CPU share to everything uncapped and ran 2.5-3x slower); it goes on once
  the chroma key and the other big thread users size from `RENDERQ_CORES`. When it is on, x264 output bytes change
  with the thread count: compare pictures and audio, not file hashes, for re-renders.
- **Quick lane (2026-10-20 evening): short clips never wait behind long renders.** Heavy work on short media takes one
  of two quick slots, first come first served: ffmpeg calls whose inputs total 20 s or less (or `-t` up to 20 s, up to
  600 frames), `clipcheck.py` on clips of 15 s or less, HyperFrames graphics of 10 s or less. An 8 s AI clip's frame
  dump, trim or clip check starts at once. Why: earlier that day 1-second frame dumps waited up to 21 min and
  21-second clip checks up to 73 min behind 10-minute renders.
- **Per-drive caps:** each drive runs at most its cap of heavy steps at once, Extreme 2, Expansion 3, internal 6,
  Seagate 2 until measured (`renderq/drives.json`, measured with `renderq/drivebench.py`). A waiter whose drive is full
  steps aside and the next job on another drive goes first. `renderq.py drives` shows each drive's load and free space.
- **Every new job's work folder comes from the queue:** `python3 .claude/skills/_shared/renderq/renderq.py workdir
  <JOB> --need <GB>` prints and creates it: the job's existing `/Volumes/<drive>/_edit_work/<JOB>/` on any drive (a job
  never splits across drives), else one on the least busy plugged-in work drive with room (Extreme keeps 30 GB free,
  the hard disks 100 GB). Do not type a drive for a new job. `--source <footage>` steers away from the hard disk the
  footage is on; `--why` prints the scores. Rounds of an existing video stay in its folder.
- **Throwaway files go in scratch on the internal SSD:** `renderq.py scratch <JOB>` prints `/tmp/absbyai-scratch/<JOB>`
  while the internal SSD keeps 50 GB free (else `_scratch` in the job folder). Frame dumps, test renders, temporary
  intermediates that nothing reads after the step that made them. Never review images, anything Dan sees, or caches a
  later round reuses (`clips_graded/`): scratch untouched for 48 h is deleted. HyperFrames graphics render there and
  move into place. Why: the Extreme SSD runs 99% full, slows down when shared by more than two jobs, and stores
  frames in 45% more space than the internal SSD (measured 2026-10-20).
- **Run builds in the background** (`run_in_background`, `nohup`, a chain script): a queued step can wait past the
  10-minute Bash timeout, and a killed waiter loses its place.
- **New per-round scripts: wrap the whole script as one step** so its steps do not re-queue:
  `python3 .claude/skills/_shared/renderq/renderq.py run --group <VIDEO> -- bash render_r2.sh` (`--light` for checks).
  Name the video with `--group` or `export GATE_GROUP=<VIDEO>` (running from `/Volumes/*/_edit_work/<job>/` names it
  automatically): a video already running goes ahead of videos not yet started. `--priority` only when Dan is waiting
  on that exact output. Drop old `wait_slot`/`pipeline_slot` loops; they double-wait behind the queue.
- `GATE_OFF=1` skips the queue for debugging only, never for a real build.
- **Why, measured 2026-08-27:** four ungated builds drove the Mac mini (10 cores) to load 242 at 0% idle and made
  `finish_audio.py` take 126 s against 13.6 s quiet (9.3x), with no throughput gain. Load average misleads on macOS
  (130 at 15% idle on 2026-10-20); the queue reads real CPU idle from the kernel. Full 08-27 numbers:
  `.claude/skills/_shared/timing/REPORT_20260827_build_timings.md`.
- **Exception: upload and setup encodes run at once on the hardware encoder (Dan, 2026-09-30):**
  `nice -n 20 ffmpeg -hwaccel videotoolbox ... -c:v h264_videotoolbox ... -c:a copy`. The queue exempts
  `h264_videotoolbox` automatically. Setup/upload copies only; editing renders, QC, transcription and x264 encodes queue.
- **Never run a pipeline script inside another session's live build directory.** It will overwrite intermediates that
  session is reading. Work in a scratch copy.
- **Keep build intermediates off the iCloud-synced project folder** (use the `renderq.py workdir` folder or `renderq.py scratch`):
  files written under the project folder's `tmp/` keep iCloud's `fileproviderd` at 50-160% CPU while it syncs them.

## Video review refinements — C1652 R3 (Dan, 2026-09-17)

- **Clip variety means different visible content, not merely different IDs or trims.** Do not reuse stock from essentially the same scene/shoot with the same actors or actresses, even from a different camera angle. Doctor inserts within one video need distinct casts and settings. Prefer suitable Pexels/known-rights footage; use authorized AI generation if no suitable distinct clip exists.
- **Exercise illustrations must vary the exercise.** For Dan demonstrating daily exercise, use ab wheel plus toe touches or kettlebell deadlifts, not repeated ab-wheel footage. This includes similar excerpts from one source video. Dan remains the same person; the exercise action must differ. Necessary repetitions inside an actual exercise teaching demonstration are a different purpose.
- **No added camera movement in horizontal16:9 presenter footage.** Do not pan, drift, track or recenter just because Dan shifts slightly. Keep a fixed composition within the shot; preserve approved framing sizes and deliberate cuts unless separately rejected. Check rendered footage, not just a fixed-center setting.
- **Requested AI narrative clips require actual motion.** A static frame, start/end montage, slow image pan or brief motion fragment followed by a held endpoint is not a completed clip. Generate and validate the intended motion from approved assets; do not ask again for unchanged approved frames. This does not prohibit real photo displays or specifically approved scientific still illustrations.
- **Three-photo screen template:** use three vertical real studio portraits with distinct poses and consistent presentation proportions; plural disclosure, now worded “Real Photos Of Me, Not AI-Generated” (2026-10-17), clear of faces/abs. Save the tested layout for reuse.
- **Organic graphics:** Soft Blue Light (GRAPHICS-STANDARDS.md, 2026-09-26) replaced the Muhammad graphics rebuild; lower thirds and full-screen treatments came from `softblue.py` at the time; since 2026-10-17 every new or revised graphic is built from the HyperFrames templates and moves for its whole screen time (section near the top of this file). Use self-contained titles that name the topic. Specific approvals with limited requested edits take precedence over a general redesign; for C1652's Zepbound/stakes lists, enlarge text as requested and preserve the otherwise approved panel design.

## Horizontal footage stays completely static — Dan, 2026-09-17

- **No added camera movement or recentering on Dan in horizontal/16:9 videos.** No tracking, pan, drift, animated crop or zoom to follow or center him. Choose a fixed composition for each shot and leave it fixed. This supersedes earlier horizontal exceptions for approaching the frame edge; tracking is only for square/vertical layouts when actually needed.
- Ordinary cuts between fixed compositions remain editing cuts, not camera motion. Graphics may animate without moving the presenter picture beneath them. Check actual rendered background landmarks: a fixed-X setting alone does not prove a static picture. If the camera source itself drifts, resolve that in source choice/stabilization rather than silently claiming the delivered picture is static.
- Dan approved C1652 R4 as good enough to ship despite a small remaining movement near1:09. Do not reopen that accepted film to enforce the future rule. Its approved master is SHA256 `eace1bdbb9f7a16fadff8bb2d2e80812ea4e777cf413a1e06575527f95d64f44`.
- C1652’s Zepbound text size is approved. Dan would prefer a third benefit, “Makes you serious about fat loss,” in a future relevant treatment; he accepted the existing two-row graphic in this final film. Do not expand its content without speech/timing context in future work.

## On-screen text graphics are KEY POINTS, not a second set of subtitles (Dan, 2026-09-18)

*The distil-not-echo rule stands. The FORMAT was narrowed on 2026-10-09 and 2026-10-16: title capitalization everywhere ("Key Point:" if the prefix is used), FULL CAPS on a word only where it truly carries the punch, about one graphic in six at most, never automatic.*

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

Read [GRAPHICS-STANDARDS.md](GRAPHICS-STANDARDS.md) before designing or revising graphics. Soft Blue Light is now the standard graphic family for all videos, including website VSLs, ads, organic videos, Shorts and newly revised square/vertical graphics; the approved Motivation lower-third format is locked for lower thirds in all videos (built from the HyperFrames templates and moving for its whole screen time since 2026-10-17). This 2026-09-26 expansion supersedes older Muhammad graphic palettes and website-only scope. Preserve already approved exports unless their graphics are explicitly being revised. Muhammad sound, camera color and transition references retain their separate scopes. That reference also defines three-portrait screens, sequential horizontal photos, credible iPhone framing, single rounded blue cards behind side text lists, with no secondary full-height field and fixed presenter positioning with intact arms. These specific approvals supersede conflicting older graphic examples. Keep source-specific crop, color and audio settings scoped to their recordings.

## Exercise demonstration timing and visual cues (Dan, 2026-09-25)

- Match each demonstration to the words being spoken. Show correct form while Dan gives the positive instruction, then show the mistake when he warns against it. If he returns to a positive instruction, return to correct form or the presenter. Set picture cuts from the heard words and check moving action on both sides of every cut. Swapping clips at their old boundaries is not enough if the result still contradicts the narration. DS-18 R7 demonstrates this for weight placement, toe direction, back position and glute squeeze versus hip thrust.
- When a form detail is hard to see, point to the relevant body part or equipment with green arrows for correct form and red arrows for the mistake. The color, label and visible action must agree. Keep arrows on the target as it moves, clear of captions and the teaching action. Do not add arrows to a shot with no specific feature to point out.
- A recurring overlay needs a clear teaching purpose. Check it against the narration, captions and action; omit it when it repeats information without helping the viewer. When removing one element from a combined graphic layer, preserve unrelated approved elements in that layer.

## Scene-content and freeze review (Dan, 2026-10-09)

Every editing skill also follows section 5 of [CUT-CONTINUITY-QC.md](CUT-CONTINUITY-QC.md): check required scenes against independently approved assets, dispose every native freeze candidate including declared graphic spans, and compare pickup joins with moving original context. Copying an approved master accurately does not prove its scene is correct. A missing phone scene or same-framing presenter reset remains a finding even when inherited. Reconcile contradictory evidence before delivery; do not carry a wrong judgment forward merely because the reviewed pixels are unchanged. This repairs the review procedure without changing automated gate thresholds or claiming new automated coverage.

## Default jump-cut and junk-footage pass (Dan, 2026-09-29)

Every new video edit and revision runs [CUT-CONTINUITY-QC.md](CUT-CONTINUITY-QC.md) by default, starting with selected source footage before the first approval preview and repeated on the exact final candidate. Inspect every source/picture join, including composite internals and cutaway entrances/exits. Remove uncovered presenter jumps using distinct fixed wide/tight cuts or complete approved clip cover; pose matching alone does not clear a same-framing jump. Detect confirmed unscripted sounds, empty lead-ins, unnecessary pauses and looking away while resetting, then remove them without clipping words, stripping normal breaths or removing purposeful teaching pauses. Review native consecutive frames and moving/audio context, record each repair, and inspect every new boundary. Detector/ASR flags require actual source verification. This supplements existing gates and preserves still/frame, motion and full-render approval requirements. Do not retrofit already approved masters without scoped revision authorization.
