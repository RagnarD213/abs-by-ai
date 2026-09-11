#!/bin/zsh
# Verify a local folder has a true copy in Google Drive.
#
#   verify-drive-copy.sh <local-dir> <drive-folder-id>
#
# Compares every file by MD5 via `rclone check`. Exits non-zero if the copy
# is incomplete or any file differs. Counts and sizes are reported too, so a
# pass is auditable and not just a green checkmark.
#
# Requires: ~/bin/rclone with the `gdrive` remote authorized.

set -u
SRC="${1:?usage: verify-drive-copy.sh <local-dir> <drive-folder-id>}"
FID="${2:?usage: verify-drive-copy.sh <local-dir> <drive-folder-id>}"
RCLONE=~/bin/rclone

[[ -d "$SRC" ]] || { print -r -- "FAIL: local dir not found: $SRC"; exit 1; }

print -r -- "=== source ==="
print -r -- "$SRC"
LOCAL_N=$(find "$SRC" -type f ! -name '.DS_Store' | wc -l | tr -d ' ')
LOCAL_B=$(find "$SRC" -type f ! -name '.DS_Store' -print0 | xargs -0 stat -f%z | awk '{s+=$1} END{print s+0}')
print -r -- "local:  $LOCAL_N files, $LOCAL_B bytes"

REMOTE_N=$($RCLONE size gdrive: --drive-root-folder-id="$FID" --exclude '.DS_Store' --json 2>/dev/null | sed -n 's/.*"count":\([0-9]*\).*/\1/p')
REMOTE_B=$($RCLONE size gdrive: --drive-root-folder-id="$FID" --exclude '.DS_Store' --json 2>/dev/null | sed -n 's/.*"bytes":\([0-9]*\).*/\1/p')
print -r -- "drive:  ${REMOTE_N:-?} files, ${REMOTE_B:-?} bytes"

print -r -- "\n=== rclone check (MD5 per file) ==="
$RCLONE check "$SRC" gdrive: --drive-root-folder-id="$FID" --exclude '.DS_Store' --one-way 2>&1 | tail -20
RC=${pipestatus[1]}

print -r -- "\n=== verdict ==="
if [[ $RC -eq 0 && "$LOCAL_N" == "$REMOTE_N" && "$LOCAL_B" == "$REMOTE_B" ]]; then
  print -r -- "PASS — $LOCAL_N files, byte-identical, every file MD5-matched."
  exit 0
fi
print -r -- "FAIL — rclone check rc=$RC; local $LOCAL_N/$LOCAL_B vs drive ${REMOTE_N:-?}/${REMOTE_B:-?}"
print -r -- "Re-run the copy to fix; rclone only re-sends what is missing or differing."
exit 1
