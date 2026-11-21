CONTENT (LFC). Task name: `First Time At The Gym Gemini LFC R1`.

# Gemini Argon editing test: I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time

**Project folder:** `/Users/danielrose/Projects/Claude/Projects/Abs By AI`. Run every command from there.

You are Gemini, joining a video operation that today runs on Claude and Codex. Dan Rose owns the business. He is not a coder, so write to him in plain language. Your job is to learn how we edit, including our green-screen editing, then edit this one long-form film from raw footage to Dan's review page, to our full standard. Dan is testing whether you can do this work as well as Claude and Codex.

The instructions in this repo were written for Claude and Codex, and they all apply to you. Wherever they say "Claude" or "Codex" as the editor, read "the editor", which is you.

## The most important fact about this film

**This film was not shot on a green screen.** Dan filmed it standing by a pool, in portrait, on four rolls. It is still edited as a long-form green-screen film. Dan's locked decisions for this kind of footage are:

- Do not put the upright picture in a boxed panel. Dan rejected that: "This looks weird with the boxed-in thing."
- Cut Dan out of the pool footage with an AI matte. Dan approved this: "Yes, this cutout works. I think we should edit the video this way."
- Treat the cut-out exactly like green-screen footage, on the locked long-form background template. The full-frame close-up "is a little bit too close", so use it rarely.
- Build a 1920x1080 long-form master. The source stays untouched and portrait.

A colour key does not work here because there is no screen behind him. You need to learn both skills: the green-screen standard, which sets the format and the quality bar, and the cut-out method, which produces the footage.

## This is a test edit of a finished video

This film is already approved and in setup, so the test works differently from a normal job in three ways:

1. **Blind on creative picks, open on method.** You get our methods and Dan's locked format above. Everything specific to this edit is yours to decide: takes, the opening, the cut, B-roll choices, background plan, graphics, colour and voice. Never open the earlier work listed under "Do not open". If you see any of it by accident, say so in your report.
2. **Isolated.** Nothing you make touches the real job, its queue row, its files or its schedule.
3. **Same bar.** Everything else is exactly the real process, including Dan's review rounds.

### Do not open

- `/Volumes/Expansion/_edit_work/RO-37/`
- `claude edited long form content/27 - I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time/`
- `Handoffs/video-editing/RO-37-i-m-41-here-s-what-i-d-do-if-i-walked-into-a-gym-for-the-first-t.md`
- `Handoffs/handoff-20261029-ro37-first-time-at-the-gym-r2.md`
- `Handoffs/handoff-20261031-ro37-first-time-gym-thumbnails-and-video-setup.md`
- Any review or thumbnail page for this film, including port 9872
- Anything in `Videos to Review/` whose name starts with `First Time At The Gym LFC`
- `.claude/skills/longform-edit/reference/ro37/`, except the method files listed in Step 1

The brief below replaces the job doc. The one film-specific file you do read is the source map named in it.

### Do not change

- Do not run `queue.py`, and do not touch `jobs.json`, `00-MASTER.md` or the Edit Queue page. The real job is finalized, and changing it would corrupt that record.
- Do not run `roll_sidecar.py mark-used`, and do not register anything in the clip library. A test should not mark footage as used.
- Do not edit `AI_COORDINATION.md`, `AGENTS.md`, `CLAUDE.md`, any skill, any gate or any threshold. If a rule or tool looks wrong, write it in your report.
- Do not commit or push. Do not upload, schedule, publish, make thumbnails or touch Blotato, YouTube or Google Drive.
- Do not send messages to anyone, and do not start or message other tasks.
- Do not run scripts inside another job's folder or inside `.claude/skills/`. Reference recipes are read-only: copy what you need into your own folder and adapt the paths.
- Raw footage is read-only. Do not move, rename or re-encode it in place.

### Money

- **Matting:** first try the free local route. `torch` and `transformers` are installed, so test BiRefNet locally on a short excerpt and compare it with the approved quality. Apple Vision also works, but its mask is softer.
- If local matting is too slow or too poor, use BiRefNet on Replicate (about $0.002 a frame). **Cap: $10 for Round 1, $25 for the whole test.** Load the key from `~/.absbyai-secrets.env` and never print it or write it to a file. Store mattes per source frame so no frame is paid for twice.
- A full film has about 14,000 frames, so full-film matting on Replicate would be about $28. Stop and ask Dan before you pass $25.
- State the estimate before each paid batch, and keep a running spend ledger including failed calls.
- **AI still frames:** only through `.claude/skills/_shared/codex-image.sh`, on the subscription. Never a paid image API.
- **AI motion:** only after Dan approves the frames, and only in Google Flow on the subscription. If you cannot drive Flow, say so. Do not use the paid video API.

## Step 0: prove you can do the work

Before anything else, check that you can actually:

- read and write files in the project folder
- read `/Volumes/Extreme` and `/Volumes/Expansion`
- run shell commands, including `Media/video_edit/bin/ffmpeg`, `python3` and `~/.npm-global/bin/hyperframes`
- look at rendered frames at full size and zoomed, and inspect audio without playing it through the speakers
- start a server on this Mac and load its page in a browser
- produce a real matte on one frame of `C1895.MP4`

Report what works in one short list. **If you cannot run commands, reach the footage or produce a matte, stop and tell Dan exactly what is missing.** Do not simulate any step, and do not describe work you did not do. A plan with no real files in it is a failed test, and an honest stop is not.

## Step 1: catch up on how we work

The repo's slash commands (`/longform-edit`) and auto-loaded files will not load for you. Read these directly, in full, in this order.

**Who we are and the standing rules**
1. `AGENTS.md`
2. `CLAUDE.md` (its `@` lines point at the files named here)
3. `AI_COORDINATION.md`, to see what else is running. Read only; do not edit.
4. `.claude/skills/_shared/VIDEO-RULES.md`. This is the main rulebook, and it is long. Newer sections sit at the top and win over older ones.
5. `Handoffs/video-editing/00-RULES.md`

**How we edit a long-form**
6. `.claude/skills/_shared/EDITOR-CARD.md`, which explains why good edits win
7. `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, the round method and review page
8. `.claude/skills/_shared/ASSET-APPROVAL.md`
9. `.claude/skills/_shared/CUT-CONTINUITY-QC.md`
10. `.claude/skills/_shared/HOOKS.md`
11. `.claude/skills/longform-edit/SKILL.md`, in full, including "Landscape presenter films" at the end
12. `.claude/skills/longform-edit/reference/HOUSE_STYLE.md`
13. `.claude/skills/longform-edit/reference/README.md`

**Green-screen editing: the format and the quality bar**
14. `.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md`, the locked way to build this kind of film. A new film changes facts, script, photos and clip windows, not the build.
15. `.claude/skills/_shared/greenscreen-bg/README.md`, the locked background types, placements and planner rules
16. `.claude/skills/_shared/chroma-key/README.md`, the house key, its measured bar, the frame-lag trap and the cut-out section
17. `.claude/skills/longform-edit/reference/ro24/README.md`, then its `round3/README.md`, `round4/README.md` and `round5/README.md`
18. `.claude/skills/shorts/reference/ds40-greenscreen/README.md`, how the house key was built
19. `.claude/skills/shorts/reference/ds40-codex-r5-reaction-format/README.md`. This is the locked format for reaction Shorts. Learn it, but it does not apply to this film.

**The cut-out method.** In `.claude/skills/longform-edit/reference/ro37/`, open only these files. They are methods, not edit decisions. A few notes name clips or numbers from that edit, so you must still search for and judge everything yourself.
20. `README.md`, `round2/README.md`, `round3/README.md`
21. `cutout_test.py`, `round2/matte.py`, `round3/refine.py`, `round3/gapfix.py`, `round3/audit_key.py`, `round3/audit_sheets.py`, `round3/hands3.py`, `round3/sidehits.py`

In that folder, do not open anything else: no `edl.py`, `plan.py`, `resolve.py`, `round2/plan_bg.py`, anything in `round4/`, or any `page*.py`.

**Look, graphics and AI**
22. `.claude/skills/_shared/SOFTBLUE.md`
23. `.claude/skills/_shared/GRAPHICS-STANDARDS.md`
24. `.claude/skills/_shared/hyperframes/README.md`
25. `.claude/skills/_shared/IMAGE-GENERATION.md`
26. `.claude/skills/_shared/framecheck/README.md`
27. `.claude/skills/_shared/veo/README.md`
28. `.claude/agents/frame-reviewer.md`

**Tools**
29. `.claude/skills/_shared/rolls/README.md`
30. `.claude/skills/_shared/cut/README.md`
31. `.claude/skills/_shared/audio/README.md`
32. `.claude/skills/_shared/cliplib/README.md`
33. `.claude/skills/_shared/renderq/README.md`
34. `.claude/skills/_shared/editcap/README.md`
35. `.claude/skills/_shared/deliver/README.md`
36. `.claude/skills/_shared/edit-sheet/README.md`
37. `.claude/agents/ra-reviewer.md`, how an independent review is done
38. `Handoffs/handoff-20260914-ad3-square-codex.md`, section 2, for traps on this Mac (paths with spaces, the project ffmpeg, and similar)

**Memory.** `Docs/memory/MEMORY.md` is the index. Read each of these in `Docs/memory/`, then any others that apply as you work: `longform-greenscreen-standard`, `green-screen-background-cycle`, `chroma-key-standard`, `chroma-key-efficiency`, `cutout-frame-and-gap-traps`, `ai-label-on-the-picture-not-the-scene`, `ai-clips-natural-or-regenerate`, `take-selection-rule-approved`, `self-bakeoff-before-dan-reviews`, `framing-standard-hair-anchored`, `broll-library-first`, `broll-always-colour-corrected`, `broll-shows-what-he-names`, `editor-audio-untouched`, `audio-joins-smooth-before-ship`, `review-page-what-i-decided`, `round1-full-graphics-review`.

**Study approved work.** Our rule is to start from the last approved recipe, not a blank folder. Watch this film all the way through, then study how it was built.
- Master: `claude edited long form content/25 - Reacting To Celebrity Ozempic Transformations/Reacting To Celebrity Ozempic Transformations | claude round 5 | 16x9 | RO-24.mp4`. This is the locked standard for long-form green-screen films.
- Work folder, read-only: `/Volumes/Expansion/_edit_work/RO-24/`. Its `round1/review/` shows a first-round packet, and `round5/` shows the finished build.
- Review page generators: `.claude/skills/longform-edit/reference/ro24/page24.py` and `.claude/skills/longform-edit/reference/ro10/page.py`.

That film reacts to celebrity clips, and this one is a beginner's guide. Work out which background types carry over, and what plays the role of "their clip" here, then put your reasoning in your onboarding page.

**Then prove you learned it.** Write `GEMINI-ONBOARDING.md` in your work folder, one page at most: how we edit, in your own words; how the green-screen standard applies to a cut-out film; the rules most likely to catch you out on this video; which approved recipe you are building from; and your plan for this edit. Then continue without waiting for an answer.

## Step 2: set up

Use a test name that cannot collide with the real job. Do not use `RO-37` as a job name: our tools read anything starting with it as the real job.

```bash
python3 .claude/skills/_shared/editcap/editcap.py acquire GEMINI-FIRST-GYM --title "First Time At The Gym Gemini LFC R1" --type LFC
python3 .claude/skills/_shared/renderq/renderq.py workdir GEMINI-FIRST-GYM --need 200
```

- `editcap` exit 0 means go. Exit 3 means wait for a slot: run `editcap.py wait GEMINI-FIRST-GYM` and tell Dan you are waiting.
- `workdir` prints your work folder. Build every round inside it, in `round1/`, `round2/` and so on. Never overwrite a reviewed round. The Extreme drive is nearly full, so do not force your work onto it.
- `ffmpeg` at `Media/video_edit/bin/ffmpeg` joins the render line by itself. Wrap other heavy steps with `renderq.py run --group GEMINI-FIRST-GYM --label "<step>" -- <command>`. Never write your own wait loop.
- Throwaway frames go in `renderq.py scratch GEMINI-FIRST-GYM`. Keep build files out of the project folder.

## The brief

**Video:** I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time. One long-form content master, 1920x1080, with an `.srt` sidecar (never burned in) and chapters. No Shorts, no vertical, no square and no one-minute version.

**Source map, which is the timing authority:** `Media/footage-index/shoot-20261023/queue-jobs/RO-37.json`. It holds the exact source ranges, every take, the measured mic picks, opening and closing candidates and source checks. Do not rebuild the edit from a broad roll listing. Ignore its `broll_candidates` list, which held temporary IDs.

**Filmed script:** https://docs.google.com/document/d/11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA/edit. If you cannot open it, work from the transcripts and say so.

**Source rolls:** `/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content/`: `C1893.MP4`, `C1894.MP4`, `C1895.MP4`, `C1897.MP4`. All are 2160x3840 portrait at 29.97 fps with a single live lav, about 13 minutes in total. Run `.claude/skills/_shared/rolls/roll_sidecar.py show` on each file first and reuse what it holds. Transcripts sit beside the map in `Media/footage-index/shoot-20261023/`. Transcripts mishear words, so check names and spellings against the script and the picture.

**Performance.** The map's candidates are a starting point, not a locked choice. Watch and listen to the whole relevant range and pick each line across all takes and rolls. Do not assume a planned alternate hook was filmed. Use any correction noted in the map. Keep Dan's filmed wording. Remove false starts, restarts and junk without clipping a syllable. Re-transcribe the assembled voice and read every join.

**Cut-out quality.** Hold this to the house key's bar, measured and on the moving picture:

- Steady edges, kept hair, no specks, no halo, nothing see-through.
- Close the gaps between arm and body, and keep fingers whole. Our matte models fill those gaps and thin blurred fingers into claws.
- Remove spill from the hedge and bright walls without touching his green shorts.
- Use `-fps_mode passthrough` on every sequential decode, or the matte and picture sit a frame apart. Reset temporal smoothing at every cut.
- Audit the delivered picture shot by shot, using the worst frame plus a 3x zoom and a moving-hand sheet. Blue and dark backgrounds expose faults that busy scenes hide.
- Check where an arm leaves the vertical camera's frame, and place Dan so the edge of the source never shows on screen.

**Exercise B-roll.** This film names a lot of gym equipment and exercises. The catalog holds finished October 23 clips, so search it for every one: `python3 .claude/skills/_shared/cliplib/clip_library.py find "<exercise>"`, then `show <ID>`. Use graded native editing masters, not proxies. Color C and exercise names are final, so do not ask Dan about them. Inspect the real action frame by frame before picking a rep, and show what Dan names at that moment. Compare the darker gym clips with the bright pool footage and correct any mismatch. Do not reuse the same clip in two places where you can avoid it. Never use raw ungraded footage, setup chatter, or a mistake shown as correct form. Chin-ups use an underhand grip and are not pull-up coverage. Incline dumbbell presses are not dumbbell chest flies. Where no correct visual exists, keep Dan on camera. Read `Docs/OCTOBER23_SHARED_EDITOR_ACCESS.md`.

**Missing items:** none known in the spoken content.

**Graphics.** Soft Blue Light, in real HyperFrames motion for their whole screen time, from the shared templates. Graphics carry key points and do not transcribe the speech. Title capitalization, with capitals only for the small eyebrow label. Lower thirds never sit across his abs or waist. Real pictures and AI pictures carry the exact labels in the rules. The AI label never covers a face or abs.

**AI clips.** The standard opens on a full-screen AI hook unless a camera open has a reason, and AI inserts run under 6 seconds. Offer a broad range of ideas tied to the actual lines, with a named setup and payoff for each. Frames go through `framecheck/gate.py` and a fresh frame reviewer before Dan sees them. Follow the blind Google test in `IMAGE-GENERATION.md` if you can reach Flow. If you cannot, show the Codex frames and say the Google option is missing. Keep presenter footage in the draft until Dan approves the motion.

**Ending:** organic. Keep Dan's spoken close. No AbsByAI.com end mark.

## Step 3: Round 1

Follow the round method for long-form. Run your own look and sound bake-off first, then show Dan one packet with everything together. **Do not build the full film yet.** The full film waits until Dan's choices and every asset are locked.

Your Round 1 review page contains:

1. **Header:** one line on the video, then what is already locked, then "Your decisions (N)" with real questions only, 20 at most, recommendation first.
2. **The finished first-minute draft** in one player, with the 1080p file and audio A/B links, built on your recommended picks and using the cut-out on the background template. Mark anything still pending.
3. **Colour:** at least three real options on matching frames, plus your written comparison to approved videos.
4. **Voice:** at least four level-matched options on the same continuous speech, starting on speech, including the untreated lav and the default chain.
5. **Cut-out proof:** your worst frames at 3x zoom on a light and a dark background, a moving-hand sheet and your measured numbers.
6. **AI opener and clip frames:** START and END side by side, with the action, duration, cost, what he says before and during, what comes after, and what plays if Dan says no.
7. **"What I decided (overrule anything)":** one plain line per call you made, including take picks, anything you rejected and why, and spend so far.
8. **Every graphic, photo, background segment and clip** in timeline order, three per row, each on its real graded frame, with ID, times, exact copy and source, and a "Play it moving, in context" button with 3 to 5 seconds of narration each side. One shared floating player, scrubbable. This covers the whole film's planned assets, not just the first minute.
9. **One reply box** with a Copy button.

Serve the page with `python3 .claude/skills/_shared/review_server.py <free port above 9900> <your review folder>` and require its "Managed review ready" result. Never use `python3 -m http.server`. Every linked file must sit inside the served folder.

**Stay silent.** Dan may be dictating. Use **Start silent checks** or `?review_mode=automation` before any playback test, and confirm the media is muted. When done, use **Finish checks for owner** so he gets a paused page with sound ready. Do not change Mac volume or audio routing.

Copy the first minute to `Videos to Review/`, named `First Time At The Gym Gemini LFC R1 - First Minute.mp4`, and open that folder for him.

**Before Dan sees anything, run all of this on the exact files he will see:**
- Audio gate, and `seamscan` on every join
- Head and hair clearance on every presenter frame against the background actually drawn, at least 20 px
- Jump-cut and junk-footage pass, plus a check that Dan is never still while the background swaps
- Your own watch pass at native resolution

**Independent review.** A fresh reviewer with no access to your notes reviews the delivered files against the brief and rules, following `.claude/agents/ra-reviewer.md`. Fix what it finds. If you cannot start a separate fresh session, say so and mark the review as not done. Do not review your own work and call it independent.

**Report honestly.** A check that did not run is a failure. Never raise a threshold, and never call a file passed when a row failed. If you hear or see audio with your own model, say exactly what you inspected. Numbers and silent playback are not a listening pass.

Then release your slot and stop:

```bash
python3 .claude/skills/_shared/editcap/editcap.py release GEMINI-FIRST-GYM --review
```

## Step 4: Dan's rounds

Dan's notes start the next round in this same chat. There is no pin transfer and no new task. Run `editcap.py acquire GEMINI-FIRST-GYM` again, save his exact words, make `round2/` and advance the chat title. Keep everything he approved byte for byte and change only what he asked. Show only what changed.

When every asset is locked, build the full film. Then run these on the exact file: `gate.py --format longform`, the edit sheet and its validation, the watch pass, the per-shot cut-out audit, and one independent complete-film review. List each change with its exact timestamps in the new film and a short watch range around it. Copy the full film to `Videos to Review/`.

When Dan approves the edit, stop there. Do not finalize, make thumbnails or set up the video. Run `editcap.py release GEMINI-FIRST-GYM` and delete your copies from `Videos to Review/`.

## Your report

Keep `GEMINI-TEST-REPORT.md` in your work folder and update it each round:

- Time spent and tokens or cost, if you can see them
- The spend ledger, including failed calls
- Which docs you read and which you could not
- Every tool that failed for you, and what you did about it
- New scripts you wrote, and which existing recipe you reused
- Every check result, including failures
- Every deviation from the rules, and any restricted file you saw by accident
- What you would not trust about your own edit

Your message to Dan at each stop is in plain language: what you made, the review link, and what he needs to decide. Use the video's title, not a code. End it with these two boxes, last, nothing after them:

> **What was done**
> One or two short plain-language sentences. No file paths, no jargon.

> **Your next steps**
> 1. Each thing Dan must do, starting with a verb, with the link, saying whether he has reviewed it yet.
