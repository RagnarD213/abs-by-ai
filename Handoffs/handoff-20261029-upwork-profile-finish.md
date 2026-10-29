# Upwork profile: finish portfolio, packages and details

Created: 2026-10-29. Status: ready to fire. Task name: Upwork Profile Finish.
Recommended: Claude Sonnet 5, high effort, with Claude in Chrome (mechanical entry of locked copy; Dan's Chrome is already signed in).

## State

- Profile is LIVE and Public: https://www.upwork.com/freelancers/~016109a7105ec3bf5d (account "Daniel Rose", Freelancer Basic; Dan's login also has the client account "SixPackAbs.com": switch via the avatar menu if a page says "for freelancers only").
- Live and checked 2026-10-29: title "Direct-Response Video Ads | Scripts & Edits That Drove 238M+ in Sales", full overview, $145/hr, English native, experience level Expert, two jobs (Social Response Marketing Jul 2019 to Jan 2026; Six Pack Shortcuts (SixPackAbs) Jan 2010 to Apr 2019, both Austin), skills Video Ad, Video Advertising, Short Video Ad.
- All approved copy and prices: `Handoffs/upwork-profile-draft.md` (sections 4, 5, 8, 9.3). Facts and entry log: `Handoffs/upwork-profile-working-brief.md`.
- Dan authorized publishing everything in the draft. Dan's standing permission (memory `personal-info-form-entry-ok`): enter his DOB, address, phone in forms without asking.

## Do, in order

1. **Availability:** set hours to less than 30 hrs/week (Dan's capacity is 15 hrs, 2 clients). Not open to contract-to-hire.
2. **Education:** Boston University, Bachelor of Science (BS) (pick from Upwork's list), 2004 to 2008. Field of study: Entrepreneurship (list pick failed during onboarding; retry, else leave blank). Description: "Double major in Entrepreneurship and Marketing."
3. **Skills:** add up to 15 total from draft section 5 (Video Editing, Video Commercial, Video Sales Letter, Scriptwriting, Direct Response Copywriting, Copywriting, Ad Creative, Marketing Video, Google Ads / YouTube Marketing, etc.). Pick only Upwork's own list entries.
4. **Portfolio (5 items, draft section 8 + captions 9.3):** HBI four-ad case study; SixPackAbs superfoods; Mind Movies; Spy Briefing; SixPackAbs fasting ad (https://www.youtube.com/watch?v=5i30KDjihrs). Each needs a cover image: grab a frame with ffmpeg from the YouTube thumbnail (`https://i.ytimg.com/vi/<id>/maxresdefault.jpg`) and upload with the `file_upload` tool. Upwork may reject ".com" text: write "SixPackAbs", not "SixPackAbs.com", if it complains. Verify the 40/300 character limits in the live form.
5. **Project Catalog (4 projects, draft section 4):** A finished ads ($950/$2,500/$4,500), B scripts ($350/$900/$1,600), C new versions ($450/$800/$1,400), D YouTube Ads Account Audit ($750, 5 days). **Added 2026-10-29 (merged Upwork plan): a fifth project, "Ad Hook Fix and New Version": $75 tier (review one ad or script; 5 hooks, 1 rewritten opening, 1 revision; 2 days) and $150 tier (1 variation up to 60 s from supplied footage, 1 format, captions, 1 revision; 3 days). If Upwork rejects a $75 tier, report the minimum it allows.** 3 revisions included on A to C. Write short, plain descriptions from the overview; no em dashes; no AI or tool mentions.
6. Re-open the public view (`?viewMode=1`), check every item, record the result in the brief, close the Chrome tab, push with `scripts/git/safe-push.sh`, delete the board entry, move this handoff out of OPEN in `Handoffs/README.md`.

## Do not

Buy Connects, subscribe to Freelancer Plus, boost or promote the profile, or apply to jobs (that is `handoff-20261007-upwork-job-applications.md`). Do not enter ID documents (Dan does ID verification himself).

## Upwork traps seen 2026-10-29

- Titles reject `> ; ! @ $ % ^ = { }`. The overview rejects website addresses (".com").
- Autocomplete fields: type with the `computer` tool, wait 2 to 3 s, then click the `li[role=option]` whose text matches (a small JS helper that clicks the exact option worked). The skill search stopped returning results after ~4 searches; reload the page to reset it.
- The page smooth-scrolls after clicks, so screenshot coordinates go stale; target fields by `find` refs or take a fresh screenshot before clicking.
- A generic "There was an error loading this page" toast appears often and is harmless.

## Starter prompt

Name this task Upwork Profile Finish. Read Handoffs/handoff-20261029-upwork-profile-finish.md and execute it in my Chrome (I'm signed in to Upwork). Add availability, education, skills, the five portfolio pieces and the four packages exactly as approved in Handoffs/upwork-profile-draft.md, check the public profile, and report the link. Don't buy Connects or apply to jobs.
