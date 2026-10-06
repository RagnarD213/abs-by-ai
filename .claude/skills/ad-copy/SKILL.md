---
name: ad-copy
description: Write the text of a paid ad for Abs By AI in Dan's own voice (Google Demand Gen headlines, long headlines and descriptions; the same lines for Meta or TikTok when asked) so Dan reads it and changes nothing. Use whenever Dan asks to write, rewrite, improve or "do the copy for" an ad, asks for headlines or descriptions, when /ad-setup needs copy for a new ad, or when Dan edits ad copy and says to learn from it, even if he doesn't say "/ad-copy". The spoken script of an ad is /scriptwriting; polishing a sales letter is /copy-edit; putting the ad live is /ad-setup.
---

> **Shared writing rules (2026-10-06):** before writing, read `.claude/skills/_shared/WRITING-RULES.md`. It holds the rules every writing skill follows and the list of memory entries (`Docs/memory/`) to read. Where it and this skill disagree, the newer dated line wins.

# /ad-copy: ad text Dan would have written himself

**The goal (Dan, 2026-10-01):** he reviews the copy and makes no revisions, and he cannot tell which lines he wrote
and which lines the session wrote. Every edit he makes is a miss. Count them, learn from them, record them here.

Built 2026-10-01 from Dan's own edits to the trial campaign `24316364155`: he rewrote 12 of 30 headlines across six
ads. The pattern in what he cut and what he wrote is the core of this skill. Second calibration 2026-10-02: his edit
of the Performance Max campaign `24308574894` (long headlines, descriptions, and lines that must fit any creative).

## Read first, every time

1. This file, all of it. The section WHAT DAN CHANGED is the calibration. For the voice behind the lines (his enemy
   framing, credentials, person-plus-outcome), `.claude/skills/_shared/DAN-VOICE.md` sections 1, 6 and 7.
2. `scripts/ads/ytads/headline-style.md`: every line Dan wrote by hand, the shapes he uses, his dated rules.
3. The live copy of the account's current ads, so new lines match what is running and nothing is duplicated by accident:
   `node scripts/ads/api/client.js search "SELECT ad_group.name, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines FROM ad_group_ad WHERE campaign.id = 24316364155 AND ad_group_ad.status != 'REMOVED'" --json`
4. The ad itself: its transcript or script. The hook, who it speaks to, and who or what it argues against.

## What a set is

| field | count | limit | case |
|---|---|---|---|
| headline | 5 | 40 characters (Dan's own run 17 to 33) | Title Case |
| long headline | 3 | 90 characters | sentence case |
| description | 3 | 90 characters | sentence case |

Business name `Abs by AI`. No registered mark. No em dash, no en dash; a spaced hyphen is his.

**Performance Max asset group (mixed assets):** up to 15 headlines of 30 characters, 5 long headlines of 90, 5
descriptions of 90. Do not fill the slots for the sake of it: Dan cut 15 headlines to 12 and left three empty. Read
"Lines that must fit any creative" below before writing one.

## How Dan writes a headline

**A headline names a person and the outcome that person wants.** It does not describe the product. Ask of every
line: would a 40-year-old dad scrolling YouTube see himself and the thing he wants in it? If the line only says
what the app does or what the video contains, Dan cuts it.

His five shapes, in the order he reaches for them:

1. **How [who] [gets the outcome]**: *How Busy Dads Get Abs*, *How 40+ Dads Can Get Abs*, *How Men 40+ Lose Belly
   Fat*, *How Busy 40+ Dads Lose Fat*, *How To Get Abs After 40*.
2. **His own history, first person**: *How I Got Abs At 40*, *How AI Got Me Abs*, *How AI Got Me Abs At 40*,
   *How I Lost Belly Fat With AI*, *How AI Fixed My Supplements*.
3. **The enemy hates him**: *Human Trainers Hate Him*, *Trainers Hate This AI App*, *Human Trainers Hate This AI*,
   *Trainers Despise Him*, *Human Trainers Despise Him*, *Supplement Corps Hate Him*. Use it when the ad argues
   against paying someone (trainer, nutritionist, supplement company, coach). Name that enemy.
4. **Fire them**: *Fire Your Personal Trainer*, *Fire Your Nutritionist*. Same condition as shape 3.
5. **Plain topic line**: *The Truth About Supplements*, *How AI Replaces Personal Trainers*, *A Busy Dad's Fitness
   System*, *A Personalized AI Fitness Plan*. At most ONE of these per set.

**Build a set of five like this:** two lines from shapes 1 and 2 (always include *How I Got Abs At 40*), one or
two from shapes 3 and 4 when the ad has an enemy, at most one from shape 5. When the ad has no enemy, fill with
shapes 1 and 2.

**Vary the wording between ads.** Dan never pasted the same enemy line twice in a row: hate / despise, him / this
AI / this AI app, trainers / human trainers. Two ads may share *How I Got Abs At 40*; they do not share all five.

**His words:** abs, belly fat, lose fat, busy dads, men 40+, 40+ dads, at 40, after 40, with AI, human trainers,
personal trainer, supplements, fire, hate, despise. The age is always there somewhere in the set.

**A headline does not have to echo the video's title.** He deleted *The Cost Of Getting Abs* from the ad with that
exact title and wrote *Fire Your Personal Trainer*.

## What Dan cuts (never write these)

Every line below was written by a session and replaced by Dan on 2026-10-01. They share one fault: they describe a
plan, a system or a feature, and name no person and no outcome.

- *A Dad's AI Fitness Plan* · *An AI Fitness Plan At 40* · *One AI Fitness Plan* · *AI Fitness Built Around You*
- *Use AI To Plan Your Workouts* · *An AI Trainer At Every Workout* · *Audit Supplements With AI*
- *Fitness At 38 And 40* · *Getting Fit After 40* · *You're Not Too Old To Get Fit* · *Fitness Advice Adds Up*
- *The Cost Of Getting Abs*

Words that mark a line he will cut: plan, planning, system, built around, personalized, practical, fitness (as the
subject), advice, getting fit. "Get fit" is not the outcome. Abs and belly fat are.

## Lines that must fit any creative (Performance Max, any mixed-asset campaign)

In a Demand Gen ad the copy sits beside one video. In Performance Max, Google pairs any line with any video or
image. **Test every line against every asset in the group: does it still make sense beside the trainer picture, the
dad-at-the-pool picture and the supplements video?** If it only fits one of them, Dan deletes it.

- Cut on 2026-10-02 for this reason: *How Busy Dads Get Abs*, *A Busy Dad's Fitness System*, *Supplement Corps Hate
  Him*, *How AI Fixed My Supplements*. Each belongs to one ad.
- Kept: the broad person-plus-outcome lines (*How I Got Abs At 40*, *How AI Got Me Abs*, *How AI Got Me Abs At 40*,
  *How To Get Abs After 40*, *How 40+ Dads Can Get Abs*, *How Men 40+ Lose Belly Fat*, *How I Lost Belly Fat With AI*)
  and the trainer lines (*Fire Your Personal Trainer*, *Human Trainers Hate Him*, *Trainers Hate This AI App*). The
  product is an AI trainer, so a trainer line fits every creative. A supplement line does not.
- His one new headline: *The Real Truth About Abs*. A curiosity line that fits anything.
- He trims an article to tighten a line: *A Personalized AI Fitness Plan* became *Personalized AI Fitness Plan*.

A copied set of single-ad lines is not a Performance Max set. Write for the whole group.

## Long headlines and descriptions: sell the click

**Corrected 2026-10-02.** The old rule here was "one plain sentence on what the video shows". Dan called those lines
weak ("didn't really persuade the user to click") and replaced 7 of 10. A long line has one job: give the reader a
reason to click. A sentence that only reports what Daniel Rose explains gives none.

His shapes, all from his own rewrite:

1. **A number and the reader's outcome.** *5 ways you can use AI to lose your stubborn stomach fat and to get six
   pack abs.* / *Learn 5 ways you can use AI to lose stubborn belly fat. Free video teaches you how.*
2. **What the app does for YOU, then the offer.** *AI fitness app shows you how to lose stomach fat and get abs. Try
   it free for 7 days!* / *This AI app shows you how to lose your belly fat. Try it free for 7 days.*
3. **The enemy, then "see why".** *Trainers despise this AI fitness app. See why men are replacing their trainer
   with AI.*
4. **A story with the ending held back.** *AI genius discovers how to use AI to lose his stubborn belly fat. Video
   reveals full story* / *I struggled with belly fat until I discovered how to use an AI trainer to get abs.*
5. **First person "Here's why".** *Here's why I stopped paying a personal trainer and use an AI trainer instead.*
   (the only long headline he kept).

What these share, and what to check on every long line:

- **The outcome is in the line, in his words:** belly fat, stomach fat, stubborn, abs, six pack abs. Not "fitness
  plan", "workout and nutrition system", "goal image".
- **It speaks to the reader:** "you", "your", or a first person story the reader sees himself in. "Daniel Rose
  shows / explains" puts a stranger's name where the reader's benefit should be.
- **It ends on a reason to click:** the offer (*Try it free for 7 days*, *Free video teaches you how*) or an open
  loop (*See why...*, *Video reveals full story*). At least two of five long headlines and two of five descriptions
  carry the offer or a loop.
- **It fits any creative** (section above) when the campaign mixes assets.
- An exclamation mark and a dropped final period are his; do not "correct" them.

Still allowed, at most one or two per set: a plain feature line he kept, *AI plans workouts and meals around your
schedule, equipment and starting point.* and *Daniel Rose shows how an AI trainer builds his plan and adjusts it at
every workout.* Never a whole set of them.

What he cut (never write these as long lines): *Daniel Rose shows how he used AI to turn a goal image into a workout
and nutrition plan.* · *A busy dad explains the workout, meal and adjustment plan he uses with AI.* · *Daniel Rose
explains how he rebuilt his fitness at 40 with a plan he could follow.* · *Daniel Rose explains why he stopped taking
supplement advice from influencers.* · *Daniel Rose shows how AI turned his goal image into a personalized fitness
plan.* · *Daniel Rose shows the workout and nutrition system he follows as a 40-year-old dad.* · *Daniel Rose shows
how AI reads the label on every supplement in his stack.*

The offer wording comes from /start: 7 days free. Check the page before writing a different offer.

## Rules on record (apply, do not discuss)

- Never the word "trick". Never a line Google already refused in this account: *This Picture Got Me Abs*,
  *Abs At 40 - The Photo That Did It*, *Why My Diets Kept Failing*.
- No claim that reads unbelievable without the video (memory `ad-copy-no-unbelievable-claims`).
- Dan's own shapes above are his call and go out as written, even where `scripts/ads/ytads/lint.js` would refuse
  them. The lint guards the automatic generator. For a hand-built ad, add his lines to `DAN_APPROVED` in
  `scripts/ads/api/dgen-add-ad.js`. If Google limits a line, rewrite only that line (memory
  `ad-retry-rule-and-no-trick`).

## Process

1. Read the four things above. Write the set.
2. Check every line: character count, Title Case, no banned word, no em dash (grep the file for the character, count must be 0), not in the
   cut list, the set mix is right, the age appears, at most one shape 5 line. Every long headline and description
   passes the "sell the click" checks. In a mixed-asset campaign, every line fits every video and image.
   Proofread his lines too: a typo he typed in the editor (*"This AI apps hows you"*, 2026-10-02) gets fixed and reported.
3. Compare against the last set you wrote for another ad. Fewer than three shared headlines.
4. Show Dan the set in chat as a numbered list per field, with the character count beside each headline. No
   commentary, no alternatives, no menu. One set.
5. On his approval, the set goes into the ad spec (`scripts/ads/api/dgen-ads/<ad>.json`) or straight onto the live
   ads with an `adOperation.update` and mask `demand_gen_video_responsive_ad.headlines`. Every format of one ad
   carries the same copy: change all of them in one mutate.
6. **Dan edits copy in the Google Ads editor himself.** When he does, read the live ads back, diff against what
   was written, and add the result to WHAT DAN CHANGED below before doing anything else. Then copy his lines to the
   ad's other formats. ⚠ His open editor holds a stale copy of every ad in the campaign: when he clicks Save it
   overwrites API changes made since he opened it (it happened twice on 2026-10-01). Apply after he has saved, and
   read back.

## WHAT DAN CHANGED

Newest last. Each entry: date, the ad, struck line → his line, and the lesson. Zero edits is the target.

### 2026-10-01, trial campaign `24316364155`: 12 of 30 headlines rewritten, 0 of 36 other lines

| ad | session's line | Dan's line |
|---|---|---|
| Ad 10 Busy Dad | A Dad's AI Fitness Plan | How Busy Dads Get Abs |
| Ad 10 Busy Dad | Fitness At 38 And 40 | How 40+ Dads Can Get Abs |
| Ad 10 Busy Dad | How AI Got Me Abs | How I Lost Belly Fat With AI |
| Ad 3 Trainers | An AI Trainer At Every Workout | Human Trainers Hate Him |
| Ad 3 Trainers | How AI Got Me Abs | Trainers Hate This AI App |
| RA-01 | AI Fitness Built Around You | Human Trainers Hate This AI |
| RA-01 | Use AI To Plan Your Workouts | Trainers Despise Him |
| Ad 6 Not Too Old | You're Not Too Old To Get Fit | How Men 40+ Lose Belly Fat |
| Ad 6 Not Too Old | Getting Fit After 40 | How To Get Abs After 40 |
| Ad 6 Not Too Old | An AI Fitness Plan At 40 | How Busy 40+ Dads Lose Fat |
| Ad 6 Not Too Old | How AI Got Me Abs | How AI Got Me Abs At 40 |
| Ad 13 Cost | The Cost Of Getting Abs | Fire Your Personal Trainer |
| Ad 13 Cost | Fitness Advice Adds Up | Human Trainers Hate This AI |
| Ad 13 Cost | One AI Fitness Plan | Human Trainers Despise Him |
| Ad 4 Supplements | Audit Supplements With AI | Supplement Corps Hate Him |

Kept as written: *How I Got Abs At 40* (all six ads), *How AI Got Me Abs* (three of six), *Fire Your Personal
Trainer*, *How AI Replaces Personal Trainers*, *A Busy Dad's Fitness System*, *A Personalized AI Fitness Plan*,
*How AI Fixed My Supplements*, *The Truth About Supplements*.

Lessons, all folded into the sections above:
1. Product-description headlines die. Person plus outcome lives.
2. "Belly fat" and "lose fat" are his words and he wants them in headlines.
3. The enemy line is his favourite new shape; he put one or two in every ad that argues against paying someone.
4. *How AI Got Me Abs* survives once per set at most, and he swaps it out when a more specific line fits the ad.
5. The age (40, 40+, after 40) goes in more lines than a session would put it in.

### 2026-10-02, Performance Max `24308574894`: 5 of 15 headlines cut, 4 of 5 long headlines and 3 of 5 descriptions rewritten

The session had copied his single-ad lines from the trial campaign into one asset group. Dan's note: he deleted
headlines "that might not have made sense with certain videos or images", and found the long lines "weak", not
persuading anyone to click.

| field | session's line (copied from the trial ads) | Dan's line |
|---|---|---|
| headline | How Busy Dads Get Abs | cut |
| headline | A Busy Dad's Fitness System | cut |
| headline | Supplement Corps Hate Him | cut |
| headline | How AI Fixed My Supplements | cut |
| headline | A Personalized AI Fitness Plan | Personalized AI Fitness Plan |
| headline | (none) | The Real Truth About Abs |
| long headline | Daniel Rose shows how he used AI to turn a goal image into a workout and nutrition plan. | 5 ways you can use AI to lose your stubborn stomach fat and to get six pack abs. |
| long headline | A busy dad explains the workout, meal and adjustment plan he uses with AI. | AI fitness app shows you how to lose stomach fat and get abs. Try it free for 7 days! |
| long headline | Daniel Rose explains how he rebuilt his fitness at 40 with a plan he could follow. | Trainers despise this AI fitness app. See why men are replacing their trainer with AI. |
| long headline | Daniel Rose explains why he stopped taking supplement advice from influencers. | AI genius discovers how to use AI to lose his stubborn belly fat. Video reveals full story |
| description | Daniel Rose shows how AI turned his goal image into a personalized fitness plan. | This AI app shows you how to lose your belly fat. Try it free for 7 days. |
| description | Daniel Rose shows the workout and nutrition system he follows as a 40-year-old dad. | I struggled with belly fat until I discovered how to use an AI trainer to get abs. |
| description | Daniel Rose shows how AI reads the label on every supplement in his stack. | Learn 5 ways you can use AI to lose stubborn belly fat. Free video teaches you how. |

Kept as written: 10 headlines (the broad outcome lines and the three trainer lines), *Here's why I stopped paying a
personal trainer and use an AI trainer instead.*, *AI plans workouts and meals around your schedule, equipment and
starting point.*, *Daniel Rose shows how an AI trainer builds his plan and adjusts it at every workout.*

Lessons, all folded into the sections above:
1. The 2026-10-01 reading "he left the long lines alone, keep the shape" was wrong. He had not looked at them yet.
2. A long line sells the click: the reader's outcome, "you", and an offer or an open loop at the end.
3. "Stubborn" belly fat, stomach fat and six pack abs are his words. The 7 day free trial belongs in the copy.
4. In a mixed-asset campaign every line must fit every video and image. Lines tied to one ad get cut.
5. Fewer good lines beat a full set. He left three headline slots empty.
