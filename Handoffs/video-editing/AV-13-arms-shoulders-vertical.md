# AV-13: "Arms & Shoulders Home Workout" (Zeeshan, organic): 9:16 full + ≤0:59

**List 3 · ORGANIC variant (not an ad) · READY.** Read `00-RULES.md` first. Added 2026-09-22 at Dan's request
("add this to our editing queue for square, vertical, and short versions"). The 16:9 is Zeeshan's final, being set up on
YouTube + Blotato by `/video-setup` the same day.

## Source and method

- Master: `Zeeshan Content Videos/arms and shoulders home workout - video 2/arms and shoulders home workout | zeeshan | 16x9 | video 2.mp4` (Zeeshan's "Video2 Rev 3", 11:00.1, 1920x1080 @ 29.97). Build only from the filed master; check its md5
  against `BLOTATO_QUEUE_PROGRESS.md` (the DONE section for this video).
- Run `/shortad-from-longform` as the method (Codex: its `SKILL.md`). Decode BT.709 from the start (memory
  `untagged-video-bt601-trap`). **Zeeshan's audio untouched**: stream-copied for the full vertical, cut only for the
  cutdown, gated `audio_gate.py --reference-mix <his> --verbatim`.
- **Fill the 9:16 frame** (VIDEO-RULES "Short-form footage fills the vertical frame"): full-screen portrait crop, a
  little space above his hair. Many shots are full-body workout wides; keep the whole movement (arms overhead, dumbbells)
  in frame and record a containment reason only where a full-screen crop genuinely cannot hold the action.
- Re-lay Zeeshan's graphics for a phone: set titles, rest timers, the AI Generated label on the goal image near 10:48
  (clear of face and abs). Captions and chips go in measured clear space, never over his face or abs.
- **≤0:59 cutdown:** a self-contained workout teaser that gives the viewer a tactic (memory `shorts-reason-to-watch`),
  not the intro. Suggested spine: the best exercise explanation plus a slice of the live round, ending on the channel/URL.
  Cut on silence; no seam through a word or a set timer.
- Every current gate on the delivered files, full-resolution watch pass, independent audit.

## Deliver

Into the source folder: `arms and shoulders home workout | <executor> | 9x16 | video 2.mp4` and
`... | 9x16 59s | video 2.mp4`, review copies, stamps, notes and recipe. Send Dan both review copies.
**Do not upload or queue.** This is organic: once Dan approves, `/video-setup` queues it through Blotato (Private on
YouTube), never `/ad-setup`. Dan's approval unblocks AS-12.

## Starter prompts

**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AV-13-arms-shoulders-vertical.md`: build the full 9:16 vertical and the ≤0:59 cutdown of Zeeshan's finalized Arms & Shoulders Home Workout with /shortad-from-longform, his audio untouched, full-frame portrait crop, labels off my face and abs. Every gate, independent audit, deliver, send me the review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/AV-13-arms-shoulders-vertical.md` using `.claude/skills/shortad-from-longform/SKILL.md` as the method. Deliver, send Dan the review copies, update `00-MASTER.md`.
