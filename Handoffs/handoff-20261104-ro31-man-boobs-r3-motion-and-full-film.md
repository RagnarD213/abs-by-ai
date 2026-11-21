# CONTENT (LFC). Man Boobs LFC R3: AI motion, juice stock, full film, gates, independent review

Video: "How To Get Rid Of Man Boobs" (RO-31), organic long-form, 10/15 studio roll C1775. Claude, Opus 5.5 high (started on Claude).
Release: Sun Jan 24 2027 (January blitz). Recipe and lessons: `.claude/skills/longform-edit/reference/ro31/README.md` (read it, then `../ro29/README.md`).

## Where it stands
- Work dirs: `/Volumes/Expansion/_edit_work/RO-31/round1/` (cut, plan, recipe, first minute, graphics renders) and `round2/` (AI frames).
- Round 1 page http://127.0.0.1:9641/ (reviewed). Round 2 frames page http://127.0.0.1:9642/ (reviewed).
- Decisions with Dan's words and frame hashes: `round2-plan/decisions.json` (round 1 notes) and `round2-plan/decisions-r2.json` (frames).
- Locked: colour A (`frames.GRADES["A"]`), voice warm bass plus (`round1/fit/eq.txt`), the first minute, all graphics and clips,
  the chest diagram, both ad-libs. Killed: A3 Jiggle Belt, A4 Four Straws, A8 Diet Books (presenter stays on camera; G12 stays).
- Cut: 3:52, EDL `round1/edl.json` (all restarts removed, junk pass clean). Plan `round1/recipe/plan.py`, timing `round1/plan_resolved.json`.

## Approved frames (motion authorized: Dan, 2026-11-04, "all frames are looking good. I like X1 for the intro...")
| slot | file pair (round2/aiframes/) | slot time | line |
|---|---|---|---|
| A1 opener | google/O3-start.jpg, google/O3-end.jpg | 0:00-3.2 | You think that you have man boobs, but you don't |
| A2 Pool Shirt | codex/A2-start.png, codex/A2-end.png | 12.8-16.2 | Watch this video if you're tired of hiding your chest... |
| A6 Doctor Visit | google/A6-start.jpg, google/A6-end.jpg | 65.0-68.3 | If you want a diagnosis, a doctor can tell you in about a minute |
| A5 T-Shirt Double Take | codex/A5-start.png, codex/A5-end.png | 140.4-144.3 | you'll be shocked at how different your chest looks in a T-shirt |
| A7 Locker Room Flex | codex/A7-start.png, codex/A7-end.png | 161.7-167.1 | Anabolic steroids... (G10 lower third rides over it) |
Each pair passed `framecheck/gate.py --verify` (gate + fresh frame-reviewer). Hashes in decisions-r2.json; re-hash before use.
Defaults where Dan did not answer: juice line (A4 slot, about 116.6-121.7 "And cut every liquid calorie...") gets STOCK footage of juice
poured down a sink (Pexels; grade it); the bodybuilder stays the Locker Room Flex as shown.

## Next actions, in order
1. `editcap.py acquire RO-31 --title "Man Boobs LFC R3" --type LFC`; rename the task `Man Boobs LFC R3`; `queue.py set RO-31 in_progress --by Claude`.
2. Motion on the Flow subscription (`_shared/veo/README.md`): `veo.py add` each pair, Veo 3.1 Fast; A1 gets 2 takes (hook);
   all slots are 3 to 5.5 s, so also queue an Omni twin (`<ID>o`, 4 or 6 s) per the README's short-clip rule. Spawn `flow-veo` in the background.
   Motion prompts: calm, natural, closed mouth, no shaking (VIDEO-RULES 2026-10-21). A1: he looks down at his chest, then holds the shirt flat over it and glances at the others.
3. Every take: `clipcheck.py` + a fresh frame-reviewer with the three sense questions; regenerate failures; never stretch a take to fit.
4. Stock for the juice slot (Pexels search "pouring juice sink", grade to the film), replace the A4 ai item with a clip.
5. Plan: A1..A7 ai items become clips (RO-29 plan.py bottom block shows how), AI-GENERATED chip clear of faces; resolve; render the
   FULL film (`build.py` via the recipe; ro29 `finish.py`/`chain_r2.sh` for the master path). Finish the voice WITHOUT the between-words
   gate so the artifacts row passes (round 1 first minute failed it narrowly); tone row fails by design (warm bass plus).
6. Gates on the exact master: edit sheet, `deliver/gate.py --format longform`, watch pass + judge, hair every 0.25 s (20 px), audio joins.
7. Independent `ra-reviewer` on the full film; fix; then deliver: page with the full film (1080p review copy only, AGENTS 2026-11-02),
   `Videos to Review/Man Boobs LFC R3 - full film.mp4`, `queue.py set RO-31 delivered`, mirror the Edit Queue db, release the slot.

## Open risks
- Codex image tool refuses man-boobs images; Google made them. Do not reword around refusals.
- A local commit (5a3d064, board + queue + ro31 recipe) was not pushed: another session's live file blocked safe-push. Re-run safe-push.
- Speech to flag for Dan in R3: "Zetbound" at 3:24 and "so the area turned into" at 2:08 (only reads of those lines).

## Starter prompt
> Read `Handoffs/handoff-20261104-ro31-man-boobs-r3-motion-and-full-film.md` and execute it: Man Boobs LFC R3. Generate the approved AI clips on the Flow subscription, put stock on the juice line, build the full film, run every gate and an independent review, deliver the review page, and update the master list.
