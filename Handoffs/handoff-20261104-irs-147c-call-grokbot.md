# Handoff: IRS Letter 147C phone call (2026-11-04)

**Type:** ops, not video. **Who runs it:** Grokbot, with Dan present on the line. **Goal:** get an IRS Letter 147C (EIN verification letter) for the LLC that will own the SixPackAbs Shopify store, so Shopify Payments verification can finish.

## Context

- Shopify Payments asks for a government-issued business document: IRS Letter 147C, or an IRS SS-4 confirmation / CP575 notice. Registered name and EIN on the form must match the document exactly.
- Dan has an EIN PDF for SIX PACK ABS DOT COM LLC (`SIX PACK ABS DOT COM LLC - EIN Assignment.pdf`, Drive) and a Google Doc "Rose Digital Holdings LLC EIN". Neither has been confirmed to be an accepted IRS notice. Dan should check both first; if one is a real IRS notice for the LLC he wants on the store, no call is needed.
- Dan cannot receive a fax. He chose to have the call placed with Grokbot.

## Rules for the call (Dan's call, written 2026-11-04)

- **Dan is on the line.** The IRS verifies the caller as the LLC's responsible party by name and Social Security number. Grokbot asks Dan for each verification detail live, Dan says it himself, and Grokbot does **not** record, transcribe, store or repeat the SSN or EIN anywhere (no notes, no logs, no chat output).
- If the IRS agent asks to speak to the responsible party, hand over to Dan at once. Do not claim to be Dan.
- Say plainly if asked that an assistant is helping on a call with the owner present.
- Do not agree to anything beyond sending the 147C (no changes to the account, address, or responsible party).

## Call details

- Number: **800-829-4933**, IRS Business & Specialty Tax Line. Monday to Friday, 7 am to 7 pm local time. Expect a long hold; use the callback option if offered.
- Say: "I need a Letter 147C, the EIN verification letter, for [exact LLC name]. Please fax it today if you can."
- Delivery: Dan cannot receive a fax directly. **Before the call**, set up one of: an online fax number (eFax or Fax.Plus, which email the fax to Dan as a PDF; check current price and trial terms), or a FedEx Office / The UPS Store fax number (small per-page fee, Dan picks it up). Give the agent that number. Mail is the fallback (takes weeks).
- Ask the agent to confirm the registered name and EIN spelling on the letter so they match Shopify's form.

## Done looks like

A 147C PDF (or scan, JPG/PNG/PDF under 10 MB) in Dan's hands, name and EIN matching the Shopify Payments form. Dan uploads it himself in the "Business document" slot (Claude cannot upload IRS documents or ID). Then Dan finishes the identity step with his driver's license (Drive: "driver's license - daniel rose.jpg", front, and "license back.jpg").

## Starter prompt

> Dan is on the line with me. We are calling the IRS Business & Specialty Tax Line at 800-829-4933 to request a Letter 147C (EIN verification letter) for [EXACT LLC NAME]. I read the script from `Handoffs/handoff-20261104-irs-147c-call-grokbot.md`. Dan supplies his own name, Social Security number, and EIN out loud. Do not record or repeat any identifier. Ask the IRS to fax the letter to [FAX NUMBER] and confirm the name and EIN spelling.

## Recommended model

Whichever Grokbot voice/phone model Dan uses; no Claude or Codex model needed. Claude Sonnet 5.5 medium can prepare the fax number and later check the uploaded document name against the form.
