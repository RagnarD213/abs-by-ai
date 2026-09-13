#!/bin/bash
# Verify a local folder has a true copy in Google Drive.
#
#   verify-drive-copy.sh <local-dir> <drive-folder-id>
#
# Compares every file by MD5 via `rclone check`, plus file counts and total
# bytes. Exits 0 ONLY on a full pass; any mismatch, missing input, or failed
# check exits non-zero. A check that could not run is a FAILURE, never a pass.
#
# Requires: ~/bin/rclone with the `gdrive` remote authorized.

set -uo pipefail

SRC="${1:-}"
FID="${2:-}"
RCLONE="$HOME/bin/rclone"

if [[ -z "$SRC" || -z "$FID" ]]; then
  echo "usage: verify-drive-copy.sh <local-dir> <drive-folder-id>" >&2; exit 2
fi
[[ -d "$SRC" ]]      || { echo "FAIL: local dir not found: $SRC" >&2; exit 2; }
[[ -x "$RCLONE" ]]   || { echo "FAIL: rclone not found at $RCLONE" >&2; exit 2; }

echo "=== source ==="
echo "$SRC"
LOCAL_N=$(find "$SRC" -type f ! -name '.DS_Store' | wc -l | tr -d ' ')
LOCAL_B=$(find "$SRC" -type f ! -name '.DS_Store' -print0 | xargs -0 stat -f%z | awk '{s+=$1} END{printf "%d", s+0}')
echo "local:  $LOCAL_N files, $LOCAL_B bytes"

SIZE_JSON=$("$RCLONE" size gdrive: --drive-root-folder-id="$FID" --exclude '.DS_Store' --json 2>/dev/null)
REMOTE_N=$(echo "$SIZE_JSON" | sed -n 's/.*"count":[[:space:]]*\([0-9]*\).*/\1/p')
REMOTE_B=$(echo "$SIZE_JSON" | sed -n 's/.*"bytes":[[:space:]]*\([0-9]*\).*/\1/p')
echo "drive:  ${REMOTE_N:-UNKNOWN} files, ${REMOTE_B:-UNKNOWN} bytes"

if [[ -z "$REMOTE_N" || -z "$REMOTE_B" ]]; then
  echo -e "\n=== verdict ===\nFAIL — could not read the Drive folder's size. The check did not run." >&2
  exit 1
fi

echo ""
echo "=== rclone check (MD5 per file) ==="
CHECK_OUT=$("$RCLONE" check "$SRC" gdrive: --drive-root-folder-id="$FID" --exclude '.DS_Store' --one-way 2>&1)
CHECK_RC=$?
echo "$CHECK_OUT" | tail -20

echo ""
echo "=== verdict ==="
FAILED=0
[[ $CHECK_RC -eq 0 ]]            || { echo "  - rclone check exited $CHECK_RC"; FAILED=1; }
[[ "$LOCAL_N" == "$REMOTE_N" ]]  || { echo "  - file count differs: local $LOCAL_N vs drive $REMOTE_N"; FAILED=1; }
[[ "$LOCAL_B" == "$REMOTE_B" ]]  || { echo "  - total bytes differ: local $LOCAL_B vs drive $REMOTE_B"; FAILED=1; }
echo "$CHECK_OUT" | grep -q '0 differences found' || { echo "  - rclone did not report '0 differences found'"; FAILED=1; }

if [[ $FAILED -eq 0 ]]; then
  echo "PASS — $LOCAL_N files, $LOCAL_B bytes, every file MD5-matched, 0 differences."
  exit 0
fi
echo "FAIL — see the reasons above."
echo "Re-run the copy to fix; rclone only re-sends what is missing or differing."
exit 1
