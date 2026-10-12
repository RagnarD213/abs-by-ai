---
name: reaction-clips
description: >
  Find clips for Dan's green screen REACTION shorts and deliver them as a review page where every clip
  plays inside the page, cued to the second he reacts to. A clip must grab attention or be
  controversial, come from a big influencer or a celebrity where possible, run under 15 seconds
  (25 at the most), and carry a lesson Dan teaches, so the viewer has a reason to watch his reaction.
  Use whenever Dan asks for reaction video ideas, clips to react to, "more reactions like the Bill
  Maher one", a new round of reaction clips, or a review page of clips for a shoot, even if he doesn't
  say "/reaction-clips". Ordinary (non-reaction) shorts ideas are /shortsideas. Writing the script for
  a chosen reaction is /shorts-scripting. The filming list of clips for shoot day is the "Reaction clip
  list" step in /teleprompterscripts.
---

> **Shared writing rules:** before writing a card, read `.claude/skills/_shared/WRITING-RULES.md` and
> `.claude/skills/_shared/HOOKS.md`. Memory: `reaction-clip-criteria`. No em dashes, anywhere.

# Reaction clips: pick the clip by Dan's rules, show it cued to the second

**STATUS: v1, 2026-10-12.** Built from two rounds for the 10/17 shoot. Round 1 was chosen for topic fit: 7 of
20 kept. Round 2 was chosen by the rules below: 8 of 20 kept, and Dan called it "substantially better". The
goal is a round where he keeps most of them.

## Related records, read them before a round

- **`/teleprompterscripts`, "What Dan killed after watching the 10/17 reaction clips, and what he kept":** the same
  day, in another task, Dan watched the 30 clips already scripted for that shoot and killed 18. His reasons there
  ("too boring", "no good lesson I can pull out of it", "not relevant to us") match the rules below. Read that list
  with the lessons log at the bottom of this file. Never re-offer something on either kill list.
- **`_shared/WRITING-RULES.md`, section 4, and memory `reaction-videos-clips-first`:** clips first. Dan watches a
  clip before any script is written around it. This skill is how that rule is carried out.
- `teleprompterscripts/reference/reaction_clips_page.py` builds a page of the clips ALREADY in a shoot doc, with
  alternates, from the doc's `[PLAY CLIP]` cues. This skill's `page.py` is for NEW ideas. Do not merge them.

## What this skill delivers

A batch of reaction short IDEAS (default 20). For each one: the clip, cued to the second, and the outline of
Dan's reaction. They go on one review page with a working YouTube player per clip. Dan kills what he does not
want. The keeps are saved as data and handed to a separate scripting task.

**This skill stops at the idea.** It does not write scripts, and it does not touch the shoot doc. Dan runs
scripting as its own task (memory `skill-creation-no-auto-execute`, and his 2026-10-12 instruction).

## Dan's rules for a clip (2026-10-12, his words where quoted)

Filter in this order. A clip that fails 1, 2 or 3 is dead no matter how good the topic is.

1. **It grabs attention in its first seconds.** "If we put this person to sleep with the clip that we're
   reacting to, they'll never even see me talk." Start the clip ON the punch line. Never on a wind-up, a
   greeting or a host's question.
2. **There is a good lesson in it.** "There's got to be a valuable lesson I get across in the short." The
   viewer must have a reason to watch Dan's reaction, and Dan must be teaching, "not just in the background
   while the video plays". Write the lesson on the card before you keep the clip. No lesson, no card.
3. **Attention-getting or controversial.** The person takes a hard position. A clip where someone says
   "somewhat good, somewhat bad" is dead: "he's not really saying anything."
4. **Ideally a big influencer or a celebrity**, so Dan piggybacks on a name people already search for. A
   smaller creator passes only when the clip is highly relevant, attention-getting and has a great lesson
   (Dr. Mike Israetel calling tirzepatide a dial passed on that basis).
5. **Ideally under 15 seconds. Never over 25.** `page.py` refuses a clip over 25 and lists every clip over 15.
6. **Obviously a fitness topic.** If a viewer would think "why is a fitness guy reacting to this?", drop it.
7. **About the average guy's problem,** not Dan's, and nothing dated.

**Benchmark: Bill Maher, "fat shaming needs to make a comeback".** Dan: "This was the best one you chose...
attention-getting, from a known celebrity, controversial. I want more like this."

## Start from the lesson, then find the clip

Every keeper so far paired a famous person's hard line with something Dan already teaches. So build the list
from both ends: a lesson Dan has on record, and a big name saying something loud about it.

Lessons Dan has on record (check `Docs/memory/dan-personal-facts-for-scripts.md` and the current shoot doc
before using one, and never invent a habit or a number; a gap is marked `[DAN: ...]` on the card):

| lesson | his fact |
|---|---|
| Weigh yourself every morning | like getting rich without looking at your bank account; catch fat gain early |
| Look at yourself: mirror, weekly photo | you stop seeing your own belly |
| Zero liquid calories | drank coconut water for years, now zero calorie electrolyte powder; black cold brew |
| Swap carb snacks for protein | chips, trail mix, dried fruit out; hard boiled eggs, sardines, Chipotle protein cups in |
| Fast until 2 PM | salad at 2, big meal by 6, small meal by 9, the last meal the smallest |
| Zepbound is a dial | 192 to 175 in 3 months; 1.5 mg a week; up to 2.5 and fewer calories if he gains; on it for life |
| Abs are a body fat number | upper abs show around 15%; at 200 pounds he was about 28% |
| The vacuum | the deep muscle that pulls your waist in; one 20 second hold |
| Train hard, briefly, every day | 7 days a week at 8 AM; 1 warm-up set, 2 hard sets; 5 minutes beats an hour you skip |
| Looks come from being lean | "having abs beats being a fat millionaire" |
| Check it with AI first | anything on social media that sounds too good to be true |

Where to look for the big name: Real Time with Bill Maher monologues, Joe Rogan clips (JRE Clips, PowerfulJRE),
late night and morning show interviews with actors about their bodies, comedians on fat and fitness, athletes'
viral moments, the biggest fitness channels (Renaissance Periodization, Jeff Nippard, Chris Bumstead), Alex
Hormozi, viral ads and news reports about fitness products and trends. Dan likes Hormozi and Planet Fitness as
targets and has not yet had a clip of either he loved.

## The process

1. **Read what is taken.** The current shoot doc's reaction sections, and the Reaction Clips document for that
   shoot (ids in `Docs/SHOOT_<date>_DOCS.md`). Never repeat a clip or a lesson already scripted.
2. **Search.** `python3 reference/yt.py s "query" 6` prints id, length, views, channel and title. Run a dozen
   queries per call. Prefer uploads from the show's own channel with real view counts.
3. **Find the second.** `python3 reference/yt.py t ID "regex" 1` prints the captions with times. When it
   answers NO TRANSCRIPT on a video that has speech, YouTube is rate-limiting (see Traps): open the video in the
   built-in browser and run `reference/transcript_panel.js`. For a clip that is a picture, not a speech (an ad,
   a viral moment), seek the video in the browser and take a screenshot, and say "check by eye" on the card.
4. **Cut it.** Start on the first word of the punch line and end on the last word of the point. If the setup and
   the payoff are far apart, use two or three pieces (`segs`), and keep the total inside the limit.
5. **Write the card:** title, verdict, the clip line, what it is, and Dan's reaction as bullets: Hook, My take,
   Lesson, Bottom line. Title format: who it is, what they say, then "He's Right." or "He's Wrong." The hook
   names the person and the surprising thing in about 15 words (`_shared/HOOKS.md`).
6. **Self-filter before Dan sees anything.** Delete, do not caveat:
   - [ ] Would a stranger stop scrolling in the clip's first 3 seconds?
   - [ ] Does the viewer know the name, or is the line strong enough without it?
   - [ ] Is the lesson something the viewer can do tomorrow, and is it Dan's own?
   - [ ] Is it the same lesson as another card in the batch or a short already scripted? Keep the better clip.
   - [ ] More than two cards from one video? Keep the best two.
   - [ ] Is the verdict backed by a position Dan has on record? If it is your guess, the card says so.
7. **Build, serve and test the page** (next section).
8. **Deliver in chat:** the `http://127.0.0.1:PORT/` address, the list of names in one glance, what to check by
   eye, and what you guessed. Numbered action items at the end.
9. **When Dan replies:** save his keeps into the data file as a locked section, rebuild the page, log the round
   in this file (kept, killed, and his reasons in his words), and write the scripting handoff. Do not script.

## The review page (locked 2026-10-12)

Dan: "solidify that process of the review page, just like you made it with a working YouTube player queued up
to the period that I'm going to react to."

- **Data in, page out.** Write the batch as JSON (`reference/data-format.md`), then
  `python3 reference/page.py DATA.json OUT_DIR`. It checks Dan's limits, asks YouTube whether every video still
  answers, and writes `OUT_DIR/index.html`. Never edit the HTML by hand.
- **Keep the data file in the repo** beside the page (`Docs/shoot-<date>-shorts-ideas/ideas.json`). It is the
  record the scripting task works from: ids, seconds, first and last words, the reaction bullets.
- **Serve it** with `python3 .claude/skills/_shared/review_server.py PORT OUT_DIR` and give Dan the
  `http://127.0.0.1:PORT/` address. **Never give him the file path or a link to the file.**
- **Layout, top to bottom:** title, "What I decided (overrule anything)", the sections, one reply box. A
  section Dan picks from has a Kill button on every card; untouched cards count as keeps. A locked section has
  no buttons. Each clip card: the player, the title, RIGHT / WRONG / MY SPIN, the clip line (a link that opens
  YouTube at the second, the time range, the length, the source and the view count), the first and last words,
  "What it is", "Your reaction", and a note when something needs his eye.
- **The player** starts at the cued second, stops at the end, and plays a multi-piece clip in order.
- **Test before delivering.** Open the page in the built-in browser, click one single-piece clip and one
  multi-piece clip, and read `lastPlayer.getCurrentTime()` to confirm the start second and the jump between
  pieces. Check the console for errors.

## Traps (each one cost time on 2026-10-12)

- **A page opened as a file cannot play YouTube (error 153).** Dan opened the file link and every player
  failed. The template now jumps from the file copy to the served copy, but the fix that matters is the address
  you hand him.
- **`review_server.py` treats any quoted string ending in .jpg, .js, .html and so on as a local file**, even
  inside a script, and refuses to start. The template builds the thumbnail path in two pieces for that reason.
  If the server fails with a launchctl error right after a rebuild, wait a few seconds and run it again.
- **YouTube rate-limits caption downloads** (HTTP 429) after roughly 40 in a row, for an hour or more. Search
  still works. Switch to the browser transcript panel.
- **The transcript panel has a "Timeline" tab on videos with chapters.** `transcript_panel.js` clicks through.
- **Some owners turn off embedding** (the check answers 401). `page.py` marks the card so its button opens
  YouTube. Prefer another upload of the same moment that plays in the page.
- **Captions are not word-accurate at the edges.** Leave half a second of room, and write the first and last
  words on the card so the editor can trim.
- **Do not assume Dan's position.** Rounds 1 and 2 guessed his view on cheat days, a stopping rule and which
  "healthy" foods made him fat. Say so on the card, every time.

## Lessons log

**Round 1, 2026-10-12 (20 clips, 7 kept).** Kept: Ronaldo's ab belt ad, fake ab surgery news report, dad bod
street interview, Bill Maher on fat shaming, Dr. Mike on tirzepatide, Oatzempic, the ChatGPT coach (idea kept,
clip called boring). Killed, with his reasons: mewing, leg lengthening surgery and Warren Buffett's Cokes ("why
is a fitness guy reacting to this?"); Ab Circle Pro ("very dated"); Mark Wahlberg, David Goggins, butter
coffee, Peter Attia ("not attention-grabbing", "no good lesson"); Hugh Jackman's water cut (not relevant to
the average guy); the GMA doctor on stopping Ozempic ("boring, puts me to sleep, not someone I care about");
Arnold asking for a vacuum (the vacuum looked weak; he wants a dramatic one); Hormozi's dessert line and a
Planet Fitness ad (likes both targets, not those clips).

**Round 2, 2026-10-12 (20 clips, 8 kept).** Kept: Bill Maher "have you ever seen a fat 90-year-old", Bill
Maher on the "please don't weigh me" card, Bert Kreischer thinking his billboard was Photoshopped, Kevin James
on his cheat day, Post Malone losing 55 pounds by cutting soda, Terry Crews not eating until 2 PM, Alex Hormozi
"why aren't you 200 pounds heavier", Chris Bumstead's vacuum. Killed with no reason given beyond "some were
still a little boring, some didn't have a good lesson": Bill Maher "cake in 1969", Ricky Gervais, all four
Joe Rogan rants (not dead yet, carnivore, food addiction, nobody calls a fat man beautiful),
Ronaldo moving the Cokes, both Rob McElhenney clips, Dr. Now, Jillian Michaels, the Planet Fitness lunk alarm.

**What the two rounds suggest (Claude's reading, not Dan's words):**
- A celebrity telling a short true story about his own body beat a celebrity giving an opinion. Post Malone,
  Kevin James, Bert Kreischer and Terry Crews all survived. Four Joe Rogan rants did not.
- The survivors each map to one concrete habit of Dan's (weigh in, fast until 2, cut soda, no cheat day, the
  vacuum). The ones that died mostly had a lesson that was an attitude or a restatement.
- A third clip from the same monologue died. Two per video is the ceiling.
- A clip with no words (Ronaldo's Cokes, the lunk alarm) died both times it had no clear payoff on screen. The
  one silent clip that survived (the ab belt ad) is the product he is reacting to.
