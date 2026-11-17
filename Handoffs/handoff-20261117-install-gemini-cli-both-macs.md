# Install the Gemini command-line tool on both Macs (2026-11-17)

**Type:** ops (no video edit, no edit slot needed). **Owner:** Codex, newest GPT Sol (GPT-6.2 Sol as of today), Medium.
**Authorization:** Dan asked for this on 2026-11-17. Do every step without asking. Installing, signing in with Dan's
Google account, writing the wrapper and pushing it are all authorized.

## Goal

Claude and Codex can hand a job to Gemini from the command line on either Mac, the same way Claude already starts
Codex, so first-pass video checks, footage logging and research stop using Claude and Codex allowance. It runs on
Dan's **Google AI subscription** (the Google-first rule, 2026-11-08), not the paid API key.

## What is true now (checked 2026-11-17)

| | M6 (Dan's Mac, user `danrrose`) | M2 Pro (headless, `ssh m2`, user `danielrose`) |
|---|---|---|
| `gemini` | not installed | not installed |
| Node / npm | v24.16.0 at `~/.local/node/bin` | v24.16.0 at `/usr/local/bin` |
| `~/.gemini` | exists (`tasks`, `users` only; no sign-in) | exists (same) |
| Project folder | `~/Projects/Claude/Projects/Abs By AI` | `~/Projects/Claude/Projects/Abs By AI` |

`GEMINI_API_KEY` is in `~/.absbyai-secrets.env` on the M6. That is the **metered** key; do not make it the
default. The M6 disk is nearly full (see the internal-drive cleanup handoffs): the install is small, but check
`df -h ~` first and do not leave caches behind.

## Steps

1. **Install on the M6:** `npm install -g @google/gemini-cli` with the M6's npm (global prefix under the user, no
   sudo). Confirm `gemini --version`, record it, and make sure `gemini` is on PATH for non-interactive shells
   (`zsh -lc 'which gemini'`) and for Codex/Claude Bash calls.
2. **Sign in with the subscription on the M6:** run `gemini` once and choose **Login with Google** using Dan's
   Google account that holds the Google AI subscription (the one Flow uses). If the browser asks for an Allow
   click, drive it in Dan's Chrome. Then make sure the API key does not take over: the wrapper in step 5 runs
   with `GEMINI_API_KEY` and `GOOGLE_API_KEY` unset. Check which plan/quota the CLI says it is using and record it.
3. **Install on the M2:** same npm install over `ssh m2`. Confirm `ssh m2 'zsh -lc "which gemini; gemini --version"'`.
4. **Sign in on the M2 (headless):** copy the M6's sign-in files (`~/.gemini/oauth_creds.json`, `google_accounts.json`,
   `settings.json`, whatever the installed version writes) to the M2's `~/.gemini/`, mode 0600. If the copied login
   is refused, use the CLI's no-browser login flow on the M2 and finish the approval in Dan's Chrome on the M6.
   Never put these files in the repo.
5. **Write the shared wrapper** `.claude/skills/_shared/gemini-cli/gemini.sh` (works on both Macs, finds the right
   `gemini`, unsets the API keys, runs non-interactive `gemini -p`, accepts file paths to attach, writes output
   to a file, exits non-zero on quota or sign-in errors) and a short `README.md` beside it: how to call it, the
   newest model to use (check what the CLI offers; do not freeze a model number), the quota you observed, and
   that a quota error means fall back or wait, not switch to the paid key silently.
6. **Smoke test on both Macs** through the wrapper, `cd` into the project folder:
   - text: "Reply with the word READY and the model name you are."
   - a still: one frame from any finished review film on that Mac.
   - a short video: a finished 1080p Short under 60 seconds; ask for a timestamped list of what is on screen.
   Save the outputs under `tmp/gemini-cli-smoke-<mac>/` and note how long each took.
7. **Push** the wrapper and README with
   `scripts/git/safe-push.sh -m "Add shared Gemini CLI wrapper" -- .claude/skills/_shared/gemini-cli/` (from the M6
   project folder; if it stops on stale files, re-run with `--adopt-stale`). Confirm the M2 checkout gets it on
   its next sync (`scripts/two-mac/checkout-sync.py --status`) or pull it there.
8. **Close out:** write `Docs/GEMINI_CLI_INSTALL_RECEIPT_20261117.md` (versions, sign-in type and plan on each Mac,
   smoke test results and times, anything that failed), push it, and remove this handoff's line from the OPEN section
   of `Handoffs/README.md`.

## Done means

`gemini.sh` answers the text, still and video smoke tests on **both** Macs using the subscription login, not the
API key; the wrapper and README are on GitHub `main`; the receipt is written. If one Mac cannot sign in, the job
stays explicitly incomplete with the exact error and the next step in the receipt.

## Not in this job

Wiring Gemini into the review or footage-logging workflows. That is the next step (first-look checks on review
cuts, then clip-library logging), done only after this install is verified.
