# AppleCare coverage check: M6 and M2 Mac minis (2026-11-24)

For Codex (GPT-6.2 Sol, medium) AND Grokbot. One of you does the whole step; whoever starts first writes "claimed by <name>" below.
Dan authorizes everything in this brief, including signing in to his Apple Account (Grokbot has the password vault), solving the Apple CAPTCHA, and reading his device coverage. Do not stop to ask him.

## Goal
Find out exactly which of Dan's devices AppleCare One covers, and whether the M6 Mac mini is covered. Report back the facts so Claude can finish the recommendation.

## Facts so far (Claude, 2026-11-24)
- M6: Mac mini, chip Apple M6, model Mac18,5, serial X1GX7TMQ0P, macOS set up Nov 13, 2026. Hostname m6.
- M2: Mac mini (M2 Pro), headless, reachable only on its own network (ssh to 10.66.0.2 timed out from the M6).
- Dan's screenshot (System Settings, AppleCare & Warranty, on the device named "M2") showed: AppleCare One plan has 3 covered devices; this M2 was offered "Add to AppleCare One Individual" at $5.99/month, "Get AppleCare+" for this Mac mini only at $3.99/month (marked Recommended), or "Swap AppleCare One Devices". Sidebar: "Eligible to Renew AppleCare, 16 days left to protect your Mac."
- Claude could not read the M6's coverage: System Settings access was declined, and Apple's coverage site needs sign-in or a CAPTCHA.

## Steps
1. On the M6: System Settings > General > AppleCare & Warranty. Record every device listed, its coverage status (covered by AppleCare One, AppleCare+, limited warranty, expired), the end date, and the monthly price. Specifically whether the row for the M6 (serial X1GX7TMQ0P) says covered.
2. If that pane is not enough, sign in at https://checkcoverage.apple.com/ (or account.apple.com, Devices) and read the same for serial X1GX7TMQ0P and for the M2.
3. Read the M2's own row: coverage status, expiry date, and the exact days left on its renewal window.
4. Do NOT buy, add, swap or renew anything. Read only. Dan decides after Claude's recommendation.

## Report (append below, no secrets, no full serial list beyond the two Macs)
- Devices on the AppleCare One plan (names and types):
- M6 coverage status and end date:
- M2 coverage status, end date, renewal window:
- Prices shown for adding the M6 and the M2:

Then tell Dan in chat, and update `Handoffs/README.md` (remove this line from OPEN).
