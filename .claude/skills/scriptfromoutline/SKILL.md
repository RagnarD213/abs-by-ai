---
name: scriptfromoutline
description: >
  Turn one of Dan's CONTENT video outlines into a word-for-word teleprompter
  script — so content videos are delivered off the teleprompter like the ads,
  instead of off the cuff. Use whenever Dan asks to script a content video from
  an outline, make a teleprompter script for a YouTube video, or "turn this
  outline into a script" for anything that is NOT an ad — even if he doesn't say
  "/scriptfromoutline". For AD scripts from ad outlines use /scriptwriting; for
  a clean teleprompter-only copy of a finished doc use /teleprompterscripts.
---

# Script From Outline: Content Outline → Teleprompter Script

**STATUS: v1 — created 2026-08-23. First test: "Your Belly Fat Is An Emergency"
(outline doc `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`). Update this file
after Dan reviews the first scripted videos — his line edits ARE the style
reference, same as /scriptwriting v2.**

## Why this skill exists (Dan's goals, 2026-08-23)

Dan's content videos were shot off the cuff from outlines. Editing them proved
what that costs: the 8/3 longform shoots cut **35–40% of runtime** (30:42→19:00,
40:16→30:28, 37:39→23:30) removing retakes, restatements, dead air, and rambling
bridges. Goals for scripted content:

1. **Tighter delivery** → far fewer cuts needed in the edit.
2. **Smoother finished product** even after editing (fewer joins = fewer zoom
   cuts and seams).
3. **Better phrasing** than off the cuff — if a point can be made sharper than
   Dan would improvise it, that's the value-add.

## Write so the edit doesn't have to happen (rules derived from what we cut)

Every rule here maps to a defect class the /longform-edit sessions removed by
hand. The script must be structured so those defects can't occur:

- **One pass per point. NEVER restate.** Restatements and re-introductions of
  the same item were the single most common junk Dan flagged (longform-edit junk
  rules 3 and 7). No "so basically…" recaps, no re-explaining a point two
  sections later, no doubled introductions. Before delivering, do a repeat scan
  of your own script: any 3–5-word phrase appearing twice within a section is a
  bug unless it's deliberate anaphora.
- **Announce the structure with numbers, then walk it.** "There are seven
  reasons… Number one…" — this is already Dan's natural content style
  (six-ways transcript) and it kills rambling bridges. Every transition is
  explicit ("Here's the second reason"), so there's never a searching-for-words
  moment on camera.
- **Short sentences, one idea each.** Teleprompter-readable, breath-friendly.
  No parentheticals, no nested clauses. Em-dash pivots are fine.
- **No throat-clearing anywhere** — not just the open. Every section starts on
  its point.
- **Front-load a reason to keep watching** in the first 30 seconds, but content
  pacing, not ad pressure: this is a viewer who chose to click, not a skip
  timer.
- **Definitions get exactly one beat.** Dan's style explains terms for the
  average guy ("let me back up a step — what tracking macros means is…") — do
  it once, at first use, never again.

## Voice (content register — ground truth)

Ground truth transcript: `YouTube Long Form Video Content/six-ways-ai-abs/v2-transcript.txt`
(38 min of Dan actually talking to camera in content mode). Content voice =
ad voice traits (see /scriptwriting) PLUS:

- "y'all guys", "Listen —", "let me explain to you why that is", "And I'll put
  a picture right here so y'all guys can see…"
- Educational, honest, no-hype: "reasonably accurate", "within plus or minus
  10%", "far, far better than doing nothing". He under-promises on camera.
- Stories with named specifics (Mike Chang / Sean Ray) — use his real stories
  and numbers, never invented ones. His numbers: before photo at **38**, two
  hundred pounds (2024); abs back at **forty**; he is **40** now; one child, a
  **daughter**. Zepbound update numbers: **192 → 181**.
- Doubled intensifiers ("really, really", "far, far", "very, very"),
  "next level", "the truth is".
- Numbers written out for the teleprompter ("two hundred pounds").
- Mid-video soft CTAs at hot moments are his real style ("If you want to start
  tracking your macros, go to absbyai.com") — short, then move on. He also
  name-drops free alternatives (Claude, Gemini) — that honesty stays.

## Content vs ads — what changes

- **Length:** 10–15 min default unless Dan says otherwise. His relaxed content
  pace is ~2.3–2.5 words/sec → target **~1,500–2,200 spoken words** (aim
  ~1,900 for a 12–14 min video). State word count + runtime estimate at top.
- **Drug names are allowed SPOKEN in content** (he has a whole Zepbound video).
  The ad rule ("weight loss medication" only) does not apply to organic
  content. **But no drug or brand name ever appears in on-screen graphics/chips**
  (standing rule), and any medication/TRT recommendation keeps a short
  "I'm not a doctor, talk to your doctor" beat — his Zepbound video kept its
  disclaimer in full, never trim it.
- **Fear is allowed when it IS the premise** (e.g. the "emergency" video). The
  ad rule "sell the goal, never the fear" softens to: land the fear beat
  honestly, then pivot each point to the goal side. Don't wallow.
- **CTA close (Dan's confirmed default 2026-08-23):** short AbsByAI.com plug
  tied to whatever AI points the video made + subscribe. Not an ad-style pitch.
- **Cue density (Dan's confirmed default 2026-08-23): LIGHT.** Bracketed cues
  only where a visual is load-bearing (before picture, a referenced video
  card). The edit adds b-roll/chips later per /longform-edit — the script stays
  clean to read. Markup convention same as /scriptwriting: everything
  non-spoken is **[BRACKETED, ALL CAPS, BOLD]**, yellow highlight for Claude's
  directions, orange for Dan's notes.
- **Outline intro sections marked "verbatim" stay near-verbatim** — smooth only
  for speakability, and say what you changed.

## Process

1. Read the outline (Drive MCP `read_file_content`; pull the .docx export if
   bullets hide images — see /scriptwriting mechanics).
2. **Ask Dan the context questions first** — specifically: (a) which points he
   has personal experience with (never fake first-person experience — the TRT
   point in video 1 is general-recommendation because he said so), (b) CTA
   preference, (c) anything the outline asserts that needs his numbers/story.
3. Write the script. Do a dedicated tightening pass over the first minute, and
   the repeat-scan pass over the whole thing.
4. **Show the full script in chat for Dan's approval BEFORE the Google Doc.**
5. Deliver into a Google Doc using the proven /scriptwriting Docs mechanics
   (osascript HTML-clipboard paste; all the clipboard/heading/undo traps
   documented there apply verbatim). **Delivery target (settled 2026-08-23):
   append the script INTO THE SAME OUTLINE DOC, below the outline** — Dan's
   "add that script to the document" meant the outline doc itself. Shoot 5
   outlines doc: `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`. Recipe that
   worked first try: cursor at end of last outline bullet → Return twice (exits
   the bullet list into Normal text) → paste. Use styled `<p>` paragraphs for
   section headers, NOT `<h2>` — avoids the heading-style trap entirely.
6. Standing visual rule: no side-by-side before/after if any frame of this
   video might be cut into an ad (shorts/ads mining is routine — assume it
   will be).

## Lessons

- (v1 — none yet. Append Dan's line-edit lessons here after the first review,
  the way /scriptwriting v2 did.)
