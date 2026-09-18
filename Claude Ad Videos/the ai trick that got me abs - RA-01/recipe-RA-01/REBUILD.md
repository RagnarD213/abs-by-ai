# Rebuilding RA-01 from this recipe (ROUND 2)

Run in this order from `/Volumes/Extreme/_edit_work/ra01/` (copy the scripts back out of here).
`capwait.sh <cmd>` runs a stage only when fewer than two video builds are going anywhere on the box.

| # | command | what it makes |
|---|---|---|
| 1 | `python3 s01_env.py` | `lav.wav`, `lav16.wav`, `env.json` — the lav pulled per `C1663.MP4.audio_source.json` |
| 2 | `./capwait.sh bash s02_tx.sh` | `tx/c1663.whisper.json` (chunked medium.en) + orphan and repeat scans |
| 3 | `./capwait.sh python3 s32_grade.py` | **round 2, R5** — `grade.json` (exposure AND saturation, measured against the approved website video for luma and the approved Ad 1 vertical for chroma) + `r2/grade/proof.jpg` |
| 4 | `HEAD_SRC=27.165 python3 s03_edl.py` | `cut.json` — take spans by phrase, airtight pause removal off the envelope. **Round 2:** the head edge is pulled to 0.12 s before the ENVELOPE ONSET (R1: the file opens on the first word) and no pause cut is made after the last word (R7). `DROP=R3B` would cut line L11 for length; it is not needed. |
| 5 | `./capwait.sh env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py` | `cut_audio.wav`, `mix.wav` (the one shared voice chain) |
| 6 | `./capwait.sh python3 s09_align.py` | `words_aligned.json` — wav2vec2 CTC forced alignment against the FINAL mix |
| 7 | `./capwait.sh python3 s04_track.py` | `framing.json` — hair top, head centre **and the face box**, 5/s, over the kept spans |
| 8 | `python3 s05_plan.py` | `beats.json` — the R1 beat map, the R2 levels and fixed centres (face box inside 8–92 % of the width), the R3 macro slice, the CTA beats, the frame-exact timeline |
| 9 | `./capwait.sh python3 s06_assets.py 9x16` and `16x9` | the card clips + `meta.json` (measured chip positions and card rectangles) |
| 10 | `./capwait.sh python3 s07_captions.py 9x16` / `16x9` | caption PNG states, `captions.mov`, `captions.srt` — **captions on every beat** (R1) |
| 11 | `./capwait.sh python3 s11_cta.py 9x16` / `16x9` | the CTA pill alpha MOV — 16:9 is a compact pill placed beside him by person mask (R4) |
| 12 | `./capwait.sh python3 s10_render.py 9x16` / `16x9` | `picture_<k>.mp4` + `timeline_<k>.json` |
| 13 | `python3 s14_deliver.py mux 9x16` / `16x9` | `master_<k>.mp4` |
| 14 | `./capwait.sh python3 s25_hard.py master_9x16.mp4` | `hard_splices.json` — which splices VISIBLY jump on the delivered picture, stamped with this cut's signature. If it forces a splice the plan did not cover, re-run 8–13. |
| 15 | `python3 s15_txmaster.py <k> master_<k>.mp4` | `transcript_<k>.json` (the FINISHED render) |
| 16 | `python3 s09_align.py master_<k>.mp4 speech_<k>.json` | `speech_<k>.json` from the DELIVERED audio |
| 17 | `python3 s20_neg.py <k> master_<k>.mp4 <n> '<findings>'` | `logs/negative_scan_<k>.json` — recorded after the sheet has been LOOKED AT |
| 18 | `_shared/deliver/watch.py master_<k>.mp4 --plan recipe-RA-01/gate_plan_<k>.json --out watchpass_<k>` | the sheets/strips/pairs a human has to look at, and `watchpass_<k>/watch_pass.json`. ⚠ **the shared tool only** |
| 19 | `_shared/deliver/watch.py --judge watchpass_<k>/watch_pass.json --findings watchpass_<k>/findings.json --by "<who looked>"` | folds the verdicts in |
| 20 | `python3 s12_gateplan.py <k> master_<k>.mp4` | `recipe-RA-01/gate_plan_<k>.json` |
| 21 | `./capwait.sh bash s24_gate.sh <k> ad9x16\|ad16x9` | re-writes the plan, then the delivery gate + stamp |
| 22 | `audio_gate.py master_<k>.mp4 --ab AB_ref-vs-ours.mp4` | the audio stamp + the A/B clip |
| 23 | `./capwait.sh python3 s33_verify.py <k> master_<k>.mp4` | `r2/verify_<k>.json` — the delivered-frame proof of R2 (face box 8–92 %, sharpness) and R5 (face luma/chroma) |
| 24 | `python3 s28_fluxdiag.py` / `python3 s30_sfx_probe.py` | `flux_diagnosis.json` / `sfx_probe.json` |
| 25 | `python3 s16_measure.py` then `python3 s31_measure_finalize.py` | `measurements-RA-01.json` (plan §8, with a completeness proof) |
| 26 | `python3 s29_ship_held.py [--masters]` | the delivery folder. **Without `--masters` it places only the review copies, A/B, notes, recipe and stamps** — the held-master path, used whenever either stamp reads FAIL |

`s23_finalize.sh <k>` chains 13, 15, 16 and the audio gate. `s26_all.sh` runs it for both aspects.

**The round-2 chains, in the order they were actually run** (each is one `capwait.sh` job):

| script | what it does |
|---|---|
| `s36_final_pass.sh` | captions → both pictures → the mix **locked to the picture** (`LOCK=picture_9x16.mp4`) → mux → audio gate → transcript → delivered-audio alignment → negative sheet |
| `s38_recut.sh` | the re-cut after `s25_hard.py` measured the visibly-jumping splices on the delivered picture: CTA overlays + both pictures + all delivered evidence |
| `s39_rest.sh` | the tail of that chain (16:9 mux, gate plans, strips, watch passes) |
| `s41_final.sh` | the final render after the macro card's first-frame and out-point fixes, then every piece of delivered evidence again |
| `s40_blink.py <master> <f0> <f1>` | eye-aspect-ratio per frame — how the macro card's out-point was chosen |

⚠ **The watch pass needs `--log watchpass_<k>/watch_pass.json`.** Without it both aspects write to
`logs/watch_pass.json` and the second overwrites the first, while `s12_gateplan.py` points the gate
at the per-aspect path.

⚠ **`s34_strips.py` filters AppleDouble `._` files.** This SSD writes them beside every PNG and they
end in `.png`, which doubled the frame count and tripped the script's own grab assertion.

Assets used (all already existed; **$0.00 of AI generation**):
`Media/example pictures/dan by pool.png`, `photos/Dan Before Pictures/01_LIGHT_plus8lb_PRIMARY.jpg`,
`photos/finalized social media photos/studio-{blue-10,gray-41,white-90}_FINAL_PRIMARY.jpg`,
`Media/ad-assets/ad2-nutritionist/clips/app-flow-macro-tracker-itemized.mp4` (**40.50–43.60 s**, the
only stretch where the itemized list and the calorie total are stable),
music `Realizer.mp3` (Pixabay, no attribution), LUT `slog3_709_e1.15.cube`.

Round 1's two masters and their four stamps are preserved in `../round1/`.

---

# ROUND 3 (plan §13) — what this recipe now rebuilds

Round 3 changed four things and nothing else. Run the round-2 chain above, with these differences:

| # | command | what changed |
|---|---|---|
| 3a | `python3 s42_bed.py` | **D3.** Writes `music/Realizer_r3bed.wav` — `Realizer.mp3` with its own 10 ms envelope inverted from 53.20 s on (gain −3.2…+14.0 dB, ramped in over 1.2 s) so the bed holds level through the exposed tail. The chain is untouched; this is an ASSET, handed to `voice_chain.py` through its existing `--bed`. |
| 8 | `python3 s05_plan.py` | **D4 + D5.** Reads `face_src_r3.json` (per-hold face-box extremes measured on EVERY frame of the round-2 masters, mapped back into source pixels) and takes the WIDER of that and the 5 Hz landmark track; places a clamped crop `MARGIN_PX = 4` inside the violated edge; computes `cx16` so every 16:9 NEAR hold takes its neighbouring FAR hold's centre (all 1088). Also pins the forced-splice list to `round2/beats.json` so the splice `s25_hard.py` found AFTER the round-2 plan (36.003 s) is not adopted. |
| 11 | `python3 s11_cta.py 16x9` | **D6.** One 396×194 three-line pill for BOTH beats, placed by a person mask unioned over 14 probes of each beat, lowest position inside the 54 px frame-safe margin → `(54, 832)`. Prints the caption clearance. |
| 5 | `env BED=music/Realizer_r3bed.wav BED_DB=-32 LOCK=picture_9x16.mp4 python3 s08_audio.py` | the only mix change: the bed file. |

New evidence stages: `s43_r3verify.py <k> <master>` (delivered face box on every talking frame + the
head-centre step at every NEAR↔FAR join), `s45_pillproof.py`, `s47_sharpness.py`, `s48_tail.py`
(`TAIL_T0` defaults to 55.40 — the window must start AFTER the last word), `s49_r3look.py`.

The round-3 chains, in the order they were run: `s44_r3a.sh` (bed + CTA + pill proof),
`s46_r3b.sh` (both pictures, the mix, both masters, every gate plan, both watch passes, the proofs),
`s50_r3c.sh` (the 9:16 re-render after hold 4's centre was corrected 962 → 950 so the face box AND
`framing:centering` both hold; 16:9 and the mix are unchanged by it), then
`s20_neg.py` for both aspects and `s24_gate.sh <k> ad9x16|ad16x9`.

⚠ **`compliance:negative_events` fails until `s20_neg.py` is re-run for the new sha.** The chain
regenerates the sheet; the verdict is recorded by hand, after the sheet has been looked at.

⚠ **`capwait4.sh` is `capwait.sh` with a 4 s poll instead of 20 s.** Same two-build cap; it just
catches a free slot sooner on a busy machine.
