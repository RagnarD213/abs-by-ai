# Dan vs. Claude by the numbers (baseline, 2026-10-06)

Measured with `scripts/voice/voice_stats.py` in Dan Voice Training P1. Counts are per 100 words. Definitions are in the
script's header. Part 2 (the AI-tell checker) uses these numbers as its thresholds. The raw text is on Drive (folder
`1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`), never in the repo, so to re-run you rebuild the piles from there.

## The piles

| pile | what is in it |
|---|---|
| Dan ads, Tier A | 10 finalized Social Response Marketing scripts 2019 to 2025 (HBI, Spy Briefing, CPA offers, Physio Tru, Darren Fujiyama, his own consulting and course videos), the HBI top-10 SRM scripts (minus the one held out for the blind test), plus the lines Dan typed into the Abs By AI batch-1 ads, his Ad 1 and Ad 3 outlines and his parts of the /start letter |
| Dan content, Tier A | his own outlines (April to October 2026), his typed inserts in Claude outlines, and the off-the-cuff Oura review transcript |
| Dan content, Tier A/B | the above plus his edited finals of Claude drafts (9/23 shoot, Shoot 5). B finals keep about 90 percent of Claude's lines, so this pile leans toward Claude |
| Book | about 11,600 words of "15 Steps to Profitable YouTube Advertising" (2019 to 2020) |
| Keith + Wes | their HBI top-10 scripts (only about 1,800 words; treat as indicative) |
| Claude drafts | the 9/23 drafts as delivered, the 09-19 Zepbound / Alcohol / Not Losing Weight drafts, the Make Time shorts draft, the Claude/Fable ad outlines, VSL Version A, Claude's parts of the /start letter, the unapproved /start VSL |

## The table

| source | words | and | lists3 | questions | you | contractions | swears | emdash | sent_mean | sent_sd | para_words | punch_pct | oneline_pct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dan ads, Tier A (all) | 32635 | 3.03 | 0.43 | 0.25 | 6.1 | 3.62 | 0.0 | 0.06 | 14.5 | 6.5 | 25.9 | 6.3 | 9.9 |
| of which HBI + other SRM 2019-25 | 26451 | 2.95 | 0.42 | 0.21 | 6.09 | 3.71 | 0.0 | 0.07 | 14.8 | 6.6 | 27.3 | 5.9 | 8.4 |
| of which Abs By AI (Dan-typed) | 6184 | 3.36 | 0.45 | 0.44 | 6.13 | 3.22 | 0.02 | 0.03 | 13.2 | 6.1 | 21.4 | 8.0 | 15.2 |
| Dan content, Tier A only | 11570 | 2.42 | 0.32 | 0.11 | 5.64 | 3.19 | 0.03 | 0.01 | 14.3 | 7.9 | 23.9 | 10.9 | 30.6 |
| of which spoken transcript | 4000 | 2.2 | 0.28 | 0.2 | 5.5 | 4.03 | 0.1 | 0.0 | 15.4 | 8.8 | n/a | 13.5 | n/a |
| Dan content, Tier A/B | 37762 | 3.08 | 0.47 | 0.1 | 6.52 | 3.16 | 0.04 | 0.0 | 13.3 | 7.1 | 29.5 | 11.1 | 14.8 |
| Book (2019-20) | 11610 | 2.41 | 0.23 | 0.09 | 4.34 | 2.7 | 0.02 | 0.63 | 18.6 | 7.5 | 34.7 | 3.3 | 7.2 |
| Keith + Wes | 1779 | 2.98 | 0.39 | 0.11 | 4.55 | 2.53 | 0.0 | 0.0 | 16.2 | 9.2 | 31.8 | 10.0 | 17.9 |
| Claude drafts (all) | 23669 | 3.55 | 0.41 | 0.13 | 6.7 | 3.21 | 0.05 | 0.41 | 12.1 | 7.1 | 30.9 | 16.1 | 6.1 |
| of which content | 17055 | 3.55 | 0.46 | 0.06 | 6.74 | 2.91 | 0.08 | 0.0 | 12.9 | 7.3 | 35.5 | 13.7 | 4.2 |
| of which ads/VSL/letter | 6614 | 3.55 | 0.26 | 0.3 | 6.59 | 3.98 | 0.0 | 1.45 | 10.4 | 6.3 | 23.1 | 20.8 | 9.4 |

Same nine scripts, Claude's draft against Dan's edited final (9/23 long-forms, calories pair, Zepbound, Alcohol, Make
Time shorts): "and" 3.54 to 3.41, kicker endings 12.5 to 10.0 percent, swears 0.08 to 0.05. Every move is in the same
direction as the gaps below, but small, because he leaves about 90 percent of lines alone.

Caveats: the transcript's paragraphs are subtitle chunks, so its paragraph numbers are meaningless. Outlines are one
bullet per line, which inflates `oneline_pct` for the Tier A content pile. Keith + Wes is a small sample.

## The five biggest Dan-versus-Claude gaps

1. **"and": confirmed. Claude uses it about 45 percent more than Dan's own writing.** Claude 3.55 per 100 words in
   every kind of piece. Dan's own content, his spoken transcript and his book: 2.2 to 2.4. His ad scripts written for
   other people to read: 3.0 (still 15 percent under Claude). Dan's sense was right. Target: 2.5 or under in content,
   3.0 or under in ads.
2. **Kicker endings: Claude ends paragraphs on a short punch 2.5 to 6 times as often.** Share of multi-sentence
   paragraphs whose last sentence is 6 words or fewer: Claude ads 20.8 percent, Claude content 13.7; Dan ads 6.3, his
   book 3.3. This is the "snappy kicker" Dan keeps cutting, now measured. Target: under 8 percent in ads.
3. **Em dashes: about 25 times Dan's rate.** Claude's ad, VSL and letter drafts: 1.45 per 100 words. Dan's ad scripts
   from 2019 to 2026: 0.06 (he writes a spaced hyphen or "--"). Even his 2019 book (0.63) is under half Claude's rate.
   Target: 0, the standing rule.
4. **Claude's sentences are shorter and more even.** Ads: Claude 10.4 words per sentence against Dan 14.5. Content:
   12.9 against 14.3 (Tier A), with a spread of 7.1 against 7.9 to 8.8 (Dan swings more between long setups and short
   turns). The book runs 18.6. Claude chops ad copy into fragments; Dan lets setups run and keeps the short sentence for
   the turn.
5. **Three-item lists: a content tell, not an ad tell.** In content Claude writes 0.46 per 100 words against Dan's 0.32
   (his book 0.23): about 45 percent more. In ads there is no gap (Dan's SRM scripts use 0.42, often "even if…, even
   if…, and even if…"). So the rule is "fewer tidy triads in scripts and articles", not "never list three things".

Also measured:
- **Claude swears more than Dan, not less.** Claude content 0.08 per 100 words; Dan's finals 0.05; his Tier A content
  0.03. The skills told Claude to swear, and it bolts swears on as punchlines, which he cuts (`../DAN-VOICE.md`,
  section 8). Write a swear where he would aim it at bad advice, not to sound edgy.
- **Questions:** in Abs By AI ads Dan asks more than Claude (0.44 against 0.30 per 100 words): short question-then-answer
  pairs about food and bodies. In content both are low.
- **"you" and contractions:** no meaningful gap. Both write in second person and spoken register.
