# RO-21 "What Every Body Fat Percentage Looks Like (On Me)": round 1 recipe (Claude Opus 5.5, 2026-10-28/29)

A 7:32 green-screen explainer from ONE roll (10/15 C1724, FX30 4K S-Cinetone, lav left only), built on RO-24's 16:9 house-key
port and the locked green-screen background template (`_shared/greenscreen-bg/`). Work dir `/Volumes/Expansion/_edit_work/RO-21/`.
Each body fat level is treated as a "person" for the background planner (its AI picture, a pair "this level / next level" for
the panel, big type for its number). Start here for any green-screen explainer that walks through levels, tiers or steps.

## Order (scripts here; copies of the work dir's recipe)
1. `edl_r1.py`: draft take list -> cut points on medium.en word edges, validated on the lav's quietest 10 ms; pieces whose
   source gap is under 0.7 s are MERGED (no time removed, no cut): only real retakes and long pauses become joins.
   `OVR` holds listened-to join fixes. Writes `edl_r1.json`, `film_words.json`.
2. `plan_r1.py`: every insert and graphic anchored to phrases (film seconds). Post-passes: a full-screen insert within 0.4 s
   of a take join snaps ONTO the join (hides it, no sliver); a card that ends within 0.35 s of a full-screen cut ends ON it.
3. `shots_r1.py` (cuts at joins, insert/card edges, sentence ends every <= ~12 s; W/T alternate), `keyranges_r1.py` (key
   only presenter-visible source frames + 6-frame handles), `key/` (calibrate on two 100-frame excerpts, then
   `key_all.sh`: keyonce stamps, SPLIT/FIRST env to run the first minute in its own queue job).
4. `facts_r1.py` -> planner -> `bg_plan.json`, then film post-passes (soft = blurred B-roll still, panel/bigtype `mov`).
5. `gfx_r1.py` (from_plan lt/l3/fact + the new `hf/ladder/` template), `phone_r1.py`, `broll_r1.py`, `manifest_r1.py`.
6. `voice_r1.py` (in-place word patch, length kept) -> voice_chain (RO-24's Bill Maher + bass lift settings).
7. `fm_r1.sh` (first minute), `colour_r1.sh` (3 grades x 2 moments), `ctx_r1.py` (context clips), `page_r1.py`.

## New template: `hf/ladder/` (NOT yet approved by Dan)
A row of N portrait pictures rising in on their words with a % under each, one AI chip for the row, optional title,
a highlight that moves tile to tile (others dim) and a glass band whose line swaps on words. Used three times: the opening
hook (8 tiles on the hook's words), "pause on the one that looks like you", and the recap (highlight + action step per level).
GSAP lint refuses left/top tweens: move the highlight with `x`.

## Traps met (each cost a re-render)
- **Soft background with an AI picture of the presenter reads as a GHOST of him** (blurred, oversized Dan behind Dan). Use a
  blurred still of the film's own graded B-roll for the section (gym, food, sleep) and no AI chip there.
- **Bottom-left AI chip crowds the lower-third band.** Chip top-left (like the set's own); on a panel, inside the first
  photo's plain backdrop.
- **Slivers:** an insert starting 0.1-0.3 s after a take join, or a card ending 0.05 s before an insert, leaves 2-8 frames of
  presenter with the wrong framing or no background segment (the assembler asserts). The plan post-passes above fix it.
- **Insert media one frame short:** the compositor needs `fr(b) - fr(a)` frames, which can exceed `round((b-a)*fps)`. Pad
  every B-roll insert with 2 cloned frames (`tpad=stop_mode=clone:stop=2`) and check all manifest media before a render.
- **A long-running graphics job keeps the plan it read at start:** it re-rendered a ladder from the OLD plan after the plan
  changed. Ladders now carry an `.ok` stamp of their config; render only changed configs, one graphics job at a time.
- **`while read ... done` around `run_key.sh`:** ffmpeg inside ate the loop's stdin and the key stopped after one range. Read
  the list on fd 3 and give the command `< /dev/null`.
- **hfbg `--snap` does not render:** panel/bigtype segments need `--render` and `mov` in the plan before any assemble.
- **Word patches:** a single replaced word from another delivery ("calorie" into a fast recap list) was heard 5/5 by a blind
  listener; even a whole-phrase swap 4/5. Test patches blind against untouched control clips (3 runs, shuffled names), and
  keep the original when only a patch fails. "shop" -> "show" passed 2 of 3 (kept).
- **Gemini video review of the first minute:** most "jump cuts" it lists are framing cuts or not edits at all, and it
  invented hair cuts and see-through patches; check every claim on full-resolution frames. It did catch the ghost.
- The 10/15 green screen key with RO-24's settings (RIM 4, plate over 3000-10000) measured mc flicker 0.52, hair 0.49-0.58,
  rim 4-4.6 %, 1 speck in 200 frames: `key/CALIBRATION.md`. 9,900 frames took about 7 h of two heavy slots on a busy Mac.

## Round 2 (2026-10-29): Dan's four changes, on round 1's files (scripts `*_r2.py` here)
Work in `round2/`; round 1 stays untouched. `plan_files_r2.py` writes `round2/film_manifest.json` + `round2/bg_plan.json` (round 1's
with the changed items repointed); `assemble_r1.py` takes them via `--plan/--manifest`. `ctx_r2.py` renders the first minute and
the context windows in `--grade rich`; `page_r2.py` is the small change-only page (first minute in its own inline player on top).
- **Lock hashes for keys are of the `K*.done` stamp, not the `.mkv`** (decisions.json). Hashing the mkv shows 22 false mismatches.
- **B01 AI clip insert** (`broll_r2.py`): inserts are opaque in the manifest, so the AI-GENERATED chip is burned into the insert
  itself (`gsbg.SB.disclosure` PNG overlaid in RGB). A 24 fps library clip still gets `fps=30000/1001` + 2 padded frames.
- **A still on the studio set's TV** (`g10clip_r2.py`): the `set` type plays only a clip or a portrait PAIR; turn a 16:9 still
  into an 11 s sub-pixel push-in mp4 and give the segment `clip: {src, windows}`. The set draws its own chip. Lift the still a
  little: the TV multiplies by 0.86. ClipSource's "Broken pipe" in the log at a segment end is harmless.
- **from_plan fit check:** a fact headline fits 766 px at 84 px (about 14-15 characters). "Upper Four Abs Show" (907 px) did not.
- **Sleeping AI frames (B10):** Codex made him bodybuilder-bulky from L08 alone: refine against `id_white57` + `id_gray2` ("slimmer
  arms, smaller shoulders") and ask for cool moonlight on his skin. A face-only edit pass removed a lopsided smirk.
- **Codex END frames swing the head** (asked for "a few degrees", gave ~38 degrees side to side; reviewer FAIL: the face would
  morph). Fix that passed gate + fresh reviewer: END = START above the collarbones, blended (rows 470-540) into Codex's breathing
  chest (after `lockstill.py` on the room). Only the breath moves; nothing for the video model to morph.
