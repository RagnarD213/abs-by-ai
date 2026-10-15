AD. RA-13 R2 final review package

Both 53.9205-second native review candidates are in Codex Ad Videos/why do most guys never get abs - RA-13/. Full physical copies are in Videos to Review/. Review: http://127.0.0.1:8973/

Media audit SHIP after CTA clearance repair. Full exact-file delivery gates FAIL, preserved explicitly in final-gate-snapshot.json. Voice tone/floor differs from studio reference; approved horizontal wide is 23.6% headheight against 27% minimum; raw splice detector flags deliberate scale cuts. No threshold changed. No upload/publish/finalization.

Current fresh-build route: build_full.py reads original cut and locked inputs from the external work root plus current cta-layout.json. It now uses the repaired safe CTA positions directly. quality_pass.py prepares actual delivered ASR/audio, complete watch-plan.json inventory and watch-final native evidence. A fresh reviewer judges all native images. write_sheet.py writes exact camera5 continuation over the audio-only seam and final audio-tail facts. Run the shared edit-sheet validator with --hash. run_delivery_gates.py runs every row and shared graphics checks. finish_package.py preserves failures honestly and packages review candidates.

repair_cta.py and post_cta_checks.py preserve the scoped historical repair phase. Do not rerun them as an extra phase after a fresh full build. All inputs/assets are source-specific, fingerprinted and read-only; paths are in roll.json, decisions.json, build-record.json and the edit sheet. Large raw media is not duplicated in Git.

Raw camera, LUT and approved source assets stay at the absolute paths recorded in the input facts. Rebuild includes the source locators and untreated cut. No AI motion was generated. Rejected A0074 and B0037 clips never appear in these masters.
