# Handoff — the 9:16 kit's first production job: Ad 10's vertical (AV-07), built by the kit

Written 2026-09-18 by Claude (Fable 5.1) at Dan's request, right after his blind verdict on the kit.
**Executor: Codex (GPT-6 Astra, High).** Claude video editing is frozen until Thu 2026-09-24 11:00 CT
(`handoff-20260918-claude-video-freeze-and-codex-routing.md`) — do not launch a Claude editor or a Claude reviewer for this.

## Why this job, and what it proves

VQC Phase 4 built a locked design kit for 9:16 ads (`.claude/skills/shortad-from-longform/reference/kit9x16/`, README there is
the map). Dan judged its from-raw Ad 1 vertical **blind** against the approved vertical on 2026-09-18 and called it a **tie**:
*"the edits look very similar to me, except for the music, and both would work."* (corpus `kit9x16-ad1-from-raw-blind-tie`; the full
story is the "✅ PHASE 4 EXECUTED" section of `Handoffs/handoff-20260911-video-quality-engine.md` — read it first.)

Both kit builds so far were Ad 1, which already had a hand-built approved vertical to lean on (`content.json` was lifted from its
`beats.py`). **The open question is whether the kit produces an approvable vertical for an ad nobody has verticalised** — with the
content sheet written fresh. Ad 10 is the cleanest test and a useful deliverable:

* Muhammad's 16:9 is finalized (09-12) and **live in Demand Gen since 09-15**; no vertical, square or cutdown exists (`AV-07`).
* Its app demos were fixed in round 3 to show **Dan's own before → Dan's goal image**, so the "man who is not Dan" fault that every
  Ad 1 judge had to note does not exist here.
* It is a from-MASTER build, so the audio is Muhammad's mix untouched — Dan's one criticism of the kit (its default music bed) cannot apply.
* Dan's approval unblocks AS-06 (the square) — keep the build dir intact.

## Inputs (verified on disk 2026-09-18)

* His master: `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/my dad bod at 38 my dad bod at 40 | muhammad | 16x9 | ad 10.mp4`
  (1920×1080, 29.97, 5,443 frames, 3:01.6) + `… ad 10.transcript.json` beside it.
* Raw roll: `/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/C1601.MP4`
  (run `_shared/audio/pick_lav.py` on it only if a stage asks; the audio here is his mix, verbatim).
* The job doc: `Handoffs/video-editing/AV-07-ad10-vertical.md` (deliverable names, this ad's real-picture times, the same-person rule,
  the BT.709 colour rule, the ≤0:59 cutdown rules). `Handoffs/video-editing/00-RULES.md` governs; claim the job with
  `python3 scripts/edit-queue/queue.py set AV-07 in_progress --by Codex`.
* Worked examples to copy from, never to build inside: `/Volumes/Extreme/_edit_work/kit9x16/ad1-master/` (from-master: `content.json`,
  `assets.py`, `run_master*.sh`, `run_l.sh` … `run_n.sh`) and `…/ad1-raw/`.

## The build — work in `/Volumes/Extreme/_edit_work/kit9x16/ad10-master/`

1. **Recover his edit** from the raw roll exactly as `/shortad-from-longform` SKILL.md does for any finished video (Step 0b verify the HD,
   then the EDL recovery → `edl_final.json`, the grade → `grade.py` decoded as **BT.709**, his word timings → `m.whisper.json` /
   `ref.whisper.json`). `kit_deliver.py setup --build B --from-build <an approved build dir>` copies the pipeline files; start from the Ad 3
   render-10/12 compositor's grade conventions per AV-07, never from `ad4-vert/` / `ad5-vert/`.
2. **Write `content.json` fresh** — WHAT goes where, phrase-anchored (`at` / `until` words from the transcript), one entry per insert,
   plate, card, lower third and CTA in HIS master, in the shape of `ad1-master/content.json`. The kit decides every time and device
   around them. Media go in `assets.py` (known-rights assets only; AI clips: check hands frame by frame BEFORE use, swap a bad clip for
   one of its own clean frames as a pushed still). Every picture of Dan's physique gets `label_kind` `real` or `ai` — exactly one.
   No asset with a label burned in (README "Measured traps").
3. `kit_deliver.py audio --mode master --approved <his master>` (his mix, stream-copied) → `build_kit.py --from-master … --reference <his master>
   --raw C1601.MP4 --grade grade.py` (decides talk AND window splices; read `kit_report.json` — a design outside `picture.json`'s range is a
   finding, never fixed by moving the range) → `kit_base.py` → `kit_track.py` → `kit_labels.py` → `kit_deliver.py words` → `picture` →
   `captions` → `mux` → `kit_plan.py` (+ `--reference-cut`, `--banned-source`/`--banned-times` for the app recording) →
   `_shared/audio/audio_gate.py <file> --reference-mix his_mix.wav --verbatim` → `kit_negscan.py sheet` → `kit_labels.py --verify` →
   `_shared/deliver/watch.py <file> --plan plan.json`.
4. **Judged watch pass, by fresh sessions that did not build it** (three Codex sessions in thirds works: sheets + first third of strips +
   the negscan sheet; middle; last). Use `watch/JUDGE_PROMPT.md` plus the design facts the Ad 1 judges needed: every bare talk cut and every
   window cut carries an instant ~20 % size step; `punch_*` strips with no join under them are 0.5 s ramps, not steps; flashes on returns
   from cards; exact file names in every entry, no non-image entries; read every caption against the speech. Then
   `kit9x16/kit_fold.sh <build dir> <video> "<who judged>"` — it merges the three findings files, stamps the watch pass, records the
   negscan and runs `gate.py --format ad9x16 --plan plan.json`. **GATE PASS 36/36 with 0 open defects, or it does not go to Dan.**
   A defect → fix in the kit (not in the build dir by hand), re-render, re-judge the whole file (the pass binds to the sha256).
5. **≤0:59 cutdown** from the finished kit vertical by the skill's cutdown method (AV-07: hook, problem, AI demo, payoff, CTA; seams on
   silence and on HIS picture cuts, never inside a flash; his mix only CUT; prove every seam against the master; check the CTA-pill
   trailing-caption overprint). It gets its own gates and its own judged watch pass.
6. **Deliver per AV-07** (names, REVIEW 540p copies, audio A/B, stamps, `notes-vertical.md`, `recipe-vertical/`) and send Dan the review
   copies. His verdict — either way, his words verbatim — becomes a corpus entry the same session (`qc_corpus/README.md`); an approval
   sets `queue.py set AV-07 delivered`, then `finalized` only when Dan says so. No blind page needed: the format already tied blind.
   If he rejects, write the delta he names into `template.json` as the next revision and stop.

## Traps this costs you if you skip them (all measured in Phase 4)

* **Never re-render into a build dir while a judge is still reading it** — the strips keep their names and the verdicts attach to pictures nobody saw.
* **Two builds max across all sessions**; wrap every heavy stage in the process-GROUP cap wait (`run_l.sh` has it). An orphaned ffmpeg from a killed
  chain ran 2 h 41 m at 5 cores — kill process groups, not just the shell.
* **`set -e` does not see a failure behind `| tail`.** A chain ran on past a crashed aligner. Check the stage's own output.
* `kit_deliver.py words` clears a stale `words_ctc.json`; `align_ctc.py` re-aligns a slipped run WITH its trusted neighbours (a lone "to" went 490 ms early alone).
* `kit_labels.py`: a placement accepted only at the 8-px tier can flip on the delivered file — `--verify` on the delivered file is the test; if a spot
  will not hold, pin the proven one or pick a different picture. It writes the chip back by the beat's END time.
* Card chips sit 68 px under the hole; region beats are on the frame grid; the phone-split window takes the chest-up crop — all in code; do not undo them.
* exFAT: `rm -rf`, not `shutil.rmtree`; symlinks for the caption frame sequence.
* The corpus currently reads FAIL on `ds17-r4-final-approved` (another session's entry, audio artifacts). Not yours; do not tune it.
* Never grade the kit yourself. Never raise a bound, never add a `known_gap`, never build a second renderer, kit assets stay in the skill.

## Done when

Both files (full 9:16 + ≤0:59) carry GATE PASS stamps and judged watch passes with 0 open defects; review copies are with Dan; AV-07's status and
the master list are updated; commit, push, confirm the push; this handoff removed from `Handoffs/README.md` and the board's HANDOFFS list.
No dashboard row unless Dan asks.

## Starter prompt (paste into a fresh Codex session — GPT-6 Astra, High)

> Read `Handoffs/handoff-20260918-kit-first-production-ad10-vertical.md` and execute it. It is job AV-07 (Ad 10's 9:16 vertical + ≤0:59 cutdown) built
> with the locked kit in `.claude/skills/shortad-from-longform/reference/kit9x16/` — read that README, the "✅ PHASE 4 EXECUTED" section of
> `Handoffs/handoff-20260911-video-quality-engine.md`, `Handoffs/video-editing/00-RULES.md` and `AV-07-ad10-vertical.md` first. Work in a scratch dir on the
> SSD, two builds max, his audio untouched, every picture of me labelled and the label off my face and abs. Fresh sessions judge every strip and sheet;
> nothing reaches me without GATE PASS 36/36 and 0 open defects. Never grade the kit yourself. Deliver the review copies and record my verdict in the corpus.
