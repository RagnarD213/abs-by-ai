AD: Fired Them All AD R5

# R5 VLC review receipt, 2026-10-10

The two requested repairs are complete. Dan finalized the exact full R5 film on 2026-10-10: "All right this video looks great. This is finalized." The normal-speed master is preserved in `Website Videos/WV-01 Version B/` and the external final folder. This video's VLC review copies and old port-8870 review service were removed. Website installation and split-test launch have not been performed.

The approved physical-phone goal scene replaces the studio freeze at frames [8248,8338), 4:35.208 - 4:38.211. The ending completes "I have never felt better in my life" before P6. Fourteen original moving studio frames finish the sentence, P6 uses fixed tight framing at [25439,25509), and the complete original 283-frame closing animation follows. All final spoken words remain intact. The approved opening and other scenes are preserved.

The recovered sentence frames reproduce the historical color conversions of the approved component. The rejected raw-color extension was discarded before delivery. Every extension and P6 frame was checked for movement, hair and gestures. Accepted PCM was reordered once without omission, duplication or new voice processing.

Audio gate, sheet validation, native seek and complete ending-sentence order pass. Independent content review covers 43 scenes, six intentional photo holds, twelve callback joins, 178 boundary strips and twelve whole-film sheets. The 368 image verdicts include pair identities covered by strip frames. Corrected original reference offsets and graphic blocks verify content, copy and layout; they do not establish 43 full-scene pixel matches. One Gemini review covers the encoded full film at 2fps plus denser repair/source contexts. This is not continuous human real-time playback.

Two inherited picture defects remain recorded in the technical evidence: the same-crop studio pose reset at 6:30.757 and overhead hand/forearm top-edge crop at 14:00.506. Freshly checked on R5, preserved under the scoped request, neither waived.

Actual R5 strict gate: **FAIL**, 31 passed, 6 failed, 4 declared not applicable. Initial full run also has two NOT MEASURED rows. Both pass the separately saved evidence-only recheck after adding actual R5 records and approved templates. This is not a new full-run verdict. Failed rows:

- `cut:min_segment`: 2 segment(s) under 0.2s: [(289.22226666666666, 289.32236666666665, 'W2'), (418.2511666666667, 418.28453333333334, 'W2')]
- `cut:jump_cut`: 7 adjacent visible segment pair(s) at one framing: [(333.67, 339.01, 'W2'), (339.01, 344.81, 'W2'), (390.76, 395.19, 'W2'), (418.25, 418.28, 'W2'), (469.4, 471.57, 'W2')]
- `cut:splice_visibility`: 16/180 joins above the file's own p99 ceiling (20.96): [(289.32, 21.16), (299.27, 21.28), (313.08, 20.99), (338.97, 21.4), (339.01, 21.4), (380.11, 22.34)]
- `captions:burned`: no burned captions required; detected on 31% of 36 sampled frames (max 10%)
- `watch:pass`: 178/178 boundaries reviewed as consecutive frames, 368/190 images judged by Fresh independent R5 reviewer; proxy boundary strips and same-frame pair coverage; scoped inherited defects open (tied to this file by sha256); 4 open defect(s): naked_splice @ 390.757; naked_splice @ 390.757; naked_splice @ 390.757; out_of_frame @ 840.506
- `junk:dead_air`: longest silence inside the speech 1.16 s (max 1.00 s); 2 over the bound: 13:20.32 (1.16 s), 9:37.24 (1.02 s); threshold -30.0 dBFS against speech at -11.7

All 25,792 frames retain 1920x1080 geometry; 1001 seek comparisons are identical. 967 retained-picture samples have minimum 43.30dB PSNR. No automated threshold or waiver changed.

One Gemini QC call has token-cost estimate $0.894088, below the announced $3 maximum; temporary provider files were removed. R5 generation spend/calls are zero. Saved cross-round generation cap $50 was not reset; prior actual charges remain unknown. Historical R4 QC estimate $0.388944 is preserved.

Full film: 14:20.593, 25,792 frames, 30000/1001, 1,195,262,710 bytes. SHA256 `903eca4cd69ba19203394ee2a1c51ebb7bc9fce5d9bd6a9d8710c05297bf16fa`.

Finalized full film and SRT/VTT: `Website Videos/WV-01 Version B/Fired Them All AD R5 - complete Version B 1080p` with the appropriate extension. Recipes, frame map, accounting and exact-file evidence: git-ignored `Media/wv01-r5-20261010/`, especially `review/final-qc-summary.json`, `review/independent/final-review.md` and `review/website-delivery-gate.json`. Heavy sources remain at `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round5/`. R4 external history and unrelated review copies remain intact. Only this video's project review copies were removed.

Next action: Claude creates a separate uniform 1.2x version for VLC review using [the acceleration and subsequent website-test handoff](../Handoffs/handoff-20261010-wv01-b-claude-1p2x-then-website-test.md). Website setup follows review and Dan's separate split-test software decision.
