# Two-Mac setup: M6 primary, M2 headless edit machine (2026-11-12)

Category: ops (not a video). Dan asked for this plan on 2026-11-12. Handoff 01 was partly executed on November 13; all requested settings were applied, but actual SMB access to the external drives fails. See [the 01 receipt](../../Docs/TWO_MAC_M2_PREP_RECEIPT_20261112.md). Handoff 02 was executed on November 13 (M6 account is `danrrose`, aliased as `/Users/danielrose`); see [the 02 receipt](../../Docs/TWO_MAC_M6_SETUP_RECEIPT_20261113.md). Handoff 03 is unexecuted.

## Goal

- **M6 Mac mini** = Dan's daily driver. Holds the one project folder, all AI apps, his personal work, and one or two video edits.
- **M2 Pro Mac mini** (32 GB, 10 cores, today's machine, computer name `Mac-mini`) = headless edit machine, joined to the M6 by a Thunderbolt cable. Takes video edits when the M6 is busy. Keeps the Extreme and Seagate (Expansion) drives and the nightly footage routine.

## Decisions already made (do not reopen; Dan can change them)

1. **No Migration Assistant.** The M2's internal drive is 837 GB full (183 GB of in-progress edit work, 20+ stale review LaunchAgents). Copy only what is needed, over the cable.
2. **Same account name on the M6: `danielrose`.** Every script and path then works unchanged.
3. **One project folder, on the M6** (`~/Projects/Claude`). The M2 reaches it through the cable at the same path. No second checkout to drift. Fallback if git over the share is too slow: see file 03.
4. **Drives stay on the M2.** The M6 mounts them over the cable at the same names (`/Volumes/Extreme`, `/Volumes/Expansion`). The nightly footage routine and Seagate checksum rules stay as they are.
5. **Edits in progress on the M2 finish on the M2.** Their work folders (`~/Projects/_edit_work`, 183 GB) do not move.
6. **Link addresses:** M6 `10.66.0.1`, M2 `10.66.0.2`, on the Thunderbolt Bridge. SSH names `m6` and `m2`.
7. **Edit slots: M6 2, M2 3** (total stays 5). Routing rules in file 03.

## The three handoffs, in order

| # | File | Runs on | Who | When |
|---|---|---|---|---|
| 1 | `01-m2-prep-codex-grokbot.md` | M2 | Codex newest Sol, medium (or Grokbot) | Now, before unboxing |
| 2 | `02-m6-setup.md` | M6 | Claude Opus 5.5, high | After Dan's first-boot steps on the M6 |
| 3 | `03-two-mac-edit-routing.md` | M6 | Claude Fable 5.2, high | After 2 is verified |

## Starter prompts (copy from here on the new Mac)

**02, Claude on the M6 (Opus 5.5, high):**

```
This is Dan's brand-new M6 Mac mini. Fetch and read these two files, then do everything in the second one: https://raw.githubusercontent.com/RagnarD213/abs-by-ai/main/Handoffs/two-mac-setup-20261112/README.md and https://raw.githubusercontent.com/RagnarD213/abs-by-ai/main/Handoffs/two-mac-setup-20261112/02-m6-setup.md. The old Mac (M2) is on the Thunderbolt cable at 10.66.0.2 and has everything. Do every step yourself; I only type passwords and sign in. Tell me in plain words exactly when you need me.
```

**03, Claude on the M6 (Fable 5.2, high), task name "Two-Mac Edit Routing":**

```
Read Handoffs/two-mac-setup-20261112/README.md and 03-two-mac-edit-routing.md and build it all: the routing rules, the link to the M2, review pages that open on this Mac, and the real test on one short. Handoff 02 is done and verified.
```

## Inventory of the M2 taken 2026-11-12 (source for file 02)

- Apps in `/Applications`: Claude, ChatGPT (holds Codex), Gemini, Grok Bot, Comet, Manus Studio, Cursor, Wispr Flow, Google Chrome, Brave, Firefox, Edge, Opera, Safari, Descript, Slack, zoom.us, Telegram, Skype, Teams classic, Thunderbird, Google Ads Editor, Android Studio, Xcode, iMazing, Adobe Acrobat DC + Reader + Creative Cloud, GIMP, VLC, Shottr, Cinch, The Unarchiver, Grammarly Editor, NordVPN, AnyDesk, Onigiri, CopyMyData, PhoneRescue, Steam, PokerStars, Keynote/Numbers/Pages/GarageBand/iMovie, printer software (Brother, Epson, HP). `~/Applications`: Civilization VI, Trader Workstation.
- Command line: node/npm in `/usr/local/bin`, `~/.local/bin/claude`, `~/bin` (rclone, yt-dlp, claude-cleanup.sh), `~/.npm-global` (railway, shopify, hyperframes), `~/.venvs/voice-pilot`, Homebrew with only `smartmontools`. ffmpeg is not on the PATH; find the copy the skills call before assuming.
- Sizes: `~/Projects/Claude` 101 GB, `~/Projects/Codex` 12 GB, `~/.claude` 56 GB, `~/.codex` 72 GB.
- Private state in the home folder (never into the repo, which is public): `.absbyai*`, `.srm-secrets.env`, `.env.local`, `.railway`, `.appstoreconnect`, `.config`, `.gemini`, `.grokbot`, `.hyperframes`, `.twc`, `.vercel`, `.android`, `.npmrc`, `.zshrc`, `.gitignore`, `.claude.json`.
- LaunchAgents worth keeping: `com.absbyai.nightly-footage` (stays on M2), `com.absbyai.review-hub`, `com.absbyai.edit-queue*`, `com.absbyai.fb-reel-covers`, `com.danrose.claude-cleanup`. The `com.absbyai.review.*` / `ro0*` ones are stale review pages.
- 45 Claude scheduled tasks in `~/.claude/scheduled-tasks` plus 3 in `~/Projects/Claude/Scheduled`. They must run on exactly one Mac (the M6) after the move.
