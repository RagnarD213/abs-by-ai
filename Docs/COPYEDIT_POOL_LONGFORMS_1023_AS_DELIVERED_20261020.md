# Copy polish, the seven 10/23 pool long-form scripts: as delivered 2026-10-20

Doc: "Gym Shorts Scripts - Friday 10-23 Pool Shoot" (`11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA`), from the heading
`SCRIPT: I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time` to the end. Run by Fable 5.1 from
`Handoffs/handoff-20261020-pool-longforms-fable-copy-polish.md`. Baseline: `Docs/SCRIPTS_1023_POOL_LONGFORM_DAN_EDITED_20261020.md`;
the doc matched it exactly (only his three soft line breaks render differently), so nothing of his had changed since.

Method: Docs connector, `suggest_builder.py` + `verify_suggestions.py`. The direct send was checked with a whole-doc
diff: 29 planned lines changed, nothing else. The tracked send was checked the same way: reject-all view identical to the
doc before it, accept-all view differs by exactly the five suggestions. Em dashes in the section: 0 before, 0 after.

## Straight in (29)

- "every single" to "every" in 13 places (the swap on record, 12 of 12 accepted): scripts 1 (2), 2 (1), 3 (1), 4 (3),
  6 (5), 7 (2). Left alone: "Every single one." in Never Sore, a standalone fragment, not a modifier.
- Hyphens: "two hour workout" to "two-hour" (twice, script 1); "five minute workout" to "five-minute" (twice, Never
  Sore, matching "15-minute" in script 1). "total-body workout" to "total body workout" (script 1) to match Dan's own
  "total body" everywhere else. "high risk" left unhyphenated: Dan types it that way in his own 10/20 lines.
- Bulking: period added after "But if you're fat and strong, you just look sloppy".
- Stop Squatting: "So between those three exercises" to "four" (Dan added the leg press). The on-screen cue now lists
  LEG PRESS and the B-roll cue says ALL FOUR.
- Never Sore: on-screen cue "1. YOU SKIP TOMORROW" to "1. MORE LIKELY TO SKIP", matching his softened line.
- Word-count lines recounted on all seven (spoken words only, minutes at 150 a minute):

| Script | Was | Now |
|---|---|---|
| I'm 41, first time in a gym | 1452, 10 min | 1587, 11 min |
| 5 Muscles Women Notice | 1078, 7 | 1077, 7 |
| Fix Your Posture | 1084, 7 | 1083, 7 |
| Stop Squatting | 996, 7 | 1075, 7 |
| Bulking Is A Scam | 1220, 8 | 1384, 9 |
| Why I Never Get Sore | 1115, 7 | 1187, 8 |
| Body Part Splits Are Dead | 1131, 8 | 1038, 7 |

## Tracked for Dan (5)

1. 5 Muscles: cut "So your abs can be there, and you can be training them hard, and they're still covered up." It repeats
   the sentence before it ("nobody will ever see them under a layer of fat").
2. Posture: cut "Your back muscles are the muscles that pull your shoulders back." from the "So why does this work?"
   paragraph. The same sentence is spoken word for word in the opening.
3. Posture: cut "So stretch your chest after every workout, so your shoulders can open back up." It restates the two
   sentences before it; "You can do it right there at the gym before you leave." stays.
4. Never Sore: "Firas Zahabi is one of the best MMA coaches in the world. He coached Georges St-Pierre." to "Firas Zahabi
   coached Georges St-Pierre." He was introduced twice in a row; this cuts Claude's intro and keeps Dan's THEY / YOU line
   whole ("Firas trains some of the most elite MMA athletes in the world. If he's recommending THEY...").
5. Body Part Splits: "Third, Greg Nuckols. Greg Nuckols is a respected strength coach and researcher, and he looked at 13
   studies." to "Third, Greg Nuckols, a respected strength coach and researcher, looked at 13 studies." The same fix Dan
   made himself for Schoenfeld in the paragraph above.

## Named in chat only (no edit)

- Bulking, "Move to a 10% caloric deficit - about a net cut of 500 calories.": the handoff read 500 as a mismatch with
  the 2,500-calorie example (10% = 250). It checks out as written: from a 250 surplus to a 250 deficit is a net cut of 500.
- Bulking: "Even a guy without that much muscle looks great if he's lean" plus the Brad Pitt split-screen cue and "But if
  you're fat and strong, you just look sloppy." sit after the cut-first advice. They could move up, right after "the lean
  guy with abs is the one who looks bigger." A move is not worth a tracked edit; Dan's call.

## Left alone on purpose

- Every line Dan typed on 10/20 (curly apostrophes), his CAPS words, the swear in the bulking close, the Brad Pitt cue,
  his bulking story, "more likely to skip".
- The short openings (hook, one credibility line, a sentence or two of context, point one). No warm-up found to cut.
- "I've got" / "you've got": Dan's own 10/20 line uses "you've still got", so the swap to "I have" does not apply here.
- The 29 shorts above the long-form section, and their four pending suggestions from the 10/18 and 10/19 passes.
- His three soft line breaks (shift+enter) in the "train your mind" paragraph and after "and you go home."

## Next

Dan rules on the five suggestions (Tools > Review suggested edits, or the cards in the right margin). Then the filming
documents per `/copy-edit`, "When the scripts are final: make the filming documents", in time for Friday 10/23.
