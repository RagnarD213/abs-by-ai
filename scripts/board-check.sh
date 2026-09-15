#!/bin/sh
# Usage: scripts/board-check.sh [board-path] | scripts/board-check.sh --hook
set -eu
exec python3 "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/board-check.py" "$@"
