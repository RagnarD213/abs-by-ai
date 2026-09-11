#!/usr/bin/env bash
# Deploy (or roll back) the sixpackabs-child theme on WordPress.com over SSH.
#
#   sixpackabs/deploy.sh staging            upload + activate + flush rewrites + run the sync
#   sixpackabs/deploy.sh prod               same, on sixpackabs.com (only on Dan's go)
#   sixpackabs/deploy.sh staging --upload-only   copy the files, leave the active theme alone
#   sixpackabs/deploy.sh rollback staging|prod   re-activate Twenty Twenty-Five (one step;
#                                                the July template overrides come back untouched)
#   sixpackabs/deploy.sh check staging|prod      connect, print WordPress/theme info, change nothing
#
# Credentials come from ~/.absbyai-secrets.env (never from this repo):
#   SPA_SSH_HOST (default sftp.wp.com)  SPA_SSH_PORT (default 22)
#   SPA_SSH_USER / SPA_SSH_PASS                  production
#   SPA_STAGING_SSH_USER / SPA_STAGING_SSH_PASS  staging
#   SPA_SSH_KEY  optional private-key path instead of passwords
# Password auth goes through SSH_ASKPASS, so no sshpass is needed. Idempotent.
set -euo pipefail

SECRETS="$HOME/.absbyai-secrets.env"
HERE="$(cd "$(dirname "$0")" && pwd)"
THEME_SRC="$HERE/theme/sixpackabs-child"

usage() { sed -n '2,19p' "$0"; exit 2; }
get() { [ -f "$SECRETS" ] && grep -E "^$1=" "$SECRETS" | tail -1 | cut -d= -f2- | sed -E 's/^"//; s/"$//' || true; }

ACTION="deploy"
case "${1:-}" in
	rollback|check) ACTION="$1"; shift ;;
esac
TARGET="${1:-}"
UPLOAD_ONLY=0
[ "${2:-}" = "--upload-only" ] && UPLOAD_ONLY=1
case "$TARGET" in staging|prod) ;; *) usage ;; esac

HOST="$(get SPA_SSH_HOST)"; HOST="${HOST:-sftp.wp.com}"
PORT="$(get SPA_SSH_PORT)"; PORT="${PORT:-22}"
KEY="$(get SPA_SSH_KEY)"
if [ "$TARGET" = prod ]; then
	SSH_USER="$(get SPA_SSH_USER)"; SSH_PASS="$(get SPA_SSH_PASS)"
else
	SSH_USER="$(get SPA_STAGING_SSH_USER)"; SSH_PASS="$(get SPA_STAGING_SSH_PASS)"
fi
if [ -z "$SSH_USER" ]; then
	echo "No SSH user for '$TARGET' in $SECRETS (expected ${TARGET/prod/SPA}_…_USER — see header)." >&2
	exit 1
fi

ASKPASS="$(mktemp -t spa-askpass.XXXXXX)"
trap 'rm -f "$ASKPASS"' EXIT
printf '#!/bin/sh\nprintf "%%s\\n" "$SPA_SSH_SECRET"\n' > "$ASKPASS"
chmod 700 "$ASKPASS"
export SPA_SSH_SECRET="$SSH_PASS" SSH_ASKPASS="$ASKPASS" SSH_ASKPASS_REQUIRE=force DISPLAY="${DISPLAY:-:0}"

SSH_OPTS=(-p "$PORT" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -o NumberOfPasswordPrompts=1 -o ServerAliveInterval=15)
[ -n "$KEY" ] && SSH_OPTS+=(-i "$KEY")
remote() { ssh "${SSH_OPTS[@]}" "$SSH_USER@$HOST" "$@" < /dev/null; }

echo "→ $TARGET: connecting to $SSH_USER@$HOST:$PORT"
SITE_URL="$(remote 'wp option get home 2>/dev/null' | tr -d '\r')"
THEMES="$(remote 'wp theme path 2>/dev/null' | tr -d '\r')"
[ -n "$SITE_URL" ] && [ -n "$THEMES" ] || { echo "Connected, but WP-CLI did not answer (home='$SITE_URL' themes='$THEMES')." >&2; exit 1; }
if [ "$TARGET" = staging ] && [ "$SITE_URL" = "https://sixpackabs.com" ]; then
	echo "Refusing: the STAGING credentials point at the production site ($SITE_URL)." >&2
	exit 1
fi
echo "  site: $SITE_URL"
echo "  themes dir: $THEMES"
echo "  active theme: $(remote 'wp theme list --status=active --field=name 2>/dev/null' | tr -d '\r')"

if [ "$ACTION" = check ]; then
	remote 'wp core version; wp plugin list --status=active --field=name | tr "\n" " "; echo' | tr -d '\r'
	exit 0
fi

if [ "$ACTION" = rollback ]; then
	remote 'wp theme activate twentytwentyfive && wp rewrite flush'
	echo "  homepage: HTTP $(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL/?spa_cb=$RANDOM")"
	exit 0
fi

echo "→ uploading theme"
if remote 'command -v rsync >/dev/null'; then
	rsync -az --delete --exclude '.DS_Store' -e "ssh ${SSH_OPTS[*]}" "$THEME_SRC/" "$SSH_USER@$HOST:$THEMES/sixpackabs-child/"
else
	tar -C "$HERE/theme" --exclude '.DS_Store' -czf - sixpackabs-child \
		| ssh "${SSH_OPTS[@]}" "$SSH_USER@$HOST" "rm -rf '$THEMES/sixpackabs-child.new' && mkdir -p '$THEMES/sixpackabs-child.new' && tar -xzf - -C '$THEMES/sixpackabs-child.new' --strip-components=1 && rm -rf '$THEMES/sixpackabs-child' && mv '$THEMES/sixpackabs-child.new' '$THEMES/sixpackabs-child'"
fi

if [ "$UPLOAD_ONLY" = 1 ]; then
	echo "  uploaded; active theme left unchanged (--upload-only)"
	exit 0
fi

echo "→ activating + flushing rewrites + syncing"
remote 'wp theme activate sixpackabs-child && wp rewrite flush && wp spa sync'
echo "  homepage: HTTP $(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL/?spa_cb=$RANDOM")"
echo "  /videos/: HTTP $(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL/videos/?spa_cb=$RANDOM")"
echo "  /shorts/: HTTP $(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL/shorts/?spa_cb=$RANDOM")"
