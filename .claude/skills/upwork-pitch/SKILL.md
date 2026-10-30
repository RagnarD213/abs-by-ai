---
name: upwork-pitch
description: Find, score and pitch client work for Dan's direct-response video ad service, on Upwork (official connector only) and by cold email to brands and agencies, and learn from every edit Dan makes. Use whenever Dan asks for Upwork proposals, job picks, an outreach list, outreach emails, follow-ups, a reply to a prospect, or the state of the client pipeline, even if he doesn't say "/upwork-pitch". Delivering a won job uses the production skills (/scriptwriting, /ad-edit, /shortad-from-longform); this skill only wins it.
---

# Upwork pitch

The plan this skill executes: `Docs/UPWORK_CLIENT_PLAN_MERGED_20261029.md`. The rules below are its working core.
**Read `LEARNED.md` in this folder before drafting anything.** It holds the rules taken from Dan's edits; it wins over
this file where they disagree.

## Hard limits (Upwork's rules and Dan's)

- Upwork is touched by AI only through the official connector (`https://mcp.upwork.com/mcp`, claude.ai connector
  "Upwork"). No scraping, no browser bot reading job lists, no unattended bidding. Every proposal and message is a draft
  Dan confirms in Upwork; offers and money are accepted by Dan on upwork.com.
- One submitting session for the account at a time (the "Upwork Clients" task owns it).
- After a submit, reopen the proposal to confirm it is live. Never retry an uncertain submission blindly.
- No free or discounted work for Upwork reviews; no friends hiring for reviews. A real paid trial is fine.
- Never claim no AI is used. Never invent an observation about a prospect's ad.
- No em dashes in anything a client reads. Fixed price only, never hourly.
- Outreach email never goes from absbyai.com or Dan's main Gmail; only the outreach mailbox. First batch: Dan approves
  list and text once; later batches: one batch approval with a count.
- Every client video is categorised as AD before any editing.

## Offer ladder

| Product | Price | Scope |
|---|---|---|
| Ad Hook Fix (trial A) | $75 | Review one ad or script; 5 new hooks, 1 rewritten opening, short reasons; 1 revision; 2 business days after inputs |
| New Version of Your Ad (trial B) | $150 | 1 variation up to 60 s from supplied footage, 1 format, captions, 1 revision; 3 business days after inputs |
| Script / New versions / Audit / Finished ad | $350 / $450 / $750 / $950+ | Approved catalog packages |
| Weekly ad pack | $800 to $1,400 a month | New hooks, cuts and formats every week for one product |
| Start to finish + Google Ads management | $950+ and $2,500/month floor | Full service |

Trials exclude new filming, multiple formats, strategy and ad management. Trial price is credited toward any core
package ordered within 14 days. A job asking for full service gets the full package bid (Dan's favourite job), not a trial.

## Finding and scoring jobs

Search terms: direct-response video ads, ad scripts, supplement ad scripts, YouTube ad scripts, VSL, UGC ad variations,
Meta ad hooks, creative variations, ad editing, ad thumbnails, AI video ads, Google/YouTube Ads management.
Skip vlogs, weddings, general channel editing, podcast editing.

Score out of 100 (a decision aid, not a model): fit 30, clear scope and usable inputs 20, economics 20 (budget vs
Connects and hours), client signals 15 (payment verified, spend, hire rate, reviews), repeat potential 15.
Shortlist at 75+. Unknown facts stay unknown; a credible new client is not penalised.
Reject or clarify: unlimited revisions, big unpaid tests, sales guarantees, a whole marketing job for a tiny fee, a ban
on AI methods. Boost only the top-scored jobs.

## Proposal format

1. One specific, true observation about their ad or brief (watch their live ads first: Meta Ad Library, Google Ads
   Transparency Center). If they have no public ads, the observation is about the brief.
2. Three new hook ideas for their product.
3. The one most relevant proof, with Dan's exact role and its number:
   - supplements / health: Healthy Back Institute's #1 ad of all time ($5.96M spend; Dan wrote it, chose the
     testimonials, directed the edit, ran the spend); 4 of HBI's top 11 ads.
   - fitness: SixPackAbs.com, built with YouTube ads to $214M+ in revenue, 5.7M subscribers.
   - info products: Mind Movies and Spy Briefing (big-spend YouTube ads; Dan wrote, directed, ran spend).
   - general: ads that drove $238M+ in sales on YouTube.
   Portfolio items live on his profile: https://www.upwork.com/freelancers/~016109a7105ec3bf5d
4. Deliverable, price and timeline: the trial or the package that fits.
5. One question, plus direct answers to every screening question.

Short (about 120 to 180 words). Lead with money results. Plain, blunt, Dan's voice: sentences drafted by the
`dan-voice-writer` agent from a content plan built here (see memory `dan-voice-guide`).

## Outreach (engine 2)

**Use Dan's own email: `TEMPLATE-outreach-email.md` (2026-10-30). It replaces the teardown-and-hooks email and the Upwork trial ask.** The offer is one free complete ad plus a variation of their best ad, then a 15-minute call.
Who: brands that run video ads on Google and YouTube, because the email leads with those, or brands with a big organic YouTube presence that could expand into YouTube ads (Dan's call on Built With Science, 2026-10-30). Check Google's Ads Transparency Center (YouTube, video, last 30 days) before adding a brand.
Send from the outreach mailbox only, 5 a day building to 10, with one batch approval from Dan.

## Tracking

Everything lives on the "Upwork Pipeline" artifact (link in `TRACKER.md`), collection `items` (one document per
Upwork job ID or outreach prospect) and `spend`. Item states: `to_approve`, `approved`, `rejected`, `sent`,
`conversation`, `funded`, `submitted`, `accepted`, `released`, `available`, `withdrawn`, `no_reply`.
Read and write it with the ArtifactData tool. Weekly numbers: proposals and emails sent, reply rates, paid contracts,
revenue, Connects and costs, cost per paid contract, Dan's minutes.

## Training loop (do this every time Dan acts on the queue)

1. Read every item whose status changed since the last run (`decided_at` newer than `LEARNED.md`'s last entry).
2. For each item where `final_text` differs from `draft_text`, diff them. For each rejected item, read `dan_note`.
3. Write each lesson into `LEARNED.md` as a rule (what to do differently, one line, with the item id and date), an
   approved example (the final text, when Dan's edit is substantial), an intake question, or a check.
   Merge with an existing rule rather than adding a near-duplicate.
4. Track the edit rate in `LEARNED.md` (items approved unchanged / items decided). The goal is near copy-paste by
   about the 5th batch; when a rule stops being broken for 3 batches, leave it in place.
5. Push the skill folder with `scripts/git/safe-push.sh`.
