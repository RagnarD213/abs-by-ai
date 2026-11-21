# Hormozi Fat Guy Off-Cuff SFC R1 (DS-44B): the off-the-cuff take, in the locked reaction format, to compare with the scripted Short

**CONTENT (SFC), a dedicated green-screen reaction Short. Fire now. Recommended: Claude Opus 5.5, high** (the video started on Claude).

## What Dan decided (2026-10-23)
- He approved the scripted version, "Alex Hormozi Asks A Fat Guy Why He Isn't 200 Pounds Heavier. He's Right." (DS-44 R2), and
  locked its structure as the format for reaction videos (`_shared/VIDEO-RULES.md`, "Reaction videos: the locked format").
- Dan: *"for all of these reactions, we filmed the scripted take and an off-the-cuff take. There should be an off-the-cuff take
  right after the scripted take and the raw footage. I want a second handoff to edit the off-the-cuff take of this so I can
  compare it to the scripted."*
- The setup task (thumbnails) runs in parallel and holds upload/queue until Dan picks a version
  (`handoff-20261023-ds44-hormozi-setup-hold.md`). This edit decides nothing; Dan compares and picks.

## The approved scripted version (the comparison)
- `Short-form video content/Hormozi Fat Guy - DS-44/Hormozi Fat Guy SFC R2 - complete Short.mp4` (61.228 s, SHA-256 starts
  `9d8deb8da3d5eb2b`), review `ROUND-2-REVIEW.md` (SHIP), recipe `recipe-r2/`.
- Work folders: `/Volumes/Expansion/_edit_work/DS-44/r1/` (all caches) and `r2/` (round 2 code; key/src/audio symlink to r1).

## The off-the-cuff take
- Roll: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4`,
  slate "off the cuff reaction to Alex Hormozi" at 2317.7 s, take **2325.0 to 2391.0** (lav left channel, `pan=mono|c0=c0`).
- What he says (roll sidecar, whisper small; re-transcribe 2318-2392 with medium.en and measure every cut on energy, as R1 did):
  "Okay, so this is a critical insight from Alex Hormozi... even a lot of hardcore Hormozi fans haven't heard this one, but he
  makes a great point here. Everyone does know how to stop eating. You just stop at the wrong point... the answer is Zepbound. So
  you heard that guy say in the clip, well, the reason why I'm not 200 pounds heavier is because I can't eat that much, but he
  could eat enough to get him significantly overweight. Imagine though, he just moves that stopping point earlier... Oh, I can't
  eat any more than that. [is what Zepbound does for you: ABANDONED, ~2364.3-2365.8] That is what Zepbound does for you
  [restart 2367.66]. It moves your stopping point... dial in your dosage... So you know how to stop eating, you're just stopping
  at the wrong point. Take some Zepbound and move that stopping point to the correct place. Subscribe to my channel for more
  exercise and nutrition insights like this." (ends 2390.8)
- Cut the abandoned fragment (keep the restart, last clean take rule), the leading "Okay," if it reads as a slate, dead air and
  any stumble (VIDEO-RULES "Stumbles inside a kept take get fixed"). Scripted claim lines are pre-approved; off-the-cuff lines
  are his own words, keep them as said (Zepbound is fine in organic).
- **Length:** the take is ~66 s and the clip opening is 15.4 s, so the natural cut is ~78 s, over the 66 s dedicated-Short
  ceiling. Get as close as possible by cutting only restarts, repeats he says twice ("you know how to stop eating, you're just
  stopping at the wrong point" appears twice) and pauses. Do not drop a point he makes once. If it cannot reach 66 s without
  losing meaning, deliver the shortest clean cut and state its length plainly on the page; Dan decides.

## Reuse (do not redo)
- **Opening and handover:** identical to the approved R2: same clip segments, the corner from `r1/key/c2_watchF/` (full-height
  key, laptop), `elbow_fw` soft edge, the shrink into the 16:9 card. Reuse frame for frame; only Dan's first words change.
- **Interview behind his head:** the same card (`r1/src/card_58-74_24fps.npy`, Hormozi's continuous shot) for about the first
  30 s of the Short, ending at a natural break in what he says.
- Colour B Warm Vivid, voice house + 1.5 dB at 120 Hz (`r1/prep.py` E_EQ), captions style, graphics family: all approved.
- Key: house key, same plate (`r1/key/plate_q.npy`); key ONLY the new talk range, through `run_key.sh` pieces (laptop cropped),
  caches beside the old ones (e.g. `c1_O`, `c2_O`). The stage-1.5 pool can hang under memory pressure: resume skips finished
  frames (see `.claude/skills/shorts/SKILL.md`, DS-44 sections, and `shorts/reference/ds44-reaction-format/README.md`).

## What changes vs the scripted cut
- Cutaways: keep the caller from the clip on "you heard that guy say in the clip... 200 pounds heavier" (it fits this take even
  better). The bathroom-scale clip A0197 only if he talks about weighing (he does not here: likely drop). The pen B-roll B0351
  on the Zepbound lines. Coverage off Dan must stay at 30 % or more.
- Graphics (Soft Blue Light HyperFrames, eyebrow CAPITALS, title case): source tag ALEX HORMOZI only on Hormozi's shot (as R2);
  key points that distil what he says in THIS take (the scripted "2 Pounds Over" rule is not said here, do not reuse it); the
  subscribe tag. Keep graphics clear of his chin while the card is up (he sits lower).

## Steps
1. Category CONTENT SFC. Name the task `Hormozi Fat Guy Off-Cuff SFC R1`. `editcap.py acquire DS-44B --title "Hormozi Fat Guy
   Off-Cuff SFC R1" --type SFC` before any render (exit 3: arm `editcap.py wait DS-44B` in the background, tell Dan, stop).
   Add DS-44B to the edit queue (`scripts/edit-queue/queue.py`) and mirror it to the Edit Queue page.
2. Work folder `/Volumes/Expansion/_edit_work/DS-44/offcuff/`, code copied from `r2/recipe/`; transcribe, edit list, key the
   new range, framing, graphics, captions, assembly, as R2.
3. Every gate (delivery gate, audio gate, watch pass), key measures, then an independent `ra-reviewer`; fix until SHIP.
4. Review page with **both versions side by side** (the approved scripted R2 and this cut), their lengths, and one question:
   which one ships. Copy to `Videos to Review/`. `editcap.py release DS-44B --review`.
5. When Dan picks: tell the setup task (or Dan) which file is final; the other stays filed, unqueued.

## Starter prompt
> Hormozi Fat Guy Off-Cuff SFC R1. Read `Handoffs/handoff-20261023-ds44-hormozi-off-the-cuff-take.md` and execute it: edit my off-the-cuff Hormozi reaction take (C1730 2325-2391) in the locked reaction format, reusing the approved scripted Short's opening, card, key, colour and voice, run every gate and an independent review, and give me a page with both versions side by side so I can pick one.
