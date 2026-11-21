---
name: absbyai-inbound-email
description: dan@absbyai.com receives mail via Namecheap forwarding to Gmail; the Mail Settings mode gotcha and why Gmail self-tests give false negatives
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2bd72eb9-34e3-4b29-828d-638ec7d60c19
  modified: 2026-07-22T20:06:08.363Z
---

`dan@absbyai.com` is a **Namecheap email forwarder** to `danroseconsulting@gmail.com` (no real mailbox, no paid product). Set up 2026-07-22 to receive the Play Console org-verification email. This is separate from its role as the Resend *sending* identity — see [[resend-welcome-autoresponder]].

**The mode gotcha that wasted the most time:** a forwarder alias in Namecheap does nothing unless Advanced DNS → **Mail Settings** is set to `Email Forwarding`. Under `Custom MX` the alias list is ignored entirely and the Domain tab reads "Your domain is using other email service." Symptom of the broken state is a 16-second hard bounce: `554 5.7.1 <addr>: Relay access denied` from `eforwardN.registrar-servers.com` — MX pointing at the forwarders with no active alias.

**Switching that mode is not cosmetic.** It stages a rewrite of the *entire MX table plus the root SPF TXT* — it would have dropped the `send` MX (SES bounce handling) and stripped `include:_spf.mlsend.com`. Snapshot every record first and re-verify against `dns1.registrar-servers.com` after. Nothing was lost in the end, but don't assume MX and TXT are independent.

**Namecheap saves can silently roll back.** The first "Save All Changes" appeared to work and did nothing; the page showed `Custom MX` again on reload. Always confirm by reloading, never by the click returning cleanly.

**Never test a forward by mailing it from the account it forwards to.** The forwarded copy keeps the same Message-ID as the Sent copy and Gmail silently drops duplicates, so a *working* forward shows nothing in the inbox (and nothing in Spam/All Mail). Test from a different sender, or infer success from the absence of a bounce.

Port 25 is blocked from Dan's machine, so SMTP `RCPT` probes aren't available for diagnosis — use bounce messages instead.

Open, non-urgent: root SPF still carries an unused MailerLite include, and DMARC is `p=none`.
