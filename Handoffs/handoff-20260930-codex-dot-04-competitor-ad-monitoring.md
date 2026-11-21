# Handoff: weekly competitor ad monitoring on the OpenAI dot (Codex sets it up)

Written 2026-09-30 by Claude (Fable 5.1). **Executor: a Codex session (GPT-6 Sol, medium), then the dot runs it
every Monday at 7:00 AM Central.** Read `handoff-20260930-codex-dot-00-shared-setup.md` first. This is a new
routine; nothing on Claude to turn off.

## Goal

Every week Dan knows what the proven fitness direct-response players are actually running: which ads have
survived 30+ days (the winners), what new hooks appeared, what their landing pages and offers look like now.
This is the raw material for the VSL campaign (`handoff-20260930-ad-performance-pick-5-for-vsl-campaign.md`),
the five landing-page mockups, and every future ad script, under Dan's standing rule: **recommend only what the
leaders run, and name who runs it** (memory `proven-direct-response-only`, 2026-09-24).

## Who to watch

Tier 1, every week: **V Shred, MadMuscles, BetterMe, Noom.**
Tier 2, every other week: **Muscle Booster (Welltech), Fitme Workouts, Kinobody** (largely dormant on YouTube;
its 2023 classics are still the reference hooks).
Background on all of them: memories `youtube-ad-competitor-research` (VidTao, 2026-07-27) and
`madmuscles-deep-dive` (2026-08-03; MadMuscles' parent is under an FTC halt, ads still running at scale).

## Sources (all free, no logins needed except VidTao)

1. **Meta Ad Library** (public): search each advertiser's page; filter active ads; note ads with a start date
   30+ days ago (survivors), new ads this week, formats (9:16 video, length, on-camera vs AI characters vs
   UGC), the first 3 seconds of the hook, the CTA and the landing URL.
2. **Google Ads Transparency Center** (public): same advertisers, video ads, date ranges.
3. **VidTao** (vidtao.com): Dan has a free-tier login in Chrome; spend columns are blurred but readable in page
   text, spend sorting is paywalled. **Do not start the $87/month trial.** If the dot cannot log in, skip
   VidTao and say so; the two public sources are enough for a weekly read.
4. **Landing pages:** open each advertiser's current quiz or VSL page once a week; note the first screen, the
   quiz length, the offer ladder and default plan, any before/after, testimonial and guarantee elements, and
   anything that changed since last week (screenshot into the log).
5. **Transcripts** of a new winner: YouTube's transcript panel in the browser (recipe in memory
   `youtube-ad-competitor-research`; yt-dlp is dead on the Mac).

## Output every Monday

A short memo to Dan plus a running Google Doc **"Competitor ad log"** (one dated section per week, anyone with
the link can view, per Dan's Drive rule):

1. **Survivors:** ads still running after 30+ days, per advertiser, with hook transcript of any new entrant to
   the list. These are the proven ones.
2. **New this week:** new hooks and formats, with a one-line read of what they are testing.
3. **Landing page and offer changes:** anything that moved.
4. **For Abs By AI, one paragraph:** the single most useful thing to copy this week, with the advertiser
   named. If nothing new is worth copying, say "nothing to change this week". No invented tactics.
5. Counts: ads scanned per advertiser, sources that could not be read.

Judging rules: a winner is one that stays live and gets versioned; judge by longevity and variants, never by
whether it looks good. Stay on design, reach and conversion; no compliance or policy commentary (Dan's
2026-09-25 rule).

## The dot assignment (paste-ready, the Codex session finalizes it)

> Every Monday at 7:00 AM Central, check the ads that V Shred, MadMuscles, BetterMe and Noom are running
> (Muscle Booster, Fitme and Kinobody every other week) in the Meta Ad Library and the Google Ads Transparency
> Center. Tell me which ads have run 30+ days, what is new this week (hook, format, length, CTA), and what
> changed on their landing pages and offers. Pull the transcript of any new long-running ad. Write it into my
> Google Doc "Competitor ad log" as a dated section and send me a short memo ending with the one thing most
> worth copying for Abs By AI, naming who runs it, or "nothing to change this week". Never start a paid trial.
> No compliance or legal commentary. Never use an em dash.

## Steps for the Codex session

1. Read the two memories named above so the first week's log has the baseline (spend tiers, the 10 swipe ads,
   MadMuscles' funnel numbers).
2. Create the Google Doc "Competitor ad log" with a "Baseline (from July and August research)" section, share
   anyone-with-link view, and record its id in `Docs/COMPETITOR_ADS.md` (new, short) with the advertiser list
   and the sources.
3. Finalize the assignment; hand it to Dan with the schedule and the note that VidTao is optional.
4. Prove one run by hand: the dot produces a first weekly section with real ads, real start dates and at
   least one transcript. Check the "for Abs By AI" paragraph names an advertiser.
5. Record in `Docs/ROUTINES.md`.

## Traps

- Meta Ad Library needs the advertiser's exact page; MadMuscles runs under several page names and shells.
  Search "MadMuscles" and "Mad Muscles" and keep the page ids in the doc once found.
- Ad Library start dates are when the ad began, not when the campaign did. Longevity is still the best free
  signal.
- Do not let the memo become a report. Five numbered parts, short, the copy-this paragraph last.

## Done means

The doc exists with a baseline and one real weekly section, the Monday schedule is set,
`Docs/COMPETITOR_ADS.md` and `Docs/ROUTINES.md` are committed, and Dan has received the first memo.

## Starter prompt

```
Read Handoffs/handoff-20260930-codex-dot-00-shared-setup.md, then execute Handoffs/handoff-20260930-codex-dot-04-competitor-ad-monitoring.md in full. Create the Competitor ad log doc with the baseline, finalize the dot assignment, prove one weekly run, record the routine.
```

Model: GPT-6 Sol, medium effort.
