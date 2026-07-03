# Abs by AI — Email Marketing Plan (MailerLite)

Created 2026-07-03. Covers: capture → MailerLite sync → autoresponder setup → product email copy → affiliate email copy (later).

---

## 1. How we collect emails

Current state: the email screen in `index.html` only does `localStorage.setItem('absbyai_email', email)` — nothing reaches the server.

**Changes:**

- **Frontend** (`index.html`, `emailForm` submit handler): after saving to localStorage, `POST /api/subscribe` with `{ email, deviceId }`. Fire-and-forget — never block the user's path to the product screen if the request fails.
- **Backend** (`server.js`): new `POST /api/subscribe` endpoint that:
  1. Validates the email format.
  2. Appends to `subscribers-data.json` persisted to the GitHub repo (same pattern as `credits-data.json`) — we always own the raw list, independent of MailerLite.
  3. Pushes to MailerLite via API (below). Idempotent — MailerLite upserts on email, and we skip the API call if the email is already in our local store.
- **Consent line** under the email input: *"We'll email you your image plus fitness tips and offers. Unsubscribe anytime."* — this is what makes later affiliate sends legitimate.
- **PostHog**: capture an `email_subscribed` event so signup rate is visible in analytics.
- **Privacy policy**: add/update a page covering email collection before affiliate sends start.

> Note: the repo holding `subscribers-data.json` must stay **private** — it will contain PII.

## 2. Sending to MailerLite

- Env var on Railway: `MAILERLITE_API_KEY`.
- API call: `POST https://connect.mailerlite.com/api/subscribers` with `Authorization: Bearer <key>`, body:
  ```json
  { "email": "...", "groups": ["<GROUP_ID>"], "fields": { "device_id": "..." } }
  ```
- **MailerLite setup checklist (manual, one-time):**
  1. Create group **"Abs by AI Users"** → copy its ID into a `MAILERLITE_GROUP_ID` env var.
  2. Authenticate the domain: add MailerLite's SPF + DKIM DNS records for **absbyai.com**. Do this before any sending — it's the single biggest deliverability lever.
  3. Sender identity: **Dan from Abs by AI <dan@absbyai.com>** (a real mailbox that receives replies — replies boost sender reputation).
  4. Single opt-in (the download unlock is the confirmation of intent; double opt-in would leak subscribers).
  5. Complete MailerLite's account-approval questionnaire (they review new accounts, usually <1 day).

- **Later option (phase 2):** host each user's generated image at a stable URL (persist to repo or reuse the Printify upload URL), pass it as a MailerLite custom field `image_url`, and embed it in Email 1 so their future self is *in the inbox*. Not required for launch.

## 3. Autoresponder structure

One MailerLite automation, trigger: **"subscriber joins group 'Abs by AI Users'"**.

| # | Timing | Job | Promotes |
|---|--------|-----|----------|
| 1 | Immediately | Deliver value, set expectations | (none — trust) |
| 2 | +1 day | Print upsell at peak motivation | Canvas/poster |
| 3 | +3 days | Value content: the 3 levers | Macro tracker |
| 4 | +5 days | Generate more versions | Credit packs |
| 5 | +7 days | Identity/consistency story, second print ask | Canvas/poster |
| 6 | +10 days | *(affiliate, later)* eat like your future self | Meal delivery |
| 7 | +14 days | *(affiliate, later)* track what you eat | Macro app / supplements |
| 8 | +21 days | *(affiliate, later)* train at home | Equipment/program |

Emails 6–8 are written below but **left out of the automation until affiliate accounts are approved** — just append them to the same automation later; new subscribers flow straight through.

Broadcasts stay off until the list is a few thousand; the sequence does the work.

---

## 4. Product autoresponder copy

Sender for all: **Dan from Abs by AI**. Keep plain-text-looking formatting (better inboxing than heavy HTML).

### Email 1 — Immediately
**Subject:** Your future self is ready 💪
**Preview text:** Save this image somewhere you'll see it every day.

> Hey — it's Dan from Abs by AI.
>
> You just did something most people never do: you actually *looked* at where you're headed. That image isn't a fantasy — it's a target.
>
> Here's what to do with it right now:
>
> **1. Set it as your lockscreen.** You unlock your phone ~150 times a day. That's 150 reminders of where you're going. (Your watermark-free download is unlocked on [absbyai.com](https://absbyai.com) — grab it if you haven't.)
>
> **2. Tell one person.** Goals you say out loud are the ones that happen.
>
> Over the next week I'll send you a few short emails on how people actually close the gap between the before and the after photo. No fluff, no 45-minute YouTube videos — just the stuff that works.
>
> Talk soon,
> Dan
>
> P.S. Hit reply and tell me your goal. I read every one.

*(The P.S. is a deliverability play — replies are the strongest positive signal an inbox provider sees.)*

### Email 2 — Day 1
**Subject:** Put your future self on the wall
**Preview text:** There's a reason boxers hang the belt photo in the gym.

> Quick question: where's your image right now?
>
> If the answer is "buried in my camera roll," it's already losing power. Motivation research is boringly consistent on this — visual cues in your environment beat willpower every time. Out of sight, out of mind isn't a cliché, it's how your brain works.
>
> That's why we print them.
>
> **Your future self, on canvas, on your wall.** Gym corner, home office, bathroom mirror wall — wherever you'll see it when the 6am alarm goes off and you're negotiating with yourself.
>
> - Poster from **$18**
> - Gallery canvas from **$34**
> - Framed canvas from **$75**
>
> [→ Print my future self](https://absbyai.com)
>
> Every morning it asks you one question: *are we doing this or not?*
>
> — Dan

### Email 3 — Day 3
**Subject:** The 3 levers (ignore everything else)
**Preview text:** The entire fitness industry, compressed into one email.

> The fitness industry makes money by making this complicated. It isn't. Getting from your before to your after is three levers:
>
> **1. Calorie deficit.** You cannot out-train a surplus. A modest deficit (300–500 cal/day) loses fat without wrecking your energy.
>
> **2. Protein.** Roughly 0.7–1g per pound of goal bodyweight. It protects muscle while you cut and keeps you full. Most people are at half that.
>
> **3. Consistency over intensity.** Four okay workouts a week for a year beats two perfect weeks followed by quitting. Every time.
>
> That's it. Lever 1 and 2 are won or lost in the kitchen, which is why we built a **free macro tracker** into Abs by AI — snap your meal, get calories and protein instantly. No accounts, no BS.
>
> [→ Track a meal in 10 seconds](https://absbyai.com)
>
> — Dan

### Email 4 — Day 5
**Subject:** What does 6 months vs. 2 years look like?
**Preview text:** Most people stop at one version. Big mistake.

> Here's something interesting from our data: the people most likely to actually follow through generate **more than one** future self.
>
> Makes sense when you think about it —
>
> - The **6-month version**: realistic, near, keeps you honest
> - The **2-year version**: the full transformation, keeps you dreaming
> - The **"what if I really committed"** version: your ceiling
>
> One image is a picture. A progression is a plan.
>
> You've got credits waiting at [absbyai.com](https://absbyai.com) — and if you're out, the Starter Pack is **5 generations for $4.99** (Power Pack: 20 for $14.99). Try different timeframes, different goals, even different styles.
>
> [→ Generate my 2-year self](https://absbyai.com)
>
> — Dan

### Email 5 — Day 7
**Subject:** You're not "trying to lose weight"
**Preview text:** The identity shift that makes it stick.

> One week since you saw your future self. Here's the mental trick that separates people who make it from people who don't:
>
> Stop saying "I'm trying to lose weight." Start saying "I'm becoming *that guy/girl*" — the one in the image.
>
> James Clear calls it identity-based habits: you don't chase outcomes, you vote for an identity. Every workout is a vote. Every tracked meal is a vote. Skipping one isn't failure, it's just a vote the other way — win the count, not every ballot.
>
> This is exactly why a printed future self works so well. It's not decor. It's your identity, staring back at you, asking for your vote today.
>
> If you didn't grab one last week: [posters from $18, canvas from $34 →](https://absbyai.com)
>
> Proud of you for still being here. Most people's motivation died 6 days ago.
>
> — Dan

---

## 5. Affiliate autoresponder copy (add later)

Rules: one offer per email, framed as a recommendation, always `[AFFILIATE_LINK]` placeholder + required disclosure line. Add to the automation only after affiliate approvals.

**Disclosure footer for all affiliate emails:**
*Heads up: links in this email may earn Abs by AI a commission at no extra cost to you. We only recommend things that move the three levers.*

### Email 6 — Day 10 · Meal delivery (Factor / Trifecta / CookUnity)
**Subject:** The lazy way to eat like your future self
**Preview text:** Remove the decision, remove the failure point.

> Real talk: most diets don't fail at the gym. They fail at 7pm on a Tuesday when you're tired, hungry, and the pizza app is right there.
>
> The fix isn't more discipline. It's **removing the decision**.
>
> That's the whole case for macro-friendly meal delivery like **[Factor / Trifecta]** — pre-made, portioned, high-protein meals in the fridge. When dinner takes 2 minutes and already fits your macros, lever #1 (deficit) and lever #2 (protein) handle themselves.
>
> [→ Try [OFFER] — [intro discount] for Abs by AI readers]([AFFILIATE_LINK])
>
> Your future self doesn't cook better than you. He just decided fewer times.
>
> — Dan

### Email 7 — Day 14 · Macro app or protein (MacroFactor / Legion / MyProtein)
**Subject:** You can't fix what you don't measure
**Preview text:** The #1 predictor of who actually transforms.

> Two weeks in. Time for the unsexy truth:
>
> In basically every study on successful fat loss, one behavior predicts success more than any other — **self-monitoring**. People who track what they eat lose 2–3x more than people who wing it. Not because tracking burns calories, but because you can't negotiate with a number.
>
> Our built-in macro tracker is perfect for quick checks. If you're ready to go a level deeper, **[MacroFactor]** is the app I'd pick — it learns your actual metabolism and adjusts your targets weekly, so plateaus don't stall you out.
>
> [→ Get [OFFER]]([AFFILIATE_LINK])
>
> *(Struggling to hit protein instead? A scoop of [whey] is 25g for ~120 calories — the best deal in nutrition: [AFFILIATE_LINK])*
>
> — Dan

### Email 8 — Day 21 · Home equipment or program
**Subject:** The $50 gym that's open at 6am
**Preview text:** Three weeks in — time to make it frictionless.

> Three weeks. If you've been moving, you're past the phase where most people quit. Now make it *easier to continue than to stop*.
>
> The biggest hidden killer of consistency is friction: the drive to the gym, the packed parking lot, the "I'll go tomorrow." Every minute between "I should work out" and actually working out is a chance to bail.
>
> A pair of **adjustable dumbbells** and a **$20 pull-up bar** in the corner of your room delete all of it. Roll out of bed, 30 minutes, done before your brain objects.
>
> [→ The home setup I recommend]([AFFILIATE_LINK])
>
> You've already seen where this ends — it's on your lockscreen. This just shortens the road.
>
> — Dan

---

## 6. Implementation checklist

- [ ] Dan: MailerLite account created + approved
- [ ] Dan: SPF/DKIM DNS records added for absbyai.com
- [ ] Dan: create group "Abs by AI Users", get `MAILERLITE_GROUP_ID`; set `MAILERLITE_API_KEY` + group ID on Railway
- [ ] Code: `POST /api/subscribe` (local store + MailerLite push)
- [ ] Code: frontend calls `/api/subscribe`; consent line under input; PostHog `email_subscribed` event
- [ ] MailerLite: build automation with Emails 1–5
- [ ] Test: subscribe with a real address, verify sequence fires, check spam placement (Gmail + Outlook)
- [ ] Legal: privacy policy page updated
- [ ] Later: apply to affiliate programs (Factor/Trifecta, MacroFactor, Legion/MyProtein, Amazon Associates); append Emails 6–8
