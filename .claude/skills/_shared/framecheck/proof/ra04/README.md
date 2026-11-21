# Frame gate proof: RA-04 leg press (2026-10-14)

`./run_proof.sh [OUTDIR]` gates the six pairs Dan and seven independent reviews judged on 2026-10-14 (frames in
`/Volumes/Extreme/_edit_work/ra04/round2/frames/`; evidence and JSON default to `../framecheck_proof/` there). Expected:
the five rejected pairs FAIL, F4h/F5p PASSES. Results and what each failure matched: the Proof table in
`../../README.md`. Run it again after any change to `gate.py` and bump `GATE_VERSION` if a check or bound changed.

Specs: `spec_AI1-3_F4h.json` (the START of the approved pair; also used for F5h2, F5j, F5m), `spec_AI1-3_F4d_b.json`,
`spec_AI1-3_F4c_a.json` (earlier STARTs).
