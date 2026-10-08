# Handoff: Dan Voice Training Part 2 (the plan)

Written 2026-10-08 from a research session (two web research passes plus a local audit). Nothing in the project was
changed by that session except this file and its index lines. This plan absorbs
`handoff-20261006-dan-voice-training-part1-finish.md`: its steps 1, 2 and 4 run inside Phase A below, and its two-piece
blind test (step 3) is replaced by the test bench in Phase A.

## Goal and finish line

Dan: "write in my voice so well that nobody ever thinks that this is AI." Cloud and local sessions both.

The finish line is measured, not felt:

| measure | target |
|---|---|
| Model judges picking the AI piece out of a real/generated pair (chance is 50%) | 60% or less over 80+ trials |
| Dan's own blind test, 20 pairs | he picks the AI one 12 times or fewer |
| 2 or 3 people who know him and use AI a lot, same page | same |
| Dan's edit rate on real drafts (words he changes) | under 5% across a month |
| Hard rules (em dash, banned phrases) | 0 |

## What the research says (drives every choice below)

| finding | source | what it means here |
|---|---|---|
| Prompting alone is capped. Frontier models given 20 excerpts plus a style description lost to human writers with expert readers, and Pangram flagged 97% of it. A model fine-tuned on the author's own text was preferred and flagged 3%. | Chakrabarty, Ginsburg, Dhillon 2025, arxiv.org/abs/2510.13939 | A better guide will not reach the goal alone. Three lanes (below). |
| Current frontier models with five author samples are still caught about 90% of the time. | Epoch AI, July 2026, epoch.ai/data-insights/ai-detectors-false-negatives | Same. |
| Text a person wrote and AI only edited is hard to tell from human text; text AI generated is not. Editing an AI draft leaves it closer to the AI than to the person. | Shan, Lee, Hao 2026 (arxiv 2608.27855); Baumler et al. 2026 (arxiv 2604.24444) | His words first for anything that matters. Nothing Claude drafted counts as his voice, even after his edits. |
| Five examples beat none; going from 2 to 10 adds little. Formal registers imitate well (about 95%), informal ones poorly (17 to 66%). Topic-matched examples made imitation worse. | Wang et al. 2025, arxiv.org/abs/2509.14543 | 3 to 5 whole passages, chosen by format and length, never by topic. His casual register is the hard part. |
| Continuing a human opening beats following a style description by a wide margin (open models, essays). | Jemama and Kumar 2025, arxiv.org/abs/2509.24930 | Seed every draft with his real words and continue. |
| Heavy AI users catch AI text 93% of the time; five of them voting missed 1 of 300. Their cues: vocabulary 53%, sentence structure 36%, grammar too clean 25%, safe unoriginal content 24%, over-explaining 20%, tidy upbeat endings. | Russell, Karpinska, Iyyer 2025, arxiv.org/abs/2501.15654 | Judges must be AI-savvy. Tells are content and structure as much as words. |
| Detectors: Pangram near zero errors on human text; a pass means "not obviously AI", not "sounds like him". Humanizer rewriters still get caught. | NBER w34223; Pangram's own reports | Detector is a tripwire only. No humanizers. |
| Fine-tuning: no current Claude model can be fine-tuned. OpenAI closed it to new accounts on 2026-05-07 (checked on its deprecations page). Open models on Together cost $0.34 per million tokens for a 9B model, $4 minimum (checked on its pricing page). The Mac (M2 Pro, 32 GB) can train one locally for free. | vendor pages, 2026-10-08 | Phase C pilot costs $0 to $10. |
| Repo hooks, skills, agents and CLAUDE.md all load in single-repo cloud sessions; `~/.claude` files do not. | code.claude.com/docs/en/cloud-environments (checked) | Everything ships in the repo. One build trains cloud and local. |

Practitioner methods worth copying (mechanism only): a hook that runs the checker on every prose write
(github.com/Abdulkader-Safi/AI-Writing-Rules); detect-only scoring with a 2-pass cap and a threshold fitted on the
person's own documents (github.com/conorbronsdon/avoid-ai-writing); rule weights fitted on his corpus against AI drafts
(github.com/eric-tramel/slop-guard); two critic agents plus an edit-diff learner that promotes a rule after an edit
recurs twice (athola's scribe plugin; TravinDSO/myvoice-skill); voice kept separate from structure
(github.com/EveryInc/compound-writing); strength labels and an anti-performative section (Ruben Hassid; Sam Dumont,
dropbars.be). Reported failure modes: caricature (pet phrases become signature moves), drift in long sessions, guide
bloat, stiff text from blanket bans, right sound with the wrong take, and a corpus polluted with AI-assisted samples.

Ruled out: humanizer rewriters; optimizing against a detector score; picking samples by topic; a claude.ai Style on its
own (tone only); more rules in the guide; OpenAI or Claude fine-tuning.

## What the local audit found (2026-10-08)

1. **Part 1 learned mostly from the wrong Dan.** 26,451 of the 32,635 ad words are scripts he wrote for other presenters
   to older buyers (HBI and other SRM). The "Tier A/B content" pile is about 90% Claude's own lines. Only about 4,000
   words were him talking as himself. Total corpus about 170k tokens, under the smallest size the fine-tuning study tested
   (890k).
2. **Unused material, all his own:**
   - 192,378 words of his dictated messages in 1,139 local Claude session files (537 messages of 100+ words hold
     111,000 words), plus 809 Codex session files, uncounted. Path:
     `~/.claude/projects/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/*.jsonl` and `~/.codex/sessions/`.
   - 39,689 spoken words in 13 finished long-form SRTs in the project folder; 20,800 of them are four fully off-the-cuff
     videos (Spray Tan, Zepbound Update, Supplements, Invest In Health).
   - 902 word-level transcripts of raw rolls (project folder and the Extreme drive).
   - About 200 substantial sent-mail threads in the last year; anything sent before 2026-06-01 is guaranteed pre-Claude.
3. **A gap Part 1 missed, measured today.** Per 1,000 words, Dan off the cuff against the five videos where he read
   Claude-drafted scripts: "actually" 0.5 against 1.4; "really" 2.8 against 1.4; "very" 2.2 against 0.7; "kind of" 0.7
   against 0.1; "stuff" 0.7 against 0.0; "things" 1.6 against 0.5; "going to" 7.0 against 4.3; "which" 1.9 against 0.8.
   "and" per 100 words: 2.28 off the cuff, 2.54 dictating, 3.02 reading Claude scripts. Claude's scripts are too clean:
   his small everyday words are missing.
4. Nothing enforces the guide (a session runs `voice_stats.py` only if it remembers), no test has ever been run, and his
   edits are folded in by hand. Local memory has no `dan-voice-guide` entry yet.

## The design: three lanes

- **Lane 1, his words first.** For the VSL, sales letters, emails to the list, personal posts and anything read by people
  who know him: Dan dictates a 3 to 5 minute take, Claude orders and cuts, at least 80% of sentences stay as he said
  them, and anything Claude adds is marked for his eye. This is the only lane the research supports for "nobody can
  tell" today.
- **Lane 2, continue from his text.** For scripts, descriptions, captions, editor messages: whole real passages first,
  his own outline wording as the seed, written as a continuation by a fresh writer agent, checked by a fresh critic agent
  and a script. Scored on the bench until it hits the targets or stalls.
- **Lane 3, a small model trained on him.** A pilot, run only if Lane 2 stalls short of the targets: an open model
  fine-tuned on his real text re-voices Claude's draft, and Claude checks facts and hard rules.

## Phase A: real corpus, test bench, baseline. LOCAL, Opus 5.5 high

A1. **Leftovers from 10-06.** Run steps 1, 2 and 4 of `handoff-20261006-dan-voice-training-part1-finish.md` as written:
more ad scripts and video transcripts, the swearing and controversy pass
(`_shared/voice/profanity-and-controversy.md`), the seven raw copies the cloud refused, the swearing contradiction
between memory `swearing-never-cut-never-ask` and `WRITING-RULES.md` section 3, the local memory copy of
`dan-voice-guide`. Keep both held-out pieces held out. Skip its step 3.

A2. **Corpus v2, sorted by who is talking to whom.** One rule decides everything: **text Claude drafted is never his
voice, whatever he changed in it.** Only his changed lines are kept, as before/after pairs.

| pile | contents | used for |
|---|---|---|
| SPOKEN-SELF | off-the-cuff finished videos, unscripted raw rolls, the top videos with no transcript, any older recordings Dan names | the baseline for every script |
| DICTATED | his session messages of 40+ words, pasted blocks and tool text stripped | editor messages, emails, replies, his everyday vocabulary |
| TYPED-SELF | sent mail before 2026-06-01, the book, scripts and letters in his own name, his own outlines | emails, letters, descriptions |
| WRITTEN-FOR-OTHERS | HBI and other SRM scripts | persuasion structure only, never voice numbers |
| CLAUDE-DRAFTED | every Claude draft and his edited finals | pairs only |

Wispr Flow punctuates his dictation, so use DICTATED for word choice and order, not for sentence length. Raw text stays
out of the public repo: local folder `voice-corpus/` (add to `.gitignore`), mirrored to Drive. DICTATED and email piles
go in a **private** Drive folder (personal material is the exception in memory `drive-always-public`). Scrub names of
private people, contact details and anything personal from every excerpt that reaches the repo.

A3. **Re-measure against the right piles.** Rebuild `voice/STATS.md` with SPOKEN-SELF as the script baseline. Add a
function-word fingerprint (Burrows' Delta, `pip install faststylometry`, pooled samples of 2,500+ words) and one style
embedding (LUAR, `rrivera1849/LUAR-MUD`). Always report a ceiling (Dan against Dan, split in half) and a floor (Dan
against cold Claude, and against one other fitness creator's transcript).

A4. **Held-out set.** 40 passages of pure Dan, 150 to 450 words, about 8 per register (long-form spoken, short, ad or
letter in his own name, email or message, description or caption; fewer where the material is thin). List them in
`voice/HELD-OUT.md`. `scripts/voice/heldout_guard.py` fails if any guide or bank file contains an 8-word run from one.
For each passage write a content-only brief: the facts and the point in neutral words, none of his phrasing.

A5. **Bench.** `scripts/voice/bench.py`: a fresh subagent writes each brief under a named setup; each judge (a fresh
Claude subagent and Gemini, key on file, cap $5) sees 8 real reference passages plus one real/generated pair in random
order, picks the AI one and says why. At least 80 trials. Output to `Docs/voice-bench/<date>-<setup>.md`: judge accuracy,
reasons tallied by cue, Delta and LUAR against ceiling and floor, the stats gaps.

A6. **Baseline and Dan's blind page.** Score two setups: cold Claude with no guide, and today's guide. Build a private
page with 20 pairs (4 per register) where Dan clicks which one is his and can say why; votes saved; shareable to 2 or 3
people. Answer key in the chat report only.

## Phase B: rebuild the method. Local or cloud, Opus 5.5 high

Score every change on the bench and keep only what moves the number.

B1. **Contrastive extraction.** Have Claude write each non-held-out real piece cold from its brief and diff it against
his. The gap list, ranked by frequency, replaces description-from-reading as the source of rules.
B2. **Sample bank of whole passages.** `voice/bank/<register>/NN.md`, 12 to 20 per register, 150 to 500 words, tagged by
move (hook, story, mechanism, explanation, close) and length. A picker returns 3 to 5 by format and length, rotated.
B3. **Prompt layout.** Samples first in tags, then his seed words, then the request, phrased as "the next piece in this
set".
B4. **Positions and stories bank.** `voice/POSITIONS.md`: his take on each recurring topic and his stock stories with
real numbers, each with its source, mined from SPOKEN-SELF and DICTATED. No take in the outline or the bank: one
question to Dan or a `[DAN: ...]` gap. Honors memory `personal-facts-only-when-relevant`.
B5. **Rewrite `DAN-VOICE.md`.** Voice (how sentences sound) apart from structure (how he argues and sells). Each rule
labelled HARD RULE, STRONG TENDENCY or LIGHT PREFERENCE, with a floor and a ceiling where it is a rate. An
anti-performative section: no pet phrase is ever required; cap each per piece. Add the small-words finding. Stay under
1,700 words; mechanical rules move into the script.
B6. **`scripts/voice/voice_check.py`.** Extends `voice_stats.py`: hard fails (em or en dash, phrases he has cut), rate
bands per register fitted on his piles against Claude drafts, clusters scored above single hits, the function-word
fingerprint, kicker endings, "not X but Y", content triads. One score plus the offending lines. Detect only.
B7. **Two agents in `.claude/agents/`.** `dan-voice-writer` drafts in a fresh context with the samples loaded (fixes
drift). `dan-voice-critic` sees only the draft and 8 samples: pass 1 marks sentences he would never say, pass 2 marks
sentences that perform his voice too hard; tags WRONG, OVERSTATED, MISSING. Rewrite flagged spans only; 2 passes at most.
B8. **Hook.** In `.claude/settings.json`: hard rules only, on text going to Google Docs, Gmail drafts and script files.
Report-only for the first week, then blocking. The full score runs inside the writer agent, not the hook.
B9. **Lane 1 mode.** A `/dan-voice` skill with an "assemble" mode for dictated takes.
B10. **Rewire the eight writing skills** to hand their content plan to the writer agent, and delete the voice rules they
each carry.
B11. Re-run the bench after each change, three rounds at most, then a second blind page for Dan.

## Phase C: fine-tune pilot. Gated. Local, Opus 5.5 high

Run only if, after Phase B, judges are still above 60% or Dan picks more than 12 of 20. Data: the pure piles only,
chunks of 250 to 650 words, each paired with a neutral summary of its content; the held-out set stays out. Train a LoRA
on an 8B to 12B open model with MLX on the Mac (free), or on Together (about $4 to $10 a run). Use it as a re-voicer:
Claude's draft goes in a chunk at a time, Claude then checks every fact against the content plan and applies the hard
rules. Adopt it only if it beats Phase B by 10 points or more on the judges. Known risks: voice drift, em dashes
creeping back, a corpus still smaller than anything the research tested.

## Phase D: learning loop and rollout. Sonnet 5.5 medium

D1. `scripts/voice/voice_diff.py`: save each delivered draft; when Dan finalizes, diff it against his final, keep voice
edits only as pairs in `voice/pairs.md`, compute the edit rate. An edit seen twice becomes a proposed rule; Dan approves
proposals in one batch.
D2. A monthly tune-up routine: fold in the pairs, re-run the bench, trim the guide to budget, report in five lines.
D3. Every surface: the repo (cloud and local), the local memory copy and `scripts/sync-memory-to-repo.sh`, the voice
skill enabled on claude.ai so chat, phone and cloud sessions load it, one pointer line in `AGENTS.md` for Codex.
D4. Update `Docs/VOICE_CORPUS_INVENTORY.md`, memory `dan-voice-guide`, `Handoffs/README.md`, the board line.

## What Dan provides (one sitting)

1. Links or folders for any older recordings of him talking as himself (podcasts, webinars, course videos, old
   channels) and any personal writing he wants included.
2. Yes or no on reading his sent mail from before June 2026 for the email register (kept in a private folder).
3. Two or three people who know him and use AI a lot, for the blind page. Optional.
4. Whether Lane 1 (dictate first) is acceptable for the VSL, letters and list emails.
5. Optional: a Pangram account for an outside detector score (about $0.05 per 100 words; he signs up himself).

## Spend

Transcription a few dollars, Gemini judging up to $5, the fine-tune pilot $0 to $10. All inside the standing $25
session cap. Pangram is separate and optional.

## Starter prompts

**Phase A. Task name `Dan Voice P2A Corpus + Bench`. Local. Claude Opus 5.5, high effort.**

> Run Phase A of `Handoffs/handoff-20261008-dan-voice-training-part2-plan.md` (it also covers steps 1, 2 and 4 of the
> 10-06 finish handoff). Use subagents for the reading. Extra sources from me: [links or "none"]. Sent mail before June
> 2026: [yes / no]. End with the baseline scores and my blind test page.

**Phase B. Task name `Dan Voice P2B Method`. Local or cloud. Claude Opus 5.5, high effort.**

> Run Phase B of `Handoffs/handoff-20261008-dan-voice-training-part2-plan.md`. Start from the newest file in
> `Docs/voice-bench/`. Score every change on the bench and keep only what moves it.

**Phase C (only if Phase B says so). Task name `Dan Voice P2C Model Pilot`. Local. Claude Opus 5.5, high effort.**

> Run Phase C of `Handoffs/handoff-20261008-dan-voice-training-part2-plan.md`. Budget $10.

**Phase D. Task name `Dan Voice P2D Loop + Rollout`. Local. Claude Sonnet 5.5, medium effort.**

> Run Phase D of `Handoffs/handoff-20261008-dan-voice-training-part2-plan.md`.
