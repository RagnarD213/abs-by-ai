# Handoff: social profile links, sixpackabs.com first, absbyai.com second

Written 2026-09-22 by Claude (Opus 5.5). Status: NOT EXECUTED.

## Goal

On every social profile Dan owns, the **first** link is `sixpackabs.com` and the **second** link is `absbyai.com`.
Dan's instruction, 2026-09-22, word for word in intent: "make sixpackabs.com the first link on all social media
profiles," with AbsByAI.com as the second link.

## Why (context from the 09-22 traffic analysis)

- GA4 for sixpackabs.com (property `531451799`, account `145219380`) showed a "spike" on Sep 19 to 21 that was
  bots: 150 users, 17 engaged sessions, 0 s engagement, exactly 3 events each, 56 old URLs at 1 view each.
- Real human traffic is about 4 to 5 engaged sessions a day. Organic social sent 35 sessions in 28 days at 2 s
  average. The profiles are not sending people to the site, which is what this task fixes.
- Instagram and TikTok in-app browsers often strip the referrer, so profile clicks land in GA4 as "Direct". **Every
  link therefore carries UTM tags** (below) so the traffic can be measured.
- Standing brand structure (memory `sixpackabs-rebrand-decision`): sixpackabs.com is Dan's fitness media home,
  Abs By AI stays the product. Putting the media home first and the product second fits that.

## The exact links to use

Use these. One `utm_source` per platform, `utm_medium=social`, `utm_campaign=profile-link`.

| Platform | Link 1 | Link 2 |
|---|---|---|
| Instagram | `https://sixpackabs.com/?utm_source=instagram&utm_medium=social&utm_campaign=profile-link` | `https://absbyai.com/?utm_source=instagram&utm_medium=social&utm_campaign=profile-link` |
| Facebook | same pattern, `utm_source=facebook` | same pattern, `utm_source=facebook` |
| TikTok | same pattern, `utm_source=tiktok` | see TikTok note |
| YouTube | same pattern, `utm_source=youtube` | same pattern, `utm_source=youtube` |
| Any other found | same pattern, `utm_source=<platform>` | same pattern |

Link titles where a platform asks for one: **"SixPackAbs.com (free workouts + videos)"** and **"Abs By AI (see
yourself with abs)"**. If a title field is short, use "SixPackAbs.com" and "Abs By AI".

Before starting, open both full URLs in a browser and confirm each loads (200) and the UTM survives any redirect.

## The profiles

Known accounts (from memory `instagram-account-state`, `social-profile-graphics-done`, `sixpackabs-site-stack`):

1. **Instagram `@danrosefit`** (Creator, the real audience; IG business id `17841401601139982`). Up to 5 links,
   orderable. Edit profile → Links. Put sixpackabs.com in slot 1, absbyai.com in slot 2; keep any other existing
   links after them unless they are dead. ⚠ Do NOT touch the Name field ("Daniel Rose", Meta Verified) or turn on
   the "AI creator" label.
2. **Instagram `@abs.by.ai`** (infrastructure/mirror account). Same two links in the same order. Dan said "all"
   profiles, so it is included.
3. **Facebook: the Abs By AI Page** (Edit details → Websites, multiple allowed, first listed = sixpackabs.com) and
   **Dan's personal Facebook** if it lists a website (Intro → Edit details → Websites and links).
4. **TikTok `@absbyai`**. TikTok shows only ONE clickable website link. Put **sixpackabs.com** there (Dan's
   priority). Add "absbyai.com" as plain text on the last line of the bio if it fits the 80-character bio limit
   without cutting existing copy; otherwise skip it and report. Website editing is usually app-only: do it via
   iPhone Mirroring (memory `iphone-mirroring-control`) if the web profile editor lacks the field. If the account
   is not eligible for a website link, report that and stop for TikTok.
5. **YouTube `@absbyai`** (channel `UC236gjadarHAhEhOMYNGJ9g`). Studio → Customization → Basic info → Links. The
   first link is the one shown on the channel header, so sixpackabs.com goes first, absbyai.com second. Keep other
   existing links after them.
6. **Inventory check for anything else**: Threads, X, Pinterest, LinkedIn, a second TikTok. Look for them from the
   links already on the known profiles and from the Blotato account list (`blotato_list_accounts`). Apply the same
   two links to any Dan-owned profile found. Do not create any new account.

Out of scope: the dormant legacy "SixPackAbs.com" channel `UCH9ciCUcWavMsFcAJtLUSyw` (Dan has not confirmed he
controls it). Do not change ManyChat DM links, video descriptions, ad destinations or Google Ads.

## How to execute

- Use Claude in Chrome (Dan's logged-in Chrome). ⚠ The board notes Chrome's Instagram was left signed in as
  `@abs.by.ai` on 09-17; switch accounts with the web account switcher, and **leave Chrome on `@danrosefit` when
  done**. Never sign out or change credentials. If a login is needed, stop that platform and ask Dan to sign in.
- A profile-link change is a public edit to Dan's own profile. Dan asked for it directly in chat on 2026-09-22,
  which is the authorization. Do it; no second approval needed.
- Before each change, record the current links (screenshot or text) in the report so it can be reverted.
- After each change, verify from a logged-out or incognito view of the public profile that the order is right and
  both links open the right page.

## Verification and finish

1. Table in chat: platform, old links, new links, verified yes/no, anything skipped and why.
2. Next day, check GA4 Traffic acquisition with "Session source / medium" for `instagram / social`,
   `youtube / social` and so on (or in PostHog for absbyai.com) to confirm the tagged clicks register.
3. Save a memory note with the final link set per platform (update `instagram-account-state` rather than
   duplicating).
4. Delete this handoff's line from `AI_COORDINATION.md` HANDOFFS and its row in `Handoffs/README.md`; commit and
   push. No dashboard row exists; do not add one.
5. No em dashes in anything written (Dan's rule). `grep -c $'\u2014'` (the em dash character, U+2014) on any new text must be 0.

## Starter prompt

```
Execute Handoffs/handoff-20260922-social-profile-links-sixpackabs-first.md. Put sixpackabs.com first and
absbyai.com second (with the UTM links in the doc) on every social profile I own, verify each on the public
profile, report a before/after table, then close the handoff per its finish steps.
```

Recommended: **Claude Sonnet 5, Medium effort** (browser clicking, low reasoning).
