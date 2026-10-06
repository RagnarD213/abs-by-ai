---
name: explain-simply
description: "Dan wants all explanations in simple, non-technical language; for multi-step account/dashboard walkthroughs, use the confirmed one-step-at-a-time template"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5f1252c4-a943-4537-96a3-dabf348e896a
  modified: 2026-07-23T22:23:40.570Z
---

When explaining anything to Dan (especially manual steps in dashboards like Stripe, Railway, MailerLite, Apple Developer, Google Play, Replicate), use plain non-technical language with numbered click-by-click steps.

**Why:** Dan said "always explain things like that to me" when asking for a simple walkthrough of a Stripe setup step (July 2026).

**Confirmed template — walkthrough/concierge tasks (2026-07-23):** Dan explicitly praised the step-by-step process used in the "three unblock actions" session (Apple enrollment check, Play Console verification, Replicate token → Railway) as much easier to follow than prior attempts that got "too complex and technical" and left him "bogged down." Make this the standard for any multi-step task where Dan is clicking through a website/dashboard himself:

1. **One atomic step per message.** Give a single action ("Go to X," "Click Y"), not a bundle of 3-4 steps at once.
2. **Stop and wait for confirmation** after each step before giving the next one — don't pre-load the next 3 steps "just in case."
3. **Dan sends a screenshot; read it and verify, don't just take his word.** Confirm explicitly what's on screen matches expectations before advancing (e.g., "Good — I can see X in the top right, confirming Y").
4. **If the screenshot reveals the task is already done, further along, or different than expected, say so plainly and skip ahead** — don't march through steps that no longer apply.
5. **No unexplained jargon.** If a technical term is unavoidable, translate it in the same sentence.

**Reinforced 2026-07-23 (iOS App Store submission).** Dan flagged this sentence as exactly what NOT to write: *"The build is the only thing I genuinely can't move without you — .p8 into ~/.appstoreconnect/private_keys/, then paste me the Issuer ID."* Three unexplained things in one line (what a `.p8` is, a filesystem path he'd have to navigate, an "Issuer ID"), and it cost a full round trip to explain. This slippage happens most often in **status summaries and wrap-up tables at the end of a long working session** — the walkthrough steps get written carefully, then the recap reverts to shorthand. Apply the same plain-language bar to summaries, tables, and "next steps" lines as to the numbered walkthrough itself. Filenames, file paths, env-var names, and API terms all need a plain-English gloss or a click-by-click alternative every single time, no matter how many times they've appeared earlier in the conversation.
6. **End each completed task with a plain summary of what just happened and why it matters**, plus (if relevant) the exact copy-paste prompt for the next Claude Code session — Dan shouldn't have to remember or reconstruct next steps himself.
7. Never ask Dan to paste secrets/tokens/passwords into chat — have him copy/paste directly between the two provider dashboards himself.

**How to apply generally:** No jargon without a one-line plain-English translation. Prefer "click X, then you'll see Y" style. Code-level detail is fine in commits/files, but the chat summary to Dan should read like instructions for a smart friend who doesn't code. For manual account/dashboard walkthroughs specifically, follow the numbered template above.
