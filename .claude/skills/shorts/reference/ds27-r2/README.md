# Home Workouts SFC R2

CONTENT dedicated Short. Owner revision01a19c75-b53d-7871-9f4d-cb668400fc13. Dan selected ColourB/GentleBass and approved the opening/inserts. Immutable approvals and data remain at `/Volumes/Expansion/_edit_work/DS-27/round2/decisions.json`; execution is separately checkpointed in execution.json. Never reapply a delivered revision.

This records the full61.428s/1841frame build at1080x1920,30000/1001, with burned J2 captions and optional SRT. Final media and quality records stay on the work drive and in the delivered folder, never Git.

## Rebuild

Verify round-controller.json productionOwner matches the active chat and phase is complete; acquire DS-27 through editcap before production. Read live VIDEO-RULES and the existing R2 execution checkpoint. Run from project root through renderq, using `recipe/repair_build_r2.sh` in the work directory. It reads final data and the shared HyperFrames manifests and does not redo the approved creative packet. Sources and immutable R1 graphics are required at their saved paths/hashes. The prepare script is revision execution/resume logic, not a command to run over a delivered revision.

## Source-specific repairs and traps

- Native C1719 is2160x3840 after rotation, Rec709 S-Cinetone; no transpose or log LUT.
- Gentle Bass is the approved shared-chain70Hz highpass and+1.5dB broad120Hz lift, no expander/dereverb,4x oversampling. Preserve tone despite the known absolute-reference failure.
- FAR1350x2400, NEAR1120x1990; source-calibrated hair anchors and shared landing.py. New AI return uses its actual source259.3027s cut-frame anchor.
- Merge the Daily excerpt override once at1467/FPS, replacing the complete old trailing chunk. Filtering only by its start duplicates Once working out because the old chunk starts8.9ms before the excerpt origin.
- A0157 original trainer hair clips earlier than its last frame. Use its clean first2.5s at output1581–1656, then a genuine camera NEAR return. Report the source's tiny existing headroom; do not invent missing hair or claim20px trainer clearance.
- JSON cache dimensions must be a list before comparison. A tuple always differs from the loaded JSON list and needlessly re-encodes approved valid scenes.
- Mac AppleDouble sidecars may move automatically with their parent file. Ignore `._` entries when preserving internal candidates, or a later rename raises missing-file errors.
- Whole-cue PNG evidence uses its actual first word to identify cue onset, not a concatenated phrase pretending to be a single word. Preserve all-cue text and full-word ASR diagnostics separately. Split hyphen suffixes can be joined lexically while preserving original first/last acoustic times and retaining raw tokens.
- Shared audio selftest currently names two missing historical Ad1 fixtures; preserve the four suite failures and distinguish available chain tests from fresh candidate gates. Do not change a shared gate/bound to hide it.

All automated listening/playback stays silent. Native/source images and numerical results are not an audible listen or full-speed perceptual watch. Independent complete-candidate review is mandatory before delivery. No covers or publishing in this task.

- Run the complete gate only after real watch judgments and scan evidence are present. The initial full R2 run took about12minutes and correctly failed unjudged watch/missing scan metadata; focused diagnostics on later metadata cannot turn that full FAIL into an overall PASS. Keep the exact-file full stamp and supplemental diagnostics distinct.
