# HANDOFF — YouTube subscriber campaign: geo restructure (all-countries + tier-1 clone)

**Created:** 2026-08-22 · **Status:** NOT STARTED · **Owner:** unassigned
**Recommended model/effort:** **Opus 5, Medium.** This is careful UI/API execution against a
live ad account, not a reasoning problem. The judgment calls are already made below.

**Platform:** Google Ads → the existing YouTube subscriber campaign (Dan calls it the
"All Countries campaign"). **Bid strategy is Target CPA** — this fact drives several
decisions below, so re-verify it before starting.

---

## Why this is being done

Dan bought ~1,000 subscribers cheaply to clear the social-proof floor. He wants to keep
buying cheap volume toward 10,000 (his call — he believes sub count gates whether people
take the channel seriously, and he's the one who has watched his own audience), **while**
starting a separate, properly-funded push at the buyers who actually matter: US, Canada,
UK, Ireland, Australia, New Zealand.

The three tasks below are his, in his words:

1. Add every country to the All Countries campaign as a targeted location, so per-country
   stats are easier to see.
2. Exclude the extremely low-quality countries. **List is in this document, Section 3.**
3. Clone the campaign; the clone targets ONLY US, Canada, UK, Ireland, Australia,
   New Zealand.

---

## STEP 0 — Do this before touching anything (5 minutes, may reframe the whole job)

**Find out what conversion action the Target CPA campaign is optimizing toward.**

Earned subscribers are NOT a Google Ads conversion action — they're a YouTube earned-metric
that appears in reporting after the fact. So tCPA is optimizing toward *something else*
(site visits? signups? a page view?). Three possible findings:

| finding | what it means | what to do |
|---|---|---|
| A real conversion with decent volume (30+/mo) | Campaign works; subs are a side effect | Proceed as written |
| A conversion with near-zero volume | tCPA has nothing to learn from and is mostly guessing | Proceed, but flag to Dan — the clone should probably launch on **Maximum CPV**, not tCPA |
| No conversion action / misconfigured | The campaign has never optimized for anything meaningful | STOP. Tell Dan. This changes the plan |

Record the finding in this doc and in `AI_COORDINATION.md` before continuing.

---

## STEP 1 — Add every country as an explicit targeted location

**Where:** Campaign → Settings → Locations → Enter another location → bulk entry.
Google Ads accepts a pasted list; the per-campaign targeting limit is 10,000 locations, so
~250 countries is comfortably fine.

**Two things to tell Dan when reporting back:**

1. **This is partly redundant and he should know that.** The per-country stats he wants are
   *already* available without this change, under Reports → Locations → the user-locations
   report, even when targeting is set to "All countries and territories." Adding countries
   explicitly does not unlock new data. What it *does* buy him is editable per-country rows
   in the campaign UI, which makes exclusions and future adjustments much easier to manage.
   That's a real benefit — just not the one he expects.
2. **Watch for a learning-period reset.** Delivery should be identical (the same countries
   were already covered by "All countries"), but Google may still flag a significant-change
   learning period on a Smart Bidding campaign. If performance wobbles for a few days after
   this, that's the cause, not the geo change itself. Note the change date so it can be
   correlated later.

**Do NOT set location bid adjustments while doing this.** On Target CPA, non-device bid
adjustments are ignored entirely — the field accepts the number and the system disregards
it. This was verified against Google's docs on 2026-08-22. Setting them creates a false
belief that a lever is engaged when it isn't.

---

## STEP 2 — Apply the exclusions

Add every country in Section 3, Tier 1 as an **excluded** location on the All Countries
campaign. Bulk-paste is supported in the same Locations panel (Exclusions tab).

Leave the Tier 2 countries **targeted** — they are the cheap-volume engine that gets Dan to
10,000, and removing them defeats the purpose of keeping this campaign alive.

Do not apply any exclusions to the new tier-1 clone; its targeting is a strict allowlist, so
exclusions are unnecessary there.

---

## STEP 3 — Clone the campaign for tier-1 English markets

**Method:** Google Ads → select campaign → Edit → Copy, then Paste. Or use Google Ads Editor,
which is more reliable for this and lets you stage everything before posting.

**Clone settings — change these from the copied original:**

| setting | value |
|---|---|
| Name | something unmistakable, e.g. `YT Subs — Tier 1 English` |
| Locations | **ONLY** United States, Canada, United Kingdom, Ireland, Australia, New Zealand |
| Location options | Set to **"Presence: People in or regularly in your targeted locations."** The default ("Presence or interest") will serve ads to people *interested in* the US while physically elsewhere, which reimports the exact problem this campaign exists to avoid. **This is the single most important setting in the whole handoff.** |
| Budget | **Its own separate budget. NOT a shared budget with the original.** A shared budget pools the money and it drains toward the cheap geo again — which is the precise failure being designed around. Budget separation is the only mechanism Google gives you to force geo allocation. |
| Language | English |
| Target CPA | **Must be raised substantially** — see below |

**On the tCPA target for the clone:** if you copy the original's target, the clone will
barely spend or won't deliver at all. Tier-1 acquisition costs many times what the cheap geos
cost, and tCPA simply won't buy anything it can't hit. Set the clone's target well above the
original's, then let it settle for a week before judging. If Step 0 found weak conversion
volume, launch the clone on **Maximum CPV** instead and revisit — a brand-new campaign with
no conversion history is the worst case for Smart Bidding.

**Budget split (Dan's call, recommend this as the default):** most of the spend stays on the
cheap campaign until 10,000 is reached, since that's a defined finish line he wants crossed.
A smaller parallel spend on the tier-1 clone, run as a *learning* budget — its job right now
is to find out what a real US subscriber costs and whether they convert, not to scale.

---

## STEP 4 — Set up the measurement that decides what happens next

Two things need to be observable after this, or the restructure was pointless:

1. **UTM the channel link** in video descriptions using the project's existing UTM
   convention, so channel-driven site visits and signups are attributable.
2. **Establish the kill criteria now, before there's data to rationalize:**
   - On the tier-1 clone: judge it on **cost per site visit / signup**, not cost per
     subscriber. That's the whole reason it exists.
   - On the cheap campaign: check whether **organic** impressions and CTR hold up as the sub
     count climbs. Flat or growing → the cheap subs are harmless, keep going to 10k. Sliding
     → the subscriber-feed drag is real and the campaign should be stopped early.
   - Once 10,000 is reached, the cheap campaign gets **paused, not scaled**. The authority
     number is a one-time purchase.

---

## Section 3 — The exclusion list

Selection criteria, stated plainly so this can be re-derived or argued with: (a) countries
with effectively zero probability of purchasing a USD-priced fitness membership, combined
with (b) geos with a well-documented concentration of incentivized-view traffic, view farms,
and low-quality YouTube inventory. This is an assessment of *ad inventory and purchasing
power*, not of people.

### Tier 1 — EXCLUDE (apply all of these)

**South and Central Asia**
Bangladesh · Pakistan · Nepal · Sri Lanka · Afghanistan · Myanmar (Burma) · Cambodia · Laos ·
Mongolia · Uzbekistan · Kyrgyzstan · Tajikistan · Turkmenistan · Kazakhstan

**Sub-Saharan Africa**
Nigeria · Ghana · Kenya · Uganda · Tanzania · Ethiopia · Cameroon · Côte d'Ivoire · Senegal ·
Zimbabwe · Zambia · Mozambique · Angola · Sudan · South Sudan · DR Congo · Congo-Brazzaville ·
Madagascar · Malawi · Rwanda · Burundi · Somalia · Mali · Burkina Faso · Niger · Chad · Benin ·
Togo · Guinea · Sierra Leone · Liberia · Mauritania · Gambia · Lesotho · Eswatini

**Middle East and North Africa**
Egypt · Morocco · Algeria · Tunisia · Libya · Iraq · Yemen · Jordan · Lebanon · Palestine

**Latin America and Caribbean**
Venezuela · Bolivia · Nicaragua · Honduras · Guatemala · El Salvador · Paraguay · Haiti ·
Guyana · Suriname

**Eastern Europe / Caucasus**
Belarus · Moldova · Ukraine · Armenia · Azerbaijan · Georgia · Albania · Kosovo ·
North Macedonia · Bosnia and Herzegovina

**Pacific**
Papua New Guinea · Fiji · Solomon Islands · Vanuatu · Timor-Leste

### Not targetable anyway — don't waste time hunting for them

Google Ads does not serve these; they will not appear or will error:
**Russia** (suspended since 2022) · **Iran** · **North Korea** · **Cuba** · **Syria** ·
**Belarus** (may be partially restricted — exclude it anyway per Tier 1, harmless either way)

### Tier 2 — KEEP TARGETED (deliberately, do not exclude)

**India · Philippines · Indonesia · Vietnam · Thailand · Malaysia · South Africa · Brazil ·
Mexico · Turkey · Colombia · Peru · Ecuador · Dominican Republic**

These are the cheap-volume engine. India and the Philippines in particular are large,
English-capable YouTube audiences — the subscribers are still low-intent for a USD product,
but they can actually watch the videos, which means their watch time is real rather than a
zero. Excluding them would spike the cost per subscriber and defeat the 10,000 goal.

**If Dan later wants to tighten further**, the next ones to cut are Vietnam, Indonesia and
Thailand (weakest English comprehension of the group, so the least real watch time).

### Optional hardening — worth doing while in the settings

- **Exclude TV screens** as a device on the cheap campaign. A meaningful share of junk
  subscribe activity arrives via connected-TV inventory.
- **Add a content exclusion** for "embedded YouTube videos" and low-quality placement
  categories if the campaign type offers it.
- **Layer a fitness affinity / in-market audience** on the cheap campaign. Costs a little
  more per subscriber and gets people who might genuinely watch a body-transformation
  channel, rather than pure number-farming.

---

## Risks and cautions

- **Live ad account with real spend.** Every step is reversible (locations and exclusions can
  be removed, a cloned campaign can be paused/deleted), but changes take effect immediately.
  Stage in Google Ads Editor if unsure.
- **Do not pause or modify the original campaign's delivery** beyond the locations and
  exclusions specified. Dan wants it running.
- **The "Presence vs. Presence or interest" setting is the highest-consequence item here.**
  Getting it wrong silently undoes the entire point of the tier-1 clone, and it fails quietly
  — the campaign will look like it's working.
- **Location bid adjustments do nothing on Target CPA.** Don't set them; don't report them as
  a lever that was pulled.
- **No product-surface, server or client change** — this is ad-account configuration only.
  **No native retest trigger. No deploy. No commit needed** beyond this document.

---

## Exact next action

Open the Google Ads account, complete **Step 0** (identify the conversion action), record the
finding, then work Steps 1 → 4 in order.

---

## Model/effort justification

**Opus 5, Medium.** The strategy work is finished and captured above; what remains is precise
execution in a live ad account where a quietly-wrong setting (Presence vs. interest, shared
vs. separate budget) does real damage. That needs care and good instruction-following, not
deep reasoning. Escalate to High only if Step 0 finds the conversion tracking is broken, in
which case the campaign structure itself needs rethinking.
