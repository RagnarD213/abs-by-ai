# Handoff: use the Google AI Ultra credits on AI clips for the next video edits (2026-11-07)

**Owner:** Claude, Opus 5.5 high (clip ideas, frames and checks). Flow is driven by background `flow-veo` agents (Sonnet).
**Authorization:** Dan, 2026-11-07: "Give me separate handoffs for #1 and #4." Item #1 was: "Get ahead on AI clips for the videos due to be edited next." Do every step without asking. Stop only for Dan's frame-pair approvals (a standing rule) and for anything that would cost money.
**Deadline:** the plan drops from the $199.99 Ultra (20x Pro) to the $99.99 Ultra (5x) on **Nov 29, 2026** (Google One screen, 2026-11-07). Spend this work's share of the credits by **Nov 28**.
**Credit budget:** the balance was 22,266 on 2026-11-07. This handoff gets up to **14,000**. The clip-library handoff (`handoff-20261107-flow-credits-clip-library.md`) gets up to 7,000, and about 1,200 stays in reserve. Read the balance before and after every batch, and log it in `Media/flow-credit-log.md` (shared with the other handoff). Veo 3.1 Fast 8 s costs 10 credits, so 14,000 is about 1,400 takes. Never pay, top up or buy credits. If Flow asks for money, stop and report.

## What to make

AI clips for the videos due to be edited next, so their edits start with the clips already made.
- **Order:** follow the release calendar. Start with the films and Shorts due in phase 2 (Nov 26 to Dec 25, kitchen content first) that are not edited yet. Then do phase 3 (January blitz: fat loss, beginner, gym, workout).
- **Sources:** `Handoffs/video-editing/00-MASTER.md` and `jobs.json`, `Docs/LONGFORM_RELEASE_CALENDAR.md` and `Docs/SHORTS_RELEASE_CALENDAR.md`.
- **Which jobs:** pick only jobs whose status is READY or not yet started. Never touch a job another session or Codex has IN PROGRESS. Any job with a live edit owns its own clips.
- **What a clip is for:** each clip is tied to a scripted line in that video's script or transcript, per `/ai-clip-ideas`. Ideas are more numerous and funnier, and an abstract line gets an unreal gag. Search `clip_library.py find` first, and never generate a clip the library already has.

## Standing rules that apply (read before starting)

Read these first:
- `.claude/skills/_shared/VIDEO-RULES.md`: the top section (Flow first, START and END together), plus AI clips, AI labels and the blind test.
- `.claude/skills/_shared/IMAGE-GENERATION.md`, "Blind Google test", and `_shared/blind-image/blind.py`.
- `.claude/skills/_shared/veo/README.md` and `FLOW-RUNBOOK.md`.

Rules:
- **Frames come before any video.** Every clip idea reaches Dan first as a complete START and END pair. For the blind test there are two complete pairs:
  - one Codex pair, made with `codex-image.sh` on the subscription;
  - one Google pair, made with Nano Banana Pro in Flow, free (`FLOW-IMAGE-RUNBOOK.md`), with each END made from its own START.
  - Show the pairs unlabeled, and never say which model made which.
- **Lessons from the 2026-11-07 exercise test:** Google keeps the camera still only if the prompt says outright "keep the framing identical: do not zoom, crop, pan or re-center; no new objects". It redraws limb proportions on big pose changes. Keep pose changes between START and END small, which suits short gag clips.
- **Every pair is checked** with `framecheck/gate.py` and a fresh `frame-reviewer` before Dan sees it.
- **Clip quality:**
  - Each clip has to make sense: cause and effect, and it shows the line.
  - The look is calm and real: a closed-mouth smile, no camera shake.
  - Regenerate a sloppy take instead of patching it.
  - AI clips carry the AI label, placed on the picture.
  - Check every AI Dan face against the identity reference.
- **Batch Dan's approvals.** Put up one review page per batch of 20 to 40 clip ideas, phone layout first. Each idea shows the script line, the two unlabeled pairs, and buttons to pick X1 or X2 or reject. Log his picks with `blind.py pick`. Aim for two batches a week, so Dan approves in a few sittings and not one video at a time.
- **After approval:** generate the videos in Flow with background `flow-veo` agents. Use `veo.py add` for the approved pairs: Veo 3.1 Fast, or Omni when the motion suits it. Run up to 3 agents at once, each in its own Chrome tab, and none may close tabs it didn't open. Check the motion with `clipcheck.py` and a motion reviewer.
- **Filing:** file each finished clip to the video's job folder and register it with `clip_library.py add --kind ai --status usable-unused --used-in "<job> (planned)"`. Then note the clip IDs in that job's handoff doc under "Pre-made AI clips", so its editor uses them.
- **Edit cap:** this is setup work, so it doesn't count against the 5-edit cap. Run renders and checks through the render queue (`renderq.py`).

## Deliver

- **Each batch:** the review page link in chat, the credits used so far, and the two wrap-up boxes. Stop there for Dan's picks.
- **By Nov 28:** a short summary doc `Docs/FLOW_CREDITS_CLIPS_RECEIPT_20261128.md` with:
  - the clips made per job;
  - their library IDs;
  - credits used;
  - anything left half done, with the exact next step.
- **Board:** keep one board entry under 80 words for this work while it is running.
