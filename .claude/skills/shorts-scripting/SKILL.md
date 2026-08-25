---
name: shorts-scripting
description: >
  Turn ONE dedicated shorts idea — a title plus bullets from /shortsideas, or a
  brief outline Dan writes himself — into a finished word-for-word teleprompter
  script with b-roll cues, built to Dan's measured 172-185 word spec, and deliver it
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

## THE SPEC — 172-185 spoken words

Measured off both of Dan's finished shorts: **177 words** and **176 words**. At his
measured 198-222 wpm that is **48-54 seconds**, which sits under YouTube's
60-second music-licence cliff and inside Instagram's best reach bucket (30-60s).

**Write to 172-185. Count the words before delivering — do not estimate.**

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
| 3 | **Structure statement** | 11-12 | "…improves your face in three ways." Tell them what's coming — **ONLY when the opener does not already name the number.** If the opener says "the three most important supplements," this beat is dead weight and Dan will delete it. See lesson 4. |
| 4 | **The numbered beats** | **21-30 each** | "Number one, the ab wheel." / "First, it defines your jawline." Name + one reason + one qualifier or scaling note. |
| 5 | **The beat nobody else says** | ~25 | The insight that isn't on the list — **and it must be about the VIEWER, not about a third party.** Interesting-but-not-personal gets deleted. See lesson 8. Only fits when there are three items, not five. |
| 6 | **The "remember" line** | 19-40 | A reframe **plus a concrete instruction with a progression.** Dan expanded this beat both times Claude wrote it as a single aphorism. See lesson 5. |
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

### 2. The close is a COMMENT ask by default — but it is not a law. Three forms.

Claude rewrote the comment CTA twice in the first two scripts, with a defensible
argument both times, and **Dan reverted it both times.** So the default stands. But
across five more scripts he then used all three of these, and **twice removed the
comment ask entirely.** Pick the form by what the script is:

| Form | Use it when | His example |
|---|---|---|
| **Comment ask** (default) | the script teaches a fact or a frame | *"Comment and let me know which ab exercise is your favorite."* |
| **Do-it-then-comment** | the script taught something he can do today | *"Try the vacuum, and leave a comment to let me know how it worked for you."* |
| **Subscribe** | the script's subject IS the channel's premise | *"Subscribe to the channel now for more tips on how to use AI to get in shape."* — preceded by a positioning line: *"on my channel, I show you exactly how to use AI tools to lose your belly fat and get defined six pack abs."* |

**And sometimes there is no CTA at all.** He ended the body-fat script on pure
conviction — *"You'll thank me once you do."* — deleting both the comment ask and the
`AbsByAI.com` cue. **When the script ends on a strong contrarian instruction, the
instruction IS the close.** Do not staple a CTA onto it.

**When you do use the comment ask, ask for a POSITION, not a report.** Claude wrote
*"Comment and let me know which one you would take."*; Dan sharpened it to **"Comment
and let me know if you think six pack abs are worth a million dollars."** A question
people will argue about beats a question people will answer.

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

- [ ] Word count is **172-185**, counted not estimated
- [ ] Opener is a direct claim or claim-plus-proof-promise, not a negation
- [ ] Structure statement's number matches the number of items actually listed
- [ ] Each numbered beat is 21-30 words
- [ ] The "nobody else says" beat is about the VIEWER's own body/life, not a third party (lesson 8)
- [ ] Consequence to the viewer comes BEFORE the mechanism, and there is at most one piece of anatomical jargon (lesson 10)
- [ ] Any b-roll that must be filmed has a `[FILM ... BEFORE STARTING]` line at the top of the script (lesson 9)
- [ ] The "remember" beat carries an actionable instruction, not just a reframe (lesson 5)
- [ ] No clever aphorism where a concrete list of nouns would do (lesson 6)
- [ ] Close matches the script type per rule 2 (comment ask / do-it-then-comment / subscribe / conviction-only) and any comment ask invites a POSITION
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

**4 — 2026-08-25, the supplements short. Dan deleted the structure beat outright.**
Claude wrote *"I take about fifteen things. These three do seventy percent of the
work."* as beat 3, with its own b-roll cue. He cut both. **His opener already said
"the three most important supplements for men," so the setup line restated a number
the viewer had just heard.** The skeleton's beat 3 is conditional, not mandatory: it
earns its place only when the opener is a claim that does NOT carry the count (the
face script's *"improves your face in three ways"* is the case where it does earn it,
because the opener there was a proof promise). **When the title is a numbered list and
the opener speaks the title, go straight from the opener into item one.**

**5 — 2026-08-25. The "remember" beat is an INSTRUCTION, not just a reframe.**
Claude wrote a single aphoristic sentence: *"two supplements you take every single day
beat a shelf of ten you take when you remember."* Dan kept the contrast, fixed the
number to match the video's three, and **added a whole second sentence telling the
viewer what to actually do, with a progression**: *"Hit your big three supplements
daily if you're just starting off, and add in more later once you get consistent."*
He also dropped *"And always remember"* to plain *"Remember,"*. This is now the
pattern — **reframe, then a concrete next step with a path forward.** It is the one
beat allowed to run long (his version is ~40 words); the word budget comes from beat 3
being deleted.

**6 — 2026-08-25. He trades clever lines for concrete nouns.**
Beat 5 shipped as *"Worth taking, but they will never save a bad diet."* He rewrote it
to *"Worth taking, but your nutrition, training, and sleep are all far more
important."* Same point, no epigram, three named things instead of one flourish. This
is the same instinct behind the AI-tells ban in `/scriptfromoutline` — **a rhetorical
line reads as written; a list of nouns reads as spoken.** When a beat is about
relative importance, name the things that matter more.

**7 — 2026-08-25. The real ceiling is ~185 spoken words, not 180.**
His edited supplements script measures **184 words (50-56 s)** and he made it longer,
not shorter, than what was delivered. 176-185 is the band. Still count, never estimate,
and still stay under 60 s finished.

**8 — 2026-08-25, the vacuum short. THE "NOBODY ELSE SAYS" BEAT MUST BE ABOUT THE
VIEWER.** Claude wrote a beat on bodybuilders getting bubble gut from heavy gear and
using vacuums to fix it — taken straight from Dan's own longform, factually his, and
genuinely the thing no other vacuum video says. **He deleted the whole beat**, and gave
the reason in his own words: *"in the short format, we have got to keep it to what they
personally care about. That's not really relevant to the viewer."* At 50 seconds there
is no room for an interesting aside about someone else's body. **Test every beat: does
this change what the guy watching does with HIS OWN body today?** If it is trivia,
context, or a story about a third party, cut it — no matter how good it is. This is
the sharpest difference between a short and a longform, where that same beat would
earn its place.

**9 — 2026-08-25. B-roll that needs filming gets a FILM-THIS line at the top of the
script.** Claude flagged in chat that the vacuum footage existed but was cut 9:16.
Dan put the instruction into the document instead, as an unbolded bracket line above
everything else: `[FILM NEW VACCUUM B ROLL IN 16:9 BEFORE STARTING]`. **A shoot
prerequisite belongs in the script, not in the chat message that gets lost.** Put it
as the first line, before the opening cue.

**10 — 2026-08-25. Consequence first, mechanism second — and one jargon word maximum.**
Claude opened the teaching with anatomy: *"Crunches and toe touches train your rectus
abdominis. That is your six pack, and it sits on the surface. The vacuum trains your
transverse abdominis, a sleeve of muscle on the inside that pulls your whole waist in
tight."* Dan rewrote it to lead with what it does to the viewer: *"Regular ab exercises
make your abs look better - if you're already lean. But if you have belly fat, they
just make your belly bulge out more. The vacuum is the only ab exercise that can
actually shrink your waist. It does this by training your transverse abdominus, the
sleeve of muscle that stabilizes your core."* Note what happened: **"rectus abdominis"
is gone entirely** (the viewer already calls that "abs"), the bad outcome lands before
any anatomy, and the one surviving Latin term got a shorter, plainer gloss. **Name the
muscle only when the viewer cannot already name it, and never open a beat on anatomy.**

**11 — 2026-08-25. He opened the short on B-ROLL, not on his face, using "THIS".**
Claude's `[COLD OPEN — tight on Dan]` was replaced with the vacuum b-roll, and the
opener became *"THIS is the only ab exercise that actually shrinks your stomach."* —
deictic, pointing at what is already on screen. **When the subject of the short is a
visible thing (an exercise, a food, a product, a photo), open on the thing and let the
first word point at it.** Cold-open-on-Dan is for shorts whose subject is an idea.

**12 — 2026-08-25. When the short teaches an ACTION, the close commands it first.**
Rule 2's form still holds, but it gained a variant. Claude wrote *"Comment and let me
know how long you can hold a vacuum."* Dan rewrote it to **"Try the vacuum, and leave a
comment to let me know how it worked for you."** The ask is the same; it is now
preceded by a do-this-today instruction. Use this form whenever the script has taught
something the viewer can do the same day. Keep the plain form for shorts that teach a
fact or a frame.

**13 — 2026-08-25, recorded but NOT yet a rule.** He removed the
`[AbsByAI.com mark on screen]` cue from the vacuum script, while keeping it in the
supplements script one section above. One instance is not a pattern — keep including
the cue, and if he deletes it a second time, drop it from the checklist.

**14 — 2026-08-25. The form cue in a how-to beat is his, not Claude's.** He inserted
*"and consciously slump. Then consciously posture,"* into the vacuum instructions. That
is a coaching detail no amount of research produces. **Write the how-to beat lean and
correct, and expect him to add the cue that makes it his.** Do not pad it with invented
technique.

**15 — 2026-08-25, the millionaire script. PUT DAN'S OWN STANDING IN THE OPENER WHEN HE
HAS IT.** Claude opened with the bare claim: *"Having a six pack is better than being a
fat millionaire."* Dan added the thing only he can say: **"I'm a multi-millionaire with
six pack abs, and I know having abs is way more important."** He has actually been both,
and that sentence is the entire reason to keep watching. **Before writing any opener,
ask what Dan personally has that makes him the one man who can make this claim** — he
was 200 lbs at 38, he got abs at 40, he is a multi-millionaire, he trains jiu-jitsu in
his forties, he has taken Zepbound. First-person proof is always allowed and is not the
same as the banned second-person age reference (rule 7).

**16 — 2026-08-25. Replace abstraction with the concrete sequence of events.** Claude's
dating beat was a nicely-turned abstraction: *"Your income is something you claim. Your
body is something she can verify in half a second."* Dan replaced it with what actually
happens, in order: **"everyone meets on dating apps and Instagram now. If you have abs,
you'll get limitless matches and women in your DMs. But if you're a fat millionaire,
every attractive woman will swipe left on you. None of them will ever find out about
your money or success."** Same idea, but it plays as a scene the viewer recognises
rather than a maxim. **If a beat could be printed on a poster, rewrite it as a
sequence.** This is the third separate time he has deleted an epigram (see lessons 2
and 8) — Claude keeps reaching for them and he keeps cutting them.

**17 — 2026-08-25. "Remember," is optional; the INSTRUCTION is not.** He deleted the
word from two of three scripts while keeping the instruction that followed it. The beat
is a summary plus a concrete thing to do — the opening word is not part of the spec.

**18 — 2026-08-25. THE CONTROVERSY IS A POSITION, NOT A SWEAR WORD.** `/scriptfromoutline`
requires profanity and a mainstream-angering beat, and Claude imported that literally,
writing *"here is the part that should piss you off."* **Dan cut the profanity** — and
then, in the same batch, wrote the most aggressive beat of the seven scripts himself,
with no swearing in it: *"Ninety percent of guys bulking would be better off cutting and
getting lean. You'll look so much better with abs than with a powerlifter 'fat but
strong' build."* **Across seven finished shorts he has used profanity zero times.**
At 50 seconds the controversial beat is a contrarian OPINION that picks a fight with a
real training camp, not a swear. Take the fight; leave the profanity in the longforms.

**19 — 2026-08-25. He writes spoken emphasis as a single ALL-CAPS word.** *"WAY better
than being a millionaire"*, *"you'll actually look BIGGER"*, *"THIS is the only ab
exercise"*. One per script or so. Use it — it is a teleprompter instruction to hit that
word, and Claude's scripts read flat without it.

**20 — 2026-08-25. His aside marker is " - ", a spaced hyphen, never an em dash.**
*"Listen - it takes decades to become a millionaire."* *"AI is an incredibly powerful
tool for getting abs - if you use it the right way."* The em-dash ban (rule 8) is about
AI tells; the spaced hyphen is the form he actually types, so write asides that way.

**21 — 2026-08-25. Stat requests come back as a bracketed CLAUDE instruction in
italics.** He wrote the beat with `X%` placeholders and an all-caps italic line beneath
it: *"CLAUDE - CHANGE TO PERCENTAGE OF MALE POPULATION 20-50 WITH SIX PACK ABS, AND
PERCENTAGE WITH NET WORTH OVER $1M. GET AS CLOSE TO THIS AS YOU CAN IF YOU CAN'T FIND
THIS EXACT STAT."* **Fill the numbers in, then delete the instruction line.** Do not
invent a precise figure to fill a placeholder — his own fallback wording ("get as close
as you can") is the licence to widen the population and say so. Numbers found for this
one, for reuse: **Federal Reserve SCF millionaire households by age — under 35: 2.1%,
35-44: 10.4%, 45-54: 20.6%**, which blends to roughly **8% under fifty**; **visible
six-pack abs: 1-2% of men**, which is a soft consumer-fitness figure with no primary
source, so it ships as *"fewer than two percent."*

**22 — 2026-08-25. NEVER MAKE THE VIEWER THE TARGET OF THE ATTACK.** This is the
boundary lesson 18 was missing. Claude wrote, in the make-time script: *"And here is the
truth nobody wants. You are NOT too busy. You watched an hour of TV last night. You are
just not convinced it matters yet."* **Dan kept "You're not too busy" and deleted every
word of the accusation.** Look at what survives across seven scripts: the fitness
industry gets attacked, guys who bulk get attacked, supplement sellers get attacked,
people who call medication cheating get attacked. **The man watching never does.** He is
the ally being let in on something. Aim the contrarian beat at an industry, a camp, or
an idea — never at the viewer's character or his last twenty-four hours.

**23 — 2026-08-25. NEVER PRE-EMPT AN OBJECTION.** Claude ended the Zepbound script by
answering the critics: *"And people love to argue about whether this is cheating. I am
not interested in that debate. I lost the weight..."* **Dan cut it entirely** and put a
plain personal commitment in its place: *"That's why I take Zepbound even though I
already have six pack abs, and why I plan on remaining on Zepbound the rest of my
life."* Raising an objection inside the video is what gives it oxygen. **State the
position; let the comments carry the fight.**

**24 — 2026-08-25. The opener's SECOND sentence is one of two things, and the claim
decides which.** Lesson 15 said to lead with Dan's standing. That is right when the
claim needs authority to be believed ("abs beat money" — he is a multi-millionaire with
abs). But on the make-time script he **deleted** Claude's credential line ("I lift seven
days a week and train jiu jitsu three times a week, and I run a company") and wrote a
**who-this-is-for plus promise** instead: *"If you want to get in shape but you're 'too
busy' to work out, this video is the solution you need."* **Authority claim ⇒ his
standing. How-to ⇒ name the guy who needs this and promise him the payoff.**

**25 — 2026-08-25. Do the arithmetic out loud.** Claude wrote the commute cost as a
rhetorical list: *"The gym is not forty five minutes. It is forty five minutes plus the
drive, plus the parking, plus finding a bench."* Dan replaced it with an actual sum:
**"If you're doing a short 30 minute workout, driving 15 minutes back and forth to the
gym DOUBLES your workout time."** Same for the session-length beat: *"Fifteen minutes
daily beats two hours three times a week."* **Numbers that multiply into an obvious
conclusion, not a pile of clauses.**

**26 — 2026-08-25. Speak to segments by name.** His AI beat: *"If you're in school, use
AI to do all your homework. If you're working a white collar job, use AI to accomplish
more in less time. You can even use AI to handle personal tasks like making reservations
at restaurants, or researching what gym to sign up for."* Claude's version had been one
narrow use case. **Name two or three concrete kinds of viewer and give each one its own
example.**

**27 — 2026-08-25. The personal-failure-then-solution beat.** He added to the sleep
point: *"I tried everything to stop eating late for years, but I was never able to
consistently do it. Zepbound was the only way I was able to stop."* **Where Dan failed
at something for years before it worked, say so** — it is more persuasive than the
benefit stated flat, and only he can supply it.

**28 — 2026-08-25. The instruction beat is a STAGED plan, not a single order.** *"Just
start with a 15 minute home workout every morning. Then over the next few weeks, figure
out how to use AI to reclaim more time."* Step one is small enough to do tomorrow; step
two is where it goes. Same shape as his supplements close (big three daily, add more
once consistent).

**29 — 2026-08-25. THE EPIGRAM BAN, FIFTH AND SIXTH KILLS. Stop writing them.** *"a
daily thing is a habit and a weekly thing is an appointment you cancel"* → his: *"You
can consistently do fifteen minute home workouts every day. But two hour long workouts
end up getting skipped."* And *"The same noise that makes you want a second plate makes
you want a third drink."* → his: *"Just like Zepbound takes away your desire for junk
food, it reduces your desire for alcohol too."* **The fix is always the same: split the
epigram into two plain sentences that say the thing literally.** Note the asymmetry —
**he kills Claude's epigrams and keeps his own** (the bank-account analogy in the
weigh-yourself idea is his and should be used verbatim). Write his; never invent one.

**30 — 2026-08-25. HIS EDIT PASS PUSHES SCRIPTS OVER THE 60-SECOND CEILING — RE-COUNT
AFTER HE EDITS.** He adds concrete detail and does not count words. His edited
make-time script came back at **228 words (62-69 s)** and the Zepbound one at **198
(54-60 s)**. Anything over ~200 words is over a minute, and **a YouTube Short between
1:00 and 3:00 carrying any Content ID claim is blocked globally** (see
`AI_COORDINATION.md`). **Always re-count after his pass and flag an over-length script
with specific proposed cuts** — do not silently rewrite his prose, and do not let it
ship long either.

**31 — 2026-08-25. Script 4 came back with ZERO edits — that shape is the model.**
"I was 200 pounds at 38" survived untouched: open on the before photo with THIS, one
beat naming what he already knew, one beat attacking the industry, one beat on what
actually worked, a three-fragment hammer (*"Not a program. Not a trainer. A picture."*),
instruction, comment ask. When a new idea is a personal-story short, build it in that
order.
