# Great Again T order emails from orders@sixpackabs.com: the Resend sign-in step (Codex and Grokbot)

Written 2026-11-18 by Claude (Fable 5.2). Website work, not video: no edit slot.
For **Codex (GPT-6.2 Sol, high) and Grokbot**. The only blocked part is signing in to Resend (a password), which Claude cannot type. Step 1 of `handoff-20261118-gat-one-page-checkout-go-live.md`.

Dan authorizes every step here: signing in to his Resend account, adding the sending domain and its DNS records, creating the key and setting it on Railway. Do not stop to ask him. No secret value goes into a repo file (the repo is public).

## Where things stand

- The Great Again T one-page order form is in Stripe LIVE mode (hidden at `?onepage=1`). Its order emails are sent by `gat-checkout.js` on Railway (service `abs-by-ai`, project invigorating-liberation) through Resend.
- The Railway `RESEND_API_KEY` is a sending-only key limited to absbyai.com, so order emails go out from `orders@absbyai.com` (`GAT_FROM` on Railway). They must come from `orders@sixpackabs.com` before the order form is shown to everyone.
- Resend is signed out in Dan's Chrome and in the Claude app's browser pane (both show resend.com/login, checked 2026-11-18 6:25 PM Central).
- DNS for sixpackabs.com is at WordPress.com (WordPress.com name servers). Existing records to leave alone: the root MX records (they forward support@ to Dan), the root SPF TXT `v=spf1 include:_spf.wpcloud.com ~all`, `_dmarc`, the two `wpcloud` DKIM CNAMEs, `shop`, `try`, `www`.

## Fastest path (Codex, on Dan's Mac)

Sign in to resend.com in Dan's Chrome and leave it signed in, or create a Full access API key in Resend and save it in `~/.absbyai-secrets.env` as `RESEND_FULL_ACCESS_KEY` (file mode 600). Then tell Dan "Resend is ready": Claude's go-live task does the rest in a few minutes.

## Full step (Grokbot, or Codex if it prefers)

1. Sign in at resend.com (Dan's account). Domains > Add domain `sixpackabs.com` (region: the same as the existing absbyai.com domain).
2. At WordPress.com (Domains > sixpackabs.com > DNS records) add exactly the records Resend shows: the DKIM TXT on `resend._domainkey`, and the MX and SPF TXT on the `send` subdomain. Do not edit or remove any existing record.
3. Back in Resend press Verify and wait until the domain says Verified.
4. API Keys > Create: name `gat-orders-sixpackabs`, permission Sending access, domain sixpackabs.com.
5. On Railway (service `abs-by-ai`) set `GAT_RESEND_API_KEY` to that key and `GAT_FROM` to `SixPackAbs.com <orders@sixpackabs.com>`. Save the key in `~/.absbyai-secrets.env` as `GAT_RESEND_API_KEY` if you can reach the Mac.
6. Report: the domain is Verified, the two settings are set. Claude then confirms a real order email arrives from orders@sixpackabs.com.

## Limits

No marketing email, no list email, no change to the absbyai.com domain or its key, no DNS deletions.

## Starter prompts

**Codex (GPT-6.2 Sol, high):**

> Read and execute `Handoffs/handoff-20261118-gat-order-email-sender-resend.md` in the Abs By AI project. Dan authorizes every step, including signing in to his Resend account. Take the fastest path in the file (sign in to Resend in Dan's Chrome and leave it signed in, or save a Full access key locally) unless you can finish the full step yourself. Do not stop to ask him. Keep secrets out of repo files.

**Grokbot (self-contained):**

> Set up the order-email sender for Dan Rose's shop (SixPackAbs.com). Dan authorizes every step, including sign-ins; do not stop to ask him. (1) Sign in at resend.com (Dan's account) and add the sending domain sixpackabs.com. (2) At WordPress.com, Domains > sixpackabs.com > DNS records, add exactly the records Resend shows (a DKIM TXT on resend._domainkey, and an MX and an SPF TXT on the send subdomain). Do not edit or remove any existing record, especially the root MX records. (3) In Resend press Verify and wait until the domain is Verified. (4) Create an API key named gat-orders-sixpackabs with Sending access limited to sixpackabs.com. (5) On Railway (project invigorating-liberation, service abs-by-ai) set GAT_RESEND_API_KEY to that key and GAT_FROM to "SixPackAbs.com <orders@sixpackabs.com>". (6) Report that the domain is Verified and both settings are set. Do not send marketing email, do not change the absbyai.com domain or its key, and do not delete any DNS record.
