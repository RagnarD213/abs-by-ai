#!/usr/bin/env bash
# URL-preservation gate for the sixpackabs.com redesign.
#
#   sixpackabs/url-check.sh <base-url> [baseline-file]
#
# Requests every URL in the baseline (every <loc> in production's post, page,
# mailpoet_page, category and author sitemaps on 2026-09-10) with the host
# swapped to <base-url>, WITHOUT following redirects, and requires HTTP 200.
# Any other status blocks the launch. Exit 0 = all 200.
#
#   sixpackabs/url-check.sh https://sixpackabs.com                  # production
#   sixpackabs/url-check.sh https://<staging>.wpcomstaging.com      # staging
set -uo pipefail

BASE="${1:?usage: url-check.sh <base-url> [baseline-file]}"
BASE="${BASE%/}"
HERE="$(cd "$(dirname "$0")" && pwd)"
BASELINE="${2:-$(ls "$HERE"/url-baseline-*.txt | sort | tail -1)}"
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36 spa-url-check'
OUT="$(mktemp -t spa-urlcheck.XXXXXX)"

sed -E "s#^https?://[^/]+#$BASE#" "$BASELINE" | grep -v '^$' \
	| xargs -P 8 -I{} sh -c 'code=$(curl -s -o /dev/null -A "$1" --max-time 30 -w "%{http_code} %{redirect_url}" "$2"); echo "$code $2"' _ "$UA" {} > "$OUT"

TOTAL=$(wc -l < "$OUT" | tr -d ' ')
OK=$(awk '$1 == 200' "$OUT" | wc -l | tr -d ' ')
echo "baseline: $BASELINE"
echo "target:   $BASE"
echo "checked:  $TOTAL   200: $OK   other: $((TOTAL - OK))"
if [ "$OK" != "$TOTAL" ]; then
	echo "--- non-200 (status redirect url) ---"
	awk '$1 != 200' "$OUT" | sort
	rm -f "$OUT"
	exit 1
fi
rm -f "$OUT"
echo "PASS — every baseline URL answers 200 with no redirect."
