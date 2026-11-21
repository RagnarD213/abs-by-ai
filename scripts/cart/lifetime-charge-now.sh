#!/bin/sh
# Run one buyer's Lifetime charge NOW instead of on day 7, for Dan's live card
# test of the web cart (Handoffs/handoff-20261002-cart-build.md, step 7).
# It calls POST /api/admin/lifetime/charge-now on production with the dashboard
# key from ~/.absbyai-secrets.env. It only charges a Lifetime checkout that is
# still waiting for its charge, and a second run charges nothing.
#
#   scripts/cart/lifetime-charge-now.sh you@example.com
set -e
EMAIL="$1"
case "$EMAIL" in
  *@*.*) ;;
  *) echo "Usage: $0 <the email used at checkout>"; exit 1 ;;
esac
case "$EMAIL" in
  *[\"\\\ ]*) echo "That email has characters this script does not send."; exit 1 ;;
esac
KEY="$(grep '^DASH_SECRET=' "$HOME/.absbyai-secrets.env" | cut -d= -f2- | tr -d '"')"
[ -n "$KEY" ] || { echo "DASH_SECRET is missing from ~/.absbyai-secrets.env"; exit 1; }
curl -sS -X POST "https://abs-by-ai-production.up.railway.app/api/admin/lifetime/charge-now" \
  -H "Content-Type: application/json" -H "X-Dash-Key: $KEY" \
  --data "{\"email\":\"$EMAIL\"}"
echo
