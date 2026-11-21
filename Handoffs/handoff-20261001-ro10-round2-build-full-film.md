# Handoff: RO-10 round 2, build the full film (everything is approved) (2026-10-01)

**Goal.** Build, gate, review and deliver the full RO-10 film, "Calories: The Reason You're Not Losing Weight" (9/23 roll
C1704, about 8:38). It is the first film whose lower thirds, fact cards, 3A side lists and cycle diagram all come from the
approved HyperFrames templates. Nothing is pending: Dan approved round 1 and every new asset. No new creative decisions.

**Dan's words (2026-09-30 / 10-01).** *"This video is looking excellent... All the graphics look great. The motion looks
great. The text that you chose for the graphics was excellent too."* *"Color correction and audio are looking good."*
*"Let's use both for the opener, the food clips first, before the scale. All the start and end frames are good... that clip
that you generated is good. Everything is approved."* Full record with hashes: `/Volumes/Extreme/_edit_work/ro10/round2-plan/decisions.json`.

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/hyperframes/README.md` ("One graphics pass
for any video"), `.claude/skills/longform-edit/reference/ro10/README.md` (script order and traps), then RO-12's
`finish.py` / RO-16's `recipe/finish.py` + `finish_chain.sh` for SRT, chapters, gate plan and delivery.

**Locked (do not change).**
- Cut, takes, shots: `/Volumes/Extreme/_edit_work/ro10/edl.json`, `shots.json` (46 shots), words `words_out.json`.
- Look and audio: colour C, W2/T2, framing solved by `recipe/build.py all_segments()`; audio = the fit in
  `FIT.mp4.voice_chain.json` + 0.9 dB at 150 Hz. Round 1's first minute: audio gate PASS 13/13.
- All 15 HyperFrames graphics, their copy and motion (`hf/manifest.json`, `hf/BEATS.md`), the 8 way titles (T1 stays
  "Get On A GLP-1 Medication"), recap G16, phone P01, clips C02 to C15.
- Three changes Dan asked for, already in `recipe/plan.py` and `plan_resolved.json`:
  1. **Opener, 0:00 to 0:06.5, two AI clips of the same man, food first then scale:** O1 `aiframes/O1_motion_v1.mp4` (0.00 to
     3.10, source 0.0 to 3.1; never use it past 3.25 s, the spoon reappears and the glass jumps), O2 `aiframes/O2_motion_v1.mp4`
     (3.10 to 6.48, source from 0.3). Dan appears on camera at "Most people" (6.48) with G01. Both carry the AI-GENERATED chip.
  2. **0:31.6 to 0:39.4:** H01 `aiframes/H01_motion_v1.mp4` replaces the junk-food stock (shirtless overweight man eating the
     snack cakes; 8.0 s clip, 7.78 s slot). AI-GENERATED chip.
  3. **G02 fact card (0:39.4 to 0:50.9):** photo is `assets/haub_after.jpg` (the same man 27 lb lighter on a scale), with the
     AI-GENERATED chip. Already re-rendered in `hf/renders/G02.mov`.
- Stills of the three new clips in place: `round2-plan/_ai_stills.jpg` (chips clear of the faces).

**Next action (in order).**
1. Board entry. `cd /Volumes/Extreme/_edit_work/ro10`; `python3 recipe/resolve.py`; `from_plan.py --plan plan_resolved.json
   --words words_out.json --shots shots.json --out hf --render` (should report every scene unchanged).
2. Full film: `python3 -c "import sys; sys.path.insert(0,'recipe'); sys.argv=['x']; import build; build.render_range(0, 518.25,
   '/Volumes/Extreme/_edit_work/ro10/round2/RO10_MASTER.mp4')"`. Two-build cap: check `ps` first; other sessions render heavily.
3. `checks.py` on the master (clearance, face, fill: round 1 numbers G08 65 px, G09 198, G13 117, G15 87; faces 189 px+).
   Hair check on the whole film (adapt `recipe/hair_first.py`; round 1 first minute: 28 px minimum).
4. SRT from the delivered audio's own transcript, chapters, then `_shared/audio/audio_gate.py` and
   `_shared/deliver/gate.py --format longform --plan plan.json`; watch pass (`_shared/deliver/watch.py`); one independent
   `ra-reviewer` on the exact file. Fix what it finds (3-round cap). Report gate rows honestly; RO-12's README lists the rows
   that read Soft Blue cards as burned captions.
5. Deliver to `claude edited long form content/10 - Calories The Reason You're Not Losing Weight/` (master, SRT, chapters,
   recipe files), send Dan the review copy, Edit Queue `delivered`, update `00-MASTER.md`.
6. Description needs: the AI-image sentence, and YouTube's altered/synthetic flag is TRUE for this video (three realistic AI
   clips). The "Zepbound tips video" link goes in when that video is public. Sources for the description: `Docs/SCRIPTS_CALORIES_PAIR_20260921.md` production notes.
7. After delivery: register O1, O2, H01 and the used stock in the clip library (`clip_library.py add ... --used-in "RO-10"`),
   mark RO-10 as the first full-template film in `_shared/hyperframes/README.md`, delete this handoff's rows and the two
   earlier RO-10 / first-full-video rows in `Handoffs/README.md` and `AI_COORDINATION.md` once Dan approves the film.

**Spend.** About $5.65 of AI spend so far (Gemini listening $1.30, frames $1.95, three motions $2.40). Dan raised this
video's cap to $10 on 10-01. No further generation is planned; a retry of one clip is about $0.60 to $1.20.

**Open risks.** O1's usable length is 3.25 s (the plan uses 3.1). The opener runs 6.5 s, not Dan's "first 5 seconds", so
his first two sentences finish before he appears; shorten O2 if he asks. H01 is a generic man, not a likeness of the real
professor. Round 1 page (old opener and old 0:36 clip): http://127.0.0.1:8801/.

**Starter prompt (Claude Opus 5.5, effort high):**

Read and execute `Handoffs/handoff-20261001-ro10-round2-build-full-film.md`. Everything in RO-10 is approved: build the full
film from the locked plan, run the checks, the gates, the watch pass and one independent review, deliver it, and send me the
review copy. Do not ask me anything mid-run.
