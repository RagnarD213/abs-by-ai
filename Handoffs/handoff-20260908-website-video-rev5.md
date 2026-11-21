# Handoff: Website conversion video — REVISION 5 (three fixes on rev 4)

**Created:** 2026-09-08 (Dan's rev-4 review, evening) · **Runner:** Fable 5.1, high effort (see the bottom) · **Skill:** `/ad-edit`
(read lessons 107–115 first) · **Budget:** $0 by default; ≤ $2.40 of Veo if a clip has to be regenerated
**Working dir (all intermediates, on the Extreme drive):** `/Volumes/Extreme/_edit_work/website-video-828/`
**Delivered rev 4:** `claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4`
(rev 1–3 beside it as `*_REV1/2/3_REJECTED`; rev 4's recipe is in `recipe/`, notes in `notes.md`, proof sheets in `pv/`)
**Reference for audio and look:** `Muhammad Ad Videos/this picture got me abs | muhammad | 16x9.mp4`

## Dan's rev-4 review, verbatim (2026-09-08)

> Okay, revisions. The framing and the cropping are all looking good. You nailed it with this one. Let's lock that in and
> crop all the videos like this going forward. Okay, the clip at 2:27: this is the right idea, but there's a weird AI
> artifact in here. When he blows on the food, there's smoke coming out of his mouth, which doesn't make any sense.
> Eliminate that blowing on the food and the smoke at the end of this clip at 2:27. For the clip at 2:33, there's another
> weird AI artifact. The meal prep slides without anything moving in it kind of disappears. Eliminate that weird AI
> artifact of meal prep sliding and disappearing at the end of this clip. At 3:36, I want to remove this picture. I want to
> keep the emphasis on the prospect and not on me at this point.

**Verdict:** the framing is APPROVED and LOCKED (already recorded: `/ad-edit` decisions table + lesson 115, memory
`framing-standard-hair-anchored`, cross-references in `/shorts` and `/longform-edit`). **Do not touch the crops, the punch
plan, `punched.mov`, the hair track, the audio chain, the captions style or the other graphics.** Three changes, all
downstream of the punch render, so this is a mix → audio → captions → gates re-render (~25 min), not a punch re-render.

## 0 — What is locked and must not change

- `punched.mov` (rev 4's hair-anchored punch, both passes) and everything that feeds it: `hairtrack.json`, `layout.py`'s
  LEVELS / `crop_for` / `punch_plan`, `tight.mov`, `tight_cuts.json`, the grade, the EDL.
- **Audio chain, verbatim:** `MUSIC_DB=-44 COMP=0 python3 audio3.py` (the work dir's file — the skill's reference copy is a
  shim). The shared gate (`_shared/audio/audio_gate.py`) must PASS again on the exact delivered file and stamp it;
  `deliver.sh` does this.
- The six lower thirds, the BEFORE/TODAY/TRIAL/PRICE/CTA cards, both phone PiPs (`gfx/pip_macro.mov`, `gfx/pip_hub.mov`),
  the AI inserts A, B, C1, C2, D3 as built, the 1.5× AI-GENERATED tag, captions.

## 1 — The clip at 2:27 (D1, grilling): the blow-and-smoke

**Measured** (`pv/rev5_D1_tail.jpg`, `ai/clips/D1.mp4` at 0.2-s steps): the man leans in toward the pans from **4.4 s** of
the source and a puff of "smoke" appears at his mouth **5.0–5.4 s**; the insert uses source 0.3–5.61 s (beat
`AI_D1` = 146.436–151.642, 5.21 s), so the artifact is the insert's last second. The cause is my own prompt
(`ai/prompts/D1_video.txt`: "leans in, breathes in the smell and smiles") — Veo rendered the breath as smoke.

**Default fix (free, deterministic):** shorten the beat so it ends before the lean-in, starting the D-run a word later:
```python
# beats.py
AI_D1 = (at("customize your eating plan"), at("and to avoid the foods"))     # 147.96 -> 151.642 = 3.68 s; was at("Your AI will also customize")
```
and in `build_inserts.py`: `EDIT["ai_d1"]=[(0.3,4.3)]` (the builder trims to the beat + 0.10 s = 3.78 s → source 0.3–4.08,
0.3 s before the lean-in). Dan stays on camera for "Your AI will also" (1.5 s) and the clips fade in on "customize". Look at
the new insert's LAST second (`pv/` strip) — it must end with him stirring, no lean, no puff.
**Fallback ($1.20):** regenerate D1 from `ai/stills/D1b.jpg` with `ai/veo.js` and a video prompt WITHOUT the smelling action
("keeps flipping the chicken and stirring the vegetables, glances down at the pans with an easy pleased expression, one small
reframe mid-shot; no steam or smoke near his face"), keep the original beat, check the strip.

## 2 — The clip at 2:33 (D2, portioning): the containers slide and vanish

**Measured** (`pv/rev5_D2_tail.jpg`): the insert is the two clean shots of `D2.mp4` cut together (`EDIT["ai_d2"]`:
source 1.0–3.85 then 4.7–7.96, around two Veo-baked dissolves — lesson 111). In the wide shot's tail the row of containers
starts to drift from **≈7.0–7.1 s** and is visibly displaced by 7.6–7.95 s. Beat `AI_D2` = 151.642–157.652 (6.01 s).

**Default fix (free):** cut the wide shot before the drift and give the difference to D3, which has spare clip:
```python
# build_inserts.py
EDIT={"ai_d1":[(0.3,4.3)], "ai_d2":[(1.0,3.85),(4.7,7.05)]}     # D2 usable = 2.85 + 2.35 = 5.20 s
INPOINT["ai_d3"]=0.2                                             # D3 usable = 0.2-7.93 = 7.73 s (the beat needs 7.68 -- verified 2026-09-08)
# beats.py
AI_D2 = (at("and to avoid the foods"), at("that you have", after=156.0)-0.25)   # 151.642 -> 156.68 = 5.04 s (needs 5.14 of clip)
AI_D3 = (AI_D2[1], end_of("you have available"))                                # 156.68 -> 164.262 = 7.58 s (needs 7.68 of clip; anchors verified: D1 3.68 s / D2 5.04 s / D3 7.58 s)
```
`build_inserts.py` asserts the usable clip covers the beat — if it fails, the numbers above drifted; recompute from
`python3 -c "import beats as B; print(B.AI_D2, B.AI_D3)"`. **First strip `D2.mp4` 6.0–8.0 s at 0.1 s and `D3.mp4` 7.3–8.0 s**
(D3 now uses its last frames): if the drift starts before 6.9 s, or D3's tail has its own artifact, the free fix does not fit —
**fallback ($1.20 each):** regenerate D2 (`ai/stills/D2.jpg`, prompt unchanged) and keep rev 4's edges; check every new clip's
first AND last second before it goes in (that is where all three artifacts of this video lived — lesson 115).

## 3 — The picture at 3:36 (the SOLVED card: Dan's goal image) — remove it

`SOLVED = (at("But now AI has solved"), end_of("a plan to get you there"))` = 215.119–221.925 (6.81 s), `gfx/solved.mov`.
Dan: "keep the emphasis on the prospect and not on me." **Default: remove the card; Dan on camera for the line, captions on,
nothing added in its place** (he asked for a removal, not a replacement — if he wants a prospect visual there, that is a new
ask; offer it in one line of the delivery message, do not build it).
- `beats.py`: delete the `SOLVED` line (nothing else references it; `_cta` anchors on "that they always wanted").
- `layout.py`: drop `("solved",B.SOLVED)` from `GFX`.
- `captions.py`: drop `B.SOLVED` from `SUPPRESS` (the line gets captions like every other on-camera line).
- `qc.py`: drop `B.SOLVED` from the check-9 `SUP` list; replace check 7's first assertion ("the goal image card exists and
  carries the tag") with `check(not hasattr(B,"SOLVED"),"no goal-image card (removed on rev 5)")` and fix its comment.
- **The punch plan does not change**: the segment 215.12–221.99 is already a VISIBLE NEAR hold (the beat never covered it
  exactly) and `hard_splices.json` has no splice strictly inside the beat (215.115 and 221.988 are its edges). Prove it:
  `python3 layout.py plan > /tmp/plan_before.txt` BEFORE editing, again after, `diff` — identical means no punch re-render.
  If it differs, run `python3 layout.py punch` (≈17 min with the cores free) before the mix.

## 4 — The chain (after the edits)

```
cd /Volumes/Extreme/_edit_work/website-video-828 && export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
python3 layout.py plan | head -4                       # unchanged plan (see §3)
python3 build_inserts.py ai_d1 ai_d2 ai_d3             # ~10 s each with the cores free
# strips of every rebuilt insert's first and last second -> pv/, LOOK (lesson 115)
python3 layout.py mix                                  # ~9 min
MUSIC_DB=-44 COMP=0 python3 audio3.py                  # the approved chain, unchanged
python3 captions.py
./deliver.sh                                           # audio gate + stamp, sheet, qc (hair gate incl.), watch, review copy
```
Run the long steps as a background script with a process waiter (lesson 96 / 112), never a foreground call. `deliver.sh`
re-runs the WHOLE gate set: the hair gate must report the same 43–82 px (nothing upstream changed), the tag check must find
7 inserts, QC 9 must pass with SOLVED gone.

## 5 — Delivery checklist

1. Strips of D1/D2/D3's first and last second checked by eye; the 3:35–3:42 stretch grabbed at 1-s steps (Dan on camera,
   captions present, no card).
2. All gates green: audio gate PASS + stamp, `qc.py` all checks, watch pass 0 frozen / 0 black (jumps only inside inserts).
3. Deliver over the same filename; rev 4 beside it as `website_video_16x9_REV4.mp4` (superseded, not rejected — the framing
   was approved); the 540p review copy, A/B, `notes.md` (rev 5: what changed, $ spend, the two fallbacks if used).
4. `notes.md`, the coordination entry (rewrite the website-video block; delete the HANDOFFS line for this doc), this doc's
   row in `Handoffs/README.md` moved to "Recently retired", the recipe copied to
   `.claude/skills/ad-edit/reference/website-video/`, commit + push. No dashboard row exists (Dan's 09-08 rule).
5. Send the review copy + A/B and say in one line that the framing is untouched from the approved rev 4.

## 6 — Things NOT to do

- Do not re-anchor, re-plan or re-punch anything for the framing. It is approved. `punched.mov` is reused as is.
- Do not slow a clip below 0.85× to fill a beat (lesson 65); shorten the beat or regenerate instead.
- Do not replace the goal image with a different picture of Dan. Do not add anything unasked.
- Never a jump cut inside a single AI shot — a straight cut is only clean between two DIFFERENT shots (D2's close → wide).

## Starter prompt (paste into a fresh session)

> Execute `Handoffs/handoff-20260908-website-video-rev5.md` with `/ad-edit`. Rev 4 of the website conversion video was
> reviewed: the framing is approved and locked, do not touch it. Three fixes, all downstream of the punch render: (1) the
> grilling clip at 2:27 ends on a lean-in with smoke — shorten the D1 beat to start on "customize" and trim the clip before
> 4.4 s; (2) the portioning clip at 2:33 has the containers drifting in its last second — cut the wide shot at 7.05 s and move
> the D2/D3 edge 0.97 s earlier; (3) remove the goal-image card at 3:36 and leave Dan on camera. The handoff has the exact
> beat numbers, the EDIT spans, the fallbacks (regenerate a clip, $1.20) and the chain. Strip the first and last second of
> every rebuilt insert and look before mixing. Deliver over the same filename with rev 4 kept beside it, all gates green.

**Recommended: Fable 5.1, high effort** (Dan's standing choice keeps Abs By AI tasks in Fable; the detector and the gates
already exist, so extra-high is not needed). **Lower-usage branch: Opus 5, high effort** — the work is three deterministic
edits, one chain run and a by-eye pass on the clip tails; the only judgment is whether a trimmed clip still reads well.
