# Batch9 R2 revisions: deferred behind M2 work

2026-11-15. Owner: original Codex chat. Owning Mac M2. No production has started for R2. Do not acquire an edit slot or enqueue builds merely because one slot is free. Dan specifically requested this edit only after nothing is waiting for the M2. Conservatively wait until other active/waiting edits and render steps have drained, then normal editcap/renderq still apply. This is a deferred revision record, not an armed automatic wake or scheduled task.

## Dan's decisions

- Bodyweight squat: the content and form look good. Trim the dead time at the end only. Dan expects about14–15seconds after trim. Preserve his accepted picture/grade/content. End with the final complete spoken word; do not add narration unless the actual trim would fall below10s.
- Battle ropes: trim the extra pause at the end.
- Push-up: trim the end; add useful content only if needed for duration, never padding.
- Knee push-up: same end trim/content rule.
- Dumbbell shoulder press: ending is good, preserve it. Remove the unnecessary middle pause. Tighten narration timing and choose/re-time natural-speed picture spans so every directional cue still matches motion. Do not speed or reverse a rep.
- Curl: remove unnecessary internal pauses. Rename and re-narrate as Hammer Curl. This is the neutral-grip movement. Use existing app identity `db-hammer-curl`; do not install neutral-grip footage as `db-curl` or rename the app's distinct supinated exercise. Fetch current live Hammer Curl demo for the correct side-by-side, retain Dumbbell Curl's existing AI unless suitable supinated footage is separately found. B0432/B0031 re-screening needed only for any separate true Dumbbell Curl replacement.
- Side lateral: Dan explicitly accepts the real take and requests a demo from it. His words: "And make one for the side lateral. My side laterals were fine the way I did it in that real video." Use B0450/original continuous source, natural speed, full movement and appropriate narration. This supersedes the R1 form hold and pickup recommendation; do not re-ask him about it. Source acceptance is not approval of an unbuilt delivered demo.
- Standing rule: end when talking stops. No silent padding. Remove unnecessary internal pauses. Add useful explanation to meet target length when needed. Target15seconds, never under10.

## Preserve and verify on resume

R1 reviewed files, reports, exact SHA manifest and page remain intact. `review_clearance.json` contains the six R1 exact files. R2 gets separate outputs and fresh audio/delivery stamps plus independent reviews. R1 gate PASS did not catch Dan's pace/tail objections; never present those stamps as clearing R2 or the new rule. Add rejection examples to regression corpus before changing any gate. The old demo format's dead-air exemption/1s-tail allowance conflicts with this instruction and must not waive the new check. Gate changes need normal regression checks and version bump on the exact implemented change, run only after queue admission.

Reuse source/voice/build tools from `/Volumes/Extreme/_edit_work/REALDEMOS-B09`. Read current files on M2, not stale M6 tools. No paid image/video generation needed. Extra cloned narration only if necessary, record usage/cost under existing authorization. All checks silent. Deliver1080p comparison review on existing port9870, changed timing/watch ranges, exact-file gates, independent review, paused/sound-ready owner handoff, then stop for Dan's review. Install/deploy only after he approves the revised exact files, under existing authorization.

## Queue and continuation limit

At deferral the M2 had DS-109, RO-24 and REALDEMOS-B08 active, multiple render steps waiting,8/8 edit cores occupied. No B09 production slot or render ticket is held. Existing priority controls support urgency and normal waiting order, but no native idle-only automatic wake is configured for this chat. No heartbeat automation was created. On the next resumed turn, first run `python3 .claude/skills/_shared/editroute/resume.py check REALDEMOS-B09`, then `round2/admission.py` on M2. Exit3 means remain deferred; exit0 means verify ownership and acquire normal edit slot before production. Do not claim this record itself will restart the chat.

Bookkeeping: the M6 board check passed at2500/2500words after B09's compact entry update; only B09's entry was edited. No unrelated entries, running processes, queue priorities, gate thresholds, or media were changed.

## One-time10p.m. backup, added after deferral

Dan: "Okay I'll resume this once the priority work is done. If I haven't resumed it then resume this edit at10pm tonight" (2026-11-15). Native Codex heartbeat `resume-batch-9-at-10-p-m` is ACTIVE, one occurrence at22:00 America/Chicago tonight, attached to original thread01a1e07d-6d4d-7812-8af5-43a6bab12fa0. This supersedes the earlier no-auto-wake note for this single fallback. Before firing/working, check for manual resumption and do not duplicate work. Pause this backup when manual production resumes or when it fires. Keep M2 idle-only admission and normal queue gates. If M2 is still busy at22:00, remain deferred and report that condition; no recurring monitor is authorized.

##10p.m. execution

At22:00 November15 M2 admission returned idle, with no other active/waiting edits or render steps. No manual R2 production had begun. The one-time backup fired and was deleted. Original chat acquired M2 slot and built seven R2 candidates; fresh independent checks are underway. No revised file is approved or installed.

## Completed for owner review

November16: all seven revised candidates rendered and cleared by fresh exact-file gates and independent reviews. The1080p page is updated and verified paused with sound ready at http://127.0.0.1:9870/ . No revised demo is approved or installed. See `Docs/REALDEMOS_B09_R2_REVIEW_20261115.md`. The one-time10p.m. fallback was deleted after firing.
