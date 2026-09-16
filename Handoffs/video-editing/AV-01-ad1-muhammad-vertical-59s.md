# AV-01 — Ad 1 (Muhammad) "This Picture Got Me Abs": 9:16 ≤0:59 cutdown

**List 3 · ad variant · READY · replaces master-queue job J2 (2026-09-13).** Read `00-RULES.md` first.

## What exists
| variant | state |
|---|---|
| 16:9 (Muhammad) | `Muhammad Ad Videos/this picture got me abs - ad 1/this picture got me abs \| muhammad \| 16x9 \| ad 1.mp4`, live |
| 9:16 full | ✅ approved 09-10, YouTube `Iz0u8KHRbyE`; build dir `/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/` |
| 1:1 full + 1:1 59s | ✅ approved 09-14, live (`VFCQAgzNIkA`, `C8tjH0-hPFg`); build dir `/Volumes/Extreme/_edit_work/ad1-sq/` |
| **9:16 59s** | ❌ **this job** |

The old `ad1-8-14/vert9x16/ad1_vertical_59s.mp4` (Aug 25) predates the approved attempt-3 vertical, the real-picture label
and the current gates. **Don't deliver it.**

## Build
* Copy the approved vertical build to `/Volumes/Extreme/_edit_work/AV-01/`. The approved vertical has **6,977 frames, one
  more than Muhammad's 6,976**, so map every cut accordingly.
* **Selection:** reuse the square's proven ≤0:59 selection (`ad1-sq/cutdown.py`: 1,493 frames, 49.82 s, three audits).
  It sits on Muhammad's 6,976 grid, so account for the one-frame offset at every seam. Read `/shortad-from-longform` [S1]
  22–24 and `reference/a11_sq_ad1/` first. That cutdown shipped only after six seam defects were fixed. Prove every
  seam's picture against the master (memory `cutdown-seams-single-source`).
* **Labels:** every real after picture of Dan in range gets the real-picture chip, off face and abs. The approved vertical
  has no chip, so those beats are re-rendered, not just cut. Reuse the square's placements where the frames match.
* **Same person:** if the app demo is in range, its before and after must be the same man.
* **Audio:** the approved vertical's AAC stream, cut at the seams only.
* Check the closing CTA pill for the trailing-caption overprint (memory `caption-trailing-entry-overprint`).

## Deliver
`this picture got me abs | claude | 9x16 59s | ad 1.mp4` + REVIEW 540p + stamps into the Ad 1 folder. Send Dan the review copy.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AV-01-ad1-muhammad-vertical-59s.md`: build Ad 1's (Muhammad) 9:16 ≤0:59 cutdown from the approved attempt-3 vertical with /shortad-from-longform, reusing the square's proven selection (mind the 6,977 vs 6,976 frame offset), real-picture labels off my face and abs, the vertical's audio cut at the seams only. Every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (including the Codex column and the environment table it points to), then execute `Handoffs/video-editing/AV-01-ad1-muhammad-vertical-59s.md`, following `.claude/skills/shortad-from-longform/SKILL.md` as the method. Deliver, send Dan the review copy, update `00-MASTER.md`.
