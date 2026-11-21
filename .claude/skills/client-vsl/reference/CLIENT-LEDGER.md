# The client ledger: nothing a client writes is ever lost again

**Rule.** Every instruction a client gives (brief, feedback doc, Upwork message, review-page picks and notes) and every
promise we make back goes into `CLIENT-LEDGER.json` in the private job folder, in the source's exact words, the same
turn it arrives. The film cannot be planned, built, reviewed or delivered past a failing ledger gate. Tool:
`.claude/skills/client-vsl/tools/client_ledger.py` (`--help` lists every command).

## Why (Joint Vigor, 2026-11-19: what actually went wrong)
Eric reviewed the trial lead in a detailed feedback doc on 11-09 (19 timestamp notes, seven overall directions) and
added a reference to it on 11-10. We replied "I can make every one of those changes", "Your feedback will be built
into the full VSL" and "I'll check it out before I start the full edit". The full film sent on 11-18 had none of the
timestamp notes and 80 of the sales-letter images he asked us not to reuse. Traced cause by cause:

| # | What failed | Evidence | What stops it now |
|---|---|---|---|
| 1 | **His notes existed only in his doc and our reply.** No file of ours listed them one by one. | The round 2 handoff shrank 19 notes to "Every timestamp revision will be made". | Sources saved word for word; one ledger item per instruction; quotes must match the source or `add` refuses |
| 2 | **Each round was planned from the last handoff plus his newest message**, in a fresh chat: a telephone game. | Round 3 handoff: timestamp notes gone. Round 4 plan: the no-sales-letter-images rule gone too. | `gate --stage plan` at the start of every round reads the whole ledger, not the last message |
| 3 | **The round structure only carried answers to OUR questions.** Notes that needed no A/B pick ("E doesn't need a comparison") had no round that owned them; the style lock was "written from the picks". | `STYLE-LOCK.md` of 11-16 has no line about his feedback doc. | The lock is written from picks AND every open ledger item; `gate --stage build` fails if an open item's id is in no brief |
| 4 | **"Approved" was invented.** He paid the $5 trial milestone and Dan approved the lead; the round 4 brief called it "approved by Eric" and said he "approved these rules in R1 to R3". His feedback doc was his review of that lead. | `BLOCKS-BRIEF.md` lines 8 and 16; a regression check then proved the head matched the un-revised trial. | `lint`: any "approved by the client" line must cite an approval item quoting his own words. A paid milestone, Dan's approval and silence are not approval |
| 5 | **Promises in our messages were not tracked.** The 11-10 reference he added, and our "I'll check it out", appear in no job file before 11-19. | No mention of it in any handoff or plan. | Our sent message is a source (`--kind ours`); each "will do" is a `promise` item. `recheck` flags a client doc that changed after we read it |
| 6 | **Every check compared the film with our own plan.** Six fresh reviews got the script, the lock and our rules, never his doc. Review F even wrote "I could not establish whether Eric approved this". | `REVIEWER-BRIEF.md` input list. | The reviewer gets his sources and `report --for reviewer`, marks every row; `gate --stage deliver` needs a PASS per item |
| 7 | **Dan's review page showed our fix list, not Eric's notes**, so Dan had no way to catch it. | `make_review_r2.py`. | The page opens with "What the client asked for", each row a chapter link |
| 8 | **The delivery message reported on picks only.** | Message of 11-18. | The message answers his notes one by one (`report --for client`) |

Seven of the eight are the same thing: the client's words were not an input to the step. Careful work on the wrong
target is what shipped.

## When to run what
| Moment | Do, in this order |
|---|---|
| **Round 0, intake** | `init`. Save the brief and every linked instruction doc as text in `<job>/client/`, `source` each, `add` one item per instruction, `itemized`. |
| **Any client message arrives** (before replying, before any other work) | Save it word for word, `source --kind message`. Fetch every doc it links, AND every doc already registered, again: `recheck` each (clients edit docs after sending them). `add` items. `itemized`. `sweep`. |
| **We reply** | After Dan sends: save the sent text, `source --kind ours`, one `promise` item per thing we said we would do or look at. |
| **Start of every round and every new chat on the job** | Read the client thread to its newest message yourself (not a handoff's summary), `sweep`, then `gate --stage plan`. A handoff never replaces this. |
| **Before the first render of a build** | `gate --stage build --brief STYLE-LOCK.md BLOCKS-BRIEF.md ...`. Every open item id must be in a brief, with its fix and its owner block. |
| **Fix landed in the finished master** | `done ID --at <film time> --evidence <frame pulled from the master>`. |
| **Before the reviewer** | `gate --stage review`. Give the reviewer `report --for reviewer` plus the client's source copies. |
| **Reviewer verdicts** | `review ID --result pass|fail --at T --by REVIEW-x` for every row. A fail is a MUST. |
| **Before Dan's page and before any client send** | `gate --stage deliver --file FILE --rows ROWS.json`. Paste its PASSED line into the receipt and the message draft. A send without it is not allowed. |

## Item rules
- **Exact words only.** Never paraphrase a client note into the ledger; `add` refuses a quote it cannot find in the
  source. Put our interpretation in the brief next to the id, not in the item.
- **One instruction, one item.** "Replace the TSL images at 5:38 and 5:41" is two film positions under one item; a
  whole-film direction ("Caucasian actors throughout") is a `rule` and is checked over the whole film, every round.
- **Positive notes are items too** ("I really like this split-screen scene", "please keep this caption style"): type
  `rule`, so a later change cannot remove what he liked.
- **Only the client drops a client item.** `waive` needs his words from one of his sources. Dan's approval, a SHIP
  review, schedule pressure or "it looks better this way" cannot close one. If we disagree, Dan asks him.
- **Newer client words replace older ones** with `supersede` (the brief said five testimonials; his feedback said
  three). Both stay in the ledger.
- **A style or key-visual pick is an `approval` item** quoting his pick message. It approves exactly what the page
  showed him, nothing around it.
- **Trial or sample footage is our draft** until he says in writing it is approved. Rebuild it from his feedback for
  the full film; never reuse it "as approved", and never write a regression check that proves the new film matches it.
- Questions he asks us are `question` items, closed when our answer is sent.
