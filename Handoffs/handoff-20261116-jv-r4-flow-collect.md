# Joint Vigor VSL R4: collect the AI clips from Flow (Codex or Grokbot)

Category: AD (client VSL, Goldenroots Naturals). Job SRM-JV-R4. Written 2026-11-16 by Claude (Opus 5.5), the editor.

**Dan's authorization:** Dan asked for this edit and set the rule that any step Claude can't do goes to Codex and Grokbot. Do the whole step without asking him. It needs no spend: the clips are already generated on Dan's Google AI subscription.

## Blocked step
Claude's Chrome stopped saving any downloads from flow.google.com after 15:23 today, probably because of Chrome's "automatic downloads" block. Flow says "downloaded", but nothing reaches ~/Downloads.

## Do
1. **Unblock Chrome downloads.** In Dan's Chrome on the M6, open Site settings for flow.google.com and set Automatic downloads to Allow. If that is not possible, use your own browser signed in to Dan's Google account.
2. **Download the chosen takes.** Open the Flow project "SRM-JV-R4 AI clips" (https://flow.google.com/project/27c372ba-6b32-4b88-ac41-2904cbaf0e03). For each need listed in `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/ai/INDEX.json`, download its start frame and every take at full resolution, as MP4 / PNG.
3. **Save them.** Put each file in `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/claude-r4/ai/<id>/incoming/`, using the take name INDEX.json gives. Check each file with ffprobe.
4. **Hand back.** Write `ai/COLLECTED.json` listing each file, its size and its SHA-256. Claude's AI-clips agent then gates, reviews and files them.

Do not judge or edit the clips. Do not send anything to the client.
