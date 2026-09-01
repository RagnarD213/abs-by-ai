# HANDOFF: ManyChat "Comment ABS" comment-to-DM automation on @danrosefit

- **Handing off from:** Claude Code (planning session, 2026-08-31)
- **Handing off to:** Claude Code (fresh execution session, with Dan at the keyboard)
- **Reason for handoff:** Execution — requires Dan's logins/OAuth at several steps
- **Last completed step:** Plan approved by Dan; NOTHING has been executed. No ManyChat
  account exists yet, no IG toggle flipped, no automation built.
- **Exact next action:** Step 1 below (Dan flips the IG message-access toggle).

## Why this is top priority

Roughly **60 scheduled posts** in the Blotato queue (27 @danrosefit reels + 33 image
posts, publishing daily through October) carry the CTA **"Comment ABS and I'll send you
the free AI preview 👇"**. Nothing delivers on that promise today — every commenter is
being silently ignored. Each day this stays dead, more posts publish with a broken promise.
It also blocks paid: the 2026-08-31 paid-ads launch sheet deliberately excluded reels with
this CTA because it was dead; once ManyChat is live those become eligible.

## What to build

Someone comments "ABS" (case-insensitive, contains-match) on any @danrosefit post →
1. **Public comment reply:** "Just sent it, check your DMs 📩"
2. **DM** with the free-preview link + UTM tracking.

Approved DM copy (Dan's register — adjust only if he edits it):

> Here it is 👊 Upload one photo and my AI shows you what you'd look like with abs —
> free, takes about 30 seconds:
> absbyai.com/?utm_source=instagram&utm_medium=dm&utm_campaign=comment-abs
>
> That preview is the exact picture that got me from 200 lbs to a six pack at 40.
> Reply here if you have questions.

⚠ Instagram often requires the user to tap a quick-reply button before an automation may
send a link (Meta anti-spam). If ManyChat enforces this, split into two beats:
"Want the free AI preview?" → [Send it] button → the link message. That's fine — the tap
counts as engagement. Do not fight it.

## Execution steps

**Step 1 — Dan, in the Instagram app (5 min):**
Settings → Messages and story replies → Message controls → **Allow access to messages**
must be ON. Without it ManyChat connects but silently cannot send. (@danrosefit is
already a Creator account — done during the Meta Verified setup 2026-08-24.)

**Step 2 — Dan: sign up + connect ManyChat (10 min):**
manychat.com, Google login, connect Instagram via his Facebook login. Connect ONLY
@danrosefit — @abs.by.ai is infrastructure, its mirrors point at @danrosefit anyway.
Credentials/OAuth are Dan's to enter (platform restriction on Claude, not Dan's rule).

**Step 3 — plan/spend decision (Dan):**
Free tier is capped at **25 active contacts** (verified 2026-08-31) — one decent reel
exhausts it in a day and ManyChat then silently stops DMing, re-breaking the promise.
Recommendation Dan has seen: test on free, upgrade to **Essential (~$15/mo) the same
day**. This is a new subscription — his card, his click.

**Step 4 — build the automation (Claude can drive in Dan's Chrome once he's logged in):**
- Trigger: comment containing "ABS" on **ALL posts and reels** — never per-post; the
  promise lives in ~60 captions and per-post selection is a maintenance trap.
- Action 1: the public reply. Action 2: the DM (or two-beat version) above.

**Step 5 — TEST before trusting (30 min):**
- Comment "ABS" from a different real account (Dan's personal one; Claude cannot log
  into IG). Verify: public reply arrives, DM arrives, link opens.
- Also test "abs" and "Abs please" to confirm contains-match, not exact-match.
- Click the link and confirm the session lands in PostHog with
  `utm_campaign=comment-abs`.

**Step 6 — measurement (Claude, standing analytics authorization):**
Build a PostHog insight on `utm_campaign=comment-abs` traffic once real traffic exists.
ManyChat's own dashboard shows comments captured → DMs sent → clicks.

**Step 7 — close out:** update AI_COORDINATION.md, check off the Key dashboard task
(`/dashboard-tasks` for mechanics), and flag to Dan that the comment-ABS reels are now
eligible for the paid-ads specs from the 2026-08-31 launch sheet.

## Risks / cautions

- Blotato's IG auto first-comment carries the absbyai.com link; the growth plan said to
  turn it off "once ManyChat is live" — **ask Dan before touching it** (it's the current
  only path from reel → site, and switching it off is a queue-wide change).
- Do not connect or touch @abs.by.ai in ManyChat.
- If ManyChat asks for broad Facebook Page permissions, that's normal for the IG API —
  but any terms/consent screens are Dan's to click.

## Starter prompt (paste into a fresh session)

> Execute Handoffs/handoff-20260831-manychat-comment-abs-setup.md — set up the ManyChat
> "Comment ABS" comment-to-DM automation on @danrosefit. I'm at my computer and can log
> in wherever needed. Walk me through my steps and drive the browser parts you can.

**Recommended runner:** Sonnet 5, default effort — this is guided UI work with a human in
the loop, not heavy reasoning. No fast mode needed.
