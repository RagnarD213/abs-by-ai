#!/bin/zsh
# cap.sh name url maxH  (env W VH SC SCROLL passed through); retries the Chrome start race
for i in 1 2 3 4; do node "$(dirname $0)/shotw.mjs" "$@" >/dev/null 2>&1 && exit 0; sleep 2; done; echo "FAILED $1"; exit 1
