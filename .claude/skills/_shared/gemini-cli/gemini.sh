#!/bin/zsh
# Hand one job to Gemini from the command line, on Dan's Google AI subscription.
# Works on the M6 and the M2. Uses Google's Antigravity CLI (`agy`), because the older
# `gemini` CLI is refused for personal Google accounts (UNSUPPORTED_CLIENT, 2026-11-17).
#
#   gemini.sh [-o OUT.txt] [-m MODEL] [-f FILE]... "prompt"
#
#   -o FILE   write the answer text here (default: print it on stdout)
#   -m MODEL  model id from `agy models` (default: whatever agy picks)
#   -f FILE   attach an image or video (png jpg gif webp mp4 mov webm avi ...); repeatable
#
# Exit codes: 0 ok | 2 bad usage | 3 quota / rate limit (wait or fall back, never switch to the paid key)
#             4 not signed in | 5 agy missing or API-key mode on | 1 any other failure
# The raw JSON envelope is saved beside OUT as OUT.json (or printed to stderr if no -o).

out=""; model=""; files=()
while getopts "o:m:f:" opt; do
  case $opt in
    o) out=$OPTARG ;;
    m) model=$OPTARG ;;
    f) files+=("$OPTARG") ;;
    *) echo "usage: gemini.sh [-o OUT] [-m MODEL] [-f FILE]... \"prompt\"" >&2; exit 2 ;;
  esac
done
shift $((OPTIND-1))
prompt="$*"
[[ -z "$prompt" ]] && { echo "gemini.sh: no prompt" >&2; exit 2; }

agy=""
for c in "$HOME/.local/bin/agy" "$(command -v agy 2>/dev/null)"; do
  [[ -n "$c" && -x "$c" ]] && { agy=$c; break; }
done
[[ -z "$agy" ]] && { echo "gemini.sh: agy not installed (see README.md)" >&2; exit 5; }

# Never run on the metered key: it must not be set, and agy must not be told to use it.
unset GEMINI_API_KEY GOOGLE_API_KEY GOOGLE_GEMINI_BASE_URL
if grep -qs '"modelProvider"[[:space:]]*:[[:space:]]*"gemini"' "$HOME/.gemini/antigravity-cli/settings.json"; then
  echo "gemini.sh: ~/.gemini/antigravity-cli/settings.json sets modelProvider=gemini (paid key mode). Remove it." >&2
  exit 5
fi

full="Answer directly in your reply. Do not create, edit or delete any file and do not write a plan or artifact. $prompt"
for f in "${files[@]}"; do
  [[ -f "$f" ]] || { echo "gemini.sh: missing file $f" >&2; exit 2; }
  full="$full @${f:A}"
done

args=(-p "$full" --output-format json)
[[ -n "$model" ]] && args+=(--model "$model")
for f in "${files[@]}"; do args+=(--add-dir "${f:A:h}"); done

tmp=$(mktemp -t geminish) || exit 1
errtmp=$(mktemp -t geminish-err) || exit 1
cd "${GEMINI_SH_CWD:-$HOME/Projects/Claude/Projects/Abs By AI}" 2>/dev/null || cd "$HOME"
"$agy" "${args[@]}" > "$tmp" 2> "$errtmp"
rc=$?

python3 - "$tmp" "$errtmp" "$out" "$rc" <<'PY'
import json, sys, re
tmp, errtmp, out, rc = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
raw = open(tmp, errors="replace").read()
err = open(errtmp, errors="replace").read()
env = None
for line in reversed(raw.strip().splitlines()):
    try:
        env = json.loads(line); break
    except Exception:
        continue
if out:
    open(out + ".json", "w").write(raw)
else:
    sys.stderr.write(raw[:2000] + "\n")
status = (env or {}).get("status", "")
text = (env or {}).get("response", "")
msg = ((env or {}).get("error") or "") + "\n" + err
low = msg.lower()
if env and status == "SUCCESS" and rc == 0:
    if out: open(out, "w").write(text)
    else: sys.stdout.write(text)
    sys.exit(0)
sys.stderr.write("gemini.sh: failed (status=%r rc=%d)\n%s\n" % (status, rc, msg.strip()[:1500]))
if re.search(r"quota|rate.?limit|resource.?exhausted|429|credits", low): sys.exit(3)
if re.search(r"auth|sign.?in|login|credential|unauthenticated", low): sys.exit(4)
sys.exit(1)
PY
code=$?
rm -f "$tmp" "$errtmp"
exit $code
