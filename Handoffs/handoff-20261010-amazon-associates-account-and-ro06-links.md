# Amazon Associates: account setup and the eight RO-06 product links

**Written 2026-10-10 by Claude.** This is business setup, not a video edit, so the video category line does not apply. It unblocks the RO-06
"How To Work Out At Home On A Budget" release (CONTENT long-form, LFC), which is fully prepared and waiting only for these links.
**Model:** Claude Sonnet 5.5, effort medium, using Claude in Chrome (Dan's real, logged-in Chrome). Opus only if Dan wants copy changes.
**Session name:** `Amazon Associates Setup`.

## 1. Goal

1. Dan has an approved Amazon Associates account tied to his YouTube channel (@danrosefit), with a tracking ID.
2. Eight Associates short links exist, one per recommended item, pasted into the RO-06 description.
3. The RO-06 release is then queued (section 5). Dan promised on camera (1:16) one Associates link per item in the description.

## 2. What only Dan can do (a hard platform limit, not Dan's rule)

Claude cannot create accounts, type passwords, enter tax or payment details, or accept legal terms. Dan does these. A session should
walk him through them one screen at a time, in plain words, and do everything else itself:

- Sign up at `affiliate-program.amazon.com` with his Amazon login (or create the account). Accept the Associates Operating Agreement.
- Enter payment and tax details (where Amazon pays him, and the tax interview). Nothing is spent.
- Verify his phone or identity if Amazon asks.

**Dan fills in, Claude guides:** the website or channel to register. Use the YouTube channel `youtube.com/@danrosefit` (the videos are where
the links live) and add `absbyai.com` and `sixpackabs.com` if the form allows. Describe the purpose as home-workout equipment recommendations.
Pick the store ID (tracking ID) with Dan, for example one ending in `-20`. Record it, it is not a secret, in `Docs/AMAZON_ASSOCIATES.md`.

⚠ Check the current rules on Amazon's own pages before advising, because they change (memory `app-store-policy-verify-first` applies in
spirit): provisional approval period and the number of qualifying sales needed within the first 180 days to keep the account, and whether
the application needs the channel to already have content with links. A new account can be provisional; that is fine for posting links.
Do not promise earnings.

## 3. Items to link (recommend the plain, cheap version, as Dan says on camera)

| # | Item | Price Dan says | Spec to find on Amazon |
|---|---|---|---|
| 1 | Yoga mat | $22 | Thin, basic (not thick, not extra-thick). About 4 to 6 mm. Plain, well reviewed. |
| 2 | Push-up handles | $10 | Basic non-rotating pair. Not the $40 rotating ones. |
| 3 | Jump rope | $9 | Cheap, basic. Not a weighted or "speed" rope. |
| 4 | Ab wheel | $17 | Basic single wheel. Wide wheel with foam handles is fine. |
| 5 | Kettlebell | $45 | 35 lb, basic black cast iron. Not rubber or vinyl coated. |
| 6 | Medicine ball | about $20 | 6 lb. Bouncy rubber type, not a slam ball. |
| 7 | Dumbbells | $29 a pair | 25 lb pair, plain hex or round. |
| 8 | Hand towels | none | A multi-pack of strong cotton hand towels. |

The on-screen price cards (and the film) show specific products and prices. Before choosing, look at the picture in the film's price cards
(`claude edited long form content/13 - How To Work Out At Home On A Budget/...round 6...mp4`, cards at 1:31, 2:36, 3:43, 4:12, 5:34, 8:08, 9:47)
and match them. Where the film shows an AI still, pick the real Amazon product that matches the spec and price. Prefer items with high
review counts and a price within a few dollars of what Dan says. Never link a product costing far more than the number he said on camera;
if nothing matches, pick the closest and tell Dan the real price.

## 4. How to get the links (Claude, once Dan is signed in)

1. In Dan's Chrome, signed into Amazon with the Associates SiteStripe bar showing, open each product page.
2. Use SiteStripe, Get Link, Short Link (`amzn.to/...`). Make sure the tracking ID is Dan's. Copy it.
3. Record a table in `Docs/AMAZON_ASSOCIATES.md`: item, product title, price at the time, `amzn.to` link, ASIN. Commit it (these are public affiliate links, not secrets).
4. Open each short link once and confirm it lands on the intended product and shows Dan's tracking ID in the final URL.

## 5. Then finish the RO-06 setup (everything else is already done)

State on 2026-10-10 (all verified): thumbnail `social media graphics/youtube/thumbnails/How To Work Out At Home On A Budget/How To Work Out At Home On A Budget - thumbnail FINAL.jpg`;
Blotato uploads done and size-matched (URLs are in `scripts/blotato/configs/ro06-home-workout-budget.build.py`); backups on Extreme done and on Google Drive
(folder `114HECkpGyv9TDxfA58ylIzUq3aW7EBQq`; confirm the mp4 finished uploading with `rclone lsl`); slot is **Sunday Dec 20, 9 AM CT** for YouTube, Monday Dec 21 for the rest.

1. Replace the eight `[LINK_...]` placeholders in `claude edited long form content/13 - How To Work Out At Home On A Budget/youtube-description.md` (the copy on Extreme and Drive too). Keep the line "As an Amazon Associate I earn from qualifying purchases."
2. `python3 scripts/blotato/configs/ro06-home-workout-budget.build.py` (it refuses while any placeholder remains), then
   `python3 scripts/blotato/ad_guard.py --scan`, `python3 scripts/blotato/longform_queue.py scripts/blotato/configs/ro06-home-workout-budget.json` (dry run), then `--apply`.
   The queue was 194 of 200; four posts fit. Verify five schedules on a fresh pull (YouTube, Facebook, Instagram @danrosefit, TikTok with `videoCoverTimestamp: 0`).
3. Receipt `Docs/RO06_SETUP_RECEIPT_<date>.md`, a board entry, Edit Queue `queue.py set RO-06 uploaded` + `ArtifactData` mirror + `mark-synced`, and add the SL- shorts job for this film (rule in the `/video-setup` skill, "Edit queue").
4. Owed after the video is public (Sun Dec 20): English captions from the `.srt` (Studio, Subtitles, Upload file), expand `sixpackabs/articles/TBD-home-workout-budget.md` to 800+ words with 1 to 3 internal links, publish and `verify.py`, check the TikTok, Facebook and Instagram posts release Monday.
5. AI flag is true on YouTube and TikTok (realistic AI clips in the film). Never upload to YouTube directly; Blotato releases it.

## 6. Reuse

Every later equipment video (kettlebell, ab wheel, home ab workouts, supplements) can reuse the same Associates account and `Docs/AMAZON_ASSOCIATES.md`.
Add a memory entry `amazon-associates-account` with the tracking ID, where the link table lives and the disclosure line.

## Starter prompt (Claude Sonnet 5.5, effort medium, Claude in Chrome)

Read `Handoffs/handoff-20261010-amazon-associates-account-and-ro06-links.md`. Name this session "Amazon Associates Setup". Walk me through signing up
for Amazon Associates one screen at a time (I will enter my login, payment and tax details myself), register my YouTube channel, then pick the eight
RO-06 products from my signed-in Chrome, get the amzn.to SiteStripe short links, record them in `Docs/AMAZON_ASSOCIATES.md`, and finish the
How To Work Out At Home On A Budget setup: fill the description, queue it in Blotato for Sunday Dec 20, and write the receipt.
