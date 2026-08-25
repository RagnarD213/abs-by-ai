---
name: shorts-scripting
description: >
  Turn ONE dedicated shorts idea — a title plus bullets from /shortsideas, or a
  brief outline Dan writes himself — into a finished word-for-word teleprompter
  script with b-roll cues, built to Dan's measured 176-180 word spec, and deliver it
  into the DEDICATED SHORTS CONTENT section of the current shoot's outline doc. Use
  whenever Dan asks to script a short, write out a shorts idea, turn a shorts title
  into a script, or edit a short he drafted himself — even if he doesn't say
  "/shorts-scripting". For generating the ideas use /shortsideas; for full-length
  CONTENT video scripts use /scriptfromoutline; for AD scripts use /scriptwriting;
  for cutting shorts out of an existing longform video use /shorts.
---

# Shorts scripting: write one short to Dan's landed spec

**STATUS: v1 — created 2026-08-25 from Dan's two finished dedicated shorts ("Top 5
Ab Exercises" and "How Getting Abs Looksmaxxes Your Face") and, more usefully, from
what he REVERTED when Claude edited them. Both finished scripts landed at 177 and
176 spoken words. That is not a coincidence and it is the spec.**

## The job

One idea in, one finished script out. The input is either a line from the
**"Ideas for shorts to write out"** list (a Title Case title plus 2-4 content
bullets) or a rough script Dan typed himself that needs editing for length and
content. The output is a teleprompter-ready script with b-roll cues, delivered into
the **DEDICATED SHORTS CONTENT** section of the current shoot's outline doc.

**One short per invocation.** These are short enough that batching them produces
generic writing.

---

## THE SPEC — 176-180 spoken words

Measured off both of Dan's finished shorts: **177 words** and **176 words**. At his
measured 198-222 wpm that is **48-54 seconds**, which sits under YouTube's
60-second music-licence cliff and inside Instagram's best reach bucket (30-60s).

**Write to 176-180. Count the words before delivering — do not estimate.**

```bash
python3 -c "
import re,sys
t=open('script.txt').read()
t=re.sub(r'\[[^\]]*\]','',t)          # strip bracketed cues
w=[x for x in re.split(r'\s+',t) if re.search(r'[A-Za-z0-9]',x)]
print(len(w),'words ->',round(len(w)/222*60),'to',round(len(w)/198*60),'seconds')"
```

Anything over 190 is a rewrite, not a trim.

---

## THE SKELETON — both of his scripts have exactly this shape

| # | Beat | Words | Notes |
|---|---|---|---|
| 1 | **Opener** | 11-14 | A direct declarative claim. See the hard rules. |
| 2 | *(optional)* **Proof beat** | ~17 | Only when there's a visual to show. The face script uses before-then-after here. |
| 3 | **Structure statement** | 11-12 | "…improves your face in three ways." / "Here are the top five ab exercises…" Tell them what's coming. |
| 4 | **The numbered beats** | **21-30 each** | "Number one, the ab wheel." / "First, it defines your jawline." Name + one reason + one qualifier or scaling note. |
| 5 | **The beat nobody else says** | ~25 | The insight that isn't on the list. Only fits when there are three items, not five. |
| 6 | **The "remember" line** | 19-23 | A summary that reframes. "And always remember, losing your stomach fat with nutrition will be more important than any ab exercise you do." |
| 7 | **Comment close** | 11-13 | "Comment and let me know which ab exercise is your favorite." |

**Three items leaves room for beat 5. Five items does not.** That is the real cost of
a five-item list and it should be said out loud when Dan picks one — beat 5 is the
most valuable thing in either script.

---

## HARD RULES — every one of these comes from Dan reverting an edit

### 1. Never speak the product. Ever.

Claude added a spoken plug to both scripts. **Dan deleted both.**

- Deleted: *"AbsByAI.com will show you what you look like lean."*
- Deleted: *"AbsByAI.com will tell you how lean you need to get."*

The **on-screen `AbsByAI.com` mark stays** — the cue `[AbsByAI.com mark on screen]`
survived in both. The product gets the graphic, not the words.

**The one exception:** when the *idea itself* is a product idea ("Top 3 Ways To Use
AI To Get Abs"), the app is the content and is spoken normally. It is a plug that's
banned, not the subject.

### 2. The close is always "Comment and let me know [specific thing]."

Claude rewrote this twice, with a defensible argument both times. **Dan reverted it
both times.**

- His: *"Comment and let me know which ab exercise is your favorite."*
- His: *"Comment below and let me know how your face changed after getting leaner."*

Write it in that form. Don't make it clever, don't turn it into a send cue, don't
"fix" it because it presupposes something about the viewer.

**The Instagram send cue is measured-correct and Dan does not want it in the script.**
A DM share outranks a comment 3-5x for reaching non-followers, so it is still worth
having — deliver it as a **one-line note beside the script**, never inside it.

### 3. Dan writes the opener, and it is a plain claim — not a contrarian negation.

Claude replaced his opener with *"No ab exercise burns belly fat…"* — a correction
hook with real data behind it. **He put his own back:** *"Here are the top five ab
exercises for getting six pack abs."*

What he kept was his own: *"Getting abs makes your face look way better. And I'll
prove it to you."* — a **claim plus a promise of proof**.

So: **open with a direct claim, or a claim plus proof promise. Never open by telling
the viewer he's wrong.** If the idea's title is already the claim, the opener can be
close to the title spoken aloud, and that is fine.

### 4. The body is fully open — cut hard, and add.

He kept **every** rewritten exercise beat verbatim, including a blunt line Claude
added (*"Useless while you're still soft."*), and he kept an entire beat Claude
invented (*"Your face leans out before your abs show up."*).

**The body is where the word count comes from.** Trim two scaling notes down to one,
merge overlapping points, delete restatements. He will not defend body wording.

### 5. Count your list items honestly.

His face draft said "three ways" and listed four. Merge until the number is true.

### 6. Sequential reveals only, and say so in the cue.

`[SHOW DAN BEFORE PICTURE — 200 lb era, FACE. Full frame, not split-screen]`.
Before-then-after is fine; two images in one frame is banned, and an editor will
reach for the split-screen unless the cue forbids it.

### 7. No second-person age.

"For Men" is fine. "If you're over 40" costs 1-2 orders of magnitude of reach —
measured three ways in memory `shorts-organic-research`. First-person is proof and is
fine: "I was 200 pounds at 38."

### 8. No em dashes in spoken text, and no other AI tells.

Full list in `/scriptfromoutline` — no self-answered rhetoricals, no coined
compounds, no aphorism triads, no Claude kicker lines. Don't duplicate that section
here, read it.

---

## Voice

Inherit the register from **`/scriptfromoutline`** — including its
**"BE CONTROVERSIAL. SWEAR."** section and the looksmaxxing-aligned framing of
attraction. Do not re-derive it.

**What's different at 55 seconds:**

- **No disclaimer beat, no scripture beat, no bio ritual.** There is no room and
  they are longform devices.
- **One blunt line per script is the target**, not three. "Useless while you're still
  soft" is the calibration.
- **Profanity is available but neither finished short uses it.** Don't force it into
  a listicle; save it for a script with a real peak.
- **Spoken numerals**: "Number one, the ab wheel." Not "1."

---

## B-roll cues

Bracketed, ALL CAPS label, placed on their own line **before** the words they cover.
Forms Dan has kept:

```
[COLD OPEN — no greeting, already talking, tight on Dan]
[B-ROLL: spiderman plank — footage exists, short4_spiderman-planks]
[B-ROLL: cable crunch — DOES NOT EXIST, use stock clip]
[SHOW DAN BEFORE PICTURE — 200 lb era, FACE. Full frame, not split-screen]
[AbsByAI.com mark on screen]
```

**Always state whether the asset exists.** Dan edits these cues himself — he changed
one from "needs filming Friday" to "use stock clip" — so the cue's job is to give him
a decision, not to hide the gap. Known library: ab-wheel longform, and cut footage of
toe touches (`short2_toe-touches`), V-sit twists (`short3_v-sit-twists`), spiderman
planks (`short4_spiderman-planks`), vacuums (`v3-short6_vacuum-exercises`), plus 33
installed exercise demo videos.

**If a script depends on an asset that may not exist, say so before writing it.** The
200 lb face photo is the live example — there is no true 200 lb shirtless photo, and
face shots need confirming.

---

## Delivery

1. **Show the script in chat first** with the word count and the runtime range. Dan
   edits in chat and in the doc.
2. Append it to the **DEDICATED SHORTS CONTENT** section of the current shoot's
   outline doc, below the last script and above nothing — the section ends with the
   ideas list.
   - Shoot 5 doc: `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`. **Confirm the
     current shoot's doc first; this changes per shoot.**
3. **Match the existing formatting**: an H3, bold, ALL CAPS title, then the script
   with bolded bracketed cues, closing with a `–` separator line.
4. The Drive MCP **cannot edit an existing Google Doc**. Use the osascript
   HTML-clipboard paste — full mechanics and every trap in **`/ad-outlines` →
   "Delivery into the Google Doc"**, plus the heading-paste trap and the
   internal-clipboard recovery in **`/scriptfromoutline`**. Screenshot immediately
   after pasting; never assume it landed.
5. **Re-read the doc through the Drive MCP immediately before pasting.** Dan types
   into this doc mid-session — he added an entire script and eight ideas while a
   session was running.
6. Verify by re-reading, and confirm his existing scripts are untouched.

---

## Checklist before delivering

- [ ] Word count is **176-180**, counted not estimated
- [ ] Opener is a direct claim or claim-plus-proof-promise, not a negation
- [ ] Structure statement's number matches the number of items actually listed
- [ ] Each numbered beat is 21-30 words
- [ ] There is one beat nobody else would say (three-item scripts only)
- [ ] There is a "remember" summary line before the close
- [ ] Close is "Comment and let me know [specific thing]"
- [ ] **The product is not spoken** (unless the idea itself is a product idea)
- [ ] `[AbsByAI.com mark on screen]` cue is present
- [ ] Zero em dashes in spoken text
- [ ] Every b-roll cue says whether the asset exists
- [ ] Any before/after cue says "full frame, not split-screen"
- [ ] Instagram send-cue alternate offered as a note beside the script, not in it

---

## Lessons log

**1 — 2026-08-25, the two founding scripts.** Dan's own "Top 5 Ab Exercises" draft ran
**345 words (1:33-1:45)**, nearly double. His "Looksmaxxes Your Face" draft ran
**181 words** and needed no cut at all — he gets the length right when the script has
three items and wrong when it has five. **A five-item list is the failure mode for
length.**

**2 — 2026-08-25.** He accepted every structural edit offered (merging two points into
one, trimming double scaling notes, adding a new insight beat) and reverted exactly
two things in each script: **the spoken product plug and the comment CTA.** Those two
are his and are now hard rules above. Everything between the opener and the close is
Claude's to shape.

**3 — 2026-08-25.** He also reverted a data-backed contrarian hook to his own plain
one. Recorded honestly: the measured evidence says a correction hook holds the first
three seconds better, and **Dan's preference wins anyway.** Offer the alternate as a
note if it's strong; don't put it in the script.

**4 — 2026-08-25, from the idea stage (`/shortsideas` batch 2).** Two things that
change how an idea arrives here and therefore how it gets scripted:

- **Some ideas arrive NESTED** — an argument or analogy bullet, then a nested
  "Here's why / Here's how" list (his "Why You Must Weigh Yourself Daily" and
  "3 Ways To Reduce Alcohol Consumption"). **When an idea is nested, the argument
  bullet becomes the opener and the proof beat; the nested list becomes the numbered
  beats.** Don't flatten it — the argument is why the video works.
- **His analogies come from money and status**, not from fitness: *"like trying to
  get rich while never looking at your bank account."* If an idea carries an analogy
  bullet, keep it in the script close to verbatim — it is the most quotable line
  he'll have.
- **A "Bottom line" bullet in the idea maps to the "remember" line in the skeleton**,
  and it usually lands on attraction: *"Bottom line is you must get lean if you want
  to look good and attract women."* Use it there rather than inventing a new summary.

**5 — 2026-08-25.** Name real foods, products and numbers in the script, never
categories. His own bullet reads *"hard boiled eggs, sardines, and chipotle protein
cups"* where Claude wrote "healthy snacks". Specificity is what separates his voice
from generic fitness content, and at 176 words there is no room for a vague beat.
