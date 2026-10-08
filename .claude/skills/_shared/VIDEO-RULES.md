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
  invite it. The frame approval gate, the $5 per video clip budget and the no-belly-framing rule are unchanged. No new voice
  is ever made: the lips follow Dan's recorded impression.
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
  `Daily Salad SFC R3 - short 4 - Stop Buying Salad Dressing.mp4`. After a re-render he will review, replace the copy.
  Then open the folder for him (`open "Videos to Review"`) and list the file names in the chat message beside the page
  link. The review page is still built every time.
- **When Dan finalizes a video, delete its copies from `Videos to Review/` in that same session.** They are copies for
  watching; the delivery folder stays the record. Delete only that video's files, never another task's.
- The folder is git-ignored (the repo is public). Claude and Codex both do this, in every video skill.
- **Review pages must survive the editing session and Mac restarts (Dan, 2026-10-08).** Start them with
  `python3 .claude/skills/_shared/review_server.py PORT DIR`. On this Mac the command installs a per-port login service,
  verifies it is running, and returns. macOS restarts it after a crash and at the next login. Do not use a temporary
  terminal server, `nohup`, or `python3 -m http.server` for a delivered review. `--serve` is for the managed worker/tests.
- Reuse the same port and review folder when repairing an existing link. Never replace another review on that port.
  The service code and web-linked review assets are copied to local Application Support. Published pages therefore
  work even when the editing drive is disconnected. This also avoids macOS background access failures on removable
  drives. Only files linked from the page are cached; raw footage and build intermediates are excluded. Run the same
  command after updating a review page or export to refresh its cache before giving Dan the link. The command checks
  the served page before reporting success. VLC copies are actual files, not shortcuts to the external drive.
- Before sending a page link, load the page and request a byte range of one video (expect 200 and 206), then verify
  browser seeking. When changing server lifecycle code, also terminate its managed worker and prove the same URL
  recovers automatically. Never claim a reboot test unless the Mac was actually restarted.
- After Dan has reviewed and finalized a video, remove only its review copies and stop its now-unused page service
  with `python3 .claude/skills/_shared/review_server.py PORT --remove`. This also removes that page's local cache.
  Retain original delivery files and approvals.
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

## Thumbnails: five choices, made by Codex inside the Claude setup task (Dan, 2026-10-02)

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
- The delivery gate still carries the ad rule on organic formats (`compliance:drug_names` and the `srt:shape` banned spelling "Zepbound"/"Ozempic" on `longform`); until that is changed with the regression corpus and a `GATE_VERSION` bump, those two rows failing on an organic video are the known mismatch, not a defect. Spoken and subtitled drug names are correct. Brand names in on-screen graphics on organic videos: not yet ruled; keep them out until Dan says otherwise.
- Related, same day: do not tell viewers to "empty the entire vial" (Dan cut that ad-lib from RO-12: people on non-standard doses do not).

## Organic content approval budget (Dan, 2026-09-29)

**Round 1 now always shows Dan every graphic, stock item and clip (Dan, 2026-10-08; section near the top of this file).** For organic content videos, the newer approval budget below replaces older requirements for Dan to approve every graphic and clip separately and the shared 10 to 15 decisions per video guidance. Keep the stepwise internal checks and the real approval gates. The **first approval round has at most 20 decisions**. In later rounds, **aim for 10 or fewer decisions per round**. These are ceilings, not targets. Ask Dan only about materially uncertain choices that require his judgment. Choose and check routine assets yourself, summarize what you chose, and let him overrule while reviewing the first minute and the finished film. Never reopen unchanged approved items or infer approval from silence. New AI motion still needs approved start/end frames first; show materially uncertain finished motion in context before locking it. The website VSL approval cadence remains separate and more detailed.

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
    with no "tap/click the button below". Organic goes through `/video-setup` only: Private YouTube holding copy +
    Blotato release on every platform.
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

- **Reaffirmed by Dan, 2026-09-16:** Gemini and Replicate generation is standing-authorized up to **$5 total per video**. Use the project's Gemini/Replicate keys, including `bakeoff/.env`, for this authorized work without asking again. Ask for spend authorization only before exceeding $5 for that video; do not request separate approval for a batch within the remaining budget. Track costs and retries across revisions. Dan explicitly approved the pending C1652 three-clip batch (estimated $0.75) after being told the earlier built-in still costs were unreported; preserve those unknown costs honestly without repeating the same permission stop.
- Up to **$5 per video** is authorized for AI clip generation. Count supporting start/end-frame generation and paid retries in that video's total; a new task or revision does not reset it. This more specific limit applies within the existing session and batch limits above.
- Before exceeding $5, discuss the specific clips, why existing assets or suitable stock will not do, and the estimated new total. Dan is generally open to **up to $10 with a reason**, but that is not automatic authorization to exceed $5.
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

## One new long-form release each Sunday (Dan, 2026-10-07)

- New organic long-form videos release on YouTube only on Sundays at 9 AM America/Chicago through Blotato, at most one per week. A revised replacement upload uses one Sunday slot. Shorts and unlisted ads have separate schedules.
- Read the live Blotato YouTube queue and recent releases before selecting a slot. If the next Sunday already holds a long-form, append the new video after the last queued long-form on the next free Sunday. Never add a Wednesday or other midweek long-form to make room.
- YouTube releases first. Schedule the long-form's Facebook, Instagram and TikTok copies no earlier than Monday at 9 AM America/Chicago, 24 hours after the Sunday YouTube slot. Do not release all platforms together. Verify the YouTube video is actually public before the other posts go out. If the YouTube release fails or is delayed, postpone the other posts until after it is public.
- If a long-form is queued midweek, move YouTube to the end of the Sunday queue and its other platform schedules to the following Monday. Verify every saved time from a fresh pull.
- This binds Claude and Codex, including handoffs and direct Blotato scheduling. `scripts/blotato/longform_queue.py` must refuse an off-Sunday or occupied Sunday YouTube slot.

## YouTube visibility — never upload Public (Dan, 2026-09-16)

- **Never upload any video to YouTube as Public, and never use YouTube's native scheduling/publish-at path.** This applies to API uploads, Studio uploads, scripts and manual work. The upload-time visibility must always be non-public.
- **Ad videos are always uploaded Unlisted.** No ad gets a separate Public YouTube copy, even if it will also be used on other platforms.
- **Organic videos: Blotato only (Dan, 2026-10-01).** No Private holding upload. Blotato creates and releases the public YouTube video at the scheduled time; we never upload organic content to YouTube ourselves and never use YouTube native scheduling or publishAt. Ads stay Unlisted via `/ad-setup`.
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
- **Exception: upload and setup encodes run anyway, on the hardware encoder at lowest priority (Dan, 2026-09-30).** When a
  `/video-setup` or `/ad-setup` task needs a platform copy (Blotato's 400 MB cap, a TikTok cover-first copy) and two or
  more builds are already running, do not wait for a slot: run it as `nice -n 20 ffmpeg -hwaccel videotoolbox ...
  -c:v h264_videotoolbox ... -c:a copy`. The Mac's media engine does the work, so it barely touches the CPU the cap
  protects. Dan approved this on RO-05 (load ~300, four builds running). It covers setup/upload copies only; editing
  renders, QC, transcription and x264 encodes still obey the two-build cap.
- **Never run a pipeline script inside another session's live build directory** — it will overwrite intermediates that session is reading. Work in a scratch copy.

## Video review refinements — C1652 R3 (Dan, 2026-09-17)

- **Clip variety means different visible content, not merely different IDs or trims.** Do not reuse stock from essentially the same scene/shoot with the same actors or actresses, even from a different camera angle. Doctor inserts within one video need distinct casts and settings. Prefer suitable Pexels/known-rights footage; use authorized AI generation if no suitable distinct clip exists.
- **Exercise illustrations must vary the exercise.** For Dan demonstrating daily exercise, use ab wheel plus toe touches or kettlebell deadlifts, not repeated ab-wheel footage. This includes similar excerpts from one source video. Dan remains the same person; the exercise action must differ. Necessary repetitions inside an actual exercise teaching demonstration are a different purpose.
- **No added camera movement in horizontal16:9 presenter footage.** Do not pan, drift, track or recenter just because Dan shifts slightly. Keep a fixed composition within the shot; preserve approved framing sizes and deliberate cuts unless separately rejected. Check rendered footage, not just a fixed-center setting.
- **Requested AI narrative clips require actual motion.** A static frame, start/end montage, slow image pan or brief motion fragment followed by a held endpoint is not a completed clip. Generate and validate the intended motion from approved assets; do not ask again for unchanged approved frames. This does not prohibit real photo displays or specifically approved scientific still illustrations.
- **Three-photo screen template:** use three vertical real studio portraits with distinct poses and consistent presentation proportions; plural disclosure “Real pictures of me — not AI-generated,” clear of faces/abs. Save the tested layout for reuse.
- **Organic graphics:** Soft Blue Light (GRAPHICS-STANDARDS.md, 2026-09-26) replaced the Muhammad graphics rebuild; lower thirds and full-screen treatments come from `softblue.py`. Use self-contained titles that name the topic. Specific approvals with limited requested edits take precedence over a general redesign; for C1652's Zepbound/stakes lists, enlarge text as requested and preserve the otherwise approved panel design.

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

## Default jump-cut and junk-footage pass (Dan, 2026-09-29)

Every new video edit and revision runs [CUT-CONTINUITY-QC.md](CUT-CONTINUITY-QC.md) by default, starting with selected source footage before the first approval preview and repeated on the exact final candidate. Inspect every source/picture join, including composite internals and cutaway entrances/exits. Remove uncovered presenter jumps using distinct fixed wide/tight cuts or complete approved clip cover; pose matching alone does not clear a same-framing jump. Detect confirmed unscripted sounds, empty lead-ins, unnecessary pauses and looking away while resetting, then remove them without clipping words, stripping normal breaths or removing purposeful teaching pauses. Review native consecutive frames and moving/audio context, record each repair, and inspect every new boundary. Detector/ASR flags require actual source verification. This supplements existing gates and preserves still/frame, motion and full-render approval requirements. Do not retrofit already approved masters without scoped revision authorization.

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
