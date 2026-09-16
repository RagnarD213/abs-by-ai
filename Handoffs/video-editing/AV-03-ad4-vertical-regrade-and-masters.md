# AV-03 — Ad 4 "Stop Wasting Money On Supplements": re-grade the vertical, deliver full + 59s masters

**List 3 · ad variant · READY · replaces J1.** Read `00-RULES.md` first. Unblocks AS-02 (Ad 4 square).

## What exists
* 16:9 (Muhammad): filed, live.
* Vertical build `/Volumes/Extreme/_edit_work/ad4-vert/`: `ad4_vertical_9x16.mp4` (09-11) + `cut/ad4_vertical_9x16_59s.mp4`
  (57.19 s). Only REVIEW copies are in `Muhammad Ad Videos/stop wasting money on supplements - ad 4/`. **Masters held.**
* **The grade has the BT.601 fault:** it was fitted through ffmpeg's default decode. Dan rejected Ad 3's vertical for exactly this.
* Muhammad's export peaks at **−0.90 dBTP**, against the −1.0 rule, so the verbatim audio stamp can't pass. **Dan accepted that
  audio on 09-11** (*"I think the audio sounded fine"*).

## Build
1. **Re-grade first.** In a copy (`_edit_work/AV-03/`), re-fit the grade with the Ad 3 render-10 tools (`ad3-vert/`: `zlut.py` +
   `lift3.py` with the BT.709 input matrix, then `zgrade2.py --post`, then `zgrade3.py` section by section). Re-render full + 59s.
   Verify against Muhammad's file decoded as BT.709.
2. **Audio exception.** Record Dan's 09-11 acceptance as an explicit, auditable per-file exception (his words + date), using
   whatever declared mechanism the audio gate and `gate.py` provide (`not_applicable` / waiver). Ad 3 has a precedent file:
   `… | 1x1 59s | ad 3.mp4.AUDIO_EXCEPTION.md`. **Never raise the bound.** If a mechanism has to be added, the corpus must pass first.
3. Re-copy the stale `caption_sync_check.py` and `captions.py` from the skill's `reference/` into the build dir, and re-run the caption gate.
   Check the CTA-pill overprint on both files. If it's present, fix it with a caption rebuild + mux.
4. Gate both at the current `GATE_VERSION`, run the independent audit, and deliver.

## Deliver
`stop wasting money on supplements | claude | 9x16 | ad 4.mp4` + `… | 9x16 59s | ad 4.mp4` + review copies (BT.709-verified) +
stamps. Send Dan the review copies. His approval unblocks AS-02.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AV-03-ad4-vertical-regrade-and-masters.md`: re-fit the Ad 4 vertical's grade with BT.709 decoding using the Ad 3 render-10 tools in a copy of `ad4-vert/`, re-render full + 59s, record my 09-11 acceptance of −0.9 dBTP as an auditable exception (never a bound change), refresh the stale caption tools, gate at the current version, audit, deliver, send me review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/AV-03-ad4-vertical-regrade-and-masters.md` using `.claude/skills/shortad-from-longform/SKILL.md` section [A12] as the method. Deliver, send Dan review copies, update `00-MASTER.md`.
