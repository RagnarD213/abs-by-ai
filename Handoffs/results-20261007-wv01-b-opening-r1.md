# AD: Fired Them All B opening R1 review handoff

2026-10-07. Current task: Fired Them All AD R1. Next revision: Fired Them All AD R2. Recommended model: GPT-6 Astra, high effort, because this is a flagship website sales opening.

## Goal and current state

The first substantial Version B opening is built for Dan to review. It is254.921333s; the opening plus10.1101s of approved A context is265.031433s. No new B creative approval has been received. Get Dan’s decisions on the opening, new visuals and join/voice, then apply only those notes in a new round. Do not infer full-film authorization from a narrow approval.

Review page: http://127.0.0.1:8870/ . Local file: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round1/index.html`.

If the server is down, from the project run:

```sh
python3 .claude/skills/_shared/review_server.py 8870 '/Volumes/Extreme/_edit_work/wv01-edit/version-b/round1'
```

It serves byte ranges for scrubbing. Chrome forward/backward seeking was verified. First-minute, full-opening and join previews exist in540p and1080p under `previews/`. All13material graphic/clip items have stills and moving context clips.

## Edit decisions and source evidence

Read `review/decisions.json`, `take-map.json`, `picture-repairs.json`, `QA.md`, `watch_pass.json`, `edit-sheet-validation.json` and the opening’s `.edit-sheet.json` before editing. They are inside `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round1`. Working opening-only subtitles are beside the previews.

C1699 source ranges, native frames:2891-4364,4563-5482,5640-6171,6306-6972,7620-8208,8364-8872,8938-11456,12185-12622. End frames are exclusive. The sixth range starts8364 to remove residual “night”; keep the previous complete “165.” The seven script beats remain intact, with no speed-up. Live scripts were checked.

New B uses the approved A grade C and Soft Blue Light system, static wide/tight framing, source-fitted shared voice processing, and the current shared HyperFrames method. Role cards are replaced by an approved app phone image; the seven-column week grid has168cells,3trainer hours and165remaining, then all168for AI availability. No strong literal drive-through/fridge clip was found, so those lines stay on Dan. Approved A proof photos and M100 full YouTube footage are reused. No new AI imagery, video generation or music.

Native-frame review found three brief intermediate camera shots. Corrected: frames202-211 land directly tight;517-526 return directly wide; the before-photo callback begins at2923 to cover a4-frame source-cut lead-in. Original candidate and audit are archived under `review/pre-picture-repair/`. Read the current exact-file checks for the repaired copy.

A begins at original frame5111 (170.537033s), ends before5414 (180.647133s), and retains its original decoded audio without gain processing. The A master remains unchanged, SHA256`acddfb5b3bad7bb6d85f937b74054fafb4be33505f49ae91cd765a8ecac88836`. Repaired opening-plus-join SHA256`6e60be3d333a603b45bf3a2214d5cc6d341bf44b3a9c59ef170157da376e7bba`.

## Checks and limits

The initial full audiovisual review and independent speech review found no major speech defects. All123junk candidates were dispositioned; maximum quiet gap0.88s. Shared opening audio and HyperFrames checks passed. Native-frame inspection produced the three picture repairs above. Current follow-up results are saved in `review/QA.md` and `watch_pass.json`; do not substitute older stamps. QC cost approximately$0.32339; generation cost$0. Recipes, media, exact source maps and check artifacts remain in the private work folder.

This is an opening review. A’s inherited website delivery gate is FAIL despite its2026-09-29 creative approval. No full-film or website-delivery PASS is claimed. Complete B, six C1700 callbacks, upload, installation and publishing remain outside this round. The dispatcher stays paused.

## Ready-to-paste starter prompt

AD: Continue WV-01 Version B as Fired Them All AD R2 using $vsl-edit and Handoffs/results-20261007-wv01-b-opening-r1.md. First read the R1 decisions and current checks, then apply my review notes to the opening and join in a new round. Preserve approved A and all B elements I approve. Show changed sections and affected graphics in context. Do not build complete B, add C1700 callbacks, upload or publish unless I explicitly authorize that scope. My notes: [paste notes].
