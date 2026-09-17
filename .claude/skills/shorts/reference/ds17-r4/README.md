# DS-17 R4 reviewed recipe snapshot

Astra planned and revised; Sol edited. Final review export SHA256: `ad4f7b464faf588909c880de7afddf703921e84e3c597ef8bdb4333bee12dc89`.

This snapshot contains the R4 changes, not a standalone media package. The complete private recipe, sources, frozen R3, captions, unchanged shot caches and evidence are in `Short-form video content/ds-17-support/` and `/Volumes/Extreme/_edit_work/ds-17-r4/r4/`. Copy these files into the package's `recipe/` folder and `edit.frozen.json` into the work root as `edit.json` before rebuilding. Do not run the historical `configure.py` over the frozen map.

## Final construction

Run `python3 recipe/r4_opening.py library-two-shot --build`, then `python3 recipe/build.py finish` from the complete R4 work directory. Check the shared two-pipeline limit first. The ten downstream R3 shot encodes remain unchanged. Do not run the generic `picture` stage: the opening uses its dedicated helper.

The finished owned library asset `jump rope 30 sec - 9x16.mov` has SHA256 `fc59d42814259d3f75489c9a75f3a7e8efa0bfd18433dadf8e85afe2199485e3`. Its actual container is1280×720 with pillars. Crop405×720 at438,0; scale1080×1920. It is already finished BT.709/tv footage: do not apply the camera-roll S-Log conversion. Source5.8s supplies75frames;16.3s supplies67frames. Both play at natural speed, with no body alteration. The142-frame/4.738s opening covers the full first spoken sentence, avoiding a22-frame presenter flash. Header/footer are absent there; existing captions remain.

The earlier single-span selections clipped hair or reached the stop/walk. The earlier66/76-frame cut clipped a shoe tip at its front-angle entry. All are rejected trials. The helper retains a `library-fit` experiment for provenance; blurred fill was rejected and is not the final design.

## Audio and verification

Final audio is stream-copied from frozen R3, AAC SHA256 `71a5cd8d3c9637720ae0b220e6b4b02f5854222cb5ce5d049e26e9540745786b`. Three supported shared-chain trials tested oversampling, gentle compression and a modest presence trim. No reliable audible improvement was established; use the handoff's R3 fallback. The proposed tone alternative belongs only in the labeled comparison. Never claim Muhammad parity or audio PASS: the absolute artifact comparison remains unresolved. No shared gate, threshold or audio implementation was changed.

Any rebuild invalidates the current hash-bound evidence. Re-run caption validation, shared watch with independent judgment, exact-file audio gate and delivery gate. Preserve any failure honestly. This is a private review revision awaiting Dan, not approval for public distribution.
