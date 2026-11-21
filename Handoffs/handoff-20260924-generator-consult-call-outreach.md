# Handoff: email everyone who generated, invite them to a 15-minute call with Dan

Written 2026-09-24. Recommended executor: **Claude Sonnet 5 / Medium** (needs the Gmail connector, which Codex
does not have). Time-sensitive: the 09-20 trialer's trial ends **2026-09-27**, so that email goes out first,
by 09-26.

## Goal

Dan personally sells by phone before we decide whether to fold the AI subscription. Every person who made an AI
abs picture and left an email gets a short personal email from Dan asking for a free 15-minute call. On the call
Dan helps them, learns why they didn't buy, and offers the membership. This is the "sales-first test" in the
fold-or-fix memo (https://claude.ai/artifact/TF99sUGBWMoLf4cR2zCrUv). Its result feeds the kill rule: fold on
2026-10-26 if fewer than 3 strangers have paid and this outreach produced 0 payments. Target: **2 paid by
2026-10-08**, plus a stated reason from everyone who says no.

## Hard rules

- **Nothing is sent until Dan approves** the final recipient count, the segments and the exact copy, in one
  message. Sending email to users is on the ask-first list in `CLAUDE.md`. One approval covers the first send and
  the single follow-up described below; anything beyond that is a new approval.
- **The repo is public. No email address, name or phone number goes into any committed file**, this handoff,
  the board, a commit message or an artifact. The working list lives outside the repo (see Tracking).
- No em dashes and no en dashes in any email or document (grep each draft for the em dash character before sending; the count must be 0).
- No invented scarcity ("only 10 spots"), no discount devices, no claims about results. Dan's rule set from the
  web cart and the FTC v. MadMuscles lesson applies.
- Every email carries an opt-out line and the postal address from `MARKETING_ADDRESS` (Railway env,
  `railway variables --service abs-by-ai --kv`). Several recipients are in Canada (CASL needs sender
  identification + a working opt-out).

## Step 1: build the list (read-only, prod Postgres)

`DATABASE_PUBLIC_URL` from `~/.absbyai-secrets.env` (read it with `grep`; `source` fails on line 16).
Measured 2026-09-24, before de-duplication: about 5 account holders with a generation, 5 `analysis` subscribers,
9 null-source subscribers. Expect **roughly 15 to 20 people**.

Include:
1. `users` rows with `before_image IS NOT NULL` or a `transformations` row.
2. `subscribers` with `source = 'analysis'` (the analysis page only appears after a generation, so all generated).
3. `subscribers` with `source IS NULL` (captured 07-03 to 09-06 by an older capture point; find it with
   `git log -S "api/subscribe" -- public/index.html`). If that capture point sat after a generation, they are
   generators; if not provable, use the **signed-up variant** of the email (below), never the generator wording.

Exclude:
- Dan and test addresses: `danroseconsulting`, any `@absbyai.com`, `@absbyai-test.com`, `@example.com`,
  `@sixpackabs.com`, `local.test`.
- `subscribers` with `unsubscribed`, `excluded` or `deleted_account` true.
- `source = 'sixpackabs'` (newsletter signups from sixpackabs.com, not generators).
- The 3 `membership_status = 'comp'` beta testers: list them separately for Dan; he decides whether to call them
  himself. They are not prospects.
- De-duplicate by lower-cased email across both tables.

Two people get their own email (identify them in Stripe, `STRIPE_SECRET_KEY`, never print the address in chat):
- **The declined-card annual buyer:** subscription created 2026-08-25, $69.99/yr, first charge failed 09-01,
  auto-cancelled.
- **The 09-20 Google Ads trialer:** monthly trial created 2026-09-20, `cancel_at_period_end` true, trial ends 09-27.
  Confirm it is still set to cancel (so "nothing will be charged" is true) right before sending.

Get a first name from Stripe `customer.name`, `users.profile`, or the part of the email before `@` only if it is
obviously a name; otherwise open with "Hey there".

## Step 2: prepare drafts, then get one approval

Create one **Gmail draft per person** in danroseconsulting@gmail.com (Gmail connector `create_draft`), plain text,
one recipient each (no CC/BCC blast). Check first whether Gmail has a send-as for dan@absbyai.com; if it does,
send from that address (the brand), otherwise from the Gmail address. Replies must land in Dan's inbox either way.

Then send Dan **one** approval message in chat: count per segment, the comp list, the exact copy of each variant,
and "drafts are in Gmail for you to spot-check." On his yes, send them (`send_message` or send the drafts), trialer
first.

### Copy (Dan's voice; the executor may only fill the brackets)

**A. Generators** · Subject: `Your abs picture`

> Hey [first name],
>
> It's Dan Rose. I built Abs By AI, and I saw you made your AI abs picture a little while back.
>
> I'd like to get on the phone with you for 15 minutes. I'll look at where you're at now, tell you exactly what
> I'd do in your shoes to get to that picture, and answer anything you want to ask. If it makes sense, I'll also
> show you how the app would build your plan. The call is free.
>
> If you're up for it, just reply with a couple of times that work this week or next, your time zone, and the best
> number to reach you. I'll call you.
>
> Talk soon,
> Dan

**A2. Signed up, generation not provable** · Same as A, with the first paragraph replaced by:
> It's Dan Rose. I built Abs By AI, and you signed up at absbyai.com a little while back.

**B. The 09-20 trialer** · Subject: `Quick question about your trial`

> Hey [first name],
>
> It's Dan Rose. I built Abs By AI. I saw you started the free trial and then cancelled it. No problem at all, and
> nothing will be charged.
>
> I'd really like to know what made you decide against it. Even one line helps me a lot.
>
> And if you're up for a free 15-minute call, I'll personally go over your picture and what I'd do to get there.
> Just reply with a couple of times, your time zone and your number.
>
> Dan

**C. The declined-card annual buyer** · Subject: `Your Abs By AI annual plan`

> Hey [first name],
>
> It's Dan Rose. I built Abs By AI. You picked the annual plan back in August, but the card didn't go through and
> your account closed. That's on us for not following up sooner.
>
> If you still want in, I'd like to set you up myself. Reply with a couple of times, your time zone and your
> number, and we'll do a quick 15-minute call where I go over your plan and get your membership back on.
>
> Dan

**Footer on every email** (plain text, below the signature):
> If you'd rather not get emails from me, just reply "stop" and I'll take you off the list.
> [MARKETING_ADDRESS]

**Follow-up, once, 3 to 4 days later, only to people who have not replied** · Reply in the same thread:
> Hey [first name], just bumping this in case it got buried. Happy to do 15 minutes whenever works for you. Dan

## Step 3: handle replies

- Watch Dan's inbox (Gmail `search_threads`) for replies to these threads. For each "yes", put a **draft reply**
  confirming one of their offered times and create a 15-minute calendar hold on Dan's Google Calendar
  (Central time, title `Abs By AI call: [first name]`, phone number in the private description). Tell Dan which
  holds were added. Dan confirms times himself if the draft needs judgment.
- "stop": set `subscribers.unsubscribed = true, unsubscribed_at = now()` for that email (reversible row update),
  and never email them again.
- A "no" with a reason: log the reason. Do not argue.

## Tracking (outside the repo, never committed)

`~/Documents/Abs By AI private/generator-outreach-2026-09.csv` (create the folder, mode 0700). Columns:
`first_name, email, segment (A/A2/B/C), source, generated_on, sent_at, followup_at, replied, call_booked,
call_done, outcome (paid/trial/no/no-reply), objection`. Dan fills `call_done`, `outcome` and `objection` after
each call, or tells a session and it fills them.

## Call guide for Dan (give it to him with the approval message)

1. Where are you now, what's the goal, and by when?
2. What have you tried before? What got in the way?
3. What went through your head when you saw your picture?
4. Give one specific, real tip from your own routine (8 am gym, glycine, meals earlier, whatever fits them).
5. Offer: "The app builds this plan for you and adjusts it as you go. It's $19.99 a month or $69.99 a year, and
   the first 7 days are free. Want me to walk you through signing up right now?" (absbyai.com → generate → cart).
6. If no: "What would make it worth it for you?" Write the answer down word for word.

## Done means

- Every eligible person emailed once (after Dan's approval), follow-up sent, replies handled, calendar holds made.
- On **2026-10-08** report in chat: sent, replied, calls booked, calls done, paid, trials, and the objections
  grouped by theme. That report is the input to the 10-12 checkpoint and the 10-26 fold decision.
- Delete this handoff's row from `Handoffs/README.md` and its line from the HANDOFFS section of
  `AI_COORDINATION.md`. No dashboard row unless Dan asks.

## Open risks

- The list is small (15 to 20). Expect 2 to 5 replies. That is still the cheapest signal we can buy.
- Stripe failed-payment recovery (Smart Retries + emails) is still off; turning it on is a separate change Dan
  should approve so the next declined card is not silently lost.
- If Gmail has no send-as for dan@absbyai.com, the emails come from danroseconsulting@gmail.com. That is fine for
  personal 1:1 outreach; flag it in the approval message.
