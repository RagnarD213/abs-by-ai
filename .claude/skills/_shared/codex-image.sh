#!/bin/bash
# Image generation through Codex on Dan's ChatGPT subscription (no API bill).
# THE default image path for every skill and every session. Rule: _shared/IMAGE-GENERATION.md
#
# Usage:
#   codex-image.sh --prompt-file p.txt --out path/to/result.png [--image ref.jpg]... [--effort low|medium|high]
#
# --image may repeat (reference photos, a plate to edit). --out may end in .png or .jpg.
# Prints one JSON line on success. Exits non-zero with the reason if no image came back.
set -euo pipefail
CODEX="${CODEX_BIN:-/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex}"
PROMPT_FILE=""; OUT=""; EFFORT="low"; IMAGES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --prompt-file) PROMPT_FILE="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --image) IMAGES+=("$2"); shift 2;;
    --effort) EFFORT="$2"; shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done
[ -f "$PROMPT_FILE" ] && [ -n "$OUT" ] || { echo "need --prompt-file <file> and --out <path>" >&2; exit 2; }
[ -x "$CODEX" ] || { echo "Codex CLI not found at $CODEX (it ships inside ChatGPT.app)" >&2; exit 3; }

PROMPT="$(cat "$PROMPT_FILE")"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/codex-image.XXXXXX")"
ARGS=(); NAMES=""; n=0
for img in ${IMAGES[@]+"${IMAGES[@]}"}; do
  [ -f "$img" ] || { echo "image not found: $img" >&2; exit 2; }
  n=$((n+1)); ext="${img##*.}"; cp "$img" "$WORK/ref$n.$ext"; ARGS+=(-i "ref$n.$ext"); NAMES="$NAMES ref$n.$ext"
done
if [ $n -gt 0 ]; then LEAD="Use your built-in image generation tool with the attached image(s)$NAMES as input."
else LEAD="Use your built-in image generation tool."; fi

# The prompt goes in on stdin: a prompt placed after -i is swallowed as another image.
( cd "$WORK" && printf '%s Do not write code to draw or composite it. %s Save the result in the current directory as out.png. Reply with the saved path only.\n' "$LEAD" "$PROMPT" \
  | "$CODEX" exec --skip-git-repo-check -s workspace-write -c model_reasoning_effort="\"$EFFORT\"" ${ARGS[@]+"${ARGS[@]}"} - > log.txt 2>&1 ) || true

if [ ! -s "$WORK/out.png" ]; then
  echo "Codex returned no image. Last lines of its log:" >&2; tail -12 "$WORK/log.txt" >&2; exit 1
fi
mkdir -p "$(dirname "$OUT")"
case "$OUT" in
  *.jpg|*.jpeg) sips -s format jpeg -s formatOptions 95 "$WORK/out.png" --out "$OUT" >/dev/null;;
  *) cp "$WORK/out.png" "$OUT";;
esac
TOKENS="$(grep -A1 'tokens used' "$WORK/log.txt" | tail -1 | tr -d ', ')"
W="$(sips -g pixelWidth "$OUT" | awk '/pixelWidth/{print $2}')"; H="$(sips -g pixelHeight "$OUT" | awk '/pixelHeight/{print $2}')"
echo "{\"ok\":true,\"out\":\"$OUT\",\"width\":$W,\"height\":$H,\"codex_tokens\":${TOKENS:-0}}"
rm -rf "$WORK"
