# Smaller Plates Reaction SFC R2: M2 execution

CONTENT. Same round, same revision and same chat; this is a host move, not a new edit or new approval round.

Dan explicitly requested the M2 on November 15, 2026: “Can you do this edit on the M2? I'm seeing there's no editing on the M2 right now”. This supersedes the M6-only statement in the original R2 handoff.

- Sole editor chat: `01a1dffe-54a2-73a3-8818-23f9c7f16278`, GPT-6.1 Sol/high. Revision `01a1dff8-6f44-77c3-8de9-57efa890463a` is still in progress and must execute only once.
- Current execution root on M2: `/Volumes/Extreme/_edit_work/DS-108`. Original M6 work and R1 review are preserved, inactive.
- Cancelled M6 waiter and removed only its DS-108 edit-cap entry. Explicit move recorded through `editroute.py pick ... --host m2 --move`. Acquired the M2 edit slot. `resume.py check DS-108` confirms M2 ownership.
- Commands/read/write work stay on M2 through `.claude/skills/_shared/editroute/resume.py run DS-108 -- ...` from the original chat. Do not launch a second editor.
- Source: M2 root `footage/C1909.MP4` points to its original on the Extreme. SHA-256 `dc1372067f1da89a77cbe0457261a2d2ad8c556fd893bc9a757417b8a314115a`, 8,590,364,031 bytes, independently measured on both Macs.
- All ten approved media hashes and the three original round records were verified on M2. Original `decisions.json`, approval manifest and controller are unchanged. The translated location/hash map is `migration/m2-transfer-manifest.json`; proof is `migration/approved-hash-verification.json`.
- The Extreme does not support hard links. The initial `rsync -aH` reported those failures; `rsync -a` copied the 245 affected files as independent, identical copies. No approved source was changed. Complete checksum comparison follows before cache reuse.
- Only new `round2/recipe/` copies received path translations for the M2 home/project and work root. `r1/recipe/` stays unchanged as provenance. Use the adapted scripts, never run old hard-coded M6 paths.
- Short watching calibration completed: 82 native frames from request 30.10, house R2 maths/RIM3 unchanged. Editor inspected native head detail and whole portraits on pink/light/dark fields at f3/39/78; no visible defect in those frames. This does not certify the whole key or full film. `round2/watch-calibration.log`, `round2/key/watch-cal/calibration.json` and `calibration-sheet.jpg` preserve it.
- Next heavy step: `round2/key-watching.sh`, through stallwatch and renderq heavy. It requires full-transfer verification, decodes watching request19.18/N642, uniquely matches all 82 calibration RGB frames, reuses stage1 and only the valid temporal interior, then keys missing frames once with keyonce stamps. No hard links on this disk. Planned quote keep[3,638) is provisional until final sync/boundary checks.

## Resume after the watching key

Read remote `round2/execution-decisions.json`, controller and original `HANDOFF.md` using these M2 path translations. Reverify the same owner and `phase=complete`; acquire M2 slot again. Inspect the process exit and native key cache; resume it if incomplete, do not launch duplicates. Then finish source word/phoneme boundaries, missing used response-key ranges, full-duration moving HyperFrames, the approved Voice C chain, complete 1080p assembly, full-AAC captions/alignment, exact-file gates and one fresh independent full-candidate audit. The full film is not yet rendered, approved, uploaded or scheduled. No spending or publishing is authorized by this move. Keep Colour B, Voice C, medium framing and G00-G03.

Source calibration and exact-file QA requirements from the original R2 handoff still apply. The legacy preview renderer contains Voice D and is not a full-film launcher; never run it unchanged. Preserve original FAIL/NOT MEASURED and source-specific approvals honestly. Serve the checked final through the managed review server, verify mirror/link/hash/range-seek and silent playback, hand Dan a paused sound-ready player, and copy the exact full review to Videos to Review on M6. Release the M2 edit slot with --review only when the checked complete review is delivered.
