# Instagram 16 stronger retouch review

Prepared 2026-09-28. Review candidate only, pending Dan's choice.

Review: http://127.0.0.1:8795/index.html#row-16

Package: `Short-form video content/covers/review/queue-bakeoff-20260924/round5-row16-retouch-20260928/`

One built-in imagegen edit produced sharper abdominal, chest, shoulder and arm definition from the R4 photographic input. No retry was needed. The prompt is saved in `prompt.txt`; the generation record is `generation.json`. Separate dollar estimate and actual charge were not reported by the built-in tool. This is an unknown cost, not a zero-cost claim.

The exact title `2-minute home arm workout`, Impact 130 type, background, olive divider, border, crop and photo placement are preserved. Rebuilding R4 from its original input produced the identical JPEG hash. Before JPEG encoding, all pixels outside the photo panel match the R4 reconstruction.

The new export is `covers/16-more-ripped-instagram.jpg`, 1080 x 1920 RGB. Its `grid-crops/16-more-ripped-grid.png` is the literal centered crop `(0,240,1080,1680)` of that exported JPEG, 1080 x 1440. The gallery contains only row 16's current/new Instagram covers and their grid crops, with four verified full-size targets.

Visual checks at full source size, full cover size and 270 x 480 phone size found stronger muscle definition, consistent identity, intact hair and arms, unchanged pose and equipment, and no obvious anatomy defects. The left workout list stays outside the crop. The full portrait, title and visible dumbbell pair survive the grid crop. Dan's visual approval remains pending.

All 34 approved hashes in `Docs/QUEUE_COVERS_APPROVALS_20260928.json` matched before and after. The R4 working cover and photographic input also matched their handoff hashes. Detailed results, source, build recipe, manifest and export hashes are preserved in the private package. Photos and recipes remain Git ignored. Installed covers, publishing queues and the locked horizontal YouTube selection were untouched.

Next action: Dan selects current R4 or stronger R5 for Instagram 16.
