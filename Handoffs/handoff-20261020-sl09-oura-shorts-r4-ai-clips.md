# Oura Ring Review SFL R4: three approved AI clips into shorts 4 and 5 (SL-09)

**CONTENT: Shorts extracted from the long-form "My Honest Oura Ring Review After 1.5 Years" (Zeeshan Video 4). SFL.**
Task name: **`Oura Ring Review SFL R4`**. Model: **Opus 5.5, high**. Written 2026-10-20 by `Oura Ring Review SFL R3` (handed off at
83% context; Dan replied two days after delivery and the remaining work is AI frames, motion and two rebuilds).

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (AI clip sections: frames, motion gate, the three sense
questions, Flow subscription first), `.claude/skills/_shared/veo/README.md`, `.claude/skills/_shared/framecheck/README.md`, and the batch
README `.claude/skills/shorts/reference/softblue-sl09/README.md` (both "What round ... taught" sections: the gate's framing rows, editor
zooms, phone screens, caption checks). Dan's words: `/Volumes/Extreme/_edit_work/sl09/round2/dan_r3_reply.json`.

## Dan's decision (verbatim, 2026-10-20)
*"Short one looks good. This is finalized. Looks good. That's finalized. Short 3 looks good. This is finalized. Some feedback: I love the
driving clips you put in there, the fast driving clips, and the test of self-driving. It really got the point across and also held the
viewer's attention. Short 4 looks good. 5 looks good as well. Opener for short 4 looks good. Smart ring close-up and ring and band in one
hand look good. Actually, no: an issue with the band. The band should be the Whoop. This is just like a bracelet, so make the band the
Whoop for the end frame of that."*
- **Finalized, do not touch:** short 1 Train Harder (A), short 2 Sleep Score (I, his second "That's finalized"), short 3 Adrenaline (H).
  Their R3 files, stamps and reviews in `Short-form video content/` are final. Their `Videos to Review/` copies are already removed.
- **Approved, make motion:** K1 (short 4 opener, thumbs-up then nods off into his coffee) and J1 (short 5 opener, smart-ring close-up).
- **Approved with one fix:** J2 (short 5, 0:13.8-0:20.6, one hand with a ring and a band). The band must read as a **WHOOP** in the END
  frame, not a bracelet. The START must match it.

## Work, in order
1. **Back up the reviewed R3 deliveries of shorts 4 and 5** (mp4 + `.audio_gate.json` + `.deliver_gate.json` + `build/K|J/ROUND-2-REVIEW.md`)
   to `/Volumes/Extreme/_edit_work/sl09/round2/r3_delivered/` before any rebuild (never overwrite a reviewed round without a copy).
   Use `cp` or `cat >`; `mv` across volumes failed on file flags in R3.
2. **J2 frames (Codex, ChatGPT subscription, `_shared/codex-image.sh`):** files in `/Volumes/Extreme/_edit_work/sl09/round2/aiframes/`
   (`J2_start.png`, `J2_end.png`, `J2.spec.json`, prompts `J2_start.txt`, `J2_end.txt`; old pair passed gate and reviewer). Replace the
   plain fabric band with a WHOOP-style strap: the slim rectangular sensor pod on a knit band, no screen, so it reads as a WHOOP at a
   glance. Keep the hand, the matte black ring on the index finger, the desk, light and camera. **The END frame must show the pod
   clearly** (that is Dan's note). Keep physics consistent: the pod sits on the same side of the wrist in both frames. If the hand still
   turns palm-up, put the pod on the inner wrist so START shows the plain strap and END reveals the pod; or keep the pod on top and turn
   the hand only part way so it stays visible. Then `gate.py J2_start.png J2_end.png --spec J2.spec.json` (resize END to 1080x1920 first
   if Codex returns another size), a fresh `frame-reviewer`, and `--verify` exit 0. Dan's approval stands once the band reads as a WHOOP;
   show the new pair on the page beside its moving clip.
3. **Motion for K1, J1, J2 on the Google Flow subscription ($0):** queue with `_shared/veo/veo.py add`, spawn the `flow-veo` agent with
   `run_in_background`. Paid Replicate only if Dan says rush. Per take: `clipcheck.py TAKE --spec ...`, a fresh `frame-reviewer` on the
   take, `--verify`, and the three sense questions (cause and effect; a stranger with the sound off says what it shows; it shows the
   line). Expect a retake or two; fix a failing take before Dan sees it. Watch J2 for finger or ring swaps during the turn.
4. **Build:** in `plans.py`, short 4 (K) cover `yawn` (o0.0-o4.30) becomes the K1 clip; short 5 (J) cover `app` (o0.0-o3.70) becomes J1
   and a new cover over o13.81-o20.59 becomes J2 (it is Dan on camera there now). Each AI cover carries `ai=[x, y, 1.6]` placed off faces
   (`chipplace.py`). Fill the frame (subject in the centre third). Then `./chain_r3.sh K J` (render, true peak, clear stale watch images,
   deliver copy + watch). Set `ai_generated: true` for shorts 4 and 5 in `oura-SHORTS.md`.
5. **Gates and review:** a fresh `ra-reviewer` per short with `r3/brief.py` (copy in the skill reference; update its CHANGED entries for K
   and J), then `watch.py --judge`, `deliver.py plan S`, `./rungate.sh S` until review SHIP and gate PASS. Run the gate early in parallel
   with the review; R3 found most gate failures that way.
6. **Page (later round: only what changed):** stills and context clips for the new clips (`export_stills.py K J`), the new J2 pair, a
   short "What changed" list with exact timestamps and watch ranges in the new files (VIDEO-RULES 2026-10-10), `decided.py`,
   `page_r1.py`, `review_server.py 8989 /Volumes/Extreme/_edit_work/sl09/round2/review`, `curl -r 0-99` gives 206, muted seek in the
   browser. Copy short 5 (45 s or more) to `Videos to Review/` as `Oura Ring Review SFL R4 - short 5 - Oura Ring Or WHOOP Which One To
   Buy.mp4` and replace the R3 copy there; short 4 is under 45 s (page only).
7. **Close-out:** queue (`queue.py set SL-09 delivered`, Edit Queue artifact `ArtifactData set` pinned with `if_version`, `mark-synced`),
   board entry, skill reference copies, push from a clean worktree (`git checkout -B <branch> origin/main`, commit only this job's files,
   `git push origin HEAD:main`: the main folder's safe-push has been blocked by other sessions' live files). Message Dan by video title.
8. **After Dan finalizes shorts 4 and 5:** register the batch's new clips in the clip library (`clip_library.py add ... --status
   used-final --used-in "SL-09"`, then `sheet`), remove the `Videos to Review/` copies, stop the page service
   (`review_server.py 8989 --remove`), set SL-09 finalized, and write the one setup handoff for all five shorts (covers by Codex,
   uploads, Blotato per `Docs/SHORTS_RELEASE_CALENDAR.md`; short 3 also has `ai_generated: true` for Zeeshan's cropped AI Tesla clip).

## State
- All five R3 files passed a fresh independent review and the delivery gate (2.6.1) on 2026-10-18. Work folder
  `/Volumes/Extreme/_edit_work/sl09/round2/`; delivered files `Short-form video content/oura-short{1..5}_*.mp4`; page
  http://127.0.0.1:8989/ (managed service, still running).
- Approved frames on disk: `aiframes/K1_start.png`, `K1_end.png` (kitchen locked with `lockstill.py`), `aiframes/J1_start.png`,
  `J1_end.png`; both pairs `gate.py --verify` exit 0. Page copies in `review/ai/`.
- SL-09 on the queue: `delivered` (2026-10-18). Spend so far: $0.
- Machine: the two-build cap was often full in R3 (other sessions' gate runs); chain renders behind `waitslot.py`, never a third build.

## Starter prompt
> Read `Handoffs/handoff-20261020-sl09-oura-shorts-r4-ai-clips.md` and finish it: fix the J2 frames so the band is a WHOOP, make the
> three approved AI clips (K1, J1, J2) on my Google subscription, put them into shorts 4 and 5 of my Oura Ring Review shorts, re-render,
> review and gate until both ship, update the review page and send me what changed with timestamps. Name this task "Oura Ring Review SFL R4".
