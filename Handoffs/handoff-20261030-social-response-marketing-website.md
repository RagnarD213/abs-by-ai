# Handoff: New Social Response Marketing website

**Date:** 2026-10-30
**Project:** Social Response Marketing (Dan's YouTube ad agency), serving the Upwork Clients task
**Business goal this serves:** profitability: first paying ad clients
**Task name:** SRM Website
**Status:** Ready. Interview Dan first. Build nothing until the interview is done.

## Objective

Build a new website for socialresponsemarketing.com that makes a cold prospect believe Dan and book a call. Today the domain has no agency site, so anyone who gets an outreach email and checks him out lands on a fitness site. This task **interviews Dan first**, then designs the site, shows it to him for review and only then publishes it.

## Current State

- **Domain:** registered at Bluehost, DNS on Dan's Cloudflare account (`danroseconsulting@gmail.com`).
- **What's live:** a Cloudflare redirect rule, "Send to SixPackAbs", sends the whole domain to https://sixpackabs.com/ with a 301 (rule id `7c329ffc42174f448f699a186f97cf05`, zone `a0ed7d3414f8b76d361c0fe41dd8c403`). Confirmed still live 2026-10-30. Going live means deleting this rule, which is the undo as well.
- **Old site:** WordPress and Elementor on a server owned by Dan's developer (AWS 52.14.128.35). That server died in September 2026. The DNS A record still points at it. Do not try to revive it.
- **Last archived copy, June 2025:** http://web.archive.org/web/20250623120223/https://socialresponsemarketing.com/ . It headlined "The World's Leading YouTube Marketing Agency" and "We teach entrepreneurs...", and it sold a $950 course, a free book, strategic coaching and agency work (minimum $100,000 a month in ad spend), plus a careers section. It carried three client testimonials and press logos. That was a teaching business. The new job is different.
- **Email:** dan@socialresponsemarketing.com forwards to Dan's Gmail through Cloudflare Email Routing, and Gmail sends as that address. SPF exists. There is no DMARC record and no Google DKIM for the domain. Dan chose this address for outreach on 2026-10-30.
- **Outreach is waiting on this site.** Dan wrote the email himself: `.claude/skills/upwork-pitch/TEMPLATE-outreach-email.md`. First send is Built With Science.

## Key Decisions Already Made

- **Dan wants the site redone.** His words, 2026-10-30: "I need to redo that website."
- **The job of the site is to support a cold email.** A prospect clicks through to check Dan out, then books a call. Everything else is secondary.
- **The offer is Dan's own:** a complete free ad plus a variation of their best ad, then a 15-minute call. Do not put the Upwork $75 and $150 trials on this site unless Dan asks.
- **Claude's recommendation, not yet approved by Dan:** one page only. Headline number, top ads, the free-ad offer, pitch video, Calendly link. Ask him; he decides.
- **Lifetime ad spend numbers are official.** Read memory `official-ad-spend-numbers`. Use them exactly, and never say the whole Healthy Back Institute figure ran on Dan's own creative. Per-ad figures and ad links are in the template.
- **Dan is the proof.** He wrote, directed and ran the spend on these ads; a human editor cut them.

## Detailed Plan

1. Read memories `official-ad-spend-numbers` and `socialresponsemarketing-email`, then `Docs/DESIGN_QUALITY_LESSONS.md`, `.claude/skills/upwork-pitch/TEMPLATE-outreach-email.md`, `Handoffs/upwork-profile-draft.md`, `Handoffs/upwork-profile-working-brief.md`, and the archived site above. Do not make Dan repeat anything these already answer.

2. **Interview Dan.** Ask a few questions at a time in plain language, and use his answers to decide what to ask next. Most of his answers are dictated. Stop when you can write the page. Cover at least:
   - **Who it's for:** which buyers matter most (founder, head of growth, agency), and which brands he wants or doesn't want.
   - **The first impression:** what a prospect should feel in 10 seconds, and any agency or personal sites he admires or hates.
   - **What he sells on the site:** done-for-you ads, Google Ads management, audits, or only the free-ad offer. Whether prices appear. Whether the old $100,000 a month minimum stays. Whether the free offer goes to everyone or is tiered (his call is still open: full free ad for high-value prospects, free variation only for lower-value ones).
   - **Scope:** one page or several. Whether the book, the course, the careers section or anything else from the old site comes back.
   - **Voice:** "we" (agency) or "I" (Dan). Is he comfortable with "CEO" and the agency being current? Does he mention AI in his process at all?
   - **Proof he can use:** which client names, ads and numbers can appear publicly. Are the three old testimonials real and still usable, and can he get new ones? Which press logos are true? Any case studies he wants told.
   - **Assets:** photo of himself, pitch video status, Calendly link, any logo he wants kept.
   - **Branding:** keep any old look, or start fresh.
   - **The call to action:** Calendly, a form, or both. Where leads go.
   - **After launch:** does he want to edit it himself?

3. Write a short site plan from the interview (sections, words, what proves what) and get Dan's yes before designing.

4. Design it. Critique desktop and phone visually before showing Dan. Follow `Docs/DESIGN_QUALITY_LESSONS.md`. Choose where the site is hosted (OPEN, see below) and say why in one line. Images of Dan are real photos; any generated image goes through `.claude/skills/_shared/codex-image.sh`.

5. Show Dan a private preview. Run his revisions. **Do not publish until he approves.**

6. On his approval: publish, delete the redirect rule, point the domain at the site, and verify it live from outside Dan's network (see Things to Avoid). Check desktop and phone.

7. While in Cloudflare, add a DMARC record (routine email setup, already authorized). Tell Dan what's needed for domain DKIM before batch sending. Google Workspace on this domain, about $7 a month, is the likely route; that purchase and account are Dan's to make.

8. Update the "Upwork Clients" board entry (re-read from disk, edit only that entry), remove this handoff from the OPEN section of `Handoffs/README.md`, and push with `scripts/git/safe-push.sh`.

**OPEN:** hosting. Decide after the interview. It must be cheap, simple and independent of the abandoned server. Spending beyond routine hosting needs Dan's yes.

## Things to Avoid / Lessons Learned

- **Dan's home internet blocks this domain.** Optimum's home DNS sends it to a block page, so local DNS, WebFetch and the Browser pane all fail or mislead here. Verify from outside: Cloudflare DNS over HTTPS (`https://1.1.1.1/dns-query`) plus `curl --resolve`. Tell Dan to check the live site on phone data. It may need an allow-list entry for his house.
- **Cloudflare dashboard trap.** In Chrome, dash.cloudflare.com freezes the tab as soon as the Claude extension touches it. The desktop Browser pane works, but Dan must sign in there himself. The app's safety checks may also block some account changes; if so, tell Dan what to click.
- **Nameserver changes at Bluehost were blocked for Claude in September.** Dan had to do them himself.
- **The `presales` and `15steps` subdomains were dropped** in the September DNS move. Do not rebuild them unless Dan asks.
- **Do not use the old claims without asking,** such as "World's Leading". The revenue figures in the archive are confirmed in the working brief; check everything else with Dan.
- **The repo is public.** Do not commit prospect contact details, and keep spend numbers to what Dan approves for the public site.
- **Site copy follows the outward-facing writing rule in `AGENTS.md`.** Check every page for dashes before publishing.
- **Copy in Dan's voice** goes through the `dan-voice-writer` agent (memory `dan-voice-guide`). If its clean mode is logged out, say so.
- **No compliance commentary** unless the copy needs it; apply the rules on record briefly for page copy that ships.

## Relevant Files & Locations

- Email template and highlights: `.claude/skills/upwork-pitch/TEMPLATE-outreach-email.md`
- Skill and tracker: `.claude/skills/upwork-pitch/`
- Merged plan: `Docs/UPWORK_CLIENT_PLAN_MERGED_20261029.md`
- Profile copy and facts: `Handoffs/upwork-profile-draft.md`, `Handoffs/upwork-profile-working-brief.md`
- Design rules: `Docs/DESIGN_QUALITY_LESSONS.md`
- Upwork profile: https://www.upwork.com/freelancers/~016109a7105ec3bf5d

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Opus 5.5, high effort |
| **If Claude usage is high / approaching a limit** | Claude Opus 5.5, high effort for the interview, page plan, copy and design; newest Codex Sol, high effort, for the mechanical build once the design is approved |

Override: design and sales copy stay on Opus per Dan's routing and his cart-design benchmark.

## Starter Prompt for the Next Task

> Name this task SRM Website. Read Handoffs/handoff-20261030-social-response-marketing-website.md and do what it says. Start by interviewing me for context before you design or build anything. Ask a few questions at a time. Don't publish anything until I approve it.
