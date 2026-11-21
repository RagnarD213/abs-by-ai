#!/bin/bash
# Run a long render in the background and wait on it CORRECTLY.
#
#   ./render_wait.sh <expected_output.mp4> <timeout_seconds> <command...>
#
# Waits on the PROCESS, not on a filename (a filename can be renamed or written
# via a temp path, which is how a 20-hour phantom "still running" task happened
# on 2026-08-22). Always prints why it exited. Probes the artifact at the end.

OUT="$1"; shift
TIMEOUT="$1"; shift

"$@" & PID=$!
START=$SECONDS

while kill -0 "$PID" 2>/dev/null; do
  if (( SECONDS - START > TIMEOUT )); then
    kill "$PID" 2>/dev/null
    echo "TIMEOUT after ${TIMEOUT}s — killed pid $PID. Render did NOT complete."
    exit 2
  fi
  sleep 10
done

wait "$PID"; CODE=$?
if (( CODE != 0 )); then
  echo "RENDER FAILED (exit $CODE) after $((SECONDS-START))s"
  exit "$CODE"
fi

if [[ ! -f "$OUT" ]]; then
  echo "RENDER COMPLETE (exit 0) but expected output is missing: $OUT"
  echo "  -> the command wrote a different path. Find it before reporting success."
  exit 3
fi

# ffprobe is NOT always on PATH (this machine's ffmpeg is a bundled static build
# with no ffprobe beside it). Probe if we can; never fail delivery over a missing probe.
PROBE=$(command -v ffprobe || echo "")
SIZE=$(du -h "$OUT" | cut -f1)
if [[ -n "$PROBE" ]]; then
  DUR=$("$PROBE" -v error -show_entries format=duration -of csv=p=0 "$OUT")
  echo "RENDER COMPLETE in $((SECONDS-START))s"
  echo "  $OUT — ${SIZE}, ${DUR}s  — READY TO REVIEW"
else
  echo "RENDER COMPLETE in $((SECONDS-START))s"
  echo "  $OUT — ${SIZE} (no ffprobe on PATH; duration unverified) — READY TO REVIEW"
fi
