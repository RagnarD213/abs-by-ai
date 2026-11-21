CONTENT (SFC). Task name: `How To Do Hamstring Curls Gemini SFC R1`.

# Gemini Argon editing test: How To Do Hamstring Curls

**Project folder:** `/Users/danielrose/Projects/Claude/Projects/Abs By AI`. Run every command from there.

You are Gemini, joining a video operation that today runs on Claude and Codex. Dan Rose owns the business. He is not a coder, so write to him in plain language. Your job is to learn how we edit, then edit this one dedicated Short from raw footage to Dan's review page, to our full standard. Dan is testing whether you can do this work as well as Claude and Codex.

The instructions in this repo were written for Claude and Codex, and they all apply to you. Wherever they say "Claude" or "Codex" as the editor, read "the editor", which is you.

## This is a test edit of a finished video

This film is already approved and in setup, so the test works differently from a normal job in three ways:

1. **Blind.** Build your own edit from the raw footage. Never open the earlier work listed under "Do not open". If you see any of it by accident, say so in your report.
2. **Isolated.** Nothing you make touches the real job, its queue row, its files or its schedule.
3. **Same bar.** Everything else is exactly the real process, including Dan's review rounds.

### Do not open

- `/Volumes/Extreme/_edit_work/DS-84/` and any other DS-84 work folder
- `Short-form video content/DS-84 How To Do Hamstring Curls/`, in the project and on Extreme
- `Handoffs/video-editing/DS-84-how-to-do-hamstring-curls.md` and `DS-84-R3-approval.json`
- `Handoffs/handoff-20261028-ds84-hamstring-curls-covers-and-setup.md`
- `Docs/DS84_*`
- Review pages on ports 9267, 9268, 9284 and 9285
- Anything in `Videos to Review/` whose name starts with `How To Do Hamstring Curls SFC`

The brief below replaces the job doc. The one DS-84 file you do read is the source map named in it.

### Do not change

- Do not run `queue.py`, and do not touch `jobs.json`, `00-MASTER.md` or the Edit Queue page. The real job is finalized, and setting it to `in_progress` would corrupt that record.
- Do not run `roll_sidecar.py mark-used`, and do not register anything in the clip library. A test should not mark footage as used.
- Do not edit `AI_COORDINATION.md`, `AGENTS.md`, `CLAUDE.md`, any skill, any gate or any threshold. If a rule or tool looks wrong, write it in your report.
- Do not commit or push. Do not upload, schedule, publish, make covers or touch Blotato, YouTube or Google Drive.
- Do not send messages to anyone, and do not start or message other tasks.
- Do not run scripts inside another job's folder. Reference folders are read-only: copy what you need into your own folder.
- Raw footage is read-only. Do not move, rename or re-encode it in place.
- Do not spend money. No paid generation calls. If an AI clip would genuinely help, propose it as a text idea on the review page and do not generate it.

## Step 0: prove you can do the work

Before anything else, check that you can actually:

- read and write files in the project folder
- read `/Volumes/Extreme` and `/Volumes/Expansion`
- run shell commands, including `Media/video_edit/bin/ffmpeg`, `python3` and `~/.npm-global/bin/hyperframes`
- look at rendered frames, and inspect audio without playing it through the speakers
- start a server on this Mac and load its page in a browser

Report what works in one short list. **If you cannot run commands or reach the footage, stop and tell Dan exactly what is missing.** Do not simulate any step, and do not describe work you did not do. A plan with no real files in it is a failed test, and an honest stop is not.

## Step 1: catch up on how we work

The repo's slash commands (`/shorts`, `/ad-edit`) and auto-loaded files will not load for you. Read these directly, in full, in this order.

**Who we are and the standing rules**
1. `AGENTS.md`
2. `CLAUDE.md` (its `@` lines point at the files named here)
3. `AI_COORDINATION.md`, to see what else is running. Read only; do not edit.
4. `.claude/skills/_shared/VIDEO-RULES.md`. This is the main rulebook, and it is long. Newer sections sit at the top and win over older ones.
5. `Handoffs/video-editing/00-RULES.md`

**How we edit**
6. `.claude/skills/_shared/EDITOR-CARD.md`, which explains why good edits win
7. `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, the round method and review page
8. `.claude/skills/_shared/ASSET-APPROVAL.md`
9. `.claude/skills/_shared/CUT-CONTINUITY-QC.md`
10. `.claude/skills/_shared/HOOKS.md`
11. `.claude/skills/ad-edit/SKILL.md`, Steps 0.4 to 4, for take selection, audio and zoom cuts
12. `.claude/skills/shorts/SKILL.md` for the vertical finishing rules. Some of it is about cutting Shorts from a long-form; use the vertical, caption, junk-scan and QC rules. This job is a dedicated Short cut from raw footage.
13. `.claude/skills/_shared/framing-motion.md`

**Look and graphics**
14. `.claude/skills/_shared/SOFTBLUE.md`
15. `.claude/skills/_shared/GRAPHICS-STANDARDS.md`
16. `.claude/skills/_shared/hyperframes/README.md`

**Tools**
17. `.claude/skills/_shared/rolls/README.md`
18. `.claude/skills/_shared/cut/README.md`
19. `.claude/skills/_shared/audio/README.md`
20. `.claude/skills/_shared/cliplib/README.md`
21. `.claude/skills/_shared/renderq/README.md`
22. `.claude/skills/_shared/editcap/README.md`
23. `.claude/skills/_shared/deliver/README.md`
24. `.claude/agents/ra-reviewer.md`, how an independent review is done
25. `Handoffs/handoff-20260914-ad3-square-codex.md`, section 2, for traps on this Mac (paths with spaces, the project ffmpeg, and similar)

**Memory.** `Docs/memory/MEMORY.md` is the index. Read each of these in `Docs/memory/`, then any others that apply as you work: `take-selection-rule-approved`, `self-bakeoff-before-dan-reviews`, `framing-standard-hair-anchored`, `vertical-centering-standard`, `shorts-show-whole-exercise`, `broll-library-first`, `broll-always-colour-corrected`, `broll-shows-what-he-names`, `no-boxes-without-reason`, `editor-audio-untouched`, `audio-joins-smooth-before-ship`, `review-page-what-i-decided`, `round1-full-graphics-review`.

**Study approved work.** Our rule is to start from the last approved recipe, not a blank folder. Read these and copy their methods into your own folder. Both are read-only.
- `/Volumes/Extreme/_edit_work/DS-76/`: "How To Do Pull-Ups". Same shoot, same kind of video, approved by Dan. Final master: `Short-form video content/DS-76 How To Do Pull-Ups/How To Do Pull-Ups SFC R2 - complete Short.mp4`. Watch it, then read `round1` and `round2`: `edit-plan.json`, `look-options.json`, `recipe`, `records`, `evidence` and `review`.
- `/Volumes/Expansion/_edit_work/DS-61/round1/`: "How To Do Bodyweight Squats". A current Round 1 review packet, with its review reports (`ROUND-1-REVIEW*.md`).

**Then prove you learned it.** Write `GEMINI-ONBOARDING.md` in your work folder, one page at most: how we edit, in your own words; the rules most likely to catch you out on this video; which approved recipe you are building from; and your plan for this edit. Then continue without waiting for an answer.

## Step 2: set up

Use a test name that cannot collide with the real job. Do not use `DS-84` as a job name: our tools read anything starting with it as the real job.

```bash
python3 .claude/skills/_shared/editcap/editcap.py acquire GEMINI-HAMSTRING --title "How To Do Hamstring Curls Gemini SFC R1" --type SFC
python3 .claude/skills/_shared/renderq/renderq.py workdir GEMINI-HAMSTRING --need 30
```

- `editcap` exit 0 means go. Exit 3 means wait for a slot: run `editcap.py wait GEMINI-HAMSTRING` and tell Dan you are waiting.
- `workdir` prints your work folder. Build every round inside it, in `round1/`, `round2/` and so on. Never overwrite a reviewed round.
- `ffmpeg` at `Media/video_edit/bin/ffmpeg` joins the render line by itself. Wrap other heavy steps with `renderq.py run --group GEMINI-HAMSTRING --label "<step>" -- <command>`. Never write your own wait loop.
- Throwaway frames go in `renderq.py scratch GEMINI-HAMSTRING`. Keep build files out of the project folder.

## The brief

**Video:** How To Do Hamstring Curls. One dedicated organic Short teaching lying machine hamstring curls, 1080x1920. No other versions and no Shorts cut from it.

**Source map, which is the timing authority:** `Media/footage-index/shoot-20261023/queue-jobs/DS-84.json`. It holds the exact source ranges, every take, the measured mic pick, opening and closing candidates and source checks. Do not rebuild the edit from a broad roll listing.

**Filmed script:** https://docs.google.com/document/d/11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA/edit. If you cannot open it, work from the transcript and say so.

**Source:** `/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content/C1887.MP4`, 2160x3840 portrait, 29.97 fps, about 72 seconds of relevant range, single live lav. Run `.claude/skills/_shared/rolls/roll_sidecar.py show` on this file first and reuse what it holds. Transcript: `Media/footage-index/shoot-20261023/C1887.transcript.json`. Transcripts mishear words, so check names and spellings against the script and the picture.

**Performance.** The map's candidates are a starting point, not a locked choice. Watch and listen to the whole relevant range and pick each line across all takes. Do not assume a planned alternate hook was filmed. Use any correction noted in the map. Keep Dan's filmed wording. Remove false starts, restarts and junk without clipping a syllable.

**Picture.** Preserve native portrait orientation and keep Dan's head and hair clear of the frame edges and graphics, measured on real masks. Make an intentional crop-size choice, and do not stretch him or cut him off.

**Exercise B-roll.** Approved library IDs: **B0626, B0627, B0628, B0629, B0630**. Pull each with `python3 .claude/skills/_shared/cliplib/clip_library.py show <ID>` and use the graded native editing master, not a proxy. Search the catalog for other hamstring-curl takes too. Color C and exercise names are final, so do not ask Dan about them. Inspect the real action frame by frame before picking a rep, and make sure each shot shows what Dan is saying at that moment. Never use raw ungraded footage, setup chatter, or a mistake shown as correct form. A clip being approved does not mean it fits a given line, so choose only what fits. Read `Docs/OCTOBER23_SHARED_EDITOR_ACCESS.md`.

**Missing items:** none known in the spoken content.

**Graphics.** Soft Blue Light, in real HyperFrames motion, from the shared templates. Graphics carry key points and do not transcribe the speech. Follow the exercise teaching rules in `shorts/SKILL.md` and the title capitalization rule in VIDEO-RULES.

## Step 3: Round 1

Follow the round method. Run your own look and sound bake-off first, then show Dan a whole Short built with your recommendations. The approved Short models above did this, and it matches the "build the whole video" rule because this film has no unseen AI clips. If you do propose something new or risky, show it separately and leave it out of the main cut.

Your Round 1 review page contains:

1. **Header:** one line on the video, then what is already locked, then "Your decisions (N)" with real questions only, recommendation first.
2. **The whole Short** in one player, with the 1080p file and audio A/B links.
3. **Colour:** at least three real options on matching frames, plus your written comparison to approved videos.
4. **Voice:** at least four level-matched options on the same continuous speech, starting on speech, including the untreated lav and the default chain.
5. **Crop:** portrait size options, with their measured head clearance.
6. **"What I decided (overrule anything)":** one plain line per call you made, including take picks and anything you rejected and why.
7. **Every graphic and clip** in timeline order, three per row, each on its real graded frame, with ID, times, exact copy and source, and a "Play it moving, in context" button with 3 to 5 seconds of narration each side. One shared floating player, scrubbable.
8. **One reply box** with a Copy button.

Serve the page with `python3 .claude/skills/_shared/review_server.py <free port above 9900> <your review folder>` and require its "Managed review ready" result. Never use `python3 -m http.server`.

**Stay silent.** Dan may be dictating. Use **Start silent checks** or `?review_mode=automation` before any playback test, and confirm the media is muted. When done, use **Finish checks for owner** so he gets a paused page with sound ready. Do not change Mac volume or audio routing.

Copy the full-quality Short to `Videos to Review/`, named `How To Do Hamstring Curls Gemini SFC R1 - Full Short.mp4`, and open that folder for him.

**Before Dan sees anything, run all of this on the exact files he will see:**
- Audio gate, `seamscan` on every join, and the delivery gate at `--format` for this Short
- Head and hair clearance across every presenter frame
- Jump-cut and junk-footage pass
- Captions against the speech: spelling, trailing entries, and the brand name `sixpackabs.com`
- Your own watch pass at native resolution

**Independent review.** A fresh reviewer with no access to your notes reviews the delivered files against the brief and rules, following `.claude/agents/ra-reviewer.md`. Fix what it finds. If you cannot start a separate fresh session, say so and mark the review as not done. Do not review your own work and call it independent.

**Report honestly.** A check that did not run is a failure. Never raise a threshold, and never call a file passed when a row failed. If you hear or see audio with your own model, say exactly what you inspected. Numbers and silent playback are not a listening pass.

Then release your slot and stop:

```bash
python3 .claude/skills/_shared/editcap/editcap.py release GEMINI-HAMSTRING --review
```

## Step 4: Dan's rounds

Dan's notes start the next round in this same chat. There is no pin transfer and no new task. Run `editcap.py acquire GEMINI-HAMSTRING` again, save his exact words, make `round2/` and advance the chat title to `R2`. Keep everything he approved byte for byte and change only what he asked. Show only what changed. In your message, list each change with its exact timestamps in the new full Short and a short watch range around it. Repeat the checks on the new exact file.

When Dan approves the edit, stop there. Do not finalize, make covers or set up the video. Run `editcap.py release GEMINI-HAMSTRING` and delete your copies from `Videos to Review/`.

## Your report

Keep `GEMINI-TEST-REPORT.md` in your work folder and update it each round:

- Time spent and tokens or cost, if you can see them
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
