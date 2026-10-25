# Dad Bod SFC R3

Contained revision of both reviewed R2 takes. Dan requested one larger Daniel Craig source photo, lower-left, with exact label `The Dad Bod she likes` and arrow through audible interview end, plus a stronger existing real studio photo at about33s in the scripted take only.

Working folder: `/Volumes/Expansion/_edit_work/DS-35/round3`. Immutable decisions, full controller and approval-manifest are there. R1/R2 media and selections remain read-only. The sole owner is `01a17430-0acf-72c1-93fa-026651f4da47`.

`build_r3_assets.py` uses maintained shared HyperFrames before-card/media-card templates. No new AI image, motion, download or paid review. The existing finalized studio-blue-11 real shoot photo is retouched; its camera original is verified in asset-provenance.json and the current real-photo disclosure stays. No new physique alteration is applied.

`render_r3.py` patches284..469 and scripted973..1058 on the 30000/1001 frame grid. The handoff prose saying24000/1001 was a typo; actual locked files/renderer/EDL are30000/1001. The renderer packet-copies full R2 AAC, with every packet and PTS verified by `qa_r3.py`. It reuses verified caption rasters and acoustic alignment only because audio packets/timing are identical, then measures caption pixels/sync on the new full file.

A larger photo extends below the interview panel into Dan’s hair. Restore the accepted original keyed foreground OVER the new photo in exactly the replaced region, never over the full already-composited frame, which would double-alpha hair edges. Internal checked context can cache this identical opening shared by both takes.

Production uses the existing edit slot and shared render queue. Fresh complete watch checks, independent review and final shared gates are required for both candidates before review delivery. Raw gate disagreements and limitations remain explicit.

R3 candidate1 was rejected by independent review: a camera switch at native frame443 moves a different interviewee under the old y282 label. Four sparse requested timestamps did not cover this. Preserve failed hashes/reports; inspect every native frame of a revised overlay span, especially source-internal cuts. V2 moves the same live HF label to y100 and uses a far-left arrow. It restores the old label/arrow region from locked R2 while preserving the already-correct enlarged photo and true foreground. No rejected QA verdict is reused. A fresh complete-file reviewer and shared watch/gate must clear each new hash.
