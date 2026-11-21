CONTENT | RO-01, "How To Keep Your Muscle While You Lose Fat" | LFC | Round 9

# Finish RO-01 with Dan's selected Bright Electronic music

Written 2026-10-05 after Dan chose **Bright Electronic**, option B in the second R9 music review. Task name: **Keep Your Muscle LFC R9**. Recommended Codex model: **GPT-6.1 Sol, high effort**. Use the `long-form-content-edit` skill and the project's `/longform-edit` workflow. Read `.claude/skills/_shared/VIDEO-RULES.md` in full before editing. The overnight dispatcher remains paused.

## Decision and current state

Dan approved the R8 first-minute picture, rejected its rap-containing music, rejected the first R9 piano, ambient and acoustic choices as too sleepy, then said of the second set: **"I like Bright Electronic the best. Let's go with that."** This selects **B, Bright Electronic**, the `Werq` instrumental. The music choice is closed. Do not present another music round or ask Dan to reapprove unchanged first-minute picture. Assemble the full 16:9 film, then show him the complete candidate for final review.

The chosen first-minute file is `/Volumes/Extreme/_edit_work/ro01/revision9/review-electronic/RO01_R9_B_werq_first_minute.mp4`, SHA256 `fc1f1425a5f46371da1b2a5b35647c3ec80eb51bbb902410b01b6a3a208bfe7b`. The review page is `http://127.0.0.1:8790/review-electronic/`, but use the exact file if the local server is gone. Its picture stream matches R8 exactly, SHA256 `3750c2826da7a1ed52af2c6a3c1a13c9deb0a0ad894d3bdba1edb526c02fb56a`. It has 1,798 frames at 30000/1001 fps, 960x540, 59.993 seconds. The finished film should be native 1920x1080, 16:9, at the same frame rate. Rebuild approved elements at final resolution and compare the first minute against this accepted preview.

The full film, final SRT and updated chapters have **not** been assembled. Do not treat R3 as the final picture or reuse its rejected music.

## Exact selected music and voice

- Source: `/Volumes/Extreme/_edit_work/ad1-8-14/music/Werq.mp3`, SHA256 `e03bc2d89a1913ba68d120c806141952bea09d93cf11fcc0cac7c2d378014d13`. It is 162.299 seconds long. Track: "Werq" by Kevin MacLeod, ISRC `USUAN1800005`. Source and attribution record: `https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1800005`. Carry its attribution into the later video setup description.
- Exact preview method: `/Volumes/Extreme/_edit_work/ro01/revision9/recipe/build_music_previews_electronic.py`. It measures the track's first-minute RMS at about -9.767 dBFS, sets the music gain to `-22.733 dB` for a -32.5 dBFS pre-duck bed, fades in over 1.5 seconds and out over the final 2 seconds of the preview, then ducks beneath the voice with `sidechaincompress=threshold=0.020:ratio=6:attack=12:release=420:makeup=1:level_sc=1`. The delivered preview's music is about 30.6 dB below the voice. Reproduce its perceived balance in the full film. Check long passages and speech gaps by listening; do not assume one fixed setting works across the entire track.
- The source song is shorter than the film. Loop or extend it at musical phrase boundaries with smooth crossfades. Preserve the exact song phase and mix through the approved first minute, avoid audible repeat points or music peaks over narration, and give the film's actual ending a deliberate fade. No lyrics, rapping, speech or vocal samples. A `small.en` screen of the complete 162-second track found no sustained intelligible speech; listen to the full rendered mix as well.
- Use the separate processed lav source at `/Volumes/Extreme/_edit_work/ro01/cache/voice-chain/lav.wav`, SHA256 `8d56c592178e17f39287262da634d143c85851159a71238102e03262c282da5e`, and the R3 chain recorded in `/Volumes/Extreme/_edit_work/ro01/mix.wav.voice_chain.json`. Original untreated voice: `/Volumes/Extreme/_edit_work/ro01/voice-untreated.wav`, SHA256 `e57da3869f60dc28a425ad3969798441e97f090c022a14747667bb270214867d`. The old stereo mix includes the rejected music, so do not remove music from it or use it as the voice stem.
- Preview QA: `/Volumes/Extreme/_edit_work/ro01/revision9/review-electronic/first-minute-QA.json` and `music-options.json`. All four second-set files have identical picture and voice, -14.2 LUFS and -1.7 dBFS true peak. The R8 versus R9 voice waveform correlation over 14 to 34 seconds is 0.99916 with about 0.22 dB gain difference. R9 generation cost was $0.

## Protected picture decisions

- R3 reference master: `/Volumes/Extreme/_edit_work/ro01/RO01_MASTER_R3.mp4`, SHA256 `17f666fc1a54f078768f6bef902ee22219f46b92681da627bbf0c68ab27a6f4f`. Keep its approved presenter color and voice treatment. Its music is rejected. `PICTURE_CLEAN.mp4` has baked old graphics, so rebuild affected sections from the correct sources.
- Approved R8 first-minute picture: `/Volumes/Extreme/_edit_work/ro01/revision8/review/RO01_R8_first_minute_H04.mp4`, SHA256 `0b5f65e663d143dee5074683c7bc2b78436600cfa12b86b00e12c6ed690232d5`. Keep H04, presenter cuts, G01, S01, G03, color, framing and J01. Its audio contains rejected music.
- H04 opener motion: `revision7/motion/H04-kling25-a1.mp4`, SHA256 `d14edee82ec4045bae1638f7a9ce0d5f4e597e1f140a10c57c13f892ff895572`. Approved B01 motion: `revision7/motion/B01-kling25-a1.mp4`, SHA256 `e9e65e10ba47f175af6bec602a9507ed7b454d9bba039bf525ca3fe690611b93`. Both paths are under `/Volumes/Extreme/_edit_work/ro01/`. H06 stays out.
- Preserve all 23 exact approved R4 items from `/Volumes/Extreme/_edit_work/ro01/revision5-plan/decisions.json`, SHA256 `8c34b785ab2ae40eb6c489aa0d7baa6548bb4c15ebdf994d495d0494d6ed4f15`: G01, S01, G03, J01, G04, G06, D01, G10, G11, G14, D02, G17, B03, G20, G22, B04, B05, G26, B06, S02, G36, G44 and B07. Verify the locked asset hashes before assembly.
- Apply J01's five-frame cut once, removing R3 57.671333 to 57.838167 seconds. Keep the complete spoken words "forever" and "Now". B02 remains removed. Fill its former R3 190.7897 to 198.4897 second slot with clean graded presenter footage and preserved narration.

## Next action and finish line

1. Verify the chosen B preview and source hashes, the 23 R4 decisions, H04/B01 and the source map. Read the earlier R8 and R9 handoffs for their implementation history. Use the chosen preview as the first-minute audiovisual reference and preserve already approved work.
2. Build the complete 1920x1080 film with the selected `Werq` music and R3 voice/color. Keep the approved picture, apply the J01 cut once, keep H06 out and B02 removed, and avoid placeholder assets. Check music loops, speech gaps, transitions and the ending.
3. Regenerate SRT and YouTube chapters from the actual final timeline. Run the exact-file picture, audio and subtitle gates, inspect every join, and watch the whole candidate in order with sound. Obtain one independent full-candidate review. Fix actual failures and recheck affected gates.
4. Deliver the complete film, SRT, chapters, hashes, gate stamps, review evidence and provider cost record for Dan's final review. No thumbnails, upload, publishing, app deployment or dispatcher resume in this task.

This is CONTENT LFC. Do not make a full vertical, square or one-minute ad-style cut. Shorts are a separate later job.

## Ready-to-paste starter prompt

Name this task **Keep Your Muscle LFC R9**. Execute `Handoffs/handoff-20261005-ro01-r9-bright-electronic-final-film.md` with `/longform-edit`. This is CONTENT, RO-01 LFC. I approved the R8 first-minute picture and selected **Bright Electronic**, option B from the second R9 music review. The chosen preview is `/Volumes/Extreme/_edit_work/ro01/revision9/review-electronic/RO01_R9_B_werq_first_minute.mp4`. Use its `Werq` bed and same voice/picture treatment through the full 16:9 film. Keep H04, B01, all 23 approved R4 items, R3 color and voice, and the J01 cut. Keep H06 out and B02 removed. Finish, gate and review the complete film with SRT and chapters, then show it to me for final review. Do not reopen the music choice or publish, upload, deploy, make ad formats or resume the dispatcher.
