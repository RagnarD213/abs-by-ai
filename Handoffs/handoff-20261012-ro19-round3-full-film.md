LFC (long-form content). Task name for this session: `My First Spray Tan LFC R3`.

# RO-19 "My First Spray Tan": round 3, Dan's round 2 notes, then the full film

**Written 2026-10-12 by Claude (Opus 5.5), after Dan reviewed round 2.** Job doc: `Handoffs/video-editing/RO-19-my-first-spray-tan.md`. Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (read in full; the top section, dated 2026-10-12, came from this review), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Recipe and traps: `.claude/skills/longform-edit/reference/ro19/README.md` (the "Round 2" section lists the order of scripts). Earlier round: `Handoffs/handoff-20261011-ro19-round2-revisions.md`.

## Where it stands

- Cut locked at 18:41 from roll C1512 (8/3 kitchen doorway). No full film exists. Work dir: `/Volumes/Extreme/_edit_work/ro19/`. Round 2 page: http://127.0.0.1:8865/ (folder `round2/`, do not overwrite; build in `round3/` on a new port, 8866 if free).
- Dan's decisions, with his exact words and hashes: `round3-plan/decisions.json`. Re-hash `round2/round2-hashes.sha256` (53 files) and `round1/round1-hashes.sha256` first and record expected against actual.
- `look_option.txt` is F. `build._PIN` (`round2-plan/segs.round1.json`) holds every shot at its reviewed size and crop; only `intro.0r0` is W. `plan_resolved.json` was patched by hand in round 2 (A1 to A4 point at motion files and trims, A3 starts at 373.52 and plays `round2/motion/A3-cut.mp4`, item A5 is the doctor placeholder, Cb02 is removed). Re-running `resolve.py` would undo that: patch again, or move the patches into the part files first.

## What Dan decided on round 2

| item | his call | do |
|---|---|---|
| Voice | "let's go with B2 with more bass" | B2 for the whole film: W4 (warm shape with the 450 Hz dip at -5 dB, light dereverb alpha 0.30 / floor -10 dB, no expander) plus `equalizer=f=120:t=q:w=0.8:g=+3.0`. Put it in `build.VOICE4`, write the film voice to a NEW file (`voice/film_voice_r3.wav`). |
| Voice, standing rule | "Let's make a subtle addition of bass to my voice the standard for all Claude and Codex video editing skills." | Already written into VIDEO-RULES and memory `voice-bass-standard`. Nothing more to do here. |
| P02 (single pale photo, 0:48) | Rejected. "I'm just looking more fat and not just pale... use a picture where I'm pale, but I still have defined abs... maybe the one where I'm standing on the driveway and my abs are more defined." | New photo from the 1 April pale shoot, driveway set (grey shorts, 14:49:59 to 14:50:58 in his Photos library). Best candidate seen on the contact sheet: 14:49:59 (asset `99BCDE30`); also 14:50:10 (`9AE93ABE`) and 14:50:13 (`06D979F4`). Look at them full size and pick the one with the most visible abs. Crop with `photocrop.py`, render to a new file (`gfx/r3/P02.mp4`), then the first minute again. |
| P04 (pair 1, arms down) | Approved with a fix. "I like that photo. However, this is actually a tan filter on that photo. The original was significantly more pale. Find the original, or if you can't find the original, just use AI to de-tan me." | The pale half used was a 2417x3348 filtered copy (assets `C60DD02A`, `AE8BE9A4`, both 14:57:50). The full frame taken the same second is asset `99501C7F` (4284x5712): confirm it is the same pose and untinted, export it (`sips`, then `exif_transpose`), crop to the same body scale as the tanned half (navel landmark, `photocrop.py`), render `gfx/r3/P04.mp4`. Only if no untinted original exists: de-tan the filtered picture with Codex (his explicit instruction for this one picture; it overrides the never-redraw rule here only) and say so on the page. |
| P05 (pair 2, side pose) | Not mentioned. | Keep. |
| P03 (three portraits) | "P03 looks good." | Keep. |
| Doctor frames (D1) | Approved (my reading: the dictation "all AI-generated clips start at 9 frames Look good" is "all AI-generated clips, start and end frames, look good"). | Generate motion for plan item A5: one 6 s take, $0.60. Slot is 5.6 s at 10:42. When Dan approves the motion, `clip_library.py add` it as the default "talk to your doctor" clip. |
| Gag frames G1 to G4 | Frames approved by the same sentence. He did not say which get motion and did not say "go over". | Inside the $5 cap: G1 (eight hour wait) and G3 (the spot he could not reach), $0.60 each. G2 and G4 would take the film to $6.00: only with his words (see the open questions; the starter prompt has a line for it). |
| Finished clips A4, A3, A2, A1 | Approved by the same sentence. | Keep as trimmed. |
| First minute | Only the P02 and voice notes. Wide open and look F drew no note. | Re-render with the new P02 and B2. |
| Headroom | Not answered. | Do NOT apply. The film keeps the camera's framing. Ask once more, in one line, when round 3 is delivered. |
| The close | Not answered in two rounds; the default was stated twice. | Build the approved app tour (`longform-edit/reference/ro06/phone_side.py`, library `B0544`). |

## Round 3 work, in order

1. Hashes, then `ps` (two-build cap), then the four changes that do not wait on anything: P02, P04 pale half, voice B2, the app tour close.
2. Motion: A5 (doctor), G1, G3 with `recipe/gen_motion.py` (extend `DUR`, add the IDs to `motion_authorized` handling: it reads `round2-plan/decisions.json` today, point it at round 3's and at `round2/round2-hashes.sha256` for the new frame hashes; prompts beside the others in `round3/motion/`). Judge each at playback speed, then frame by frame. A big change between start and end frames comes back as a fade or dissolve (round 2 trap): trim or cut on a word rather than buy a second take.
3. Place the gag clips in the plan by their words: G1 at 349.2 s ("I needed to wait eight hours before taking the shower", about 3.7 s, lower third Gb15 sits over it), G3 at 819.1 s ("If you don't have a partner and you can't reach your whole body", about 4.3 s, lower third Gd03). G2 would go at 429.6 s and G4 at 328.2 s. Each carries the AI-GENERATED label. Check each against the lower third above it.
4. Before the full render: the two open risks from round 1 (the two poolside posing clips Cd07 and Cd20 may be the same take; pin the solve again after any clip edge moves), all B-roll graded against the presenter frames (rule of 2026-10-11), a music bed transcribed for zero words, chapters from the round 1 page.
5. The full film: `build.py range 0 <end>`, the delivery gate (`_shared/deliver/gate.py --format longform`), the audio gate with its A/B clip, `CUT-CONTINUITY-QC.md` on the exact file, the watch pass, one independent review (`ra-reviewer`), the edit sheet. Expect the audio gate's tone row to fail on the fixed warm shape (known mismatch) and the delivery gate's hair rows to fail without the headroom fix: report both plainly, do not tune either.
6. One page (later-round layout): the full film, the first minute, the three new clips in context, the two changed photos, a revision list with exact timestamps and watch ranges, "What I decided", one reply box. Copy the film and the first minute to `Videos to Review/` and delete the R1 and R2 copies of this video from that folder. Then stop for Dan. No upload, no queue.

## Open questions for Dan (he can answer in the starter prompt)

1. Gag clips: G1 and G3 are inside the limit. Does he also want G2 (washcloth) and G4 (bored specialist), which takes this video to $6.00 against the $5.00 limit?
2. Headroom above his hair: apply it to the whole film (after the two flaws are fixed), or leave the camera's framing? Unanswered means it stays as shot.

## Cuts already applied (do not apply twice)

All in `recipe/edl.py`, each piece with its reason; five wordless slivers dropped and pauses of 0.70 s or more tightened once in `recipe/shots.py`. Nothing was cut in round 2.

## Gate status, stated honestly

- No delivery gate, watch pass, edit sheet or independent review has run: there is no film.
- Round 2's first minute audio gate was 10 of 12 on voice W4 (tone, and the damage row at 0.083 against 0.080). B2 has not been gated on a first minute yet; on the 31 s audition window it measured room decay 48 ms, flux 0.0794 (limit 0.0795), tone distance 1.63.

## Cost ledger

- AI motion: $3.00 of $5.00 (`round2/motion/ledger.json`). Planned: A5 $0.60, G1 $0.60, G3 $0.60, total $4.80. G2 and G4 would add $1.20.
- Images: 18 frame images on the Codex subscription across both rounds. Gemini: about 16 listening calls, a few cents.

## Model and effort

Opus 5.5, high.

## Starter prompt

```
My First Spray Tan LFC R3. Read Handoffs/handoff-20261012-ro19-round3-full-film.md and build round 3 of RO-19 exactly as it lists: voice B2 on the whole film, a new pale photo at 0:48 from the driveway set where my abs are defined, the untinted original for the pale half of pair 1, motion for the doctor clip and gag clips G1 and G3, the app tour close, then the full film with every gate, the watch pass and an independent review. One review page with a timestamped revision list, then stop for my reply. Use the Codex subscription for any images. Do not upload or queue.
Gag clips G2 and G4 as well (goes over the $5 limit): no
Headroom above my hair on the whole film: no
```
