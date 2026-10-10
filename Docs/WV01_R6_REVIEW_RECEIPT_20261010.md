AD: Fired Them All AD R6

# R6 (Version B at 1.2x) review receipt, 2026-10-10

R6 is a separate uniform 1.2x copy of the finalized R5 film. R5 and its captions are untouched. No website upload, test software choice or test launch was done.

## Files

- Film: `Website Videos/WV-01 Version B/Fired Them All AD R6 - Version B 1.2x 1080p.mp4` (copy in `Videos to Review/`), plus `.srt` and `.vtt`. SHA256 `83519c7af2cb4cbf3192f900a40d902398aed8c1bcf5b96279140536fbaa8bec`.
- 21,493 frames, 1920x1080, 30000/1001, 11:57.150. Source R5 hash `903eca4c...` verified before and after.
- Heavy work, recipes and evidence: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/speed-1p2/` (`review/` holds every report).

## Method

Picture `setpts=PTS/1.2` at 30000/1001. Audio is the accepted R5 PCM with `atempo=1.2`, encoded once to AAC and muxed with the stream-copied picture. A first pass that sped the already-AAC audio again failed the exact-reference audio row (waveform no longer matched the retimed PCM) and was replaced; its video stream is byte-identical to the final one. Captions: 273 cues each, every start and end is the R5 value divided by 1.2, text identical.

## Results

- Audio gate PASS: correlation 0.9998 to the retimed accepted PCM, level within 0.11 dB every second, -14.40 LUFS, true peak -2.00 dBTP. Pitch ratio median 1.000 (middle 80 percent 0.989 to 1.014) over 1,314 voiced windows.
- Full decode clean. Every one of 21,493 frames decodes at 1920x1080 and matches an R5 frame at no more than 0.21/255 mean error. No black frames. Every frozen run sits on an R5 frozen run.
- Fresh ASR: all narration present in order; ending reads "I have never felt better in my life. You've been doing this alone long enough, so tap the button below..." and the last words are "I'll see you inside." Missing words in base.en output were rechecked with medium.en and are ASR misses.
- Phone scene 3:49.34 to 3:51.84 matches the independent approved `P04-lock.mp4` (hash `87ae103e...`): hand-held phone, goal photo, label, moving.
- Six callbacks: every entry and exit is a distinct wide/tight change. P6 tight shot 11:47.340 to 11:49.275, then the full closing card to the end. "Life" ends 11:47.24, before P6.
- Six frozen runs disposed by editor and by the independent judge: all approved static photo holds.
- Independent reviews: one Gemini full-film review (2 fps plus dense phone and ending contexts): no speed-induced defect, tempo fast but intelligible, text readable (shortest card 2.5 s). One fresh Opus 5.5 judge opened all 12 sheets and all 186 strips: 187 clean, 8 expected, 3 new inherited defects. Pair images were mapped from their strips by the editor. This is not continuous playback.

## Inherited findings (all present in R5, none caused by the speed change)

5:25.6 same-crop pose reset (known); 11:40 overhead forearm crop (known); newly reported by the judge, each confirmed identical in R5: 7:25.7 (R5 8:54.8), 10:46.6 (R5 12:55.9), 11:46.4 (R5 14:07.7, head snap during "never felt better").

## Website gate (exact file, strict): FAIL, 32 passed, 7 failed

`cut:min_segment`, `cut:jump_cut`, `cut:splice_visibility` (3 joins versus 16 in R5), `captions:burned`, `watch:pass` (open inherited defects) are R5's failures carried over. `junk:dead_air` now passes only because the 1.16 s pause shortens to 0.96 s. New at 1.2x: `audio:click_at_joins` (the file's own ceiling fell from 0.31 to 0.20; the flagged join at 10:12.67 has the same waveform step as R5, no new pop) and `framing:headroom` (two holds at 25 and 29 normalized px against a 30 minimum; frames inspected, ample space, hair-top row passes at 24 px minimum). No threshold or waiver changed.

## Spend

No generation. One Gemini review, estimated $0.329614 (announced about $0.85); cumulative known Gemini QC estimate across R5 and R6 is $1.223702 (cap $5), recorded in `review/accounting/spend.json`.

## Next

Dan reviews R6 in VLC. Website setup and split test follow `Handoffs/handoff-20261010-wv01-b-claude-1p2x-then-website-test.md` and the separate test plan.
