# Dan vs. Claude by the numbers (per type, 2026-10-08)

Rebuilt in Dan Voice P2A; re-measured 2026-10-10 after Dan's authorship answers (one short and one shorts ad turned out
to be Claude's, and the launch-video scripts written for a host moved to Tier 2). No gap moved. Dan set four types of writing on 2026-10-08 (content, ads, website conversion videos,
products), and **a baseline for a type comes only from that type's Tier 1**: material that is really him talking or
writing to an audience. Text Claude drafted is never in a Dan pile, whatever he changed in it. The 40 hold-out passages
(`HELD-OUT.md`) are cut out of every pile before measuring.

Rebuild: `python3 scripts/voice/corpus_stats.py` (local only; it reads `voice-corpus/`, which is on the Mac and in
Drive folder `1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`, never in this repo). One draft: `python3 scripts/voice/voice_stats.py
draft.txt`, `... --small draft.txt`, and `python3 scripts/voice/voice_fingerprint.py --type content draft.txt`.
The 2026-10-06 version of this file (Part 1, built mostly from ads he wrote for other presenters) is in git history.

## The piles

| type | Tier 1 (the baseline) | words | Tier 2 and 3 | the floor |
|---|---|---:|---|---|
| Content | 21 Abs By AI videos filmed from outlines with no script (2026), 8 shorts he wrote himself, 32 solo videos from his old business channel (2020 to 2021), his side of Travel Like a Boss episode 252 | 203,000 | his half of the Dan & Dani podcast, his typed outlines (44,000); four Six Pack Shortcuts videos (13,000) | Claude's content scripts as delivered (14,900); the same scripts as Dan read them on camera (9,700); two other fitness creators (16,800) |
| Ads | ads he wrote for himself: Abs By AI Ads 1 and 3, nine Abs By AI shorts ads, his typed lines in the batch-1 ads, six 2020 book ads | 9,600 | 107 ads he wrote for other presenters, HBI, Spy Briefing, CPA offers, Physio Tru, 2019 to 2025 (66,800): structure and persuasion, not voice numbers | Claude's and Fable's ad scripts (10,900) |
| Conversion | his own sales videos and letters: the 2019 consulting video and DR site VSL, the 2020 book funnel and launch videos, the 2021 Black Belt sales pages, his sections of the 2026 /start letter | 27,900 | the 2025 Fujiyama VSL and the 2020 launch-video scripts he wrote partly for a host to deliver (5,700) | VSL Version A, the /start VSL scripts, Claude's letter sections (4,500) |
| Products | The Sex God Method (2007, 54,400) and 20 Black Belt course videos (2021, 127,400) | 181,800 | 15 Steps (122,800) | none: Claude has never written a product for him |

Thin spots: **ads Tier 1** (under 10,000 words, four samples), **shorts** (eight scripts), and **consumer conversion
copy** (only his sections of the /start letter; the rest sells to business owners).

## Counts

Per 100 words unless the name says otherwise. Definitions are in the header of `scripts/voice/voice_stats.py`.

| pile | words | and | lists3 | questions | you | contractions | swears | emdash | sent_mean | sent_sd | para_words | punch_pct | oneline_pct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CONTENT Tier 1 (all) | 202878 | 2.44 | 0.26 | 0.1 | 6.24 | 4.03 | 0.02 | 0.0 | 18.3 | 17.6 | 89.9 | 11.7 | 0.2 |
| Abs By AI off the cuff, 2026 | 72551 | 2.43 | 0.33 | 0.08 | 6.89 | 4.45 | 0.03 | 0.0 | 16.5 | 11.8 | 81.8 | 13.4 | 0.0 |
| shorts he wrote, 2026 | 899 | 2.45 | 0.22 | 0.11 | 7.23 | 3.34 | 0.0 | 0.0 | 14.7 | 6.1 | 34.6 | 0.0 | 3.8 |
| old channel solo, 2020-21 | 120529 | 2.44 | 0.23 | 0.11 | 6.15 | 3.81 | 0.02 | 0.0 | 19.8 | 21.2 | 98.8 | 11.1 | 0.2 |
| Travel Like a Boss, 2020 | 8899 | 2.64 | 0.21 | 0.13 | 2.05 | 3.65 | 0.02 | 0.0 | 16.7 | 10.1 | 72.3 | 7.8 | 0.0 |
| content Tier 2 (podcast half, outlines) | 44333 | 2.22 | 0.28 | 0.34 | 4.79 | 4.44 | 0.02 | 0.0 | 14.0 | 16.4 | 75.1 | 30.3 | 5.1 |
| content Tier 3 (Six Pack Shortcuts) | 12841 | 3.01 | 0.26 | 0.23 | 4.61 | 4.07 | 0.0 | 0.0 | 22.0 | 53.3 | 102.7 | 3.3 | 0.0 |
| Claude content drafts | 14907 | 3.52 | 0.42 | 0.07 | 6.98 | 2.41 | 0.08 | 0.0 | 12.8 | 7.4 | 34.8 | 14.8 | 5.1 |
| Dan reading Claude scripts | 9666 | 3.32 | 0.57 | 0.09 | 6.95 | 3.2 | 0.05 | 0.0 | 13.6 | 7.9 | 67.1 | 21.8 | 0.7 |
| Other fitness creators | 16794 | 3.16 | 0.34 | 0.31 | 5.14 | 3.36 | 0.01 | 0.0 | 21.4 | 15.5 | 106.3 | 9.6 | 0.0 |
| ADS Tier 1 (own ads) | 9614 | 2.97 | 0.29 | 0.35 | 6.76 | 3.73 | 0.02 | 0.03 | 14.3 | 6.4 | 46 | 6.1 | 12.0 |
| ads Tier 2 (for other presenters) | 66782 | 2.96 | 0.43 | 0.26 | 5.83 | 3.52 | 0.0 | 0.06 | 14.1 | 6.2 | 24.7 | 6.6 | 10.5 |
| Claude ad drafts | 11089 | 3.37 | 0.41 | 0.14 | 7.26 | 4.13 | 0.0 | 0.92 | 10.8 | 6.5 | 34.7 | 12.8 | 6.9 |
| CONVERSION Tier 1 | 27882 | 2.92 | 0.3 | 0.11 | 6.59 | 4.01 | 0.0 | 0.0 | 17.6 | 9.3 | 64.5 | 4.1 | 7.6 |
| conversion Tier 2 (Fujiyama) | 5733 | 3.19 | 0.4 | 0.26 | 6.72 | 4.99 | 0.0 | 0.0 | 16.3 | 6.7 | 35.6 | 1.7 | 6.8 |
| Claude conversion drafts | 4470 | 3.78 | 0.34 | 0.45 | 6.02 | 3.42 | 0.0 | 1.72 | 8.9 | 6.0 | 20.9 | 29.7 | 13.1 |
| PRODUCTS Tier 1 (all) | 181765 | 2.2 | 0.28 | 0.06 | 5.53 | 3.15 | 0.17 | 0.1 | 19.4 | 17.8 | 85.6 | 7.2 | 5.1 |
| The Sex God Method, 2007 | 54379 | 2.22 | 0.3 | 0.1 | 5.03 | 1.53 | 0.55 | 0.33 | 15.9 | 7.5 | 59.0 | 7.2 | 11.7 |
| Black Belt course videos, 2021 | 127386 | 2.19 | 0.27 | 0.04 | 5.75 | 3.84 | 0.0 | 0.0 | 21.3 | 21.3 | 106.0 | 7.2 | 0.0 |
| products Tier 2 (15 Steps) | 122795 | 2.17 | 0.26 | 0.12 | 6.12 | 2.96 | 0.01 | 0.46 | 17.5 | 8.4 | 32.8 | 3.2 | 14.2 |

Caveats: a spoken transcript's paragraphs are set by the transcriber, so `para_words`, `punch_pct` and `oneline_pct`
mean nothing on the spoken rows; read them only on written rows (ads, conversion, The Sex God Method, 15 Steps,
Claude's drafts). Spoken sentences run long partly because speech has no full stops. The Sex God Method is from 2007
(few contractions, some em dashes): learn how he explains and motivates, not its punctuation.

## Small everyday words (per 1,000 words)

| per 1,000 words | actually | really | very | kind of | stuff | things | going to | gonna | which | because | just | so | pretty | a lot | you know | basically | like | now | right |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CONTENT Tier 1 (all) | 0.98 | 2.74 | 1.85 | 1.43 | 0.3 | 1.52 | 7.1 | 0.87 | 1.45 | 2.49 | 5.9 | 10.74 | 0.45 | 2.67 | 0.51 | 0.55 | 5.19 | 6.1 | 3.89 |
| Abs By AI off the cuff, 2026 | 0.91 | 2.32 | 1.27 | 1.01 | 0.59 | 1.63 | 9.39 | 0.57 | 1.36 | 2.4 | 5.82 | 11.58 | 0.23 | 2.15 | 0.19 | 0.14 | 5.21 | 5.2 | 4.37 |
| shorts he wrote, 2026 | 0.0 | 0.0 | 3.34 | 0.0 | 0.0 | 0.0 | 2.22 | 0.0 | 1.11 | 5.56 | 6.67 | 4.45 | 0.0 | 2.22 | 0.0 | 0.0 | 1.11 | 2.22 | 2.22 |
| old channel solo, 2020-21 | 0.95 | 2.75 | 2.23 | 1.27 | 0.13 | 1.4 | 6.06 | 1.12 | 1.56 | 2.43 | 5.78 | 10.25 | 0.53 | 2.85 | 0.69 | 0.66 | 4.16 | 6.87 | 3.75 |
| Travel Like a Boss, 2020 | 2.02 | 6.29 | 1.35 | 7.19 | 0.11 | 2.47 | 3.03 | 0.0 | 0.67 | 3.71 | 7.98 | 11.12 | 1.12 | 4.61 | 0.67 | 2.47 | 19.44 | 3.48 | 2.02 |
| content Tier 2 (podcast half, outlines) | 1.49 | 5.1 | 1.06 | 3.11 | 0.2 | 2.98 | 4.56 | 0.02 | 1.17 | 2.28 | 6.43 | 13.26 | 0.72 | 4.15 | 0.65 | 1.15 | 7.71 | 2.35 | 3.32 |
| content Tier 3 (Six Pack Shortcuts) | 2.02 | 11.45 | 1.17 | 4.52 | 1.87 | 5.06 | 6.0 | 0.0 | 1.71 | 3.97 | 6.78 | 9.11 | 0.31 | 5.53 | 7.01 | 0.39 | 16.28 | 2.73 | 3.58 |
| Claude content drafts | 0.87 | 0.8 | 0.47 | 0.07 | 0.27 | 0.67 | 4.02 | 0.0 | 0.67 | 3.89 | 3.42 | 7.04 | 0.13 | 2.15 | 0.2 | 0.13 | 2.55 | 4.02 | 2.08 |
| Dan reading Claude scripts | 1.03 | 0.93 | 0.41 | 0.0 | 0.0 | 0.72 | 2.9 | 0.21 | 0.52 | 3.93 | 3.62 | 6.83 | 0.1 | 1.97 | 0.31 | 0.1 | 3.0 | 3.83 | 2.17 |
| Other fitness creators | 1.91 | 3.33 | 2.38 | 0.48 | 0.3 | 2.44 | 5.36 | 0.0 | 2.44 | 3.63 | 8.4 | 8.16 | 0.48 | 1.13 | 1.43 | 0.48 | 4.23 | 2.74 | 1.01 |
| ADS Tier 1 (own ads) | 0.73 | 0.31 | 1.14 | 0.21 | 0.1 | 0.94 | 2.18 | 0.0 | 0.94 | 2.81 | 5.51 | 4.58 | 0.1 | 0.1 | 0.42 | 0.0 | 2.81 | 5.51 | 2.29 |
| ads Tier 2 (for other presenters) | 1.21 | 0.27 | 0.69 | 0.01 | 0.01 | 0.36 | 1.05 | 0.0 | 3.19 | 3.43 | 4.85 | 3.28 | 0.16 | 0.21 | 0.96 | 0.03 | 3.67 | 4.09 | 1.38 |
| Claude ad drafts | 5.14 | 0.09 | 0.09 | 0.0 | 0.27 | 0.18 | 0.9 | 0.0 | 1.08 | 2.89 | 3.43 | 4.87 | 0.0 | 0.36 | 0.09 | 0.0 | 4.06 | 2.53 | 1.98 |
| CONVERSION Tier 1 | 0.93 | 1.94 | 2.26 | 0.32 | 0.07 | 1.15 | 3.91 | 0.04 | 1.26 | 2.4 | 4.99 | 6.1 | 0.18 | 1.0 | 0.72 | 0.36 | 3.95 | 5.56 | 3.01 |
| conversion Tier 2 (Fujiyama) | 0.17 | 0.7 | 0.52 | 0.0 | 0.0 | 0.35 | 2.44 | 0.0 | 0.52 | 2.09 | 3.84 | 4.71 | 0.17 | 0.52 | 0.7 | 0.0 | 4.01 | 5.06 | 2.97 |
| Claude conversion drafts | 2.46 | 0.89 | 0.22 | 0.0 | 0.0 | 1.12 | 1.12 | 0.0 | 0.89 | 0.89 | 2.68 | 5.59 | 0.0 | 0.0 | 0.45 | 0.45 | 3.13 | 4.25 | 2.46 |
| PRODUCTS Tier 1 (all) | 0.78 | 1.53 | 2.3 | 0.83 | 0.18 | 1.38 | 3.39 | 0.62 | 2.2 | 2.22 | 4.6 | 10.1 | 0.35 | 1.48 | 0.37 | 0.58 | 2.63 | 3.8 | 2.75 |
| The Sex God Method, 2007 | 0.72 | 0.94 | 1.66 | 0.17 | 0.06 | 0.86 | 1.07 | 0.0 | 1.49 | 1.86 | 2.35 | 3.35 | 0.04 | 0.35 | 0.31 | 0.04 | 2.89 | 0.68 | 1.29 |
| Black Belt course videos, 2021 | 0.8 | 1.79 | 2.57 | 1.11 | 0.24 | 1.6 | 4.38 | 0.88 | 2.5 | 2.37 | 5.57 | 12.98 | 0.48 | 1.96 | 0.4 | 0.82 | 2.52 | 5.13 | 3.37 |
| products Tier 2 (15 Steps) | 0.53 | 0.55 | 1.73 | 0.07 | 0.12 | 0.58 | 0.77 | 0.0 | 1.81 | 2.37 | 2.87 | 2.59 | 0.06 | 0.59 | 0.47 | 0.09 | 3.05 | 1.32 | 1.29 |

## Style distances: ceiling and floor

From `scripts/voice/voice_fingerprint.py`. **Delta** is the function-word fingerprint (Burrows' Delta over the 150
commonest grammar words): lower is closer to Dan. **LUAR** is a style embedding (`rrivera1849/LUAR-MUD`): higher is
closer. Samples are about 2,500 words each. The ceiling is each of Dan's samples against the average of his others.
The floors are Claude's drafts of that type, and two other fitness creators, against Dan's average. A draft is doing
well when it sits at the ceiling and far from both floors.

| type | Dan Tier 1 words | samples | Delta ceiling (Dan vs Dan) | Delta floor (Claude) | Delta floor (other creators) | LUAR ceiling (Dan vs Dan) | LUAR floor (Claude) | LUAR floor (other creators) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| content | 201577 | 81 | 0.757 | 0.877 | 0.848 | 0.963 | 0.897 | 0.898 |
| ads | 9525 | 4 | 0.813 | 0.928 | 1.126 | 0.962 | 0.939 | 0.858 |
| conversion | 27638 | 11 | 0.777 | 0.987 | 0.953 | 0.973 | 0.887 | 0.845 |
| products | 180861 | 72 | 0.773 | n/a | 0.852 | 0.945 | n/a | 0.883 |

The gap between ceiling and floor is real but not wide, so these two numbers are for pooled text (a whole bench run,
2,500 words or more), never for one script. Ads Tier 1 has only four samples: treat its row as rough.

## The gaps, per type

**Content (Abs By AI off the cuff, 2026, against Claude's content scripts).** This is where Claude is furthest off.

1. **Claude's scripts are too clean: his small words are missing.** Per 1,000 words, Dan against Claude: "really" 2.3
   against 0.8; "very" 1.3 against 0.5; "kind of" 1.0 against 0.1; "things" 1.6 against 0.7; "going to" 9.4 against
   4.0; "which" 1.4 against 0.7; "just" 5.8 against 3.4; "so" 11.6 against 7.0; "like" 5.2 against 2.6; "right" 4.4
   against 2.1. Reading a Claude script on camera he does not put them back (the "Dan reading Claude scripts" row sits
   on Claude's numbers, not his).
2. **"and": 2.4 per 100 for him, 3.5 for Claude.** The same across 203,000 words of his speech, old and new.
3. **Sentences: his average 16.5 words with a spread of 11.8; Claude's 12.8 with 7.4.** He runs long loose setups and
   Claude writes short even ones.
4. **Contractions: 4.5 per 100 against Claude's 2.4.** Claude writes "it is" and "you are" where he says "it's" and
   "you're".
5. **"because": Claude uses more (3.9 per 1,000 against 2.4).** Claude explains with "because"; he more often says
   "so" and "which".
6. Three-item lists: 0.33 against 0.42. Swears: 0.03 per 100 against 0.08 (see `profanity-and-controversy.md`).
7. "actually" is NOT a content gap (0.9 for both). It is an ad gap, below.

**Ads (his own ads against Claude's ad scripts).**

1. **"actually": 0.7 per 1,000 for him, 5.1 for Claude.** Seven times his rate. The clearest single-word tell.
2. Sentences 14.3 words against 10.8. Kicker endings 6.1 percent against 12.8. Em dashes 0.03 per 100 against 0.94.
3. He asks more questions (0.35 per 100 against 0.15) and says "very" (1.1 per 1,000 against 0.1), "just" (5.5
   against 3.4), "now" (5.5 against 2.5) and "going to" (2.2 against 0.9) more.
4. "and": 3.0 against 3.4. His client ads (Tier 2) match his own on "and", sentence length and kickers.

**Conversion (his sales videos and letters against Claude's VSL and letter drafts; Claude's pile is small).**

1. **Sentences: 17.6 words against 8.9.** Claude chops sales copy into fragments. Kicker endings: 4.1 percent of his
   paragraphs against 29.7 of Claude's.
2. Em dashes: 0 against 1.72 per 100. "and": 2.9 against 3.8. Questions: 0.13 against 0.45 (here Claude asks more).
3. "very" 2.3 per 1,000 against 0.2; "really" 1.9 against 0.9; "going to" 3.9 against 1.1; "because" 2.4 against 0.9;
   "just" 5.0 against 2.7; "actually" 0.9 against 2.5.

**Products.** No Claude pile exists yet; the bench's cold-Claude run is the first one. His two registers differ: the
book (2007) is tight, 15.9 words a sentence, few contractions, more swearing than anything else he has made (0.55 per
100, though see the note on its explicit chapters in `passages-products.md`); the course videos (2021) are loose
teaching, 21 words a sentence, "so" 13 times per 1,000.

## Targets for a draft (until Phase B fits bands per type)

| measure | content | ads | conversion |
|---|---|---|---|
| "and" per 100 | 2.5 or under | 3.0 or under | 3.0 or under |
| sentence length, average | 15 or more, with long and short mixed | 13 to 15 | 15 or more |
| contractions per 100 | 4 or more | 3.5 or more | 4 or more |
| "actually" per 1,000 | about 1 | under 1 | under 1 |
| "really", "very", "kind of", "things", "just", "so", "going to" | present at about his rates above; a script with none of them reads as AI | "very", "just", "now" present | "very", "really", "going to" present |
| kicker endings (written pieces) | under 8 percent | under 8 percent | under 5 percent |
| em dashes | 0 | 0 | 0 |

No small word is ever required in a given sentence: sprinkle none in by rule. They show up when the sentence is built
the way he talks (a long setup, a plain turn), and the rate is the check, not the method.
