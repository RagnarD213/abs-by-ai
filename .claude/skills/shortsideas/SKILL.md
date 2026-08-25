---
name: shortsideas
description: >
  Brainstorm a batch of DEDICATED short-form video ideas (YouTube Shorts / IG Reels)
  in Dan's own idea format — a Title Case title plus 2-4 concrete content bullets —
  and add the survivors to the "Ideas for shorts to write out" list at the bottom of
  the current shoot's outline doc. Use whenever Dan asks for shorts ideas, shorts
  topics, "what shorts should I film", more ideas like the ones he wrote, or ideas
  for the next shoot — even if he doesn't say "/shortsideas". For turning a chosen
  idea into a word-for-word script use /scriptfromoutline; for AD ideas and ad
  outlines use /ad-outlines; for cutting shorts out of an existing longform use
  /shorts.
---

# Shorts ideas: generate ideas in Dan's format, not in Claude's

**STATUS: v1 — created 2026-08-25 from the diff between a 20-idea batch Claude
delivered and the 8 ideas Dan actually chose to keep. Dan's verdict on the batch:
"mostly I think they're pretty bad." He kept 4 in altered form, wrote 4 himself, and
killed 12. This skill exists to close that gap.**

## The job

Dan is filming dedicated short-form content (not cutdowns of longforms). He needs a
list of ideas he can hand to `/scriptfromoutline` one at a time. The deliverable is
**a batch of titles with content bullets**, shown in chat for him to kill, then the
survivors appended to the **"Ideas for shorts to write out"** list at the bottom of
the current shoot's outline doc.

**This skill produces IDEAS, not scripts.** Stop at the idea. Writing the script is a
separate session and a separate skill — that separation is deliberate and saves Dan
tokens and context.

---

## THE TITLE IS THE DELIVERABLE

Claude's first batch delivered **spoken hook sentences** in Dan's voice
("Stand up right now. If you can't hold this for thirty seconds…"). Dan converted
every single survivor into a **Title Case title**. Not one hook-shaped line survived
as written except the one he took verbatim.

**Write titles. Title Case. The kind of thing someone could type into YouTube search.**

The hook is a scripting decision and belongs to `/scriptfromoutline`. An idea that
only exists as a hook is an idea Dan cannot file, reorder, or hand to an editor.

### The shape of exactly one idea

```
  - The 3 Most Important Supplements For Men

  - 3 Unexpected Ways Zepbound Helped Me
      - Reduced my alcohol consumption
      - Made me more productive at work
      - Made me sleep better (due to less late night eating)

  - What Every Body Fat Percentage Looks Like
      - Similar to: <https://www.youtube.com/shorts/dWLK29sX4Pc>
```

- **Title, Title Case, on its own bullet.**
- **2-4 sub-bullets underneath, and they must be the actual content**, not a
  description of the content. "Reduced my alcohol consumption" is a beat.
  "Discuss the unexpected benefits" is not.
- **A title with no list behind it takes no sub-bullets.** Don't manufacture them.
- **Attach a comp link when a real measured one exists** — Dan used the exact
  YouTube Short link he was given, in the form `Similar to: <url>`. Never invent a
  link; only use one that has been verified live.

---

## The 2026-08-25 batch review — what he changed, and why

This table is the whole lesson. Read it before writing anything.

| Claude wrote | Dan wrote | Rule extracted |
|---|---|---|
| "Money changed how people treated me. Abs changed it more." | **Why Having Abs Is Better Than Being A Fat Millionaire** (+ more rare / attracts more women on dating apps / money does you no good if you're dead) | Name a **villain or a rival person**, not an abstraction. "A fat millionaire" is a guy you can picture. "Money" is not. |
| "This is what 15% body fat actually looks like." | **What Every Body Fat Percentage Looks Like** | Widen the scope and make it **searchable**. One number is a moment; the whole scale is a video someone looks for. |
| "I took Zepbound. Here's the part nobody selling it will tell you." | **3 Unexpected Ways Zepbound Helped Me** | **Countable + specific + a curiosity word.** "Unexpected" earns its place because the three items genuinely are. |
| "Watch AI count the calories in my lunch in 4 seconds." | *killed* — folded in as one bullet of **Top 3 Ways To Use AI To Get Abs** | **The product is one item in a list of three. Never the subject of the video.** A demo is an ad; a list containing a demo is content. |
| "I was 200 pounds at 38. The thing that fixed it wasn't a workout." | **kept verbatim**, + "motivation was the key and the AI image gave me motivation" | The one sentence-shaped title he accepted. A first-person confession with a withheld answer survives. Use this shape **sparingly — roughly one per batch.** |
| "Stop weighing your food. Take a picture of it." · "Stop doing sit-ups." · "If you're doing cardio to lose your gut, you picked the slowest tool." | **all killed** | See the kill list below. |
| "Stand up right now…" · "Look down…" · "Pinch right here…" | **all killed** | See the kill list below. |
| — | **The 3 Most Important Supplements For Men** | Plain, evergreen, searchable. A boring title on a topic he has real opinions about beats a clever title on a generic one. |
| — | **The Only Ab Exercise That Shrinks Your Belly Fat (The Vacuum)** | **Absolute claim + the payload named in parentheses.** The parenthetical is not a spoiler; it's the proof the video has a real answer. |
| — | **How To Make Time To Work Out** | Title the **objection**, not the tactic. "How to make time" is what the viewer says to himself; "do short daily workouts" is only the answer. |

---

## The kill list — these died 100% and must not be regenerated

**1. "Stop doing X" corrections.** Every one was killed, despite corrections being
the highest-volume winning shape in the measured YouTube data. They are commodity
fitness-creator content, they carry none of Dan's brand, and they are about the
viewer's mistake rather than about anything Dan knows. If a correction idea is
genuinely strong, **re-title it as a superlative or a list** — "The Only Ab Exercise
That…" is a correction wearing the right clothes.

**2. Self-tests** ("stand up and try this", "look down", "pinch here"). All three
killed. They measure well on other channels; they are not how Dan talks.

**3. Bare product demos.** See the AI-calorie-counting row above. The rule is
absolute: the app appears **inside** a list, never as the title's subject.

**4. Conversational, unsearchable titles.** "Nobody tells you the first month of
getting lean makes you look worse" is a fine *line* and a bad *title*.

**5. Anything whose only content is that Dan is in shape.** Standing rule, predates
this skill. The viewer must walk away with a tactic, an opinion, or a correction —
never just "Dan looks good."

---

## Dan's topic territory

Every idea he kept sits in one of these. **Ideas outside this list have a much lower
hit rate — generate them only when he asks to widen.**

| Territory | What he actually has |
|---|---|
| Supplements | The supplements longform; strong, specific opinions; the app's Supplement Audit |
| Ab exercises | The ab-wheel longform, plus cut footage of toe touches, V-sit twists, spiderman planks, vacuums, and 33 installed exercise demos |
| Status, attraction, dating | His real register — looksmaxxing / red-pill framing of attraction. Highest-ceiling territory in the measured data (a status Short did 11M) |
| Body-fat calibration | **The uncontested lane.** The app generates the picture; competitors hold up borrowed photos and do 4-5M |
| AI and the app | Generation, macro-tracking from a photo, AI trainer, nutritionist, sleep coach, supplement audit |
| His own transformation | 200 lbs at 38, real abs at 40, the AI goal image as the motivation trigger |
| Time and busy-guy constraints | Home workouts, short daily sessions, automating life with AI |
| Zepbound / GLP-1 | He is on it and honest about it. **Naming the drug organically is fine** — a rival channel did 503K on "Most Adults Should Take Tirzepatide". The no-drug-names rule is an **ad-compliance** rule only |

---

## Title mechanics that work

- **Numbers in the title whenever there's a list.** "The 3 Most Important…",
  "Top 3 Ways…", "3 Unexpected Ways…". Three, not five, not ten.
- **Superlatives and absolutes are welcome, not hedged.** "The Only", "Every",
  "Most Important", "Better Than". Dan's brand tolerates a strong claim; it does not
  tolerate a mealy one.
- **A curiosity qualifier only when it's true.** "Unexpected" works because the three
  Zepbound items really are surprising. Don't staple it onto an ordinary list.
- **"For Men" is a fine qualifier. Second-person age is not.** "The 3 Most Important
  Supplements For Men" — good. "…For Men Over 40" — costs 1-2 orders of magnitude of
  reach (measured three separate ways; see memory `shorts-organic-research`).
  First-person age is proof and is fine: "I was 200 pounds at 38" survived.
- **Parenthetical payload.** "(The Vacuum)" tells the viewer the video has a real,
  specific answer.

---

## Constraints every idea has to survive

These come from the measured research (memory `shorts-organic-research`) and from
Dan's standing rules. An idea that can't be made inside them is not an idea.

1. **It has to fit 165-205 spoken words** — that's 45-58 seconds at Dan's measured
   198-222 wpm, and it keeps the Short under YouTube's 60-second music-licence cliff.
   If a title needs five items explained, it's two ideas, not one.
2. **Sequential reveals only.** Before-then-after is fine; a side-by-side before/after
   in one frame is banned.
3. **No follow-along workouts.** Dan's own account data: 1.8-2.0s average watch time.
4. **Say what asset it needs** if it isn't obvious, and flag anything that has to be
   filmed versus anything that can be built from footage already in the library.
5. **Be willing to be controversial.** Dan's standing writing rule — at least some of
   a batch should say something the mainstream would object to. Bland ideas are the
   named failure mode.

---

## Batch size and self-filtering

Default to **12 ideas, not 20.** The 20-idea batch had a ~20% hit rate and Dan wrote
half the survivors himself. Fewer, better, all in his format.

**Before showing him anything, run each idea against this and delete failures — do
not deliver them with a caveat:**

- [ ] Is it a Title Case title someone could type into YouTube search?
- [ ] Does it have 2-4 sub-bullets that are real content beats (or legitimately none)?
- [ ] Is it inside Dan's topic territory?
- [ ] Is it a "stop doing X", a self-test, or a bare product demo? → **delete**
- [ ] Does it fit in 165-205 spoken words?
- [ ] If it's a comparison, is the other side a **person**?
- [ ] If the app appears, is it one of three items rather than the subject?
- [ ] Would Dan, who has been fat and is now lean at 40, have a real opinion about
      this — or is it generic fitness instruction anyone could give?

The last box is the one that killed most of batch 1.

---

## Delivery

**Show the batch in chat first.** Dan triages by killing, and he will rewrite some
titles himself — that rewriting is the most valuable feedback this skill gets, so
capture it in the Lessons log below.

Then append the survivors to the **"Ideas for shorts to write out"** bulleted list at
the bottom of the current shoot's outline doc.

- Shoot 5 doc: `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`
  ("Abs By AI Shoot 5 Outlines"). **Confirm the current shoot's doc before writing —
  this changes per shoot.**
- **The Drive MCP cannot edit an existing Google Doc.** Delivery goes through Dan's
  logged-in Chrome via the osascript HTML-clipboard paste. The full mechanics and
  every trap are documented in **`/ad-outlines` → "Delivery into the Google Doc"** —
  read that section rather than re-deriving it. The load-bearing points: write the
  bullets as an HTML file, set the macOS clipboard to the **HTML flavor** with
  `osascript`, verify with `clipboard info`, click the target line, `cmd+Right`,
  `Return`, `cmd+v`, then screenshot immediately — never assume the paste landed.
- **Re-read the doc through the Drive MCP right before pasting.** Dan types his own
  ideas into this list mid-session, and a stale copy will clobber them. This has
  already happened once on this doc.
- **Verify** by re-reading the doc and confirming his existing ideas are unchanged.

---

## Lessons log

Append what Dan changes, every batch. His edits are the calibration.

**1 — 2026-08-25, batch 1 (20 ideas, ~20% kept).** Dan: *"mostly I think they're
pretty bad."* The ideas were not wrong about the market — they were measured against
real YouTube performance and several had 5-11M comps. They were wrong about **him**:
delivered as spoken hooks instead of titles, heavy on correction and self-test shapes
he doesn't use, and one was a bare product demo. The four he kept, he retitled. The
four he added himself were plainer, more searchable, and more opinionated than
anything in the batch. **Being right about the algorithm is not the same as being
right for Dan's brand — when the two conflict, his format wins and the algorithm
lesson gets re-expressed inside it.**

**2 — 2026-08-25.** He accepted the measured comp link verbatim
(`Similar to: <youtube.com/shorts/dWLK29sX4Pc>`). Comps are wanted; they just have to
be real and verified live.
