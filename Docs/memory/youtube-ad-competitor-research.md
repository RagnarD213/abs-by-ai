---
name: youtube-ad-competitor-research
description: "VidTao research (2026-07-27) — who the big YouTube fitness advertisers for men are, their spend, and the 10 swipe ads picked for Dan's ad creation"
metadata: 
  node_type: memory
  type: project
  originSessionId: 49114322-ea34-4543-8daa-5350b20fa383
  modified: 2026-09-10T14:54:13.130Z
---

Researched in VidTao (vidtao.com — Dan calls it "VidTow"; Dan is logged in in Chrome, free tier: spend columns visually blurred but readable via page text; ad-spend SORTING and "open on YouTube" are paywalled — do NOT start the $87/mo trial).

Key market facts (as of 2026-07-27):
- **MadMuscles** (AmoApps): $487M/yr YouTube spend, #1 fitness advertiser, ALL male-targeted 9:16 ~90s ads, "military/respect" themed. Single creatives at $100k+/30 days.
- **V Shred**: $20.3M/yr (=$131M lifetime). Current monster ad: $306.8k total. Actively testing AI-themed hooks ("endless_cardio_AI_hook", "ai-frozenlake-fat-man-hook").
- **Muscle Booster** (Welltech): $35.2M/yr, #1 Bodybuilding category; sprays dozens of ~$500–$2k 2–5min vertical creatives weekly, male-targeted.
- **Fitme Workouts**: $48.3M/yr; creative names encode gender (gF/gM) and hook type; runs explicit "AIhook" male creatives.
- **Kinobody**: essentially stopped YouTube ads ($23 in last 365d; ~$85.5k lifetime). Best classics from Jan 2023: "You See That Guy? That Used To Be Me" and "People Freak Out When I Tell Them I Lift Weights Just Twice Per Week".

The 10 swipe ads (YouTube IDs) delivered to Dan for the Abs By AI ad creator: lfa71t4RAyw, HZLYJPGi8gI ($115k MadMuscles), oxP-KvqWQAg ($306k V Shred), PVHD4bffdVI, syKJ5NA2NxA (V Shred AI hook), U6EOLyB1qPo ($22k Fitme male), 1jCH9YGJSN0 (Fitme AI hook), iDZqaVd0ABE (Muscle Booster), nMaVPl_R6pg, No_i6mChp10 (Kinobody classics).

**Pulling an ad's transcript (works 2026-09-10):** yt-dlp is dead here (YouTube's "page needs to be reloaded" bot
wall; the Mac has no Python ≥ 3.10 for a current yt-dlp) and caption `baseUrl`s return 0 bytes. What works: the
in-app Browser pane → `navigate` to `youtube.com/watch?v=ID` → one `javascript_tool` call that clicks
`#description-inline-expander #expand`, then the `ytd-video-description-transcript-section-renderer button`, polls
for `ytd-transcript-segment-renderer`, and returns the text. Chain navigate → wait 4 s → that call per video in one
`browser_batch`; ten ads took ~2 minutes. The page title is the advertiser's creative filename (it encodes theme,
variant and hook). Transcripts of all ten swipe ads above were used for the /start VSL script (2026-09-10).

Related: [[proof-banner-image-gen-process]], [[vsl-landing-page]]
