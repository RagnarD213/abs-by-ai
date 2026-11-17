# Gemini CLI install receipt, 2026-11-17 (INCOMPLETE: blocked)

Handoff: `Handoffs/handoff-20261117-install-gemini-cli-both-macs.md`. Owner of this run: Claude.

## What was done
- `@google/gemini-cli` 0.68.0 (the latest npm release) installed on the M6 (`~/.npm-global/bin/gemini`) and the M2 (`~/.npm-global/bin/gemini`). On the M2 `gemini` is not on the PATH of a plain `ssh m2` shell; a wrapper must add `~/.npm-global/bin` and `/usr/local/bin`.
- M6 signed in with "Login with Google" as Dan's gmail account (oauth files written in `~/.gemini/`, mode 0600). **Not signed in on the M2** (pointless, see below).

## What failed
Every request through the signed-in CLI fails with `IneligibleTierError: UNSUPPORTED_CLIENT` ("This client is no longer supported for Gemini Code Assist for individuals ... migrate to the Antigravity suite", `https://antigravity.google`). 0.68.0 is the newest release, so a personal Google login cannot run `gemini -p` at all. The subscription route for this tool is closed. No text, still or video smoke test could run, and no wrapper was written.

## Options found (none taken without Dan)
1. **Antigravity CLI (`agy`)**, Google's official replacement, with `agy -p`, `--output-format json`, ACP. I installed it on the M6 from Google's official script (`curl -fsSL https://antigravity.google/cli/install.sh | bash`, checksum verified): `agy` 1.5.10 at `~/.local/bin/agy`; the installer appended a PATH line to `~/.zshrc`. I stopped at its Google sign-in approval (the automatic permission check blocked clicking Allow, because the handoff authorized the Gemini CLI, not Antigravity). Not installed on the M2. Whether it bills against Dan's Google AI subscription is unconfirmed.
2. **Gemini CLI with `GEMINI_API_KEY`** (metered API). The handoff forbids making this the default or switching to it silently.

## Next step
Dan chooses 1 or 2. For 1: approve the Antigravity sign-in, then repeat the M2 install and sign-in (`agy` prints a URL and code flow over SSH), write `gemini-cli/` wrapper around `agy -p`, run the three smoke tests on both Macs, push. Leftovers to remove if option 1 is rejected: `~/.local/bin/agy`, `~/.gemini/antigravity-cli`, the PATH line in `~/.zshrc`, the M6 `~/.gemini/oauth_creds.json`.
