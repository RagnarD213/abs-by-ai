# Gemini from the command line (both Macs)

Claude and Codex can hand a job to Gemini the way Claude starts Codex. It runs on **Dan's Google AI subscription**
(Google-first rule, 2026-11-08), never the metered `GEMINI_API_KEY`. Built 2026-11-17.

## Why `agy`, not `gemini`
Google's `gemini` CLI (`@google/gemini-cli` 0.68.0, the latest) now refuses personal Google accounts:
`IneligibleTierError: UNSUPPORTED_CLIENT ... migrate to the Antigravity suite`. Google's replacement is the
**Antigravity CLI, `agy`** (installed at `~/.local/bin/agy` on both Macs, version 1.5.10 on 2026-11-17, from
`curl -fsSL https://antigravity.google/cli/install.sh | bash`). Signed in with danroseconsulting@gmail.com on both.
The old `gemini` binary is also installed (`~/.npm-global/bin/gemini`) but is useless; ignore it.

## Call it
```bash
.claude/skills/_shared/gemini-cli/gemini.sh [-o OUT.txt] [-m MODEL] [-f FILE]... "prompt"
```
- `-f` attaches an image (png jpg gif webp bmp tiff svg) or video (mp4 mov webm avi); repeat for several.
  The wrapper adds `@/abs/path` to the prompt and `--add-dir` for the folder.
- `-o OUT.txt` writes the answer there and the raw JSON envelope to `OUT.txt.json` (status, duration, tokens).
  Without `-o` the answer prints on stdout.
- Runs from the project folder, with the API keys unset, headless (`agy -p --output-format json`). The prompt
  is prefixed so the agent only answers (no files or plans). Plan mode is NOT used: it makes `agy` write a
  plan document instead of answering.
- Exit codes: 0 ok, 2 bad usage, **3 quota or rate limit**, 4 not signed in, 5 `agy` missing or paid-key mode on, 1 other.
- A quota exit means wait for the reset or fall back to another model/AI. **Never switch to the paid key silently.**
- On the M2 it works over plain `ssh m2 '<project>/.claude/skills/_shared/gemini-cli/gemini.sh ...'` (no PATH
  setup needed, the wrapper finds `~/.local/bin/agy`).

## Models and quota (observed 2026-11-17)
- `agy models` lists the current ids; do not freeze one. On 2026-11-17: Gemini 4 Carbon/Argon/Hydrogen
  (low/medium/high, Hydrogen also xhigh), Gemini 3.8 Flash, plus Claude and GPT models on the same subscription.
  Default with no `-m` is **Gemini 4 Carbon (medium)**. `-m gemini-4-carbon-high` etc. to change.
- Plan limits, from `agy -p "/usage"`: separate **weekly** and **five-hour** limits for "Gemini Models" and for
  "Claude and GPT models" (all ~100% at first check). Run that command to see the live percentages and reset times.
- Speed: text answer 5 to 20 s, still 22 s, 20 s 1080x1920 video 23 to 60 s (M6).

## Sign-in
`agy` keeps the login in the macOS keychain. If the wrapper exits 4, sign in again: run `agy` in an interactive
terminal, choose **1. Google OAuth**, open the printed URL in Dan's Chrome, pick danroseconsulting@gmail.com,
click Sign in, paste the code. Over SSH it prints the URL and code prompt automatically. Never put token or
credential files in the repo.

## Full agent mode (whole jobs, not one answer), checked on the M6 2026-11-27
`gemini.sh` only asks a question and forbids file changes. To give Gemini a whole job, start `agy` itself from the
project folder: `agy --model <id> --dangerously-skip-permissions -i "<brief>"` (interactive, Dan can answer a stop),
or `-p` for an unattended run. Checked headless on the M6 (agy 1.5.18): it writes files, can read
`~/.absbyai-secrets.env`, runs `~/bin/rclone`, and its built-in image generator returns a 768x1376 PNG for 9:16.
- It wrote its files into the `--add-dir` folder, not the folder it was started in. Give absolute paths.
- `agy mcp list` is empty: no Blotato, Upwork, WordPress or Gmail connectors. Use project scripts and REST, or add a
  server with `agy mcp add`.
- `agy models` also lists Claude Opus 5.5 and Sonnet 5.5 on a separate "Claude and GPT models" allowance (100% unused
  on 2026-11-27). Its size per job is not measured yet.
- Gemini Desktop Task Mode is a different surface: writes into `Handoffs/` were denied there and the keys sit outside
  its connected folders. Use `agy` for anything that writes to the repo or needs keys.

First whole-job trials: `Docs/AGY_CHROMA_TEST_20261124.md` (edit) and the two setup tests in `Handoffs/` dated 2026-11-27.
