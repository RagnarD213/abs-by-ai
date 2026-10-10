# Dan voice corpus: inventory

**Rebuilt 2026-10-08 (Dan Voice P2A).** The corpus is now sorted into Dan's four types of writing, and a pile holds
only material that is really him talking or writing to an audience. The Part 1 tables (2026-10-06) are kept below for
their Drive ids and authorship notes.

## The rules (Dan, 2026-10-08)

- **Four types, each trained on its own material:** content (YouTube and every other platform), ads, website
  conversion videos and letters (the VSL, the /start letter), products (what the customer gets).
- **Never a source:** his dictation or prompts to Claude or any AI, and business email.
- **Text Claude drafted is never his voice, whatever he changed in it.** Only the lines he changed are kept, as
  before/after pairs.
- Tier 1 is the baseline for a type. Tier 2 supports (structure, persuasion). Tier 3 is dated and lowest weight.
  2026 material weighs most; an older pattern counts only if it also shows up in 2026.

## Where it lives

- Local: `voice-corpus/` in the project folder (git-ignored). One `.txt` per source, by type and tier, with a manifest
  row each in `voice-corpus/_manifest/*.jsonl` (type, tier, year, spoken or written, audience, source, authorship).
- Drive mirror: folder **`Dan voice corpus (raw) 2026-10`** (`1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`), subfolder
  `voice-corpus-2026-10-08/`. A cloud session pulls it from there.
- Every file, with its tags and source id or link: **`Docs/VOICE_CORPUS_SOURCES.md`** (generated).
- Loader: `python3 scripts/voice/corpus.py` prints words per type and tier.

## What is in it (2026-10-08; words after the hold-out set is cut out)

| type | Tier 1 (the baseline) | words | Tier 2 | words | Tier 3 | words |
|---|---|---:|---|---:|---|---:|
| **Content** | 21 Abs By AI videos filmed from outlines, no script (72,600; four are raw rolls with retakes); 8 shorts he wrote himself (900 after hold-out); 32 solo videos from the old channel `@danielrose-socialresponse7768`, 2020 to 2021 (120,500); his side of Travel Like a Boss episode 252, 2020 (8,900) | 203,000 | his half of 10 Dan & Dani podcast episodes (36,800); his typed outlines for four shoots and his podcast outlines (7,600) | 44,300 | four Six Pack Shortcuts era videos with him on camera, 2011 to 2017 | 12,800 |
| **Ads** | Abs By AI Ads 1 and 3 as he wrote them; nine Abs By AI shorts ads ("Approach #2"); his typed lines in batch-1 Ads 2 to 15; six 2020 ads for his book | 9,800 | 107 ads for other presenters: Spy Briefing 58, HBI 19, CPA offers 16, Physio Tru 14 (2019 to 2025) | 66,800 | | |
| **Conversion** | 2019 consulting sales video, 2019 DR marketing site VSL and copy, 2020 book sales page, upsells and launch videos (five also as spoken), 2021 Black Belt sales video outline, cart page, sales page and upsells, his sections of the 2026 /start letter, his 2026 VSL outline | 31,300 | 2025 Fujiyama VSL and one host-read launch video | 2,300 | | |
| **Products** | The Sex God Method, 2007, 50 chapter files (54,400; 29,900 of it explicit technique, tagged and never quoted); 20 Black Belt course videos, 2021 (127,400) | 181,800 | 15 Steps to Profitable YouTube Advertising, 2020 | 122,800 | | |

Not Dan, kept as the comparison floor: Claude's content scripts as delivered (14,900 words), the same scripts as he
read them on camera (9,700), Claude's and Fable's ad scripts (10,900), Claude's VSL and letter drafts (4,500), and six
videos from two other fitness creators, Sean Nalewanyj and Thomas DeLauer (16,800).

Pairs (local, `voice-corpus/pairs/`): 176 script-versus-spoken pairs from 14 teleprompter videos (what he changed
while reading), and 33 new doc-edit pairs (RO-14, Alcohol, Zepbound, Make Time shorts) on top of the Part 1 pairs in
`.claude/skills/_shared/voice/dan-edits-2026-10-06.md`.

**Thin spots:** ads Tier 1 (under 10,000 words); shorts (nine scripts that are wholly his); consumer-facing conversion
copy (only his sections of the /start letter); nothing of his in 2026 for products.

## How each video was classified

A video is "filmed from an outline" only if its shoot doc is bullets and under 6 percent of the transcript's six-word
runs appear in that doc. Teleprompter videos (Belly Fat Emergency, RO-10, RO-12, RO-13, RO-16, the DS shorts) match
their scripts at 63 to 77 percent: they are Claude's words and sit in the floor pile, not in content.

## Left out, and why

- The V2 long-form, its short "Supplements Are Only 3%" and "The Upload" (Dan's earlier call).
- Keith's and Wes's HBI scripts, Jordan's Spy Briefing scripts, "JESSE'S EDITED VERSION", the AI-looking compliance
  rewrites of the 2024 CPA ads, "HBI scripts adapted from emails 2024" (authorship unclear), "What Five Leading
  Specialists" (unclear, leans not his).
- "Dedicated Shorts Ads Scripts" and five of the "Approach #2" ads (Claude's), the 15 Claude-drafted Shoot 5 shorts,
  the 10/17 shoot's 14 shorts scripts (Claude's), DS-04 (Claude's draft, about half rewritten by Dan: pairs only).
- Shoot 3 and Shoot 4 outline docs (his inserts cannot be told from Claude's lines in an export).
- The second podcast guest spot ("SMART Businesses Do This", 2022-04-05, 14 minutes): it is him, but the host's audio
  file refuses downloads.
- "YouTube Ad Scripts Portfolio For Daniel Rose" (`1QAEr2M07HapKXT5vnj6n4ZxspN9Q42KXNmIvqMLBjBU`): a freelance
  copywriter's portfolio (Lutfi Isnin) shared with Dan in 2021. Not his writing.
- `sgm.pdf` (`1NlsoD4c-ieqB-alkjHI38d6HnQj21rni`): a 13-page excerpt of one chapter of the same book, not a sales page.
- The two loose Black Belt files ("EXPLORATION DRILLING STRATEGY", "VIDEO 6 - LTV"): raw takes of lessons whose
  finished versions are in the folder. Nothing on Drive was deleted.

## Dan's answers on authorship (2026-10-10), applied

- **Battle Ropes short:** he believes Claude wrote it. Out of the corpus and out of the hold-out set. Eight shorts are
  now counted as his.
- **"AI Took My Job" shorts ad:** his outline, Claude's script. Moved to the Claude floor pile. The other nine
  "Approach #2" shorts ads stay his (the 2026-08-23 board archive records that he wrote them as his own examples).
- **15 Steps launch-video scripts that include the host's lines** (videos 6, 9, 12, 13): his writing, but written for
  someone else to deliver, so "not a good example". Tier 2 now. His own answers in those videos, as spoken, stay Tier 1.
- **Black Belt folder videos:** confirmed, these are all the product videos he made.
- **Lutfi Isnin's portfolio doc:** he does not know the name and does not think he wrote for the agency. Stays out.
- **"What Five Leading Specialists":** he is not sure. Stays out.
- **Make Time shorts hooks:** he does not recall them. They stay as pairs only.
- **Six Pack Shortcuts videos:** he will send links.

## The hold-out set and the bench

40 real passages are locked away for blind testing (`.claude/skills/_shared/voice/HELD-OUT.md`; guard:
`python3 scripts/voice/heldout_guard.py`). The HBI "Five Foods To Avoid" script stays held out from end to end. RO-14
was released: it is a Claude draft he edited. The bench (`scripts/voice/bench.py`) replaces the two-piece blind test
planned in Part 1; results are in `Docs/voice-bench/`.

---

# Part 1 tables (2026-10-06)

Built in Dan Voice Training P1 (`Handoffs/handoff-20261006-dan-voice-training-part1.md`). What was read, whose words they
are, and where the raw copy lives. Analysis and short excerpts are in `.claude/skills/_shared/DAN-VOICE.md` and
`.claude/skills/_shared/voice/`. Raw text stays on Drive, never in this public repo: folder **`Dan voice corpus (raw)
2026-10`** (`1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`). "denied" = the cloud session's permission check refused the copy
(client docs flagged as sensitive); the original id still works for a re-read.

Tiers: A = Dan wrote it. B = Dan's edits to a Claude draft. K = Keith or Wes (technique only). C = Claude text he kept.

## HBI top 10 (sheet `1RtcUMgsJAdOHu5VKKaMOhhVXNvGi8DvfZ8XU3CCrKtw`)

| source id | title | date | writer | tier | spend / CPA | raw copy |
|---|---|---|---|---|---|---|
| 1MTi-ReCiFmSSiNPfDy0KyehULpXrC8mRINWZGKXIuS8 | Dr. Brian Paris Protein = Pain Adaptation (row 1) | 2020-07 | SRM (Dan) | A | $5,963,939 / $66.66 | denied |
| 1nCn7t0bF3aC0GrJZiG04UD26TRl86EhWCCR4EY_XAUQ | Jesse's Scripts For 9/10 Shoot (row 3 = "Five Foods To Avoid") | 2020-09 | SRM (Dan); "JESSE'S EDITED VERSION" section is Jesse Cannone, excluded | A | $1,691,482 / $69.79 | denied. **Held out of the guide for the blind test** |
| 1Q32YqOspDsiDXsx9wc3knuSzo07pPxPFiEEzAC4yrpQ | ad scripts, hbi, april 2020, MARK (rows 8 and 11) | 2020-04 | SRM (Dan); "What Five Leading Specialists" section unclear | A | $904,578 / $48.70; $854,862 / $48.14 (row 11 mapped to the "Seniors having fun" section by inference) | 1OSHszQGx3XPn9tCVamHYolDGyiUe9GCufAgmS0CqSBg |
| 15TvJnQGCOcmp8HUqJojhLqhOX09iHwrqy7DmJILKQSA | Keith "3 Changes", Dr. Paris (rows 6, 9; row 2 very likely the same) | 2021-03 | Keith | K | $1,033,345 / $70.61; $883,674 / $68.26; row 2 $2,784,155 / $78.47 | 1h8KDE1QG0QfqlLUeJIofg7sCtuxOXfFN5yCvniqwV-s |
| 1dZA0-mG7myrGuAqCMuOfu1ge70CYomxBfFDtBqLdZ7k | Keith "Bionic Boomers" (row 5) | 2022-08 | Keith | K | $1,039,871 / $85.36 | 1oOnSYwTgxhYRONs8Zygv_44RljQgVreZs4wKQXPmhG4 |
| 1V7Xo51ZarLXPvoGrJpwjFZpCcf7xzWyHqT-wVCZKZnU | Dan's "Batch 2 Greatest Hits" doc: transcripts of In The Fridge (row 4), Elmer Egg Photo (row 7), 2 Bad Proteins (row 10) | 2022-04 | Keith, Keith, Wes (Wes's back half is Dan's SRM close) | K | $1,331,699 / $57.99; $950,076 / $57.67; $879,959 / $73.78 | 1Vw4G3xtTFUEwW-lGD2qsBat5xeyg7mmNFT0J1z9D5yk |

The four Dropbox links in the sheet are disabled (Dropbox error page), so the transcripts above were used instead.

## Dan's other ad scripts (10 of about 115 found, 2019 to 2025)

| source id | title | writer | tier | raw copy |
|---|---|---|---|---|
| 1T7QYBDFfGNPaMXQfXr68CAJpegm2lsWPRWJCyjmhrw4 | ad scripts, hbi, september 2019 | SRM (Dan) | A | 1WYMDvQ-nezGLhhR81gb74gxVIcPOMJhFahhufsF419E |
| 11V9Z7wET-nS_fipMnWBY2tJ3nj9-bukmMCmBS_LJ9hA | consulting sales video script (2019) | Dan, own name | A | 1Cz54Y2iOLYwvSgMKj2NUqce3oNU7KUGKD3OQJXsL5vk |
| 1kDbP09aenW35kLzD0wSKJJXAURaA2FJzm_orJ31NsbE | YouTube Ad Management Black Belt sales video outline (2021) | Dan, own name | A | denied |
| 119mng1tchgMcJxY3hOkBwJVy6lC_sm0nxeYyStLV_X8 | ad scripts, hbi, december 2021, FINALIZED | SRM (Dan) | A | 1OrlwtZL0-bYdNgU73mVE0GdKdT9YA_t4lSC992plBBY |
| 1AZUSGQdzksSBRS7-wQI7CQvmpzJ5Bn_lqlEDWz6AEkc | spy briefing, february 2022, Mike's scripts | SRM (Dan); 2 ads by another writer excluded | A | 13XleWq2uKKVgUyqiu8oxHm-i1YkJ1iV0D0B1CqfodNU |
| 1kLmYEmElqKadygdW4PVip1l2FUQ-agxaYFwitzgonnY | Spy Briefing Jan/Feb 2023, scripts for Jason, FINALIZED | SRM (Dan) | A | 1VnwHxxFz5VnUJm7BO-7vfFTqtFR25TV2PG_TgJPdJNo |
| 1C4rxeMIxElsRcByLHkV8tqgpOB6viAfcO2K_fbImF2I | cpa offers, september 2023, FINALIZED | SRM (Dan); offer-VSL stories excluded | A | 10DGQcfLBxFRfsWXEaGRG32kENZZiI7MHfkstcaO61uM |
| 1SQYUM6-_KQeYBU35gROPEolb83lhzXwKRQxfB5aIZyI | physio tru, february 2024 | SRM (Dan) | A | 1scfu1Ga6ob7YySR_vDsWb991OSYoXfwJGXoo5tJumpk |
| 1OAYtZnrpuvOyQXX682OI47eo5-9SsZwytwi27ZSFU2I | vsl script, darren fujiyama (2025, "DAN'S EDITS FINALIZED") | SRM (Dan) | A | 12YjgnznO1phoDaiw2-w7lRVDskiulIFdmDMqBJWKVic |
| 1OuVbgga0YjGZNLLbW2HIkwQ9ihELFkO4giy1_97MSZ4 | spy briefing, september 2025, scripts for Jason, FINALIZED | SRM (Dan); herb-study bullets look swiped | A | 1osNQ67SLklHAqIRzzQt8uvdahYIEBuW74NRsv3TkudM |

## Book

| source id | title | tier | raw copy |
|---|---|---|---|
| 12wKH4OUzxbcNGv40YbnBx2DBUFXuRgcW1W19OsPewdk | 15 Steps to Profitable YouTube Advertising, FINAL MANUSCRIPT (2019 to 2020, about 121,000 words) | A | 1arZ7wE67R9I8Ob3g3zt2L_OncOSMAw3GpcD8PecOhQQ |

No other book was found. Every "manuscript" hit is a version of the same book (drafts, part 1/2 splits, v2 .docx and
.pdf, print exports). Related, unread: book funnel copy `100vap0GosZz9ATkILuGip2Z1sds51xy8nEvvlZuLKJM`, book pre-order
video outline `1AL89B3zrbQHJTtqZnTwvk4OFEfaWGPray9ctalhZ9F0`, podcast outlines `1mFZIF6iFm6KcURLVWSoWfq79mQ26aCyNnSHAz88-pd8`.

## Abs By AI ads, VSL and sales letter (2026)

| source id | title | writer | tier | raw copy |
|---|---|---|---|---|
| 160O1s3xcUGlVU_BjtZR5u_V2WgE9JSREUftUTPuZQEw | Abs By AI ad outlines, batch 1 | Ads 1 and 3 Dan; Ad 2 Claude from his outline; 4 to 12 Claude; 13 to 15 Fable (labels in headings) | A for Ads 1, 3; C otherwise | denied |
| 1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg / 1bpEndCcM-imeOWS0tp86l7Ud0bGyxLQ-MWZVAwcacgA | batch 1 finalized scripts / teleprompter | Claude drafts, Dan line-edited all 15 (about 08-10) | B; heavy for Ads 5, 6, 7, 8, 10, 13, 14; Ads 1, 2 effectively C | 1dLtnUhIf73vuNnCf7FE70Y9ZEUsRJN98mHBoW49aH5M / 1r0QOvnnb8u3Jf_a81ppPbKJnGIBb9qCzEwZM5YEWmXk |
| 1AVRvxiINZ0EDkoFv77piXbg5xGuizHGuHE7vRVWXRKk / 1n1FIVgNaBZZ6j0aJsEyqLAE8oT82SQQNJ_pGrCLVVwg | Ads 2 to 15 editor copies | duplicates of batch 1 | not counted | denied / 1SlFU20pN4IflmkZn7an4ZX2Z7zk66R7ekYM34Tl5ERA |
| 1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o | Sales letter "AI Got Me Abs at 40", final copy | Claude v1, Dan rewrote headline, offer card, S4 to the Five Ways intro | A (his sections), B (hacks), C (S10 to S13) | 1hckoXb0NFzTYYSb4y-eD9RSWr3elW6kMeWyAoMFg-yM |
| 1lHzTMJydS7CBH3yigTYDDv1g3z9AJMcqwaPNyyKcIVc | VSL Version A "AI Got Me Abs at Forty" | Claude, with a few Dan inserts | C | 1WPRKtn7lticFGBzgYetKyX1503aPpT63tG-6LgSqhIA |
| 1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA | /start VSL scripts | Claude only, never approved | C (not a voice model) | 125nyaJxjqy2DnhdSYH2BqtL8CiZ1xwJqsjPHkbog7HQ |

How to tell Dan's lines from Claude's in a Google Doc: text Dan types gets curly apostrophes; Claude's pasted text keeps
straight ones. Works for batch 1 Ads 1 to 10, the VSL A doc, the letter and the content docs.

## Abs By AI content (2026)

| source id | title | writer | tier | raw copy |
|---|---|---|---|---|
| 1OmsgBzpsfW05tjkQvqQUb2-QcUp2XajNMAgs0FRjh8U | First Batch Video Outlines (incl. Top 10 Tips `2T4LrQrmz9s`, 13k views) | Dan | A | 1KJi2IJopnJHVKFy0FZpXPSmO2oCK515XxV_-_NTRC3o |
| 15gg6GP_Huy93ZBfTpbQuUtHGDrgHL-bs6Op-nN2UBr8 | Second Shoot Outlines (Every Day, Fasting, STOP Deadlifting) | Dan | A | 10NZD_YOqCwlagFwHp2czjoiS72lkWyFAjP71O4rCzu8 |
| 100prkvoE0lcxTLn1d7w_X1zeUbT0I3Xy6H3dDT6ZDCg | Third Batch Outlines (Home Workout Budget, Invest In Health) | Dan | A | 1yEZJAH_5i9Now7WZWkEne4wfrmoqWRc5l_UgKUpHCOY |
| 1VeNXATtvHBVe_Y5S3fxmSjllZxva0zwgo5NghW-G_bU / 1uDAWvxoAjXUaawZctgdSDj_9JPa5mfk5MMM2Sh8L7yE | Shoot 3 and Shoot 4 outlines (incl. Ab Wheel `bkzT-3ENpoU`) | Claude outlines with Dan's typed inserts | A for inserts only | 18S__iflhWdlHJvX9Yk_ds8bawWCQS1GziCt6lSFm3NA / 1_xInDF99QQ36_9fRYFFHX-e6hzXRqFnEpiKZRzsg_7U |
| 1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k | Shoot 5 scripts (Belly Fat Emergency `v2R4QpnURqA`, Real Reason, shorts incl. Jump Rope `LTkjlBr_3tg`, 5k views) | Claude + Dan; 7 shorts all Dan | B; A for those 7 shorts | 1Lt6Kt9ylgZXOwlYxnwVorn--pihMHZScKTHoWjl2bwg |
| 1ND_BTQKfIIBdfBC_WJGhxc_SZHtQFh32HI3ksD_dIVo | Shoot 5 Outlines Not Yet Filmed, with Claude's 09-19 scripts | Claude (the "before" for Zepbound, Alcohol, Not Losing Weight) | C | 1DvxSFoBWX9mBIas-aoeS7jV-yyk5chqQVJHhJFs4_BY |
| 1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4 | 9/23 Shoot Scripts (filmed finals) | Dan-edited | B. **"Why You're Not Losing Weight" (RO-14) held out of the guide for the blind test** | 1nyTc7vJNveDUw3HBCE6xU6ZKkfcM3HkJudEllVl7Xmc |
| 1DN1QMARJrqEJL4xl7Y2X3-CSjeag7SCSm6bBtmeefjc / 1hkRlNqkG5Ic4d2cUS50Y6ErDj5DmJdvxqgjIFAJ98H4 | Make Time shorts: Claude 09-22 backup / "USE THIS SCRIPT" | Claude / Dan's hook rewrites | C / B | 1xKy66m5qVv64YBtyURFlJvFF8kKd5rw9VMtN2xVrff8 / not copied (duplicate) |
| 1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0 | 10/17 shoot outline ("I'm 41. I wasted my life.") | Dan, live | A | 1-8NS6l4pV2GOh0FMNcNcTLvFpjFvi6k2PlqKN2t3OrY |
| 16nrufNrDMyyp82rDeojtK4FHyGxbz13O | Oura Ring review SRT (off the cuff) | Dan, spoken | A | 1Cmsf2XRoEvq3EOCoqjJ2Mm0ZcelXsCxQ |

Excluded: the V2 long-form and "The Upload" (Dan's call), the 2022 Gundry scripts, "SixPackAbs.com 15 YouTube Video
Outlines" (an AI research memo), editor-facing duplicates, docs titled OLD / DO NOT USE.

## Top videos with no script and no transcript (need a local transcript)

Long-form: Top 10 Tips `2T4LrQrmz9s` (Dan's outline only), Ab Wheel `bkzT-3ENpoU` (Claude outline only). Shorts: 2
Minute Arm Pump `qDvrtKbuhf4`, Toe Touch `I_IpdKpT2-0`, You Have 4 Ab Muscles `A8_uiK0D8nc`, Supplements Are Only 3%
`P9VUGyWeNtY`, Never Start Your Day With Carbs `_Ep_hVPZYzE`, Why I Skip Breakfast `UFga137pseM`, Why Bodybuilders Suck
Their Stomach In `QuswpGj635A`, Your Protein Shake `B6Oku5GjrLs`, Milk Is Not A Health Food `YvfQfo9Qh4s`, Stop Doing
Ab Exercises `GVNzvm5sUbk`. Cloud sessions cannot pull YouTube captions. Two unconverted SRTs on Drive are also Dan off
the cuff: Stop Deadlifting `1NeSaKftqqXs3VlZwoY6iz0stOghaOrBm`, Keep Your Muscle `176MKh1QPa83ziaDAoEFqF0xZiNfjcXu3`.

## Blind test (step 10): superseded 2026-10-08 by the bench above. The Part 1 plan, for the record

Skipped on 2026-10-06 to save Dan's cloud credit. To run it later (about a dollar or two): give a fresh writer ONLY
`DAN-VOICE.md`, `voice/`, `WRITING-RULES.md` and `dan-personal-facts-for-scripts`, plus (1) a brief for the HBI "Five
Foods To Avoid If You Have Arthritis" ad (Jesse reads it; reveal tomatoes and solanine; hold back four; free
presentation normally $49.95; "Watch Now") and (2) Dan's outline "5. Why You're Not Losing Weight" from
`1ND_BTQKfIIBdfBC_WJGhxc_SZHtQFh32HI3ksD_dIVo`. Compare with the real ones (`1nCn7t0bF…` Five Foods section;
`1tTPTksuG…` RO-14 final) using `scripts/voice/voice_stats.py`, fix the guide once, then put the real and generated
RO-14 side by side in a Drive doc as A and B for Dan.
