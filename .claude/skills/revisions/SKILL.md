---
name: revisions
description: Review a video cut delivered by an editor (human or a cheaper-model pipeline session) and produce a revisions document in Dan's exact format — timestamped, with specific directions, specific replacement text, and direct links to the exact assets to use. Use whenever Dan shares a video (usually a Google Drive link) and asks to "review it", "give revisions", "write up revision notes", or "check the editor's cut" — even if he doesn't say "/revisions". For revising videos OUR pipeline will re-render itself, /ad-edit and /longform-edit remain the execution skills; this skill produces the review document.
---

# /revisions — review a delivered cut and write Dan-style revision notes

The deliverable is a **Google Doc in Dan's Drive**, written in Dan's voice and format,
**as a draft for Dan's review** — Dan reads it and forwards the link to the editor
himself. Never send anything to the editor directly. Also save a markdown copy in
`revision docs/` in the project folder (repo is public — nothing sensitive in it).

**ALWAYS CONFIRM WHO THE EDITOR IS AND WHICH ROUND THIS IS BEFORE WRITING.** Dan runs
tryouts where several editors cut the SAME script, so a new cut of a video you have
already reviewed is usually a DIFFERENT editor's first attempt, not round 2 of the same
one. Getting this wrong makes the doc read as "you ignored my last notes" to someone who
has never seen them. If the cut arrives as a bare Drive link, ask.

**Write goals, not tool steps.** Dan's editors work with AI editing tools, not a fixed NLE.
Never prescribe a program's menu path ("In Premiere: Modify → Audio Channels"). State the
outcome — "the finished audio must come from the RIGHT channel only, as mono" — and leave
the method to them. A named-tool instruction reads as ignorance of how they work.

Two audiences, same skill:
- **Human editor** (default): plain-language, tool-agnostic directions, links to assets,
  no jargon, no file paths on Dan's machine.
- **Pipeline session** (an /ad-edit or /longform-edit session executing the fixes):
  same document plus exact source timecodes, local asset paths, and script names.
  When Dan asks Fable to review a cheaper model's pipeline output, write BOTH layers —
  the human-readable item and, indented under it, the machine-actionable detail.

## Dan's document format (learned from his own revision docs)

- Title: video name + editor + round number ("Video 1 revisions - Waleed - round 1").
  **Round numbers are per EDITOR, not per video** — during a tryout, three editors can each
  be on their own round 1 of the same script.
- A **THROUGHOUT VIDEO** section FIRST for anything not tied to one timecode, in
  \*\*BOLD ALL CAPS\*\* headers, each with sub-bullets. Rules he repeats every round
  live here (capitalization, crops, disclosure labels).
- Then a flat list of **timestamped items** in play order. Each item: the timecode
  (single `0:14` or range `1:41 - 1:52`), what to change, and — critical — the
  **specific replacement**: the exact text to put in a graphic, the exact asset with a
  direct Drive link, or exact source timecodes to pull ("Insert 0:57 - 1:02 from this
  video"). "Accelerate footage to fit duration" is the standard instruction when a
  replacement is longer than its slot.
- Give the on-screen POSITION of graphics (lower third, upper right corner, top two
  thirds / lower third splits, full screen).
- Exact text is quoted verbatim; capitalization instruction: Title Capitalization on
  all graphics, "don't use the capitalization I have in this document".
- For AI clips to be generated: give DIRECTIONS for what to generate, don't generate
  it. If we already have a matching asset, link that exact asset instead.
- Why-explanations appear only when the rule is new ("Why this is important: …").
- New standing rules get flagged: "For all future videos, …" / "Hard rule for future videos: …".
- **STANDING RULE blocks (Dan, 2026-09-10).** Muhammad edits with an AI tool, so a rule stated the same way every
  time gets learned and stops needing repeating. Every item that violates a standing rule gets, as its LAST
  sub-bullet, a bold line beginning `STANDING RULE:` — one or two sentences, the rule plus the why — and the
  same line is repeated under every item in every ad where it applies (Dan pasted the before/after rule into
  four ads and the goal-image rule into five). Use the canonical wordings in "Standing rules to check" below
  verbatim; do not paraphrase them per ad.
- **Bold the key change in every item.** The item is one diagnostic sentence, then the action in bold (the
  replacement, the removal, the exact text), then the timing. Dan bolded "**Replace it with the bad Photoshop with
  my face on the bodybuilder's body**" and cut a five-sentence 0:00 item down to "Take the logo out." plus the rule
  plus "Remove all graphics from this duration, just make this plain camera scene". A reader skimming the bold
  should be able to do the edit.
- **A finished ad gets one bold line under its H2: `APPROVED - FINALIZED - READY FOR HIGH QUALITY EXPORT`**,
  then the credit paragraph, and nothing else — no THROUGHOUT, no items (Ad 5 round 3, 2026-09-10).

## Calibration from Dan's edits — the doc must need ZERO changes (2026-09-03)

Dan's stated goal: he stops re-watching the cut and re-editing our doc; it goes to the editor as
written. These rules come from diffing our markdown copies of the Ad 3, 4 and 5 reviews (Muhammad,
batch 2) against the Google Doc after Dan edited it. Every item in every future doc is checked
against them before delivery (workflow step 7). Ads 2 and earlier in the same doc are Dan's own
notes — the register to match: "Remove this clip, use camera scene", "Replace with 0:00 - 0:05 from
this clip", "Insert these images full screen one after another with motion effect".

**Things he ADDED — defects we missed:**

1. **Transcribe every text graphic and check every word against the script AND the ad's subject.**
   Ad 3's bullet panel said "nutrition coach" — Ad 2's vocabulary, the template carried over — and
   our contact-sheet pass missed it; Dan added `2:08 Change "nutrition coach" to "personal trainer"`.
   Batch editors reuse graphic templates between ads, so the previous ad's nouns are a specific
   error class. Method: crop every panel/chip/card at full resolution, write its text out, compare
   to the transcript line under it and to the subject of THIS ad. Typos, wrong words, mixed
   capitals, a noun from the other ad — each is an item with the exact replacement text.
2. **Check EXITS, not only entries.** Ad 3 round 2: the phone mockup stayed up after the
   assessment clip ended; Dan added `3:22 Remove phone graphic from screen at this point`. For
   every insert and overlay, find the frame where it should leave and confirm it does; a frame
   element that lingers into the next beat is an item.
3. **Never cut before-imagery straight into after-imagery — the camera scene goes between.**
   Ad 5: our fat-dad pictures at 0:09 - 0:14 ran into "this is what I look like today" at 0:14.
   Dan shortened the insert to 0:09 - 0:12 and added "Briefly show camera scene again before
   showing after pictures (avoid showing before and after pictures back to back)". Back-to-back
   is a sequential before/after and reads the same to Google as a side-by-side. Check every
   before→after adjacency in the timeline INCLUDING the ones our own inserts would create, and
   give the before insert an end time that leaves ~2 s of camera before the after visual.
4. **Check panel composition, not just content.** Ad 5 0:17: the header sat at the top of the panel
   and the one bullet in the bottom third with dead space between; Dan added "Move text up to
   center of graphic, rather than bottom". Text block vertically centred in its panel, header and
   bullets together, nothing jammed against an edge.

**Things he CHANGED — our directions were mis-calibrated:**

5. **A directed new clip is always "stock footage or AI clip".** Dan added "or AI clip" to both of
   our "Insert stock footage of …" items in Ad 5. Write "Insert stock footage or an AI clip of …"
   and, when the AI label rule is not already in THROUGHOUT, "if it is AI, it gets the label".
6. **The casting rule is for the man the viewer is meant to be; antagonists are cast as the
   caricature.** Ad 4 0:43 influencer: we wrote "White or Asian man, 30 - 50, in shape"; Dan
   rewrote it to "fitness influencer bro … Man around 20 years old in good shape, but who looks
   douchey." Fat trainer, influencer bro, the "somebody else" whose plan you downloaded — cast them
   as what the script mocks. Aspirational or identification shots (a man training, cooking, the
   fitness-model line, the dad at the kitchen table) — white or Asian, 30 - 50, in shape. A neutral
   prop shot (a man opening a pill bottle, Ad 4 2:06) is not a swap item on its own; if the casting
   rule needs restating, one line in THROUGHOUT covers it.
7. **State the requirement; diagnose the person on screen only when it is the reason and you
   verified it at full resolution.** Ad 5 2:42: Dan struck "Same problem, he has the dad bod the ad
   is selling against." and kept only "In shape white or Asian man, 30 - 50, cooking a healthy
   meal". He kept "he is an average build" (0:58) and "He is 60 and obese" (2:29) because those were
   accurate and were the reason for the swap. A guessed body judgement costs credibility with the
   editor; an unmistakable one is the argument.
8. **Only fix what is wrong against the script or a rule; the editor's own header labels are his.**
   Ad 5 0:17: we asked for the header "IN TODAY'S EPISODE" to become "IN THE NEXT FEW MINUTES"
   ("this is an ad, not an episode"); Dan deleted that and kept only the bullet-text fix, which was
   a real error against the script. Header/label wording is an item only when it is misspelled,
   mis-capitalised, or contradicts the script or a rule — never because we would have worded it
   differently.

**Things he DELETED — items that should not have been written:**

9. **Do not pad a line that already has a correct asset.** Ad 3 2:40: one photo-shoot picture was
   on "this is what I look like today"; we asked for three more from the reference folder. Dan cut
   the item. An item must fix something — wrong asset, missing asset, rule violation, dead
   stretch, wrong text, bad exit. "More of the same" is not a fix.
10. **Do not force an asset onto a line it does not literally match, and do not stack before
    imagery.** Ad 4 2:16: we put the heavier-Dan couch clip on "a cabinet full of supplements and
    still getting fat", directly ahead of the before picture and two fat-dad photos at 2:20 — four
    "before" visuals in seven seconds, none of them a cabinet of supplements. Dan cut it. One
    before beat per section, on the line that names it.
11. **Not every dead stretch gets a bullet build.** Ad 5 2:17 - 2:29 ("built for someone else …
    different work hours, a different budget, a different body, foods you honestly hate"): we wrote
    a four-bullet build of that list straight after the CTA build at 2:05; Dan cut it and kept the
    other eight fills. Every fill he kept puts a benefit, a hook or a claim on screen ("It adjusts
    your calories", "Built around steak", "It stopped being a wish"). Do not put a list of negatives
    on screen, and let the beat right after the CTA build sit on camera. If two builds would land
    within ~15 s of each other, keep the one that carries a benefit.

### Calibration pass 2 — Dan's edits to the 2026-09-08 batch (Ads 3–8, Zeeshan r3, Waleed r3)

Dan's verdict on the batch: "very good, you got most of the major things", with one correction: **too many
calls for graphics.** His rule, in his words: a graphic goes in when it adds value; 10 to 20 seconds of just
him talking is fine when a graphic would not contribute anything; **but when in doubt, put it in — a graphic
is easy for the editor to remove, and sometimes the idea is good.** So the error to avoid is the reflexive
fill, not the occasional judgement call. The diff of what he cut (method: lesson 34) makes the line precise:

12. **A text chip earns its place by stating an outcome or benefit in his positive voice.** Kept: "It stopped
    being a struggle" → "It started to feel easy" (twice), "You get the picture AND the plan", "The two-picture
    trick that made my motivation automatic". Cut, regardless of gap length (7 s and 12 s alike): anything that
    paraphrases or quotes the sentence being spoken, a list of negatives, a question chip, a "2" added to the
    editor's numbered chips, a two-line near-verbatim restatement (that is a subtitle). Text-chip fills went 5
    kept of 14; picture and clip fills went 4 of 4. **Budget about two added text chips per ad** and choose
    the two strongest benefit lines instead of filling every stretch you list.
13. **Bullet builds are the heaviest form and get cut first** (0 of 2 new builds survived), and **never direct
    a panel that already exists in another ad of the batch** — the Ad 6 "IT ADAPTS TO YOU" build was Ad 3's
    panel, and the Ad 6 "Day 1 / Day 4 / Day 10" chips were Ad 5's device. Each ad gets its own graphics.
14. **App screens are repairs, not fills.** Every app screen that REPLACED a wrong visual survived; all three
    meal-plan / workout screens dropped into a talking-head gap were cut. Direct an app screen only where the
    line names the app doing something and the picture on screen is wrong or missing.
15. **The VISUAL DENSITY paragraph must not promise a fill per stretch, and no item may point at another
    ("fix in the 0:00 item below").** Dan deletes items without repairing cross-references: Ads 6, 7 and 8
    went out listing stretches whose fills were gone, Ad 6's THROUGHOUT pointed at a deleted item, and Ad 3
    still said "Four things are left" after he cut one. Write every item self-contained and count nothing.
16. **A truncated lower third is a chip, not a defect.** Ad 3 R3's "…let your AI trainer help" item asked the
    editor to complete it into the spoken sentence; Dan cut it — completing it would make a subtitle. Do not
    ask to lengthen a chip.
17. **Check the hero asset against the literal script claim, not the concept.** Ad 7's title is "I Photoshopped
    MY FACE on a Fitness Model"; the editor's gag image did not use Dan's face and we praised it. Dan added
    "Swap this for an AI clip of my before picture's face on a bodybuilder's body" and propagated "(with MY
    FACE …)" into both callbacks of the asset. When a hook asset is corrected, correct every callback in the
    same doc.
18. **On-screen text must stand alone.** Dan replaced "it's far better at it than ChatGPT…" (our item only
    fixed the capital I) with "Abs by AI is FAR BETTER at generating your fitness goal image than ChatGPT or
    any general purpose AI". A panel whose pronoun has no referent for a viewer reading it cold is a text
    item, with the product and the claim named and the superlative in caps — rule 8's "leave his wording"
    yields here.
19. **The proof on a "got the abs" line is two real pool-shoot after photos, the same two as the previous
    ads — not the AI goal image, and not four stills.** Ad 8: he swapped our goal-image beat for "Show TWO
    after pictures from pool photo shoot here, same as used in previous ads" and cut our four-photo run to
    two. Two stills per beat; split a longer set across two beats; reuse the batch's after photos.
20. **Typography consistency is part of the text-panel pass.** He added "The spacing between letters on
    calories is different from the other words" under our capital-I item — check tracking, weight and size
    of every chip against its neighbours, not just the words.
21. **In a closing round, do not add a footage request for a mild picture/line mismatch.** Zeeshan r3: a
    kneeling rollout under the line about the standing variation was cut as an item; "none of it is new
    work" has to be true. **American spelling always** (COLOUR → COLOR was his only edit to Waleed's doc).

### Calibration pass 3 — Dan's edits to the 2026-09-09 batch (Ad 3 r4, Ad 5 r3, Ad 6 r2, Ad 7 r2, Ads 9/10/13/14 r1)

Dan's verdict: "pretty good", with one big correction — **too picky on audio in rounds 2 and 3** — plus the two
format rules above (STANDING RULE blocks, bold the key change). The diff (method: lesson 34) makes it precise:

22. **Late-round audio: once it sounds right, stop asking.** He deleted the whole audio block on Ad 5 r3 (−14.0 LUFS,
    true peak −0.2), Ad 6 r2 (−13.7, −0.8, tone and NR off) and Ad 7 r2 (−13.6, −0.7, NR off), and kept it on Ad 3 r4
    (−15.3 LUFS, 0.0 dBTP with 35 clipped samples) and on every round-1 cut. The line: on a round ≥ 2, audio is an
    item ONLY if the level is outside −14 ±1, or the true peak is at/over 0 with clipped samples, or the mic/room is
    wrong. Tone, the artifacts row and a ceiling at −0.7/−0.8 dBTP are round-1 notes, never a reason for another
    round. If audio was the only thing left, the section is the APPROVED line (Ad 5).
23. **Do not itemise the end hold.** Every "hold the last frame ~2 s" item was deleted (Ads 5, 6, 7, 9, 10, 14 — holds of
    0.2 to 1.2 s). The only end item that survived is Ad 13's, where the button LEFT while he was still saying "get
    started". Rule: an end item exists only if the button or the picture cuts off before the last word ends.
24. **Fills are still being cut.** Ad 9's one benefit chip (2:08) went, and so did the phone-lock-screen asset swap at
    1:52 (the goal image on the card is fine on that line) and Ad 13's "$1,000+/Month" chip replacing his two verbatim
    hook chips (his skip-stopper chips are his). Round-1 fills: none unless a 15 s+ stretch has nothing and the chip
    is a benefit. Never replace an editor's own hook chips with ours.
25. **App / phone demos are a one-line fix plus the rule, and the fix is a link.** Dan replaced both Ad 10 demo items
    (a paragraph each about the upload being a stranger) with the same block: "The real app recording is the right
    thing here, keep it. But it ends on the Generating screen and never pays off. … end on that recording's own
    after picture alone … Small AI-GENERATED tag on it" + the recording link + STANDING RULE. Write that block, link
    the recording, and let the link carry the "whose photo" fix. **But the identity check is still ours to do:** he
    ADDED an item we missed on Ad 14 — "2:00 - 2:07 Use this photo for before picture in clip. The script says 'my
    body, my photo' but the before picture isn't me." Check the before picture inside every phone/app clip against the
    real before picture at full res (lesson 10 in reverse) and, when it is not Dan, one line + the before-picture link.
26. **After-photo beats: two real photos, Dan picks which.** He struck the item asking for the script's specific
    "trees, hands on hips" still (any real after photo satisfies the cue), kept "Show TWO pictures here" but removed
    our picks and links, leaving empty image slots he fills himself, and wrote "use these ones, different from
    before" on the second beat. Rule: itemise count (two) and label (none), write "images below" with two empty
    sub-bullets, do not choose the stills, and never repeat the pair used in an earlier beat of the same ad. The
    "used my family as an excuse" line takes the two fat-dad-with-daughter photos, not the before picture.
27. **Adjacency inside or beside an approved AI asset is not an item.** Ad 7 0:26: the phone clip (heavier me holding
    the ripped picture) running into real ripped me on the mat was cut — after→after is fine, and the heavier/ripped
    pair inside that clip is the approved asset itself.
28. **A bullet panel mid-build is not a composition defect.** Ad 10 2:07 ("first bullet at the top with dead space
    until the second comes in") was cut; rule 4 applies to a finished, static panel only.
29. **Logo item = "take the logo out" + STANDING RULE + "camera scene".** Do not design the replacement title chip
    (Ad 14 0:00: our two-line title and "drop the lower third" were cut; he wants plain camera scene there).
30. **Missed defect to add to the pass:** the before picture inside the Ad 14 phone clip at 2:00 was not Dan (rule 25).
    Nothing else was added, so the picture pass is otherwise calibrated.

### Calibration pass 4 — Dan's edits to Zeeshan's content-batch video 1, round 1 (2026-09-11, a workout follow-along)

He added three THROUGHOUT items to our doc, all of them things we measured and then credited instead of flagging:

31. **Framing is checked on every cut, workout sets included, against the hair-anchored standard** (memory
    `framing-standard-hair-anchored`). He added "**Crop in closer by 20-30% throughout the video**": in the wide shot no excess
    space above the head or to the sides, in the tight shot almost as tight as possible without cutting him off. Our pass
    confirmed that a wide / punch-in / wide pattern existed and never judged how big he was in the frame.
    `reference/framing.py` now measures it (step 3).
32. **The effort sound in a live set is NOT "right because it matches the raw clip".** We proved the camera track ran under
    the sets at the same gain as his talking and credited it; he added "**Reduce volume of my mic by 80% while I am actively
    doing sets. Keep volume the same when I am talking**". Grunts at their natural level (momentary −9 LUFS against −14 to −16
    for speech) are too loud for him. `reference/sets_level.py` measures it (step 1): the effort peaks must sit 5-14 dB
    under the talking level; within 5 dB of it (or above), write his item plus the STANDING RULE below.
33. **Judge the music bed's genre and energy against the video type, not only its level.** We credited "the music sitting under
    my voice where it should" (the level was right); he added "**Change music to this music track**" plus the rule below. For a
    workout, a bed that is chill or elevator-like is an item even at the perfect level. Supply the replacement link yourself
    (Pixabay, not Content ID registered: the track page must NOT show "Content ID Registered"), and check the genre tag. A
    "trip-hop" or "lofi" tag is chill however high its BPM.
34. **When he adds an item that contradicts a credit sentence, fix the credit sentence in the same pass.** His 80% item sat
    under our line "the wheel and my breathing sit at the same level as my talking, which is exactly right".

**Dan's vocabulary — use his words:** "camera scene" (the talking head), "motion effect" (the
Ken Burns move on stills), "accelerate footage to fit duration", "clip", "bro", "douchey". A simple
item is one line in that register; keep the longer form only where the editor needs exact text,
exact timing or an exact link.

## Review workflow

0. **Fetch.** Drive file IDs come from the URL. Download with
   `python3 -m gdown <FILEID> -O video.mp4` into the scratchpad (installed for
   python3.9). `ffmpeg`/`ffprobe` are NOT on PATH — use the static builds in
   `Media/video_edit/bin/`.
1. **Audio first — run the shared standard on the editor's file, so the doc quotes the same numbers
   we hold ourselves to** (2026-09-02; `echo_check.py` and `chan_align.py` are now shims):

       python3 .claude/skills/_shared/audio/pick_lav.py CUT.mp4 --analyse
       python3 .claude/skills/_shared/audio/audio_gate.py CUT.mp4 --no-stamp --ab AB_his-vs-editor.mp4

   `pick_lav --analyse` prints every stream/channel with SNR, decay, EDT, clipping, and the pairwise
   lag + polarity — it handles 2-channel files AND the 8/28 four-track rolls (the old `chan_align.py`
   exited "not stereo — nothing to compare" on those, so the review gate reported nothing wrong).
   `audio_gate` measures the delivered file against Muhammad's ad on the ten rows Dan rejects on
   (image, comb, room, tone, floor, dryness, loudness, spread, true peak, silence/length). Quote the
   FAIL rows with their numbers in the doc, in editor-friendly words, and attach the A/B clip. The
   signatures to recognise:
   - L/R strongly correlated at 0 lag but echo peak ~7–8 ms in speech ⇒ the editor
     **summed the two camera mics** (right = lav, left = room mic ~2.6 m away; the
     comb filter is baked in and un-EQ-able). The fix must happen at the source:
     rebuild the voice from the RIGHT channel only, as mono. State that as the outcome,
     not as a menu path. Full background: /longform-edit
     Step 0.4. Write this as the #1 THROUGHOUT item in editor-friendly words.
   - Two mics hard-panned (raw pair shipped): `pick_lav` reads a strong pair peak at ±7–8 ms,
     zero-lag near 0, and the gate's L/R row fails. Two mics summed: L/R ≈ +1.0 but the gate's comb
     row fails (ripple ≈ 1.1 dB vs his 0.54). Roomy: the EDT row (>80 ms; his 40).
   - Loudness and true peak are gate rows (−14 ±1 LUFS, ≤ −1.0 dBTP). Editors have shipped
     −8 LUFS / +2.5 dBTP with audible clipping.
   - Music bed: noise floor p5 above ≈ −45 dB in speech gaps *suggests* one; our shoots' raw
     floor is ≈ −53 dB. **This heuristic false-positives on an over-loud, hard-limited master** —
     confirm with per-band gap spectra on the lav channel before claiming a bed exists.
   - **Workout videos (live sets): measure the effort sound against the talking** (calibration rule 32):

         python3 .claude/skills/revisions/reference/sets_level.py CUT.mp4 --whisper CUT.json

     Transcribe with `--word_timestamps True` for this: after music, segment starts snap to Whisper's 30 s windows
     and swallow the end of a set. Target: the grunting, breathing and equipment are audible but clearly under the
     voice, with the effort peaks (p95 momentary) **5-14 dB under the talking level**. LOUD (within 5 dB, or above
     it) is Dan's "reduce volume of my mic by 80% while I am actively doing sets" item plus the workout-sets STANDING
     RULE. BURIED (max more than 20 dB under) is the explainer round-3 "no sound in the sets" item. Zeeshan's ab
     wheel follow-along read +2.2 to +5.4 dB ABOVE the talking (single grunts +10 to +12 dB): all three sets LOUD,
     and Dan rejected it. His approved ab wheel explainer (09-09) read -6.9 to -9.9 dB: all three OK. The 5 dB line
     sits between the two, and Dan's "80%" on the rejected cut lands at about -9 to -12 dB. The script measures in
     the 250-4000 Hz band, where grunting lives. Full-band, the explainer's set 2 false-alarmed on the music's bass.
2. **Transcribe** with local Whisper `small` (segment timestamps are enough) — this
   maps every script beat to a timecode for the doc.
3. **Look at every second.** Extract frames at 1/2s, montage into labeled contact
   sheets (~60 frames per sheet), and READ them: catalog every insert, graphic,
   stock clip, label, and typo with its timecode. Zoom into anything suspicious.
   Then two passes the contact sheet cannot do (calibration rules 1, 2, 4): crop every
   text panel at full resolution and transcribe it word for word against the script;
   and for every insert/overlay, extract the frame after its line ends and confirm it
   has left the screen. Note the vertical placement of text inside each panel.
   Then **measure the framing** (calibration rule 31). The contact sheet shows it, and a reviewer still missed it:

       python3 .claude/skills/revisions/reference/framing.py CUT.mp4 --sheet framing_sheet.jpg

   Per shot it reports the empty frame above and beside Dan and how far the shot could be cropped in without
   cutting him off. LOOSE = an upright shot with more than 8% of the frame above his head, or with his knees in
   frame (the banned full-body wide), or a movement shot that could be cropped in 15% or more. Write Dan's item with
   the number ("Crop in closer by about 30%") plus the framing STANDING RULE, and LOOK at the proof sheet (a pose
   miss is reported as NO SUBJECT, never passed). Zeeshan's follow-along: 10 of 13 camera shots LOOSE (every wide
   could crop in 24-35%, every talking shot had his knees in frame); the tight punch-ins on the rollouts were
   already full width and read OK, which is right, because cropping them further would cut the rep off.
4. **Compare against the target style** (currently Muhammad A's reference edit:
   pause-free pacing, music bed ~−20 dB under voice, whoosh/pop SFX on every graphic,
   animated bullet builds / lower-third chips / title cards, phrase-synced punch-ins,
   highlight boxes on referenced photos, brighter grade, NO burned captions) — but
   re-skinned to OUR brand, never his pastel cyan.
   **Judge the music's genre, not only its level** (calibration rule 33). For a workout or live-set video the bed
   must be upbeat and high energy: electronic, hip-hop or rock. Chill, lofi, trip-hop, ambient, corporate or
   "elevator" music is an item at any level. The reviewer cannot hear it under the camera sound, so ask the editor
   for the track name (the brief asks for it with every delivery) and read its genre and mood tags. If the track is
   unknown or not clearly high energy, write Dan's "Change music to this music track" item with a replacement link
   found by the recipe in the asset library, plus the workout-music STANDING RULE. Dan's rule: when in doubt, put it in.
5. **Check every standing rule** (below). Each violation becomes an item; new
   classes of violation also get a "hard rule for future videos" line.
6. **Choose replacement assets from what already exists** before directing anything
   new (see asset library). Only direct new AI generation when nothing fits.
7. **Self-check the draft against the calibration section above — the doc goes to the
   editor as written, Dan does not re-review.** For every item confirm: it fixes something
   wrong (not an upgrade of something acceptable); the asset matches the literal words under
   it; it creates no before→after adjacency; a directed clip says "stock footage or AI clip";
   casting is aimed at the aspirational figure, antagonists at the caricature; any body
   judgement was verified at full resolution; no header wording is itemised on taste; every
   insert has an exit; every text panel was transcribed. Then walk the timeline once more
   for the two things Dan added on top of ours: lingering graphics and before→after cuts.
   Then the pass-2 checks (rules 12–21): every added text chip states a benefit, about two per ad, none
   restating the line, none a list of negatives or a question; no bullet build or device copied from another
   ad in the batch; no app screen used as a gap fill; no item cross-references another and no item count in
   the prose; the hero asset matches the script's literal claim; American spelling throughout.
   Then the pass-3 checks (rules 22–30): on a round ≥ 2, audio is an item only for level outside −14 ±1, peaks at 0
   with clipping, or the wrong mic/room — otherwise the audio block is deleted, and an ad with nothing else left gets
   the APPROVED line instead of a section; no end-hold item unless the button leaves before the last word; every
   rule violation carries its bold STANDING RULE sub-bullet in the canonical wording; the key change in every item is
   bolded; app/phone demo items are the one-line block + recording link; every phone/app before picture was
   identity-checked against Dan; after-photo beats say "two, images below" with empty slots and no picks.
   Then the pass-4 checks (rules 31-34) on any cut with a talking head or live sets: `framing.py` ran and every
   LOOSE shot is an item with its crop-in number; `sets_level.py` ran on a workout and a LOUD or BURIED verdict is an
   item; the music's genre was checked and a workout bed is upbeat and high energy; no credit sentence contradicts
   an item.
8. **Write the Google Doc** via the Google Drive MCP `create_file` with
   `contentMimeType: text/markdown` — it converts cleanly to a Doc, including links.
   Keep Dan's `\*\*…\*\*` literal-asterisk look for THROUGHOUT headers. Save the
   markdown copy in `revision docs/`.
9. **Report to Dan** with the Doc link, the top findings, and anything that needs his
   call. He forwards it.

## Standing rules to check every review (Dan's accumulated rulings)

- **Audio**: the `_shared/audio` gate rows above — lav only (per `pick_lav`, never "right channel"
  on an 8/28 roll), no comb, room ≤ 80 ms, −14 LUFS, true peak ≤ −1.0 dBTP.
- **Compliance (Google Ads)**: NO before and after in one frame, ever — side-by-sides,
  two-panels with an arrow, the app's "Meet the new you" reveal; NO before-imagery cut
  straight into after-imagery (camera scene between them, calibration rule 3); NO
  morph/transformation-in-one-shot; NO body-shaming — belly-fat grabs, pinches, zooms;
  NO email-capture form on screen.
- **Disclosure**: "*AI Generated" on every AI visual, full duration; upper-left and
  ~50% larger on full-frame AI clips; centered small tag on panel inserts.
- **Brand graphics**: black bg (or #162118 dark green field), headers large dark
  green ALL CAPS (#8C9858 olive reads on black), body off-white #E9EEDE, red #E22222
  only as attention accent, Manrope, Title Capitalization. Look = YouTube Shorts
  covers / `ad-edit/reference/motionlib.py` GREEN palette.
- **Casting**: the man the viewer is meant to be is white or Asian, 30–50,
  shredded-not-bulky, no unmanly outfits. Antagonists (influencer bro, fat trainer) are
  cast as the caricature the script mocks; neutral prop shots are not swap items
  (calibration rule 6). New clips are always "stock footage or AI clip" (rule 5).
- **Product truth**: real app screens and the real generation flow only — never
  invented dashboards or generic AI-app mockups. End cards / demo flows end on the
  after picture ALONE.
- **Presentation**: no raw black pillarboxing of 9:16 assets (brand card or blurred
  fill); alternating ~50%/~70% punch-ins on talking heads; no dead air > 0.3s; every
  insert and overlay leaves when its line ends (rule 2); text centred in its panel
  (rule 4, finished panels only); the end is an item ONLY if the button or picture cuts off before the last
  word ends (rule 23) — never for a short hold.
- **Framing** (Dan, 2026-09-08 and 2026-09-11): hair-anchored and tight, with a small margin above his hair and at
  the sides; never the full-body wide on a talking shot; movement shots hold the whole rep tightly. Measured by
  `reference/framing.py` (step 3).
- **Workout audio** (2026-09-11): during live sets the mic comes down (Dan: "by 80%", about −14 dB), so the effort
  sounds stay audible but sit 5-14 dB under the talking; back to full level when he talks. Measured by
  `reference/sets_level.py` (step 1).
- **Workout music** (2026-09-11): upbeat and high energy, electronic / hip-hop / rock, never chill or elevator-like;
  Pixabay only, never a track whose page says "Content ID Registered".
- **Canonical STANDING RULE wordings (Dan's own, 2026-09-10 — paste verbatim, bold, as the last sub-bullet of
  every item that violates one, in every ad it applies to):**
  - `STANDING RULE: do not show before and after images on screen at the same time, or immediately before and after each other. Always break them up with camera scene footage or something else to avoid having the ad suspended for violating Google Ads policies.`
  - `STANDING RULE: Always show the AI generated goal image in clips where I am talking about generation functionality. Always label goal image at the end AI generated`
  - `STANDING RULE: Do not put AI generated label on real photos, only AI generated photos. All pictures from pool photo shoot used as after photos are real photos. Pool picture of me that is used as AI generated example is the only pool photo that is AI generated, the rest are real.`
  - `STANDING RULE (Dan, 2026-09-11): Every real after picture of me carries the label "Real picture of me — not AI-generated" (viewers were taking them for AI). AI pictures keep AI-GENERATED. One label or the other on every picture of my physique, never over my face.`
  - `STANDING RULE: Make all AI generated clips of someone who is supposed to look like the successful prospect someone who looks like this. White or Asian man with abs, 30-50. Not fat, not bodybuilder muscular.`
  - `STANDING RULE: Use a guy who looks like this to illustrate "before" unsuccessful prospect. White or Asian male 30-50 in American average shape, with small belly`
  - `STANDING RULE: Do not use logos of other companies in our ads. Names of other companies are OK`
  - Audio (write it the same way each time, round 1 or when the level/peaks are wrong): `STANDING RULE: Every finished mix reads -14 LUFS integrated with a limiter on the finished mix at -1 dBTP true peak, nothing at 0, one mic, no heavy noise reduction on a dry recording.`
  - Workout sets (Dan, 2026-09-11): `STANDING RULE: Keep audio during workout sets, but if grunting is extremely loud and blowing out mic reduce volume significantly to avoid this becoming annoying to the viewer.`
  - Workout music (Dan, 2026-09-11): `STANDING RULE: Use upbeat, high energy music for workouts. Consider electronic, hip-hop, and rock. Avoid any music that is chill, relaxing, or which sounds like elevator music`
  - Framing (built from Dan's own 09-11 item wording): `STANDING RULE: Crop in closer. In the wide shot, avoid excessive space above my head and towards the sides. In the tight shot, leave only a small amount of space above me and to the sides, almost as tight as possible without me going out of frame.`
- **Voice input caveat**: Dan dictates; if a quoted correction seems odd, check the
  transcript audio before flagging his script wording as a "typo".

## Asset library (already uploaded to Dan's Drive — link these, don't re-upload)

- Folder **"00 ASSETS USED IN THE REFERENCE AD"** (`10veL4yDYVaaDh1q_2VKJObfa-YpGEW_A`):
  01 hook/endcard pool after-image, 02 before-picture 200lb, 03 heavier-Dan couch AI
  clip, 04–07 photo-shoot stills, 08 crude-photoshop gag clip, 09 REAL
  app-generate-future-self screen recording (use ~0:03–0:26; cut before its
  side-by-side ending), 10–12 REAL app screens (assessment / Monday workout / meal plan).
- Folder **"AI clips for Muhammad"** (`1bO1mZAk0ii9c-m45-YhSYmuYq_qPIpvm`): the four
  Veo benefit/dad clips — attractive-to-women (pool), men-respect-you (gym),
  feel-better (beach run), busy-dad (kitchen) — plus two real fat-dad photos.
- Local-only extras (Seagate `/Volumes/Extreme/_edit_work/ad1-8-14/assets_v1/`):
  `stats_scan.mp4` (scan+stats animation), `p_phone_mock.jpg` (lock-screen mockup).
  For human editors, direct them to REBUILD these natively in brand colors (better
  than compositing our render); only offer the files if Dan wants.
- List a Drive folder's contents with the Drive MCP:
  `search_files` query `parentId = '<folderId>'`.
- **Music for a workout video: the replacement recipe (2026-09-11).** Pixabay only (licence settled: commercial,
  no attribution). Most popular workout tracks there are Content ID registered, so check every candidate: the
  search listing shows a small shield beside the duration of a registered track, and its page says "Content ID
  Registered" (WebFetch reads it; no such text = not registered). Accept genre electronic / hip-hop / rock with mood
  energetic; reject "Laid Back", "Smooth", lofi, trip-hop, corporate and ambient. Instrumental, and as long as the
  video or loopable. Current pick: "Energy Gym Thunder" (knox-gym, rock, 3:32, AI-generated, not registered),
  <https://pixabay.com/music/rock-energy-gym-thunder-538872/>. Dan listens before it goes out. NOT for workouts: our
  cleared bed `Media/music beds/rhythmical-melodic-syncopation-triphop-130bpm-pixabay-10091.mp3` (trip-hop; a
  talking-content bed).

## Lessons

1. **Google Drive web upload cannot be automated from the Chrome extension.** The
   file input is created transiently and clicked natively; synthetic DragEvent drops
   are ignored (Drive reads `webkitGetAsEntry`, null for scripted DataTransfer), and
   a prototype-click hook did not catch it. Check whether the asset already exists in
   Drive FIRST (it usually does — earlier sessions uploaded the ad1 set); for genuinely
   new small files use Drive MCP `create_file` with base64; for big files ask Dan to
   drag-drop, or convert the item into a "rebuild it natively" direction.
2. **The delivered export can hide the audio defect**: if L/R are identical the editor
   already summed the mics — cross-channel analysis alone says "fine"; only the
   autocorrelation echo peak reveals it. Always run both (echo_check.py does).
3. **Drive UI menus mis-click** (items shift between opens). Keyboard shortcuts are
   reliable: in Drive, `ctrl+c` then `f` = new folder. Screenshot fresh before any
   menu click.
4. Muhammad-reference measured targets, for pacing/music checks: zero gaps ≥ 0.25s,
   music ~−20 dB under voice (floor p5 ≈ −40 dB), luma median ~67, no burned captions.
5. **A new cut of a video you already reviewed is usually a DIFFERENT editor, not round 2.** Dan runs
   tryouts where several editors cut the same script. On 2026-08-25 a cut of Video 1 was reviewed as
   "round 2" for the previous editor; it was Waleed's FIRST cut and had to be rewritten from scratch.
   Confirm the editor's name and round before writing a word — the framing changes every section,
   and "you didn't do what I asked" aimed at someone who never got the notes is the worst possible
   first contact. Open a first-round doc by crediting what already works ("keep this"), then the fixes.
6. **The two-mic source fault produces DIFFERENT symptoms per editor — test for both.** Editor A's
   Video 1 cut had L and R *identical* (they summed the mics before export). Waleed's cut of the same
   script shipped the **raw two-mic stereo pair** instead — L/R correlation **−0.72 at −7.8 ms**,
   polarity inverted, mono fold-down losing ~4 dB of voice. `echo_check.py` catches the first and
   reads the second as merely "channels differ". The decisive test is a **best-fit delay+gain
   alignment residual** (< −12 dB ⇒ one mic; ≈ −3 dB ⇒ two genuinely different mics) plus a **mono
   fold-down penalty** in the 300–3400 Hz voice band. Both are in `chan_align.py`; run it on every
   cut from every editor. Until an editor is told, they cannot know — write it as source-rig
   background, not as a complaint.
7. **Always measure integrated loudness and true peak, every round.** This cut shipped at
   **−8.04 LUFS / +2.53 dBTP with 166k clipped samples in L**. Nothing in the picture review would
   have surfaced it, and it is the kind of defect that survives to upload.
8. **Do not infer "music bed" from the noise floor alone.** A hard-limited over-loud master pushes
   the inter-word floor to ≈ −31 dB, which trips the "floor above −45 dB ⇒ music" heuristic with no
   music present. Confirm with per-band gap spectra on the LAV channel (a real bed at −20 dB under
   voice reads ≈ −30 dB in 80–500 Hz; this cut read −56 to −61 dB) and check the floor's *variance* —
   a bed is constant, room noise is not.
9. **Check that the right asset is on the right line, not just that an asset is present.** The
   single worst finding this round was the **crude-photoshop gag image used as the hook** at 0:00
   ("this picture got me abs") and again at 2:37 ("the picture that motivated me") — correct only at
   1:04, the photoshop line. Read the transcript against each insert; a technically-clean insert on
   the wrong sentence is worse than a missing one.
10. **Verify who is on screen before writing about it.** Dan is Asian; a reviewer working from
    stills can wrongly conclude a cut features a different presenter. Cross-check against
    `Short-form video content/instagram-danrosefit/profile-photo_danrosefit_1080.jpg` before
    claiming casting problems.
11. **Drive MCP `update_file` is metadata-only** — it cannot rewrite a Doc's body. To fix a
    conversion glitch, `create_file` again and `trash_file` the first. Also: a literal `*` inside a
    `**bold**` run (e.g. `**… "*AI Generated" …**`) breaks the markdown→Docs conversion; escape it
    as `\*` or reword.
12. **Read the Upwork/message thread BEFORE writing a round-2 doc.** On 2026-08-30 Waleed delivered
    a "final video" whose picture was byte-for-byte his first cut. The thread settled the framing:
    Dan *had* sent the round-1 doc and Waleed *had* acknowledged it — but every message in both
    directions for the five days after was about audio only. So the doc leads with "our conversation
    narrowed to audio" instead of "you ignored my notes". Same facts, opposite outcome for whether
    the editor stays. Establish (a) was the doc actually sent, (b) what has been discussed since,
    (c) what the editor believes the remaining scope is.
13. **Frame-diff the new cut against the previous delivery — it is the decisive measurement for
    "were the revisions applied".** `ffmpeg -i old -i new -filter_complex
    "[0:v]scale=320:180,format=gray[a];[1:v]scale=320:180,format=gray[b];[a][b]blend=all_mode=difference,
    signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=diff.txt"`. Waleed's read **0.144
    mean / 0.547 max luma levels across all 8,012 frames, zero above 2.0** — pure re-encode noise.
    Identical frame count and identical duration to the microsecond corroborate it. This turns
    "you didn't do the revisions" from an accusation into a number, which is both fairer and harder
    to argue with. It also means **every timecode in the previous doc is still exactly valid** — say
    so, it makes the re-do feel far smaller to the editor.
14. **`_edit_work/<job>/C1591.wav` is a 16 kHz MONO Whisper input, not the camera audio.** Panning
    `c0=c1` off it returns silence and every spectral comparison reads exactly zero correlation. The
    real two-channel 48 kHz audio is in the camera `.MP4`. `ffprobe` the channel count before
    trusting any raw-file comparison.
15. **Music can only ADD energy, never subtract — so a measured HF deficit against the raw file is
    always real attenuation, whatever the bed is doing.** Useful because the bed contaminates the
    band ratios: on this cut it sat only 7.7 dB below the mix at 3.5–6k and 4.8 dB at 6–9k, so the
    measured −2.6 dB HF cut understated a true voice cut nearer −3.5 dB. Quote the conservative
    number; it cannot be argued down. Measure the bed's per-band contribution (speech-frame vs
    gap-frame band energy) before attributing any boost to EQ — a low-end lift *can* be the bed.
16. **When an editor draws a scope line, concede the subjective half and keep the objective half.**
    Waleed's covering note declared further audio work to be "specialist audio-post… spectral
    matching, multiband processing, professional mastering". Contesting that invites a walk-off.
    The doc instead reframed the three remaining audio items as what they measurably are — a limiter
    ceiling, a fader move, and one tonal note explicitly marked "your call" — and let the clipping
    stand on its own (**6,333 samples pinned at full scale, up from 2,426**), because a sample at
    0 dBFS is not a matter of taste. Give the editor a way to comply without retracting anything.
17. **`whisper` shells out to `ffmpeg` by name.** Without the static build on `PATH` the transcribe
    call fails and writes an EMPTY transcript rather than erroring visibly. Check the output has
    lines before using it. **scipy is not installed on this Mac** — write the alignment and band
    analysis with numpy only (`np.correlate` plus cumulative-sum sliding normalisation works fine).
18. **Retention is part of the deliverable when Dan says so.** Alongside the doc, write the
    paste-ready messages: one to send, one for a scope pushback, one nudge. The thing that makes a
    fixed-price freelancer quit is believing the revision loop is unbounded — state explicitly that
    nothing in the doc is new, that the list ends the job, and that there is more paid work behind
    it. Advise Dan **not to release a funded milestone** before the outstanding work lands; it is
    the only structural leverage left.
19. **When the editor's OWN earlier cuts already have the right sound, measure those and make them the
    target.** Muhammad's Ad 3 (2026-09-01) shipped the raw two-mic pair (L/R −0.72 at −7.85 ms,
    inverted) while his Ad 1 and Ad 2 measured as one mic (residual −18 to −26 dB). "Do exactly what you
    did on Ad 1 and Ad 2" lands better than any explanation, and it is provably achievable by him.
    Compare speech-band spectra too: the bare right channel is ~6 dB duller above 2.5 kHz than his
    Ad 1 mix, so say "add the same top-end back" or the single-mic fix will sound worse to him.
20. **"Add it to this doc" = append a new H2 section in the SAME bullet format, via the osascript HTML
    clipboard + cmd+v at the end of the doc (click the last line, End, Return x3 to leave the list).
    Set the clipboard IMMEDIATELY before the paste** — a concurrent session overwrote it between set
    and paste and a stray file path landed in Dan's doc; cmd+z, re-set, paste again, then verify by
    Drive read-back. Check the pasted section AND that the previous section is byte-unchanged.
21. **Asset folder for the trainer-ad AI clips is `1ZO4wukehoHAwnRRyDyFKm4hFtXMYF2Ex`** (8 s hook
    cutdown `1Io6XQlkym21ufR2aUZz_dc_j0tU_2VMC`, 35 s story `1mW5nEDjDbPCJUJGtjHUCrGqRVsX-Lhie`); the
    real app screens (trainer assessment `1wFsyT9eKeUVzDcF0L7bbAPn5DSAVdRIs`, workout day
    `11AS0LYjs-LfUPuhhVqGdAtiN1sjkJ02j`) are in the reference-ad folder, and the installed exercise
    demos are public at `https://absbyai.com/exercise-demos/<id>.mp4` — link them, never re-upload.
    The trainer-assessment screen shows the GOAL image alone, so it is the clean replacement whenever
    an editor puts the app's "Meet the new you" side-by-side on screen (three editors have now).

22. **Every revision doc is written as Dan, first person, and never says Claude wrote any of it (Dan,
    2026-09-02).** No "Claude's additions", no "reviewed by Claude", no split between his items and ours.
    When Dan has already typed a few items into the doc, absorb them into the full list in the same voice
    and format — rewrite his bullets in the doc's style rather than leaving them as a separate block — so
    a reader cannot tell which items he typed and which were measured. The editor is to believe Dan did
    every revision personally. Same rule for the markdown copy and the section headers.

23. **Round 2 of Muhammad's Ad 3 (2026-09-02) — three measurements that decided the doc.** (a) *Which mic
    did the editor use?* Cross-correlate the new cut's mono against EACH channel of the previous delivery
    with an FFT over a ±2 s lag window — his V2 matched V1-RIGHT at +0.89 to +0.91 and V1-LEFT at −0.7,
    at a constant +13.7 ms (a re-conform offset; under a frame, not a sync fault). A ±12.5 ms sample-loop
    search returned ~0.2 and would have said "unknown source". (b) *Same duration to the microsecond does
    NOT mean the picture is unchanged* — he replaced inserts in place; the frame-diff was 27 mean with the
    only quiet stretches being the two "keep" clips. Read the diff as a map of what changed, not just a
    changed/unchanged verdict. (c) His masters sit at −18 LUFS (Ad 1 −18.2, Ad 2 −19.1, V2 −18.4), so the
    gate's loudness row fails on every cut of his; the doc asked for −14 with a limiter rather than
    "match Ad 1" again. His review copies are 854×480 (Ad 2's was too); the 1080p comes with the final,
    so ask for it, don't flag it as a defect.
24. **Google Docs paste inherits the cursor line's character style.** The round-2 section landed entirely
    bold because the last empty paragraph carried bold from the previous section (the B button was lit).
    Look at the toolbar before cmd+v; if B is active press cmd+b first. cmd+z removes the whole paste
    cleanly. Also: `cmd+End` does nothing in Docs on a Mac — `cmd+ArrowDown` goes to the end.

25. **Getting a NEW small clip to the editor when the Drive uploader cannot be driven (2026-09-02).** Base64
    through the Drive MCP is a token trap (a 1.8 MB clip is ~2.5 M characters in one tool call — never do
    it), and Drive's web uploader still exposes no file input to `file_upload`. The route that works:
    drop the muted clip in `public/ad-assets/` (gitignore exception `!public/ad-assets/*.mp4`, keep each
    under ~3 MB), commit, push, wait for the Railway deploy, and link
    `https://absbyai.com/ad-assets/<name>.mp4` in the doc — the exercise demos already ship this way.
    Only Dan's own footage that is going into a public ad anyway; the repo is public.
26. **Dan's real supplement stack is on camera for the whole 03 supplements longform**
    (`claude edited long form content/03 - …/CUT_v1_graded_NO-GRAPHICS.mp4`, no lower thirds). A bottom-band
    crop panned across the counter (`crop=1280:720:x='(in_w-1280)*t/5.5':y=340` → 1080p) makes clean
    product B-roll with his face out of frame; the pan is at `Media/ad-assets/batch1-ads/clips/`.
27. **In Google Docs, `cmd+End` did nothing through the extension; `cmd+ArrowDown` jumps to the end of the
    document.** The last line of a Muhammad doc has been a plain paragraph, so no Return x3 was needed —
    screenshot first and read the toolbar's list button before pressing Return.
28. **A script can hand the editor ONE app clip for a whole section, and he will lay it under the first
    line of that section.** Ad 4's supplement-audit scroll ran under "upload a picture… generate a future
    self", not under "take a photo of your supplements" seven seconds later. Walk every app screen against
    the exact sentence it plays under, the same as lesson 9 for images.
29. **Whisper is a Python module here, not a command: `python3 -m whisper CUT.mp4 --model small --language en
    --output_format json`** with `Media/video_edit/bin` on PATH. A bare `whisper` call fails silently inside a
    backgrounded shell (lesson 17's empty transcript, again). Also: in zsh, `echo ==== X` errors ("= not found")
    because a leading `=` is filename expansion — quote separators. Both cost a rerun on Ad 5 (2026-09-03).
30. **Peaks at 0 dBTP on a −19 LUFS master can be the VOICE, not the SFX.** Ad 5 measured −18.9 LUFS with 58
    separate seconds touching 0 and 1,800 clipped samples; per-second peak scan (numpy on the mono decode)
    showed plain talking-head seconds (1:36, 1:40, 1:52, no whoosh) at +2.4 dB. Ad 4's whoosh-only finding does
    not generalise — always run the per-second scan and name the quiet seconds in the doc, so the editor puts
    a limiter on the mix rather than just turning the SFX down.
31. **The SCRIPT can contradict a standing rule — the rule wins, and say so in the doc.** Ad 5's script cue
    for the closing app clip reads "the app's own before/after reveal screen — in-product footage is the one
    place a before/after pair is safe". It is not (Dan's rulings on Ads 2, 3 and 4). The doc told Muhammad to
    ignore the note; the scripts doc itself still needs correcting. Read every bracketed cue against the
    rules list before assuming the editor got it wrong.
32. **Two new layouts that are still a before/after in one frame:** a two-panel with an ARROW between heavier
    Dan and ripped Dan (Ad 5, 1:27 — the editor split a single AI clip into panels), and any belly-grab /
    pinch stock close-up (Ad 5, 1:11 — body-shaming under Google's weight-loss policy). Both are now in the
    standing rules. The fix for the arrow panel is to play the clip full frame in one panel, not to drop it.
33. **Appending to Muhammad's batch doc: `reference/md_to_docs_clipboard.py <md>` builds the nested-list HTML
    and sets the clipboard in one step** (the `markdown` package is not installed; a hand-rolled converter
    mangled Dan's `\*\*` headers twice before the tree version). Then in Docs: click in the body,
    `cmd+ArrowDown`, check B is off, `cmd+v`, and verify with a Drive `read_file_content` read-back that the
    new H2 is there and the previous sections are unchanged. Pasted H2s land black while Dan's are blue —
    cosmetic, he has not objected.
34. **2026-09-03 calibration pass.** Dan asked for the skill to learn from his edits so he can stop
    re-reviewing. Method that worked: keep the markdown copy byte-exact at delivery, read the Doc back
    with Drive `read_file_content` after he has edited it, and diff section by section — every
    addition is a missed defect, every rewrite a mis-calibrated direction, every deletion an item that
    should not exist. The findings are the calibration section at the top; repeat the diff after every
    doc he touches and fold new rules in there, not here. ⚠ Two adjacent Ad 4 items (2:06 pill-bottle
    swap, 2:16 couch clip) vanished together while the THROUGHOUT still says the 2:06 clip "needs to be
    swapped (see below)" — flagged to Dan as a possible block deletion.

35. **Batch sweep of 8 editor cuts in one session (2026-09-08) — the recipe that worked.** Downloads by `gdown` into
    `/Volumes/Extreme/_edit_work/revisions-<date>/dl/`, then ONE prep script per cut (`prep.sh`: ffprobe, `pick_lav
    --analyse`, `audio_gate --no-stamp --ab`, per-second peak scan, silencedetect, scene count, mean luma, 2 fps frames →
    labelled 10×6 contact sheets, Whisper small) run through `xargs -P 2` (the two-build cap), and one reviewer subagent per
    cut launched the moment its prep finishes, all reading a shared `BRIEF.md` that points at the skill and the work dir (start from `reference/BRIEF_template.md`, which carries the pass-3 rules).
    Each subagent writes `out/<name>.md` (the section, in the `md_to_docs_clipboard.py` dialect) and `out/<name>.summary.md`
    (scorecard + paste-ready Upwork message). Muhammad's six sections were concatenated and pasted in ONE cmd+v at the end
    of his doc; read-back showed the old text byte-intact and all six headings. Traps: the editors' earlier review copies
    are NOT re-downloadable with gdown ("can't retrieve" = permission) — compare V2→V3 item by item instead; a previous
    delivery you only need audio numbers from should be gate-only (skip whisper/frames); Whisper throughput collapsed from
    150 to 8 frames/s when the Mac was swapping (load 60, 4.7 GB swap from other sessions) — nothing to fix, just expect
    the last two cuts to take as long as the first six; Docs would not render in the extension until the load fell.
36. **Insert a round at the TOP of a doc (Zeeshan's convention):** click at the start of the first heading, `cmd+Left`,
    `Return`, `Up`, `cmd+alt+0` (Normal text, so the paste does not inherit Heading 1), confirm B is off, set the clipboard,
    `cmd+v`. The pasted H2 lands bold; the old first heading is untouched.
37. **Dan asked for the review sweep with "do not message him yet" — the deliverable is the docs plus the messages in chat.**
    Confirm sent-status from the Upwork room text (`get_page_text` on the room URL with `companyReference=…&sidebar=true`;
    a bare room URL redirected to the most recent room), not from Gmail — Upwork's notification emails only carry the
    editor's side and are 90 KB of tracking links each.
38. **Editors "fix" clipping by turning the mix down (Ad 5 V2 landed at −29.7 LUFS) and "fix" an email screen by deleting
    the whole after-picture screen (Ad 3 V3).** When the previous round asked for two things on one element, check that the
    fix for one did not remove the other; write the fix as an ordered recipe (limiter first, then lift; hold the screen at
    the top, do not scroll) so the next attempt cannot go the wrong way again.
39. **Batch 3 (2026-09-09, eight Muhammad cuts) — three things to check before reviewing anything.** (a) **md5 every
    re-delivered link against the previous download.** His "AD 02 v2" link was the Ad 4 v2 file byte for byte and his "AD 08"
    link was the unchanged 09-07 file — Drive `get_file_metadata` (title + modifiedTime) plus an md5 against the 0908 `dl/`
    copy settled both in a minute; reviewing either as a new cut would have produced a doc for a video that does not exist.
    (b) **Once the level lands, the next failure is over-done noise reduction.** Six of eight cuts failed the gate's
    `artifacts` row (flux ×1.17–1.29 of Ad 1, HF swirl ×1.15–1.31) on rooms already at 32–40 ms; write it as "watery /
    underwater top end, back it off, gaps only, no de-reverb", never as a number the editor cannot meter. (c) **Check the
    doc's own links before blaming the editor.** Dan's Ad 7 item linked the plain before picture under the "bad Photoshop"
    slot, so Muhammad put the before picture there; the round-2 doc owns the link in Dan's voice ("the link I gave you was
    wrong, which is on me"). Also: the SFX can bypass a limiter placed on the voice track (Ad 3 v4: voice capped at −2.6 dB,
    whoosh at +0.02) — say "limiter on the finished mix, the last thing before export". Recipe as in lesson 35; a full batch of
    eight took 25 min of prep (two at a time, load 8–28) and one subagent per cut at ~220–310k tokens each.

40. **Batch 4 (2026-09-10, seven Muhammad cuts) — the app recording is a STRANGER, and a "final HD" gets a gate + frame-diff, not
    a review.** (a) The only real app screen recording in the asset library — `example generation video.MP4`
    (`1fwRGtoHh4oTlwfQZ0gItY3Oj7DZPkN6P`, the link Dan pasted into his Ad 8 / 10 items) is byte-identical (62,300,869 bytes) to
    `09_CLIP_app-generate-future-self.mp4` in the reference-ad folder, and the photo it uploads is a heavier, older man who is
    NOT Dan (checked side by side against `02_BEFORE-PICTURE_dan-200lb.png` and his profile photo). So every phone demo in the
    batch carries a stranger as the before picture, and there is no "recording of my own upload" to link — a reviewer that
    writes "use this recording of my own upload instead" is wrong (Ad 15's first draft did). The correct item is Dan's own Ad 14
    form: "the before picture inside the phone is not me" + **Use this photo for the before picture in the clip** + the
    `02_BEFORE-PICTURE` link + the goal-image STANDING RULE. Three subagents independently called the man a stranger, which is
    what lesson 10 warns against — so the check that settled it was a four-panel strip (real before, the recording's upload
    frame, `ai_warning_heavier.png`, profile photo) read once. (b) A delivered "V3 HD" of an APPROVED cut is not a review: run
    the gate and `framediff.sh` against the approved review copy. Ad 5's read frame-identical (mean diff 0.53, max 1.27 — pure
    re-encode noise), 1080p at 10 Mbps, −14.0 LUFS at exactly −1.0 dBTP, every gate row PASS except the un-measurable
    `do_no_harm` (needs our own untreated baseline; declare it, don't hide it). Nothing goes in the doc; it goes in Dan's
    message and the delivery filing. (c) Muhammad delivers from two Drive accounts (`wadeededitteam@` and
    `sharkimageryproduction@` — Ad 8 v1, Ad 8 v2 and Ad 15 came from the second); an unfamiliar owner is not a different editor.
    (d) Once his level lands, rounds 2+ are picture-only and go fast: six reviewers at 210–250k tokens each, 4–8 minutes
    apiece, and two of six came back as the APPROVED form with zero items. The doc paste (six sections, 25 KB HTML, 72 bullets)
    verified as an exact-prefix read-back in one go.

41. **A workout-only cut (Zeeshan, content batch video 1, 2026-09-11) — three checks the standard pass misses.** (a) The gate's
    20 s + 120 s window lands inside the live sets, so its tone / floor / artifacts rows grade music and wheel noise, not the
    voice — do not quote them. Prove the brief's "keep the camera sound under the sets" item instead by cross-correlating the
    cut against the raw clip (FFT over ±4 s, least-squares gain): the track under all three sets read +0.2 to +1.0 dB of the
    raw lav at correlation 0.8–0.98, the same gain as his talking, so it is present and unprocessed. (b) Outdoor wide shots
    carry crew gear: a gold reflector swung across set 2 for 1.5 s (1:49.1–1:50.6) and read as a smudge on the 2 fps sheet —
    zoom any colour intrusion at a frame edge. (c) A close the editor stopped early often has a clean pickup after an
    interruption: C1633's plane pause (6:37–6:53, lav RMS rising −51 → −31 dB and falling) was followed by Dan re-saying the
    line and finishing the pitch. Run word-timestamped Whisper on the raw pickup and hand the editor the exact range. Also:
    Zeeshan names deliveries by his own running count ("Video 3.mp4" was batch video 1) and shared this one as a single file,
    not in his folders — identify the video by its content and his Upwork message, never by the file name.
