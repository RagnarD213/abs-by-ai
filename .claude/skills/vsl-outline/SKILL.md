---
name: vsl-outline
description: >
  Outline (and, once Dan approves the outline, script) a video sales letter (VSL) by modeling the winning VSLs in its
  category instead of Claude's own taste: find who is spending the most on VidTao right now, download and transcribe
  their VSLs, map their structure, timing and tactics, then build an outline that is unique and attention-grabbing in
  the first minutes and follows the winners closely after that. Use whenever Dan asks for a VSL, a sales video, a
  sales video outline, a funnel to model, "what are the winners doing", or a VSL contest between AIs, even if he
  doesn't say "/vsl-outline". For ads use /ad-outlines and /scriptwriting; for organic videos /scriptfromoutline.
---

# /vsl-outline

Built 2026-11-08 from the Great Again T work (`Handoffs/great-again-t-20261105/vsl-outlines-AB-20261108.md` is the
worked example; the research is in `Docs/testosterone-funnels-20261105/`).

## The rule this skill exists for

Dan, 2026-11-08: *"Using Claude's own judgment and taste for these things doesn't work. That's why so many people have
tried to make ads with Claude, and they didn't work. That's why a lot of our ads previously that we made didn't work.
We need to use the judgment of people who are proven to be successful."*

What went wrong before this skill, all in one session, all caught by Dan: Claude recommended opening on Dan's story
(neither winner does); paid off every food in its own section (neither winner does: the foods are bait); and on audit
had about 15 more places where it followed its own preference (length, shock proof, stats montage, client story,
"food first, supplement second", voiceover vs on camera, Q&A questions, page details). Memory:
`model-proven-funnels-exactly`.

**So the default is: copy what the winners actually do, checked line by line against their transcripts and pages.**
The only allowed reasons to differ, and each one is written down next to the change:
1. **Rip-off risk**, mostly in the first few minutes (see "Unique up front" below).
2. **Untrue for us**: a fake regular price, invented scarcity, a doctor we don't have, testimonials we don't have. Keep
   the tactic and write the truthful version of it; never drop it for a softer substitute.
3. **Product difference**: our ingredients, our mechanism, our offer.
4. **Dan's explicit call.**

Anything else that differs from the winners is a mistake. A deliberate experiment is allowed only when labeled as an
untested bet, never presented as the recommendation.

## Steps

### 0. Before anything
- AGENTS.md "Sales videos: outline first": the outline is agreed with Dan before any script. Dan can waive it explicitly.
- AGENTS.md "Marketing advice: proven direct response only": name who runs each tactic.
- Category check: a VSL is sales copy that ships, so the claims rules on record apply (briefly). No em or en dashes in
  anything outward facing.

### 1. Find the winners (VidTao, Dan's login, Claude in Chrome)
- Ad search sorted by recent spend: `https://www.vidtao.com/ad-search?q=<term>&sort=spend30&dir=desc`. Search the
  category words and the hero ingredient. Brand pages `https://www.vidtao.com/brand/<id>` show lifetime spend, last 30
  days, monthly spend, top ads with lengths and hooks, and **landing pages ranked by share of spend**.
- **Recent spend beats lifetime spend.** A brand at its peak month right now (TestoGreens, Oct 2026) is stronger evidence
  than a big lifetime number that has cooled off.
- Pick two models: usually the biggest current pure-marketing funnel (no brand to lean on) and the closest big brand
  to Dan's position (a fit founder: V Shred). Note how many ads each tests into one page; volume is often the real edge.
- Never start the paid VidTao trial. If the page redirects to onboarding, pick the niches and go back to the URL.
- JS output that contains `?`, `=` or `&` gets blocked as cookie data: strip them before returning (`.replace(/[?=&]/g,' ')`).

### 2. Get the full VSLs and transcribe them
- On the sales page, list the video streams:
  `performance.getEntriesByType('resource').map(e=>e.name).filter(n=>/m3u8/.test(n))` (strip `?=&` before returning).
  Most use Vidalytics: `.../stream.m3u8` plus `..._variant.m3u8` files; the variant name shows the format
  (`1920x1080` horizontal, `720x1280` vertical).
- Download audio only with the repo ffmpeg and a Referer header, then transcribe: `scripts/transcribe.py` (usage and
  traps in its header). An 80-minute pair takes roughly 20 minutes.
- Ads: VidTao's ad modal often has no transcript; play the ad in the modal and read the YouTube id from the iframe
  (`embed/<id>`), then yt-dlp the audio.
- Save one transcripts file, paragraphs with start timestamps: `Docs/<topic>-funnels-<date>/VSL_TRANSCRIPTS.md`.

### 3. Inspect the funnel itself
- **Take the quiz** with "No" on every answer and see where it goes. V Shred's 4-question quiz is a dummy: every answer
  lands on the same video. Its jobs are the "Take the quiz" call to action, small yeses, and previewing the video's
  promises. Dan, 2026-11-08: no data questions (Google Ads already reports age; asking is intrusive).
- Note every page element: headline, "click to unmute," resume watching, "In this video you'll learn" bullets, when the
  buy button appears, study references under the video, the price ladder, the guarantee, bonuses, upsells.
- Check every landing page the brand runs (VidTao's list): a no-quiz and a quiz version of the same VSL is a real
  head-to-head (V Shred: ~$4.0M direct vs ~$2.2M quiz; the quiz version is the one still running).

### 4. Map the structure
- `python3 scripts/sections.py <transcripts.md> "<start heading>" "<end heading>"` gives words per paragraph and a
  running total. Build a table: section, timestamp, words, what it does.
- Write down specifically: what the headline promises and **when (or whether) it is paid off**; when the spokesman
  first appears (in both winners: after the hook, about minute 3); the mechanism's name and how often it repeats; the
  shock proof; the stats montage; where the client story and testimonials sit; ingredient lore; the price staircase;
  the bonus stack and its curiosity bullets; scarcity; the close (option one and option two); the Q&A after the close.

### 5. Write the outline
- **Unique up front, modeled after.** Dan: *"It's really the beginning that we need to make unique and especially
  attention-getting. The later part... we can model more closely, except for things that clearly need to be
  different."* The first 2 to 3 minutes get a different opening line, different foods or objects, a different shock
  proof, a different villain and mechanism name, and different wording. Same category is fine (both winners open on
  foods; ours does too, with other foods). After that, same section order, proportions and machinery.
- Every section header carries the model's matching time in brackets, e.g. `[V Shred 7:38 to 17:10]`.
- Include: a claims table (each claim, the study, the institution or country, verified); a **truthful-version table**
  for every tactic we can't copy literally; Dan-fact slots; a rip-off check table (first line, shock proof, villain,
  foods, messenger, hero ingredient, theirs vs ours); a short "Decisions for Dan" list.
- **Dan's facts: ask, never invent.** Personal story, numbers, blood work, client stories. Missing = a marked blank.
  Use only what earns its place (memory `personal-facts-only-when-relevant`).
- **Check our own label against our villains.** Great Again T contains licorice extract, so licorice could not be a "bad
  food"; it uses zinc oxide, so V Shred's "cheap zinc oxide" argument would attack our own product; two tablets already
  hold 50 mg zinc, so TestoGreens' "double dose" tactic was a safety problem.
- Deliver as a Google Doc (`scripts/md2html.py` then Drive create_file as text/html, set anyone-with-link) plus the
  repo markdown, and list it in `Handoffs/README.md` OPEN.

### 6. Audit before Dan sees it
Go through the outline element by element against the transcripts: proven (say where) or a deviation (say which of the
four allowed reasons). Fix everything else. This audit is what Dan asked for on 2026-11-08 and it found 15 items.

### 7. The first 30 seconds
- Rules: `.claude/skills/_shared/HOOKS.md` (first sentence stops the scroll alone, payoff by second 5, open loop, blame
  a thing, stay true). Write three hooks per VSL; film all three as hook takes.
- **Panel 1, blind, first 30 seconds.** Put the winners' real openings (first ~100 words, with a line on what's on
  screen) unlabeled among ours; two independent agents judge them (a supplement copy chief, and the target viewer: when
  he'd leave, what he believes). Use it for similarity pairs and concrete leaks, **not as the verdict**: on 2026-11-08
  a general panel scored the proven winners 20 to 77 out of 100. Generic AI taste punishes exactly the things that
  convert (scare language, conspiracy shocks, "you need to know" stalls). Dan: "Don't use default Claude judgment,
  think like the guys running V Shred and TestoGreens."
- **Panel 2, operators, first 5 minutes.** Give two agents the winners' real first 5 minutes labeled as proven
  controls (with spend) and ours as challengers. One plays the winner's head of marketing, one the winner's lead
  copywriter; they judge by the controls' standards: would you split test it expecting it to beat your control, where
  do viewers leak, which lines would a control viewer recognize, and line edits using only our true facts. Iterate until
  both say the challenger beats or matches its control with no recognizable lines. Dan's bar: top 5% of VSL openings,
  better than the winners, not a rip-off, and a smooth transition into the marketing message.
- **The operators' first-5-minute playbook** (both winners do all of it): threat inside something he trusts; damage in
  manhood terms within about 20 seconds; an escalating shock ("wait till you hear this"); the threat is everywhere; a
  named hidden enemy; why his effort fails; not his fault; a big, simple promise (seconds a day, no prescription); an
  early "imagine"; open loops repeated; authority at about minute 3; a symptom list he recognizes; transformation with
  numbers; identity stakes (provider, father, "shell of the man").
- **What the operator panels taught on Great Again T (2026-11-08, four rounds):** never reveal the product format
  ("two tablets") or name or locate the hero ingredient in the first 5 minutes (neither winner does; a named root lets
  savvy viewers leave and search); the enemy needs a present-tense edge, not only a past one (V's "sprayed every single
  day... in the air you breathe"); a symptom block after the hook must pay off a promise ("what this is really costing
  you"), not rewind; never end minute 5 on a stall; check every six-word run against the transcripts (a quick n-gram
  script) because "modeling closely" drifts into copied signature lines; one reviewer's verdict is not the answer,
  so use at least two fresh, unanchored reviewers for the final call.
- **The founder's story only claims what's true.** If the transformation also involved other things (Dan's included
  Zepbound, training and calorie tracking), the script must not let the product or the food swap take the credit.

### 8. Scripting (only after Dan approves the outline)
- Match the model's proportions section by section (`scripts/sections.py --script <file>`). Dan reads about 165 words
  a minute; the winners read faster (V Shred ~206, TestoGreens ~187), so match time and section share, not raw words.
- His voice: plain, direct, his charged words kept (memory `claude-softens-strong-language`); the dan-voice method is
  `/dan-voice`. Swap blocks for sale versions (`[JANUARY VERSION: ...]`). Every bracketed note is for the edit, not read.
- Close each script with a section map table: our section, time, model section, deviation and reason.

### 9. Contest option
When Dan wants a contest: one blind brief per AI. Codex reads the repo (point it at the outline and transcripts, tell
it never to open Claude's folder). Gemini and Grokbot can't read the Mac, so build one self-contained package (brief +
outline + transcripts) as a shared Google Doc. Starter prompts in chat with model and effort. Example:
`Handoffs/great-again-t-20261105/contest/`.

## Files
- `scripts/transcribe.py`: Whisper transcription (render-queue aware), with the audio download commands in its header.
- `scripts/sections.py`: words per section for the model and for our script.
- `scripts/md2html.py`: markdown to HTML for a Google Doc upload.
- `scripts/copycheck.py`: lists every 6+ word run our script shares with a model transcript, with its minute; rewrite
  runs of 8+ words, and keep the first 5 minutes at zero.
