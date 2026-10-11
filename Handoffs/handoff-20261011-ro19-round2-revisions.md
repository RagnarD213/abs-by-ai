LFC (long-form content). Task name for this session: `My First Spray Tan LFC R2`.


## ROUND 2 DELIVERED 2026-10-11 (Claude, Opus 5.5): waiting for Dan's reply

Page: http://127.0.0.1:8865/ (`/Volumes/Extreme/_edit_work/ro19/round2/`). VLC copy: `Videos to Review/My First Spray Tan LFC R2 - first minute.mp4`. Hashes: `round2/round2-hashes.sha256`. Round 1's 235 files re-hashed unchanged before work started.

Built, as listed below: the first minute again (wide open, look F, voice W4); seven voice options plus the untreated one in `audio/opts2/` (W1 to W4 warm with less room echo, B1 to B3 = W4 with +1.5, +3, +4.5 dB of bass) on film 25.99 to 56.99 s, which starts on speech; two new same-pose pairs from the 1 April pale shoot (P04 arms down with photo 247, P05 side pose with photo 107), P02 and P03 each given a new photo so nothing repeats; doctor frames `aiframes/D1-*.png` (plan item A5 replaces Cc16) and four gag frame pairs G1 to G4; motion for A4, A3, A2, A1, one take each, in `round2/motion/`; headroom proofs in look F.

Dan's five questions on the page: voice (recommended B2), the two pairs, the doctor frames, which gag clips get motion (recommended G1 and G3), headroom (recommended yes after two flaws are fixed).

When he replies: record it in `round3-plan/decisions.json` with the hashes; then round 3 = doctor motion and the chosen gag clips (place them in the plan: G1 at 349.2, G2 at 429.6, G3 at 819.1, G4 at 328.2), his voice into `build.VOICE4`, the app tour close, the headroom fix if approved, then the full film with every gate, the watch pass and one independent review.

State to know: `look_option.txt` is F. `build._PIN` holds every shot at the round 1 size and crop; only `intro.0r0` is W. `plan_resolved.json` was patched by hand (round 1 copy: `round2-plan/plan_resolved.round1.json`): A1 to A4 point at the motion files and trims, A3 starts at 373.52 and plays `A3-cut.mp4`, Cb02 (library B0437, banned) is removed. Re-running `resolve.py` would undo these: patch again or move them into the part files first.

Gate status: the first minute's audio gate is 10 of 12 on voice W4 (fails tone and the damage row at 0.083 against 0.080); that voice is not Dan's pick. No delivery gate, watch pass or independent review has run: there is no film.

Cost ledger: motion $3.00 of $5.00 (`round2/motion/ledger.json`). Doctor at 6 s takes it to $3.60; two 6 s gag clips to $4.80. Ten frame images on the Codex subscription. Six Gemini listening calls, a few cents.

Starter prompt for round 3 (Opus 5.5, high), once Dan has replied:

```
My First Spray Tan LFC R3. Read Handoffs/handoff-20261011-ro19-round2-revisions.md (the ROUND 2 DELIVERED section first) and my reply to the round 2 page below. Record my decisions, then build round 3 of RO-19: my voice pick, the doctor clip and the gag clips I chose as finished motion, the app tour close, the headroom fix if I approved it, then the full film with every gate, the watch pass and an independent review. Use the Codex subscription for any images. Do not upload or queue.

[paste the reply box from http://127.0.0.1:8865/]
```

# RO-19 "My First Spray Tan": round 2, Dan's round 1 notes

**Written 2026-10-11 by Claude (Opus 5.5), after Dan reviewed round 1.** Job doc: `Handoffs/video-editing/RO-19-my-first-spray-tan.md`. Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (read the two sections dated 2026-10-11 at the top: more AI clip ideas, audio clips start on speech), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Recipe and traps: `.claude/skills/longform-edit/reference/ro19/README.md`.

## Where it stands

- Cut locked at 18:41 from roll C1512 (8/3 kitchen doorway). No full film exists. Work dir: `/Volumes/Extreme/_edit_work/ro19/`. Round 1 page: http://127.0.0.1:8863/ (folder `round1/`, do not overwrite it; build in `round2/` on a new port).
- Dan's decisions, with his exact words and hashes: `/Volumes/Extreme/_edit_work/ro19/round2-plan/decisions.json`. Re-hash `round1/round1-hashes.sha256` first and record expected against actual.

## What Dan decided on round 1

| item | his call | do |
|---|---|---|
| Opening shot | "start the video on the wide shot" (he saw his hair cut off in the punch-in) | The first shot (0:00 to 0:03) is the camera's wide frame, not the 1.3x punch-in (`build.OVERRIDE` for `intro.0r0`). |
| Opening before and after (P01) | "I like that before-and-after comparison. That gets it across well at 10 seconds." | Keep exactly. |
| Colour | "go F in between. F for the closer size as well. F throughout the video." | `look_option.txt` = `F`. Everything graded is re-rendered. |
| Voice | Not chosen. He wants "four warm, less room-echo options" and "a few options for slightly more bass in my voice to make it sound more authoritative". | Build them (below). |
| P04, P05 (photo section pairs) | Rejected. "two separate shots where I'm doing the same pose, pale and tanned... We already did that front double bicep... tanned, looking the most tan and the best, and pale ones where I'm looking the most pale and the worst. Apple-to-apple comparison." | Two new pairs (below). |
| Cc16 (stock doctor at a desk, 10:42) | Rejected as weak. "a man that looks like the prospect talking to his doctor: a male doctor and a male prospect... something that we can use over and over again". | New AI clip, frames first (below). |
| AI frames A4, A3, A2, A1 | Approved (my reading of "the rest of these are looking good" plus his praise of all four). | Generate motion. |
| Everything else | "the rest of these are looking good" | Keep. |
| The close (app tour or lower thirds) | Not answered. | Default: build the approved app tour; say so at delivery so he can overrule. |

## The voice bake-off in round 1 was void (my error)

The audition window was a typed roll time (166 to 197 s) that sits between two takes: 27 s of silence, 4 s of speech. Nine blind trials ranked room tone and the first minute was built on "voice 1" from them. Nothing was learned about this roll's voice. `recipe/audio_options20.py` now refuses a window with no speech in its first 0.5 s or a pause over 1.5 s.

Build the new options on a window that starts on speech, taken from a kept piece (for example roll 195.1 s, "If you guys want to look good in photos", 31 s; check it with the guard and listen to it):
- Four "warm, less room echo" versions: the warm fixed tone shape with the chain's light dereverb at four strengths or shapes (start from RO-07's voice 4: alpha 0.30, floor -10 dB; vary the dereverb amount and the 450 Hz cut). No expander unless one of the four is that test.
- Two or three "slightly more bass" versions on the best-measuring warm one: a low shelf or a wide bell around 100 to 160 Hz, +1.5, +3 and +4.5 dB; watch for boom and for the lav's handling rumble.
- Level match through the shared finisher, name them plainly, and put all of them on the page with one line each. Run the blind listen as a cross-check only; Dan picks by ear. Never process past the reference (memory `audio-never-over-strip`).

## New photo pairs for P04 and P05

Same pose in both halves of each pair, neither a front double biceps. After: the pool shoot photos where he looks most tanned and best (`photos/finalized social media photos/`, numbered `photo-N`; not the frowning folder, no Speedo photos; candidates seen in round 1: 13, 221, 223, 247, 251, 273, 276, 289, 10). Before: the pale earlier shoot where he looks palest and worst. Round 1 only had four pale files (`/Volumes/Extreme/_edit_work/ro19/photos/src/pale_*.png`: arms down, hands at hips, two double biceps). Look for more from that pale shoot first (memory `dan-before-photo-search` explains scanning his Photos library; also `photos/Dan Before Pictures/`). If only the four exist, the two honest matches are arms down (pale_a with 251 or 247) and hands at hips (pale_b with 273 or 13 or 10). P02 at 0:48 currently uses pale_a alone: no photo twice, so move P02 to another pale photo or drop it. Crop both halves of a pair to the same body scale (`recipe/pairs.py`; the crop step is in the reference README). Show both pairs to Dan as stills before the full render.

## The reusable doctor clip (replaces Cc16)

Start and end frames, Codex subscription (`.claude/skills/_shared/codex-image.sh`), 16:9, for Dan's approval before motion. A man who looks like the prospect (about 40 to 50, ordinary build, clothed, shown whole or from the chest up) sits talking with a male doctor in a normal exam room or office. No stomach framing, no hands on the body, no text, no brand. Make it generic enough to reuse on any "talk to your doctor" line; when Dan approves the motion, register it in the clip library (`clip_library.py add`) with that description. Here it plays under the skin cancer line at about 10:42 (the slot is 5.6 s).

## More AI clip ideas (new standing rule)

Dan wants more ideas per video, mostly funny, and expects to reject about a third. For this film the approved four plus the doctor clip cost about $3.80 of the $5.00 motion cap, so there is room for one more 6 s clip at most. Still bring two or three more funny frame pairs for lines that have no good picture (ideas the plan writers left: the man in a bathrobe staring at a clock outside his taped-off shower at "wait eight hours"; one wipe of a washcloth leaving a pale stripe at 7:15; the mitt-shaped pale patch in the middle of a man's back at 13:44), tell him the cap, and let him choose which get motion.

## Hair (his question on round 1)

The camera framed his hair on the top row of the picture for the whole roll: there is no room above it to crop (measured on all 134 shots; raw frames in `round1/raw_top_check.jpg`). A proof that ADDS headroom exists and has not been shown to or approved by Dan: `recipe/headroom.py` moves the picture down 56 rows, continues the wall, trim and door frame straight up, and rounds off his hair with a cap drawn from his own hair pixels. Proofs: `headroom/intro_T.mp4`, `intro_W.mp4`, `photos_T.mp4` (left camera, right with headroom), copies in `Videos to Review/`. It looks right on three of four test frames; the wide-shot cap is slightly flat on some frames and needs work before it could run on the whole film. Put the before and after on the round 2 page as one question: apply it film-wide, or leave the camera's framing.

## Round 2 deliverable (one page, then stop)

1. The first minute re-rendered: wide open, look F, his chosen voice left open (render it with the best-measuring warm option and say which).
2. Voice options (above), on a clip that starts on speech.
3. The two new pairs as stills.
4. Doctor clip frames, plus the extra funny frame pairs.
5. The four approved AI clips as finished motion, each in context (generate with `recipe/gen_motion.py`, Veo 3.1 Fast, $0.10 a second: A4 one 6 s take, A3, A2, A1 one 8 s take each; judge at playback speed, then frame by frame; keep the ledger).
6. The headroom question.
7. "What I decided" and one reply box. Later rounds show only what changed. Copy any review clip of 45 s or more to `Videos to Review/` and list timestamps of each change.
The full film is rendered in round 3, after his voice pick, the pairs and the doctor frames are locked.

## Cuts already applied (do not apply twice)

All in `recipe/edl.py`, each piece with its reason; five wordless slivers dropped and pauses of 0.70 s or more tightened once in `recipe/shots.py`. Full list in the reference README and in git history of this handoff's round 1 version.

## Gate status, stated honestly

- No delivery gate, watch pass, edit sheet or independent review has run: there is no film.
- The round 1 first minute's audio gate (10 of 12, failing the room and tone rows) describes a voice Dan did not pick; it carries nothing forward.
- Expect the hair rows of the delivery gate to fail on the full film unless the headroom fix is approved and applied.

## Cost ledger

- AI motion: $0.00 of $5.00. Planned: about $3.00 (four clips) plus about $0.60 to $0.80 (doctor).
- Images: 8 frame images on the Codex subscription.
- Gemini: 9 listening trials (void) and 1 first-minute review, a few cents.

## Open risks

- Two poolside posing clips of Dan (Cd07's second shot and Cd20) may be the same take: check the rolls and swap one before the full render.
- Changing a clip's edges re-solves framing for the whole film: pin the solve before the full render (`build._PIN`).
- The machine was shared with the RO-20 build in round 1 and renders ran one at a time at low priority, over the two-build cap. Check `ps` first and wait if two builds are running.

## Model and effort

Opus 5.5, high.

## Starter prompt

```
My First Spray Tan LFC R2. Read Handoffs/handoff-20261011-ro19-round2-revisions.md and build round 2 of RO-19 exactly as it lists: open on the wide shot, look F throughout, new voice options on a clip that starts on speech (four warm with less room echo, plus a few with slightly more bass), two new same-pose pale and tanned photo pairs, start and end frames for a reusable "man talking to his male doctor" AI clip plus two or three more funny AI clip ideas, motion for the four approved AI clips, and the headroom before and after as one question. One review page, then stop for my reply. Use the Codex subscription to generate the images. Do not render the full film, upload or queue.
```
