# Gemini CLI install receipt, 2026-11-17 (DONE, using Antigravity `agy`)

Handoff: `Handoffs/handoff-20261117-install-gemini-cli-both-macs.md`. Run by Claude. Dan approved the switch to Antigravity in chat after the first attempt was blocked.

## Result
Both Macs answer text, still and video prompts through `.claude/skills/_shared/gemini-cli/gemini.sh`, signed in with Dan's Google account (danroseconsulting@gmail.com) on the subscription login, with `GEMINI_API_KEY` unset and paid-key mode refused by the wrapper. Wrapper and README are on GitHub `main` (commit `ff04b7d`); the M2 checkout received them through `checkout-sync.py`.

## What changed from the handoff
`@google/gemini-cli` 0.68.0 (latest) installed on both Macs and signed in on the M6, but every call fails with `IneligibleTierError: UNSUPPORTED_CLIENT` (personal Google accounts are refused; Google points to Antigravity). So the working tool is Google's **Antigravity CLI `agy` 1.5.10** (`~/.local/bin/agy`, both Macs, installed from Google's official script, checksum verified). The `gemini` binaries stay installed but unused. The M6 installer appended a PATH line to `~/.zshrc`; the M2's was not added (the wrapper does not need it).

## Sign-in
- M6: Google OAuth, browser flow approved in Dan's Chrome. M2: same, over SSH with the printed URL and code (headless keychain worked for later non-interactive calls).
- Plan limits (`agy -p "/usage"`): separate weekly and five-hour limits for "Gemini Models" and "Claude and GPT models", 100% and 99% at first check.

## Smoke tests (wrapper, project folder, outputs in `tmp/gemini-cli-smoke-<mac>/`)
| | M6 | M2 |
|---|---|---|
| text ("READY and the model name") | OK, 21 s, "READY, Gemini 4 Carbon" | OK, 14 s, same |
| still (frame from the 20 s app video) | OK, 22 s | OK, 29 s |
| video (20 s 1080x1920 `public/ad-assets/app-supplement-audit-results_20s_1080x1920_muted.mp4`, timestamped list) | OK, 60 s, accurate list | OK, 71 s |

The still on the M6 used a frame of the RA-16 review film (outdoor pool shot). The video is a finished 1080x1920 asset, not a review film (no 1080p review short was handy).

## Things that went wrong and the fixes
- First wrapper used `--mode plan`; the agent then wrote a plan file instead of answering. Removed; the prompt is prefixed to answer only and not touch files.
- Default model with no `-m` is Gemini 4 Carbon (medium). Not frozen; see `agy models`.

## Not done
Wiring Gemini into review checks or clip-library logging (next step, per the handoff).
