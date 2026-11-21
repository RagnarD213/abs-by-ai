CONTENT | RO-01, "How To Keep Your Muscle While You Lose Fat" | LFC | Round 9

# Quiet instrumental music choices, then the final film

Written 2026-10-05 after Dan reviewed the finished R8 first minute. Recommended next task: **Claude Opus 5.5, high effort**, using `/longform-edit`. Task name: **Keep Your Muscle LFC R9**. Read `.claude/skills/_shared/VIDEO-RULES.md` in full before video or audio work. The overnight dispatcher remains paused.

## Dan's R8 verdict and the one open choice

Dan said: "Everything in the video itself looks good but I don't like the background music. I want something that's not distracting in the background without lyrics. I want to avoid hip-hop where there's rapping in the background beneath my talking. Make a handoff for the next round to see a few different options for non-distracting background music."

The **R8 first-minute picture is approved**. Keep its H04 opener, presenter cuts, camera color, G01/S01/G03 graphics and J01 five-frame pause cut. The **music is rejected**, so do not treat the R8 first minute as fully approved for final assembly. Keep the voice and its approved treatment, replace the music bed, and show Dan options in narration context. Do not offer the current music as a candidate.

R8 first minute: `/Volumes/Extreme/_edit_work/ro01/revision8/review/RO01_R8_first_minute_H04.mp4`, SHA256 `0b5f65e663d143dee5074683c7bc2b78436600cfa12b86b00e12c6ed690232d5`. It is 960x540, 29.97 fps, 59.993 seconds. Build and QA records are in `revision8/recipe/build_first_minute.py` and `revision8/review/first-minute-QA.json`. The local review page at port 8788 may not survive a new task; use the exact file.

## Audio source and protected work

- R3 master: `/Volumes/Extreme/_edit_work/ro01/RO01_MASTER_R3.mp4`, SHA256 `17f666fc1a54f078768f6bef902ee22219f46b92681da627bbf0c68ab27a6f4f`. Its camera color and spoken voice treatment remain the reference. Its **music selection is no longer locked**.
- Original assembled voice source: `/Volumes/Extreme/_edit_work/ro01/voice-untreated.wav`, SHA256 `e57da3869f60dc28a425ad3969798441e97f090c022a14747667bb270214867d`. The shared voice chain and old settings are recorded in `/Volumes/Extreme/_edit_work/ro01/audio-plan.json` and `audio-settings.json`.
- The old plan used `Media/codex-video-trial/02-organic-sample/cache/independent-bed.mp3`, SHA256 `4fae540055bd980aa1e5316fb72bc3c7c57c45b4c8ab767f9439d6a24d6344ca`, at `--bed-db -42`. Check whether the audible rapping comes from this bed or any other source before replacing it. Rebuild from the separate voice source. Do not try to remove music from the finished R3 stereo mix.
- Preserve the 23 exact approved R4 items in `/Volumes/Extreme/_edit_work/ro01/revision5-plan/decisions.json`, SHA256 `8c34b785ab2ae40eb6c489aa0d7baa6548bb4c15ebdf994d495d0494d6ed4f15`. H04 and B01 motion remain approved as recorded in `Handoffs/handoff-20261005-ro01-r8-h04-first-minute-and-final-film.md` and `revision7/decisions-20261005.json`. H06 stays out and B02 stays removed.

## Next task, in order

1. Make **three different instrumental music options** from usable tracks. Each must have no singing, rapping, spoken words or vocal samples. Choose subtle arrangements that sit behind Dan's narration, with no prominent beat, melody or sharp accents competing with his words. A quiet ambient texture, a sparse piano or pad bed, and a gentle organic instrumental are possible directions if suitable tracks are available. Also provide a voice-only reference for comparison, separate from the three music choices.
2. Keep the same approved R8 first-minute picture and the same processed voice in every version. Change only the music. Use the shared audio chain, compare the resulting voice against R3, and mix all three beds at a similarly unobtrusive perceived level under speech. Inspect transitions, pauses and the ending so a track never calls attention to itself. Record each track's source path, exact hash and mix setting. Do not generate new picture assets or run paid music generation just to make these auditions.
3. Put the three **finished first-minute mixes under narration** on one working review page, plus the voice-only reference. Let Dan hear them at matched playback volume. Explain the musical difference in one short line per option, then stop for his pick or correction. Do not assemble the full film before this music decision.
4. After Dan picks and approves the revised first minute, assemble the complete 16:9 RO-01 film using that bed and the approved picture decisions. Keep the R3 voice treatment and color, all 23 exact R4 items, H04 and B01. Apply J01's five-frame cut once, retain complete "forever" and "Now," and use clean graded presenter footage in B02's former R3 190.7897 to 198.4897 second slot.
5. Regenerate the SRT and chapters against the actual final timeline. Run exact-file picture, audio and subtitle gates, inspect every join and watch the complete candidate with sound, then obtain one independent full-candidate review. Fix real failures and recheck affected gates. Deliver the full film, SRT, chapters, stamps, review evidence and provider cost record for Dan's final review.

Do not make a full vertical, square or one-minute cut of this CONTENT video. Do not make thumbnails, upload, publish, deploy the app or resume the dispatcher in this edit task.

## Ready-to-paste starter prompt

Name this task **Keep Your Muscle LFC R9**. Execute `Handoffs/handoff-20261005-ro01-r9-instrumental-music-options-and-final-film.md` with `/longform-edit`. This is CONTENT, RO-01 LFC. I approved the R8 first-minute picture, including H04, but rejected the background music. Show me three clearly different, quiet instrumental beds with no lyrics, rapping, speech or vocal samples, each mixed under the same first-minute narration and picture, plus a voice-only reference. Keep the R3 voice treatment and color, all 23 approved R4 items, approved B01, and the J01 cut. Keep H06 out and B02 removed. Stop for my music pick. After I approve the revised minute, finish and check the full 16:9 film with SRT and chapters. Do not publish, upload, deploy or resume the dispatcher.
