# Handoff: point the dead Test Reload link on sixpackabs.com at Great Again T

Date: 2026-11-13. Type: site configuration (not a video). Recommended: Codex, newest Sol, medium effort (Codex owns the open Google Ads appeal this waits on). Grokbot can run it from the starter prompt below.

## HOLD: do not run yet

Run this only after Google resolves the compromised-site appeal 61736603 on campaign `24453238073` (state and next action: `Docs/SIXPACKABS_AD_POLICY_INVESTIGATION_20261110.md`, `Docs/SIXPACKABS_TEXT_COMPLIANCE_CLEANUP_20261110.md`). The evidence sent to Google says the site has canonical redirects only and that no WPCode snippet contains an external redirect. A new redirect to another host while that appeal is open would contradict it. The traffic at stake is small, so waiting costs almost nothing.

## Goal

Visitors who click an old Test Reload link land on the Great Again T product page instead of a "not found" page.

## Facts (checked 2026-11-13)

- The old YouTube channel "SixPackAbs.com" (handle @sixpackshortcuts, 4.46M subscribers, 695 videos, owned by the 2019 buyers, no upload since July 2022) still links to URLs on sixpackabs.com, a domain Dan owns. Its profile link `sixpackabs.com/pages/green-detox` already lands on Dan's greens page through WordPress's automatic slug guess.
- `https://sixpackabs.com/pages/test-reload` returns 404.
- Great Again T product page: `https://shop.sixpackabs.com/products/great-again-t`.
- TEST RELOAD is a live registered trademark of another company (Reg. 5391063). Use a silent redirect only. Do not publish a page that shows the words Test Reload or says it became Great Again T.
- `sixpackabs/deploy.sh check prod` found no production SSH user in `~/.absbyai-secrets.env` on 2026-11-13, so wp-admin is the likely route.

## The step

1. Confirm the appeal is resolved and re-read `AI_COORDINATION.md` from disk.
2. Add a 302 redirect from `/pages/test-reload` (with and without the trailing slash) to `https://shop.sixpackabs.com/products/great-again-t?utm_source=youtube&utm_medium=old-channel&utm_campaign=test-reload-link`. Use the smallest method available: a redirect entry, or one small PHP snippet on `template_redirect`. Keep a copy of any snippet under `sixpackabs/`.
3. When the Great Again T sales video page exists, switch the target to it.
4. Optional sweep: list the links in the old channel's video descriptions with the YouTube Data API, test each sixpackabs.com URL, and redirect other dead supplement URLs the same way. Count them first and skip the sweep if there are only a few.

## Verify

- `curl -sIL -A "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)" https://sixpackabs.com/pages/test-reload` shows a 302 and then a 200 on the shop page.
- `sixpackabs/url-check.sh https://sixpackabs.com` still passes 219 of 219.
- Record the redirect in `Docs/SIXPACKABS_SITE.md` and push it with `scripts/git/safe-push.sh`.

Done means the old link lands on the Great Again T product page on a phone, the baseline URL check still passes, and the site doc records it.

## Starter prompt

Read `Handoffs/handoff-20261113-sixpackabs-test-reload-redirect.md` in the Abs By AI project and run it. First confirm Google has resolved the compromised-site appeal on sixpackabs.com; if it has not, stop and say so. Dan has authorized site changes on sixpackabs.com (standing authorization in `AGENTS.md`), so do the whole step without asking him.
